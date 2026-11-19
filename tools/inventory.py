"""Inventory of every mob of the add-on, written to docs/mobs/<mob>.md (only between the auto markers).

    python tools/inventory.py [mob ...] [--quiet]

Per client entity of RP/: vanilla entity it is built on, gate (v.mv_active), skins in the order of
mv:variant with their BP weight, extra skin arrays (angry, charging, saddled), coverage check of each
skin on the vanilla geometry (vanilla bones painted in the vanilla texture but < 60 % in the skin: they
would show holes, e.g. crossed arms of illagers), BP events that roll mv:variant, and the files of the mob.
Writes the section between `<!-- inventory:start -->` and `<!-- inventory:end -->` of docs/mobs/<mob>.md
(creates the file if needed; the rest of the file is hand-written and kept) and the table of
docs/mobs/README.md. Prints the skins with coverage problems. Needs Pillow for the coverage check.
"""
from __future__ import annotations

import os
import re
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import (ROOT, VRP, Json, cube_faces, files, find_pack, geo_index, load, rc_list, rel, texture_file,  # noqa: E402
                   vanilla_client_entity)

DOCS = os.path.join(ROOT, "docs", "mobs")
START, END = "<!-- inventory:start -->", "<!-- inventory:end -->"
STATE_ARRAYS = {"array.mv_angry": "enfadada", "array.mv_charging": "disparando", "array.mv_saddled": "con silla"}

try:
    from PIL import Image
except ImportError:  # coverage check skipped
    Image = None  # type: ignore[assignment]


def coverage(path: str, geo: Any, vpath: str | None) -> list[str]:
    """Vanilla bones fully painted in the vanilla texture but < 60 % painted in `path`."""
    if Image is None or not path.endswith(".png"):
        return []
    im = Image.open(path).convert("RGBA")
    tw, th = geo.desc.get("texture_width", 64), geo.desc.get("texture_height", 64)
    if abs(im.width / im.height - tw / th) > 1e-3:
        return [f"tamaño {im.width}x{im.height} no encaja con el UV {tw}x{th}"]
    vim = Image.open(vpath).convert("RGBA") if vpath and vpath.endswith(".png") else None

    def cov(img: Any, b: Json) -> float | None:
        sx, sy = img.width / tw, img.height / th
        n = t = 0
        for c in b.get("cubes", []):
            for (u, v, w, h) in cube_faces(c).values():
                for x in range(int(min(u, u + w) * sx), int(max(u, u + w) * sx)):
                    for y in range(int(min(v, v + h) * sy), int(max(v, v + h) * sy)):
                        t += 1
                        n += 0 <= x < img.width and 0 <= y < img.height and img.getpixel((x, y))[3] > 0
        return n / t if t else None

    out = []
    for b in geo.bones:
        if b.get("cubes") and all("inflate" in c for c in b["cubes"]):
            continue  # outer layers (hat, jacket…): may be left empty
        o = cov(im, b)
        v = cov(vim, b) if vim else 1.0
        if o is not None and v and v > 0.9 and o < 0.6:
            out.append(f"{b['name']} {o:.0%}")
    return out


def variant_rolls(node: Json, path: str, out: dict[str, list[tuple[int, float]]]) -> None:
    if isinstance(node, dict):
        rnd = node.get("randomize")
        if isinstance(rnd, list) and any("mv:variant" in (o.get("set_property") or {}) for o in rnd):
            out[path] = [(int(o["set_property"]["mv:variant"]), float(o.get("weight", 1))) for o in rnd
                         if "mv:variant" in (o.get("set_property") or {})]
        for k, v in node.items():
            variant_rolls(v, path if k in ("sequence", "randomize") or path else k, out)
    elif isinstance(node, list):
        for v in node:
            variant_rolls(v, path, out)


