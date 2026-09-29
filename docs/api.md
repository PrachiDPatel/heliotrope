# Heliotrope REST API — Phase 1 outline

Base: same origin as the app. All `/api/*` except `POST /api/auth/login`, `GET /api/health`, and `POST /api/digest` require the session cookie (`HttpOnly; Secure; SameSite=Lax`). All responses are JSON. Errors: `{ "error": "message" }` with the appropriate status (400 validation, 401 unauthenticated, 403 forbidden — e.g. reading outside your share scope, 404, 409 conflict, 501 not yet implemented).

Conventions:
- Dates are `YYYY-MM-DD`; datetimes are ISO-8601 UTC.
- List endpoints paginate with `?limit=&cursor=`; `cursor` is opaque.
- Every personal-data object carries `owner_id`; family viewers only ever see rows within their granted scope.

## Auth

| Method & path | Body | Returns |
|---|---|---|
| `POST /api/auth/login` | `{ username, password }` | `{ ok, user: { id, displayName, role } }` + sets session cookie |
| `POST /api/auth/logout` | — | `{ ok: true }` + clears cookie |
| `GET /api/auth/me` | — | `{ user, readableOwnerIds, shares }` (Phase 2: device sessions) |

## Today

| Method & path | Notes |
|---|---|
| `GET /api/today?date=YYYY-MM-DD` | Aggregated: meds due now, to-dos due, refill warnings, today's digest link. The "what do I need right now" screen. |

## Body

| Method & path | Notes |
|---|---|
| `GET /api/body/systems` | Body-system cards with current status summaries (each links deeper in Phase 2) |

## Meds

| Method & path | Body | Returns |
|---|---|---|
| `GET /api/meds` | — | `[{ id, name, photo_key, schedule_text, next_dose_at, refill: { refills_left, pharmacy, phone } }]` |
| `POST /api/meds` | `{ name, schedule_text, ... }` | created med |
| `GET /api/meds/:id` | — | med detail incl. dose history |
| `PATCH /api/meds/:id` | partial | updated med |
| `POST /api/meds/:id/taken` | `{ taken_at?, dose? }` | dose log entry |
| `POST /api/photos/upload` | multipart `photo` | `{ key }` — R2 object key for bottle/label photos (Phase 2) |

## Labs

| Method & path | Notes |
|---|---|
| `GET /api/labs` | All panels: `[{ id, date, panel, markers: [{ marker, value, unit, flag }] }]` |
| `GET /api/labs/series?marker=ferritin` | Time series for trend charts + doctor export |

## Care team

| Method & path | Notes |
|---|---|
| `GET /api/care-team` | `[{ id, kind: doctor\|pharmacy\|insurance, name, specialty, phone, address, notes }]` |
| `POST /api/care-team` / `PATCH /api/care-team/:id` | Phase 2 |

## To-dos

| Method & path | Body | Notes |
|---|---|---|
| `GET /api/todos?status=open` | — | `[{ id, title, priority, due, notes, kind: find-doctor\|appointment\|... }]` |
| `POST /api/todos` | `{ title, priority?, due?, notes? }` | create |
| `PATCH /api/todos/:id` | `{ status?, ... }` | update / complete |

## Nourish

| Method & path | Notes |
|---|---|
| `GET /api/nourish?date=YYYY-MM-DD` | day's food log |
| `POST /api/nourish` | `{ date, entries: [{ time, text, photo_key? }] }` — low-friction, "food, such as it is" |

## Cycle / Stress / Skin / Weight

| Method & path | Notes |
|---|---|
| `GET /api/cycle` / `POST /api/cycle` | cycle log entries |
| `GET /api/stress` / `POST /api/stress` | stress check-ins `{ date, level 1-5, note? }` |
| `GET /api/skin` / `POST /api/skin` | skin log `{ date, note, photo_key? }` |
| `GET /api/weight` / `POST /api/weight` | weight entries `{ date, value, unit }` |

## Mind

| Method & path | Notes |
|---|---|
| `GET /api/mind/entries?from=&to=` | diary/pattern entries — patterns, not diagnoses |
| `POST /api/mind/entries` | `{ date, text, tags? }` |

## Orders

| Method & path | Notes |
|---|---|
| `GET /api/orders` | `[{ id, item, ordered_at, status, tracking?, source: inbox }]` — health stuff tracked from her inbox (Phase 2: inbox sync) |

## Reports

| Method & path | Notes |
|---|---|
| `GET /api/reports/visit-summary?from=&to=` | One-tap doctor visit summary: meds, recent labs, open to-dos, digest highlights (Phase 2: PDF export) |

## Digest ingest (implemented, Phase 1)

Service-to-service. The scheduled job files the day's chat summary here.

```
POST /api/digest
Authorization: Bearer <DIGEST_INGEST_SECRET>   # Worker secret, never in git
Content-Type: application/json

{
  "title": "Tue Sep 29 — sleep doctor + labs",
  "date": "2026-09-29",
  "summary_markdown": "# ...\n## Health facts\n...",
  "health_facts": [
    { "fact": "string", "category": "sleep|meds|mood|...", "confidence": 0.0-1.0 }
  ]
}
```

Responses: `201 { ok: true, id }` · `400` missing/invalid fields · `401` bad or missing service secret.

`GET /api/digests?from=&to=` (Phase 2) lists filed digests for the Today/Mind tabs.

## Phase 1 implementation status

Implemented now: `GET /api/health`, `POST /api/auth/login`, `POST /api/auth/logout`, `POST /api/digest`. Everything else returns `501 { error: "not implemented" }` with its route name so frontend teams can build against the contract. Auth middleware (session resolution + scope) is real and guards all `/api/*` routes.
