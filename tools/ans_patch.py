"""Build a local compatibility resource pack "Mob Variants x Actions & Stuff" (A&S) from the A&S pack
installed by the user. Nothing of A&S goes into git: the output folder is ignored (dist/).

    python tools/ans_patch.py [mob ...] [--ans DIR] [--subpack SP0] [--out DIR] [--install]

  mob            mobs of RP/entity to merge (default: every mob the tool supports)
  --ans DIR      A&S resource pack (folder with manifest.json and __brarchive/; default Action_Stuff)
  --subpack SP   A&S subpack the user plays with (default SP0, the one with vanilla textures)
  --out DIR      output pack (default dist/MV_ANS_RP)
  --install      also make a junction to the output in development_resource_packs (Windows)

Per mob: A&S client entity (subpack over root) + our texture keys, local roll (initialize), gate
(pre_animation) and, in place of the A&S body render controller, two entries: the A&S one with
`!v.mv_active` and `controller.render.mv.ans.<mob>` (a copy of it where `Texture.default` becomes our
skin array) with `v.mv_active`. Model and animations stay A&S. The BP of Mob Variants is unchanged.
Skins are checked against the A&S model: UV rectangles that A&S draws but vanilla does not (extra cubes,
e.g. the zombie's shoulder/foot pads on the hat area) get the pixels of the vanilla texture, so a skin's
hat does not show up on them; those skins are written to textures/mv_ans/<mob>/ in the output pack.
Pack order in the game: MV x A&S on top, then A&S, then Mob Variants RP at the bottom (its entities would
hide the A&S ones of the mobs not merged yet; from below it still gives the textures). BP as usual.
"""
from __future__ import annotations

import copy
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import uuid
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import (ROOT, VRP, Json, cube_faces, find_pack, geo_index, keyed_ids, load, rc_list, rel,  # noqa: E402
                   require_vanilla, resolve_geo, save, texture_file, vanilla_client_entity)

CACHE = os.path.join(ROOT, "out", "ans")
NS = uuid.UUID("6f1c6c1e-2b0e-4b8e-9f43-6d7a1e0c5a11")


# ---------------------------------------------------------------- A&S extraction


