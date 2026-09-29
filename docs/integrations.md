# Integrations — research & implementation plan (Phase 1)

How Heliotrope connects to the rest of her world: her scale, her inbox,
her diary app, her insurance. Each section: what was verified, the exact
design, what she has to do, and what's feasible now vs later.

Status as of 2026-09-29.

---

## 1. Weight — Fit Index Bluetooth scale

### Verdict: the path is Fit Index app → Apple Health → Heliotrope. It works, but nothing is flowing yet.

**Why not direct Bluetooth:** iOS Safari has no Web Bluetooth. There is no way
for an iPhone web app to talk to a BLE scale. Any design that needs Bluetooth
in the browser is a dead end on her phone — full stop.

**What the vendor says:** Fit Index publishes an official "Apple Health Kit
Setting Guide" ([fit-index.com](https://fit-index.com/de/pages/004)) confirming
the Fit Index app syncs measurements into Apple Health. In the iPhone Health
app the Fit Index app shows up as **"Gennec"** (their publisher name) — that's
the name she should look for, not "Fit Index".

**What comes across:** Weight, Body Fat %, BMI, and Lean Body Mass. That gives
us more than a weight line — body-composition trends basically free.

**Her setup steps (iPhone, ~2 minutes):**
1. Health app → profile picture (top right) → **Apps** → **Gennec**
2. Turn on all categories (weight, body fat, BMI, lean body mass)
3. Step on the scale with her iPhone nearby; the Fit Index app syncs the
   reading into Health. The scale has onboard memory — weigh-ins taken without
   the phone nearby backfill the next time the app connects.

**Read path into Heliotrope:** two layers.
- *Agent side (already working):* `health-cli query metrics --provider healthkit
  --fields body_mass_average,body_fat_percentage,bmi`. The fields exist in her
  sync schema, but as of 2026-09-29 **none have been observed in her synced
  data** — i.e. the Fit Index → Health link is not enabled yet. Once she does
  the two-minute setup above, readings will appear here.
- *App side (the real gap):* Apple HealthKit has no cloud API and no OAuth —
  it's device-only. A web app can't read it, and the health-cli connector is
  agent infrastructure, not something the Heliotrope web app can call. So:
  - **Phase 1:** an iOS Shortcut she runs (or an Automation) that reads today's
    weight/body-fat from Health and POSTs it to the Heliotrope Worker API.
    Free, no App Store, she keeps control. This is the recommended path.
  - **Phase 2 (later):** a native wrapper (Capacitor/React Native) with the
    HealthKit entitlement, reading directly on-device.

**Blockers:** none technical. She just has to enable the sync (her action) and
approve the Shortcut approach.

---

## 2. Gmail order scan → Orders tab

### Verdict: buildable now with the Gmail skill. Amazon supplements/health gear is fully covered; pharmacy is NOT in Gmail.

**What her inbox actually shows (verified read-only, metadata only, 2026-09-29):**

- Order confirmations come from `auto-confirm@amazon.com` with subjects like
  **"Ordered 1 item: Supplements"** and **"Ordered 1 item: Health Care"** —
  the category after the colon is the product category, which is a reliable
  health filter. (A recent supplements order — the "Supplements" one is
  hers, presumably the incoming magnesium/l-theanine.)
- Shipping updates come from `shipment-tracking@amazon.com` with subjects like
  "Shipped 1 item: Health Care", "Out for delivery 1 item: Health Care".
- **Pharmacy:** zero emails from Publix in the last 90 days. Publix pharmacy
  notifies by text/app, not email. The Gmail scan will never see her
  prescriptions or refills — those stay manual entry (or a future Publix-app
  angle). Document this so the Orders tab doesn't silently promise coverage it
  can't deliver.

**Query patterns (Gmail search syntax):**

| What | Query |
|---|---|
| Health orders | `from:auto-confirm@amazon.com subject:("Health Care" OR "Supplements")` |
| Health shipments | `from:shipment-tracking@amazon.com subject:("Health Care" OR "Supplements")` |
| Daily scan | either query + `newer_than:2d` |

**Extraction:** for candidates, read the thread (`users threads get`) — an
order confirmation, its shipped notice, and its delivered notice all live in
one thread. Pull the Amazon order number (`###-#######-#######` from the body),
item name(s), price, and status stage. Prefer transactional mail over promo;
the two senders above are the transactional ones.

**Dedupe:** natural key = **Gmail threadId** (stable, groups the whole
order lifecycle); secondary key = Amazon order number for cross-thread safety.
Idempotent upsert into D1 — re-running the scan never duplicates.

