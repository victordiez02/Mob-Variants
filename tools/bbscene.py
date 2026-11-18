"""Prepare a mob variant for Blockbench (through the Blockbench MCP) with all its layers and animations.

    python -I tools/bbscene.py <mob> [--bp mv:variant=3] [--nobp] [--q is_angry=1] [--q climate=warm]

Evaluates the entity like render.py (same options) and writes tools/out/bb/<mob>.scene.json: every
geometry drawn in that state (base + layers, 1.8 inheritance resolved), its texture and UV size, the
bones hidden by part_visibility and the animation files of the entity. Prints the one-line
`execute_script` code that loads it into Blockbench (tools/bb/load_scene.js): a new Bedrock project with
all layers merged (each with its own texture) and the entity's animations, also applied to layer bones
that share a name with a base bone, as in the game. Only reads the repo.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import ROOT, VRP, find_pack, geo_index, keyed_ids, require_vanilla, resolve_geo, texture_file  # noqa: E402
from molang import truthy, evaluate  # noqa: E402
from mvlib import Json, load  # noqa: E402
from mvsim import Mob, State, bone_visible, bp_entity, spawn_distribution  # noqa: E402

# Molang values Blockbench uses while previewing (it has no real entity): a mob walking at normal speed.
PLACEHOLDERS = chr(10).join([
    "query.modified_distance_moved = query.anim_time * 8;",
    "query.modified_move_speed = 0.7;",
    "query.is_moving = 1;",
    "query.is_on_ground = 1;",
    "variable.gliding_speed_value = 1;",
])


def active_animations(mob: Mob, acs: dict[str, Json]) -> list[str]:
    """Animations the entity runs in the evaluated state (conditions true; controllers: initial state)."""
    env = mob.last_env
    out: list[str] = []

    def run(entry: Json) -> None:
        key, cond = (entry, None) if isinstance(entry, str) else next(iter(entry.items()))
        if cond is not None and env is not None:
            try:
                if not truthy(evaluate(cond, env)):
                    return
            except (SyntaxError, KeyError):
                return
        ident = mob.keys["animations"].get(str(key).lower(), str(key))
        if ident in out:
            return
        if ident in acs:
            st = (acs[ident].get("states") or {}).get(acs[ident].get("initial_state", "default")) or {}
            for e in st.get("animations") or []:
                run(e)
        else:
            out.append(ident)

    for entry in mob.animate:
        run(entry)
    return out

LOADER = os.path.join(ROOT, "tools", "bb", "load_scene.js").replace("\\", "/")


def parse_args(argv: list[str]) -> tuple[str, dict[str, list[str]], set[str]]:
    flags = {"--nobp"}
    opts: dict[str, list[str]] = {}
    seen: set[str] = set()
    i = 1
    while i < len(argv):
        if argv[i] in flags:
            seen.add(argv[i])
            i += 1
        else:
            opts.setdefault(argv[i], []).append(argv[i + 1] if i + 1 < len(argv) else "")
            i += 2
    return argv[0], opts, seen


def main() -> int:
    require_vanilla()
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        print(__doc__)
        return 2
    mob_name, opts, flags = parse_args(sys.argv[1:])
    rp = find_pack("RP")
    f = os.path.join(rp, "entity", f"{mob_name}.entity.json")
    if not os.path.exists(f):
        print("no entity", f)
        return 2
    mob = Mob(f)
    queries: dict[str, float | str] = {}
    climate = "temperate"
    for kv in opts.get("--q", []):
        k, _, v = kv.partition("=")
        k = k.strip().lower()
        if k == "climate":
            climate = v.strip()
            continue
        k = k.split(".", 1)[1] if k.startswith(("q.", "query.")) else k
        try:
            queries[k] = float(v)
        except ValueError:
            queries[k] = v.strip()
    forced = {k.strip(): int(v) for k, _, v in (x.partition("=") for x in opts.get("--bp", []))}
    ent = bp_entity(mob.ident)
    if forced:
        props = {p: 0 for p in ((ent or {}).get("description", {}).get("properties") or {}) if p.startswith("mv:")}
        props.update(forced)
        st = State(props, queries=queries, climate=climate)
    elif ent and "--nobp" not in flags:
        st = State(spawn_distribution(ent)[0][1], queries=queries, climate=climate)  # most likely result
    else:
        st = State(None, queries=queries, climate=climate)
    _, layers, errors = mob.run(st)

    geos = (geo_index(rp), geo_index(VRP))
    out_layers = []
    for lay in layers:
        if not lay.geometry or "empty" in lay.geometry or not lay.textures:
            continue
        desc, bones = resolve_geo(lay.geometry, *geos)
        tex = texture_file(lay.textures[0], [rp, VRP])
        hidden = sorted({b["name"].lower() for b in bones if not bone_visible(lay, b["name"])})
        out_layers.append({
            "rc": lay.rc, "geometry": lay.geometry, "bones": bones,
            "texture_width": desc.get("texture_width", 64), "texture_height": desc.get("texture_height", 64),
            "texture": (tex or "").replace("\\", "/"), "hidden": hidden,
        })
    anim_ids = set((mob.desc.get("animations") or {}).values())
    acs: dict[str, Json] = {}
    for base in (VRP, rp):
        for ident, path in keyed_ids(base, "animation_controllers", "animation_controllers").items():
            acs[ident] = load(path)["animation_controllers"][ident]
    active = active_animations(mob, acs)
    anim_files: set[str] = set()
    for base in (VRP, rp):
        for kind in ("animations",):
            for ident, path in keyed_ids(base, kind, kind).items():
                if ident in anim_ids:
                    anim_files.add(path.replace("\\", "/"))
    scene = {"name": f"{mob_name} {' '.join(f'{k}={v}' for k, v in (st.bp or {}).items())}".strip(),
             "layers": out_layers, "animation_files": sorted(anim_files), "animations": sorted(anim_ids),
             "active": active, "placeholders": PLACEHOLDERS}
    out_dir = os.path.join(ROOT, "tools", "out", "bb")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{mob_name}.scene.json").replace("\\", "/")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(scene, fh)
    print(f"{len(out_layers)} layers: " + ", ".join(f"{x['geometry']} ({os.path.basename(x['texture'])})" for x in out_layers))
    for e in sorted(errors):
        print("  ERROR", e)
    print("always playing: " + ", ".join(active))
    print("execute_script code:")
    print(f'let s;Blockbench.read(["{LOADER}"],{{readtype:"text"}},f=>{{s=f[0].content}});'
          f'return new Function("scenePath",s)("{path}");')
    return 0


if __name__ == "__main__":
    sys.exit(main())
