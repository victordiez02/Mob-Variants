import sys, json; import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from facecheck import faces, inside, A, V
VRP = os.path.join(VAN, "resource_pack")
def ver(s): return tuple(int(x) for x in (s or "0.0.0").split("."))
cands = {}
for f in files(VRP, "entity"):
    d = load(f)[0]["minecraft:client_entity"]["description"]
    for k, g in (d.get("geometry") or {}).items():
        if "baby" not in k and g in V: cands.setdefault(d["identifier"], set()).add(g)
def score(a, vid):
    try: _, vb = resolve(vid, V)
    except Exception: vb = V[vid]["bones"]
    vfs = [r for b in vb for c in b.get("cubes", []) for r in faces(c).values()]
    tot = ok = 0; outside = []
    for b in A[a]["bones"]:
        for c in b.get("cubes", []):
            for k, r in faces(c).items():
                if not r[2] or not r[3]: continue
                tot += 1
                if any(inside(r, R) for R in vfs): ok += 1
                else: outside.append(b["name"])
    return ok / max(tot, 1), sorted(set(outside))
RP = find_pack("RP")
for f in sorted(files(RP, "entity")):
    d = load(f)[0]["minecraft:client_entity"]["description"]
    a = d.get("geometry", {}).get("mv_default")
    if not a or a not in A: continue
    tw = A[a]["desc"]
    print(f"## {os.path.basename(f)} {a} [{tw.get('texture_width')}x{tw.get('texture_height')}]")
    for vid in sorted(cands.get(d["identifier"], [])):
        s, out = score(a, vid)
        vd = V[vid]["desc"]
        print(f"   {vid:34} [{vd.get('texture_width')}x{vd.get('texture_height')}] {s:.0%}  outside bones: {out}")
