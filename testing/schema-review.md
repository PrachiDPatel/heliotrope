# Heliotrope — Schema / Migration Constraint Review

Runs once the data team's schema and migrations land in `db/`. The
question is always: **what bad data can get in, and what good data gets
rejected?**

## How it runs

1. Apply all migrations to a scratch local D1, in order, from empty.
2. Walk the coverage matrix below: for every row, run the SQL and record
   PASS (rejected/accepted exactly as specified) or FAIL.
3. Test rollback: apply, seed a few rows, migrate down (if supported),
   migrate back up — data must survive or the migration must say it won't.
4. Re-run after any migration change. Migrations are append-only; a fix
   is a new migration, never an edit to a landed one.

## Coverage matrix

Fill the `Gate` column per gate: PASS / FAIL-BLOCKED.

### Structural

| # | Check | Gate |
|---|-------|------|
| S1 | Migrations apply cleanly on an empty DB, in filename order | |
| S2 | Re-running all migrations on an already-migrated DB is a no-op (idempotent) | |
| S3 | Every table has a primary key; every FK references a real PK | |
| S4 | `created_at` / `updated_at` defaults exist and are sane (UTC) | |

### Constraint coverage — the actual matrix

| # | Table / column | Bad insert attempted | Must… | Gate |
|---|---------------|----------------------|-------|------|
| C1 | meds.status | `'sometimes'` (not in enum) | REJECT | |
| C2 | meds.dose_value | `-5`, `0`, `'a lot'` | REJECT | |
| C3 | meds.dose_unit | `'handful'` (not in closed unit list) | REJECT | |
| C4 | meds.schedule | free-text outside the schedule vocabulary | REJECT | |
| C5 | meds.refill_phone | `'call mom'`, 7-digit number | REJECT (when present) | |
| C6 | meds.prescriber_id | FK to a doctor that doesn't exist | REJECT | |
| C7 | doctors.status | `'maybe'` | REJECT | |
| C8 | lab_results.value | non-numeric | REJECT | |
| C9 | lab_results.collected_date | `2026-02-30`, future date | REJECT | |
| C10 | lab_results.flag | `'kinda low'` | REJECT (closed set) | |
| C11 | lab_results | analyte row with no panel FK | REJECT | |
| C12 | todos.priority | `'urgent-ish'` | REJECT | |
| C13 | notes.body | 100k-char blob (over column limit) | REJECT cleanly, not silent-truncate | |
| C14 | share_scope (family) | `'everyone lol'` | REJECT | |
| C15 | family_members.user_id | duplicate membership | REJECT (unique) | |
| C16 | any text column | `NULL` where the app promises a value (NOT NULL coverage per spec) | REJECT | |
| C17 | any unique column | duplicate insert | REJECT | |

### Good-data survival (the other half — constraints must not eat real data)

| # | Check | Gate |
|---|-------|------|
| G1 | Full seed fixture inserts cleanly (all tables, all relations) | |
| G2 | Rich-text note with unicode/emoji round-trips byte-identical | |
| G3 | Long lab panel (20+ analytes) inserts and reads back in order | |
| G4 | Update a med's status current → has_but_not_taking; history preserved or explicitly versioned per spec | |
| G5 | Delete a todo; no orphaned notes left behind (or orphans explicitly allowed per spec) | |

### Sync-safety

| # | Check | Gate |
|---|-------|------|
| Y1 | Two clients write different fields of the same row → merge, no silent overwrite (per architects' conflict rule) | |
| Y2 | Write with a stale `updated_at` → conflict surfaces, not silent loss | |

## Red flags (instant FAIL-BLOCKED)

- A migration edits a previously landed migration instead of adding a new one.
- `TEXT` column with no length limit holding user notes (silent-truncate risk).
- FK missing where the app assumes a relation (med → doctor, lab row → panel).
- Enum enforced only in the Worker, not in D1 (DB must be the last line of defense).
- Timestamps in local time instead of UTC.
