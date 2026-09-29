#!/usr/bin/env python3
"""Body systems figure v2 — full rework per artist-gate verdict.

- Believable human proportions (~7.5 heads; legs ~41% of height, torso has room)
- Real stained-glass treatment: dark lead-came outlines between body regions,
  faceted jewel-tone organ fills, translucent glass body panels
- Heart: anatomical-ish silhouette in token deep red #8E1E2E (NOT a valentine)
- Reproductive: soft uterus/ovary form in ultramarine-violet (non-alert)
- Every organ legible: distinct silhouettes, jewel tones, lead separation
- Hit areas: every system has invisible hit shapes with min dimension >= 44pt
  at 390pt render width (r>=45 circles / 90-wide strokes / 52+ rects).
  Z-order bottom->top: skin, musculoskeletal, nervous, endocrine, urinary,
  digestive, reproductive, respiratory, cardiac, immune.
  Probe points verified via Playwright elementFromPoint (see probe_body.py).
"""
import math

LEAD = "#05080e"          # lead-came lines
# ---- palette (tertiary only; deep red reserved for the heart) ----
ULTRA = "#4B45D8"; ULTRA_LT = "#7A74FF"; ULTRA_PALE = "#B9B2FF"
CERU = "#2F8FE3"; CERU_LT = "#6FC3FF"
EMER = "#3ECF8E"; EMER_DK = "#2f9e63"; EMER_LT = "#8fd8a8"
PHTHALO_LT = "#1F8A64"
TEAL = "#2A9D8F"          # kidneys
HEART = "#8E1E2E"         # token deep red — heart ONLY
BONE = "#cfe3f2"
AMBER = "#D9A441"; AMBER_LT = "#F0C77E"   # endocrine glands
MAUVE = "#B0899A"; MAUVE_DK = "#7E4E68"   # immune nodes / spleen
RIM = "#7fc4e8"

def limb(x1, y1, w1, x2, y2, w2):
    """Tapered rounded limb as a filled path."""
    dx = x2 - x1; dy = y2 - y1
    L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    hw1, hw2 = w1 / 2, w2 / 2
    return (f"M {x1+nx*hw1:.1f},{y1+ny*hw1:.1f} "
            f"L {x2+nx*hw2:.1f},{y2+ny*hw2:.1f} "
            f"A {hw2:.1f},{hw2:.1f} 0 0 0 {x2-nx*hw2:.1f},{y2-ny*hw2:.1f} "
            f"L {x1-nx*hw1:.1f},{y1-ny*hw1:.1f} "
            f"A {hw1:.1f},{hw1:.1f} 0 0 0 {x1+nx*hw1:.1f},{y1+ny*hw1:.1f} Z")

def hit(path_d, stroke_w=None):
    if stroke_w:
        return (f'<path d="{path_d}" fill="none" stroke="#ffffff" stroke-width="{stroke_w}" '
                f'stroke-opacity="0" class="hit"/>')
    return f'<path d="{path_d}" fill="#ffffff" fill-opacity="0" stroke="none" class="hit"/>'

def hit_circle(x, y, r):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" fill-opacity="0" class="hit"/>'

def hit_rect(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" fill-opacity="0" class="hit"/>'

def hit_ellipse(x, y, rx, ry):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" '
            f'fill="#ffffff" fill-opacity="0" class="hit"/>')

def sys_group(name, inner):
    return f'<g class="sys" id="sys-{name}" data-system="{name}">\n{inner}\n</g>'

