"""Render a mob's variants to PNG (software renderer, needs Pillow) so they can be checked without the game.

    python tools/render.py <mob> [options]

  --nobp              use the local rolls (RP only) instead of the BP spawn results
  --q name=value      set a query/variable/property, e.g. --q is_angry=1 --q v.ischarging=1
                      --q property:minecraft:has_nectar=1 --q climate=warm --q is_baby=1
  --bp name=value     force BP values, e.g. --bp mv:variant=3 --bp mv:mark_variant=1 (one tile)
  --view front|back|side|top|all   camera (default front: 3/4 from the front-left)
  --max N             at most N tiles (default 30, most likely first)
  --size PX           tile size (default 256)
  --nopose            bind pose (ignore the entity animations)
  --out FILE          output PNG (default tools/out/<mob>.png)

What it draws: every render controller whose condition is true, its geometry (with 1.8 inheritance),
its textures, part_visibility, and the pose that the entity's animations give at time 0 with every
query at 0 (setup/pose animations, e.g. the pig's legacy setup or the enderman's raised body).
Not drawn: materials (blend/emissive are drawn as alpha-test), uv animations, particles, attachables.
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw  # noqa: E402

from molang import Env, Value, evaluate, num, truthy  # noqa: E402
from mvlib import (ROOT, VRP, Geo, Json, find_pack, geo_index, keyed_ids, load, require_vanilla,  # noqa: E402
                   resolve_geo, texture_file)
from mvsim import Layer, Mob, State, bone_visible, bp_entity, spawn_distribution  # noqa: E402

Vec = tuple[float, float, float]
Mat = list[list[float]]  # 4x4

# ---------------------------------------------------------------- math


def mat_mul(a: Mat, b: Mat) -> Mat:
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def translate(x: float, y: float, z: float) -> Mat:
    return [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]


def scale_m(x: float, y: float, z: float) -> Mat:
    return [[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]]


def rot_bb(rx: float, ry: float, rz: float) -> Mat:
    """Rotation in Blockbench space from Bedrock degrees: Euler (-rx, -ry, rz), order ZYX (R = Rz·Ry·Rx)."""
    ax, ay, az = math.radians(-rx), math.radians(-ry), math.radians(rz)
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    mx = [[1, 0, 0, 0], [0, cx, -sx, 0], [0, sx, cx, 0], [0, 0, 0, 1]]
    my = [[cy, 0, sy, 0], [0, 1, 0, 0], [-sy, 0, cy, 0], [0, 0, 0, 1]]
    mz = [[cz, -sz, 0, 0], [sz, cz, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    return mat_mul(mz, mat_mul(my, mx))


def apply(m: Mat, p: Vec) -> Vec:
    x, y, z = p
    return (m[0][0] * x + m[0][1] * y + m[0][2] * z + m[0][3],
            m[1][0] * x + m[1][1] * y + m[1][2] * z + m[1][3],
            m[2][0] * x + m[2][1] * y + m[2][2] * z + m[2][3])


def about(pivot: Vec, m: Mat) -> Mat:
    return mat_mul(translate(*pivot), mat_mul(m, translate(-pivot[0], -pivot[1], -pivot[2])))


def bb(p: list[float] | tuple[float, ...]) -> Vec:
    """Bedrock model coordinates -> Blockbench space (X mirrored)."""
    return (-float(p[0]), float(p[1]), float(p[2]))


# ---------------------------------------------------------------- pose from animations


@dataclass
class BonePose:
    rot: list[float]
    pos: list[float]
    scale: list[float]


def _channel(v: Json, env: Env, this: list[float]) -> list[float] | None:
    """First keyframe of a channel; `this` = the bone's current value (bind pose)."""
    if isinstance(v, dict):  # keyframes: first one
        try:
            first = min(v, key=lambda k: float(k))
        except ValueError:
            return None
        v = v[first]
        if isinstance(v, dict):
            v = v.get("post", v.get("pre"))
    if isinstance(v, (int, float, str)):
        v = [v, v, v]
    if not isinstance(v, list) or len(v) != 3:
        return None
    try:
        return [num(evaluate(x, Env(lambda n, a, i=i: this[i] if n == "this" else env.lookup(n, a), env.arrays)))
                for i, x in enumerate(v)]
    except (SyntaxError, KeyError, ValueError, ZeroDivisionError):
        return None


