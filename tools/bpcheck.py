"""Static checks of the behavior pack.

    python -I tools/bpcheck.py

- component groups / events referenced but not defined, mv:* properties undeclared or out of range;
- rule 5: each entity = the current vanilla file + only mv additions (format_version, components and
  component groups identical to vanilla; extra groups/events must be mv:*);
- mv:* properties must be int with client_sync (the RP reads them);
- nothing of ours inside minecraft:add_attributes (not an engine event).
Problems vanilla itself has are listed as EXPECTED. Exit code 1 if there are errors.
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections.abc import Callable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import Json, files, find_pack, load, rel, require_vanilla, vanilla_behavior_entity  # noqa: E402


# Engine events we may add to a vanilla entity.
ENGINE_EVENTS = {"minecraft:entity_spawned", "minecraft:entity_transformed", "minecraft:entity_born"}
# Documented deviations from vanilla (docs/ARCHITECTURE.md, "Mecánicas propias conservadas").
ALLOWED_DIFFS = {("minecraft:zombie", "minecraft:behavior.pickup_items")}  # stuck zombies do not pick up items


def walk(node: Json, fn: Callable[[Json], None]) -> None:
    if isinstance(node, dict):
        fn(node)
        for k in ("randomize", "sequence"):
            for c in node.get(k) or []:
                walk(c, fn)


def event_problems(e: Json) -> set[str]:
    cg = e.get("component_groups") or {}
    ev = e.get("events") or {}
    props = e["description"].get("properties") or {}
    out: set[str] = set()

    def check(n: Json) -> None:
        for k in ("add", "remove"):
            for g in (n.get(k) or {}).get("component_groups", []):
                if g not in cg:
                    out.add(f"missing group {g}")
        for p, v in (n.get("set_property") or {}).items():
            if p not in props:
                out.add(f"undeclared property {p}")
            elif props[p].get("type") == "int" and isinstance(v, int):
                lo, hi = props[p]["range"]
                if not lo <= v <= hi:
                    out.add(f"{p}={v} out of range [{lo}, {hi}]")
        t = n.get("trigger")
        t = t if isinstance(t, str) or t is None else t.get("event")
        if t and t not in ev and not t.startswith("minecraft:"):
            out.add(f"missing event {t}")

    for body in ev.values():
        walk(body, check)
    s = json.dumps(cg)
    for ref in re.findall(r'"event": "([^"]+)"', s):
        if ref not in ev and not ref.startswith("minecraft:"):
            out.add(f"group refers to missing event {ref}")
    for ref in set(re.findall(r'"event": "(minecraft:[^"]+)"', s + json.dumps(e.get("components", {})))):
        if ref not in ev:
            out.add(f"refers to undefined vanilla-named event {ref}")
    return out


def main() -> int:
    require_vanilla()
    bp = find_pack("BP")
    n_err = 0
    for f in files(bp, "entities"):
        name = os.path.basename(f)
        d = load(f)
        e = d["minecraft:entity"]
        ident = e["description"]["identifier"]
        props = e["description"].get("properties") or {}
        errs: list[str] = []
        warns: list[str] = []
        probs = event_problems(e)
        van = vanilla_behavior_entity(ident)
        expected: set[str] = set()
        if van is None:
            warns.append("no vanilla entity with this identifier")
        else:
            vf, vd = van
            ve = vd["minecraft:entity"]
            expected = probs & event_problems(ve)  # vanilla has the same problem
            if d.get("format_version") != vd.get("format_version"):
                errs.append(f"format_version {d.get('format_version')} != vanilla {vd.get('format_version')}")
            vc, mc = ve.get("components") or {}, e.get("components") or {}
            diff = sorted(k for k in set(vc) | set(mc) if vc.get(k) != mc.get(k) and (ident, k) not in ALLOWED_DIFFS)
            if diff:
                errs.append(f"components differ from vanilla: {diff}")
            vg, mg = ve.get("component_groups") or {}, e.get("component_groups") or {}
            for g in sorted(set(vg) | set(mg)):
                if g not in mg:
                    errs.append(f"vanilla group {g} missing")
                elif g not in vg:
                    if not g.startswith("mv:"):
                        errs.append(f"extra group {g} outside the mv: namespace")
                elif vg[g] != mg[g]:
                    errs.append(f"group {g} differs from vanilla")
            vev, mev = ve.get("events") or {}, e.get("events") or {}
            for k in sorted(set(vev) - set(mev)):
                errs.append(f"vanilla event {k} missing")
            for k in sorted(set(mev) - set(vev)):
                if not k.startswith("mv:") and k not in ENGINE_EVENTS:
                    errs.append(f"extra event {k} outside the mv: namespace")
            vprops = ve["description"].get("properties") or {}
            for p in sorted(set(vprops) | set(props)):
                if p.startswith("mv:"):
                    continue
                if vprops.get(p) != props.get(p):
                    errs.append(f"vanilla property {p} changed or missing")
        errs.extend(sorted(probs - expected))
        for p, spec in props.items():
            if p.startswith("mv:") and (spec.get("type") != "int" or not spec.get("client_sync")):
                errs.append(f"{p} must be int with client_sync: true")
            if not p.startswith(("mv:", "minecraft:")):
                errs.append(f"property {p} outside the mv: namespace")
        aa = (e.get("events") or {}).get("minecraft:add_attributes")
        if aa and "mv:" in json.dumps(aa):
            errs.append("mv logic inside minecraft:add_attributes (never runs: use minecraft:entity_spawned)")
        ranges = {k: v.get("range") for k, v in props.items() if k.startswith("mv:")}
        status = "OK" if not errs else "ERRORS"
        print(f"{name:24} {status} {ranges}" + (f"  expected (vanilla): {len(expected)}" if expected else ""))
        for x in errs:
            print("    ERROR", x)
        for x in warns:
            print("    warning", x)
        n_err += bool(errs)
    print(f"files with errors: {n_err}  ({rel(bp)})")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