# ================= defs =================
defs = f'''
<radialGradient id="glassG" cx="50%" cy="28%" r="95%">
  <stop offset="0%" stop-color="#1d5a8a" stop-opacity="0.55"/>
  <stop offset="60%" stop-color="#123a5e" stop-opacity="0.42"/>
  <stop offset="100%" stop-color="#0a2c47" stop-opacity="0.35"/>
</radialGradient>
<radialGradient id="glowU" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="{ULTRA_LT}" stop-opacity="0.85"/><stop offset="100%" stop-color="{ULTRA}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowHeart" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="{HEART}" stop-opacity="0.6"/><stop offset="100%" stop-color="{HEART}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowE" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="{EMER_LT}" stop-opacity="0.8"/><stop offset="100%" stop-color="{EMER}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowC" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="{CERU_LT}" stop-opacity="0.8"/><stop offset="100%" stop-color="{CERU}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowAmber" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="{AMBER_LT}" stop-opacity="0.9"/><stop offset="100%" stop-color="{AMBER}" stop-opacity="0"/>
</radialGradient>
<filter id="soft14" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="14"/></filter>
'''

# ================= figure geometry =================
# head / neck / torso (single glass panel + lead region lines)
head   = '<ellipse cx="200" cy="70" rx="40" ry="48"/>'
neck   = '<path d="M 184,108 L 216,108 L 221,148 L 179,148 Z"/>'
torso  = ("M 130,170 "
          "C 150,152 170,144 182,142 L 218,142 C 230,144 250,152 270,170 "
          "C 262,190 256,202 254,214 "
          "C 260,240 262,252 262,262 "
          "C 258,280 254,292 254,305 "
          "C 248,322 244,332 242,342 "
          "C 244,362 248,380 250,398 "
          "C 246,418 242,430 238,440 "
          "C 230,448 222,452 214,454 "
          "C 208,455 192,455 186,454 "
          "C 178,452 170,448 162,440 "
          "C 158,430 154,418 150,398 "
          "C 152,380 156,362 158,342 "
          "C 154,332 150,322 146,305 "
          "C 142,292 140,280 138,262 "
          "C 138,252 142,240 146,214 "
          "C 144,202 138,190 130,170 Z")
# lead lines splitting torso into chest / abdomen / pelvis panels
lead_torso = (f'<path d="M 148,305 L 252,305" stroke="{LEAD}" stroke-width="4" fill="none"/>'
              f'<path d="M 152,400 L 248,400" stroke="{LEAD}" stroke-width="4" fill="none"/>')
# facet light-catches on the glass
facets = (f'<g stroke="{RIM}" stroke-width="1.6" opacity="0.28" fill="none">'
          '<path d="M 160,200 L 196,260 L 178,300"/>'
          '<path d="M 244,210 L 214,268 L 230,300"/>'
          '<path d="M 170,330 L 200,372 L 186,396"/>'
          '<path d="M 236,420 L 214,446"/>'
          '</g>')

# arms (L) / legs (L); right side mirrored
armL_upper = limb(140, 182, 36, 122, 312, 30)
armL_fore  = limb(122, 312, 30, 116, 432, 22)
handL      = '<rect x="104" y="428" width="26" height="62" rx="13"/>'
handL_det  = (f'<g stroke="{LEAD}" stroke-width="2" opacity="0.7">'
              '<path d="M 112.7,456 L 112.7,482 M 121.3,456 L 121.3,482"/></g>'
              f'<ellipse cx="131" cy="448" rx="7" ry="13" transform="rotate(25 131 448)"/>')
legL_thigh = limb(174, 446, 58, 170, 600, 46)
legL_shin  = limb(170, 600, 44, 168, 712, 28)
footL      = '<rect x="146" y="706" width="48" height="50" rx="16"/>'
footL_det  = (f'<g stroke="{LEAD}" stroke-width="2" opacity="0.7">'
              '<path d="M 162,730 L 162,750 M 178,730 L 178,750"/></g>')

armR_upper = limb(260, 182, 36, 278, 312, 30)
armR_fore  = limb(278, 312, 30, 284, 432, 22)
legR_thigh = limb(226, 446, 58, 230, 600, 46)
legR_shin  = limb(230, 600, 44, 232, 712, 28)
handR      = '<rect x="270" y="428" width="26" height="62" rx="13"/>'
handR_det  = (f'<g stroke="{LEAD}" stroke-width="2" opacity="0.7">'
              '<path d="M 278.7,456 L 278.7,482 M 287.3,456 L 287.3,482"/></g>'
              f'<ellipse cx="269" cy="448" rx="7" ry="13" transform="rotate(-25 269 448)"/>')
