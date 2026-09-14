#!/usr/bin/env python3
"""Crop the viewBox of one or more SVGs tight around their rendered artwork.

Renders each file, takes the union bounding box, and rewrites every viewBox to
one shared square, so a set of variants stays identical in size. The square is
never smaller than what an inscribed circular mask can hold, which is what
avatar crops actually apply.

All inputs must share a user-space coordinate system (variants of one mark do).

    python retighten_viewbox.py --pad 0.03 assets/mark*.svg
    python retighten_viewbox.py --dry-run assets/mark.svg
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

VIEWBOX = re.compile(r'viewBox="\s*([-\d.eE]+)[,\s]+([-\d.eE]+)[,\s]+([-\d.eE]+)[,\s]+([-\d.eE]+)\s*"')


def read_viewbox(svg: Path) -> tuple[float, float, float, float]:
    m = VIEWBOX.search(svg.read_text())
    if not m:
        raise SystemExit(f"{svg}: no viewBox found; add one before cropping")
    return tuple(float(v) for v in m.groups())


def content_points(svg: Path, render_size: int, alpha_threshold: int, scratch: Path) -> np.ndarray:
    """Coordinates of every visible pixel, in the SVG's user space."""
    vx, vy, vw, vh = read_viewbox(svg)
    width = render_size
    height = max(1, round(render_size * vh / vw))
    png = scratch / f"{svg.stem}-bbox.png"
    subprocess.run(
        ["resvg", "--width", str(width), "--height", str(height), str(svg), str(png)],
        check=True,
    )
    alpha = np.asarray(Image.open(png).convert("RGBA"))[..., 3]
    ys, xs = np.nonzero(alpha > alpha_threshold)
    if len(xs) == 0:
        raise SystemExit(f"{svg}: rendered empty; nothing to crop around")
    return np.stack([vx + (xs + 0.5) * vw / width, vy + (ys + 0.5) * vh / height], axis=1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svgs", nargs="+", type=Path)
    ap.add_argument("--pad", type=float, default=0.03, help="breathing room per side, as a fraction (default: 0.03)")
    ap.add_argument("--render-size", type=int, default=1024, help="measurement resolution (default: 1024)")
    ap.add_argument("--alpha-threshold", type=int, default=8, help="alpha above which a pixel counts (default: 8)")
    ap.add_argument("--dry-run", action="store_true", help="report the numbers without editing files")
    args = ap.parse_args()

    if shutil.which("resvg") is None:
        print("resvg not found. Install it with: brew install resvg", file=sys.stderr)
        return 1

    scratch = Path(tempfile.mkdtemp(prefix="logo-crop-"))
    points = []
    for svg in args.svgs:
        p = content_points(svg, args.render_size, args.alpha_threshold, scratch)
        print(f"{svg.name}: x {p[:, 0].min():.1f}-{p[:, 0].max():.1f}  y {p[:, 1].min():.1f}-{p[:, 1].max():.1f}")
        points.append(p)

    allp = np.concatenate(points)
    x0, y0 = allp.min(axis=0)
    x1, y1 = allp.max(axis=0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    box_side = max(x1 - x0, y1 - y0)
    circle_side = 2 * np.hypot(allp[:, 0] - cx, allp[:, 1] - cy).max()
    # Padding is breathing room around the box; the circle is a hard floor, so it
    # raises the result rather than being padded on top of.
    side = max(box_side * (1 + 2 * args.pad), circle_side)

    print(f"\nunion box      {x1 - x0:.1f} x {y1 - y0:.1f}, center ({cx:.1f}, {cy:.1f})")
    padded = box_side * (1 + 2 * args.pad)
    print(f"square needed  {box_side:.1f}, {padded:.1f} with {args.pad:.0%} pad")
    print(f"circle floor   {circle_side:.1f}" + ("  <-- binding, pad ignored" if circle_side > padded else ""))
    print(f"result         {side:.1f}  (artwork fills {100 * box_side / side:.0f}% of the canvas)")

    viewbox = f"{cx - side / 2:.1f} {cy - side / 2:.1f} {side:.1f} {side:.1f}"
    if args.dry_run:
        print(f'\nwould apply viewBox="{viewbox}"')
        return 0

    for svg in args.svgs:
        svg.write_text(VIEWBOX.sub(f'viewBox="{viewbox}"', svg.read_text(), count=1))
    print(f'\napplied viewBox="{viewbox}" to {len(args.svgs)} file(s)')
    print("re-export the PNG sizes now; the old ones have the old crop")
    return 0


if __name__ == "__main__":
    sys.exit(main())
