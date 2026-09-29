# Heliotrope — Screenshot Harness

Her aesthetic is dark blue + shimmer + glow. Readability is policed by
script, not by eyeballing. This doc defines the standard shots; the
contrast script (`testing/scripts/contrast.py`) enforces the numbers.

## Standard shots

Every shipped screen gets both, every gate:

| Name | Viewport | DPR | Tool |
|------|----------|-----|------|
| iPhone | 390x844, mobile, touch | 2 | `~/workspace/.venvs/eyes/shoot.py <html> <out.png>` (defaults) |
| Desktop | 1280x800 | 1 | `shoot.py <html> <out.png> 1280 800` |

- `wait_ms`: 2500 default. Use 4000+ for screens with entrance
  animations or async data (glows need to settle before the contrast
  script samples pixels).
- Evidence lives at `testing/evidence/<gate>/<flow>/` with the shot +
  a `contrast.txt` report from the script.
- Screenshots containing her real seeded data never leave the local
  machine (same privacy rule as everything else).

## Contrast checks — the method

The dark shimmer background is a gradient with glow; a single background
color doesn't exist. So the script does this:

1. Render the page at iPhone 390x844 DPR2, wait for animations to settle.
2. Collect every visible text element (computed color, font size/weight,
   bounding rect).
3. Sample real pixels from the screenshot at multiple points across each
   text element's box — top, middle, bottom, left, right — because the
   shimmer moves behind the words.
4. Compute the WCAG 2.1 contrast ratio of the text color against the
   WORST (lowest-ratio) sampled background point. The worst point is the
   verdict; glow hotspots don't get to hide dim text.
5. Report PASS/FAIL per element + a summary. Non-zero exit on any FAIL.

### Thresholds

| Text | WCAG bar | Our bar (her taste, dark bg) |
|------|----------|------------------------------|
| Normal text (< 24px, or < 18.66px bold) | 4.5:1 AA | **7:1** — fail below 4.5:1, warn 4.5–7 |
| Large text (≥ 24px, or ≥ 18.66px bold) | 3:1 AA | **4.5:1** — fail below 3:1, warn 3–4.5 |
| UI components / icons conveying meaning | 3:1 | 3:1 hard fail |

Why stricter than WCAG: small glowing text on a moving shimmer
background reads worse than the math says. The warn band (4.5–7:1) goes
to the artist reviewer; the fail band blocks the gate.

### Running it

```bash
~/workspace/.venvs/eyes/bin/python testing/scripts/contrast.py <html-or-url> [--out report.txt] [--min-normal 4.5] [--min-large 3.0]
```

Reads back the page's real rendered pixels — never trust the CSS hex
values alone (gradients, glows, and translucency lie).

## Tap tests

Pathway tap verification uses the same Playwright/Chromium setup.
Every tap that should do something gets its tap verified on the iPhone
viewport with touch enabled — dead taps are FAIL-BLOCKED. (Full tap
scripts land in Phase 2 when screens exist.)

## What "verified" means

Per her standing rule: verified = the testing lead looked at the real
render with their own eyes AND the contrast script passed. Screenshots
are compared side-by-side at the same size against her references —
never a glance at a thumbnail.
