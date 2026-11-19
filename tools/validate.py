"""Static checks of the resource pack against itself and the vanilla template.

    python -I tools/validate.py [--all]

ERRORS break the pack in game; WARNINGS are probably wrong; INFO is housekeeping.
Known vanilla gaps (exist in game, missing in bedrock-samples) are counted as EXPECTED, not errors.
--all also lists files not used by any entity. Exit code 1 if there are errors.
"""
from __future__ import annotations

import json
import os
import re
import hashlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import (VRP, Json, client_entities, files, find_pack, geo_index, keyed_ids, load_ex, rc_list,  # noqa: E402
                   png_size, rel, require_vanilla, resolve_geo, texture_file,
                   vanilla_client_entity)

# Animations the game has but bedrock-samples lacks (see CLAUDE.md).
EXPECTED_MISSING = {"animation.ghast.scale", "controller.animation.ghast.scale", "animation.warden.hurt",
                    "controller.animation.warden.hurt", "animation.sheep.setup.v2", "animation.cat.baby_transform",
                    "animation.fox.baby_transform", "animation.sheep.baby_transform", "animation.villager.get_in_bed_baby"}
# Add-on IDs that intentionally keep a non-mv name (rule 1 exception).
ALLOWED_IDS: set[str] = set()

errors: list[str] = []
warnings: list[str] = []
info: list[str] = []
expected: list[str] = []


def _ver(s: object) -> tuple[int, ...]:
    try:
        return tuple(int(x) for x in str(s).split("."))
    except ValueError:
        return (0,)


def main() -> int:
    require_vanilla()
    rp = find_pack("RP")
    geos_v, geos_a = geo_index(VRP), geo_index(rp)
    anims_v = keyed_ids(VRP, "animations", "animations")
    anims_a = keyed_ids(rp, "animations", "animations")
    acs_v = keyed_ids(VRP, "animation_controllers", "animation_controllers")
    acs_a = keyed_ids(rp, "animation_controllers", "animation_controllers")
    rcs_v = keyed_ids(VRP, "render_controllers", "render_controllers")
    rcs_a = keyed_ids(rp, "render_controllers", "render_controllers")
    rc_defs: dict[str, Json] = {}
    for idx in (rcs_v, rcs_a):
        for name, f in idx.items():
            rc_defs[name] = load_ex(f)[0]["render_controllers"][name]

    # ---- parse + comments
    commented = 0
    for sub in ("entity", "render_controllers", "models", "animations", "animation_controllers"):
        for f in files(rp, sub):
            try:
                commented += load_ex(f)[1]
            except ValueError as e:
                errors.append(f"PARSE {rel(f)}: {e}")

    # ---- ids: never redefine vanilla, use the mv namespace
    for kind, mine, van in (("geometry", geos_a, geos_v), ("animation", anims_a, anims_v),
                            ("animation controller", acs_a, acs_v), ("render controller", rcs_a, rcs_v)):
        for ident in mine:
            where = mine[ident].file if kind == "geometry" else mine[ident]  # type: ignore[union-attr]
            if ident in ALLOWED_IDS:
                continue
            if ident in van:
                errors.append(f"{rel(str(where))}: redefines vanilla {kind} {ident} (rule 4)")
            elif ".mv." not in ident:
                warnings.append(f"{rel(str(where))}: {kind} {ident} outside the mv namespace")

    vanilla_materials = {m for _, (_, d) in client_entities(VRP).items() for m in (d.get("materials") or {}).values()}
    all_geos = {**geos_v, **geos_a}

    # ---- entities
    used_tex: set[str] = set()
    used_geo: set[str] = set()
    used_rc: set[str] = set()
    for f, (ident, desc) in client_entities(rp).items():
        r = rel(f)
        data = load_ex(f)[0]
        van = vanilla_client_entity(ident)
        if van:
            vf, vd = van
            mine_v, van_v = _ver(data.get("format_version")), _ver(vd.get("format_version"))
            if mine_v < van_v:  # 1.26 entities split Molang over lines: an older format does not load
                errors.append(f"{r}: format_version {data.get('format_version')} < vanilla "
                              f"{vd.get('format_version')} ({os.path.basename(vf)})")
            elif mine_v > van_v:
                info.append(f"{r}: format_version {data.get('format_version')} (vanilla {vd.get('format_version')})")
            vmin = vd["minecraft:client_entity"]["description"].get("min_engine_version")
            if desc.get("min_engine_version") != vmin:
                info.append(f"{r}: min_engine_version {desc.get('min_engine_version')} (vanilla {vmin})")
        if "animation_controllers" in desc:
            errors.append(f"{r}: uses the old 'animation_controllers' list (put them in 'animations')")
        for k, p in (desc.get("textures") or {}).items():
            used_tex.add(p.replace("\\", "/").lower())
            if not texture_file(p, [rp, VRP]):
                errors.append(f"{r}: texture {k} -> {p} missing")
        for k, g in (desc.get("geometry") or {}).items():
            used_geo.add(g)
            if g not in all_geos:
                errors.append(f"{r}: geometry {k} -> {g} missing")
        for k, m in (desc.get("materials") or {}).items():
            if m not in vanilla_materials:
                errors.append(f"{r}: material {k} -> {m} is not a vanilla material (invalidates the entity)")
        for k, a in (desc.get("animations") or {}).items():
            if a not in anims_a and a not in anims_v and a not in acs_a and a not in acs_v:
                (expected if a in EXPECTED_MISSING else errors).append(f"{r}: animation {k} -> {a} missing")
        # Texture./Geometry./Material. keys used by its render controllers
        keys = {s: {k.lower() for k in (desc.get(s) or {})} for s in ("textures", "geometry", "materials")}
        texts = [json.dumps(desc.get("scripts") or {})]
        for name, cond in rc_list(desc):
            used_rc.add(name)
            rc = rc_defs.get(name)
            if rc is None:
                errors.append(f"{r}: render controller {name} missing")
                continue
            txt = json.dumps(rc) + (cond or "")
            texts.append(txt)
            for kind, sect in (("texture", "textures"), ("geometry", "geometry"), ("material", "materials")):
                for m in set(re.findall(rf"\b{kind}\.(\w+)", txt, re.I)):
                    if m.lower() not in keys[sect]:
                        errors.append(f"{r}: {name} uses {kind.capitalize()}.{m}, not defined in the entity")
        # q.property('mv:x') must be guarded by q.has_property('mv:x')
        for t in texts:
            for expr in re.findall(r'"((?:[^"\\]|\\.)*)"', t):
                for prop in set(re.findall(r"property\('(mv:\w+)'\)", expr)):
                    if f"has_property('{prop}')" not in expr:
                        errors.append(f"{r}: q.property('{prop}') without q.has_property guard: {expr[:70]}")
        # our variables (v.mv_*, v.xvar/yvar/zvar) must be assigned in the entity scripts; the editor
        # extension cannot check this (it stops at the multi-line Molang blocks of 1.26 entities)
        assigned = {m.lower() for m in re.findall(r"\b(?:v|variable)\.(\w+)\s*=(?!=)", texts[0], re.I)}
        for m in sorted({m.lower() for t in texts for m in re.findall(r"\b(?:v|variable)\.(mv_\w+|[xyz]var)\b", t, re.I)}):
            if m not in assigned:
                errors.append(f"{r}: v.{m} is used but never assigned in its scripts")
        layer_check(r, desc, geos_a, geos_v)

    # ---- packs
    for kind in ("RP", "BP"):
        icon = os.path.join(find_pack(kind), "pack_icon.png")
        size = png_size(icon) if os.path.exists(icon) else None
        if size and (size[0] != size[1] or size[0] not in (2 ** i for i in range(1, 10))):
            warnings.append(f"{kind}/pack_icon.png is {size[0]}x{size[1]}: must be square 16..256, power of 2")

    # ---- unused (textures at vanilla paths are retextures, not unused)
    unused: list[str] = []
    for f in files(rp, "textures", "**/*.*"):
        p = os.path.relpath(f, rp).replace("\\", "/")
        stem = os.path.splitext(p)[0].lower()
        if p.endswith(".json") or stem in used_tex or texture_file(os.path.splitext(p)[0], [VRP]):
            continue
        unused.append(p)
    # identical texture files (often a copy that should reuse the same path)
    by_hash: dict[str, list[str]] = {}
    for f in files(rp, "textures", "**/*.png"):
        with open(f, "rb") as fh:
            by_hash.setdefault(hashlib.sha1(fh.read()).hexdigest(), []).append(os.path.relpath(f, rp).replace("\\", "/"))
    for same in by_hash.values():
        if len(same) > 1:
            info.append("identical textures: " + ", ".join(sorted(same)))
    unused_geo = sorted(g for g in geos_a if g not in used_geo and not any(
        x.parent == g for x in geos_a.values()))
    unused_rc = sorted(x for x in rcs_a if x not in used_rc)
    for label, items in (("unused textures", unused), ("unused geometries", unused_geo), ("unused render controllers", unused_rc)):
        if items:
            info.append(f"{len(items)} {label}" + ("" if "--all" in sys.argv else " (--all to list)"))
            if "--all" in sys.argv:
                info.extend("    " + x for x in items)
    if commented:
        info.append(f"{commented} files with comments or trailing commas (accepted by the game)")

    for title, items in (("ERRORS", errors), ("WARNINGS", warnings), ("INFO", info)):
        print(f"== {title} {len(items)}")
        for x in sorted(set(items)) if title != "INFO" else items:
            print("  " + x)
    print(f"== EXPECTED (vanilla gaps) {len(expected)}")
    return 1 if errors else 0


