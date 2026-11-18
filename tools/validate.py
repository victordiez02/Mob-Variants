"""Cross-reference validator for the Mob Variants RP against itself + vanilla."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import *

RP = find_pack("RP")
VRP = os.path.join(VAN, "resource_pack")

geos = {**geo_ids(VRP), **geo_ids(RP)}
anims = {**keyed_ids(VRP, "animations", "animations"), **keyed_ids(RP, "animations", "animations")}
acs = {**keyed_ids(VRP, "animation_controllers", "animation_controllers"), **keyed_ids(RP, "animation_controllers", "animation_controllers")}
rcs_addon = keyed_ids(RP, "render_controllers", "render_controllers")
rcs = {**keyed_ids(VRP, "render_controllers", "render_controllers"), **rcs_addon}

problems = []
commented = []
for sub in ("entity", "render_controllers", "models", "animations", "animation_controllers"):
    for f in files(RP, sub):
        try:
            _, c = load(f)
            if c: commented.append(os.path.relpath(f, RP))
        except Exception as e:
            problems.append(f"PARSE {os.path.relpath(f, RP)}: {e}")

for f in sorted(files(RP, "entity")):
    rel = os.path.relpath(f, RP)
    d, _ = load(f)
    desc = d["minecraft:client_entity"]["description"]
    for k, p in (desc.get("textures") or {}).items():
        if not (texture_exists(RP, p) or texture_exists(VRP, p)):
            problems.append(f"{rel}: texture {k} -> {p} missing")
    for k, g in (desc.get("geometry") or {}).items():
        if g not in geos:
            problems.append(f"{rel}: geometry {k} -> {g} missing")
    for k, a in (desc.get("animations") or {}).items():
        if a not in anims and a not in acs:
            problems.append(f"{rel}: animation {k} -> {a} missing")
    for r in desc.get("render_controllers") or []:
        name = r if isinstance(r, str) else list(r)[0]
        if name not in rcs:
            problems.append(f"{rel}: render controller {name} missing")
    # keys used by render controllers vs defined keys
    tex_keys = {k.lower() for k in (desc.get("textures") or {})}
    geo_keys = {k.lower() for k in (desc.get("geometry") or {})}
    mat_keys = {k.lower() for k in (desc.get("materials") or {})}
    for r in desc.get("render_controllers") or []:
        name = r if isinstance(r, str) else list(r)[0]
        src = rcs.get(name)
        if not src: continue
        rd, _ = load(src)
        txt = str(rd["render_controllers"][name])
        for m in set(re.findall(r"[Tt]exture\.([A-Za-z0-9_]+)", txt)):
            if m.lower() not in tex_keys: problems.append(f"{rel}: {name} uses Texture.{m} not defined")
        for m in set(re.findall(r"[Gg]eometry\.([A-Za-z0-9_]+)", txt)):
            if m.lower() not in geo_keys: problems.append(f"{rel}: {name} uses Geometry.{m} not defined")
        for m in set(re.findall(r"[Mm]aterial\.([A-Za-z0-9_]+)", txt)):
            if m.lower() not in mat_keys: problems.append(f"{rel}: {name} uses Material.{m} not defined")

# unused textures in RP
used = set()
for f in files(RP, "entity"):
    d, _ = load(f)
    for p in (d["minecraft:client_entity"]["description"].get("textures") or {}).values():
        used.add(p.replace("\\", "/").lower())
unused = []
for f in glob.glob(os.path.join(glob.escape(RP), "textures", "**", "*.*"), recursive=True):
    rel = os.path.relpath(f, RP).replace("\\", "/")
    stem = os.path.splitext(rel)[0].lower()
    if stem not in used and not rel.endswith(".json"):
        unused.append(rel)
unused_geo = [g for g, f in geo_ids(RP).items() if not any(g in open(e, encoding="utf-8-sig").read() for e in files(RP, "entity"))]
unused_rc = [r for r in rcs_addon if not any(r in open(e, encoding="utf-8-sig").read() for e in files(RP, "entity"))]

print("== PROBLEMS", len(problems)); print("\n".join(problems))
print("== FILES WITH COMMENTS/TRAILING COMMAS", len(commented)); print("\n".join(commented))
print("== UNUSED TEXTURES", len(unused)); print("\n".join(unused))
print("== UNUSED GEOMETRIES", len(unused_geo)); print("\n".join(unused_geo))
print("== UNUSED RENDER CONTROLLERS", len(unused_rc)); print("\n".join(unused_rc))
