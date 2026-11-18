"""Geometry normalization (1.8 -> 1.12 structure) and comparison helpers."""
import os, sys, json, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import *

DESC_MAP = {"texturewidth": "texture_width", "textureheight": "texture_height",
            "visible_bounds_width": "visible_bounds_width", "visible_bounds_height": "visible_bounds_height",
            "visible_bounds_offset": "visible_bounds_offset"}

def parse_file(path):
    """Return list of (identifier, parent_or_None, desc_dict, bones, fmt) for a model file."""
    d, _ = load(path)
    out = []
    fmt = d.get("format_version", "1.8.0")
    if "minecraft:geometry" in d:
        for g in d["minecraft:geometry"]:
            desc = dict(g["description"]); ident = desc.pop("identifier")
            out.append((ident, None, desc, g.get("bones", []), fmt, {k: v for k, v in g.items() if k not in ("description", "bones")}))
    else:
        for k, v in d.items():
            if not k.startswith("geometry."): continue
            ident, _, parent = k.partition(":")
            desc = {DESC_MAP[x]: v[x] for x in v if x in DESC_MAP}
            extra = {x: v[x] for x in v if x not in DESC_MAP and x != "bones"}
            out.append((ident, parent or None, desc, v.get("bones", []), fmt, extra))
    return out

def index(base):
    idx = {}
    for f in files(base, "models"):
        for ident, parent, desc, bones, fmt, extra in parse_file(f):
            idx[ident] = dict(file=f, parent=parent, desc=desc, bones=bones, fmt=fmt, extra=extra)
    return idx

def resolve(ident, idx, fallback=None):
    g = idx.get(ident) or (fallback or {}).get(ident)
    if g is None: raise KeyError(ident)
    desc, bones = dict(g["desc"]), copy.deepcopy(g["bones"])
    if g["parent"]:
        pdesc, pbones = resolve(g["parent"], idx, fallback)
        merged = {b["name"]: b for b in pbones}
        order = [b["name"] for b in pbones]
        for b in bones:
            if b["name"] not in merged: order.append(b["name"])
            merged[b["name"]] = b
        bones = [merged[n] for n in order]
        desc = {**pdesc, **desc}
    return desc, bones

def _num(o):
    if isinstance(o, bool): return o
    if isinstance(o, (int, float)): return round(float(o), 4)
    if isinstance(o, list): return [_num(x) for x in o]
    if isinstance(o, dict): return {k: _num(v) for k, v in o.items()}
    return o

def canon(desc, bones):
    bones = _num(bones); desc = _num(desc)
    def cb(b):
        b = {k: v for k, v in b.items() if k not in ("META_BoneType",)}
        return json.dumps(b, sort_keys=True)
    d = {k: desc.get(k) for k in ("texture_width", "texture_height")}
    return json.dumps(d, sort_keys=True) + "|" + "|".join(sorted(cb(b) for b in bones))
