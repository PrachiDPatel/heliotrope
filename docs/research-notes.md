# Research Notes — Phase 1

What I studied before writing `design-tokens.md`, and what I took from
each. All sources are public; no logins used. (Note: as a subagent I
can search and fetch page text, not operate a live browser — none of
this claims a hands-on website visit.)

## A. Healthcare app design guidance (2026)

- **ComfyGen healthcare app design roundup (2026):** blues and greens
  dominate as calm/clinical; keep red exclusively for genuine alerts
  because using it as a brand accent means real alerts stop
  registering; 4.5:1 contrast, 44pt minimum touch targets, never use
  color alone to convey meaning. Gamification is fine for wellness but
  trivializes chronic/mental health — match the register to the
  context. Adapted into token usage rules: deep-red-lit reserved for
  alerts, ember for warmth, never color-alone signaling.
  Source: https://www.comfygen.com/blog/healthcare-app-design/

- **Apple CareKit HIG patterns:** task views with header + stacked
  content subviews, circular checkmark buttons for med intake at
  different times of day, charts comparing symptoms (e.g. nausea)
  against medication intake, contacts with phone/message/email/map.
  Taken: the med-task card shape, symptom-vs-med correlation charts
  (became feature idea #6), Care-team one-tap contacts.
  Source: Apple HIG CareKit references.

- **Apple HealthKit editorial rules:** refer to it as "Apple Health,"
  never "HealthKit," in user copy; don't mimic Apple imagery. Taken:
  naming discipline for any import/integration surface.

- **mbombeck/healthlog (PWA) UI guidelines:** Dracula-themed,
  semantic tokens for chrome vs `--dracula-*` tokens for dataviz only,
  dark mode default. Taken: the chrome/viz token split (our tokens do
  the same), and the habit of a single-source-of-truth doc like this
  one. Source: https://github.com/mbombeck/healthlog/blob/HEAD/docs/ui-guidelines.md

- **healthlog-ios CHANGELOG patterns:** skeleton loaders instead of
  spinners, single-settle rendering (no re-flashing), LTTB downsampling
  for long charts, uniform sheet detents. Taken: shimmer skeletons,
  draw-once chart rule, downsampling note.
  Source: https://github.com/mbombeck/healthlog-ios/blob/HEAD/CHANGELOG.md

## B. Artsy dataviz and dashboard design

- **second-brain dataviz-design skill teardowns:** Bloomberg Terminal
  (extreme density, color as a second axis), TradingView
  (interaction on the canvas), Stripe Dashboard (stat tile: big number
  + delta badge + sparkline, immaculate right-aligned tabular
  tables), Mercury ("calm finance" — density with breathing room),
  Linear/Arc/Raycast (craft-level motion). Taken: the stat-tile
  pattern for chart cards, tabular numerals everywhere, density with
  breathing room as the UX north star.
  Source: https://github.com/sircharan/second-brain/blob/HEAD/starter-pack/skills/dataviz-design/SKILL.md

- **moonmind DashboardDesignSystem:** strict surface hierarchy —
  Atmosphere (ambient gradients, star/noise texture) → matte data
  slabs for dense content → satin forms → glass controls →
  accent/live surfaces used sparingly. "Controlled neon energy, never
  used as a page-wide base." Taken almost wholesale: our atmosphere /
  matte slab / glass control split, and the rule that glow marks the
  important thing while dense content stays matte.
  Source: https://github.com/moonladderstudios/moonmind/blob/HEAD/docs/UI/DashboardDesignSystem.md

- **aidj dashboard prompt patterns:** glass cards with backdrop blur,
  floating glow orbs with 8–10s float loops, gradient text, mood cards
  with per-mood gradients (chill cyan→blue, focus emerald→teal),
  staggered 100ms fade-up entrances, shimmer loading. Taken:
  atmosphere orbs, float durations, stagger pattern, mood-gradient
  language — but slowed and softened to her "gentle" register.
  Source: https://github.com/lolimmlost/aidj/blob/HEAD/docs/LOVABLE_DASHBOARD_PROMPT.md

- **horizon-project visual do-nots:** don't animate line drawing on
  every refresh, don't omit units or threshold labels, don't use
  loading spinners when skeleton structure is known, don't bounce,
  respect reduced motion. Taken as chart/motion rules.
  Source: https://github.com/anhkhoa1804/horizon-project/blob/HEAD/docs/VISUAL_DO_NOTS.md

## C. Real health apps she overlaps with

- **Oura (2025 redesign):** cut from five tabs to three (Today,
  Vitals, My Health); "One Big Thing" per day; parts of the app
  change color with biometrics for at-a-glance status; glanceable
  Circles for readiness/sleep/activity; Cycle Insights moved to a
  12-month window with predictions from a single night. Taken: the
  One Big Thing concept (feature idea #1), 12-month cycle view
  (idea #7), and the lesson that 11 tabs need a primary/More split.
  Source: https://9to5google.com/2025/10/20/oura-app-redesign/

- **Whoop/NOOP community docs:** honest-data invariant (never show a
  number you didn't measure; estimates carry marks), recovery scoring
  from HRV + resting HR + sleep composite, strain vs recovery
  framing. Taken: body battery concept (idea #2) and the honest-data
  rule for any computed score.
  Source: https://github.com/ryanbr/noop/blob/HEAD/docs/superpowers/specs/2026-06-29-oura-onboarding-ux.md

## D. Her own constraints (from the suite and her lists)

- things-i-like.md: tertiary-only palette, dark blue + shimmer,
  sun-through-leaves, glows, flares, stained glass, subtle rainbows,
  gentle motion. Applied as token hard rules.
- Sleep-tracker rules: restrained accent palette (never rainbow as
  UI), IQR-tinted distribution pills, headers bigger than subtext,
  one-line row labels, month-colored date squares. Carried into chart
  conventions.
- Her standing "deep work" design rule (AGENTS.md): research first,
  extract concrete tokens from references, self-check against them,
  report honestly. Followed.

## What I deliberately did NOT take

- Primary-color health app conventions (clinical blue `#0052CC` style)
  — she hates primaries; the tokens route clinical blue through
  ultramarine/cerulean instead.
- Gamified streak language and rainbow-everywhere wellness aesthetics
  — register mismatch for chronic health; streaks became
  constellations, rainbows stay dull/subtle.
- Decorative gradients as identity, chart-redraw animations,
  bouncy/spring motion — all in the do-nots.
