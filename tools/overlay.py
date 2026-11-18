"""Build an overlay geometry from parts of an addon model, re-parented to vanilla bone names."""
import sys, json, copy
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from facecheck import faces, inside
def build(src_bones, plan, ident, desc, rename=None, offset=(0, 0, 0)):
    """plan: {vanilla_bone: {"pivot": [...], "cubes_from": [(addon_bone, [cube idx...])], "children": [addon_bone,...]}}"""
    by = {b["name"]: b for b in src_bones}
    rename = rename or {}
    def sh(p): return [round(p[0] + offset[0], 4), round(p[1] + offset[1], 4), round(p[2] + offset[2], 4)]
    def mv(c):
        c = copy.deepcopy(c); c["origin"] = sh(c["origin"])
        if "pivot" in c: c["pivot"] = sh(c["pivot"])
        return c
    out = []
    def add_subtree(name, parent):
        b = copy.deepcopy(by[name]); nb = {"name": rename.get(name, "mv_" + name), "parent": parent}
        if "pivot" in b: nb["pivot"] = sh(b["pivot"])
        for k in ("rotation", "mirror", "inflate"):
            if k in b: nb[k] = b[k]
        if b.get("cubes"): nb["cubes"] = [mv(c) for c in b["cubes"]]
        out.append(nb)
        for c in src_bones:
            if c.get("parent") == name and c["name"] not in SKIP: add_subtree(c["name"], nb["name"])
    for vb, spec in plan.items():
        b = {"name": vb, "pivot": spec["pivot"]}
        if spec.get("parent"): b["parent"] = spec["parent"]
        cubes = [mv(by[ab]["cubes"][i]) for ab, idx in spec.get("cubes_from", []) for i in idx]
        if cubes: b["cubes"] = cubes
        out.append(b)
        for ch in spec.get("children", []): add_subtree(ch, vb)
    return {"format_version": "1.12.0", "minecraft:geometry": [{"description": {"identifier": ident, **desc}, "bones": out}]}
SKIP = set()
