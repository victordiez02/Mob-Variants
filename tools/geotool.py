"""Geometry tools for moving skins from re-rigged models to vanilla models + layers.

    python -I tools/geotool.py fit
        For every entity whose mv_default is an add-on model: % of its UV faces inside each vanilla
        model's UV of that mob (do the skins fit the vanilla model?).
    python -I tools/geotool.py faces <addon geo> <vanilla geo> [addonBone=vanillaBone ...]
        The same, face by face, listing the faces that fall outside.
    python tools/geotool.py limbmerge <addon geo> <vanilla geo> <texture without extension> ...
        Repaint split limbs (upper + knee, box UV) into the single vanilla limb layout.
        MODIFIES the textures (commit first). Needs Pillow.

As a module: build_overlay(src_bones, plan, ident, desc) builds a layer geometry from bones of an old
model hung from vanilla-named bones (used for witch, spider, pig; see git log).
"""
from __future__ import annotations

import copy
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import (VRP, Geo, Json, Rect, client_entities, cube_faces, find_pack, geo_index, rect_inside,  # noqa: E402
                   resolve_geo)

Bone = dict[str, Any]


def _bones(ident: str, *idx: dict[str, Geo]) -> list[Bone]:
    return resolve_geo(ident, *idx)[1]


def face_rects(bones: list[Bone]) -> dict[str, list[Rect]]:
    out: dict[str, list[Rect]] = {}
    for b in bones:
        for c in b.get("cubes", []):
            out.setdefault(b["name"], []).extend(cube_faces(c).values())
    return out


def fit() -> None:
    rp = find_pack("RP")
    A, V = geo_index(rp), geo_index(VRP)
    cands: dict[str, set[str]] = {}
    for _, (ident, d) in client_entities(VRP).items():
        for k, g in (d.get("geometry") or {}).items():
            if "baby" not in k and g in V:
                cands.setdefault(ident, set()).add(g)
    for f, (ident, d) in client_entities(rp).items():
        a = (d.get("geometry") or {}).get("mv_default")
        if not a or a not in A:
            continue
        print(f"## {os.path.basename(f)} {a} [{A[a].desc.get('texture_width')}x{A[a].desc.get('texture_height')}]")
        abones = _bones(a, A, V)
        for vid in sorted(cands.get(ident, [])):
            vf = [r for rs in face_rects(_bones(vid, V)).values() for r in rs]
            tot = ok = 0
            outside: set[str] = set()
            for b in abones:
                for c in b.get("cubes", []):
                    for r in cube_faces(c).values():
                        if not r[2] or not r[3]:
                            continue
                        tot += 1
                        if any(rect_inside(r, R) for R in vf):
                            ok += 1
                        else:
                            outside.add(b["name"])
            vd = V[vid].desc
            print(f"   {vid:34} [{vd.get('texture_width')}x{vd.get('texture_height')}] {ok / max(tot, 1):.0%}"
                  f"  outside bones: {sorted(outside)}")


def faces(a: str, v: str, mapping: dict[str, str]) -> None:
    rp = find_pack("RP")
    A, V = geo_index(rp), geo_index(VRP)
    vf = face_rects(_bones(v, V))
    ok, bad, extra = 0, [], set()
    for b in _bones(a, A, V):
        target = mapping.get(b["name"], b["name"])
        for c in b.get("cubes", []):
            for k, r in cube_faces(c).items():
                if r[2] == 0 or r[3] == 0:
                    continue
                if target not in vf:
                    extra.add(b["name"])
                elif any(rect_inside(r, R) for R in vf[target]):
                    ok += 1
                else:
                    bad.append((b["name"], k, r))
    print(f"{a}: faces inside vanilla={ok} outside={len(bad)} bones not in vanilla={sorted(extra)}")
    for x in bad[:20]:
        print("   outside:", x)