def layer_check(r: str, desc: Json, geos_a: dict, geos_v: dict) -> None:  # type: ignore[type-arg]
    """Bones of overlay geometries named like base bones must share pivot and parent (rule 2)."""
    g = desc.get("geometry") or {}
    base_id = g.get("mv_default") or g.get("default")
    if not base_id:
        return
    try:
        _, base = resolve_geo(base_id, geos_a, geos_v)
    except KeyError:
        return
    bb = {b["name"].lower(): b for b in base}
    for key, gid in g.items():
        if not key.startswith("mv_") or gid == base_id or gid not in geos_a:
            continue
        _, bones = resolve_geo(gid, geos_a, geos_v)
        shared = [b for b in bones if b["name"].lower() in bb]
        if not shared or sum(1 for b in shared if b.get("cubes")) >= 3:
            continue  # a full replacement model (cubes on several base bones), not a layer
        bad: list[str] = []
        for b in shared:
            v = bb[b["name"].lower()]
            piv = [round(float(x), 2) for x in b.get("pivot", [0, 0, 0])]
            vpiv = [round(float(x), 2) for x in v.get("pivot", [0, 0, 0])]
            par, vpar = (b.get("parent") or "").lower(), (v.get("parent") or "").lower()
            if piv != vpiv:
                bad.append(f"{b['name']} pivot {piv}≠{vpiv}")
            if par != vpar:
                bad.append(f"{b['name']} parent '{par}'≠'{vpar}'")
        if bad:
            warnings.append(f"{r}: layer {gid} vs {base_id}: " + "; ".join(bad))


if __name__ == "__main__":
    sys.exit(main())
