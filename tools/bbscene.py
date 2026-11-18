"""Prepare a mob variant for Blockbench (through the Blockbench MCP) with all its layers and animations.

    python -I tools/bbscene.py <mob> [--bp mv:variant=3] [--nobp [--roll xvar=20]] [--q is_angry=1] [--q climate=warm]

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
import re
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
    flags = {"--nobp", "--all-layers"}
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


_BABY = re.compile(r"(?<![!\w.])(?:q|query)\.is_baby\b", re.I)


def adult_animations(mob: Mob, acs: dict[str, Json]) -> list[str]:
    """Every animation the entity can run (all controller states) except those only for babies."""
    out: list[str] = []

    def run(entry: Json, baby: bool, depth: int = 0) -> None:
        key, cond = (entry, "") if isinstance(entry, str) else next(iter(entry.items()))
        baby = baby or bool(_BABY.search(str(cond))) or "baby" in str(key).lower()
        ident = mob.keys["animations"].get(str(key).lower(), str(key))
        if ident in acs and depth < 8:
            for state in (acs[ident].get("states") or {}).values():
                for e in state.get("animations") or []:
                    run(e, baby, depth + 1)
        elif not baby and ident not in out:
            out.append(ident)

    for entry in mob.animate:
        run(entry, False)
    return out


class Scene:
    """Result of build(): where the scene file is and how to load it."""

    def __init__(self, path: str, code: str, info: list[str], errors: list[str], data: Json):
        self.path, self.code, self.info, self.errors, self.data = path, code, info, errors, data


def build(argv: list[str]) -> Scene:
    """argv = [mob, options…] as on the command line. Writes tools/out/bb/<mob>.scene.json."""
    mob_name, opts, flags = parse_args(argv)
    rp = find_pack("RP")
    f = os.path.join(rp, "entity", f"{mob_name}.entity.json")
    if not os.path.exists(f):
        raise SystemExit(f"no entity {f}")
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
    rolls = {"xvar": 50.0, "yvar": 50.0, "zvar": 50.0}  # local roll without BP (0-99), e.g. --roll xvar=20
    for kv in opts.get("--roll", []):
        k, _, v = kv.partition("=")
        rolls[k.strip().lower().removeprefix("v.")] = float(v) + 0.5
    ent = bp_entity(mob.ident)
    if forced:
        props = {p: 0 for p in ((ent or {}).get("description", {}).get("properties") or {}) if p.startswith("mv:")}
        props.update(forced)
        st = State(props, queries=queries, climate=climate)
    elif ent and "--nobp" not in flags:
        st = State(spawn_distribution(ent)[0][1], queries=queries, climate=climate)  # most likely result
    else:
        st = State(None, rolls, queries=queries, climate=climate)
    _, layers, errors = mob.run(st)
    if "--all-layers" in flags:  # every geometry the mob can draw (for measuring, not a real outfit)
        seen = {lay.geometry for lay in layers}
        states = [State(None, {"xvar": x + 0.5, "yvar": x + 0.5, "zvar": (x * 7 % 100) + 0.5}) for x in range(100)]
        states += [State(props) for _, props in (spawn_distribution(ent) if ent else [])]
        for extra in states:
            for lay in mob.run(extra)[1]:
                if lay.geometry and lay.geometry not in seen and "empty" not in lay.geometry:
                    seen.add(lay.geometry)
                    layers.append(lay)

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
    if out_layers:  # a "layer" with cubes on 3+ bones of the base is a full replacement model
        base_names = {b["name"].lower() for b in out_layers[0]["bones"]}
        for x in out_layers[1:]:
            x["full_model"] = sum(1 for b in x["bones"] if b["name"].lower() in base_names and b.get("cubes")) >= 3
    anim_ids = set((mob.desc.get("animations") or {}).values())
    acs: dict[str, Json] = {}
    for base in (VRP, rp):
        for ident, path in keyed_ids(base, "animation_controllers", "animation_controllers").items():
            acs[ident] = load(path)["animation_controllers"][ident]
    active = active_animations(mob, acs)
    anim_files: set[str] = set()
    for base in (VRP, rp):
        for ident, path in keyed_ids(base, "animations", "animations").items():
            if ident in anim_ids:
                anim_files.add(path.replace("\\", "/"))
    data = {"name": f"{mob_name} {' '.join(f'{k}={v}' for k, v in (st.bp or {}).items())}".strip(),
            "layers": out_layers, "animation_files": sorted(anim_files), "animations": sorted(anim_ids),
            "active": active, "placeholders": PLACEHOLDERS, "adult_animations": adult_animations(mob, acs)}
    out_dir = os.path.join(ROOT, "tools", "out", "bb")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{mob_name}.scene.json").replace("\\", "/")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    info = [f"{len(out_layers)} layers: " + ", ".join(f"{x['geometry']} ({os.path.basename(x['texture'])})" for x in out_layers),
            "always playing: " + ", ".join(active)]
    code = (f'let s;Blockbench.read(["{LOADER}"],{{readtype:"text"}},f=>{{s=f[0].content}});'
            f'return new Function("scenePath",s)("{path}");')
    return Scene(path, code, info, sorted(errors), data)


def main() -> int:
    require_vanilla()
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        print(__doc__)
        return 2
    sc = build(sys.argv[1:])
    for line in sc.info:
        print(line)
    for e in sc.errors:
        print("  ERROR", e)
    print("execute_script code:")
    print(sc.code)
    return 0


if __name__ == "__main__":
    sys.exit(main())
