# Heliotrope Design Tokens

Phase 1 UI/UX research deliverable. Everything here is grounded in her
aesthetic source of truth (`~/memory/personality/things-i-like.md`):
tertiary palette only, dark blue + shimmer base, sun-through-leaves light,
glows, camera flares, stained-glass translucency, subtle rainbows,
gradients, gentle motion. Dense but calm — maximum relevant info per
screen, minimal scrolling, never overwhelming.

These are tokens, not components. The app team consumes them as CSS
custom properties in `apps/web` (or CSS-in-JS equivalents).

---

## 1. Color — tertiary only

Rule #1 from her list: **HATE primary colors.** No pure red/blue/yellow
anywhere. Everything below sits in the tertiary family (a primary plus a
secondary, or mixed beyond recognition).

### Surfaces (deep dark blue base)

| Token | Hex | Usage |
|---|---|---|
| `--heli-void` | `#020A16` | App background, page base |
| `--heli-deep` | `#071731` | Card base / default card fill |
| `--heli-slab` | `#0D2242` | Raised slabs (tables, log lists, dense content) |
| `--heli-glass` | `rgba(24, 52, 96, 0.45)` | Glass surfaces (nav rail, sheets, toolbars) |
| `--heli-border` | `rgba(130, 185, 255, 0.16)` | Hairline borders on cards and glass |
| `--heli-border-strong` | `rgba(130, 185, 255, 0.30)` | Active/selected outlines, focus rings |

- Glass gets `backdrop-filter: blur(20px) saturate(1.4)` plus a faint top
  specular highlight: `inset 0 1px 0 rgba(255,255,255,0.10)` — the
  stained-glass translucency she likes.
- Dense data surfaces (lab tables, med logs) stay matte and opaque for
  crispness; glass is reserved for chrome (nav, sheets, modals).

### Accents

| Token | Hex | Where it lives |
|---|---|---|
| `--heli-ultramarine` | `#4B45D8` | Brand accent, primary actions, active nav |
| `--heli-ultramarine-glow` | `#7A74FF` | Hover/lit state of ultramarine, chart highlights |
| `--heli-cerulean` | `#2F8FE3` | Water/hydration, sleep, info, secondary actions |
| `--heli-cerulean-glow` | `#6FC3FF` | Lit state |
| `--heli-phthalo-blue` | `#0A1B8A` | Deep background washes, gradient anchors |
| `--heli-phthalo-green` | `#123A2E` | Deep background washes for nourish/nature |
| `--heli-phthalo-green-lit` | `#1F8A64` | Growth/good trend accents |
| `--heli-prussian` | `#062B4A` | Secondary surface tint, pressed states |
| `--heli-emerald` | `#3ECF8E` | Positive/restorative signal: taken, in-range, improving |
| `--heli-deepred` | `#8E1E2E` | Deep red accent (cycle, spice, warmth motifs) |
| `--heli-deepred-lit` | `#D6506B` | Genuine alerts and warnings |
| `--heli-ember` | `#D9A441` | Fireflies/candlelight accent; amber-adjacent but tertiary |
| `--heli-ember-soft` | `#F0C77E` | Lit state; gentle, never garish |

Guidance:
- **Ultramarine** is the app's signature. One brand accent, used
  sparingly — CTAs, active states, key chart lines.
- **Emerald** = good news (med taken, lab in range, streak alive).
- **Deep red lit** = genuine alerts only (missed critical med, lab out of
  range). Never used decoratively, per the healthcare rule: if red is
  wallpaper, real alerts stop registering.
- **Ember** is the warmth accent (streaks, celebrations, gentle nudges) —
  her candlelight/firefly motif.
- Colors always pair with a label or icon. **Never convey meaning by
  color alone** (4.5:1 rule + colorblind safety).

### Text

| Token | Hex | Contrast on `--heli-void` |
|---|---|---|
| `--heli-ink` | `#EDF3FC` | ~16:1, primary text |
| `--heli-ink-dim` | `#A9BDD8` | ~8:1, secondary text |
| `--heli-ink-faint` | `#6E85A3` | ~4.7:1, captions only — never small-body copy |

