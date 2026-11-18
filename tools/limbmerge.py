"""Repaint skins of split limbs (upper + knee/elbow, box UV) into the single vanilla limb layout."""
import sys, json; import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import *
from PIL import Image
RP = find_pack("RP"); VRP = os.path.join(VAN, "resource_pack")
A = index(RP); V = index(VRP)
def pairs(addon_id, vanilla_id):
    ab = {b["name"]: b for b in A[addon_id]["bones"]}
    try: _, vb = resolve(vanilla_id, V)
    except Exception: vb = V[vanilla_id]["bones"]
    vcubes = [c for b in vb for c in b.get("cubes", []) if isinstance(c.get("uv"), list)]
    out = []
    for b in ab.values():
        kids = [k for k in ab.values() if k.get("parent") == b["name"] and k.get("cubes")]
        if len(b.get("cubes", [])) < 1: continue
        for k in kids:
            up, lo = b["cubes"][0], k["cubes"][0]
            if not (isinstance(up.get("uv"), list) and isinstance(lo.get("uv"), list)): continue
            w, h1, d = up["size"]; w2, h2, d2 = lo["size"]
            if (w, d) != (w2, d2): continue
            match = [c for c in vcubes if list(c["uv"]) == list(up["uv"]) and c["size"] == [w, h1 + h2, d]]
            if match: out.append((b["name"], k["name"], up["uv"], lo["uv"], (int(w), int(h1), int(h2), int(d))))
    return out
def repaint(img, plist):
    src = img.copy(); dst = img
    for _, _, (u, v), (u2, v2), (w, h1, h2, d) in plist:
        # side faces: rows of the lower cube go below the upper ones
        side = src.crop((u2, v2 + d, u2 + 2 * d + 2 * w, v2 + d + h2))
        dst.paste(side, (u, v + d + h1))
        # bottom face comes from the lower cube
        dst.paste(src.crop((u2 + d + w, v2, u2 + d + 2 * w, v2 + d)), (u + d + w, v))
    return dst
if __name__ == "__main__":
    addon_id, vanilla_id, *tex = sys.argv[1:]
    pl = pairs(addon_id, vanilla_id)
    print("limbs:", [(a, b) for a, b, *_ in pl])
    for t in tex:
        p = os.path.join(RP, t + ".png"); im = Image.open(p).convert("RGBA")
        repaint(im, pl).save(p); print("repainted", t)
