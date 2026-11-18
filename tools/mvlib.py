"""Shared helpers: paths, Bedrock JSON (comments / trailing commas), pack indexes and geometry.

Every tool imports this module. Nothing here writes files except `save()`.
"""
from __future__ import annotations

import copy
import glob
import json
import os
import re
import struct
import sys
import time
from typing import Any

Json = Any  # parsed JSON value (dict / list / str / float / bool / None)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
VAN = os.path.join(ROOT, "vanilla")
VRP = os.path.join(VAN, "resource_pack")
VBP = os.path.join(VAN, "behavior_pack")

# Windows consoles default to cp1252; tools print paths and names with any character.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except AttributeError:
        pass


def find_pack(kind: str) -> str:
    """Path of the add-on pack `kind` ("RP" or "BP") in the repo root."""
    for name in os.listdir(ROOT):
        p = os.path.join(ROOT, name)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "manifest.json")):
            if name == kind or f"[{kind}]" in name:
                return p
    raise SystemExit(f"pack not found: {kind}")


def require_vanilla() -> None:
    if not os.path.isdir(VRP) or not os.path.isdir(VBP):
        raise SystemExit("vanilla/ not found: see 'Plantilla vanilla' in CLAUDE.md")


# ---------------------------------------------------------------- JSON


def strip_comments(s: str) -> str:
    """Remove // and /* */ comments (outside strings) and trailing commas."""
    out: list[str] = []
    i, n, in_str = 0, len(s), False
    while i < n:
        c = s[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(s[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
        elif s.startswith("//", i):
            j = s.find("\n", i)
            i = n if j < 0 else j
            continue
        elif s.startswith("/*", i):
            j = s.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        out.append(c)
        i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def load_ex(path: str) -> tuple[Json, bool]:
    """(data, had_comments_or_trailing_commas)."""
    with open(path, encoding="utf-8-sig") as f:
        raw = f.read()
    try:
        return json.loads(raw), False
    except json.JSONDecodeError:
        return json.loads(strip_comments(raw)), True


def load(path: str) -> Json:
    return load_ex(path)[0]


def load_for_edit(path: str) -> tuple[Json, str | None]:
    """(data, header) for files that will be re-saved with save(path, data, header).

    The header is the block of leading `//` lines. Comments anywhere else would be lost: refuse them.
    """
    with open(path, encoding="utf-8-sig") as f:
        lines = f.read().split("\n")
    head: list[str] = []
    while lines and lines[0].lstrip().startswith("//"):
        head.append(lines.pop(0).rstrip("\r"))
    try:
        data = json.loads("\n".join(lines))
    except json.JSONDecodeError as e:
        raise SystemExit(f"{rel(path)}: comments or trailing commas inside the JSON; edit it by hand ({e})") from e
    return data, "\n".join(head) or None


def files(base: str, sub: str, pattern: str = "**/*.json") -> list[str]:
    return sorted(glob.glob(os.path.join(glob.escape(base), sub, pattern), recursive=True))


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT).replace("\\", "/")


def _inline(v: Json) -> bool:
    if isinstance(v, list):
        return all(not isinstance(x, (dict, list)) for x in v) and len(json.dumps(v)) <= 100
    if isinstance(v, dict):
        return len(v) <= 2 and all(not isinstance(x, (dict, list)) for x in v.values()) and len(json.dumps(v)) <= 60
    return False


def to_json(o: Json, ind: int = 0, step: int = 2) -> str:
    """JSON with short lists/objects on one line (the style used in the packs)."""
    sp, sp2 = " " * ind, " " * (ind + step)
    dump = lambda x: json.dumps(x, ensure_ascii=False)  # noqa: E731
    if isinstance(o, dict):
        if not o:
            return "{}"
        if _inline(o):
            return "{ " + ", ".join(f"{dump(k)}: {dump(v)}" for k, v in o.items()) + " }"
        body = ",\n".join(f"{sp2}{dump(k)}: {to_json(v, ind + step)}" for k, v in o.items())
        return "{\n" + body + f"\n{sp}}}"
    if isinstance(o, list):
        if not o:
            return "[]"
        if _inline(o):
            return "[" + ", ".join(dump(x) for x in o) + "]"
        return "[\n" + ",\n".join(f"{sp2}{to_json(v, ind + step)}" for v in o) + f"\n{sp}]"
    return dump(o)


def save(path: str, obj: Json, header: str | None = None) -> None:
    """Write JSON (optionally preceded by `//` comment lines); retries if the editor locks the file."""
    text = (header.rstrip() + "\n" if header else "") + to_json(obj) + "\n"
    for _ in range(40):
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            return
        except OSError:
            time.sleep(0.25)
    raise OSError("could not write " + path)


# ---------------------------------------------------------------- pack indexes


def keyed_ids(base: str, sub: str, key: str) -> dict[str, str]:
    """{id: file} for files whose top-level `key` is a dict of ids (animations, render controllers…)."""
    ids: dict[str, str] = {}
    for f in files(base, sub):
        try:
            d = load(f)
        except (OSError, ValueError) as e:
            print("PARSE", rel(f), e)
            continue
        for k in d.get(key) or {}:
            ids[k] = f
    return ids


def texture_file(path: str, bases: list[str]) -> str | None:
    for base in bases:
        for ext in (".png", ".tga", ".jpg", ".jpeg", ".texture_set.json"):
            p = os.path.join(base, path + ext)
            if os.path.exists(p):
                return p
    return None


def png_size(path: str) -> tuple[int, int] | None:
    """(width, height) of a PNG without Pillow; None for other formats."""
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]):  # PNG signature
        return None
    w, h = struct.unpack(">II", head[16:24])
    return int(w), int(h)