def unbrarchive(path: str, out: str) -> int:
    """Extract one .brarchive (Mojang pack archive: 16-byte header, 256-byte entries, then data)."""
    data = open(path, "rb").read()
    n = struct.unpack_from("<I", data, 8)[0]
    base = 16 + n * 256
    for i in range(n):
        e = 16 + i * 256
        name = data[e + 1:e + 1 + data[e]].decode("utf-8")
        off, size = struct.unpack_from("<II", data, e + 248)
        dst = os.path.join(out, name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as fh:
            fh.write(data[base + off:base + off + size])
    return n


def extract(ans: str, subpack: str) -> str:
    """A&S root with the subpack on top, as loose files in out/ans/<subpack> (cached per A&S version)."""
    version = json.load(open(os.path.join(ans, "manifest.json"), encoding="utf-8"))["header"]["version"]
    dst = os.path.join(CACHE, subpack)
    stamp = os.path.join(dst, ".version")
    if os.path.exists(stamp) and open(stamp, encoding="utf-8").read() == f"{version}":
        return dst
    shutil.rmtree(dst, ignore_errors=True)
    for src in (os.path.join(ans, "__brarchive"), os.path.join(ans, "subpacks", subpack, "__brarchive")):
        if not os.path.isdir(src):
            raise SystemExit(f"not found: {src}")
        for dp, _, fs in os.walk(src):
            for f in fs:
                if f.endswith(".brarchive"):
                    p = os.path.join(dp, f)
                    unbrarchive(p, os.path.join(dst, os.path.relpath(p, src)[:-len(".brarchive")]))
    with open(stamp, "w", encoding="utf-8") as fh:
        fh.write(f"{version}")
    return dst


# ---------------------------------------------------------------- merge


def ans_entities(base: str) -> dict[str, tuple[str, Json]]:
    out: dict[str, tuple[str, Json]] = {}
    for dp, _, fs in os.walk(os.path.join(base, "entity")):
        for f in fs:
            d = load(os.path.join(dp, f))
            ce = d.get("minecraft:client_entity")
            if ce:
                out[ce["description"]["identifier"]] = (os.path.join(dp, f), d)
    return out


def all_false(rc: Json) -> bool:
    pv = rc.get("part_visibility") or []
    return pv == [{"*": False}] or pv == [{"*": "0"}]


def face_rects(bones: list[dict[str, Any]]) -> set[tuple[float, ...]]:
    return {r for b in bones for c in b.get("cubes") or [] for r in cube_faces(c).values() if r[2] and r[3]}


def merge(mob: str, ctx: dict[str, Any]) -> list[str]:
    """Write the merged entity, render controller and textures of `mob`. Returns warnings (empty: OK)."""
    rp, out = ctx["rp"], ctx["out"]
    mv = load(os.path.join(rp, "entity", f"{mob}.entity.json"))["minecraft:client_entity"]["description"]
    ident = mv["identifier"]
    if ident not in ctx["ans_ents"]:
        return [f"A&S has no client entity {ident}"]
    _, ans_doc = ctx["ans_ents"][ident]
    doc = copy.deepcopy(ans_doc)
    d = doc["minecraft:client_entity"]["description"]

    # our skin array and the expression that replaces Texture.default
    own = [n for n, _ in rc_list(mv) if n.startswith("controller.render.mv.")]
    if len(own) != 1:
        return [f"{len(own)} own render controllers (only 1 supported)"]
    mvrc = load(ctx["rcs"][own[0]])["render_controllers"][own[0]]
    arrays = (mvrc.get("arrays") or {}).get("textures") or {}
    if list(arrays) != ["array.mv_skins"]:
        return [f"texture arrays {list(arrays)} (only array.mv_skins supported)"]
    m = re.search(r"array\.mv_skins\[[^\]]+\]", " ".join(mvrc.get("textures", [])), re.I)
    if not m:
        return ["array.mv_skins not used in the textures of our render controller"]
    skin_expr = m.group(0)

    # A&S must use the vanilla texture (same UV) as Texture.default
    van = vanilla_client_entity(ident)
    vtex = (van[1]["minecraft:client_entity"]["description"].get("textures") or {}).get("default") if van else None
    atex = (d.get("textures") or {}).get("default")
    if not vtex or atex != vtex:
        return [f"A&S Texture.default is {atex!r}, not the vanilla {vtex!r}: this subpack has its own skin"]

    # A&S body render controller: draws Geometry.default with Texture.default and is not hidden
    body = None
    for i, (n, cond) in enumerate(rc_list(d)):
        rc = ctx["ans_rcs"].get(n)
        if rc and not all_false(rc) and "Texture.default" in json.dumps(rc.get("textures")) \
                and "Geometry.default" in json.dumps(rc.get("geometry")):
            if body is not None:
                return [f"two candidate body render controllers: {body[1]} and {n}"]
            body = (i, n, cond, rc)
    if body is None:
        return ["no A&S body render controller (Geometry.default + Texture.default) found"]
    idx, bname, bcond, brc = body
    if "Texture.default" in json.dumps(brc.get("arrays") or {}):
        return [f"{bname}: Texture.default inside an array (not supported yet)"]
    myrc = copy.deepcopy(brc)
    myrc["textures"] = [re.sub(r"\bTexture\.default\b", skin_expr, t) for t in brc["textures"]]
    myrc.setdefault("arrays", {}).setdefault("textures", {})["array.mv_skins"] = arrays["array.mv_skins"]
    myname = f"controller.render.mv.ans.{mob}"
    base_cond = f"({bcond})" if bcond not in (None, True, "true", "1") else ""
    entries = d["render_controllers"]
    entries[idx] = {bname: f"{base_cond} && !v.mv_active" if base_cond else "!v.mv_active"}
    entries.insert(idx + 1, {myname: f"{base_cond} && v.mv_active" if base_cond else "v.mv_active"})

    # scripts: our roll and gate
    mvs, sc = mv.get("scripts") or {}, d.setdefault("scripts", {})
    sc["initialize"] = (sc.get("initialize") or []) + [x for x in mvs.get("initialize") or [] if "v.xvar" in x]
    sc["pre_animation"] = [x for x in mvs.get("pre_animation") or [] if x.startswith("v.mv_")] + (sc.get("pre_animation") or [])

    # textures: our keys; skins fixed for the A&S model when needed
    warn: list[str] = []
    try:
        fixed = fix_regions(d, van, ctx)
    except (KeyError, ValueError) as e:
        return [f"A&S model: {e}"]
    for k, path in (mv.get("textures") or {}).items():
        if not k.startswith("mv_"):
            continue
        d["textures"][k] = path
        if fixed:
            src = texture_file(path, [rp, VRP])
            new = paint_regions(src, fixed, ctx, mob) if src and src.endswith(".png") else None
            if new:
                d["textures"][k] = new
    for sub in ("entity", "render_controllers"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    save(os.path.join(out, "entity", f"{mob}.entity.json"), doc)
    save(os.path.join(out, "render_controllers", f"{mob}.render_controllers.json"),
         {"format_version": "1.10.0", "render_controllers": {myname: myrc}})
    ctx["log"].append(f"{mob}: {bname} -> {myname}; {len([k for k in d['textures'] if k.startswith('mv_')])} skins, "
                      f"{ctx['painted'].get(mob, 0)} fixed for the A&S model")
    return warn


def fix_regions(d: Json, van: Any, ctx: dict[str, Any]) -> tuple[Any, ...] | None:
    """(vanilla texture file, rects drawn only by A&S, rects drawn by both) or None if nothing to fix."""
    vd = van[1]["minecraft:client_entity"]["description"]
    vgeo = resolve_geo(vd["geometry"]["default"], ctx["vgeo"])
    agid = d["geometry"]["default"]
    ageo = resolve_geo(agid, ctx["ans_geo"])
    if (ageo[0].get("texture_width"), ageo[0].get("texture_height")) != (vgeo[0].get("texture_width"), vgeo[0].get("texture_height")):
        raise ValueError(f"{agid}: texture size differs from vanilla")
    vr, ar = face_rects(vgeo[1]), face_rects(ageo[1])
    only = sorted(ar - vr)
    if not only:
        return None
    vtex = texture_file(vd["textures"]["default"], [VRP])
    return (vtex, ageo[0], only, sorted(ar & vr))


def paint_regions(src: str, fixed: Any, ctx: dict[str, Any], mob: str) -> str | None:
    from PIL import Image
    vtex, desc, only, shared = fixed
    im = Image.open(src).convert("RGBA")
    vim = Image.open(vtex).convert("RGBA").resize(im.size, Image.Resampling.NEAREST)
    sx, sy = im.width / desc["texture_width"], im.height / desc["texture_height"]

    def inside(x: int, y: int, rects: list[tuple[float, ...]]) -> bool:
        return any(u * sx <= x < (u + w) * sx and v * sy <= y < (v + h) * sy for u, v, w, h in rects)

    changed = False
    for u, v, w, h in only:
        for x in range(int(u * sx), int((u + w) * sx)):
            for y in range(int(v * sy), int((v + h) * sy)):
                if 0 <= x < im.width and 0 <= y < im.height and not inside(x, y, shared):
                    px = vim.getpixel((x, y))
                    if px is not None and im.getpixel((x, y)) != px:
                        im.putpixel((x, y), px)
                        changed = True
    if not changed:
        return None
    name = os.path.splitext(os.path.basename(src))[0]
    path = f"textures/mv_ans/{mob}/{name}"
    os.makedirs(os.path.join(ctx["out"], os.path.dirname(path)), exist_ok=True)
    im.save(os.path.join(ctx["out"], path + ".png"))
    ctx["painted"][mob] = ctx["painted"].get(mob, 0) + 1
    return path


# ---------------------------------------------------------------- pack


def write_manifest(out: str, rp: str, subpack: str, ans_version: str) -> None:
    os.makedirs(out, exist_ok=True)
    mvm = load(os.path.join(rp, "manifest.json"))
    v = mvm["header"]["version"]
    save(os.path.join(out, "manifest.json"), {
        "format_version": 2,
        "header": {"name": f"Mob Variants x Actions & Stuff ({subpack})",
                   "description": f"Local compatibility pack, generated by tools/ans_patch.py for A&S {ans_version}.",
                   "uuid": str(uuid.uuid5(NS, f"header-{subpack}")), "version": v,
                   "min_engine_version": mvm["header"]["min_engine_version"]},
        "modules": [{"type": "resources", "uuid": str(uuid.uuid5(NS, f"module-{subpack}")), "version": v}],
        "dependencies": [{"uuid": mvm["header"]["uuid"], "version": v}]})
    icon = os.path.join(rp, "pack_icon.png")
    if os.path.exists(icon):
        shutil.copyfile(icon, os.path.join(out, "pack_icon.png"))


def install(out: str) -> None:
    dev = os.path.join(os.environ.get("APPDATA", ""), "Minecraft Bedrock", "Users", "Shared", "games", "com.mojang",
                       "development_resource_packs")
    link = os.path.join(dev, os.path.basename(out))
    if os.path.exists(link):
        print("already installed:", link)
        return
    subprocess.run(["cmd", "/c", "mklink", "/J", link, os.path.abspath(out)], check=True)


def main() -> int:
    require_vanilla()
    argv = sys.argv[1:]
    opts: dict[str, str] = {}
    mobs: list[str] = []
    i = 0
    while i < len(argv):
        if argv[i] == "--install":
            opts["--install"] = "1"
            i += 1
        elif argv[i].startswith("--"):
            opts[argv[i]] = argv[i + 1]
            i += 2
        else:
            mobs.append(argv[i])
            i += 1
    ans = opts.get("--ans", os.path.join(ROOT, "Action_Stuff"))
    subpack = opts.get("--subpack", "SP0")
    out = opts.get("--out", os.path.join(ROOT, "dist", "MV_ANS_RP"))
    rp = find_pack("RP")
    base = extract(ans, subpack)
    ans_rcs: dict[str, Json] = {}
    for f in sorted(os.listdir(os.path.join(base, "render_controllers"))):
        ans_rcs.update(load(os.path.join(base, "render_controllers", f)).get("render_controllers") or {})
    shutil.rmtree(out, ignore_errors=True)
    ctx: dict[str, Any] = {"rp": rp, "out": out, "ans": base, "ans_ents": ans_entities(base), "ans_rcs": ans_rcs,
                           "rcs": keyed_ids(rp, "render_controllers", "render_controllers"),
                           "vgeo": geo_index(VRP), "ans_geo": geo_index(base), "painted": {}, "log": []}
    mobs = mobs or sorted(os.path.basename(f).split(".")[0] for f in os.listdir(os.path.join(rp, "entity")))
    skipped = []
    for mob in mobs:
        warns = merge(mob, ctx)
        if warns:
            skipped.append(f"{mob}: {'; '.join(warns)}")
    ans_version = str(load(os.path.join(ans, "manifest.json"))["header"]["version"])
    write_manifest(out, rp, subpack, ans_version)
    for line in ctx["log"]:
        print(line)
    for line in skipped:
        print("skip", line)
    print(f"{len(ctx['log'])} mobs -> {rel(out)}")
    if "--install" in opts:
        install(out)
    return 0 if ctx["log"] else 1


if __name__ == "__main__":
    sys.exit(main())
