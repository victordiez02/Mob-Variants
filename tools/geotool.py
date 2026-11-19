"""Geometry tools for moving skins from re-rigged models to vanilla models + layers.

    python -I tools/geotool.py fit
        For every entity whose mv_default is an add-on model: % of its UV faces inside each vanilla
        model's UV of that mob (do the skins fit the vanilla model?).
    python -I tools/geotool.py faces <addon geo> <vanilla geo> [addonBone=vanillaBone ...]
        The same, face by face, listing the faces that fall outside.
    python tools/geotool.py limbmerge <addon geo> <vanilla geo> <texture without extension> ...
        Repaint split limbs (upper + knee, box UV) into the single vanilla limb layout.
        MODIFIES the textures (commit first). Needs Pillow.
    python tools/geotool.py relayer <layer geo> <base geo> [--write]
        Rule 2 on an existing layer: vanilla-named bones get the base pivot/parent/rotation (cubes move to
        an mv_<bone> child if needed), missing vanilla ancestors are added empty, other bones get mv_ (same
        parent). Refuses if the rest pose changes. Needs Pillow.

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


def _world(bones: list[Bone]) -> dict[str, list[list[float]]]:
    """Rest matrix of every bone (rotations about pivots, inherited from parents). Needs render.py (Pillow)."""
    from render import about, bb, mat_mul, rot_bb, translate
    by = {b["name"].lower(): b for b in bones}
    out: dict[str, list[list[float]]] = {}

    def m(n: str, depth: int = 0) -> list[list[float]]:
        if n not in out:
            b = by[n]
            p = (b.get("parent") or "").lower()
            pm = m(p, depth + 1) if p in by and depth < 64 else translate(0, 0, 0)
            rot = [float(x) for x in b.get("rotation", [0, 0, 0])]
            out[n] = mat_mul(pm, about(bb(b.get("pivot", [0, 0, 0])), rot_bb(*rot)))
        return out[n]
    for n in by:
        m(n)
    return out


def relayer(layer_id: str, base_id: str, write: bool) -> int:
    """Rule 2 for an existing layer: vanilla-named bones get the base pivot, parent and rotation (and the
    missing vanilla ancestors are added, empty); their cubes move to an `mv_<name>` child when needed so
    that nothing moves at rest; other bones get the `mv_` prefix and hang from their nearest vanilla-named
    ancestor. Refuses if the rest pose would change."""
    from mvlib import load_for_edit, save
    geos_a, geos_v = geo_index(find_pack("RP")), geo_index(VRP)
    g = geos_a[layer_id]
    if g.parent:
        print(f"{layer_id}: 1.8 inheritance not supported")
        return 1
    _, base = resolve_geo(base_id, geos_a, geos_v)
    vb = {b["name"].lower(): b for b in base}
    old = copy.deepcopy(g.bones)
    by = {b["name"].lower(): b for b in old}
    zero = [0.0, 0.0, 0.0]

    def fl(v: Any) -> list[float]:
        return [round(float(x), 4) for x in (v or zero)]

    new: list[Bone] = []
    names: dict[str, str] = {}  # old lower name -> new name
    holder: dict[str, str] = {}  # vanilla-named bone -> bone that receives its cubes and custom children
    customs: list[tuple[Bone, Bone]] = []  # (new, old) for bones that are not vanilla-named
    for b in old:
        n = b["name"].lower()
        names[n] = vb[n]["name"] if n in vb else (b["name"] if n.startswith("mv_") else "mv_" + b["name"])
    has_child = {(b.get("parent") or "").lower() for b in old if (b.get("name") or "").lower() not in vb}
    changes: list[str] = []
    for b in old:
        n = b["name"].lower()
        if n in vb:
            v = vb[n]
            nb: Bone = {"name": v["name"]}
            if v.get("parent"):
                nb["parent"] = v["parent"]
            nb["pivot"] = v.get("pivot", zero)
            if v.get("rotation"):
                nb["rotation"] = v["rotation"]
            r_old, vr = fl(b.get("rotation")), fl(v.get("rotation") or v.get("bind_pose_rotation"))
            if r_old != vr:  # animations with `this` (pig.setup.v1.0: "90.0 - this") override it: decide by hand
                print(f"{layer_id}: {b['name']} rotation {b.get('rotation')} ≠ vanilla {v.get('rotation')}: fix by hand")
                return 1
            # rotated custom ancestors (old roots/spines) also place the bone at rest: keep them as frames
            frames: list[Bone] = []
            p = (b.get("parent") or "").lower()
            while p in by and p not in vb and len(frames) < 64:
                if fl(by[p].get("rotation")) != fl(zero):
                    frames.insert(0, by[p])
                p = (by[p].get("parent") or "").lower()
            # the bone's frame only matters at rest if something rotates
            same = not frames and ((r_old == vr == fl(zero)) or (fl(b.get("pivot")) == fl(v.get("pivot")) and r_old == vr))
            extra = {k: x for k, x in b.items() if k not in ("name", "pivot", "parent", "rotation", "cubes")}
            holder[n] = v["name"]
            new.append(nb)
            if same:
                nb.update(extra)
                if b.get("cubes"):
                    nb["cubes"] = b["cubes"]
            elif b.get("cubes") or n in has_child:
                attach = v["name"]
                if vr != fl(zero):  # undo the vanilla rest rotation (exact for single-axis rotations)
                    attach = f"mv_{b['name']}_rest"
                    new.append({"name": attach, "parent": v["name"], "pivot": v.get("pivot", zero),
                                "rotation": [-x for x in vr]})
                for fr in frames:
                    name = f"mv_{fr['name']}_frame"
                    new.append({"name": name, "parent": attach, "pivot": fr.get("pivot", zero), "rotation": fr["rotation"]})
                    attach = name
                child: Bone = {"name": "mv_" + b["name"], "parent": attach, "pivot": b.get("pivot", zero)}
                if r_old != fl(zero):
                    child["rotation"] = b["rotation"]
                child.update(extra)
                if b.get("cubes"):
                    child["cubes"] = b["cubes"]
                new.append(child)
                holder[n] = child["name"]
                changes.append(f"{b['name']}: own frame kept in {child['name']}")
            if (b.get("parent") or "").lower() != (v.get("parent") or "").lower() or fl(b.get("pivot")) != fl(v.get("pivot")) \
                    or r_old != vr:
                changes.append(f"{b['name']}: parent {b.get('parent')!r}->{v.get('parent')!r}, pivot {b.get('pivot')}->{v.get('pivot')}"
                               + (f", rotation {b.get('rotation')}->{v.get('rotation')}" if r_old != vr else ""))
        else:
            nb = dict(b)
            nb["name"] = names[n]
            new.append(nb)
            customs.append((nb, b))
    for nb, src in customs:  # custom bones: same parent, renamed (or the holder of a vanilla parent)
        p = (src.get("parent") or "").lower()
        if p in by:
            nb["parent"] = holder.get(p, names[p])
        if nb["name"] != src["name"] or nb.get("parent") != src.get("parent"):
            changes.append(f"{src['name']} -> {nb['name']} (parent {src.get('parent')!r}->{nb.get('parent')!r})")
    # drop custom bones left without cubes or children (old roots/spines)
    while True:
        parents = {(b.get("parent") or "").lower() for b in new}
        drop = [b for b in new if b["name"].lower() not in vb and not b.get("cubes") and b["name"].lower() not in parents]
        if not drop:
            break
        for b in drop:
            new.remove(b)
            changes.append(f"- {b['name']} (empty)")
    # empty vanilla ancestors so the layer inherits the same rest pose / animations
    have = {b["name"].lower() for b in new}
    for b in list(new):
        p = (b.get("parent") or "").lower()
        while p and p in vb and p not in have:
            v = vb[p]
            anc: Bone = {"name": v["name"]}
            if v.get("parent"):
                anc["parent"] = v["parent"]
            anc["pivot"] = v.get("pivot", zero)
            if v.get("rotation"):
                anc["rotation"] = v["rotation"]
            new.insert(0, anc)
            have.add(p)
            changes.append(f"+ {v['name']} (empty vanilla ancestor)")
            p = (v.get("parent") or "").lower()
    # rest pose must not change for any bone with cubes
    w_old, w_new = _world(old), _world(new)
    bad = []
    for b in old:
        if not b.get("cubes"):
            continue
        n = b["name"].lower()
        nn = holder[n].lower() if n in vb else names[n].lower()
        a, c = w_old[n], w_new[nn]
        if max(abs(a[i][j] - c[i][j]) for i in range(3) for j in range(4)) > 1e-3:
            bad.append(b["name"])
    print(f"{layer_id} vs {base_id}:")
    for c in changes:
        print("   ", c)
    if bad:
        print("    REFUSED: rest pose would change for", bad)
        return 1
    if not changes:
        print("    nothing to do")
        return 0
    if write:
        data, header = load_for_edit(g.file)
        for geo in data["minecraft:geometry"]:
            if geo["description"]["identifier"] == layer_id:
                geo["bones"] = new
        save(g.file, data, header)
        print("    written", os.path.relpath(g.file))
    return 0


def rebone(geo_id: str, base_id: str, renames: dict[str, str], drop: set[str], write: bool) -> int:
    """Full-model variant drawn instead of the base: bones renamed to the vanilla names (renames, plus the ones
    already called like a vanilla bone) so the vanilla animations move them; their own pivots are kept (each
    piece turns at its own joint). Bones in `drop` go with their subtree (eyelids). Vanilla-named bones take
    the vanilla parent when that does not move anything at rest; other bones get the mv_ prefix; empty
    custom bones are removed."""
    from mvlib import load_for_edit, save
    geos_a, geos_v = geo_index(find_pack("RP")), geo_index(VRP)
    g = geos_a[geo_id]
    if g.parent:
        print(f"{geo_id}: 1.8 inheritance not supported")
        return 1
    _, base = resolve_geo(base_id, geos_a, geos_v)
    vb = {b["name"].lower(): b for b in base}
    old = [b for b in copy.deepcopy(g.bones)]
    low = {k.lower(): v for k, v in renames.items()}
    dropped = {d.lower() for d in drop}
    while True:  # subtrees of dropped bones
        more = {b["name"].lower() for b in old if (b.get("parent") or "").lower() in dropped} - dropped
        if not more:
            break
        dropped |= more
    old = [b for b in old if b["name"].lower() not in dropped]

    def newname(n: str) -> str:
        if n.lower() in low:
            return low[n.lower()]
        if n.lower() in vb:
            return vb[n.lower()]["name"]
        return n if n.lower().startswith("mv_") else "mv_" + n
    names = {b["name"].lower(): newname(b["name"]) for b in old}
    if len(set(x.lower() for x in names.values())) != len(names):
        print(f"{geo_id}: two bones would get the same name: {sorted(names.values())}")
        return 1
    new: list[Bone] = []
    for b in old:
        nb = dict(b)
        nb["name"] = names[b["name"].lower()]
        p = (b.get("parent") or "").lower()
        if p in names:
            nb["parent"] = names[p]
        new.append(nb)
    by = {b["name"].lower(): b for b in new}
    w_ref = _world(new)  # renaming does not move anything: this is the rest pose to keep
    adopted: list[str] = []
    for b in new:
        n = b["name"].lower()
        if n not in vb:
            continue
        vpar = (vb[n].get("parent") or "")
        if vpar.lower() == (b.get("parent") or "").lower() or (vpar and vpar.lower() not in by):
            continue
        before = b.get("parent")
        if vpar:
            b["parent"] = by[vpar.lower()]["name"]
        else:
            b.pop("parent", None)
        w = _world(new)
        if all(max(abs(w[k][i][j] - w_ref[k][i][j]) for i in range(3) for j in range(4)) < 1e-3 for k in w_ref):
            adopted.append(f"{b['name']} -> parent {vpar or '(root)'}")
        elif before is None:
            b.pop("parent", None)
        else:
            b["parent"] = before
    while True:  # empty custom bones
        parents = {(b.get("parent") or "").lower() for b in new}
        empty = [b for b in new if b["name"].lower() not in vb and not b.get("cubes") and b["name"].lower() not in parents]
        if not empty:
            break
        for b in empty:
            new.remove(b)
    print(f"{geo_id}: dropped {sorted(dropped) or '-'}")
    print("    renamed:", {k: v for k, v in names.items() if k != v.lower()} or "-")
    print("    vanilla parent:", adopted or "-")
    vanilla_named = sorted(b["name"] for b in new if b["name"].lower() in vb)
    print("    animated as vanilla:", vanilla_named)
    if write:
        data, header = load_for_edit(g.file)
        for geo in data["minecraft:geometry"]:
            if geo["description"]["identifier"] == geo_id:
                geo["bones"] = new
        save(g.file, data, header)
        print("    written", os.path.relpath(g.file))
    return 0


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
    elif cmd == "relayer" and len(rest) >= 2:
        return relayer(rest[0], rest[1], "--write" in rest)
    elif cmd == "rebone" and len(rest) >= 2:
        opts = [x for x in rest[2:] if not x.startswith("--")]
        drop = {d for x in rest if x.startswith("--drop=") for d in x[7:].split(",") if d}
        return rebone(rest[0], rest[1], dict(x.split("=", 1) for x in opts), drop, "--write" in rest)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