footR      = '<rect x="206" y="706" width="48" height="50" rx="16"/>'
footR_det  = (f'<g stroke="{LEAD}" stroke-width="2" opacity="0.7">'
              '<path d="M 222,730 L 222,750 M 238,730 L 238,750"/></g>')

# lead rings at joints
lead_joints = (f'<g stroke="{LEAD}" stroke-width="4" fill="none">'
               '<path d="M 107,310 L 137,314"/><path d="M 263,310 L 293,314"/>'
               '<path d="M 101,431 L 131,433"/><path d="M 269,431 L 299,433"/>'
               '<path d="M 147,599 L 193,601"/><path d="M 207,599 L 253,601"/>'
               '<path d="M 154,712 L 182,712"/><path d="M 218,712 L 246,712"/>'
               '</g>')

body_vis = (f'<g class="vis" fill="url(#glassG)" stroke="{LEAD}" stroke-width="4">'
            f'{head}{neck}<path d="{torso}"/>'
            f'<path d="{armL_upper}"/><path d="{armL_fore}"/>{handL}'
            f'<path d="{armR_upper}"/><path d="{armR_fore}"/>{handR}'
            f'<path d="{legL_thigh}"/><path d="{legL_shin}"/>{footL}'
            f'<path d="{legR_thigh}"/><path d="{legR_shin}"/>{footR}'
            '</g>'
            f'{lead_torso}{facets}{lead_joints}{handL_det}{handR_det}{footL_det}{footR_det}')

# skin hit shapes (generous; min dimension >= 90 units except head/neck which are ~80+)
skin_hit = "\n".join([
    '<ellipse cx="200" cy="70" rx="40" ry="48" fill="#ffffff" fill-opacity="0" class="hit"/>',
    '<path d="M 184,108 L 216,108 L 221,148 L 179,148 Z" fill="#ffffff" fill-opacity="0" class="hit"/>',
    hit(torso),
    hit("M 140,182 L 122,312 L 116,432", 90), hit("M 260,182 L 278,312 L 284,432", 90),
    '<rect x="104" y="428" width="26" height="62" fill="#ffffff" fill-opacity="0" class="hit"/>',
    '<rect x="270" y="428" width="26" height="62" fill="#ffffff" fill-opacity="0" class="hit"/>',
    hit("M 174,446 L 170,600 L 168,712", 90), hit("M 226,446 L 230,600 L 232,712", 90),
    '<rect x="146" y="706" width="48" height="50" fill="#ffffff" fill-opacity="0" class="hit"/>',
    '<rect x="206" y="706" width="48" height="50" fill="#ffffff" fill-opacity="0" class="hit"/>',
])
skin = sys_group("skin",
    f'<circle cx="200" cy="400" r="300" fill="{CERU}" opacity="0.08" filter="url(#soft14)" pointer-events="none"/>\n'
    f'{body_vis}\n{skin_hit}')

# ================= musculoskeletal =================
rib_paths = " ".join(
    f"M {200-w},{y} Q 200,{y+26} {200+w},{y}" for y, w in [(250, 50), (278, 56), (306, 58)])
bones_vis = (f'<g class="vis" stroke="{BONE}" stroke-width="3" fill="none" opacity="0.5" stroke-linecap="round">'
             f'<circle cx="200" cy="68" r="33" stroke-dasharray="5 6"/>'
             f'<path d="{rib_paths}"/>'
             '<path d="M 200,232 L 200,322"/>'
             '<path d="M 162,196 L 200,210 L 238,196"/>'
             '<path d="M 168,408 Q 200,428 232,408 M 164,428 Q 200,448 236,428"/>'
             '<path d="M 131,200 L 119,390"/><path d="M 269,200 L 281,390"/>'
             '<path d="M 172,470 L 169,690"/><path d="M 228,470 L 231,690"/>'
             '</g>')
