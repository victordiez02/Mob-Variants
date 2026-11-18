"""Validate BP entities: referenced groups/events exist, properties declared, JSON shape."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import *
BP = find_pack("BP")
def walk(n, fn):
    if isinstance(n, dict):
        fn(n)
        for k in ("randomize", "sequence"):
            for c in n.get(k, []): walk(c, fn)
bad = 0
for f in sorted(files(BP, "entities")):
    e = load(f)[0]["minecraft:entity"]; name = os.path.basename(f)
    cg = e.get("component_groups", {}); ev = e.get("events", {}) or {}; props = e["description"].get("properties", {})
    problems = []
    def check(n):
        for k in ("add", "remove"):
            for g in (n.get(k) or {}).get("component_groups", []):
                if g not in cg: problems.append(f"missing group {g}")
        for p, v in (n.get("set_property") or {}).items():
            if p not in props: problems.append(f"undeclared property {p}")
            elif props[p]["type"] == "int" and isinstance(v, int) and not (props[p]["range"][0] <= v <= props[p]["range"][1]): problems.append(f"{p}={v} out of range")
        t = n.get("trigger"); t = t if isinstance(t, str) or t is None else t.get("event")
        if t and t not in ev and not t.startswith("minecraft:"): problems.append(f"missing event {t}")
    for body in ev.values(): walk(body, check)
    s = json.dumps(cg)
    import re
    for ref in re.findall(r'"event": "([^"]+)"', s):
        if ref not in ev and not ref.startswith("minecraft:"): problems.append(f"group refers to missing event {ref}")
    for ref in set(re.findall(r'"event": "(minecraft:[^"]+)"', s + json.dumps(e.get("components", {})))):
        if ref not in ev: problems.append(f"refers to undefined vanilla-named event {ref}")
    if problems: bad += 1; print(name, sorted(set(problems)))
    else: print(name, "OK", {k: v["range"] for k, v in props.items() if k.startswith("mv:")})
print("files with problems:", bad)
