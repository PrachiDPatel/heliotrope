# Heliotrope — Pathway Checklist (living)

Every user flow, walked end-to-end. Status per gate. This file ships with
every gate report.

**Gate verdicts:** `NOT-BUILT` (flow doesn't exist yet) · `PASS` (walked
end-to-end, evidence attached) · `FAIL-BLOCKED` (broken or untested —
gate does not pass, owner + fix round named). **No maybes.**

Evidence convention: `testing/evidence/<gate>/<flow>/` holds the
screenshot(s) + notes. Screenshots taken on iPhone 390x844 unless noted.

## Auth & family accounts

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| A1 | Sign in with cached login (persistent session) | NOT-BUILT | | | | |
| A2 | Session survives app close/reopen (httpOnly cookie) | NOT-BUILT | | | | |
| A3 | Family member login → sees ONLY shared data (med list scoped, labs hidden unless shared) | NOT-BUILT | | | | |
| A4 | Family member cannot reach her private endpoints (API rejects cross-scope reads) | NOT-BUILT | | | | |
| A5 | Sign out ends session everywhere it should | NOT-BUILT | | | | |

## Today

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| T1 | Today shows meds due now (from seeded schedule) | NOT-BUILT | | | | |
| T2 | Today shows top-priority todos | NOT-BUILT | | | | |
| T3 | Marking a med "taken" updates the Today state | NOT-BUILT | | | | |

## Body

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| B1 | Tap a body system (e.g. nervous) → her problems/notes for it appear | NOT-BUILT | | | | |
| B2 | Every tap region on the illustration is reachable (no dead zones) | NOT-BUILT | | | | |
| B3 | Add a note to a body system → persists and reappears on revisit | NOT-BUILT | | | | |
| B4 | Seeded known issues (fatigue, dizziness, brain fog, jaw tension, allergies/congestion, sleep disorder) all present | NOT-BUILT | | | | |

## Meds

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| M1 | Add a med → appears in list with correct name/dose | NOT-BUILT | | | | |
| M2 | Set schedule → plain-language schedule renders ("after breakfast") | NOT-BUILT | | | | |
| M3 | Bottle photo capture → photo attaches to med record | NOT-BUILT | | | | |
| M4 | Low-stock detection → refill alert fires | NOT-BUILT | | | | |
| M5 | Refill alert → one-tap call reaches the RIGHT number (pharmacy vs doctor per med) | NOT-BUILT | | | | |
| M6 | Full chain: add med → schedule → refill alert → tap-to-call | NOT-BUILT | | | | |
| M7 | Interaction scanner flags a known interaction over her med list (informational tone, routes to pharmacist/doctor) | NOT-BUILT | | | | |
| M8 | "Can I drink tonight?" alcohol check → informational answer, never medical advice | NOT-BUILT | | | | |
| M9 | Seeded med statuses correct: current / incoming / has-but-not-taking / previously-mentioned-confirm (never mislabeled as current) | NOT-BUILT | | | | |

## Labs

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| L1 | Upload a lab result (image) → stored in R2, record in D1 | NOT-BUILT | | | | |
| L2 | Enter lab values → trend chart updates | NOT-BUILT | | | | |
| L3 | One-tap share/send a lab trend to a doctor | NOT-BUILT | | | | |
| L4 | Full chain: upload lab → trend → share with doctor | NOT-BUILT | | | | |
| L5 | Seeded 2026-09-09 panel values match transcription exactly (all rows, incl. flagged LOW % saturation) | NOT-BUILT | | | | |
| L6 | Reference ranges display with the value (flag out-of-range) | NOT-BUILT | | | | |

## Care team

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| C1 | Doctor directory shows current doctors (PCP / psychiatrist / therapist) | NOT-BUILT | | | | |
| C2 | "To find" list shows open specialties with status (endocrinologist, cardiologist, new PCP, sleep, psychiatrist, therapist, chiropractor, optometrist, dentist) | NOT-BUILT | | | | |
| C3 | Pharmacy card → tap-to-call dials the pharmacy | NOT-BUILT | | | | |
| C4 | Insurance card renders beautifully from seed (plan name, PPO) | NOT-BUILT | | | | |
| C5 | Documents: insurance card scans + passport card display | NOT-BUILT | | | | |

## To-dos

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| D1 | Create a todo → appears in list | NOT-BUILT | | | | |
| D2 | Set priority → list re-sorts by priority | NOT-BUILT | | | | |
| D3 | Rich-text note on a todo → formatting persists | NOT-BUILT | | | | |
| D4 | Full chain: create → prioritize → rich-text note → complete | NOT-BUILT | | | | |

## Nourish

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| N1 | Log a meal → appears in the day's log | NOT-BUILT | | | | |
| N2 | Vegetarian-aware: flags/suggests appropriately | NOT-BUILT | | | | |

## Cycle / Stress / Skin / Body / Weight

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| W1 | Log a period day → cycle chart + prediction update | NOT-BUILT | | | | |
| W2 | Log a stress check-in → stress chart updates | NOT-BUILT | | | | |
| W3 | Log weight (HealthKit path) → weight chart updates | NOT-BUILT | | | | |
| W4 | Skincare / body-care routine check-off persists | NOT-BUILT | | | | |
| W5 | Full chain: log period + stress + weight → all three charts update | NOT-BUILT | | | | |

## Mind

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| P1 | Diary entry → appears in timeline, patterns page reads from real entries | NOT-BUILT | | | | |
| P2 | Pattern summaries framed as patterns, never diagnoses (review-board check) | NOT-BUILT | | | | |
| P3 | Prionaria import → entries land in Mind, tone stays gentle | NOT-BUILT | | | | |

## Orders

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| O1 | Gmail scan detects a health shipment → appears in Orders with tracking | NOT-BUILT | | | | |
| O2 | Manually add an order → tracking visible | NOT-BUILT | | | | |

## Reports

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| R1 | Generate a visit summary → contains meds, labs, symptoms, sleep | NOT-BUILT | | | | |
| R2 | Send report → reaches the right person (share sheet / doctor contact) | NOT-BUILT | | | | |
| R3 | Full chain: generate → send | NOT-BUILT | | | | |

## Notifications

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| E1 | Med low-stock → notification with "call pharmacy" deep link | NOT-BUILT | | | | |
| E2 | Appointment reminder fires at the right time | NOT-BUILT | | | | |

## Sync & data integrity

| # | Flow | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| S1 | Write locally → sync → server row matches (count + content diff) | NOT-BUILT | | | | |
| S2 | Write while offline → reconnect → no rows lost, no duplicates | NOT-BUILT | | | | |
| S3 | Edit a synced record → edit survives (no silent revert) | NOT-BUILT | | | | |

## Accessibility (every visual gate)

| # | Check | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|------|---------|---------|---------|---------|---------|
| X1 | Contrast script PASS on all text (see screenshot-harness.md) | NOT-BUILT | | | | |
| X2 | Touch targets ≥ 44pt on iPhone viewport | NOT-BUILT | | | | |
| X3 | Screens readable with reduced-motion on (glows/animations off) | NOT-BUILT | | | | |

---

## Gate log

- **Phase 1** (2026-09-29): harness set up. All flows NOT-BUILT — expected.
