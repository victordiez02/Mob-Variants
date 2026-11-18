"""Helpers to load Bedrock JSON (with comments / trailing commas) and index packs."""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
VAN = os.path.join(ROOT, "vanilla")


def find_pack(kind):
    for name in os.listdir(ROOT):
        p = os.path.join(ROOT, name)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "manifest.json")):
            if kind == "RP" and ("[RP]" in name or name == "RP"):
                return p
            if kind == "BP" and ("[BP]" in name or name == "BP"):
                return p
    raise SystemExit("pack not found " + kind)


def strip_comments(s):
    out, i, n, in_str = [], 0, len(s), False
    while i < n:
        c = s[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(s[i + 1]); i += 2; continue
            if c == '"':
                in_str = False
            i += 1; continue
        if c == '"':
            in_str = True; out.append(c); i += 1; continue
        if s.startswith("//", i):
            j = s.find("\n", i); i = n if j < 0 else j; continue
        if s.startswith("/*", i):
            j = s.find("*/", i + 2); i = n if j < 0 else j + 2; continue
        out.append(c); i += 1
    t = "".join(out)
    t = re.sub(r",(\s*[}\]])", r"\1", t)
    return t


def load(path):
    with open(path, encoding="utf-8-sig") as f:
        raw = f.read()
    try:
        return json.loads(raw), False
    except Exception:
        return json.loads(strip_comments(raw)), True


def files(base, sub, pattern="**/*.json"):
    return glob.glob(os.path.join(glob.escape(base), sub, pattern), recursive=True)


def geo_ids(base):
    ids = {}
    for f in files(base, "models"):
        try:
            d, _ = load(f)
        except Exception as e:
            print("PARSE", f, e); continue
        for k, v in d.items():
            if k == "minecraft:geometry":
                for g in v:
                    ids[g["description"]["identifier"]] = f
            elif k.startswith("geometry."):
                ids[k.split(":")[0]] = f
    return ids


def keyed_ids(base, sub, key):
    ids = {}
    for f in files(base, sub):
        try:
            d, _ = load(f)
        except Exception as e:
            print("PARSE", f, e); continue
        for k in (d.get(key) or {}):
            ids[k] = f
    return ids


def texture_exists(base, path):
    for ext in (".png", ".tga", ".jpg", ".jpeg", ".texture_set.json"):
        if os.path.exists(os.path.join(base, path + ext)):
            return True
    return False


def _inline(v):
    return isinstance(v, list) and all(not isinstance(x, (dict, list)) for x in v) and len(json.dumps(v)) <= 100 \
        or isinstance(v, dict) and len(v) <= 2 and all(not isinstance(x, (dict, list)) for x in v.values()) and len(json.dumps(v)) <= 60


def to_json(o, ind=0, step=2):
    sp, sp2 = " " * ind, " " * (ind + step)
    if isinstance(o, dict):
        if not o: return "{}"
        if _inline(o): return "{ " + ", ".join(f"{json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}" for k, v in o.items()) + " }"
        return "{\n" + ",\n".join(f"{sp2}{json.dumps(k, ensure_ascii=False)}: {to_json(v, ind + step)}" for k, v in o.items()) + f"\n{sp}}}"
    if isinstance(o, list):
        if not o: return "[]"
        if _inline(o): return "[" + ", ".join(json.dumps(x, ensure_ascii=False) for x in o) + "]"
        return "[\n" + ",\n".join(f"{sp2}{to_json(v, ind + step)}" for v in o) + f"\n{sp}]"
    return json.dumps(o, ensure_ascii=False)


def save(path, obj, header=None):
    import time
    text = (header.rstrip() + "\n" if header else "") + to_json(obj) + "\n"
    for _ in range(40):  # the editor sometimes locks files for a moment on Windows
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            return
        except OSError:
            time.sleep(0.25)
    raise OSError("could not write " + path)