def client_entities(base: str) -> dict[str, tuple[str, Json]]:
    """{file: (identifier, description)} of the client entities of a resource pack."""
    out: dict[str, tuple[str, Json]] = {}
    for f in files(base, "entity"):
        desc = load(f)["minecraft:client_entity"]["description"]
        out[f] = (desc["identifier"], desc)
    return out


def _ver(s: Any) -> tuple[int, ...]:
    try:
        return tuple(int(x) for x in str(s).split("."))
    except ValueError:
        return (0,)


def vanilla_client_entity(ident: str) -> tuple[str, Json] | None:
    """Current vanilla client entity for `ident`: highest min_engine_version, ignoring *.v1.0 files."""
    best: tuple[tuple[int, ...], str, Json] | None = None
    for f in files(VRP, "entity"):
        d = load(f)
        desc = d["minecraft:client_entity"]["description"]
        if desc["identifier"] != ident:
            continue
        key = _ver(desc.get("min_engine_version", "0"))
        if ".v1.0." in os.path.basename(f):
            key = (-1,) + key
        if best is None or key > best[0]:
            best = (key, f, d)
    return (best[1], best[2]) if best else None


def vanilla_behavior_entity(ident: str) -> tuple[str, Json] | None:
    for f in files(VBP, "entities"):
        d = load(f)
        if d.get("minecraft:entity", {}).get("description", {}).get("identifier") == ident:
            return f, d
    return None


def rc_list(desc: Json) -> list[tuple[str, str | None]]:
    """Entity render_controllers as [(name, condition or None)]."""
    out: list[tuple[str, str | None]] = []
    for r in desc.get("render_controllers") or []:
        if isinstance(r, str):
            out.append((r, None))
        else:
            name, cond = next(iter(r.items()))
            out.append((name, cond))
    return out


# ---------------------------------------------------------------- geometry

_DESC_MAP = ("texture_width", "texture_height", "visible_bounds_width", "visible_bounds_height", "visible_bounds_offset")
_OLD_DESC = {"texturewidth": "texture_width", "textureheight": "texture_height"}


class Geo:
    """One geometry definition (1.8 or 1.12+ format)."""

    def __init__(self, ident: str, file: str, parent: str | None, desc: dict[str, Any], bones: list[dict[str, Any]], fmt: str):
        self.ident, self.file, self.parent, self.desc, self.bones, self.fmt = ident, file, parent, desc, bones, fmt


def parse_geo_file(path: str) -> list[Geo]:
    d = load(path)
    out: list[Geo] = []
    fmt = str(d.get("format_version", "1.8.0"))
    for g in d.get("minecraft:geometry", []):
        desc = dict(g["description"])
        ident = desc.pop("identifier")
        out.append(Geo(ident, path, None, desc, g.get("bones", []), fmt))
    for k, v in d.items():
        if not k.startswith("geometry."):
            continue
        ident, _, parent = k.partition(":")
        desc = {_OLD_DESC.get(str(x), str(x)): v[x] for x in v if _OLD_DESC.get(str(x), str(x)) in _DESC_MAP}
        out.append(Geo(ident, path, parent or None, desc, v.get("bones", []), fmt))
    return out


def geo_index(base: str) -> dict[str, Geo]:
    idx: dict[str, Geo] = {}
    for f in files(base, "models"):
        try:
            for g in parse_geo_file(f):
                idx[g.ident] = g
        except (OSError, ValueError, KeyError) as e:
            print("PARSE", rel(f), e)
    return idx


def resolve_geo(ident: str, *indexes: dict[str, Geo]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """(description, bones) with 1.8 inheritance (`geometry.a:geometry.b`) applied."""
    g = next((i[ident] for i in indexes if ident in i), None)
    if g is None:
        raise KeyError(ident)
    desc, bones = dict(g.desc), copy.deepcopy(g.bones)
    if g.parent:
        pdesc, pbones = resolve_geo(g.parent, *indexes)
        merged = {b["name"]: b for b in pbones}
        order = [b["name"] for b in pbones]
        for b in bones:
            if b["name"] not in merged:
                order.append(b["name"])
            merged[b["name"]] = b
        bones = [merged[n] for n in order]
        desc = {**pdesc, **desc}
    return desc, bones


Rect = tuple[float, float, float, float]  # u, v, width, height (always positive)


def cube_faces(c: dict[str, Any]) -> dict[str, Rect]:
    """UV rectangle of each face of a cube (box UV or per-face UV)."""
    u = c.get("uv", [0, 0])
    w, h, d = (abs(float(x)) for x in c["size"])
    if isinstance(u, dict):
        out: dict[str, Rect] = {}
        for k, f in u.items():
            (x, y), (sw, sh) = f["uv"], f.get("uv_size", [0, 0])
            out[k] = (min(x, x + sw), min(y, y + sh), abs(sw), abs(sh))
        return out
    x, y = float(u[0]), float(u[1])
    return {"up": (x + d, y, w, d), "down": (x + d + w, y, w, d), "east": (x, y + d, d, h),
            "north": (x + d, y + d, w, h), "west": (x + d + w, y + d, d, h), "south": (x + 2 * d + w, y + d, w, h)}


def rect_inside(r: Rect, outer: Rect, eps: float = 1e-6) -> bool:
    return (r[0] >= outer[0] - eps and r[1] >= outer[1] - eps
            and r[0] + r[2] <= outer[0] + outer[2] + eps and r[1] + r[3] <= outer[1] + outer[3] + eps)
