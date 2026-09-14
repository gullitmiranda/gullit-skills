---
name: logo-vectorization
description: >-
  Trace a raster logo into a faithful multi-color SVG, recolor it into variants,
  and crop it for avatars, favicons, and app icons. Use when converting a logo
  or brand mark PNG to SVG, recoloring a mark, or when a logo breaks on a light
  background or inside a circular avatar crop.
---

# Logo Vectorization

Turn a raster mark into a shipped asset set: traced SVG, color variants, and
exports sized for real surfaces.

## Hard Rules

- Do not trace a full-color image in one pass. Split it into color and
  luminance layers, trace each, recompose. One pass throws the palette away.
- potrace reads **dark** as foreground. Invert every mask before writing the
  PGM, or the trace comes out inside-out.
- Export PNG with `resvg` only. `qlmanage` flattens alpha onto white and
  `cairosvg` drops SVG filters, silently deleting a glow.
- Do not ship a viewBox inherited from the source raster. Measure the rendered
  bounding box and re-crop, or the mark floats inside every avatar badge.
- A glow mark dies on a light background. Do not fix that by removing the glow;
  give it its own dark panel, or ship a separate file and say where each is
  allowed.
- Never report fidelity you did not compute. Render, diff, then speak.
- Choose between options by rendering them side by side on the real
  backgrounds, not by describing them.

## Model and Reasoning

- Trace, sweep parameters, and decide crop and light/dark on a frontier
  multimodal model at **high reasoning effort**. Validated end to end on Claude
  Opus 5 at high effort in Cursor — one run, so a known-good starting point,
  not a benchmark.
- The model must render images into its own context and look at them. A
  text-only model cannot tell an under-glow from a correct one: the numerically
  optimal glow here is visibly wrong.
- Delegate only the mechanical tail to a fast model — re-exporting sizes,
  renaming, wiring references, drafting the assets README.

## Procedure

1. Install `potrace` and `resvg`, plus `pillow` and `numpy`.
2. Trace by layer and recompose with gradients sampled from the source,
   following references/tracing-pipeline.md.
3. Verify with `scripts/compare_render.py` until the verdict is FAITHFUL, then
   look at the side-by-side yourself and show it to the user. The verdict
   catches structural mistakes, not weak glow.
4. Settle variants, light and dark, crop, and badge color using
   references/delivery-checks.md and `scripts/retighten_viewbox.py`.
5. Export the size set, wire the app and repo references, and document what
   each file is for and where it must not be used.
