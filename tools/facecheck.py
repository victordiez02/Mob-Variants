"""Are the faces of an addon (re-rigged) model inside the UV faces of the vanilla model?"""
import sys, json, re
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
RP = find_pack("RP"); A = index(RP); V = index(os.path.join(VAN, "resource_pack"))
def faces(c):
    u = c.get("uv", [0, 0]); w, h, d = [abs(x) for x in c["size"]]
    if isinstance(u, dict):
        out = {}
        for k, f in u.items():
            (x, y), (sw, sh) = f["uv"], f.get("uv_size", [0, 0])
            out[k] = (min(x, x + sw), min(y, y + sh), abs(sw), abs(sh))
        return out
    x, y = u
    return {"up": (x + d, y, w, d), "down": (x + d + w, y, w, d), "east": (x, y + d, d, h), "north": (x + d, y + d, w, h),
            "west": (x + d + w, y + d, d, h), "south": (x + 2 * d + w, y + d, w, h)}
def inside(r, R): return r[0] >= R[0] - 1e-6 and r[1] >= R[1] - 1e-6 and r[0] + r[2] <= R[0] + R[2] + 1e-6 and r[1] + r[3] <= R[1] + R[3] + 1e-6
def check(a, v, mapping):
    ga, gv = A[a], V[v]
    vf = {}
    for b in gv["bones"]:
        for c in b.get("cubes", []):
            vf.setdefault(b["name"], []).extend(faces(c).values())
    allv = [r for rs in vf.values() for r in rs]
    ok, bad, extra = 0, [], []
    for b in ga["bones"]:
        target = mapping.get(b["name"], b["name"])
        for c in b.get("cubes", []):
            for k, r in faces(c).items():
                if r[2] == 0 or r[3] == 0: continue
                if target in vf and any(inside(r, R) for R in vf[target]): ok += 1
                elif target not in vf: extra.append(b["name"])
                else: bad.append((b["name"], k, r))
    print(f"{a}: faces inside vanilla={ok} outside={len(bad)} extra bones={sorted(set(extra))}")
    for x in bad[:12]: print("   outside:", x)
if __name__ == "__main__":
    # usage: python tools/facecheck.py <addon geometry id> <vanilla geometry id> [addonBone=vanillaBone ...]
    a, v, *maps = sys.argv[1:]
    check(a, v, dict(m.split("=") for m in maps))
