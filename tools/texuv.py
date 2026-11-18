"""Texture tools (need Pillow): UV templates, moving a skin to another model's UV, recolouring, linting.

    python tools/texuv.py template <geometry> [texture]
        PNG with every face outlined on the texture (colour = face, label = bone) -> tools/out/tex/.
        For an artist painting by hand and to see which pixels a face uses.
    python tools/texuv.py retarget <src geometry> <dst geometry> <src texture> [dstBone=srcBone[+srcBone2] ...] [--out F]
        Builds a texture for <dst geometry> by copying, face by face, what <src geometry> shows on the
        same bone (default: same name) and same face. `leg0=leg0+knee0` stacks the side faces of a split
        limb. Different sizes are rescaled (nearest) and reported. Faces without source stay transparent.
        Writes tools/out/tex/<name>.png unless --out is given (never overwrites the source).
    python tools/texuv.py recolor <texture> [--hue DEG] [--sat F] [--val F] [--like other] [--out F]
        HSV shift and/or colour transfer from another skin (mean/deviation of its opaque pixels).
    python tools/texuv.py lint [mob ...] [--min 20]
        For every (geometry, texture) the mob can draw: opaque pixels outside every face (lost work) and
        semi-transparent pixels (alpha-test materials show them fully or not at all).

Textures are given like in entities (textures/entity/pig/pig, no extension) or as a file path.
"""
from __future__ import annotations

import colorsys
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw  # noqa: E402

from mvlib import ROOT, VRP, Geo, find_pack, geo_index, rel, resolve_geo, texture_file  # noqa: E402

Rect = tuple[float, float, float, float]
FACE_COLORS = {"north": (255, 60, 60), "south": (60, 200, 255), "east": (255, 200, 0), "west": (60, 220, 60),
               "up": (255, 255, 255), "down": (180, 90, 255)}
OUT = os.path.join(ROOT, "tools", "out", "tex")
_GEOS: tuple[dict[str, Geo], dict[str, Geo]] | None = None


def geos() -> tuple[dict[str, Geo], dict[str, Geo]]:
    global _GEOS
    if _GEOS is None:
        _GEOS = (geo_index(find_pack("RP")), geo_index(VRP))
    return _GEOS


def open_texture(ref: str) -> tuple[Image.Image, str]:
    path = ref if os.path.isfile(ref) else texture_file(ref, [find_pack("RP"), VRP])
    if not path or path.endswith(".json"):
        raise SystemExit(f"texture not found: {ref}")
    return Image.open(path).convert("RGBA"), path


def face_display(c: dict[str, Any], key: str) -> tuple[Rect, bool, bool] | None:
    """Texture rect shown on face `key`, and the flips that bring it to the box-UV orientation."""
    w, h, d = (abs(float(x)) for x in c["size"])
    uv = c.get("uv", [0, 0])
    if isinstance(uv, dict):
        f = uv.get(key)
        if not f:
            return None
        (u, v), (du, dv) = f["uv"], f.get("uv_size", [w, h])
        u, v, du, dv = float(u), float(v), float(du), float(dv)
        fx, fy = du < 0, dv < 0
        if key in ("up", "down"):  # Bedrock per-face up/down are rotated 180° vs. box UV
            fx, fy = not fx, not fy
        return (min(u, u + du), min(v, v + dv), abs(du), abs(dv)), fx, fy
    x, y = float(uv[0]), float(uv[1])
    rects = {"up": (x + d, y, w, d), "down": (x + d + w, y, w, d), "east": (x, y + d, d, h),
             "north": (x + d, y + d, w, h), "west": (x + d + w, y + d, d, h), "south": (x + 2 * d + w, y + d, w, h)}
    if c.get("mirror"):
        swap = {"east": "west", "west": "east"}.get(key, key)
        return rects[swap], True, False
    return rects[key], False, False


