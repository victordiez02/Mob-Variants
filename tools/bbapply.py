"""Put a layer edited in Blockbench back into the add-on's geometry file.

    python -I tools/bbapply.py <geometry id> [--dry-run]

Reads tools/out/bb/<geometry>.export.json (written by mvExportLayer() in Blockbench, see the
mv-blockbench skill) and replaces the bones of that geometry in RP/models/, keeping its description and
the project's JSON style. Only add-on geometries (geometry.mv.*) in 1.12+ format can be written.
Then run: python -I tools/check.py <mob> (validate checks pivots/parents against the base model).
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import ROOT, Json, find_pack, geo_index, load_for_edit, rel, save  # noqa: E402


def clean(o: Json) -> Json:
    """Round floats (Blockbench writes 0.30000000000000004) and drop empty or default fields."""
    if isinstance(o, float):
        r = round(o, 5)
        return int(r) if r == int(r) else r
    if isinstance(o, list):
        return [clean(x) for x in o]
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            if v in ([], {}, None) or (k == "rotation" and v == [0, 0, 0]):
                continue
            out[k] = clean(v)
        return out
    return o


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    ident = args[0]
    src = os.path.join(ROOT, "tools", "out", "bb", f"{ident}.export.json")
    if not os.path.exists(src):
        print("missing", rel(src), "- run mvExportLayer in Blockbench first")
        return 2
    if not ident.startswith("geometry.mv."):
        print("only add-on geometries (geometry.mv.*) can be written")
        return 2
    geo = geo_index(find_pack("RP")).get(ident)
    if geo is None:
        print("geometry not found in RP:", ident)
        return 2
    with open(src, encoding="utf-8") as f:
        bones = clean(json.load(f)["bones"])
    data, header = load_for_edit(geo.file)
    entry = next((g for g in data.get("minecraft:geometry", []) if g["description"]["identifier"] == ident), None)
    if entry is None:
        print(f"{rel(geo.file)}: {ident} is in the old 1.8 format; convert it first")
        return 2
    old = {b["name"]: b for b in entry.get("bones", [])}
    new = {b["name"]: b for b in bones}
    changed = sorted(n for n in new if n in old and json.dumps(old[n], sort_keys=True) != json.dumps(new[n], sort_keys=True))
    print(f"{rel(geo.file)}: {len(bones)} bones; changed {changed}; added {sorted(set(new) - set(old))}; "
          f"removed {sorted(set(old) - set(new))}")
    if "--dry-run" in sys.argv:
        return 0
    entry["bones"] = bones
    save(geo.file, data, header)
    return 0


if __name__ == "__main__":
    sys.exit(main())
