#!/usr/bin/env python3
"""Heliotrope app icon v2 — rework per artist-gate verdict.

- The ULTRAMARINE BLOSSOM leads (app is HELIOTROPE): cluster spans ~38% of
  tile width, centered low, with a soft ultramarine aura behind it.
- Sun deepened toward oxblood #8E1E2E, shrunk (~24% of tile), glow softened —
  no longer the loudest element, no near-primary red-orange.
- Stem thickened (34px) so it survives small sizes; petal detail simplified
  into fewer, larger blossoms.
- Kept: Pleiades cluster, star field, dark-blue void base.
"""
import math, random

random.seed(7)
S = 1024
cx = S / 2

# ---- palette (tertiary only) ----
PRUSSIAN   = "#0a2c47"
NAVY_DEEP  = "#041322"
ULTRAMARINE= "#3b2fc4"
ULTRA_LT   = "#7a6cf0"
CERULEAN   = "#2ea3c8"
PHThALO_G  = "#14532d"
EMERALD    = "#2f9e63"
OXBLOOD    = "#8E1E2E"   # deepened sun — token deep red family
OXBLOOD_DK = "#5e1420"
EMBER      = "#D9A441"

def star_dots(n, x0, y0, x1, y1, rmin=1, rmax=3, op=0.5):
    out = []
    for _ in range(n):
        x = random.uniform(x0, x1); y = random.uniform(y0, y1)
        r = random.uniform(rmin, rmax); o = round(random.uniform(0.15, op), 2)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#bfe3f2" opacity="{o}"/>')
    return "\n".join(out)

def blossom(x, y, r, rot=0):
    """5-petal heliotrope blossom — larger, simpler petals."""
    p = []
    for i in range(5):
        a = math.radians(rot + i * 72)
        px = x + math.cos(a) * r * 0.60; py = y + math.sin(a) * r * 0.60
        p.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{r*0.55:.1f}" ry="{r*0.36:.1f}" '
                 f'fill="url(#petalG)" transform="rotate({rot+i*72:.0f} {px:.1f} {py:.1f})" opacity="0.96"/>')
    c = (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*0.24:.1f}" fill="{CERULEAN}"/>'
         f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*0.12:.1f}" fill="#eaf7fd"/>')
    return "\n".join(p) + c

# stem: thick curve rising from bottom into the blossom cluster
stem = ("M 430 1024 C 440 900, 460 800, 500 730 "
        "C 520 695, 540 675, 560 665")
# blossom cluster: spans x ~330-725 (~38% of tile), centered (527, 630)
blooms = [(395, 620, 60, 12), (465, 575, 68, 42), (545, 568, 70, 75),
          (620, 592, 66, 20), (672, 645, 58, 55), (610, 700, 58, 8),
          (515, 705, 62, 60), (435, 682, 56, 30)]
# leaves along the stem
leaf1 = "M 452 880 C 380 870, 320 830, 300 760 C 380 770, 440 815, 452 880 Z"
leaf2 = "M 478 800 C 545 855, 605 915, 690 945 C 625 865, 560 815, 478 800 Z"
leaf3 = "M 520 720 C 470 700, 420 700, 380 720 C 430 740, 480 740, 520 720 Z"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}">
<defs>
<radialGradient id="bgG" cx="50%" cy="42%" r="75%">
  <stop offset="0%" stop-color="#10405f"/>
  <stop offset="45%" stop-color="{PRUSSIAN}"/>
  <stop offset="100%" stop-color="{NAVY_DEEP}"/>
</radialGradient>
<radialGradient id="sunG" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="{OXBLOOD}"/>
  <stop offset="55%" stop-color="{OXBLOOD_DK}"/>
  <stop offset="100%" stop-color="{OXBLOOD_DK}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="auraU" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="{ULTRA_LT}" stop-opacity="0.55"/>
  <stop offset="100%" stop-color="{ULTRAMARINE}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="petalG" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="{ULTRA_LT}"/>
  <stop offset="55%" stop-color="{ULTRAMARINE}"/>
  <stop offset="100%" stop-color="#241d86"/>
</linearGradient>
<linearGradient id="leafG" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="{EMERALD}"/>
  <stop offset="100%" stop-color="{PHThALO_G}"/>
</linearGradient>
<clipPath id="clip"><rect x="0" y="0" width="{S}" height="{S}" rx="235"/></clipPath>
</defs>
<rect x="0" y="0" width="{S}" height="{S}" rx="235" fill="url(#bgG)"/>
<g clip-path="url(#clip)">
{star_dots(46, 40, 40, 984, 700)}
<!-- Pleiades cluster, top-right -->
<g fill="#cfeafb">
<circle cx="830" cy="120" r="5"/><circle cx="862" cy="104" r="4"/>
<circle cx="890" cy="126" r="5.5"/><circle cx="872" cy="152" r="3.5"/>
<circle cx="838" cy="158" r="4"/><circle cx="905" cy="162" r="3"/>
<circle cx="815" cy="96" r="3"/>
</g>
<!-- sun: smaller, oxblood, softened -->
<circle cx="{cx:.0f}" cy="400" r="250" fill="url(#sunG)" opacity="0.8"/>
<circle cx="{cx:.0f}" cy="400" r="150" fill="{OXBLOOD}"/>
<circle cx="{cx:.0f}" cy="400" r="150" fill="url(#sunG)" opacity="0.85"/>
<!-- faint ember rays -->
<g stroke="{EMBER}" stroke-width="8" opacity="0.16" stroke-linecap="round">
{''.join(f'<line x1="{cx+math.cos(math.radians(a))*172:.0f}" y1="{400+math.sin(math.radians(a))*172:.0f}" x2="{cx+math.cos(math.radians(a))*205:.0f}" y2="{400+math.sin(math.radians(a))*205:.0f}"/>' for a in range(0,360,45))}
</g>
<!-- ultramarine aura: the blossom leads -->
<circle cx="527" cy="630" r="230" fill="url(#auraU)" opacity="0.5"/>
<!-- leaves behind stem -->
<path d="{leaf1}" fill="url(#leafG)" opacity="0.95"/>
<path d="{leaf2}" fill="url(#leafG)" opacity="0.85"/>
<path d="{leaf3}" fill="url(#leafG)" opacity="0.9"/>
<!-- stem: thickened -->
<path d="{stem}" fill="none" stroke="{EMERALD}" stroke-width="34" stroke-linecap="round"/>
<path d="{stem}" fill="none" stroke="#0c2f1c" stroke-width="34" stroke-linecap="round" opacity="0.25" transform="translate(7,7)"/>
<!-- blossom cluster (~38% of tile) -->
{''.join(blossom(x,y,r,rot) for x,y,r,rot in blooms)}
</g>
<rect x="0" y="0" width="{S}" height="{S}" rx="235" fill="none" stroke="#ffffff" stroke-opacity="0.08" stroke-width="4"/>
</svg>'''

open("/home/hatch/workspace/heliotrope-wt/art/assets/icon.svg", "w").write(svg)
print("wrote icon.svg v2")