def pose(mob: Mob, env: Env, anims: dict[str, Json], acs: dict[str, Json],
         bind: dict[str, Json]) -> dict[str, BonePose]:
    """Static pose of the entity's animations at time 0; `bind` = bones of the geometry by lower-case name."""
    out: dict[str, BonePose] = {}
    seen: set[str] = set()

    def run_entry(entry: Json) -> None:
        if isinstance(entry, str):
            key, cond = entry, None
        else:
            key, cond = next(iter(entry.items()))
        if cond is not None:
            try:
                if not truthy(evaluate(cond, env)):
                    return
            except (SyntaxError, KeyError):
                return
        ident = mob.keys["animations"].get(key.lower(), key)
        if ident in seen:
            return
        seen.add(ident)
        if ident in acs:
            ac = acs[ident]
            states = ac.get("states") or {}
            st = states.get(ac.get("initial_state", "default")) or {}
            for e in st.get("animations") or []:
                run_entry(e)
            return
        a = anims.get(ident)
        if not a:
            return
        for bone, ch in (a.get("bones") or {}).items():
            bp = out.setdefault(bone.lower(), BonePose([0, 0, 0], [0, 0, 0], [1, 1, 1]))
            b0 = bind.get(bone.lower()) or {}
            rot0 = [float(x) for x in b0.get("rotation", [0, 0, 0])]
            r = _channel(ch.get("rotation"), env, rot0) if "rotation" in ch else None
            p = _channel(ch.get("position"), env, [0.0, 0.0, 0.0]) if "position" in ch else None
            s = _channel(ch.get("scale"), env, [1.0, 1.0, 1.0]) if "scale" in ch else None
            if r:
                bp.rot = [bp.rot[i] + r[i] for i in range(3)]
            if p:
                bp.pos = [bp.pos[i] + p[i] for i in range(3)]
            if s:
                bp.scale = [bp.scale[i] * s[i] for i in range(3)]

    for entry in mob.animate:
        run_entry(entry)
    return out


# ---------------------------------------------------------------- faces

SHADE = {"up": 1.0, "north": 0.85, "south": 0.85, "east": 0.7, "west": 0.7, "down": 0.55}
NORMAL: dict[str, Vec] = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0),
                          "up": (0, 1, 0), "down": (0, -1, 0)}


@dataclass
class Face:
    p0: Vec          # world corner at texture (u0, v0)
    pu: Vec          # corner at (u0 + du, v0)
    pv: Vec          # corner at (u0, v0 + dv)
    uv: tuple[float, float, float, float]   # u0, v0, du, dv (texture units, may be negative)
    shade: float
    normal: Vec
    tex: int         # index of the texture pass


