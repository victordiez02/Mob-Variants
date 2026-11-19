"""Add a skin to a mob that uses the standard variant pattern, in every file at once.

    python -I tools/addskin.py <mob> <png> [--array array.xskins] [--key mv_defaultN] [--weight W] [--dry-run]

Steps (the four places that are easy to forget by hand):
1. copies the PNG to RP/textures/entity/<mob>/ (unless it is already inside RP/);
2. adds `"<key>": "<texture path>"` to the client entity (default key: next free mv_defaultN);
3. appends `Texture.<key>` to the array of controller.render.mv.<mob> (default: its first texture array);
4. if the render controller reads that array as `array[v.mv_variant - 1]`: raises the local roll of the
   entity (`v.xvar = math.random_integer(1, N)`, used without BP) and, if the mob has a BP, widens the
   range of mv:variant and adds `{weight, set_property: {mv:variant: N}}` to every randomize that sets
   mv:variant (entity_spawned, entity_born, entity_transformed; default weight: the last entry's).
Mobs with a second skin array (bee angry, ghast charging, pig saddled): add that texture by hand.
Then run: python -I tools/check.py <mob> and python tools/render.py <mob> --bp mv:variant=N
"""
from __future__ import annotations

import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import Json, files, find_pack, load_for_edit, rel, save  # noqa: E402


def opt(args: list[str], name: str) -> str | None:
    return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else None


def variant_randomizes(node: Json, out: list[list[Json]]) -> list[list[Json]]:
    """Every randomize list (in any event) whose entries set mv:variant."""
    if isinstance(node, dict):
        rnd = node.get("randomize")
        if isinstance(rnd, list) and any("mv:variant" in (o.get("set_property") or {}) for o in rnd):
            out.append(rnd)
        for v in node.values():
            variant_randomizes(v, out)
    elif isinstance(node, list):
        for v in node:
            variant_randomizes(v, out)
    return out


