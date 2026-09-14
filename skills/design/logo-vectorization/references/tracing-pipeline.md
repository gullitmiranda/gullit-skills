# Tracing Pipeline

Raster mark in, layered SVG out. Numbers below are for a 1024 x 1024 working
space; scale them if the canvas differs.

## Setup

```sh
brew install potrace resvg
python3 -m venv .venv && .venv/bin/pip install pillow numpy
```

Work in a scratch directory, not in the repo. Only finished files get committed.

## 1. Separate layers

Classify source pixels into the smallest set of regions that carry the design —
typically panel, outline/rim, and each accent shape. Use hue for chromatic
separation and luminance for the rest. Print the pixel count per layer before
tracing; a layer with a few hundred pixels is a threshold mistake, not a shape.

Interior regions (the fill inside a closed outline) are best recovered with a
flood fill from outside the outline, then inverted.

**Gotcha:** `ImageDraw.floodfill` silently does nothing on a PIL image backed by
a NumPy array, because the buffer is read-only. Force a copy:

```python
im = Image.fromarray(mask_u8).copy()      # .copy() is load-bearing
ImageDraw.floodfill(im, (0, 0), 128)
filled = np.array(im)
```

## 2. Trace each layer

Supersample 2x before thresholding so potrace sees clean edges, and use a soft
threshold (half-width ~12 levels of 255) instead of a hard cut, to keep
antialiased edges from turning into stairs.

```python
SS = 2                                     # supersample factor
big = im.resize((w * SS, h * SS), Image.BICUBIC)

def soft(x, t, hw=12.0):                   # t = threshold, hw = half-width
    return np.clip((x - (t - hw)) / (2 * hw), 0, 1)
```

Write the PGM **inverted**, because potrace traces dark pixels:

```python
Image.fromarray(((1 - np.clip(alpha, 0, 1)) * 255).astype(np.uint8), "L").save(pgm)
```

```sh
potrace -b svg -k 0.5 -t 4 -a 1.0 -O 0.2 -u 10 -o layer.svg layer.pgm
```

- `-t 4` drops specks; raise it if the trace picks up compression noise.
- `-a 1.0` and `-O 0.2` keep curves smooth without flattening corners.
- `-u 10` fixes the output unit so coordinates stay easy to rescale.

potrace emits its own `<g transform="...">` with a flipped Y axis. Do not keep
it. Bake the transform into the path data instead, mapping into the final space
with `X = x * s` and `Y = H - y * s`, negating `dy` for relative commands. One
transform per file is one more thing that breaks when the viewBox is cropped.

## 3. Recompose and recolor

One `<path>` per layer, one `<linearGradient>` per path, all with
`gradientUnits="userSpaceOnUse"`. Sample the stops from the source: erode the
layer mask a few pixels so edge antialiasing does not pollute the sample, then
take percentile bands along the gradient axis.

Set each gradient's `y1`/`y2` to the layer's own extent, not the canvas. Stop
positions then stay readable against the original artwork, and recoloring a
variant is just editing hex values.

**Keep path coordinates in the original working space.** Crop with the viewBox
only (step 4 of the skill). Rewriting coordinates to a cropped origin makes
every gradient offset meaningless.

## 4. Glow

Reproduce a neon glow as a blurred copy of the path underneath the sharp fill,
not as baked pixels. Two filters read better than one — a wide halo plus a tight
bloom:

```xml
<filter id="glowWide" x="-35%" y="-35%" width="170%" height="170%"
        color-interpolation-filters="sRGB">
  <feGaussianBlur stdDeviation="20"/>
</filter>
<filter id="glowTight" x="-25%" y="-25%" width="150%" height="150%"
        color-interpolation-filters="sRGB">
  <feGaussianBlur stdDeviation="5"/>
</filter>
```

- `stdDeviation` ~2% of canvas for the halo, ~0.5% for the bloom.
- The enlarged filter region is required. At the default `-10%/120%` the blur is
  clipped into a visible box.
- `color-interpolation-filters="sRGB"` is required. The linearRGB default
  renders the glow washed out and too wide.

**Do not tune the glow by minimizing pixel error.** Blur bleeds into the dark
background, so the diff-optimal `stdDeviation` is always too small and the mark
looks flat. Render a sweep, look at it, and expect to land around 1.3-1.5x the
numeric optimum.

## 5. Verify

```sh
python scripts/compare_render.py source.png traced.svg --out-dir /tmp/svgwork
```

It prints a FAITHFUL / NOT FAITHFUL verdict from three threshold-free numbers,
and writes a side-by-side plus a difference heatmap that shows which layer is
wrong.

The gates are calibrated on two verified traces, which scored artwork error
7.5 and 9.0, zero badly-wrong pixels, and soft IoU 0.895 and 0.878. Feeding one
mark's raster against the other mark's SVG scores 78.7, 7.8%, and 0.284, so the
gates separate a good trace from a broken one by a wide margin.

**What the verdict does not cover:** it rules out structural mistakes — an
inverted trace, a dropped layer, a mangled path — and says nothing about whether
the glow is right or the curves are pretty. Always look at the side-by-side.

Do not swap these for a hard-threshold silhouette IoU. Every fixed luminance cut
is palette-dependent: on this artwork, IoU ranged from 0.67 to 0.99 across cuts
for the *same* faithful trace, because one cut landed on the dark panel's own
luminance and others landed inside the glow falloff.
