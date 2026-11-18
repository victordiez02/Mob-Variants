"""Check variants in Blockbench without driving it by hand (needs Blockbench open with the MCP bridge).

    python -I tools/bbcheck.py <mob> [bbscene options] [--anim A ...] [--views front_right,left] [--frames 4] [--size 320]
        Loads the variant (bbscene), plays each animation (default: the ones the entity has that move
        something; the pose/setup ones always play) and saves ONE contact sheet:
        tools/out/bb/<mob>_sheet.png (rows = animation and view, columns = moments). Also measures layers.
    python -I tools/bbcheck.py --measure [mob ...] [--max-px 0.5] [--verbose]
        No images: for each mob (default all), with every layer it can draw, how far each layer's cubes
        drift from the vanilla bone with the same name during every animation an adult runs (baby-only
        animations are skipped: skins never apply to babies). A layer that copies the vanilla bone's name,
        pivot and parent stays at 0 px. Prints only drifting layers (--verbose: also OK ones and cubes that
        could not be measured). Exit code 1 if any layer drifts more than --max-px.

Talks to the bridge at 127.0.0.1:8787 (the same one the MCP uses). Never starts Blockbench: if the bridge
is not up it says what the user must do. Leaves a temporary project open in Blockbench.
"""
from __future__ import annotations

import base64
import io
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bbscene import build  # noqa: E402
from mvlib import ROOT, files, find_pack, require_vanilla  # noqa: E402

BRIDGE = "http://127.0.0.1:8787"
NOT_UP = ("Blockbench bridge not reachable. Ask the user: open Blockbench (desktop); the toast "
          "'MCP server started on port 8787' must appear (else Tools > Start MCP Server).")
_ids = 0


