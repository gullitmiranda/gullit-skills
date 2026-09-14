#!/usr/bin/env python3
"""Measure how faithfully a traced SVG reproduces its source raster.

Renders the SVG at the source's size with resvg, composites it over the source's
own background color, and reports threshold-free fidelity metrics. Writes a
side-by-side and an amplified difference heatmap so the failing layer is visible.

The gates catch structural mistakes — an inverted trace, a dropped layer, the
wrong artwork. They cannot tell you a glow is too weak. Look at the render.

    python compare_render.py source.png traced.svg --out-dir /tmp/svgwork
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image


def render(svg: Path, size: tuple[int, int], dest: Path) -> Image.Image:
    subprocess.run(
        ["resvg", "--width", str(size[0]), "--height", str(size[1]), str(svg), str(dest)],
        check=True,
    )
    return Image.open(dest).convert("RGBA")


def background_of(source: Image.Image) -> np.ndarray:
    """Median of the four corners, so the composite matches the source canvas."""
    a = np.asarray(source.convert("RGB"), dtype=float)
    corners = np.stack([a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]])
    return np.median(corners, axis=0)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path, help="original raster")
    ap.add_argument("svg", type=Path, help="traced SVG to check")
    ap.add_argument(
        "--background",
        default=None,
        help="composite color as R,G,B; defaults to the source's corner color",
    )
    ap.add_argument("--out-dir", type=Path, default=None, help="where to write the comparison images")
    args = ap.parse_args()

    if shutil.which("resvg") is None:
        print("resvg not found. Install it with: brew install resvg", file=sys.stderr)
        return 1

    src = Image.open(args.source).convert("RGB")
    out_dir = args.out_dir or Path(tempfile.mkdtemp(prefix="logo-compare-"))
    out_dir.mkdir(parents=True, exist_ok=True)

    rendered = render(args.svg, src.size, out_dir / f"{args.svg.stem}-render.png")
    if rendered.size != src.size:
        rendered = rendered.resize(src.size, Image.LANCZOS)

    bg = np.array([float(v) for v in args.background.split(",")]) if args.background else background_of(src)
    rgba = np.asarray(rendered, dtype=float)
    alpha = rgba[..., 3:4] / 255.0
    composited = rgba[..., :3] * alpha + bg * (1 - alpha)

    a = np.asarray(src, dtype=float)
    diff = np.abs(a - composited)
    per_pixel = diff.max(axis=2)

    # Coverage: how far each pixel sits from the background, normalized. This is
    # a soft silhouette. A hard threshold would be a trap — a low cut lands in a
    # glow's falloff and a cut near a flat region's own luminance flips that
    # whole region in or out, so either can report a disaster for a good trace.
    def coverage(img: np.ndarray) -> np.ndarray:
        d = np.linalg.norm(img - bg, axis=2)
        scale = np.percentile(d, 99.5)
        return np.clip(d / scale, 0, 1) if scale > 0 else np.zeros_like(d)

    cov_src, cov_svg = coverage(a), coverage(composited)
    overlap = np.minimum(cov_src, cov_svg).sum() / max(np.maximum(cov_src, cov_svg).sum(), 1e-9)

    # Whole-image error flatters a small mark on a big canvas, so also weight the
    # error by where the source actually has artwork.
    mean_error = diff.mean()
    artwork_error = (diff.mean(axis=2) * cov_src).sum() / max(cov_src.sum(), 1e-9)
    badly_wrong = 100 * (per_pixel > 100).mean()

    print(f"mean abs error   {mean_error:.2f} of 255  (whole canvas)")
    print(f"artwork error    {artwork_error:.2f} of 255  (weighted to where the source has ink)")
    print(f"badly wrong px   {badly_wrong:.2f}%  (>100 diff: a missing, extra, or inverted shape)")
    print(f"soft IoU         {overlap:.4f}  (threshold-free silhouette overlap)")

    failures = []
    if artwork_error >= 12:
        failures.append(f"artwork error {artwork_error:.2f} >= 12")
    if badly_wrong >= 0.5:
        failures.append(f"{badly_wrong:.2f}% of pixels badly wrong >= 0.5%")
    if overlap < 0.85:
        failures.append(f"soft IoU {overlap:.4f} < 0.85")
    print("\nFAITHFUL" if not failures else "\nNOT FAITHFUL: " + "; ".join(failures))
    print("Numbers rule out structural mistakes; they do not judge a glow. Look at the render.")

    Image.fromarray(np.clip(per_pixel * 3, 0, 255).astype(np.uint8)).save(out_dir / "diff-heatmap.png")
    side = Image.new("RGB", (src.width * 2, src.height))
    side.paste(src, (0, 0))
    side.paste(Image.fromarray(composited.astype(np.uint8)), (src.width, 0))
    side.save(out_dir / "side-by-side.png")
    print(f"\nwrote {out_dir}/side-by-side.png and {out_dir}/diff-heatmap.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