**Architecture:**
- **Phase 1:** a scheduled agent cron runs the Gmail skill (`+triage` to find
  candidates, reads for details), then POSTs structured orders to the
  Heliotrope Worker `/api/orders/import`. Cost budget: `+triage` runs
  ~5+20N units; keep `--max` small, run searches sequentially, widen dates
  only if a scan comes up short.
- **Phase 2 (later):** Worker-side Gmail access via Google OAuth (client ID/
  secret in Worker secrets) so the scan lives entirely in the Worker cron.
  Needs her one-time OAuth consent — she already approved the Gmail connection
  for the agent, so this is a familiar ask.

**Proposed D1 `orders` table:**
`id (threadId), source, order_number, item_name, category, price, status
(ordered|shipped|out_for_delivery|delivered), ordered_at, shipped_at,
delivered_at, raw_json, updated_at`

**Her action needed:** none. Gmail is already connected. Optional: confirm she
also wants "Beauty"/"Personal Care" categories included, or keep it strictly
Health Care + Supplements.

---

## 3. Prionaria diary import → Mind tab

### Verdict: buildable now, but only with her explicit consent and a restricted service account.

**What Prionaria actually is (verified):** there is no public repo named
"Prionaria". Prionaria is the *app's* name; the public repo is
**PrachiDPatel/petrova-log** — the Project Hail Mary two-person letter app
she built for herself and Orion. The public demo (petrova-log.pages.dev) runs
with `DEMO_MODE=true`, so visitors' writes never reach the database — her real
letters with Orion live in the private Firestore behind the same project and
are untouched by the demo.

**Data model (read from the repo source):**
- Firestore project: `petrova-log`
- Collection: **`letters`**, document ID = `{date}_{uid}`
- Fields: `from`, `to`, `fromEmail`, `fromUid`, `date`, `content`,
  `salutation`, `signoffWord`, `signoffName`, `wordCount`,
  `mood` (`ecstatic | happy | eh | sad | devastated | null`),
  `createdAt`, `editableUntil`, `lastEdited`
- Also a `users` collection (push tokens — not needed for import)

**Import design:**
- Auth: a Firebase **service account restricted to Firestore read**, created
  by her in the Firebase console (project petrova-log → Service accounts →
  generate key). The key JSON goes into Worker secrets — **never committed**,
  the repo is public.
- Pull: list `letters` ordered by `date` desc; incremental sync keyed on
  `lastEdited`/`createdAt` cursor; a Worker cron or one-time agent backfill +
  nightly delta.
- Store: D1 `diary_entries(id = Firestore doc id, date, author, mood,
  word_count, content, imported_at)` — doc ID is the natural dedupe key,
  upsert on it.
- The Mind tab consumes mood + dates + word counts for pattern views; full
  text stays available for her own reading and for pattern summaries.

> **TONE CONSTRAINT — read this before touching this data.** Her letters
> contain dramatic writing about her turbulent relationship with her boyfriend.
> All analysis stays about **her patterns** — her words, her moods, her days —
> with a **gentle, non-pathologizing tone**. Never diagnose the relationship,
> never evaluate him, never label what's happening between them. Quote her own
> words rather than summarizing with loaded framing. The Mind tab is
> "patterns from my days and diary, not diagnoses" — hold that line.

**Her actions needed:** (1) explicit yes to importing diary content into
Heliotrope — this is her private writing, and per her rules nothing gets saved
without her approval; (2) create the restricted service account (~5 min in
Firebase console) and hand it over through the secure flow.

**Blockers:** her consent; the service-account key.

---

## 4. Insurance linking — Anthem FHIR Patient Access API

### Verdict: real and standards-based, but production access is a "weeks of paperwork" timeline. Sandbox now, production later.

**What's real:** Under CMS-9115-F (Interoperability and Patient Access final
rule), US payers must offer a FHIR Patient Access API. Anthem (now Elevance
Health) runs one — documented at anthem.com/developer:
- **FHIR R4 4.0.1**, CARIN IG for Blue Button STU 2.1.0, US Core 6.1.0,
  **SMART App Launch 2.2.0**
- Production bases are brand-specific:
  `https://totalview.healthos.elevancehealth.com/resources/registered/<Brand>/api/v1/fhir`
  (brands include Anthem Blue Cross Blue Shield, Wellpoint, etc. — her exact
  brand slug needs confirming against her plan)
- Sandbox with synthetic data, open on developer self-registration — this is
  where we build and test
