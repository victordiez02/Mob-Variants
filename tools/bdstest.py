"""Test the behavior pack in the real engine with a Bedrock Dedicated Server (BDS).

    python -I tools/bdstest.py --bds <BDS folder> [mob ...] [--count 200] [--timeout 600] [--keep]

The BDS folder can also come from the MV_BDS environment variable. Steps (all inside the BDS folder;
the repo is not modified): copies RP, BP and the harness tools/bds/mv_test_bp as development packs,
creates a fresh superflat world "mv_test" with the packs enabled, sets server.properties (backup in
server.properties.mvbak, restored at the end unless --keep), starts the server, and for every mob of the BP
spawns it --count times (fires minecraft:entity_spawned) and reads its mv:* properties.

Reports per mob and property: observed % of each value vs. the % expected from the BP randomize
(mvsim.spawn_distribution, which ignores filters), values never seen, values out of range, and every
error/warning the server prints (pack loading, JSON, scripts). Result also in tools/out/bdstest.json.
Exit code 1 on errors or big deviations.
"""
from __future__ import annotations

import json
import math
import os
import queue
import shutil
import subprocess
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mvlib import ROOT, files, find_pack, load  # noqa: E402
from mvsim import spawn_distribution  # noqa: E402

HARNESS = os.path.join(ROOT, "tools", "bds", "mv_test_bp")
WORLD = "mv_test"
BOSSES = ["minecraft:ender_dragon", "minecraft:wither", "minecraft:warden", "minecraft:elder_guardian"]
PROPS = {
    "level-name": WORLD, "level-type": "FLAT", "gamemode": "creative", "difficulty": "easy",
    "server-port": "19152", "server-portv6": "19153", "content-log-file-enabled": "true",
    "content-log-console-output-enabled": "true", "allow-cheats": "true", "online-mode": "false",
}


def opt(args: list[str], name: str, default: str | None = None) -> str | None:
    return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default


def set_properties(path: str, values: dict[str, str]) -> None:
    lines = open(path, encoding="utf-8").read().splitlines() if os.path.exists(path) else []
    seen: set[str] = set()
    out: list[str] = []
    for line in lines:
        key = line.split("=", 1)[0].strip()
        if not line.lstrip().startswith("#") and key in values:
            out.append(f"{key}={values[key]}")
            seen.add(key)
        else:
            out.append(line)
    out += [f"{k}={v}" for k, v in values.items() if k not in seen]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")


def pack_ref(folder: str) -> dict[str, object]:
    h = load(os.path.join(folder, "manifest.json"))["header"]
    return {"pack_id": h["uuid"], "version": h["version"]}


def prepare(bds: str, mobs: list[dict[str, object]], count: int) -> None:
    rp, bp = find_pack("RP"), find_pack("BP")
    dev_bp, dev_rp = os.path.join(bds, "development_behavior_packs"), os.path.join(bds, "development_resource_packs")
    targets = {os.path.join(dev_bp, "mv_bp"): bp, os.path.join(dev_bp, "mv_test_bp"): HARNESS, os.path.join(dev_rp, "mv_rp"): rp}
    for dst, src in targets.items():
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".mcattributes", "desktop.ini"))
    config = (f"export const MOBS = {json.dumps(mobs)};\nexport const COUNT = {count};\n"
              f"export const BOSS_COUNT = {max(5, count // 10)};\nexport const BOSSES = {json.dumps(BOSSES)};\n")
    with open(os.path.join(dev_bp, "mv_test_bp", "scripts", "config.js"), "w", encoding="utf-8") as f:
        f.write(config)
    world = os.path.join(bds, "worlds", WORLD)
    if os.path.isdir(world):
        shutil.rmtree(world)
    os.makedirs(world)
    with open(os.path.join(world, "world_behavior_packs.json"), "w", encoding="utf-8") as f:
        json.dump([pack_ref(bp), pack_ref(HARNESS)], f, indent=2)
    with open(os.path.join(world, "world_resource_packs.json"), "w", encoding="utf-8") as f:
        json.dump([pack_ref(rp)], f, indent=2)
    props = os.path.join(bds, "server.properties")
    backup = props + ".mvbak"
    if os.path.exists(props) and not os.path.exists(backup):
        shutil.copyfile(props, backup)
    set_properties(props, PROPS)