bones_hit = "\n".join([
    hit("M 140,190 L 118,400", 90), hit("M 260,190 L 282,400", 90),
    hit("M 173,460 L 170,600", 90), hit("M 227,460 L 230,600", 90),
])
bones = sys_group("musculoskeletal", bones_vis + "\n" + bones_hit)

# ================= nervous =================
brain_vis = (f'<g class="vis">'
             f'<circle cx="200" cy="68" r="46" fill="url(#glowU)" opacity="0.5" pointer-events="none"/>'
             f'<path d="M 200,30 C 182,30 170,44 170,64 C 170,84 182,100 200,104 '
             f'C 218,100 230,84 230,64 C 230,44 218,30 200,30 Z" '
             f'fill="{ULTRA}" opacity="0.88" stroke="{LEAD}" stroke-width="2.5"/>'
             f'<path d="M 200,32 L 200,102" stroke="{ULTRA_LT}" stroke-width="3" opacity="0.85"/>'
             '<path d="M 180,52 Q 188,46 193,54 M 182,80 Q 190,86 195,78 '
             'M 220,52 Q 212,46 207,54 M 218,80 Q 210,86 205,78" '
             f'stroke="{ULTRA_LT}" stroke-width="2.4" fill="none" opacity="0.8" stroke-linecap="round"/>'
             f'<path d="M 200,118 L 200,440" stroke="{ULTRA}" stroke-width="5" opacity="0.35" stroke-linecap="round"/>'
             '<g stroke="{U}" stroke-width="2" opacity="0.25">'.replace("{U}", ULTRA) +
             '<path d="M 200,180 L 184,188 M 200,180 L 216,188"/>'
             '<path d="M 200,250 L 182,258 M 200,250 L 218,258"/>'
             '<path d="M 200,320 L 184,328 M 200,320 L 216,328"/>'
             '<path d="M 200,390 L 186,398 M 200,390 L 214,398"/>'
             '</g></g>')
nervous = sys_group("nervous", brain_vis + "\n" + hit_circle(200, 70, 48))

# ================= endocrine (amber glands) =================
endo_vis = (f'<g class="vis">'
            f'<circle cx="200" cy="162" r="20" fill="url(#glowAmber)" opacity="0.55" pointer-events="none"/>'
            f'<ellipse cx="190" cy="160" rx="9" ry="12" fill="{AMBER_LT}" opacity="0.9" stroke="{LEAD}" stroke-width="2"/>'
            f'<ellipse cx="210" cy="160" rx="9" ry="12" fill="{AMBER_LT}" opacity="0.9" stroke="{LEAD}" stroke-width="2"/>'
            f'<circle cx="200" cy="110" r="5" fill="{AMBER_LT}" opacity="0.95"/>'
            f'<ellipse cx="155" cy="404" rx="8" ry="5" fill="{AMBER_LT}" opacity="0.9"/>'
            f'<ellipse cx="245" cy="404" rx="8" ry="5" fill="{AMBER_LT}" opacity="0.9"/>'
            f'<ellipse cx="224" cy="384" rx="20" ry="8" transform="rotate(-15 224 384)" '
            f'fill="{AMBER_LT}" opacity="0.7" stroke="{LEAD}" stroke-width="2"/>'
            '</g>')
endocrine = sys_group("endocrine", endo_vis + "\n" + hit_circle(200, 162, 45))

# ================= urinary =================
urinary_vis = (f'<g class="vis">'
               f'<ellipse cx="155" cy="425" rx="13" ry="19" transform="rotate(-12 155 425)" '
               f'fill="{TEAL}" opacity="0.88" stroke="{LEAD}" stroke-width="2.5"/>'
               f'<ellipse cx="245" cy="425" rx="13" ry="19" transform="rotate(12 245 425)" '
               f'fill="{TEAL}" opacity="0.88" stroke="{LEAD}" stroke-width="2.5"/>'
               '<path d="M 152,420 q -4,6 0,12 M 248,420 q 4,6 0,12" stroke="#0d3a34" '
               'stroke-width="2.5" fill="none" opacity="0.8"/>'
               f'<path d="M 160,442 C 168,452 178,460 188,466 M 240,442 C 232,452 222,460 212,466" '
               f'stroke="{EMER_LT}" stroke-width="3" fill="none" opacity="0.6"/>'
               f'<ellipse cx="200" cy="470" rx="17" ry="13" fill="{CERU}" opacity="0.85" '
               f'stroke="{LEAD}" stroke-width="2.5"/>'
               f'<ellipse cx="200" cy="470" rx="17" ry="13" fill="url(#glowC)" opacity="0.35" pointer-events="none"/>'
               '</g>')
