# Delivery Checks

Between a faithful trace and a shippable mark sit decisions that only render
tests can settle. Run these in order; each one narrows the next.

## 1. Light and dark

Render the mark on white, light gray, dark, and over a photo. A glow drawn for
a dark background turns into a gray smudge on white.

There are two fixes, and the difference matters:

- **Panel.** Give the mark its own dark background shape. The file still has a
  transparent canvas but no longer depends on one, so it reads the same
  everywhere. This is the only form that is safe as an avatar.
- **Open.** No panel, neon floating on whatever is behind it. Keep it for dark
  surfaces at large sizes and say so in the docs.

Flattening the glow to survive white is the wrong third option: it costs the
mark its character and still looks weaker than the panel version.

Ship the panel form as primary. Keep the open form only if the user wants it,
and name it so the constraint is visible (`-open`).

## 2. Crop

Generated artwork carries padding that was never meant to ship. Platforms add
their own inset on top, so baked padding gets counted twice and the mark ends up
floating in the middle of a badge.

```sh
python scripts/retighten_viewbox.py --pad 0.03 assets/mark*.svg
```

The script renders each file, takes the union bounding box, and rewrites every
viewBox to one shared square so a set of variants stays visually identical in
size. Padding is breathing room around that box, but the script also computes
the **minimum square that survives a circular mask** from the farthest content
pixel, and treats it as a hard floor that overrides a too-small pad.

On the validated mark: bounding box 808 units, circle floor 836, result 857 at
3% pad — artwork filling 94% of the canvas. At 100% a circular avatar mask cut
the top arc and the bottom tip.

Left and right gaps that exist because the artwork is taller than it is wide are
not padding. Do not try to close them.

## 3. Small sizes

Render 16, 32, and 64px on light and dark and look at them. Marks that depend
on an outline lose their silhouette first; that is usually what rules out the
open variant below ~64px and decides whether the favicon needs a simplified
file.

## 4. Badge background

When the mark sits inside a platform badge (GitHub App avatar, Slack), the badge
color has to contrast with the mark's **own panel**, not with the page.

Compute the contrast ratio rather than guessing. A dark badge behind a
dark-panel mark measured 1.1:1 — the panel merged into the circle and the
silhouette disappeared.

Recommend a light badge. Pulling the value from the artwork's own palette (the
first stop of an accent gradient, e.g. `#ede9fe`) reads as intentional; `#fff`
is the neutral fallback.

## 5. Exports

Transparent PNG at 1024, 512, 256, 128, 64, 32 for the panel variants. 512 is a
good avatar default.

```sh
resvg --width 512 --height 512 assets/mark.svg assets/png/mark-512.png
```

Renderers that ignore SVG filters drop the glow, since it is an `feGaussianBlur`
rather than baked pixels. `resvg` and browsers handle it.

## 6. Wiring and naming

- Name files by role. Never ship the primary asset under an exploration name
  like `alt`, `v2`, or `final`.
- Find every existing reference to the old logo before swapping — app `public/`,
  favicon in the HTML head, README, and any platform avatar uploaded by hand.
- If the app keeps copies rather than symlinks, say so in the assets README so
  the next change re-copies them.
- Move superseded assets to `legacy/` instead of deleting, and write down why
  they are kept.
- The assets README should say, per file, what it is and where it must not be
  used. That constraint is the part nobody can rediscover from the file itself.