def call(action: str, params: dict[str, Any], timeout: float = 120) -> Any:
    global _ids
    _ids += 1
    body = json.dumps({"id": f"bbcheck{_ids}", "action": action, "params": params}).encode()
    req = urllib.request.Request(f"{BRIDGE}/command", data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            res = json.loads(r.read().decode("utf-8"))
    except (urllib.error.URLError, ConnectionError) as e:
        raise SystemExit(f"{NOT_UP} ({e})") from e
    if not res.get("ok"):
        raise RuntimeError(f"{action}: {res.get('error')}")
    return res.get("result")


def js(code: str) -> Any:
    return call("execute_script", {"code": code})


def load(argv: list[str]) -> tuple[Any, Any]:
    sc = build(argv)
    report = js(sc.code)
    return sc, report


def moving_animations(sc: Any) -> list[str]:
    names = [n for n in sc.data["animations"] if n not in sc.data["active"]]
    prefer = [n for n in names if any(k in n for k in ("walk", "move", "attack", "fly", "swim"))]
    return prefer[:3] or names[:2]


def sheet(argv: list[str], anims: list[str], views: list[str], frames: int, size: int) -> int:
    from PIL import Image, ImageDraw

    sc, report = load(argv)
    print("\n".join(sc.info))
    anims = anims or moving_animations(sc)
    lengths = js("return Object.fromEntries(Animation.all.map(a => [a.name, a.length || 1]))")
    rows: list[tuple[str, list[Image.Image]]] = []
    rest: list[Image.Image] = []
    for view in views:
        js("return mvPose(null, 0)")
        rest.append(_shot(view, size))
    rows.append(("reposo (pose base)", rest))
    for anim in anims:
        if anim not in lengths:
            print(f"  animation not in scene: {anim}")
            continue
        for view in views:
            shots = []
            for i in range(frames):
                t = lengths[anim] * (i + 0.5) / frames
                js(f"return mvPose({json.dumps(anim)}, {t})")
                shots.append(_shot(view, size))
            rows.append((f"{anim}  [{view}]", shots))
    js("return mvPose(null, 0)")
    cols = max(len(r[1]) for r in rows)
    label_h = 18
    out = Image.new("RGB", (cols * size, len(rows) * (size + label_h)), (30, 32, 36))
    d = ImageDraw.Draw(out)
    for r, (label, imgs) in enumerate(rows):
        y = r * (size + label_h)
        d.text((4, y + 3), label, fill=(230, 230, 230))
        for c, im in enumerate(imgs):
            out.paste(im.convert("RGB"), (c * size, y + label_h))
    mob = argv[0]
    path = os.path.join(ROOT, "tools", "out", "bb", f"{mob}_sheet.png")
    out.save(path)
    print(f"sheet: {os.path.relpath(path, ROOT)}  ({len(rows)} rows x {cols})")
    m = js(f"return mvMeasure({json.dumps(anims)})")
    _print_measure(mob, m, 0.5)
    return 0


def _shot(view: str, size: int) -> Any:
    from PIL import Image
    res = call("screenshot", {"view": view})
    img = Image.open(io.BytesIO(base64.b64decode(res["base64"])))
    img.thumbnail((size, size))
    canvas = Image.new("RGBA", (size, size), (30, 32, 36, 255))
    canvas.paste(img, ((size - img.width) // 2, (size - img.height) // 2))
    return canvas


def _print_measure(mob: str, m: Any, max_px: float, verbose: bool = True, full: set[str] | None = None) -> bool:
    """Prints only drifting layers unless verbose (OK layers and cubes that could not be measured).

    Full replacement models (`full`) are drawn instead of the base, not over it: their drift says how
    differently vanilla animations move them (pivots not vanilla), tagged FULL and not counted as BAD."""
    full = full or set()
    bad = False
    for geo, w in sorted(m["worst"].items()):
        drift = w["px"] > max_px
        if drift and geo in full:
            if verbose:
                print(f"  FULL {mob:17} {geo:40} {w['px']:6.2f} px  ({w['bone']} in {w['animation']}; full model, pivots not vanilla)")
            continue
        bad |= drift
        if drift:
            print(f"  BAD {mob:18} {geo:40} {w['px']:6.2f} px  ({w['bone']} in {w['animation']} t={w['time']})")
        elif verbose:
            print(f"  OK  {mob:18} {geo:40} {w['px']:6.2f} px")
    if verbose:
        for geo, n in m.get("unanchored", {}).items():
            print(f"  note {mob:17} {geo}: {n} cubes not under any bone the base model has (not measured)")
    return bad


def measure(mobs: list[str], max_px: float, verbose: bool) -> int:
    require_vanilla()
    names = mobs or [os.path.basename(f).split(".")[0] for f in files(find_pack("RP"), "entity")]
    bad = layers = 0
    for mob in names:
        sc = build([mob, "--all-layers"])
        if len(sc.data["layers"]) < 2:
            continue  # nothing to compare: do not load it into Blockbench
        try:
            js(sc.code)
            m = js("return mvMeasure()")
        except RuntimeError as e:
            print(f"  ERR {mob}: {e}")
            continue
        full = {x["geometry"] for x in sc.data["layers"] if x.get("full_model")}
        bad += _print_measure(mob, m, max_px, verbose, full)
        layers += len(m["worst"])
    print(f"{layers} layers measured; mobs with layers drifting more than {max_px} px: {bad}")
    return 1 if bad else 0


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 2

    def take(name: str, default: str | None = None) -> str | None:
        if name in a:
            i = a.index(name)
            v = a[i + 1] if i + 1 < len(a) else default
            del a[i:i + 2]
            return v
        return default

    if "--measure" in a:
        a.remove("--measure")
        max_px = float(take("--max-px", "0.5") or 0.5)
        verbose = "--verbose" in a
        return measure([x for x in a if not x.startswith("--")], max_px, verbose)
    anims: list[str] = []
    while "--anim" in a:
        anims.append(take("--anim") or "")
    views = (take("--views", "front_right,left") or "front_right").split(",")
    frames = int(take("--frames", "4") or 4)
    size = int(take("--size", "320") or 320)
    return sheet(a, anims, views, frames, size)


if __name__ == "__main__":
    sys.exit(main())