def cube_faces_world(c: Json, m: Mat, tw: float, th: float, bone_mirror: bool, tex: int) -> list[Face]:
    o, s = c["origin"], c["size"]
    inf = float(c.get("inflate", 0))
    x0 = -(float(o[0]) + float(s[0])) - inf  # Bedrock -> Blockbench
    x1 = -float(o[0]) + inf
    y0, y1 = float(o[1]) - inf, float(o[1]) + float(s[1]) + inf
    z0, z1 = float(o[2]) - inf, float(o[2]) + float(s[2]) + inf
    if "rotation" in c:
        # no cube pivot: Bedrock rotates the cube about its own centre (vanilla chicken body)
        piv = bb(c.get("pivot") or [float(o[i]) + float(s[i]) / 2 for i in range(3)])
        m = mat_mul(m, about(piv, rot_bb(*[float(x) for x in c["rotation"]])))
    corners = {  # p0, pu, pv per face (Blockbench box-UV orientation)
        "north": ((x1, y1, z0), (x0, y1, z0), (x1, y0, z0)),
        "south": ((x0, y1, z1), (x1, y1, z1), (x0, y0, z1)),
        "east": ((x1, y1, z1), (x1, y1, z0), (x1, y0, z1)),
        "west": ((x0, y1, z0), (x0, y1, z1), (x0, y0, z0)),
        "up": ((x1, y1, z1), (x0, y1, z1), (x1, y1, z0)),
        "down": ((x1, y0, z0), (x0, y0, z0), (x1, y0, z1)),
    }
    w, h, d = (abs(float(v)) for v in s)
    uv = c.get("uv", [0, 0])
    rects: dict[str, tuple[float, float, float, float]] = {}
    if isinstance(uv, dict):
        for k, f in uv.items():
            if k not in corners:
                continue
            (u, v), (du, dv) = f["uv"], f.get("uv_size", [w, h])
            u, v, du, dv = float(u), float(v), float(du), float(dv)
            if k in ("up", "down"):  # Bedrock per-face up/down are rotated 180° vs. Blockbench
                u, v, du, dv = u + du, v + dv, -du, -dv
            rects[k] = (u, v, du, dv)
    else:
        u, v = float(uv[0]), float(uv[1])
        mirror = bool(c.get("mirror", bone_mirror))
        rects = {"up": (u + d, v, w, d), "down": (u + d + w, v, w, d), "north": (u + d, v + d, w, h),
                 "south": (u + 2 * d + w, v + d, w, h), "east": (u, v + d, d, h), "west": (u + d + w, v + d, d, h)}
        if mirror:
            rects["east"], rects["west"] = rects["west"], rects["east"]
            rects = {k: (r[0] + r[2], r[1], -r[2], r[3]) for k, r in rects.items()}
    out: list[Face] = []
    rot_only = [row[:3] + [0.0] for row in m[:3]] + [[0, 0, 0, 1]]
    for k, (p0, pu, pv) in corners.items():
        if k not in rects or rects[k][2] == 0 or rects[k][3] == 0:
            continue
        n = apply(rot_only, NORMAL[k])
        out.append(Face(apply(m, p0), apply(m, pu), apply(m, pv), rects[k], SHADE[k], n, tex))
    return out


def model_faces(bones: list[Json], desc: Json, poses: dict[str, BonePose], layer: Layer, tex_count: int) -> list[Face]:
    tw = float(desc.get("texture_width", 64))
    th = float(desc.get("texture_height", 64))
    by = {b["name"].lower(): b for b in bones}
    world: dict[str, Mat] = {}
    visible: dict[str, bool] = {}

    def mat_of(name: str, depth: int = 0) -> Mat:
        if name in world:
            return world[name]
        b = by[name]
        parent = (b.get("parent") or "").lower()
        pm = mat_of(parent, depth + 1) if parent in by and depth < 64 else translate(0, 0, 0)
        piv = bb(b.get("pivot", [0, 0, 0]))
        rot = [float(x) for x in b.get("rotation", [0, 0, 0])]
        bind = b.get("bind_pose_rotation")  # 1.8 rest rotation (zombie villager hat brim)
        if bind:
            rot = [rot[i] + float(bind[i]) for i in range(3)]
        ps = poses.get(name)
        local = translate(0, 0, 0)
        if ps:
            local = translate(*bb(ps.pos))
            rot = [rot[i] + ps.rot[i] for i in range(3)]
        r = rot_bb(*rot)
        if ps and ps.scale != [1, 1, 1]:
            r = mat_mul(r, scale_m(*ps.scale))
        world[name] = mat_mul(pm, mat_mul(local, about(piv, r)))
        return world[name]

    def vis(name: str, depth: int = 0) -> bool:
        """part_visibility is inherited by the children; neverRender is not (it only hides the bone's own
        cubes: the zombie villager's waist has it and is the parent of the whole body)."""
        if name not in visible:
            parent = (by[name].get("parent") or "").lower()
            ok = bone_visible(layer, by[name]["name"])
            visible[name] = ok and (vis(parent, depth + 1) if parent in by and depth < 64 else True)
        return visible[name]

    faces: list[Face] = []
    for name, b in by.items():
        if not b.get("cubes") or b.get("neverRender") or not vis(name):
            continue
        m = mat_of(name)
        for c in b["cubes"]:
            for t in range(tex_count):
                faces.extend(cube_faces_world(c, m, tw, th, bool(b.get("mirror")), t))
    return faces


