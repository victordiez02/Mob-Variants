"""Simulate every mob's render controllers over all rolls (no BP) and all BP spawn results.

    python -I tools/simulate.py [mob ...] [--detail]

Per mob: how many distinct (geometry, textures) each add-on render controller produces without BP
and with BP. 1 means that layer never changes (its variants do not work). Also reports:
- mv_* textures/geometries of the entity that no state ever draws;
- layers that, with BP, still depend on the local roll (each player would see something different);
- Molang errors.
--detail prints the probability of each result (BP: weights of the minecraft:entity_spawned randomize).
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import VRP, Geo, files, find_pack, geo_index, png_size, rc_list, require_vanilla, resolve_geo, texture_file  # noqa: E402
from mvsim import Layer, Mob, State, bp_entity, capped, spawn_distribution  # noqa: E402

_SKIP_Q = {"property", "has_property", "position", "life_time", "anim_time", "modified_move_speed", "target_x_rotation",
           "target_y_rotation", "head_x_rotation", "head_y_rotation", "body_y_rotation", "time_stamp", "delta_time"}


def explored_queries(mob: Mob) -> dict[str, list[float | str]]:
    """Queries the entity and its render controllers read, with the values worth trying."""
    text = json.dumps(mob.desc.get("scripts")) + json.dumps([mob.render_controllers().get(n) for n, _ in rc_list(mob.desc)])
    out: dict[str, list[float | str]] = {}
    for q in set(re.findall(r"\b(?:q|query)\.(\w+)", text, re.I)):
        q = q.lower()
        if q in _SKIP_Q:
            continue
        out[q] = [float(i) for i in range(1, 16)] if q in ("variant", "mark_variant", "skin_id") else [1.0, 2.0, 3.0, 4.0]
    for p in set(re.findall(r"property\('(minecraft:\w+)'\)", text)):  # vanilla properties (has_nectar…)
        if p != "minecraft:climate_variant":
            out["property:" + p] = [1.0, 2.0]
    assigned = {m.lower() for m in re.findall(r"\b(?:v|variable)\.(\w+)\s*=[^=]", text, re.I)}
    for v in set(re.findall(r"\b(?:v|variable)\.(\w+)", text, re.I)):  # engine-set variables (ischarging…)
        if v.lower() not in assigned and v.lower() not in ("xvar", "yvar", "zvar"):
            out["v." + v.lower()] = [1.0]
    return out

Result = tuple[str | None, tuple[str, ...]]


_GEOS: tuple[dict[str, Geo], dict[str, Geo]] | None = None


def ratio_problems(pairs: set[tuple[str, str]]) -> list[str]:
    """Textures whose aspect ratio differs from texture_width/height of the geometry they are drawn with."""
    global _GEOS
    if _GEOS is None:
        _GEOS = (geo_index(find_pack("RP")), geo_index(VRP))
    out: list[str] = []
    for geo, tex in sorted(pairs):
        try:
            desc, _ = resolve_geo(geo, *_GEOS)
        except KeyError:
            continue
        f = texture_file(tex, [find_pack("RP")])  # vanilla textures are not ours (wither_armor_blue is 64x32 in vanilla)
        size = png_size(f) if f and f.endswith(".png") else None
        tw, th = float(desc.get("texture_width", 64)), float(desc.get("texture_height", 64))
        if size and "empty" not in tex and abs(size[0] / size[1] - tw / th) > 1e-3:
            out.append(f"{os.path.basename(tex)} {size[0]}x{size[1]} on {geo} ({tw:g}x{th:g})")
    return out


def short(r: Result) -> str:
    g, t = r
    return f"{(g or '-').replace('geometry.', '')} + {', '.join(os.path.basename(x) for x in t)}"


def drawn(layers: list[Layer]) -> dict[str, Result]:
    return {lay.rc: (lay.geometry, tuple(lay.textures)) for lay in layers
            if lay.rc.startswith("controller.render.mv.") and lay.geometry and "empty" not in lay.geometry}


def simulate_mob(f: str, name: str, detail: bool) -> bool:
    """Print the report of one entity; True if it has Molang errors."""
    failed = False
    mob = Mob(f)
    errors: set[str] = set()
    used_tex: set[str] = set()
    used_geo: set[str] = set()
    nobp: dict[str, dict[Result, float]] = defaultdict(lambda: defaultdict(float))
    bp: dict[str, dict[Result, float]] = defaultdict(lambda: defaultdict(float))
    roll_dependent: set[str] = set()

    pairs: set[tuple[str, str]] = set()

    def record(st: State, into: dict[str, dict[Result, float]], weight: float) -> dict[str, Result]:
        _, layers, errs = mob.run(st)
        errors.update(errs)
        out = drawn(layers)
        for lay in layers:
            used_tex.update(lay.textures)
            if lay.geometry:
                used_geo.add(lay.geometry)
                if "empty" not in lay.geometry:
                    pairs.update((lay.geometry, t) for t in lay.textures)
        for rc, r in out.items():
            into[rc][r] += weight
        return out

    ys = (0.5, 10.5, 30.5, 60.5, 99.5)
    for x in range(100):
        for y in ys:
            record(State(None, {"xvar": x + 0.5, "yvar": y, "zvar": (x * 7 % 100) + 0.5}), nobp, 1 / (100 * len(ys)))
    ent = bp_entity(mob.ident)
    dist = capped(spawn_distribution(ent)) if ent else []
    for p, props in dist or [(1.0, {})]:
        bpv = props if ent else None
        res = record(State(bpv, {"xvar": 50.5, "yvar": 50.5, "zvar": 50.5}), bp, p)
        if ent:
            for x in (0.5, 99.5):
                other = mob.run(State(bpv, {"xvar": x, "yvar": x, "zvar": x}))[1]
                for rc, r in drawn(other).items():
                    if res.get(rc) != r:
                        roll_dependent.add(rc.removeprefix("controller.render.mv."))

    # other states (angry, saddled, tamed, profession…), only to find what is never drawn
    sink: dict[str, dict[Result, float]] = defaultdict(lambda: defaultdict(float))
    for q, values in explored_queries(mob).items():
        for val in values:
            for x in range(0, 100, 3):
                record(State(None, {"xvar": x + 0.5, "yvar": 50.5, "zvar": 50.5}, queries={q: val}), sink, 0)
            for _, props in dist[:50]:
                record(State(props, queries={q: val}), sink, 0)
    for climate in ("warm", "cold"):
        record(State(None, climate=climate), sink, 0)

    summary = lambda d: {rc.removeprefix("controller.render.mv."): len(v) for rc, v in d.items()}  # noqa: E731
    line = f"{name:22} noBP={summary(nobp)}  BP={summary(bp) if ent else '(sin BP)'}"
    print(line)
    unused_t = sorted(k for k, v in mob.keys["textures"].items() if k.startswith("mv_") and v not in used_tex)
    unused_g = sorted(k for k, v in mob.keys["geometry"].items()
                      if k.startswith("mv_") and v not in used_geo and "empty" not in v)
    for label, items in (("textures never drawn", unused_t), ("geometries never drawn", unused_g),
                         ("BP result depends on local roll", sorted(roll_dependent)),
                         ("texture size does not match the geometry UV", ratio_problems(pairs)), ("ERRORS", sorted(errors))):
        if items:
            print(f"    {label}: {items}")
            failed = failed or label == "ERRORS"
    if detail:
        for title, d in (("no BP", nobp), ("BP", bp if ent else {})):
            for rc, results in d.items():
                print(f"    [{title}] {rc.removeprefix('controller.render.mv.')}")
                for r, p in sorted(results.items(), key=lambda kv: -kv[1]):
                    print(f"        {p:7.2%}  {short(r)}")
    return failed


def main() -> int:
    require_vanilla()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    detail = "--detail" in sys.argv
    problems = 0
    for f in files(find_pack("RP"), "entity"):
        name = os.path.basename(f).split(".")[0]
        if args and name not in args:
            continue
        problems += simulate_mob(f, name, detail)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
