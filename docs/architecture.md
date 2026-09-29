# Heliotrope — System Architecture (Phase 1)

Status: scaffold + auth skeleton. Endpoint handlers beyond auth/health/digest are 501 stubs for Phase 2 teams.

## 1. The shape of the thing

Heliotrope is an iPhone-first web app backed by a Cloudflare Worker with D1 for structured data and R2 for photos. It is the sibling of her sleep tracker (`sleep-tracker` worker + D1), and the two share an app family, a design language, and cross-links — but each keeps its own database, so one app's outage never takes the other down.

```
┌─────────────────────────────┐
│  apps/web (iPhone-first UI) │   tabs: Today · Body · Meds · Labs · Care team
│  static, served by Worker   │         To-dos · Nourish · Cycle/Stress/Skin/Weight
└──────────────┬──────────────┘         Mind · Orders · Reports
               │  same-origin /api/*
┌──────────────▼──────────────┐
│  worker (Cloudflare Worker) │
│  src/index.js  — router      │
│  src/auth.js   — sessions    │
└──────┬──────────────┬───────┘
       │ D1 binding   │ R2 binding
┌──────▼──────┐  ┌────▼──────────┐
│ heliotrope- │  │ heliotrope-   │
│ db (D1)     │  │ photos (R2)   │
└─────────────┘  └───────────────┘
```

Request path: the browser talks only to the Worker on the same origin. The Worker is the only thing that touches D1/R2. There is no direct database access from the client, ever.

## 2. Why this stack

- **Cloudflare Worker + D1** — same as the sleep tracker, which she already operates. Zero new infrastructure to learn, one deploy pattern (`wrangler deploy`), one dashboard. D1's included 5 GB is plenty for years of structured health data; nothing about this app is storage-hungry.
- **R2 for photos** — med-bottle photos, lab-result scans, insurance cards. Binary blobs don't belong in a relational DB; R2 is the same object-storage pattern, no egress fees, and the Worker signs short-lived URLs so photos are never publicly listable.
- **No framework on the backend** — plain modules. The sleep tracker proved a ~300-line Worker is easier for her to read and debug at 3 AM than an ORM or framework. Same philosophy here.
- **Frontend in `apps/web`** — plain HTML/CSS/JS in Phase 1 (she edits it by hand on her phone-adjacent workflow today). A build step is a Phase 3 decision, not Phase 1.

## 3. Monorepo layout

| Path | Owns | Notes |
|---|---|---|
| `apps/web/` | iPhone-first frontend | served by the Worker in later phases (Workers static assets or inlined, TBD by the frontend team — sleep tracker inlines via build.py; Heliotrope should pick one pattern and stick to it) |
| `worker/` | API | `wrangler.toml`, `src/index.js` (router), `src/auth.js` (sessions). One route per tab + shared endpoints |
| `db/` | D1 schema + migrations | numbered `NNNN_name.sql` migrations; `schema.sql` is the Phase 1 bootstrap only |
| `docs/` | architecture, API, design tokens, local dev | the docs you are reading |
| `assets/` | icon, illustrations, ambient art | shared with the design-system notes in `docs/design-tokens.md` (Phase 2) |
| `scripts/` | helpers | seed scripts live **outside git** (`scripts/seed.local/`, gitignored) — see §6 |

Phase 1 ships `worker/`, `db/schema.sql`, and `docs/`. `apps/web/` and `assets/` are empty pending the frontend/design teams.

## 4. Sharing with the sleep tracker

The two apps are siblings, not one app. The sharing contract is deliberately thin:

1. **Design system** — one shared token file (`docs/design-tokens.md` in Phase 2; CSS custom properties: bg, surface, text, accent, radius, the night-sky palette the sleep tracker uses). Heliotrope uses the same tokens so the suite feels like one product. The tokens doc is the single source of truth; each app's CSS imports/copies it.
2. **Cross-links, not shared state** — the sleep tracker's "open this night in Heliotrope" and Heliotrope's Mind tab "view sleep for this date" are deep links (`heliotrope…/mind?date=YYYY-MM-DD`), each app reading its own DB. No cross-database joins, no shared sessions.
3. **Shared ops pattern** — same `wrangler.toml` shape, same `POST /api/digest`-style ingest convention, same local-dev flow, so knowledge transfers.

What is explicitly NOT shared: databases, user sessions, or deploy pipelines. Coupling those would turn two simple apps into one fragile one.

## 5. Auth — family accounts with long-lived sessions ("cached login")

She hates re-logging in. The design gives her a 90-day rolling session while keeping the security properties that matter. Full detail is in the code (`worker/src/auth.js`); the decisions:

**Server-side sessions, not JWTs.**
The cookie holds an opaque 256-bit random token; D1 stores only its SHA-256 hash plus expiry. Why: sessions can be revoked instantly (logout actually logs out), a leaked DB dump can't replay tokens, and there's no secret-signing key to rotate. The cost — one D1 read per request — is trivial at this scale.

