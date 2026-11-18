"""Run every static check and print a short verdict (the command to use after any change).

    python -I tools/check.py [mob ...]

Runs validate.py, bpcheck.py and simulate.py (only for the given mobs, if any) and shows their
errors and warnings. Use the individual scripts to see everything. Exit code 1 if any fails.
"""
from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


def keep(script: str, section: str, line: str) -> bool:
    """Lines worth showing in the summary."""
    if script == "validate.py":
        return not line.startswith("  ") or section in ("ERRORS", "WARNINGS")
    if script == "bpcheck.py":
        return "ERROR" in line or "warning" in line or line.startswith("files")
    return line.startswith("    ") and "never drawn" not in line


def run(script: str, *args: str) -> tuple[int, str]:
    p = subprocess.run([sys.executable, "-I", os.path.join(HERE, script), *args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout + p.stderr


def main() -> int:
    mobs = sys.argv[1:]
    failed = False
    for script, args in (("validate.py", []), ("bpcheck.py", []), ("simulate.py", mobs)):
        code, out = run(script, *args)
        failed |= code != 0
        print(f"=== {script}: {'OK' if code == 0 else 'FAILED'}")
        section = ""
        for line in out.splitlines():
            if line.startswith("== "):
                section = line.split()[1]
            if keep(script, section, line):
                print(line)
    print("=== RESULT:", "FAILED" if failed else "OK")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