### Rainbow (soft, dull — never garish)

Her line: "soft or dull rainbows (subtle, never garish)."

| Token | Value |
|---|---|
| `--heli-rainbow` | `linear-gradient(135deg, #4B45D8, #2F8FE3, #1F8A64, #D9A441, #8E1E2E)` |
| `--heli-rainbow-dull` | same stops at 55% saturation / 45% opacity over `--heli-deep` |

Usage: data-series sequences on charts, decorative bands, streak
gradients, the aurora treatment on hero surfaces. Never on body text,
never full-strength in daylight UI, never more than a band at a time.

---

## 2. Typography

iPhone-first web app: use the system stack so it reads native on iOS.

- **Font stack:** `-apple-system, BlinkMacSystemFont, "SF Pro Text",
  "SF Pro Display", "Helvetica Neue", sans-serif`
- **Numerals:** `font-feature-settings: "tnum"` on every metric — tabular
  figures are the difference between a dashboard and a ransom note.
- **Scale** (iPhone 390pt reference):

| Token | Size / weight | Usage |
|---|---|---|
| `--type-hero` | 34 / 700 | Big answer of the day (Today tab: "One Big Thing") |
| `--type-title` | 28 / 700 | Screen titles |
| `--type-head` | 22 / 650 | Card titles — always larger than any subtext |
| `--type-body` | 17 / 400 | Body copy, minimum size for paragraphs |
| `--type-sub` | 15 / 500 | Row labels — must fit on ONE line, no wrapping |
| `--type-caption` | 13 / 400 | Captions, timestamps |
| `--type-tiny` | 11 / 600, uppercase, +0.08em | Eyebrow labels, section headers |

- Rule from her sleep-tracker: headers always larger than all subtext;
  row labels one line, no wrap (truncate with ellipsis instead).

---

## 3. Spacing, radii, targets

- **Base unit 4pt.** Gutters: 16px screen, 12px card padding, 8px stack
  gaps, 4px tight pairs.
- **Radii:** cards `--r-lg: 16px`; nested/sub cards `--r-md: 12px`;
  hero/featured `--r-xl: 20px`; pills `--r-full: 999px`.
- **Touch targets:** minimum 44×44pt (Apple HIG). Med-check circles,
  body-map hotspots, tab bar — all 44pt+.
- **Density:** dense but calm. Cards group 2–4 facts; dividers are
  hairlines (`--heli-border`); section headers act as anchors. When a tab
  holds 10+ rows, use the Oura lesson: one glanceable answer up top,
  drill-down below.

---

## 4. Light, glow, shadow

Her signature. The rule: **light effects are atmosphere, not data.**
Glow marks the *important* thing; matte surfaces carry the *dense* thing.

| Effect | Value |
|---|---|
| Card rest | `0 2px 12px rgba(2, 10, 22, 0.5)` |
| Card lift (hover/press-out) | `0 8px 28px rgba(2, 10, 22, 0.55)` |
| Brand glow (ultramarine CTA) | `0 0 24px rgba(75, 69, 216, 0.40)` |
| Emerald glow (positive) | `0 0 20px rgba(62, 207, 142, 0.30)` |
| Deep-red glow (alert) | `0 0 20px rgba(214, 80, 107, 0.35)` |
| Text glow (hero numbers) | `0 0 32px rgba(111, 195, 255, 0.45)` |
| Chart line glow | SVG/CSS `drop-shadow(0 0 6px currentColor)` on the series path |

- **Sun-through-leaves:** hero/atmosphere layers use layered radial
  gradients (emerald→transparent, cerulean→transparent) at low opacity
  over the void — dappled, never a flat wash.
- **Shimmer:** skeleton loaders and the void background get a slow
  `linear-gradient` sheen sweep (see Motion). No spinners when the
  structure is known — skeletons only.
- **Camera flare:** reserved for delight moments only (streak milestones,
  report completed) — a brief diagonal streak, then gone.

---

## 5. Motion — everything gently alive

She listed gradients, animations, and movement as three separate likes.
The register: **gentle, liquid, never bouncy.**

