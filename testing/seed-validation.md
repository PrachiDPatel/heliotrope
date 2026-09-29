# Heliotrope — Seed Validation Procedure

Validates her real seeded data against what she actually told us, without
ever committing personal data to this public repo.

## The two-hop model

```
her stated facts  ←→  data team's seed fixture  ←→  rows in D1
      (hop 1)                  (hop 2)
```

- **Hop 1** — the fixture matches her facts. The data team's seed fixtures
  live outside git (`scripts/seed.local/`). The testing lead checks every
  value against the expected-values fixture, not against the data team's
  word.
- **Hop 2** — the database matches the fixture. Run the seed script against
  a scratch local D1, then dump and diff every table against the fixture:
  no dropped rows, no truncated text, no type coercion (e.g. doses stored
  as numbers losing units), no missing relations.

A gate passes only when both hops are green. Execute once the data team
delivers the seed, and re-run after any seed change.

## Expected-values fixture (gitignored, never committed)

- Template: `testing/fixtures/seed-expectations.TEMPLATE.yaml`
  (committed — placeholders only).
- Real file: `testing/fixtures/seed-expectations.local.yaml`
  (gitignored — built by the testing lead from her stated facts: the
  2026-09-29 statements, the lab transcription at
  `~/workspace/health/labs/2026-09-09/README.md`, her prescriber's session
  notes, and the insurance card scans).
- If the fixture and her stated facts disagree, **her stated facts win**
  and the data team re-seeds. Record the discrepancy in the gate report.

## Record categories to validate

Every seeded record is checked on all of these; one line per record in the
validation run output.

1. **Identity** — the record is the right thing (correct med, correct
   doctor, correct lab panel, correct todo).
2. **Completeness** — no field she stated is dropped (dose, schedule,
   phone, specialty, reference range, flag status).
3. **Status correctness** — meds land in the right bucket: current /
   incoming / has-but-not-taking / previously-mentioned-confirm-status.
   The classic failure is a "confirm status" med seeded as current.
4. **Precision** — numbers match exactly (lab values, reference ranges,
   doses). Decimal and unit fidelity: `65 mg` must not become `65`.
5. **Relations** — med → prescriber, todo → specialty, refill alert →
   correct phone number. A med pointing at the wrong doctor is a data bug.
6. **Flags** — lab flags preserved (`% saturation LOW` must still read LOW
   in the app), prescriber warnings attached to the right med
   (e.g. the birth-control-effectiveness note on modafinil).

## Input validation rules (forms, edge + DB)

Every write path enforces these; the migration tests prove the DB side
and the pathway tests prove the UI side.

| Field | Rule |
|-------|------|
| Dates | Real calendar dates only; no 2026-02-30; lab collection date ≤ today; no far-future dates on historical records |
| Times / schedules | Valid HH:MM; schedule anchors (e.g. "after breakfast") from a closed vocabulary, no free-text schedule drift |
| Doses | Number + unit required; unit from a closed list (mg, mcg, g, mL, tablets, IU, %); dose > 0 |
| Phone numbers | 10 digits (US) after stripping formatting; tap-to-call must produce a dialable `tel:` link |
| Lab values | Numeric; stored with the unit and reference range as recorded; flagged status is data, not presentation |
| Text (notes, rich text) | Stored verbatim; no silent truncation (max length defined per column and enforced, not clipped) |
| Enums (med status, todo priority, share scope) | Closed set; unknown values rejected at insert |

## The validation run (how to execute)

1. `cp testing/fixtures/seed-expectations.TEMPLATE.yaml testing/fixtures/seed-expectations.local.yaml` and fill from her stated facts (one time; update when she states new facts).
2. Apply migrations to a scratch local D1.
3. Run the data team's seed script against the scratch D1.
4. Dump every seeded table to JSON.
5. For each expected record: check identity, completeness, status,
   precision, relations, flags (the six checks above). Fail the run on
   the first mismatch — then fix, re-seed from scratch, re-run.
6. Row counts per table must equal the fixture exactly (no silent drops).
7. Write the run log to `testing/evidence/<gate>/seed-validation/` and
   summarize in the gate report.
8. **Delete the scratch D1** after the run. Never leave seeded real data
   in a disposable copy.

## Red flags (instant FAIL-BLOCKED)

- A med she has-but-doesn't-take seeded as current.
- A "confirm status" med seeded as current.
- A lab flag (LOW/HIGH) lost or inverted.
- A refill phone number that dials the wrong party.
- Any record from her stated list missing after seeding.
- Any seeded record NOT in her stated list (phantom data).
- Personal data found in any committed file or log (privacy violation —
  stop and scrub before continuing).
