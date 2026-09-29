# Heliotrope — Test Strategy (Testing lead)

This is the standing test plan for both mandates. It never changes without a
gate review.

## The two mandates

**1. DATA VALIDATION** — her data is the app. A wrong med name or a dropped
lab row is worse than a broken button.
- Every seeded record (meds, doctors, labs, insurance, todos, body issues)
  validated against what she actually told us. Source of truth: the data
  team's seed fixtures (outside git), cross-checked against her stated facts.
- Form inputs validated at the edge AND the DB: dates real, doses sane,
  phone numbers well-formed.
- Every migration has a constraint test: bad data must be rejected, good data
  must survive round-trips.
- No silent data loss on sync — local write → API → D1 must be provable,
  not assumed.

**2. PATHWAY CHECKS** — every user flow walked end-to-end, tapped by hand
(or by Playwright taps), before any gate passes. The living checklist is
`pathway-checklist.md`. Green or blocked, no maybes.

## What "passes" means

A gate passes when ALL of these are true:
1. Every row in `pathway-checklist.md` marked with a gate verdict of
   PASS, or FAIL-BLOCKED with an owner + fix round (blockers are fine,
   maybes are not).
2. Seed validation ran against the latest seed fixtures and the full
   expected-values list matched (`seed-validation.md`).
3. Schema review ran against the latest migrations; every constraint in
   `schema-review.md`'s coverage matrix is exercised (`db` dir in repo).
4. Screenshots exist for every shipped screen: iPhone 390x844 + desktop
   1280x800, and the contrast script reports PASS on all text
   (`screenshot-harness.md`).
5. Review board sign-off (psychologist / physician / artist) recorded in
   the gate report.

## Environments

- **Local D1** (`wrangler d1 execute --local`): all data tests run here
  first. Cheap, fast, no production risk.
- **Preview** (Worker on a preview URL): pathway tap-tests, screenshots.
- **Production**: nothing is ever tested in production. Seed validation
  runs against her local DB copy before she ever opens the app.

## Test layers

1. **Migration tests** (SQL, local D1): apply migrations up, insert
   representative good rows, attempt representative bad rows, roll back.
   Bad inserts must fail with the constraint we intended.
2. **API tests** (Worker): every REST endpoint, happy path + malformed
   input + unauthorized + cross-family-user access (scoped access).
   Family scoping gets its own suite — this is privacy-critical.
3. **Pathway tests** (Playwright + manual tap): user flows from
   `pathway-checklist.md`, on iPhone viewport with touch. Every tap that
   should do something gets its tap verified.
4. **Visual tests**: screenshot per screen per gate + contrast checks.
   Her aesthetic is dark blue + shimmer + glow — readability is policed
   by script, not by eyeballing.
5. **Sync/loss tests**: write locally, sync, diff. Write while offline,
   reconnect, diff. Every write must be accounted for; the test counts
   rows before and after.

## Test data rules (privacy)

This repo is public. **Zero personal data in git — ever.** That includes
test fixtures with her real med names, doctor names, or lab values.

- Expected values live in a gitignored fixture
  (`testing/fixtures/seed-expectations.local.yaml`, never committed).
  A placeholder template (`seed-expectations.TEMPLATE.yaml`) documents the
  shape with `<placeholder>` values.
- The data team's real seed fixtures also live outside git
  (`scripts/seed.local/`).
- Generic/dummy fixtures used in automated tests are invented data
  ("Test Med 250mg", "Dr. Example") — safe to commit.
- Screenshots with seeded real data never leave the local machine.
- CI (if any) runs against invented data only.

## Reporting

Each gate gets a report in `testing/gate-reports/<phase-N>.md` with:
the checklist verdicts, the data-validation result, the schema-review
result, screenshot + contrast results, review-board sign-offs, and the
blocker list with owners. A gate is not passed until this file exists
and the coordinator has merged it.
