"""Evaluate what a client entity renders in a given state (BP values, rolls, queries).

Shared by simulate.py (statistics) and render.py (pictures).
"""
from __future__ import annotations

import fnmatch
import json
import re
from dataclasses import dataclass, field
from typing import Any

from molang import Env, Value, evaluate, num, truthy
from mvlib import Json, VRP, files, find_pack, keyed_ids, load, rc_list


@dataclass
class State:
    """Inputs of one simulated mob. bp=None means 'no behavior pack' (properties do not exist)."""
    bp: dict[str, int] | None = None              # {"mv:variant": 3, "mv:mark_variant": 1}
    rolls: dict[str, float] = field(default_factory=lambda: {"xvar": 50.0, "yvar": 50.0, "zvar": 50.0})
    random: float = 0.5                           # math.random(a, b) -> a + (b - a) * random
    queries: dict[str, Value] = field(default_factory=dict)
    climate: str = "temperate"

    def query(self, name: str) -> Value:
        return self.queries.get(name, 0.0)


@dataclass
class Layer:
    rc: str
    geometry_key: str
    geometry: str | None             # geometry identifier (None if the key is undefined)
    textures: list[str]              # texture paths (without extension)
    part_visibility: list[tuple[str, bool]]


_NS = {"v": "v", "variable": "v", "t": "t", "temp": "t", "c": "c", "context": "c", "q": "q", "query": "q"}


def _norm(name: str) -> tuple[str, str]:
    head, _, rest = name.lower().partition(".")
    return _NS.get(head, head), rest


class Mob:
    """A client entity of the add-on with the render controllers it can use."""

    _rcs: dict[str, Json] | None = None

    def __init__(self, file: str):
        self.file = file
        self.desc: Json = load(file)["minecraft:client_entity"]["description"]
        self.ident: str = self.desc["identifier"]
        self.keys = {s: {k.lower(): v for k, v in (self.desc.get(s) or {}).items()}
                     for s in ("textures", "geometry", "materials", "animations")}
        scripts = self.desc.get("scripts") or {}
        self.init_lines: list[str] = list(scripts.get("initialize") or [])
        self.pre_lines: list[str] = list(scripts.get("pre_animation") or [])
        self.animate: list[Json] = list(scripts.get("animate") or [])
        self.last_env: Env | None = None

    @classmethod
    def render_controllers(cls) -> dict[str, Json]:
        if cls._rcs is None:
            rp = find_pack("RP")
            cls._rcs = {}
            for base in (VRP, rp):  # add-on wins
                for name, f in keyed_ids(base, "render_controllers", "render_controllers").items():
                    cls._rcs[name] = load(f)["render_controllers"][name]
        return cls._rcs

    # ------------------------------------------------------------ evaluation

    def run(self, st: State) -> tuple[dict[str, Value], list[Layer], set[str]]:
        """(variables, layers drawn, errors) for state `st`."""
        variables: dict[str, Value] = {}
        errors: set[str] = set()

        def lookup(name: str, args: list[Value] | None) -> Value:
            if name.startswith("="):
                ns, var = _norm(name[1:])
                variables[f"{ns}.{var}"] = args[0] if args else 0.0
                return 0.0
            ns, rest = _norm(name)
            if ns in ("v", "t", "c"):
                return variables.get(f"{ns}.{rest}", st.queries.get(f"{ns}.{rest}", 0.0))  # engine-set variables
            if ns == "q":
                a0 = str(args[0]) if args else ""
                if rest == "has_property":
                    return 1.0 if not a0.startswith("mv:") or (st.bp is not None and a0 in st.bp) else 0.0
                if rest == "property":
                    if a0 == "minecraft:climate_variant":
                        return st.climate
                    if a0.startswith("mv:"):
                        if st.bp is None or a0 not in st.bp:
                            errors.add(f"q.property('{a0}') without the property")
                            return 0.0
                        return float(st.bp[a0])
                    return st.query(f"property:{a0}")
                return st.query(rest)
            if ns == "math" and rest in ("random", "random_integer", "die_roll", "die_roll_integer"):
                a = [num(x) for x in (args or [])] + [0.0, 1.0]
                v = a[0] + (a[1] - a[0]) * st.random
                return float(int(v)) if "integer" in rest else v
            if ns in ("texture", "geometry", "material"):
                return f"{ns}.{rest}"
            if ns == "array":
                raise KeyError("array without index: " + name)
            return 0.0

        env = Env(lookup)
        self.last_env = env  # render.py evaluates the pose animations with the same variables
        for line in self.init_lines + self.pre_lines:
            m = re.match(r"\s*v(?:ariable)?\.([xyz]var)\s*=", line, re.I)
            if m and m.group(1).lower() in st.rolls:
                variables["v." + m.group(1).lower()] = st.rolls[m.group(1).lower()]
                continue
            if "{" in line or "}" in line:
                continue  # multi-line blocks of 1.26 entities: not supported (vanilla logic only)
            try:
                evaluate(line, env)
            except (SyntaxError, KeyError, ValueError, ZeroDivisionError) as e:
                if re.search(r"mv_|[xyz]var", line, re.I):
                    errors.add(f"script {line.strip()[:50]!r}: {e}")
        layers: list[Layer] = []
        for name, cond in rc_list(self.desc):
            try:
                if cond is not None and not truthy(evaluate(cond, env)):
                    continue
            except (SyntaxError, KeyError) as e:
                errors.add(f"condition of {name}: {e}")
                continue
            rc = self.render_controllers().get(name)
            if rc is None:
                errors.add(f"render controller {name} missing")
                continue
            try:
                layers.append(self._layer(name, rc, lookup))
            except (SyntaxError, KeyError, IndexError) as e:
                errors.add(f"{name}: {e}")
        return variables, layers, errors

    def _layer(self, name: str, rc: Json, lookup: Any) -> Layer:
        arrays: dict[str, list[str]] = {}
        for arrs in (rc.get("arrays") or {}).values():
            for an, av in arrs.items():
                arrays[an] = av
        env = Env(lookup, arrays)
        gkey = str(evaluate(rc.get("geometry", "0"), env)).lower()
        geo = self.keys["geometry"].get(gkey.partition(".")[2]) if gkey.startswith("geometry.") else None
        texs: list[str] = []
        for t in rc.get("textures") or []:
            tk = str(evaluate(t, env)).lower()
            if not tk.startswith("texture."):
                raise KeyError(f"texture expression gives {tk!r}")
            path = self.keys["textures"].get(tk.partition(".")[2])
            if path is None:
                raise KeyError(f"Texture.{tk.partition('.')[2]} not defined")
            texs.append(path)
        vis: list[tuple[str, bool]] = []
        for entry in rc.get("part_visibility") or []:
            for pat, expr in entry.items():
                vis.append((pat.lower(), truthy(evaluate(expr, env))))
        return Layer(name, gkey, geo, texs, vis)