| Token | Value | Usage |
|---|---|---|
| `--ease-out` | `cubic-bezier(0.22, 1, 0.36, 1)` | Default for all transitions |
| `--dur-instant` | `120ms` | Pressed-state scale (down to `0.97`) |
| `--dur-fast` | `200ms` | Hover, chips, tab switches |
| `--dur-med` | `400ms` | Card entrances, sheet slides |
| `--dur-stagger` | `70ms` | Between siblings on list entrance |
| `--dur-float` | `7s ease-in-out infinite` | Ambient float on hero orbs / firefly dots |
| `--dur-aurora` | `18s ease-in-out infinite alternate` | Slow gradient drift on atmosphere layers |
| `--dur-shimmer` | `2.4s linear infinite` | Skeleton sheen |
| `--dur-chart-draw` | `800ms var(--ease-out)` | Line/bar draw **once on mount only** — never re-animate on refresh |

Rules:
- No bounce, no spring, no playful overshoot.
- Entrance: `fade + translateY(8px)`, staggered 70ms per child.
- Ambient loops (float, aurora, shimmer) pause under
  `prefers-reduced-motion`; chart-draw becomes instant.
- Warnings/alerts never blink or pulse repeatedly — a static glow,
  not a strobe.

---

## 6. Charts (her signature surface)

She thinks in distributional summaries, not averages (sleep-tracker
rule: duration pills tinted by IQR position; date squares colored by
month).

- **Line:** 2.5px, round caps/joins, series color from accent set,
  gradient area fill `color 32% → 0%`, `drop-shadow(0 0 6px)` line glow.
- **Bars:** radius 4px tops, gradient fill along the tertiary axis;
  distribution bars tint by IQR position (longer bluer, shorter redder)
  — keep the sleep-tracker convention across the suite.
- **Donut/rings:** 10px track, gradient stroke, rounded caps; ring
  segments for meds adherence, sleep stages, macro split.
- **Sparklines:** 36px tall, inside stat tiles — big number + delta badge
  + sparkline, the Stripe-dashboard pattern she liked.
- Every chart: clear title, unit, and threshold labels when thresholds
  matter (her lab lines need reference ranges drawn, not described).
- Range selector: pill control (W / M / 3M / 6M / 1Y / ALL).
- Long ranges downsample for rendering, keep full resolution for stats.

---

## 7. Navigation pattern (recommendation from research)

She sketched 11 tabs. Research says: Oura cut 5 tabs to 3 and put a
"One Big Thing" on top; Apple CareKit puts tasks and charts on one
screen. Recommendation for the app team:

- **Bottom tab bar:** Today, Body, Meds, Mind, More — 44pt targets,
  ultramarine active glow, SF Symbol-style glyphs.
- **More:** Labs, Care team, To-dos, Nourish, Cycle, Orders, Reports —
  a grouped list, each row one line, no wrap.
- Glass nav bar (`--heli-glass`) floating over content, 16px side inset.
- Every screen: one glanceable answer at top, progressive disclosure
  below.

---

## 8. Dark-background contrast notes

- All body text hits WCAG AA 4.5:1 on `--heli-void` (see table §1).
- `deepred-lit` (#D6506B) text on void ≈ 5.2:1 — safe for alert copy.
- `ember` (#D9A441) text on void ≈ 8:1 — safe for captions.
- `ultramarine` (#4B45D8) on void ≈ 3.4:1 — **not safe for text**; use
  for large glyphs, rings, backgrounds, and buttons with white text
  (white on #4B45D8 ≈ 6.8:1, safe).
- Translucency layers never drop effective contrast below 4.5:1 —
  test glass cards with the shimmer/atmosphere behind them, not on
  flat color.
- True black (`#000`) avoided: pure black crushes the shimmer and reads
  cheap against her glows; `#020A16` keeps depth.

---

*Tokens derived 2026-09-29. Season lightly: pick 2–3 motifs per surface
(sun-through-leaves, stained glass, fireflies, Pleiades stars, aurora,
subtle rainbow) — never all at once.*