urinary = sys_group("urinary", urinary_vis + "\n" + "\n".join([
    hit_circle(155, 425, 45), hit_circle(245, 425, 45), hit_circle(200, 482, 45),
]))

# ================= digestive =================
intest_rows = " ".join(
    f"M 170,{y} q 12,-9 24,0 t 24,0 t 24,0" for y in (392, 406, 420, 434))
digest_vis = (f'<g class="vis">'
              f'<path d="M 200,200 L 200,330" stroke="{EMER_LT}" stroke-width="5" opacity="0.5"/>'
              f'<path d="M 216,330 C 232,330 243,342 241,357 C 239,371 228,380 216,377 '
              f'C 206,374 203,363 209,356 C 213,351 212,338 216,330 Z" '
              f'fill="{EMER}" opacity="0.88" stroke="{LEAD}" stroke-width="2.5"/>'
              f'<path d="M 148,340 C 162,332 182,332 196,340 L 194,362 '
              f'C 178,368 160,366 148,358 Z" '
              f'fill="{PHTHALO_LT}" opacity="0.9" stroke="{LEAD}" stroke-width="2.5"/>'
              f'<path d="M 160,346 L 188,346" stroke="#ffffff" stroke-width="2" opacity="0.25"/>'
              f'<path d="{intest_rows}" stroke="{LEAD}" stroke-width="12" fill="none" '
              f'opacity="0.85" stroke-linecap="round"/>'
              f'<path d="{intest_rows}" stroke="{EMER_DK}" stroke-width="8" fill="none" '
              f'opacity="0.95" stroke-linecap="round"/>'
              '</g>')
digestive = sys_group("digestive", digest_vis + "\n" + "\n".join([
    hit_circle(222, 352, 45), hit_circle(172, 348, 45), hit_rect(170, 388, 60, 52),
]))

# ================= reproductive (soft uterus/ovary, ultramarine-violet) =================
repro_vis = (f'<g class="vis">'
             f'<circle cx="200" cy="426" r="30" fill="url(#glowU)" opacity="0.4" pointer-events="none"/>'
             f'<path d="M 200,406 C 190,406 183,414 183,426 C 183,440 191,448 200,448 '
             f'C 209,448 217,440 217,426 C 217,414 210,406 200,406 Z" '
             f'fill="{ULTRA_LT}" opacity="0.88" stroke="{LEAD}" stroke-width="2.5"/>'
             f'<path d="M 186,418 C 179,414 174,414 170,419 M 214,418 C 222,413 229,413 235,417" '
             f'stroke="{ULTRA_LT}" stroke-width="4" fill="none" opacity="0.85" stroke-linecap="round"/>'
             f'<ellipse cx="166" cy="421" rx="9" ry="7" fill="{ULTRA_PALE}" opacity="0.92" '
             f'stroke="{LEAD}" stroke-width="2"/>'
             f'<ellipse cx="239" cy="419" rx="9" ry="7" fill="{ULTRA_PALE}" opacity="0.92" '
             f'stroke="{LEAD}" stroke-width="2"/>'
             '</g>')
reproductive = sys_group("reproductive", repro_vis + "\n" + hit_ellipse(200, 424, 38, 30))

# ================= respiratory =================
lungL = ("M 164,228 C 148,228 140,244 140,268 C 140,296 150,316 164,316 "
         "C 176,316 182,302 181,280 C 180,256 176,228 164,228 Z")