**Cookie flags: `HttpOnly; Secure; SameSite=Lax; Path=/`.**
`HttpOnly` means page JavaScript can never read the token (XSS can't steal it). `SameSite=Lax` plus a same-origin API means CSRF is a non-issue without a token dance: cross-site POSTs simply don't carry the cookie, and there are no cross-origin clients in Phase 1.

**Password storage: PBKDF2-SHA256, 210k iterations, per-password salt, constant-time compare.**
Workers have WebCrypto but no argon2/bcrypt, so PBKDF2 at OWASP's current iteration count is the right native choice. Stored format is `pbkdf2-sha256$iter$salt$hash` — self-describing so iteration counts can be raised later. Never plaintext, never in logs, and login returns the same "invalid credentials" whether the username or password was wrong.

**"Cached login": 90-day sliding sessions.**
Every authenticated request extends `expires_at` by 90 days from now. She stays logged in indefinitely as long as she opens the app at least quarterly. Rotation: the token is re-issued on role/privilege changes; old tokens are revoked server-side.

**Per-user scoping: `owner_id` on everything.**
Every personal-data table carries `owner_id → users(id)`. The auth middleware attaches `ctx.scope.readableOwnerIds` (own id + any granted shares) and every query filters with `WHERE owner_id IN (...)`. There is no code path that reads another user's rows without an explicit grant row.

**Family accounts: default-deny sharing.**
Accounts are `owner` (her) or `family`. A family member sees **only** what she explicitly shares via a `shares` row (`scope: summary | full`), revocable at any time (`revoked_at`). No share row = no data. The intended uses are things like a parent seeing the med refill schedule — never labs, never the diary — and the grant UI (Phase 2) defaults to `summary`.

**What's stubbed for later:** login rate limiting (per-IP/username throttle, Phase 2 — noted as a TODO in the code), the share-grant management UI and API, session device listing ("log out everywhere"), and R2 signed-URL issuance for photos.

## 6. Data flow and privacy

The repo is **public**. The hard rule, enforced by `.gitignore` and by review:

- Git holds: schema, migrations, code, docs, design assets. Never: meds, labs, doctors, insurance, session secrets, D1 database IDs for production, `.dev.vars`.
- Personal data enters D1 only through a **gitignored local script** (`scripts/seed.local/`, owned by the data team) run on her own machine. It is never committed, never pasted into issues, never in screenshots of the repo.
- The digest ingest endpoint (`POST /api/digest`) authenticates with a **Worker secret** (`DIGEST_INGEST_SECRET`) in the `Authorization: Bearer` header — service-to-service, not a user session. The scheduled job that files chat digests holds the secret; it's set with `wrangler secret put` and lives only in Cloudflare and her local `.dev.vars`.
- Photos go to R2; D1 stores only the object key + metadata. Access is via Worker-signed URLs, never public bucket listing.

## 7. API surface

Full route list and payload shapes: `docs/api.md`. In brief:

- `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me`
- One route group per tab: `/api/today`, `/api/meds*`, `/api/labs*`, `/api/care-team*`, `/api/todos*`, `/api/nourish*`, `/api/cycle`, `/api/stress`, `/api/skin`, `/api/weight`, `/api/mind/entries`, `/api/orders*`, `/api/reports/visit-summary`, `/api/body/systems`
- `POST /api/digest` — service-authenticated ingest for daily chat summaries (implemented in Phase 1)
- `POST /api/photos/upload` → R2 (Phase 2)

All `/api/*` except login/health/digest require the session cookie. All responses are JSON; errors are `{ error: "..." }` with the right status code.

## 8. Environments

- **Local**: `npx wrangler dev` from `worker/` — ephemeral local D1/R2, `.dev.vars` for secrets (gitignored). See `docs/local-dev.md`.
- **Preview/production**: `wrangler deploy`. Production `database_id` and bucket names are set in `wrangler.toml` at deploy time by the coordinator — never committed with real IDs in a team branch.

## 9. What's stubbed for later phases (explicit non-goals of Phase 1)

- Every domain endpoint handler (meds, labs, todos, …) — 501 stubs with planned shapes in `docs/api.md`
- Frontend (`apps/web/`) — tab UI, design tokens doc, offline behavior
- Share-grant management UI/API, login rate limiting, "log out everywhere"
- R2 signed-URL photo upload flow
- Report generation (visit summaries) beyond the route stub
- Any background jobs besides the digest ingest contract

## 10. Open questions for the coordinator

1. Frontend serving pattern: Workers static assets vs. inlined single-file (sleep tracker style)? Frontend team to decide; the worker currently returns a placeholder at `/`.
2. Should the sleep tracker get a Heliotrope deep link in its next deploy, or wait until Heliotrope has a real frontend?
3. Family account creation flow: does she invite family herself (owner-created accounts), or self-serve signup with an invite code? Recommend owner-created — simpler, no open registration on a health app.
