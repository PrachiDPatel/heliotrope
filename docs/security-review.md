# Heliotrope — Security & Privacy Review (Phase 1)

**Status:** requirements + review, 2026-09-29. No architect implementation exists yet in
any worktree (all teams are at the initial skeleton commit), so this document doubles
as the **security requirements spec** the architects must satisfy in Phase 2. It will be
re-run as a code review once the Worker, schema, and auth code land.

**Scope:** public GitHub repo `PrachiDPatel/heliotrope`, Cloudflare Worker + D1 (+ R2 for
photos), family accounts (Prachi + mom + dad + brother) with long-lived sessions, health
data (meds, labs, insurance, diary), and the agent ingest endpoints (`POST /api/digest`,
order scan, memory scan).

**Threat model (who we're defending against):**
1. **Random internet user** — the repo is public and the Worker URL is reachable. No
   open endpoints, no open registration, no enumerable IDs.
2. **Curious family member** — one family account must never see another's data except
   through explicit, revocable, time-boxed shares.
3. **Shared-device picker-upper** — long-lived sessions on a family iPad or mom's phone
   mean physical access ≈ account access. Per-device sessions, per-device logout, and an
   app-level lock are required mitigations.
4. **Logged-in device thief** — stolen unlocked phone. Session binding + remote revoke-all
   + short presigned media URLs limit blast radius.
5. **The agent infrastructure** — the daily digest / order-scan / memory-scan jobs hold a
   service credential. Least privilege: write-only, per-job keys, never a user session.
6. **Supply chain / processors** — Cloudflare and GitHub are trusted processors, not
   trusted with plaintext for the most sensitive fields (see §4).

**What "done" means:** every P0 item in §6 is implemented and tested before the Phase 2
gate passes. P1 items before family onboarding.

---

## 1. Public-repo hygiene

### 1.1 What may enter git
- Schema and migrations (structure only — see 1.3)
- Worker + frontend source code
- Docs and architecture notes **with placeholder data only** (see 1.4)
- A **synthetic** seed example (`scripts/seed.example.js`) using obviously fake data —
  never derived from her real records
- The secret-scanner itself (`scripts/check-secrets.sh`) — it contains patterns, not secrets
- Art, icons, design tokens

### 1.2 What must NEVER enter git
- Real meds, doses, schedules; lab names/values/dates; doctor names, phones, addresses;
  pharmacy details; insurance carrier, member/group IDs, card scans; diary/journal text;
  anything from the Prionaria import; family members' names tied to health facts
- Any credential: Worker secrets, API tokens, service keys, invite codes, session tokens,
  OAuth client secrets, Cloudflare API tokens, D1 database IDs are fine in wrangler config
  (not secret) but API tokens never
- `.env`, `.dev.vars`, local D1 state (`.wrangler/`), local sqlite dumps, key/cert files,
  editor configs that embed paths, test screenshots taken against real seeded data
- Real Gmail content (order-scan fixtures must be synthetic)

### 1.3 Migration rule
Migrations are **schema-only**. `CREATE TABLE`, indexes, and `INSERT`s of non-personal
lookup data (e.g. a static list of body systems) are fine. Any migration containing an
`INSERT` with names, dates of real events, or medical facts is rejected at merge review.
The coordinator greps every migration diff for `INSERT` (checklist §7).

### 1.4 Placeholder convention (for docs, examples, tests)
- People: role labels (`mom`, `dad`, `brother`) or `Jane Doe` — never real names
- Phones: `555-01xx` range. Emails: `@example.com`. Addresses: obviously fake
- Insurance IDs: `XXX-XX-0000` / `MEMBER_ID_EXAMPLE`. Dates: fixed fake dates
- Photos in fixtures: generated/placeholder images only, EXIF-stripped

### 1.5 .gitignore verification (done 2026-09-29)
Verified with `git check-ignore` that all of these are ignored: `.env`, `.env.*`,
`.dev.vars`, `.wrangler/` (covers local D1 state), `scripts/seed.local/`, `seed.local/`,
`*.local.js`, `node_modules/`, `*.log`, `.DS_Store`. **Gaps found and fixed in this
branch:** `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.sqlite`, `*.sqlite3`, `*.db`,
`dist/`, `build/`, `test-results/`, `playwright-report/` (test screenshots may show real
seeded data), `.vscode/`, `.idea/`, `*.bak`, `*.orig`, `*~`. Re-verified after the fix.

`wrangler.toml`/`wrangler.jsonc` itself is **tracked** (it's needed) but must contain zero
secret values — only `vars` (non-secret config) and references; real secrets go through
`wrangler secret put` and never appear in the file. Merge checklist §7 enforces this.

### 1.6 Secret-scanning guidance for the coordinator's merge reviews
GitHub push protection + secret scanning should be enabled on the repo (repo-settings
action for the coordinator), but they are a backstop, not the process. Before **every**
merge to `main`:
1. Run `scripts/check-secrets.sh` (added in this branch) against the branch diff.
2. `git ls-files | grep -Ei '\.(pem|key|p12|pfx|sqlite3?|db)$|seed\.local|\.env$|\.dev\.vars'`
   must return nothing.
3. Review every **added binary file** (`git diff --stat main...HEAD` shows them) — a PNG
   in `docs/` could be a photo of her real insurance card. Binaries need a human look.
4. Before the **first** push to public GitHub, scan full history:
   `git rev-list --all | xargs -I{} git grep -n -E -f scripts/secret-patterns.txt {} -- . ':!scripts/secret-patterns.txt'`
   History rewrites after going public are painful — do this once, before the repo is public.

High-signal patterns the scanner covers: `ghp_`/`github_pat_`, `AKIA`, `xoxb-`,
`sk_live`, Cloudflare tokens (`v1.0-` + 40 hex), `-----BEGIN .*PRIVATE KEY-----`,
`Bearer eyJ` (JWT-shaped), `password\s*[:=]\s*['"][^'"]{4,}`, `secret\s*[:=]`,
Anthem-style member IDs near the words `member`/`group`, `postgresql://`/`d1://` URLs
with credentials, and 10-digit phone-like strings in `docs/`/`db/`.

---

## 2. Auth review — family accounts, long-lived sessions

The architects' direction (httpOnly cookies, hashed passwords, session rotation) is the
right skeleton. Below is what "done correctly" requires.

### 2.1 Password storage — REQUIRED
- **argon2id**, via a WASM build that runs in Workers (e.g. the `hash-wasm` package —
  pure WASM, no Node APIs). Parameters per the current OWASP Password Storage Cheat
  Sheet.
- Fallback only if WASM argon2id can't fit the Worker's CPU budget on the chosen plan:
  PBKDF2-HMAC-SHA-256 via WebCrypto `SubtleCrypto` at ≥600k iterations (OWASP figure).
  **The architects must benchmark login hashing on the actual plan and record the
  numbers** — never silently pick a weak iteration count to fit free-tier CPU.
- Passwords are never logged, never returned by any API, never stored anywhere but the
  `password_hash` column. Password-reset flows (if any) use single-use expiring tokens,
  not emailed passwords.
- Policy: minimum length 12, no complexity theater (NIST 800-63B). Check new passwords
  against a breached-password list (k-anonymity API or a local top-100k blocklist).
  Auth error messages are generic — "Invalid email or password" for both bad-user and
  bad-password (no account enumeration).

### 2.2 Registration — invite-only (P0 finding)
There must be **no open registration**. The Worker will be on a public URL; open signup
would let anyone create an account on her infrastructure and probe the API. Flow:
- Only Prachi (role `admin`) generates **single-use invite codes** (256-bit random,
  48-hour expiry, bound to a role + a display label like "Mom").
- She sends the code to the family member out-of-band (in person / her existing chat
  with them — never committed anywhere).
- Redeeming a code creates the account; the code is then burned.
- The architects must also rate-limit invite redemption (§5).

### 2.3 Sessions — long-lived "cached login" done safely
- **Token design:** 256-bit CSPRNG session token. The cookie carries the raw token;
  D1 stores **only SHA-256(token)** plus metadata. A DB read alone never yields a live
  session (protects against D1 backup/log exposure).
- **Cookie:** name with `__Host-` prefix (e.g. `__Host-heliotrope-session`), `HttpOnly`,
  `Secure`, `SameSite=Lax`, `Path=/`. No `Domain` attribute (host-only).
- **Lifetimes:** sliding 30-day expiry, absolute 90-day max, then forced re-login.
  **Rotate the token on every refresh** (rotating refresh-token pattern): each use
  issues a new token and invalidates the old; **reuse of an old token = suspected
  theft → revoke the whole token family and notify her.**
- **Device binding (soft):** store a hash of User-Agent + coarse network hint per
  session and a human label ("Prachi's iPhone", "Mom's iPad" — user-confirmable at
  login). On mismatch, don't hard-block (mobile IPs roam) — but flag it in the
  Devices screen and in the audit log.
- **Devices screen (P0 feature):** she sees every active session per account —
  device label, created, last seen, approximate location hint — with **per-device
  revoke** and **"log out everywhere"**. Password change revokes ALL sessions
  immediately.
- **Logout** is server-side: delete the session row AND clear the cookie. Client-only
  logout is not logout.

### 2.4 Shared-device mitigations (threat #3 — the realistic one)
A long-lived session on mom's iPad means anyone holding the iPad is logged in as mom.
Required:
- Per-account **app-level lock**: optional PIN or device biometrics (WebAuthn
  `userVerification`) gating the app after N minutes idle (default 15, configurable).
  At minimum, the lock must cover Prachi's own account.
- Sensitive surfaces (insurance card view, lab export, share-grant creation, report
  send) require **step-up re-authentication** (password or biometrics) even inside a
  valid session.
- No "remember this device" that bypasses the above on a device she marked shared.
- **Roadmap (P1): passkeys.** WebAuthn/passkeys are the right end state on iPhone —
  phishing-resistant, no passwords to share or reuse. TOTP 2FA as the Phase-2
  stopgap, **required for her admin account**, optional for family.

### 2.5 Login hardening
- Rate limit: 5 attempts / 15 min / IP per account, then exponential backoff; notify
  Prachi on lockout (she's the admin — a lockout notice is a compromise canary).
- Constant-time password comparison; timing-safe token compares everywhere
  (`crypto.subtle.timingSafeEqual` or equivalent).
- `Cache-Control: no-store` on all auth responses; never cache session-bearing pages.

---

## 3. Data scoping — family sees ONLY what she explicitly shares

### 3.1 Default-deny data model (P0)
- Every data table carries `owner_user_id NOT NULL`. There is **exactly one** data-access
  path in the Worker: `db.forUser(user, ...)` (or equivalent) that injects the scoping
  predicate. Raw unscoped queries are banned by convention and caught in review.
- Default rule: a family member sees **nothing** of anyone else's — not med lists, not
  todos, not "she has 4 meds". Zero cross-user reads without a grant.
- IDs are unguessable (UUIDs / NanoIDs), never sequential integers — no IDOR by
  incrementing.
- The **testing team** owns negative tests: authenticated-as-mom requests for Prachi's
  resources must return 403/404 (404 preferred — don't confirm existence), and this is
  asserted per endpoint, per gate.

### 3.2 Explicit sharing (the only exception)
Two mechanisms, both revocable by the data owner:
1. **Share grants** — row-level: `(grantee_id, resource_type, resource_id, scope,
   granted_by, expires_at)`. Scope is `read` or `read+write`; default `read`;
   **default expiry 30 days**, renewable. Example: mom gets read on "Meds" so she can
   check a dose; brother gets nothing unless granted.
2. **One-time report links** — for "send this visit summary to Dr. X": a signed,
   256-bit random token URL, **single-view or 24-hour expiry** (whichever first),
   access logged. Not a persistent grant; not guessable.
- Sharing UI always shows **what is shared, with whom, until when**, with one-tap
  revoke. Revocation is immediate (grant row deleted → queries stop matching).
- **Audit log** (append-only table): logins, password changes, invite redemptions,
  grant create/revoke/expire, report-link views, device revocations. Prachi can view
  it. Retain 1 year, then roll off.

### 3.3 What family accounts do NOT get
- No admin role, no invite generation, no viewing the audit log, no seeing that other
  family members exist beyond what is shared with them (no user enumeration via share
  dialogs — grantee picker only lists people who already share with you or are invited
  by the admin flow).

---

## 4. Health-data handling — D1 / R2 / transit

### 4.1 In transit
TLS everywhere, no exceptions: Cloudflare automatic TLS on the zone, **HTTPS redirect
+ HSTS** (`max-age=31536000; includeSubDomains; preload` once stable), TLS 1.2 minimum.
The Worker never fetches upstream over plain HTTP. `Referrer-Policy: no-referrer`;
sensitive pages get `Cache-Control: no-store`.

### 4.2 At rest — Cloudflare defaults and the gaps
- **Default:** D1 data is encrypted at rest by Cloudflare (platform-managed keys), and
  R2 objects are encrypted at rest server-side. This covers stolen-disk / decommissioned
  hardware. It does **not** cover: Cloudflare itself, D1 backups, or anyone with the
  Cloudflare API token.
- **Gap → recommendation (P0 decision needed): app-layer encryption for the most
  sensitive fields.** Encrypt at the Worker before writing: insurance member/group IDs,
  passport-card images' extracted text (if any), and **diary/Mind text** with AES-256-GCM
  via WebCrypto, key stored in **Workers Secrets** (never in git, never in D1), with a
  documented rotation story (key version column, decrypt-with-old/encrypt-with-new job).
  Rationale: these fields are identity-theft-grade (insurance IDs) or the most intimate
  (diary). Labs/meds stay access-controlled but plaintext-in-D1 so trends, search, and
  the interaction scanner can query them — document this tradeoff explicitly.
- **D1 access pattern:** the Worker (via its Cloudflare API token / binding) is the
  **only** reader/writer. The D1 HTTP API is never called from the browser; the API
  token lives in server-side secrets with minimum scope. No direct DB credentials exist
  anywhere a client could reach.
- **Backups & deletion honesty:** D1 automatic backups retain data after a user-visible
  delete (roughly 30 days, Cloudflare-managed). The app's delete must hard-delete the
  live row + R2 objects immediately and the privacy doc must state the backup window
  honestly — "deleted from the app immediately; removed from backups within ~30 days."

### 4.3 R2 photo handling (bottle pics, insurance card scans — P0)
- Bucket is **private**: no public `r2.dev` URL, no public bucket policy, ever.
- Access is **proxied through the Worker** (auth check → scope check → stream bytes) or
  via **presigned URLs with ≤15-minute expiry**. One auth path either way; never a
  long-lived public link.
- Object keys: `{owner_user_id}/{uuid}.{ext}` — **no PII in key names** (no
  `insurance-card-front.jpg` with her name; no timestamps that leak event dates).
- **EXIF strip on upload (P0):** phone photos carry GPS. The upload path strips all
  EXIF/metadata server-side before storing. Reject non-image magic bytes; MIME
  allowlist `image/jpeg`, `image/png`, `image/webp`; per-file cap (e.g. 10 MB).
- Insurance card scans are RED-class: they unlock medical identity theft. They get the
  step-up re-auth gate (§2.4) on view, and are never included in report links unless she
  explicitly attaches them.

### 4.4 Logging discipline
Structured logs with an **allowlist of fields**. Never log: request bodies, health
facts, tokens, passwords, insurance IDs, photo bytes. Log: endpoint, status code,
latency, authenticated user id (hashed or internal UUID only), error class. `wrangler
tail` in dev sees what prod logs — keep the allowlist in both. Error responses to
clients are generic; stack traces stay server-side.

### 4.5 Third parties & privacy posture
- No third-party analytics/trackers on health pages. If usage telemetry is ever added,
  it is self-hosted and documented.
- Integrations (Anthem FHIR, pharmacy SSO) use OAuth with **minimum scopes**; tokens
  stored encrypted (same app-layer key story as §4.2), refresh server-side only, and
  every connection is shown in a "Connected accounts" screen with one-tap disconnect.
- This is a personal app, not a HIPAA covered entity — but the bar here (audit log,
  encryption, access control, breach-minded defaults) is deliberately HIPAA-adjacent.
  (Not legal advice; a real compliance review is out of scope for Phase 1.)

---

## 5. API security

### 5.1 Default-deny auth
Every `/api/*` route requires authentication **except** an explicit allowlist:
`POST /api/auth/login`, `POST /api/auth/invite/redeem`, `GET /api/health` (liveness only,
no data), and the service ingest endpoints (§5.2, credential-gated). Auth is a single
middleware — routes opt out explicitly, never opt in. Unauthenticated → 401, wrong-user
→ 404 (not 403, to avoid confirming existence).

### 5.2 POST /api/digest — authenticated ingest (P0)
This endpoint writes summaries of her health chat into her DB. **An open ingest is not
just a privacy hole, it's a patient-safety hole:** forged entries (fake meds, fake
doses, fake "doctor said") would be rendered to her as her own data. Required:
- **Service credential:** 256-bit random bearer token, stored in Workers Secrets and in
  her secure vault only. `Authorization: Bearer <token>`, compared in constant time.
  Rotatable without deploy (versioned: `DIGEST_KEY_1`, accept N and N-1 during rotation).
- **Least privilege:** the digest key authorizes **only** `POST /api/digest` (write-only).
  Separate keys for the order-scan job and the memory-scan job, each scoped to its own
  endpoint. Service keys can never read health data and can never mint user sessions.
- **Never from browsers:** the endpoint rejects cookie/session auth; only the service
  bearer is accepted. CORS does not apply (same-origin + no browser callers).
- **Rate limit:** the job runs daily — cap at ~30 requests/hour per key. Anything above
  is abuse; alert her.
- **Validation:** strict schema (zod or equivalent), max body 256 KB, unknown fields
  rejected, timestamps sanity-checked, idempotency key required (job retries must not
  double-write diary entries).
- The coordinator must confirm the cron jobs store the key in the platform's secret
  store — it must never appear in a cron definition, a chat transcript, or a file.

### 5.3 Rate limiting (tiers)
| Surface | Limit | Notes |
|---|---|---|
| Login | 5 / 15 min / IP+account | then exponential backoff; lockout notifies her |
| Invite redeem | 10 / hour / IP | |
| `/api/digest` + job endpoints | 30 / hour / key | alert on exceed |
| Authed API (per session) | 100 / min | burst-tolerant, per-session not per-IP (shared IPs) |
| Photo upload | 20 / hour / user | + 10 MB/file cap |
Implement in-Worker (token bucket in D1/KV) **and** Cloudflare Rate Limiting rules on
the zone as a backstop. 429s return `Retry-After`, no data.

### 5.4 Input validation (every endpoint, no exceptions)
- Schema-validate all input (zod/valibot); reject unknown fields; coerce nothing silently.
- Global JSON body cap (1 MB); photo uploads separate path with own caps (§4.3).
- Rich-text notes (To-dos): **Markdown-only storage**, rendered through a sanitizer;
  no raw HTML stored, no `dangerouslySetInnerHTML` without an allowlist sanitizer.
- Dates/doses/phones validated at the edge; DB constraints (`CHECK`, `NOT NULL`,
  foreign keys) as the second layer — the testing team owns constraint tests.
- Output encoding: JSON responses; frontend escapes by default; CSP (below) as backup.

### 5.5 Headers, CORS, CSRF
- `Content-Security-Policy`: default-src 'self', no inline scripts/styles (nonce if a
  build tooling needs it), `frame-ancestors 'none'`, no third-party frames.
- `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`,
  `Referrer-Policy: no-referrer`, `Permissions-Policy` (camera/mic/geolocation locked
  down except where the photo capture needs camera — scoped to that route).
- CORS: same-origin only. No `Access-Control-Allow-Origin: *` anywhere.
- CSRF: `SameSite=Lax` cookies + synchronizer CSRF tokens on all mutating endpoints +
  `Origin`/`Referer` check in the API middleware. (Lax alone doesn't cover
  top-level-GET-triggered flows; do all three.)

---

## 6. Required fixes / decisions for the architects

**P0 — gate-blockers for Phase 2 (build is not shippable without these):**
1. Invite-only registration; no open signup route exists.
2. argon2id password hashing (benchmark on the real plan); generic auth errors.
3. Session design per §2.3: hashed-at-rest tokens, `__Host-` cookie flags, 30d sliding /
   90d absolute, rotation with reuse detection, Devices screen with per-device revoke +
   log-out-everywhere, password change revokes all.
4. Single scoped data-access path (`owner_user_id` on every table); UUIDs; negative
   403/404 tests per endpoint (with the testing team).
5. Share-grant model with default 30-day expiry + one-tap revoke + one-time report
   links (24h/single-view) + audit log.
6. R2: private bucket, Worker-proxied or ≤15-min presigned access, no PII in keys,
   EXIF strip, magic-byte + MIME validation.
7. `/api/digest` (+ order/memory jobs): per-job bearer keys, write-only scope,
   constant-time compare, rate limits, strict schema, idempotency keys.
8. Security-headers + CSRF + same-origin CORS middleware; default-deny API auth.
9. Login rate limiting with backoff + lockout notification to her.
10. App-level lock (PIN/biometric, 15-min idle default) + step-up re-auth on insurance
    card view, lab export, share creation, report send.
11. Logging allowlist — no health data, bodies, or tokens in logs.

**P1 — before family onboarding:**
12. TOTP 2FA, required for her admin account.
13. App-layer AES-GCM encryption for insurance IDs + diary text (§4.2 decision — needs
    her explicit ack; it complicates search).
14. "Connected accounts" screen with one-tap OAuth disconnect.
15. Passkeys/WebAuthn roadmap to replace passwords.

**Decisions needed (coordinator → parent → Prachi):**
- D1 sizing is fine, but **Cloudflare plan (Free vs Paid)** changes the hashing CPU
  budget and rate-limiting features — confirm before architects benchmark.
- App-layer encryption (§4.2): recommend yes for insurance IDs + diary; she must accept
  the search/reporting tradeoff.
- Confirm **invite-only onboarding** for mom/dad/brother (no self-signup link).
- Data retention: audit log 1 year ok? Deleted-data backup window (~30d) disclosed in
  the app's privacy note ok?

---

## 7. Merge checklist — coordinator runs this before EVERY push to GitHub

```bash
# 1. Sensitive paths must not be tracked
git ls-files | grep -Ei '\.(pem|key|p12|pfx|sqlite3?|db)$|seed\.local|\.env$|\.dev\.vars|test-results|playwright-report' \
  && { echo "FAIL: sensitive paths tracked"; exit 1; }

# 2. Secret-pattern scan over the branch diff
./scripts/check-secrets.sh main...HEAD || { echo "FAIL: secret scan"; exit 1; }

# 3. .gitignore protections intact (no removals)
git diff main...HEAD -- .gitignore | grep -E '^-' | grep -v '^---' \
  && { echo "FAIL: .gitignore lines removed — review"; exit 1; }

# 4. Migrations are schema-only (no personal-data INSERTs)
git diff main...HEAD -- db/ | grep -iE '^\+.*insert into' \
  && { echo "FAIL: INSERT in migration — human review required"; exit 1; }

# 5. wrangler config carries no secret VALUES (only refs/vars)
git diff main...HEAD -- wrangler.* | grep -iE '^\+.*(token|secret|password|api[_-]?key)\s*[:=]\s*["'\''][^"'\'']+["'\'']' \
  && { echo "FAIL: possible secret value in wrangler config"; exit 1; }

# 6. New binaries get a human look (photos of real cards must never ship)
git diff --stat main...HEAD | grep -E '\.(png|jpg|jpeg|webp|pdf)$' \
  && echo "NOTICE: binary files added — visually verify no real personal data"

# 7. Docs contain no real identifiers (spot-check the diff)
git diff main...HEAD -- docs/ README.md | grep -Ei '\b\d{3}[-.]?\d{3}[-.]?\d{4}\b' \
  && echo "NOTICE: phone-like number in docs — verify it's 555-01xx"

echo "checks done"
```

Plus, on the **first** push to public GitHub only: full-history secret scan (§1.6.4).
Plus: confirm GitHub repo settings — push protection on, secret scanning on, private
vulnerability reporting on.

---

## 8. Residual risks (accepted, documented)
- Cloudflare as processor holds D1/R2 data and TLS-terminates traffic; app-layer
  encryption (§4.2) narrows but doesn't remove this.
- Backups retain "deleted" data ~30 days — disclosed, not hidden.
- A compromised agent-infrastructure host holding a job key could write forged digest
  entries until the key is rotated — mitigated by per-job keys, tight rate limits, and
  the audit log; rotation runbook required.
- Physical device access defeats most software controls — the app-level lock (§2.4) is
  mitigation, not cure; her iPhone's own device passcode/biometrics remain the real
  perimeter.

---

*Next review: re-run against the Worker + schema + auth implementation at the Phase 2
gate. Any P0 miss blocks the gate.*
