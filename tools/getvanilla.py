"""Download the vanilla reference packs (Mojang/bedrock-samples) into vanilla/.

    python -I tools/getvanilla.py            # download VERSION if vanilla/ is missing or older
    python -I tools/getvanilla.py --force    # download again
    python -I tools/getvanilla.py --version  # print the version the project uses

VERSION is the single source of truth (CI caches by it). To move to a new Minecraft version, change
it to the new stable tag of https://github.com/Mojang/bedrock-samples/releases and run --force.
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile

VERSION = "v1.26.60.5"
URL = "https://github.com/Mojang/bedrock-samples/releases/download/{v}/bedrock-samples-{v}-full.zip"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "vanilla")


def installed() -> str:
    try:
        with open(os.path.join(DEST, "VERSION.txt"), encoding="utf-8") as f:
            return f.read().split()[1]
    except (OSError, IndexError):
        return ""


def main() -> int:
    if "--version" in sys.argv:
        print(VERSION)
        return 0
    if installed() == VERSION and "--force" not in sys.argv:
        print(f"vanilla/ already at {VERSION}")
        return 0
    url = URL.format(v=VERSION)
    with tempfile.TemporaryDirectory() as tmp:
        zpath = os.path.join(tmp, "samples.zip")
        print("downloading", url)
        req = urllib.request.Request(url, headers={"User-Agent": "mob-variants-tools"})
        with urllib.request.urlopen(req) as r, open(zpath, "wb") as f:
            shutil.copyfileobj(r, f, 1 << 20)
        out = os.path.join(tmp, "x")
        with zipfile.ZipFile(zpath) as z:
            for name in z.namelist():  # refuse paths that escape the target folder
                if name.startswith(("/", "\\")) or ".." in name.replace("\\", "/").split("/"):
                    raise SystemExit(f"unsafe path in zip: {name}")
            z.extractall(out)
        src = out
        for dirpath, dirnames, _ in os.walk(out):  # the folder that holds resource_pack/
            if "resource_pack" in dirnames and "behavior_pack" in dirnames:
                src = dirpath
                break
        else:
            raise SystemExit("resource_pack/ and behavior_pack/ not found in the zip")
        if os.path.isdir(DEST):
            shutil.rmtree(DEST)
        shutil.move(src, DEST)
    with open(os.path.join(DEST, "VERSION.txt"), "w", encoding="utf-8") as f:
        f.write(f"Mojang/bedrock-samples {VERSION} (stable)\n")
    print("vanilla/ ready at", VERSION)
    return 0


if __name__ == "__main__":
    sys.exit(main())