def main() -> int:
    args = sys.argv[1:]
    pos = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or not args[i - 1].startswith("--"))]
    if len(pos) < 2:
        print(__doc__)
        return 2
    mob, png = pos[0], pos[1]
    dry = "--dry-run" in args
    rp, bp = find_pack("RP"), find_pack("BP")
    ent_file = os.path.join(rp, "entity", f"{mob}.entity.json")
    if not os.path.exists(ent_file) or not os.path.exists(png):
        print("missing", ent_file if not os.path.exists(ent_file) else png)
        return 2
    ent, ent_head = load_for_edit(ent_file)
    desc = ent["minecraft:client_entity"]["description"]
    textures: dict[str, str] = desc.setdefault("textures", {})

    # 1. texture path
    png_abs = os.path.abspath(png)
    if png_abs.startswith(os.path.abspath(rp) + os.sep):
        tex_path = os.path.splitext(os.path.relpath(png_abs, rp))[0].replace("\\", "/")
        copy_to = None
    else:
        tex_path = f"textures/entity/{mob}/{os.path.splitext(os.path.basename(png))[0]}"
        copy_to = os.path.join(rp, tex_path + ".png")
        if os.path.exists(copy_to):
            print(f"{rel(copy_to)} already exists; rename the PNG")
            return 2
    if tex_path in textures.values():
        print(f"{tex_path} is already used by the entity")
        return 2

    # 2. key
    key = opt(args, "--key")
    if not key:
        n = 1
        while (f"mv_default{n}" if n > 1 else "mv_default") in textures:
            n += 1
        key = f"mv_default{n}" if n > 1 else "mv_default"
    if key in textures:
        print(f"key {key} already exists")
        return 2
    textures[key] = tex_path

    # 3. render controller array
    rc_name = f"controller.render.mv.{mob}"
    rc_file = next((f for f in files(rp, "render_controllers") if rc_name in open(f, encoding="utf-8-sig").read()), None)
    if rc_file is None:
        print("no render controller", rc_name)
        return 2
    rcs, rc_head = load_for_edit(rc_file)
    rc = rcs["render_controllers"][rc_name]
    arrays: dict[str, list[str]] = (rc.get("arrays") or {}).get("textures") or {}
    if not arrays:
        print(f"{rc_name} has no texture arrays: add the skin by hand")
        return 2
    arr_name = opt(args, "--array") or next(iter(arrays))
    match = next((a for a in arrays if a.lower() == arr_name.lower()), None)
    if match is None:
        print(f"{rc_name} has no {arr_name}; arrays: {list(arrays)}")
        return 2
    arrays[match].append(f"Texture.{key}")
    index = len(arrays[match])  # BP value = position (1-based)
    texts = " ".join(rc.get("textures") or [])
    standard = re.search(re.escape(match) + r"\[\s*v(?:ariable)?\.mv_variant\s*-\s*1\s*\]", texts, re.I) is not None

    # 4. local roll (RP alone) and BP
    roll_change = "local roll: not found (v.xvar = math.random_integer(1, N)), update it by hand"
    if standard:
        init = (desc.get("scripts") or {}).get("initialize") or []
        for i, line in enumerate(init):
            m = re.match(r"(v(?:ariable)?\.xvar\s*=\s*math\.random_integer\(\s*1\s*,\s*)(\d+)(\s*\);?)$", line, re.I)
            if m:
                init[i] = f"{m.group(1)}{index}{m.group(3)}"
                roll_change = f"local roll: 1-{index}"
    bp_change = "no BP change"
    ident = desc["identifier"]
    bp_file = next((f for f in files(bp, "entities")
                    if load_for_edit(f)[0]["minecraft:entity"]["description"]["identifier"] == ident), "")
    bp_data: Json = None
    bp_head: str | None = None
    if bp_file and standard:
        bp_data, bp_head = load_for_edit(bp_file)
        e = bp_data["minecraft:entity"]
        prop = (e["description"].get("properties") or {}).get("mv:variant")
        rnds = variant_randomizes(e.get("events") or {}, [])
        if prop is None or not rnds:
            bp_change = "BP: mv:variant or its randomize not found, update it by hand"
            bp_data = None
        else:
            weight = int(opt(args, "--weight") or rnds[0][-1].get("weight", 1))
            for rnd in rnds:
                values = {int(o["set_property"]["mv:variant"]) for o in rnd if "mv:variant" in (o.get("set_property") or {})}
                if index not in values:
                    rnd.append({"weight": weight, "set_property": {"mv:variant": index}})
            prop["range"][1] = max(int(prop["range"][1]), index)
            bp_change = f"BP: mv:variant={index} weight {weight} in {len(rnds)} randomize, range {prop['range']}"
    elif not standard:
        bp_change = f"{match} is not read as [v.mv_variant - 1]: BP not changed, check the render controller"

    print(f"texture  {tex_path}" + (f"  (copy {png} -> {rel(copy_to)})" if copy_to else ""))
    print(f"entity   {rel(ent_file)}: {key}")
    print(f"rc       {rel(rc_file)}: {match}[{index - 1}] = Texture.{key}")
    print(f"roll     {roll_change}")
    print(f"bp       {bp_change}")
    if len(arrays) > 1:
        print(f"WARNING  {rc_name} has more skin arrays ({', '.join(a for a in arrays if a != match)}): add their texture by hand")
    if dry:
        print("(dry run: nothing written)")
        return 0
    if copy_to:
        os.makedirs(os.path.dirname(copy_to), exist_ok=True)
        shutil.copyfile(png, copy_to)
    save(ent_file, ent, ent_head)
    save(rc_file, rcs, rc_head)
    if bp_data is not None:
        save(bp_file, bp_data, bp_head)
    print(f"next: python -I tools/check.py {mob} && python tools/render.py {mob} --bp mv:variant={index}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