def bones_of(ident: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    try:
        return resolve_geo(ident, *geos())
    except KeyError:
        raise SystemExit(f"geometry not found: {ident}") from None


def with_mirror(bones: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Cubes inherit the bone's `mirror` (1.8 style)."""
    for b in bones:
        if b.get("mirror"):
            for c in b.get("cubes", []):
                c.setdefault("mirror", True)
    return bones


def crop(img: Image.Image, scale: tuple[float, float], disp: tuple[Rect, bool, bool]) -> Image.Image | None:
    (u, v, w, h), fx, fy = disp
    sx, sy = scale
    box = (round(u * sx), round(v * sy), round((u + w) * sx), round((v + h) * sy))
    if box[2] <= box[0] or box[3] <= box[1]:
        return None
    part = img.crop(box)
    if fx:
        part = part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if fy:
        part = part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return part


def paste(img: Image.Image, scale: tuple[float, float], disp: tuple[Rect, bool, bool], part: Image.Image) -> bool:
    """Paste `part` (box-UV orientation) into the face; True if it had to be rescaled."""
    (u, v, w, h), fx, fy = disp
    sx, sy = scale
    size = (max(round(w * sx), 1), max(round(h * sy), 1))
    scaled = part.size != size
    if scaled:
        part = part.resize(size, Image.Resampling.NEAREST)
    if fx:
        part = part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if fy:
        part = part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    img.paste(part, (round(u * sx), round(v * sy)))
    return scaled


def box(u: float, v: float, w: float, h: float, sx: float, sy: float) -> list[float]:
    """Pixel rectangle of a face (faces under one pixel still cover one)."""
    x0, y0 = u * sx, v * sy
    return [x0, y0, max(x0, (u + w) * sx - 1), max(y0, (v + h) * sy - 1)]


# ---------------------------------------------------------------- commands


def template(ident: str, tex_ref: str | None) -> None:
    desc, bones = bones_of(ident)
    bones = with_mirror(bones)
    tw, th = float(desc.get("texture_width", 64)), float(desc.get("texture_height", 64))
    if tex_ref:
        base, _ = open_texture(tex_ref)
    else:
        base = Image.new("RGBA", (int(tw), int(th)), (0, 0, 0, 0))
    k = max(1, 1024 // max(base.width, base.height))
    sx, sy = base.width / tw * k, base.height / th * k
    big = base.resize((base.width * k, base.height * k), Image.Resampling.NEAREST)
    sheet = Image.new("RGBA", big.size, (60, 64, 72, 255))
    checker = ImageDraw.Draw(sheet)
    step = max(k * 2, 8)
    for yy in range(0, sheet.height, step):
        for xx in range((yy // step) % 2 * step, sheet.width, step * 2):
            checker.rectangle([xx, yy, xx + step - 1, yy + step - 1], fill=(80, 85, 95, 255))
    sheet.alpha_composite(big)
    d = ImageDraw.Draw(sheet)
    for b in bones:
        for i, c in enumerate(b.get("cubes", [])):
            for key in FACE_COLORS:
                disp = face_display(c, key)
                if not disp or disp[0][2] == 0 or disp[0][3] == 0:
                    continue
                u, v, w, h = disp[0]
                d.rectangle(box(u, v, w, h, sx, sy), outline=FACE_COLORS[key])
                if key == "north":
                    d.text((u * sx + 2, v * sy + 1), f"{b['name']}{'' if i == 0 else i}", fill=(255, 255, 255))
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, f"{ident.replace('geometry.', '')}_uv.png")
    sheet.convert("RGB").save(out)
    print(f"{rel(out)}  (colours: north red, south blue, east yellow, west green, up white, down purple)")


def retarget(src_id: str, dst_id: str, tex_ref: str, maps: list[str], out: str | None) -> None:
    sdesc, sbones = bones_of(src_id)
    ddesc, dbones = bones_of(dst_id)
    sbones, dbones = with_mirror(sbones), with_mirror(dbones)
    img, path = open_texture(tex_ref)
    stw, sth = float(sdesc.get("texture_width", 64)), float(sdesc.get("texture_height", 64))
    dtw, dth = float(ddesc.get("texture_width", 64)), float(ddesc.get("texture_height", 64))
    s_scale = (img.width / stw, img.height / sth)
    d_scale = s_scale  # same pixels per UV unit as the source
    result = Image.new("RGBA", (round(dtw * d_scale[0]), round(dth * d_scale[1])), (0, 0, 0, 0))
    by_name = {b["name"].lower(): b for b in sbones}
    mapping = {k.lower(): [x.lower() for x in v.split("+")] for k, _, v in (m.partition("=") for m in maps)}
    copied, scaled, missing = 0, [], []
    for b in dbones:
        srcs = [by_name[n] for n in mapping.get(b["name"].lower(), [b["name"].lower()]) if n in by_name]
        for i, c in enumerate(b.get("cubes", [])):
            for key in FACE_COLORS:
                ddisp = face_display(c, key)
                if not ddisp or ddisp[0][2] == 0 or ddisp[0][3] == 0:
                    continue
                part = None
                if len(srcs) == 1:
                    cubes = srcs[0].get("cubes", [])
                    sc = cubes[i] if i < len(cubes) else (cubes[0] if cubes else None)
                    sdisp = face_display(sc, key) if sc else None
                    part = crop(img, s_scale, sdisp) if sdisp else None
                elif len(srcs) > 1:  # split limb: stack side faces top to bottom
                    parts = []
                    order = srcs if key != "down" else srcs[-1:]
                    order = order if key != "up" else srcs[:1]
                    for s in order:
                        sc = (s.get("cubes") or [None])[0]
                        sdisp = face_display(sc, key) if sc else None
                        p = crop(img, s_scale, sdisp) if sdisp else None
                        if p:
                            parts.append(p)
                    if parts:
                        part = Image.new("RGBA", (max(p.width for p in parts), sum(p.height for p in parts)))
                        y = 0
                        for p in parts:
                            part.paste(p, (0, y))
                            y += p.height
                if part is None:
                    missing.append(f"{b['name']}[{i}].{key}")
                    continue
                if paste(result, d_scale, ddisp, part):
                    scaled.append(f"{b['name']}[{i}].{key}")
                copied += 1
    os.makedirs(OUT, exist_ok=True)
    out = out or os.path.join(OUT, f"{os.path.splitext(os.path.basename(path))[0]}_{dst_id.replace('geometry.', '')}.png")
    if os.path.abspath(out) == os.path.abspath(path):
        raise SystemExit("refusing to overwrite the source texture")
    result.save(out)
    print(f"{rel(out)}: {copied} faces copied, {len(scaled)} rescaled, {len(missing)} without source")
    if scaled:
        print("  rescaled:", ", ".join(scaled[:30]))
    if missing:
        print("  without source (paint by hand):", ", ".join(missing[:40]))
    used = {n for b in dbones for n in mapping.get(b["name"].lower(), [b["name"].lower()])}
    left = sorted(b["name"] for b in sbones if b.get("cubes") and b["name"].lower() not in used)
    if left:
        print("  source bones with no place in the destination (candidates for a layer):", ", ".join(left))


def recolor(tex_ref: str, hue: float, sat: float, val: float, like: str | None, out: str | None) -> None:
    img, path = open_texture(tex_ref)
    px = img.load()
    assert px is not None
    opaque = [(x, y) for y in range(img.height) for x in range(img.width) if px[x, y][3] > 0]  # type: ignore[index]
    if like:
        ref, _ = open_texture(like)
        rp = ref.load()
        assert rp is not None
        ref_px = [rp[x, y] for y in range(ref.height) for x in range(ref.width) if rp[x, y][3] > 0]  # type: ignore[index]
        src_px = [px[x, y] for x, y in opaque]

        def stats(values: list[Any], ch: int) -> tuple[float, float]:
            vals = [v[ch] for v in values]
            m = sum(vals) / max(len(vals), 1)
            return m, (sum((x - m) ** 2 for x in vals) / max(len(vals), 1)) ** 0.5 or 1.0

        tr = [(stats(src_px, ch), stats(ref_px, ch)) for ch in range(3)]
        for x, y in opaque:
            p: tuple[int, int, int, int] = px[x, y]  # type: ignore[assignment]
            rgb = [max(0, min(255, round((p[ch] - tr[ch][0][0]) / tr[ch][0][1] * tr[ch][1][1] + tr[ch][1][0])))
                   for ch in range(3)]
            px[x, y] = (rgb[0], rgb[1], rgb[2], p[3])
    if hue or sat != 1 or val != 1:
        for x, y in opaque:
            r, g, b, a = px[x, y]  # type: ignore[misc]
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            r2, g2, b2 = colorsys.hsv_to_rgb((hh + hue / 360) % 1, min(ss * sat, 1), min(vv * val, 1))
            px[x, y] = (round(r2 * 255), round(g2 * 255), round(b2 * 255), a)
    os.makedirs(OUT, exist_ok=True)
    out = out or os.path.join(OUT, os.path.splitext(os.path.basename(path))[0] + "_recolor.png")
    if os.path.abspath(out) == os.path.abspath(path):
        raise SystemExit("refusing to overwrite the source texture (copy it first)")
    img.save(out)
    print(rel(out))


def lint(mobs: list[str], minimum: int = 20) -> None:
    from mvsim import Mob, State
    rp = find_pack("RP")
    pairs: set[tuple[str, str]] = set()
    for f in sorted(os.listdir(os.path.join(rp, "entity"))):
        name = f.split(".")[0]
        if mobs and name not in mobs:
            continue
        mob = Mob(os.path.join(rp, "entity", f))
        for x in range(0, 100, 2):
            for lay in mob.run(State(None, {"xvar": x + 0.5, "yvar": x + 0.5, "zvar": x + 0.5}))[1]:
                if lay.geometry and "empty" not in lay.geometry and lay.rc.startswith("controller.render.mv."):
                    pairs.update((lay.geometry, t) for t in lay.textures)
    by_tex: dict[str, list[str]] = {}  # a texture can be shared by several geometries (base + layers)
    for geo, tex in sorted(pairs):
        if "empty" not in tex:
            by_tex.setdefault(tex, []).append(geo)
    found: list[tuple[int, str]] = []
    for tex, geo_ids in sorted(by_tex.items()):
        img, _ = open_texture(tex)
        mask = Image.new("L", img.size, 0)
        md = ImageDraw.Draw(mask)
        for geo in geo_ids:
            desc, bones = bones_of(geo)
            tw, th = float(desc.get("texture_width", 64)), float(desc.get("texture_height", 64))
            sx, sy = img.width / tw, img.height / th
            for b in with_mirror(bones):
                for c in b.get("cubes", []):
                    for key in FACE_COLORS:
                        disp = face_display(c, key)
                        if disp and disp[0][2] and disp[0][3]:
                            u, v, w, h = disp[0]
                            md.rectangle(box(u, v, w, h, sx, sy), fill=255)
        alpha = img.getchannel("A").tobytes()
        inside = mask.tobytes()
        outside = sum(1 for a, m in zip(alpha, inside, strict=True) if a and not m)
        semi = sum(1 for a, m in zip(alpha, inside, strict=True) if 0 < a < 255 and m)
        if outside >= minimum or semi >= minimum:
            names = ", ".join(g.replace("geometry.", "") for g in geo_ids)
            found.append((outside + semi, f"{os.path.basename(tex)} on {names}: "
                                          f"{outside} opaque px outside the UV, {semi} semi-transparent px"))
    for _, line in sorted(found, reverse=True):
        print(line)
    print(f"{len(found)} textures with >= {minimum} px outside the UV or semi-transparent ({len(by_tex)} checked)")


def main() -> int:
    a = sys.argv[1:]

    def opt(name: str, default: str | None = None) -> str | None:
        return a[a.index(name) + 1] if name in a and a.index(name) + 1 < len(a) else default

    pos = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or not a[i - 1].startswith("--"))]
    if not pos:
        print(__doc__)
        return 2
    cmd, rest = pos[0], pos[1:]
    if cmd == "template" and rest:
        template(rest[0], rest[1] if len(rest) > 1 else None)
    elif cmd == "retarget" and len(rest) >= 3:
        retarget(rest[0], rest[1], rest[2], rest[3:], opt("--out"))
    elif cmd == "recolor" and rest:
        recolor(rest[0], float(opt("--hue", "0") or 0), float(opt("--sat", "1") or 1), float(opt("--val", "1") or 1),
                opt("--like"), opt("--out"))
    elif cmd == "lint":
        lint(rest, int(opt("--min", "20") or 20))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