def mob_section(f: str, rp: str, bp: str, gi: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    d = load(f)["minecraft:client_entity"]["description"]
    name = os.path.basename(f).split(".")[0]
    ident = d["identifier"]
    van = vanilla_client_entity(ident)
    vdesc = van[1]["minecraft:client_entity"]["description"] if van else {}
    rcs: dict[str, Json] = {}
    rc_files: dict[str, str] = {}
    for rf in files(rp, "render_controllers"):
        for k, v in load(rf)["render_controllers"].items():
            rcs[k], rc_files[k] = v, rf
    own = [(n, c) for n, c in rc_list(d) if n.startswith("controller.render.mv.")]
    pre = (d.get("scripts") or {}).get("pre_animation") or []
    gate = next((x for x in pre if x.startswith("v.mv_active")), "(sin puerta: siempre)")
    textures = {k.lower(): v for k, v in (d.get("textures") or {}).items()}
    geometry = (d.get("geometry") or {})
    bpf = next((x for x in files(bp, "entities") if load(x)["minecraft:entity"]["description"]["identifier"] == ident), None)
    rolls: dict[str, list[tuple[int, float]]] = {}
    prop = None
    if bpf:
        e = load(bpf)["minecraft:entity"]
        prop = ((e["description"].get("properties") or {}).get("mv:variant") or {}).get("range")
        variant_rolls(e.get("events") or {}, "", rolls)
    weights = dict(next(iter(rolls.values()), []))
    total = sum(weights.values()) or 1.0
    lines = [START, "", "## Estado actual (generado por `tools/inventory.py`, no editar a mano)", "",
             f"- Entidad: `{rel(f)}` sobre la vanilla `{os.path.basename(van[0]) if van else '?'}`",
             f"- Puerta: `{gate}`"]
    for n, c in own:
        lines.append(f"- Render controller: `{n}` ({rel(rc_files[n]) if n in rc_files else 'NO DEFINIDO'})"
                     + (f" con condición `{c}`" if c else ""))
    lines.append(f"- BP: `{rel(bpf)}`, `mv:variant` {prop}, sorteo en: {', '.join(sorted(rolls)) or '—'}" if bpf
                 else "- BP: no tiene")
    problems: list[str] = []
    skins_n = 0
    for n, _ in own:
        rc = rcs.get(n) or {}
        arrays = ((rc.get("arrays") or {}).get("textures") or {})
        gkeys = [k for k in re.findall(r"Geometry\.(\w+)", str(rc.get("geometry", ""))) if "baby" not in k.lower()]
        geo_id = geometry.get(gkeys[0] if gkeys else "default")
        geo = gi.get(geo_id) if geo_id else None
        vt = vdesc.get("textures", {})
        vtex = texture_file(vt.get("default") or next(iter(vt.values()), ""), [VRP]) if vt else None
        for an, items in arrays.items():
            label = STATE_ARRAYS.get(an, "skins")
            lines += ["", f"### `{an}` ({label}, {len(items)})", "",
                      "| `mv:variant` | Clave | Textura | Peso BP | Revisar |", "|---|---|---|---|---|"]
            for i, t in enumerate(items, 1):
                k = t.split(".", 1)[1]
                path = textures.get(k.lower(), "?")
                tf = texture_file(path, [rp, VRP])
                cv = coverage(tf, geo, vtex) if tf and geo is not None and label in ("skins", "con silla") else []
                if cv:
                    problems.append(f"{name}: {os.path.basename(path)} {', '.join(cv)}")
                w = weights.get(i)
                wtxt = f"{w:g} ({w / total:.1%})" if w is not None else "—"
                src = "vanilla" if tf and os.path.abspath(tf).startswith(os.path.abspath(VRP)) else "pack"
                lines.append(f"| {i} | `{k}` | `{path}` ({src}) | {wtxt} | {', '.join(cv)} |")
            if label == "skins":
                skins_n = max(skins_n, len(items))
    lines += ["", END]
    return "\n".join(lines), {"name": name, "skins": skins_n, "bp": bool(bpf), "problems": problems}


def write(path: str, section: str, title: str) -> None:
    if os.path.exists(path):
        text = open(path, encoding="utf-8").read()
        if START in text and END in text:
            text = text[:text.index(START)] + section + text[text.index(END) + len(END):]
        else:
            text = text.rstrip() + "\n\n" + section + "\n"
    else:
        text = f"# {title}\n\n{section}\n"
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    quiet = "--quiet" in sys.argv
    rp, bp = find_pack("RP"), find_pack("BP")
    gi = geo_index(VRP)
    os.makedirs(DOCS, exist_ok=True)
    summary = []
    for f in files(rp, "entity"):
        name = os.path.basename(f).split(".")[0]
        section, info = mob_section(f, rp, bp, gi)
        summary.append(info)
        if args and name not in args:
            continue
        write(os.path.join(DOCS, f"{name}.md"), section, name)
        for p in info["problems"]:
            print("coverage:", p)
    # index
    with_entity = {s["name"] for s in summary}
    legacy_only = sorted(os.path.basename(x)[:-3] for x in os.listdir(DOCS)
                         if x.endswith(".md") and x != "README.md" and x[:-3] not in with_entity)
    rows = ["| Mob | Skins | BP | Skins a revisar |", "|---|---|---|---|"]
    rows += [f"| [{s['name']}]({s['name']}.md) | {s['skins']} | {'sí' if s['bp'] else 'no'} | {len(s['problems']) or ''} |"
             for s in sorted(summary, key=lambda s: s["name"])]
    if legacy_only:
        rows += ["", "Sin entidad en el pack (vanilla puro de momento; ver su md): "
                 + ", ".join(f"[{n}]({n}.md)" for n in legacy_only) + "."]
    write(os.path.join(DOCS, "README.md"), START + "\n\n" + "\n".join(rows) + "\n\n" + END, "Mobs")
    if not quiet:
        print(f"{len(summary)} mobs -> {rel(DOCS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