# ---------------------------------------------------------------- rasterizer


class Camera:
    def __init__(self, yaw: float, pitch: float):
        cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
        pos = (sy * cp, sp, -cy * cp)                 # camera direction from the model (front = -Z)
        f = (-pos[0], -pos[1], -pos[2])
        r = (f[1] * 0 - f[2] * 1, f[2] * 0 - f[0] * 0, f[0] * 1 - f[1] * 0)  # f x up
        rl = math.sqrt(sum(x * x for x in r)) or 1
        self.r: Vec = (r[0] / rl, r[1] / rl, r[2] / rl)
        self.u: Vec = (self.r[1] * f[2] - self.r[2] * f[1], self.r[2] * f[0] - self.r[0] * f[2], self.r[0] * f[1] - self.r[1] * f[0])
        self.f: Vec = f

    def project(self, p: Vec) -> Vec:
        dot = lambda a, b: a[0] * b[0] + a[1] * b[1] + a[2] * b[2]  # noqa: E731
        return dot(p, self.r), dot(p, self.u), dot(p, self.f)


VIEWS = {"front": (35.0, 25.0), "back": (215.0, 25.0), "side": (90.0, 10.0), "top": (20.0, 70.0)}


def rasterize(faces: list[Face], textures: list[tuple[Image.Image, float, float]], cam: Camera, size: int) -> Image.Image:
    """textures: (image, uv width, uv height of its geometry)."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    if not faces:
        return img
    proj = [(cam.project(f.p0), cam.project(f.pu), cam.project(f.pv)) for f in faces]
    xs = [p[i][0] for p in proj for i in range(3)] + [p[1][0] + p[2][0] - p[0][0] for p in proj]
    ys = [p[i][1] for p in proj for i in range(3)] + [p[1][1] + p[2][1] - p[0][1] for p in proj]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    k = (size - 8) / max(maxx - minx, maxy - miny, 1e-6)
    ox = (size - (maxx - minx) * k) / 2 - minx * k
    oy = (size - (maxy - miny) * k) / 2 + maxy * k
    zbuf = [[math.inf] * size for _ in range(size)]
    px = img.load()
    assert px is not None
    tpx = [t[0].load() for t in textures]
    if any(t is None for t in tpx):
        return img
    order = sorted(range(len(faces)), key=lambda i: faces[i].tex)  # overlays after base pass
    for i in order:
        f = faces[i]
        if f.normal[0] * cam.f[0] + f.normal[1] * cam.f[1] + f.normal[2] * cam.f[2] >= -1e-6:
            continue  # back face
        tex, tw, th = textures[f.tex]
        tp = tpx[f.tex]
        sx_t, sy_t = tex.width / tw, tex.height / th
        (ax, ay, az), (bx, by_, bz), (cx, cy, cz) = proj[i]
        p0 = (ox + ax * k, oy - ay * k)
        eu = (ox + bx * k - p0[0], oy - by_ * k - p0[1])
        ev = (ox + cx * k - p0[0], oy - cy * k - p0[1])
        det = eu[0] * ev[1] - eu[1] * ev[0]
        if abs(det) < 1e-9:
            continue
        dz_u, dz_v = bz - az, cz - az
        u0, v0, du, dv = f.uv
        corners_x = (p0[0], p0[0] + eu[0], p0[0] + ev[0], p0[0] + eu[0] + ev[0])
        corners_y = (p0[1], p0[1] + eu[1], p0[1] + ev[1], p0[1] + eu[1] + ev[1])
        x_lo, x_hi = max(int(min(corners_x)), 0), min(int(max(corners_x)) + 1, size)
        y_lo, y_hi = max(int(min(corners_y)), 0), min(int(max(corners_y)) + 1, size)
        bias = 1e-3 * f.tex
        for y in range(y_lo, y_hi):
            row = zbuf[y]
            qy = y + 0.5 - p0[1]
            for x in range(x_lo, x_hi):
                qx = x + 0.5 - p0[0]
                a = (qx * ev[1] - qy * ev[0]) / det
                if a < 0 or a > 1:
                    continue
                b = (eu[0] * qy - eu[1] * qx) / det
                if b < 0 or b > 1:
                    continue
                z = az + a * dz_u + b * dz_v - bias
                if z >= row[x]:
                    continue
                tu = int((u0 + a * du) * sx_t - (1e-4 if du < 0 else 0))
                tv = int((v0 + b * dv) * sy_t - (1e-4 if dv < 0 else 0))
                if not (0 <= tu < tex.width and 0 <= tv < tex.height):
                    continue
                c = tp[tu, tv]  # type: ignore[index]
                if not isinstance(c, tuple) or c[3] < 100:
                    continue
                row[x] = z
                s = f.shade
                px[x, y] = (int(c[0] * s), int(c[1] * s), int(c[2] * s), 255)
    return img


# ---------------------------------------------------------------- scene


class Renderer:
    def __init__(self) -> None:
        rp = find_pack("RP")
        self.rp = rp
        self.geos: tuple[dict[str, Geo], dict[str, Geo]] = (geo_index(rp), geo_index(VRP))
        self.anims: dict[str, Json] = {}
        self.acs: dict[str, Json] = {}
        for base in (VRP, rp):
            for name, f in keyed_ids(base, "animations", "animations").items():
                self.anims[name] = load(f)["animations"][name]
            for name, f in keyed_ids(base, "animation_controllers", "animation_controllers").items():
                self.acs[name] = load(f)["animation_controllers"][name]
        self._tex: dict[str, Image.Image | None] = {}

    def texture(self, path: str) -> Image.Image | None:
        if path not in self._tex:
            f = texture_file(path, [self.rp, VRP])
            self._tex[path] = Image.open(f).convert("RGBA") if f and not f.endswith(".json") else None
        return self._tex[path]

    def draw(self, mob: Mob, st: State, view: str, size: int, use_pose: bool) -> tuple[Image.Image, list[Layer], set[str]]:
        _, layers, errors = mob.run(st)
        env = mob.last_env
        cam = Camera(*VIEWS[view])
        canvas_faces: list[Face] = []
        textures: list[tuple[Image.Image, float, float]] = []
        # all layers share one z-buffer: merge them, remapping texture indices
        for lay in layers:
            if not lay.geometry or "empty" in lay.geometry:
                continue
            try:
                desc, bones = resolve_geo(lay.geometry, *self.geos)
            except KeyError:
                errors.add(f"geometry {lay.geometry} not found")
                continue
            imgs = [self.texture(t) for t in lay.textures]
            if not imgs or any(i is None for i in imgs):
                errors.add(f"{lay.rc}: texture not found {lay.textures}")
                continue
            tw = float(desc.get("texture_width", 64))
            th = float(desc.get("texture_height", 64))
            base = len(textures)
            for im in imgs:
                assert im is not None
                textures.append((im, tw, th))
            bind = {b["name"].lower(): b for b in bones}
            if use_pose and any(b.get("reset") for b in bones):
                errors.add(f"note: {lay.geometry} has legacy 'reset' bones; its animated pose is approximate (try --nopose)")
            poses = pose(mob, env, self.anims, self.acs, bind) if use_pose and env else {}
            for fc in model_faces(bones, desc, poses, lay, len(imgs)):
                fc.tex += base
                canvas_faces.append(fc)
        return rasterize(canvas_faces, textures, cam, size), layers, errors


def label(layers: list[Layer]) -> str:
    parts: list[str] = []
    for lay in layers:
        if not lay.geometry or "empty" in lay.geometry:
            continue
        g = lay.geometry.replace("geometry.", "").replace("mv.", "")
        t = "+".join(os.path.basename(x) for x in lay.textures)
        parts.append(f"{g}:{t}")
    return " | ".join(parts)


def parse_kv(items: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for it in items:
        k, _, v = it.partition("=")
        out[k.strip()] = v.strip()
    return out


def main() -> int:
    require_vanilla()
    argv = sys.argv[1:]
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    mob_name = argv[0]
    opts: dict[str, list[str]] = {}
    i = 1
    flags = {"--nobp", "--nopose"}
    while i < len(argv):
        a = argv[i]
        if a in flags:
            opts.setdefault(a, []).append("1")
            i += 1
        else:
            opts.setdefault(a, []).append(argv[i + 1] if i + 1 < len(argv) else "")
            i += 2
    f = os.path.join(find_pack("RP"), "entity", f"{mob_name}.entity.json")
    if not os.path.exists(f):
        print("no entity", f)
        return 2
    mob = Mob(f)
    queries: dict[str, Value] = {}
    climate = "temperate"
    for k, v in parse_kv(opts.get("--q", [])).items():
        if k == "climate":
            climate = v
            continue
        k = k.lower().replace("query.", "").replace("q.", "", 1) if k.lower().startswith(("q.", "query.")) else k.lower()
        try:
            queries[k] = float(v)
        except ValueError:
            queries[k] = v
    size = int(opts.get("--size", ["256"])[0])
    limit = int(opts.get("--max", ["30"])[0])
    views = list(VIEWS) if opts.get("--view", ["front"])[0] == "all" else [opts.get("--view", ["front"])[0]]
    use_pose = "--nopose" not in opts

    states: list[tuple[float, State]] = []
    forced = {k: int(v) for k, v in parse_kv(opts.get("--bp", [])).items()}
    ent = bp_entity(mob.ident)
    if forced:
        props = {p: 0 for p in ((ent or {}).get("description", {}).get("properties") or {}) if p.startswith("mv:")}
        props.update(forced)
        states.append((1.0, State(props, queries=queries, climate=climate)))
    elif ent and "--nobp" not in opts:
        for p, props in spawn_distribution(ent):
            states.append((p, State(props, queries=queries, climate=climate)))
    else:
        for x in range(100):
            states.append((0.01, State(None, {"xvar": x + 0.5, "yvar": x + 0.5, "zvar": (x * 7 % 100) + 0.5},
                                       queries=queries, climate=climate)))

    # group identical outfits
    groups: dict[str, tuple[float, State, list[Layer]]] = {}
    errors: set[str] = set()
    for p, st in states:
        _, layers, errs = mob.run(st)
        errors |= errs
        key = repr([(lay.geometry, lay.textures, lay.part_visibility) for lay in layers])
        if key in groups:
            groups[key] = (groups[key][0] + p, groups[key][1], groups[key][2])
        else:
            groups[key] = (p, st, layers)
    chosen = sorted(groups.values(), key=lambda g: -g[0])[:limit]

    r = Renderer()
    tiles: list[tuple[Image.Image, str]] = []
    for p, st, layers in chosen:
        bpdesc = " ".join(f"{k.removeprefix('mv:')}={v}" for k, v in (st.bp or {}).items())
        for view in views:
            img, _, errs = r.draw(mob, st, view, size, use_pose)
            errors |= errs
            tiles.append((img, f"{p:.1%} {bpdesc}\n{label(layers)}"))
    cols = min(len(tiles), 6 if len(views) == 1 else len(views) * max(1, 6 // len(views)))
    rows = math.ceil(len(tiles) / max(cols, 1))
    lab_h = 30
    sheet = Image.new("RGBA", (max(cols, 1) * size, max(rows, 1) * (size + lab_h)), (40, 44, 52, 255))
    d = ImageDraw.Draw(sheet)
    for n, (img, text) in enumerate(tiles):
        x, y = (n % cols) * size, (n // cols) * (size + lab_h)
        checker = Image.new("RGBA", (size, size), (70, 76, 88, 255))
        sheet.paste(checker, (x, y))
        sheet.alpha_composite(img, (x, y))
        d.text((x + 3, y + size + 2), _fit(text, size), fill=(230, 230, 230, 255))
    out = opts.get("--out", [os.path.join(ROOT, "tools", "out", f"{mob_name}.png")])[0]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sheet.convert("RGB").save(out)
    print(f"{len(tiles)} tiles ({len(groups)} distinct outfits) -> {out}")
    for e in sorted(errors):
        print("  " + (e if e.startswith("note:") else "ERROR " + e))
    return 1 if any(not e.startswith("note:") for e in errors) else 0


def _fit(text: str, width: int) -> str:
    chars = max(width // 6, 10)
    return "\n".join(line[:chars] for line in text.split("\n"))


if __name__ == "__main__":
    sys.exit(main())