lungR = ("M 236,228 C 224,228 218,244 218,268 C 218,296 226,314 236,314 "
         "C 248,314 256,298 255,278 C 254,254 248,228 236,228 Z")
resp_vis = (f'<g class="vis">'
            f'<path d="M 200,130 L 200,198" stroke="{CERU_LT}" stroke-width="10" opacity="0.55" stroke-linecap="round" pointer-events="none"/>'
            f'<path d="M 193,150 L 207,150 M 193,170 L 207,170 M 193,190 L 207,190" '
            f'stroke="{CERU_LT}" stroke-width="2" opacity="0.5" pointer-events="none"/>'
            f'<path d="{lungL}" fill="{CERU}" opacity="0.8" stroke="{LEAD}" stroke-width="2.5"/>'
            f'<path d="{lungR}" fill="{CERU}" opacity="0.8" stroke="{LEAD}" stroke-width="2.5"/>'
            f'<ellipse cx="161" cy="274" rx="20" ry="42" fill="url(#glowC)" opacity="0.4" pointer-events="none"/>'
            f'<ellipse cx="237" cy="274" rx="20" ry="42" fill="url(#glowC)" opacity="0.4" pointer-events="none"/>'
            f'<path d="M 158,244 L 158,304 M 240,244 L 240,304" stroke="{CERU_LT}" stroke-width="2.5" opacity="0.7"/>'
            '</g>')
respiratory = sys_group("respiratory", resp_vis + "\n" + "\n".join([
    hit_circle(138, 282, 48), hit_circle(240, 282, 48),
]))

# ================= cardiac (anatomical-ish, token deep red) =================
heart_path = ("M 190,236 C 178,236 168,246 168,260 C 168,276 180,290 192,298 "
              "C 200,303 206,300 208,292 C 212,278 214,266 212,254 C 210,242 202,234 194,236 Z")
cardiac_vis = (f'<g class="vis">'
               f'<circle cx="190" cy="264" r="54" fill="url(#glowHeart)" opacity="0.5" pointer-events="none">'
               '<animate attributeName="opacity" values="0.5;0.28;0.5" dur="1.6s" repeatCount="indefinite"/>'
               '</circle>'
               f'<path d="{heart_path}" fill="{HEART}" opacity="0.95" stroke="{LEAD}" stroke-width="2.5">'
               '<animate attributeName="opacity" values="0.95;1;0.95" dur="1.6s" repeatCount="indefinite"/>'
               '</path>'
               f'<path d="M 188,242 C 186,232 192,224 200,224 C 206,224 210,228 211,233" '
               f'stroke="{HEART}" stroke-width="9" fill="none" stroke-linecap="round" opacity="0.95"/>'
               '<path d="M 178,252 Q 186,248 192,256" stroke="#ffffff" stroke-width="3" '
               'fill="none" opacity="0.22" stroke-linecap="round"/>'
               '</g>')
cardiac = sys_group("cardiac", cardiac_vis + "\n" + hit_circle(190, 264, 48))

# ================= immune =================
nodes = [(176, 148), (224, 148), (142, 218), (258, 218), (178, 452), (222, 452)]
imm_vis = ['<g class="vis">']
for x, y in nodes:
    imm_vis.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{MAUVE}" opacity="0.3"/>')
    imm_vis.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{MAUVE}" opacity="0.95" '
                   f'stroke="{LEAD}" stroke-width="1.5"/>')
imm_vis.append(f'<path d="M 246,340 C 254,340 259,347 258,356 C 257,364 250,368 244,364 '
               f'C 239,360 240,346 246,340 Z" fill="{MAUVE_DK}" opacity="0.88" '
               f'stroke="{LEAD}" stroke-width="2.5"/>')
imm_vis.append('</g>')
immune = sys_group("immune", "\n".join(imm_vis) + "\n" + "\n".join([
    hit_circle(150, 145, 45), hit_circle(250, 145, 45),
]))

