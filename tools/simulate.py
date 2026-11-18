"""Simulate every mob's addon render controllers over all rolls; report distinct skins/models per mode."""
import sys, os, json, re; import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import *
from molang import evaluate, truthy
RP = find_pack("RP"); BP = find_pack("BP")
rcs = {}
for f in files(RP, "render_controllers"):
    for k, v in load(f)[0]["render_controllers"].items(): rcs[k] = v
def bp_values(ident):
    for f in files(BP, "entities"):
        d = load(f)[0]["minecraft:entity"]
        if d["description"]["identifier"] == ident:
            s = json.dumps(d.get("events", {}))
            return ({int(x) for x in re.findall(r'"mv:variant": (\d+)', s)}, {int(x) for x in re.findall(r'"mv:mark_variant": (\d+)', s)})
    return set(), set()
only = sys.argv[1:]
for f in sorted(files(RP, "entity")):
    mob = os.path.basename(f).split(".")[0]
    if only and mob not in only: continue
    desc = load(f)[0]["minecraft:client_entity"]["description"]
    keys = {s: {k.lower(): v for k, v in (desc.get(s) or {}).items()} for s in ("textures", "geometry", "materials")}
    pre = desc.get("scripts", {}).get("pre_animation", []); init = desc.get("scripts", {}).get("initialize", [])
    mvlines = [l for l in init + pre if re.match(r"\s*v(ariable)?\.(mv_\w+|[xyzX]?var)\s*=", l, re.I)]
    variants, marks = bp_values(desc["identifier"])
    results = {}
    errors = set()
    def run(mode, rolls, bpv, bpm):
        V = {"is_baby": 0.0, "variant": 0.0, "mark_variant": 0.0, "is_tamed": 0.0, "is_saddled": 0.0, "is_angry": 0.0}
        vars_ = {}
        def lookup(name, args):
            n = name.split(".", 1)
            if n[0] in ("v", "variable", "t", "temp"): return vars_.get(n[1].lower(), 0.0)
            if n[0] in ("q", "query"):
                if n[1] == "has_property": return 1.0 if bpv is not None else 0.0
                if n[1] == "property":
                    if args and args[0] == "mv:variant": return float(bpv or 0)
                    if args and args[0] == "mv:mark_variant": return float(bpm or 0)
                    if args and args[0] == "minecraft:climate_variant": return "temperate"
                    return 0.0
                if n[1] == "position": return 64.0
                return V.get(n[1], 0.0)
            if n[0] in ("math",):
                fn = n[1]; a = [float(x) if not isinstance(x, str) else 0 for x in (args or [])]
                return {"random": lambda: rolls.get("_r", 50.0), "floor": lambda: float(int(a[0] // 1)), "mod": lambda: a[0] % a[1] if a[1] else 0.0,
                        "random_integer": lambda: float(int(a[0])), "clamp": lambda: min(max(a[0], a[1]), a[2]), "abs": lambda: abs(a[0])}.get(fn, lambda: 0.0)()
            if n[0] in ("texture", "geometry", "material"): return f"{n[0]}.{n[1]}"
            if n[0] == "array": raise KeyError("array without index " + name)
            return 0.0
        for l in mvlines:
            m = re.match(r"\s*v(?:ariable)?\.(\w+)\s*=\s*(.*?);?\s*$", l)
            name = m.group(1).lower()
            if name in ("xvar", "yvar", "zvar"): vars_[name] = rolls[name]; continue
            try: vars_[name] = evaluate(m.group(2), {"arrays": {}, "resolve": lambda x: x, "lookup": lookup})
            except Exception as e: errors.add(f"pre: {l[:60]} -> {e}")
        out = []
        for r in desc.get("render_controllers", []):
            name = r if isinstance(r, str) else next(iter(r))
            if not name.startswith("controller.render.mv."): continue
            if not isinstance(r, str):
                try:
                    if not truthy(evaluate(next(iter(r.values())), {"arrays": {}, "resolve": lambda x: x, "lookup": lookup})): continue
                except Exception as e: errors.add(f"cond {name}: {e}"); continue
            rc = rcs.get(name)
            arrays = {}
            for kind, arrs in (rc.get("arrays") or {}).items():
                for an, av in arrs.items(): arrays[an.lower()] = av
            env = {"arrays": arrays, "resolve": lambda x: lookup(x.lower(), None), "lookup": lookup}
            try:
                g = evaluate(rc["geometry"], env)
                t = [evaluate(x, env) for x in rc.get("textures", [])]
                out.append((name.split(".")[-1], g, tuple(t)))
            except Exception as e: errors.add(f"{name}: {e}")
        return tuple(out)
    combos = set()
    for x in range(0, 100):
        for y in (0, 10, 30, 60, 99):
            combos.add(("no BP", run("noBP", {"xvar": x + 0.5, "yvar": y + 0.5, "zvar": (x * 7 % 100) + 0.5}, None, None)))
    for v in sorted(variants or {0}):
        for m in sorted(marks or {0}):
            combos.add(("BP", run("BP", {"xvar": 50.5, "yvar": 50.5, "zvar": 50.5}, v, m)))
    base_tex = {"no BP": set(), "BP": set()}
    for mode, o in combos:
        for rcname, g, t in o:
            if g and "empty" not in str(g):
                base_tex[mode].add((rcname, g, t))
    def summarize(mode):
        s = base_tex[mode]
        by = {}
        for rc, g, t in s: by.setdefault(rc, set()).add((g, t))
        return {rc: len(v) for rc, v in by.items()}
    print(f"{mob:22} noBP={summarize('no BP')}  BP={summarize('BP')}" + (f"  ERRORS={sorted(errors)[:3]}" if errors else ""))
