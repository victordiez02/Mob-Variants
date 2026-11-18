"""Read Minecraft's Content Log (no need to copy it by hand).

    python -I tools/contentlog.py [--since HH:MM] [--all] [--verbose] [--file PATH] [--list]

Default: newest %APPDATA%/Minecraft Bedrock/logs/ContentLog*.txt, only [error]/[warning] entries,
grouped (same message counted once). The game appends to the same file until it restarts, so use
--since with the time the world was entered. --all also shows [inform]; --verbose shows [verbose].
Exit code 1 if there are errors.
"""
from __future__ import annotations

import glob
import os
import re
import sys
from collections import Counter

_ENTRY = re.compile(r"^(\d\d:\d\d:\d\d)\[([^\]]+)\]\[([^\]]+)\]-(.*)$")


def log_dir() -> str:
    return os.path.join(os.environ.get("APPDATA", ""), "Minecraft Bedrock", "logs")


def parse(path: str) -> list[tuple[str, str, str, str]]:
    """[(time, category, level, message)] with continuation lines joined."""
    out: list[tuple[str, str, str, str]] = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            m = _ENTRY.match(line)
            if m:
                out.append((m.group(1), m.group(2), m.group(3), m.group(4)))
            elif out and line.strip():
                t, c, lv, msg = out[-1]
                out[-1] = (t, c, lv, msg + " " + line.strip())
    return out


def main() -> int:
    args = sys.argv[1:]

    def opt(name: str) -> str | None:
        return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else None

    logs = sorted(glob.glob(os.path.join(glob.escape(log_dir()), "ContentLog*.txt")), key=os.path.getmtime)
    if "--list" in args:
        for p in logs:
            print(p)
        return 0
    path = opt("--file") or (logs[-1] if logs else None)
    if not path:
        print("no Content Log found in", log_dir())
        return 2
    levels = {"error", "warning"} | ({"inform"} if "--all" in args else set()) | ({"verbose"} if "--verbose" in args else set())
    since = opt("--since") or ""
    entries = [e for e in parse(path) if e[2] in levels and e[0] >= since]
    print(f"{path}  ({len(entries)} entries{', since ' + since if since else ''})")
    groups: Counter[tuple[str, str, str]] = Counter()
    first: dict[tuple[str, str, str], str] = {}
    for t, cat, lv, msg in entries:
        key = (lv, cat, msg[:400])
        groups[key] += 1
        first.setdefault(key, t)
    for (lv, cat, msg), n in sorted(groups.items(), key=lambda kv: (kv[0][0] != "error", first[kv[0]])):
        print(f"{first[(lv, cat, msg)]} [{cat}][{lv}] x{n}  {msg}")
    return 1 if any(k[0] == "error" for k in groups) else 0


if __name__ == "__main__":
    sys.exit(main())