- Older publicly-inspectable surface: `https://patient360c.anthem.com/P360Member/api/fhir`
  (FHIR DSTU2) with an anonymous discovery document at
  `.../identityserver/.well-known/openid-configuration`

**OAuth flow (SMART on FHIR, member-authorized):**
1. Register our app at anthem.com/developers/request-anthem-io → get
   `client_id`/`client_secret` (stored in Worker secrets)
2. Send her to Anthem's authorization endpoint with PKCE (S256),
   scopes like `patient/Claim.read patient/Coverage.read patient/Condition.read`
   — narrow scopes only; the consent screen shows her exactly what we ask for
3. She signs in with her **own Anthem member login** (Sydney Health / anthem.com)
   and approves — we never see or touch her password
4. Exchange the code at the token endpoint; `fhirUser` + `patientidentifier`
   claims on the id token identify her; then `GET /Claim?patient=...`,
   `/Coverage`, `/Condition`, `/Observation`, `/MedicationOrder`,
   `/Immunization`, `/AllergyIntolerance`

**What data is available:** up to five years of medical, dental, vision and
pharmacy claims plus clinical data (conditions, observations, meds,
immunizations, allergies). **Prior-auth data is NOT there yet** — committed by
2027-01-01 under CMS-0057-F but absent today.

**Exactly what we'd ask her for, and when:**
- *Now (sandbox dev):* nothing from her. We build against synthetic data.
- *Later (production go-live):* one login + consent at Anthem's screen using
  her member credentials; re-consent every **90 days** (Anthem tokens expire —
  schedule the re-consent nudge, don't silently refresh). She can revoke
  anytime (revocation + end-session endpoints exist).
- *Clarifications needed before go-live:* which brand slug matches her plan
  (she's on her **parent's** Anthem BCBS plan — need her to confirm she has her
  own Sydney Health login as a dependent; covered dependents get their own
  logins), and which narrow scopes she approves.

**What's aspirational:** 
- SMART-on-FHIR for **provider** apps (EHR launch, `launch/encounter` context
  inside a doctor's system) — not our architecture. Heliotrope is
  patient-facing; we use standalone launch. Provider-flavor is out of scope.
- Any claim that we'd get real-time data or prior-auths — not available today.

**Known gaps (per third-party API profile, 2026-09):** Anthem publishes no
rate limits, no changelog, no status page, no error reference. Production app
approval "can take several weeks" — plan the timeline accordingly.

---

## 5. SSO inventory — what can we actually offer her?

| Integration | Real OAuth/SSO? | What the ask looks like |
|---|---|---|
| **Gmail** | ✅ Yes — connected now | Already done via connector; Phase 2 Worker-side OAuth would be a one-click consent |
| **Anthem / Elevance** | ✅ Yes — SMART on FHIR | Later: her member login + consent at Anthem's screen, 90-day re-consent cadence. Production app approval takes weeks first. |
| **Apple Health** | ❌ No — device-synced, no login exists | Nothing to offer; she enables the Fit Index→Health sync on her iPhone; data enters Heliotrope via the iOS Shortcut (Phase 1) |
| **Fit Index scale app** | ❌ No public API or SSO | Phone-app only; the integration *is* the Apple Health sync — no credentials involved |
| **Prionaria (Firestore)** | ⚠️ Service account, not SSO | She creates a read-restricted service account in Firebase console; no password sharing, no OAuth screen |
| **Amazon orders** | ❌ No order-history API | Covered by the Gmail scan instead |

**She approved being asked for SSO connections** — so the Gmail (Phase 2) and
Anthem (production) asks are pre-cleared in principle; ask at the moment each
is actually needed, not before.

---

## Summary: feasible now vs later

**Now (Phase 1, no blockers beyond her actions):**
- Weight: her 2-minute Health-app setup + iOS Shortcut → Worker API
- Gmail order scan: agent cron → Worker `/api/orders/import`
- Prionaria import: pending her consent + service-account key

**Later (real, but gated):**
- Anthem claims/coverage: sandbox integration now; production after app
  approval (weeks) + her member login/consent + 90-day re-consent rhythm
- Native HealthKit in-app: needs a native wrapper app (Phase 2)
- Worker-side Gmail OAuth: one consent screen away, do it when the agent cron
  becomes annoying

**Not possible / not planned:**
- Direct Bluetooth from the web app (iOS won't allow it)
- Pharmacy via Gmail (Publix doesn't email pharmacy notifications)
- Provider-flavor SMART-on-FHIR (wrong architecture for a patient app)
