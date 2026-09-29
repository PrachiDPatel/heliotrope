# Heliotrope data dictionary

Describes the D1 schema in `db/schema.sql` (built from `db/migrations/`).
No personal data lives in this repo — this doc describes shapes only.

Conventions: `id` is always a TEXT primary key. `user_id` foreign keys cascade on
delete. Timestamps are ISO-8601 UTC strings. JSON-ish columns store JSON text.

## users
Family accounts sharing one Heliotrope instance. `relationship`: self, spouse,
partner, child, parent, sibling, other. `color` is a UI accent per account.
Auth: `username`/`password_hash` (nullable — family accounts can exist without a
login), `role`: owner or family. `display_name` is the auth-facing name.

## sessions / shares / digests
Server-side opaque sessions (90-day sliding "cached login"); share grants
(default-deny family access); service-ingested daily chat digests.

## meds
Everything she takes, is about to take, or has on hand. `status`: `current`
(taking now), `incoming` (bought/planned, not started), `on_hand` (has it, not
taking), `inactive` (was mentioned, status unconfirmed), `discontinued`.
`directions` holds plain-language how/when plus the prescriber's titration plan.
`schedule_json` holds machine-readable schedule info (e.g. `{"anchor":"wake_time"}`
for meds taken at wake rather than clock time). `photo_r2_key` points at
the bottle photo in R2. Links to `pharmacy` for refills.

## med_wisdom_cards
Plain-language cards attached to a med (or standalone): interactions, timing
rules, food notes, side effects, tips, and her own recorded experiences.
`category`: interaction, timing, food, side_effect, tip, experience.

## doctors
Care team. `status`: `current`, `seeking` (has one, looking for a replacement),
`former`, `to_find`. `role` is a free-text slot like pcp, psychiatrist, therapist.

## pharmacy
Her pharmacy/pharmacies: name, address, phone, fax, hours.

## insurance_docs
Metadata only — card scans live in R2 (`r2_key_front`, `r2_key_back`). Holds the
transcribed fields: insurer, plan, member ID, group, plan code, Rx BIN/PCN/GRP,
effective date, copays (primary / specialist / ER / urgent), Rx tiers
(retail + mail), deductibles, coinsurance, employer, member services phone.

## labs
One row per blood draw: `collected_date`, `ordered_by`, `performed_by`, `note`.

## lab_panels
One row per analyte. `panel_name` groups rows (e.g. "Comprehensive metabolic panel").
`value_num` for numbers, `value_text` when it isn't numeric. `ref_low`/`ref_high`
are the reference range; either may be NULL (e.g. eGFR is reported as >60).
`flag`: low, normal, high, critical. `notes` carries report remarks like
"flagged LOW on report" or "calculated".

## todos
The to-do list, including the find-a-doctor list. `category`: doctor,
appointment, refill, lab, insurance, other. `priority`: 1 (highest) to 5.
`status`: open, in_progress, done, snoozed. `related_doctor_id` links a todo to
a doctor row when relevant.

## diet_entries
Food log: `logged_at`, `meal_type` (breakfast/lunch/dinner/snack), free-text
`description`, `calories`, `protein_g`, optional meal photo in R2.

## cycle_entries
One row per date (unique per user+date). `flow`: none, spotting, light, medium,
heavy. `symptoms_json` is a JSON array of symptom tags.

## stress_entries
Stress check-ins: `logged_at`, `level` 1–10, free-text `triggers`.

## skincare_routine / bodycare_routine
Ordered routine steps: `step_order`, `name`, `product`, `frequency`
(am, pm, both, weekly, as_needed), `active` flag.

## weight_entries
One row per date (unique per user+date): `weight_lb`, optional `body_fat_pct`.

## mind_entries
Daily patterns, not diagnoses. One row per date (unique per user+date): `mood`,
`energy`, `anxiety`, `focus`, `sleep_quality` (each 1–5), plus free-text `notes`.

## diary_entries
Journal entries: `date`, `title`, `body`, `tags_json` (JSON array).

## orders
Health stuff she ordered, tracked from her inbox: `vendor`, `order_number`,
`status` (ordered, shipped, delivered, cancelled), `expected_date`,
`tracking_url`, `cost_cents`.

## reports
One-tap doctor-ready summaries: `kind` (visit_summary, lab_summary, custom),
linked `doctor_id`, `visit_date`, the `summary` text, optional `r2_key` for a
PDF/photo attachment.

## chat_digests
Summaries pulled from her chats (e.g. the health side chat): `digest_date`,
`source` (which chat), `summary`, `key_points_json` (JSON array). Unique per
user + date + source.