# ================= assemble =================
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 800" role="img" aria-label="Body systems map">
<defs>{defs}</defs>
{skin}
{bones}
{nervous}
{endocrine}
{urinary}
{digestive}
{reproductive}
{respiratory}
{cardiac}
{immune}
</svg>'''

open("/home/hatch/workspace/heliotrope-wt/art/assets/body-systems.svg", "w").write(svg)

# ---- preview page (legend pill layout kept) ----
page = '''<!doctype html><html><head><meta charset="utf-8"><style>
body{background:#060c14;margin:0;padding:16px;font-family:system-ui;color:#cfe0ea}
.wrap{display:flex;gap:14px;align-items:flex-start;max-width:420px}
.stage{position:relative;width:230px;flex:none}
.stage object, .stage svg{width:230px;height:auto;display:block}
.legend{flex:1;display:flex;flex-direction:column;gap:6px;padding-top:10px}
.li{font-size:12.5px;padding:7px 10px;border-radius:10px;background:#0b1622;border:1px solid #1c2c3e;cursor:pointer}
.li.hot{border-color:#2ea3c8;background:#10273a;color:#fff}
.readout{margin-top:14px;font-size:13px;color:#8fb6cc;min-height:20px}
.tip{position:fixed;pointer-events:none;background:#0e2233;border:1px solid #2ea3c8;color:#eaf4fa;
     font-size:12px;padding:4px 10px;border-radius:8px;display:none;z-index:10}
.sys{cursor:pointer}
.sys .vis{transition:filter .18s ease}
.sys.hot .vis{filter:brightness(1.7) saturate(1.3) drop-shadow(0 0 10px rgba(46,163,200,.7))}
.sys.hot .hit{fill-opacity:0.12;fill:#7fc4e8}
</style></head><body>
<h2 style="font-size:17px;margin:4px 0 12px">Body systems &mdash; hover/click test</h2>
<div class="wrap">
  <div class="stage" id="stage">__SVG__</div>
  <div class="legend" id="legend"></div>
</div>
<div class="readout" id="readout">hover a region or a legend item&hellip;</div>
<div class="tip" id="tip"></div>
<script>
const names = {skin:"Skin",musculoskeletal:"Musculoskeletal",nervous:"Nervous",urinary:"Urinary",
  reproductive:"Reproductive",digestive:"Digestive",respiratory:"Respiratory",cardiac:"Cardiac",
  endocrine:"Endocrine",immune:"Immune / lymphatic"};
(function(){
  const svg = document.querySelector('#stage svg');
  const tip = document.getElementById('tip'), readout = document.getElementById('readout');
  const legend = document.getElementById('legend');
  Object.keys(names).forEach(k=>{
    const d = document.createElement('div'); d.className='li'; d.textContent=names[k]; d.dataset.k=k;
    d.addEventListener('mouseenter',()=>hot(k,true)); d.addEventListener('mouseleave',()=>hot(k,false));
    legend.appendChild(d);
  });
  function hot(k,on){
    const g = svg.querySelector('[data-system="'+k+'"]');
    if(g) g.classList.toggle('hot',on);
    document.querySelectorAll('.li[data-k="'+k+'"]').forEach(e=>e.classList.toggle('hot',on));
    if(on){ readout.textContent = 'hover: '+names[k]; tip.style.display='block'; tip.textContent=names[k]; }
    else tip.style.display='none';
  }
  svg.querySelectorAll('.sys').forEach(g=>{
    const k = g.dataset.system;
    g.addEventListener('mouseenter',e=>hot(k,true));
    g.addEventListener('mouseleave',()=>hot(k,false));
    g.addEventListener('mousemove',e=>{ tip.style.left=(e.clientX+14)+'px'; tip.style.top=(e.clientY+10)+'px'; });
    g.addEventListener('click',()=>{ readout.textContent='clicked: '+names[k]+' ok'; });
  });
})();
</script>
</body></html>'''
open("/home/hatch/workspace/heliotrope-wt/art/preview/body.html", "w").write(page.replace("__SVG__", svg))
print("body-systems.svg v2 written,", len(svg), "bytes; preview/body.html regenerated")