def bone_visible(layer: Layer, bone: str) -> bool:
    vis = True
    for pat, on in layer.part_visibility:
        if fnmatch.fnmatchcase(bone.lower(), pat):
            vis = on
    return vis


# ---------------------------------------------------------------- BP spawn distribution


def bp_entity(ident: str) -> Json | None:
    for f in files(find_pack("BP"), "entities"):
        e = load(f).get("minecraft:entity", {})
        if e.get("description", {}).get("identifier") == ident:
            return e
    return None


def spawn_distribution(entity: Json, event: str = "minecraft:entity_spawned") -> list[tuple[float, dict[str, int]]]:
    """[(probability, {mv property: value})] after `event` (filters are ignored: approximate)."""
    events = entity.get("events") or {}
    props = entity.get("description", {}).get("properties") or {}
    base = {p: int(v.get("default", 0)) for p, v in props.items() if p.startswith("mv:") and v.get("type") == "int"}

    def walk(node: Json, dist: dict[str, float], depth: int = 0) -> dict[str, float]:
        if not isinstance(node, dict) or depth > 20:
            return dist
        sp = {k: int(v) for k, v in (node.get("set_property") or {}).items() if k.startswith("mv:") and isinstance(v, (int, float))}
        if sp:
            new: dict[str, float] = {}
            for key, p in dist.items():
                d = json.loads(key)
                d.update(sp)
                k2 = json.dumps(d, sort_keys=True)
                new[k2] = new.get(k2, 0.0) + p
            dist = new
        trig = node.get("trigger")
        tname = trig if isinstance(trig, str) else (trig or {}).get("event")
        if tname and tname in events and tname != event:
            dist = walk(events[tname], dist, depth + 1)
        for child in node.get("sequence") or []:
            dist = walk(child, dist, depth + 1)
        opts = node.get("randomize") or []
        total = sum(float(o.get("weight", 1)) for o in opts)
        if opts and total > 0:
            merged: dict[str, float] = {}
            for o in opts:
                w = float(o.get("weight", 1)) / total
                for k, p in walk(o, dist, depth + 1).items():
                    merged[k] = merged.get(k, 0.0) + p * w
            dist = merged
        return dist

    start = {json.dumps(base, sort_keys=True): 1.0}
    out = walk(events.get(event) or {}, start)
    return sorted(((p, json.loads(k)) for k, p in out.items()), key=lambda x: -x[0])


def capped(dist: list[tuple[float, dict[str, int]]], limit: int = 1500) -> list[tuple[float, dict[str, int]]]:
    """At most `limit` outcomes of spawn_distribution (one property per feature multiplies them: the zombie
    has ~400k): the most probable ones plus, for every property value, its most probable outcome. The
    probabilities are those of the full distribution (they no longer add up to 1)."""
    if len(dist) <= limit:
        return dist
    keep: dict[str, tuple[float, dict[str, int]]] = {}
    seen: set[tuple[str, int]] = set()
    for p, d in dist:  # sorted by probability
        new = {(k, v) for k, v in d.items()} - seen
        if new or len(keep) < limit:
            keep[json.dumps(d, sort_keys=True)] = (p, d)
            seen |= new
    return sorted(keep.values(), key=lambda x: -x[0])