def limb_pairs(addon_id: str, vanilla_id: str) -> list[tuple[str, str, list[float], list[float], tuple[int, int, int, int]]]:
    rp = find_pack("RP")
    A, V = geo_index(rp), geo_index(VRP)
    ab = {b["name"]: b for b in _bones(addon_id, A, V)}
    vcubes = [c for b in _bones(vanilla_id, V) for c in b.get("cubes", []) if isinstance(c.get("uv"), list)]
    out = []
    for b in ab.values():
        if not b.get("cubes"):
            continue
        for k in (k for k in ab.values() if k.get("parent") == b["name"] and k.get("cubes")):
            up, lo = b["cubes"][0], k["cubes"][0]
            if not (isinstance(up.get("uv"), list) and isinstance(lo.get("uv"), list)):
                continue
            w, h1, d = up["size"]
            w2, h2, d2 = lo["size"]
            if (w, d) != (w2, d2):
                continue
            if any(list(c["uv"]) == list(up["uv"]) and c["size"] == [w, h1 + h2, d] for c in vcubes):
                out.append((b["name"], k["name"], up["uv"], lo["uv"], (int(w), int(h1), int(h2), int(d))))
    return out


def limbmerge(addon_id: str, vanilla_id: str, textures: list[str]) -> None:
    from PIL import Image
    pl = limb_pairs(addon_id, vanilla_id)
    print("limbs:", [(a, b) for a, b, *_ in pl])
    rp = find_pack("RP")
    for t in textures:
        p = os.path.join(rp, t + ".png")
        img = Image.open(p).convert("RGBA")
        src = img.copy()
        for _, _, (u, v), (u2, v2), (w, h1, h2, d) in pl:
            u, v, u2, v2 = int(u), int(v), int(u2), int(v2)
            img.paste(src.crop((u2, v2 + d, u2 + 2 * d + 2 * w, v2 + d + h2)), (u, v + d + h1))  # sides below
            img.paste(src.crop((u2 + d + w, v2, u2 + d + 2 * w, v2 + d)), (u + d + w, v))          # bottom face
        img.save(p)
        print("repainted", t)


def build_overlay(src_bones: list[Bone], plan: dict[str, Json], ident: str, desc: dict[str, Any],
                  rename: dict[str, str] | None = None, offset: tuple[float, float, float] = (0, 0, 0),
                  skip: set[str] | None = None) -> Json:
    """plan: {vanilla_bone: {"pivot": [...], "parent": str?, "cubes_from": [(addon_bone, [cube idx])],
    "children": [addon_bone, ...]}}. Children are copied with their subtree, renamed mv_<name>."""
    by = {b["name"]: b for b in src_bones}
    rename = rename or {}
    skip = skip or set()

    def sh(p: list[float]) -> list[float]:
        return [round(p[i] + offset[i], 4) for i in range(3)]

    def mv(c: Json) -> Json:
        c = copy.deepcopy(c)
        c["origin"] = sh(c["origin"])
        if "pivot" in c:
            c["pivot"] = sh(c["pivot"])
        return c

    out: list[Bone] = []

    def add_subtree(name: str, parent: str) -> None:
        b = by[name]
        nb: Bone = {"name": rename.get(name, "mv_" + name), "parent": parent}
        if "pivot" in b:
            nb["pivot"] = sh(b["pivot"])
        for k in ("rotation", "mirror", "inflate"):
            if k in b:
                nb[k] = b[k]
        if b.get("cubes"):
            nb["cubes"] = [mv(c) for c in b["cubes"]]
        out.append(nb)
        for c in src_bones:
            if c.get("parent") == name and c["name"] not in skip:
                add_subtree(c["name"], nb["name"])

    for vb, spec in plan.items():
        b: Bone = {"name": vb, "pivot": spec["pivot"]}
        if spec.get("parent"):
            b["parent"] = spec["parent"]
        cubes = [mv(by[ab]["cubes"][i]) for ab, idx in spec.get("cubes_from", []) for i in idx]
        if cubes:
            b["cubes"] = cubes
        out.append(b)
        for ch in spec.get("children", []):
            add_subtree(ch, vb)
    return {"format_version": "1.12.0", "minecraft:geometry": [{"description": {"identifier": ident, **desc}, "bones": out}]}


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    cmd, rest = args[0], args[1:]
    if cmd == "fit":
        fit()
    elif cmd == "faces" and len(rest) >= 2:
        faces(rest[0], rest[1], dict(m.split("=", 1) for m in rest[2:]))
    elif cmd == "limbmerge" and len(rest) >= 3:
        limbmerge(rest[0], rest[1], rest[2:])
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