def run_server(bds: str, timeout: float) -> tuple[list[str], bool]:
    exe = next((os.path.join(bds, n) for n in ("bedrock_server.exe", "bedrock_server") if os.path.exists(os.path.join(bds, n))), None)
    if exe is None:
        raise SystemExit(f"bedrock_server(.exe) not found in {bds}")
    env = dict(os.environ)
    if not exe.endswith(".exe"):
        env["LD_LIBRARY_PATH"] = bds
    p = subprocess.Popen([exe], cwd=bds, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, encoding="utf-8", errors="replace", env=env)
    q: queue.Queue[str | None] = queue.Queue()

    def reader() -> None:
        assert p.stdout is not None
        for line in p.stdout:
            q.put(line.rstrip("\n"))
        q.put(None)

    threading.Thread(target=reader, daemon=True).start()
    lines: list[str] = []
    done = False
    start = time.time()
    stopping = False
    while True:
        try:
            line = q.get(timeout=1)
        except queue.Empty:
            line = ""
        if line is None:
            break
        if line:
            lines.append(line)
            if "MVTEST " in line:
                print("  " + line.split("MVTEST ", 1)[1][:160])
            elif "Server started" in line:
                print("server started, running the harness…")
        if "MVTEST-DONE" in line and not stopping:
            done = True
        if (done or time.time() - start > timeout) and not stopping:
            stopping = True
            assert p.stdin is not None
            p.stdin.write("stop\n")
            p.stdin.flush()
        if stopping and time.time() - start > timeout + 60:
            p.kill()
            break
    p.wait(timeout=30)
    return lines, done


def main() -> int:
    args = sys.argv[1:]
    bds = opt(args, "--bds") or os.environ.get("MV_BDS")
    if not bds or not os.path.isdir(bds):
        print(__doc__)
        return 2
    count = int(opt(args, "--count", "200") or 200)
    timeout = float(opt(args, "--timeout", "600") or 600)
    flagged_values = {"--bds", "--count", "--timeout"}
    only = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] not in flagged_values)]

    mobs: list[dict[str, object]] = []
    expected: dict[str, dict[str, dict[str, float]]] = {}
    ranges: dict[str, dict[str, list[int]]] = {}
    for f in files(find_pack("BP"), "entities"):
        e = load(f)["minecraft:entity"]
        ident = e["description"]["identifier"]
        props = {k: v for k, v in (e["description"].get("properties") or {}).items() if k.startswith("mv:")}
        if not props or (only and ident.split(":")[1] not in only):
            continue
        mobs.append({"id": ident, "props": sorted(props)})
        ranges[ident] = {k: v.get("range", [0, 0]) for k, v in props.items()}
        exp: dict[str, dict[str, float]] = {p: {} for p in props}
        for prob, vals in spawn_distribution(e):
            for p in props:
                k = str(vals.get(p, 0))
                exp[p][k] = exp[p].get(k, 0.0) + prob
        expected[ident] = exp

    print(f"preparing {bds} ({len(mobs)} mobs, {count} each)")
    prepare(bds, mobs, count)
    try:
        lines, done = run_server(bds, timeout)
    finally:
        backup = os.path.join(bds, "server.properties.mvbak")
        if "--keep" not in args and os.path.exists(backup):
            shutil.move(backup, os.path.join(bds, "server.properties"))

    results = {}
    for line in lines:
        if "MVTEST {" in line:
            d = json.loads(line.split("MVTEST ", 1)[1])
            if "mob" in d:
                results[d["mob"]] = d
    log_lines = [ln for ln in lines if ("ERROR" in ln or "WARN" in ln or "[Json]" in ln or "error" in ln.lower())
                 and "MVTEST" not in ln]
    problems = 0
    print()
    if not done:
        print("ERROR: the harness did not finish (timeout or crash); see the server output above")
        problems += 1
    for m in mobs:
        ident = str(m["id"])
        r = results.get(ident)
        if r is None:
            print(f"{ident}: no result")
            problems += 1
            continue
        head = f"{ident}: spawned {r['spawned']}, read {r['read']}" + (f", spawn error: {r['error']}" if r.get("error") else "")
        print(head)
        n = max(int(r["read"]), 1)
        for p, counts in r["counts"].items():
            lo, hi = ranges[ident][p]
            exp_p: dict[str, float] = expected[ident][p]
            notes: list[str] = []
            for k in sorted(set(counts) | set(exp_p), key=lambda x: (len(x), x)):
                obs = counts.get(k, 0) / n
                want = exp_p.get(k, 0.0)
                sigma = math.sqrt(max(want * (1 - want), 1e-9) / n)
                bad = abs(obs - want) > 4 * sigma + 0.02
                out_of_range = k.lstrip("-").isdigit() and not lo <= int(k) <= hi
                if bad or out_of_range:
                    notes.append(f"{k}: {obs:.1%} (expected {want:.1%}){' OUT OF RANGE' if out_of_range else ''}")
            status = "OK" if not notes else "CHECK"
            problems += bool(notes)
            print(f"    {p}: {status} ({len(counts)} values seen)" + "".join("\n        " + x for x in notes))
    if log_lines:
        print("\nserver errors/warnings:")
        for ln in dict.fromkeys(log_lines):
            print("  " + ln[:300])
        problems += 1
    os.makedirs(os.path.join(ROOT, "tools", "out"), exist_ok=True)
    with open(os.path.join(ROOT, "tools", "out", "bdstest.json"), "w", encoding="utf-8") as f:
        json.dump({"results": results, "expected": expected, "log": log_lines}, f, indent=1)
    print("\n" + ("RESULT: OK" if not problems else f"RESULT: {problems} things to check "
                                                     "(deviations can come from event filters: biome, baby…)"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
