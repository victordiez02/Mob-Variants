"""Build the distributable packages into dist/.

    python -I tools/package.py

Creates dist/MobVariants_RP_<version>.mcpack, dist/MobVariants_BP_<version>.mcpack and
dist/MobVariants_<version>.mcaddon (both packs). Editor-only files (.mcattributes, desktop.ini…) are left
out. Fails if the manifests disagree (versions, BP -> RP dependency).
"""
from __future__ import annotations

import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import ROOT, find_pack, load, rel  # noqa: E402

SKIP_NAMES = {".mcattributes", "desktop.ini", "Thumbs.db", ".DS_Store"}


def manifest_problems(rp: str, bp: str) -> list[str]:
    r, b = load(os.path.join(rp, "manifest.json")), load(os.path.join(bp, "manifest.json"))
    out: list[str] = []
    rv, bv = r["header"]["version"], b["header"]["version"]
    if rv != bv:
        out.append(f"RP version {rv} != BP version {bv}")
    for m in r.get("modules", []) + b.get("modules", []):
        if m.get("version") != rv:
            out.append(f"module {m.get('uuid')} version {m.get('version')} != {rv}")
    dep = [d for d in b.get("dependencies", []) if d.get("uuid") == r["header"]["uuid"]]
    if not dep:
        out.append("BP does not depend on the RP uuid")
    elif dep[0].get("version") != rv:
        out.append(f"BP depends on RP {dep[0].get('version')}, RP is {rv}")
    if r["header"]["min_engine_version"] != b["header"]["min_engine_version"]:
        out.append("RP and BP min_engine_version differ")
    return out


def add_tree(z: zipfile.ZipFile, src: str, prefix: str) -> int:
    n = 0
    for dirpath, dirnames, filenames in os.walk(src):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for name in sorted(filenames):
            if name in SKIP_NAMES:
                continue
            full = os.path.join(dirpath, name)
            arc = os.path.join(prefix, os.path.relpath(full, src)).replace("\\", "/")
            z.write(full, arc)
            n += 1
    return n


def main() -> int:
    rp, bp = find_pack("RP"), find_pack("BP")
    problems = manifest_problems(rp, bp)
    for p in problems:
        print("ERROR", p)
    if problems:
        return 1
    version = ".".join(str(x) for x in load(os.path.join(rp, "manifest.json"))["header"]["version"])
    dist = os.path.join(ROOT, "dist")
    os.makedirs(dist, exist_ok=True)
    outputs = {
        f"MobVariants_RP_{version}.mcpack": [(rp, "")],
        f"MobVariants_BP_{version}.mcpack": [(bp, "")],
        f"MobVariants_{version}.mcaddon": [(rp, "MobVariants_RP"), (bp, "MobVariants_BP")],
    }
    for name, trees in outputs.items():
        path = os.path.join(dist, name)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            n = sum(add_tree(z, src, prefix) for src, prefix in trees)
        print(f"{rel(path)}  {n} files  {os.path.getsize(path) / 1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
