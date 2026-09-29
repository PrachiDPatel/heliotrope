#!/usr/bin/env python3
"""Contrast checker for Heliotrope's dark shimmer backgrounds.

Renders the page, then for every visible text element samples REAL
screenshot pixels across its bounding box (top/mid/bottom, left/mid/right)
and reports the WORST WCAG 2.1 contrast ratio. Glow hotspots don't get to
hide dim text.

Usage:
    contrast.py <html-or-url> [--out report.txt]
                [--min-normal 4.5] [--min-large 3.0] [--wait 4000]

Exit code 0 = all text passed, 1 = at least one FAIL.
"""
import sys
import math
import argparse
from io import BytesIO

from playwright.sync_api import sync_playwright
from PIL import Image


def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)


def ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def parse_rgb(s):
    # "rgb(255, 255, 255)" / "rgba(255, 255, 255, 0.8)" -> (r,g,b)
    s = s.strip()
    inner = s[s.index("(") + 1 : s.rindex(")")]
    parts = [p.strip() for p in inner.split(",")]
    return tuple(int(float(parts[i])) for i in range(3))


ELEMENT_JS = """() => {
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  let el;
  while ((el = walker.nextNode())) {
    if (!el.textContent || !el.textContent.trim()) continue;
    // skip if all text lives in child elements (avoid double counting parents)
    const own = Array.from(el.childNodes)
      .filter(n => n.nodeType === 3 && n.textContent.trim()).length;
    if (!own) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (parseFloat(cs.opacity || '1') < 0.05) continue;
    const rects = Array.from(el.getClientRects()).filter(r => r.width > 1 && r.height > 1);
    if (!rects.length) continue;
    const r = rects[0];
    const fs = parseFloat(cs.fontSize);
    const bold = parseInt(cs.fontWeight) >= 700;
    out.push({
      text: el.textContent.trim().slice(0, 60),
      color: cs.color,
      fontSize: fs,
      bold: bold,
      x: r.x, y: r.y, w: r.width, h: r.height,
    });
    if (out.length > 400) break;
  }
  return out;
}"""


def sample_points(rect, scale):
    x, y, w, h = rect["x"], rect["y"], rect["w"], rect["h"]
    pts = []
    for fy in (0.15, 0.5, 0.85):
        for fx in (0.15, 0.5, 0.85):
            pts.append((int((x + w * fx) * scale), int((y + h * fy) * scale)))
    return pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--out", default=None)
    ap.add_argument("--min-normal", type=float, default=4.5)
    ap.add_argument("--min-large", type=float, default=3.0)
    ap.add_argument("--wait", type=int, default=4000)
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--height", type=int, default=844)
    args = ap.parse_args()

    scale = 2  # device_scale_factor
    results = []
    with sync_playwright() as p:
        b = p.chromium.launch(
            executable_path="/opt/meta-chromium/chrome",
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        pg = b.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=scale,
            is_mobile=True,
            has_touch=True,
        )
        url = args.target
        if not url.startswith(("http://", "https://", "file://")):
            url = "file://" + url
        pg.goto(url)
        pg.wait_for_timeout(args.wait)
        shot = pg.screenshot()
        elements = pg.evaluate(ELEMENT_JS)
        b.close()

    img = Image.open(BytesIO(shot)).convert("RGB")
    px = img.load()
    W, H = img.size

    fails = 0
    for el in elements:
        try:
            fg = parse_rgb(el["color"])
        except Exception:
            continue
        large = el["fontSize"] >= 24 or (el["fontSize"] >= 18.66 and el["bold"])
        minimum = args.min_large if large else args.min_normal
        worst = 21.0
        for sx, sy in sample_points(el, scale):
            sx = min(max(sx, 0), W - 1)
            sy = min(max(sy, 0), H - 1)
            worst = min(worst, ratio(fg, px[sx, sy]))
        verdict = "PASS" if worst >= minimum else "FAIL"
        if verdict == "FAIL":
            fails += 1
        results.append(
            f"{verdict}  {worst:5.2f}:1  (min {minimum:.1f}, "
            f"{'large' if large else 'normal'}, {el['fontSize']:.0f}px)  "
            f"'{el['text']}'"
        )

    summary = (
        f"\n{len(results) - fails}/{len(results)} text elements passed "
        f"(iPhone {args.width}x{args.height}@{scale}x, worst-pixel sampling)."
    )
    report = "\n".join(results) + summary
    if args.out:
        with open(args.out, "w") as f:
            f.write(report + "\n")
    print(report)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
