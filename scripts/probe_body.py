#!/usr/bin/env python3
"""Playwright elementFromPoint probe: verifies every body-system hit area.

Loads preview/body.html, maps SVG coords to page coords via the svg's
bounding box, and asserts document.elementFromPoint resolves to the
expected data-system for each probe point.
"""
from playwright.sync_api import sync_playwright

PROBES = {
    "skin":             [(185, 665), (108, 470)],
    "musculoskeletal":  [(110, 340), (171, 530)],
    "nervous":          [(200, 70)],
    "endocrine":        [(200, 162)],
    "urinary":          [(155, 425), (200, 482)],
    "digestive":        [(222, 352), (172, 348), (180, 398)],
    "reproductive":     [(200, 418)],
    "respiratory":      [(138, 282), (240, 282)],
    "cardiac":          [(190, 264)],
    "immune":           [(176, 150), (224, 150)],
}

HTML = "file:///home/hatch/workspace/heliotrope-wt/art/preview/body.html"

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/meta-chromium/chrome",
                          args=["--no-sandbox", "--disable-dev-shm-usage"])
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(HTML)
    pg.wait_for_timeout(800)
    box = pg.evaluate("""() => {
        const r = document.querySelector('#stage svg').getBoundingClientRect();
        return {x: r.x, y: r.y, w: r.width, h: r.height};
    }""")
    fails = 0
    for system, pts in PROBES.items():
        for sx, sy in pts:
            px = box["x"] + (sx / 400) * box["w"]
            py = box["y"] + (sy / 800) * box["h"]
            got = pg.evaluate(
                """([x, y]) => {
                    const el = document.elementFromPoint(x, y);
                    const g = el && el.closest ? el.closest('.sys') : null;
                    return g ? g.dataset.system : (el ? el.tagName : 'null');
                }""", [px, py])
            ok = got == system
            fails += not ok
            print(f"{'PASS' if ok else 'FAIL'}  ({sx},{sy}) -> {got}  (expected {system})")
    b.close()

print("ALL PASS" if fails == 0 else f"{fails} FAILURES")
raise SystemExit(1 if fails else 0)
