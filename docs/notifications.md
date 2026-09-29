# Heliotrope — Notifications design (Phase 1)

Owner: notifications team (team/notifications). Status: design + implementation sketch.

Philosophy, from her: **one calm place**. Notifications must be quiet, relevant,
and actionable — never nagging. Every notification earns its interruption:
it carries who to call, where to go, or what to do, in one tap.

Physician-reviewer note (gate requirement): every notification is
informational-only. Copy frames stock estimates as estimates ("looks like
you may be running low"), never advice, and every med alert routes to a
human (pharmacist/doctor) rather than telling her what to do.

Privacy: all personal data (pill counts, appointment details, phone numbers)
is seeded via the gitignored local seed script — never committed. This doc
covers schema/code/contracts only.

---

## 1. Med refill low-stock alerts

### Flow

1. **Capture** — In the Meds tab, she photographs the bottle (R2, `med_bottle_photos/`).
   On the same screen she enters: pill count in the bottle (manual entry —
   Phase 1; OCR of label counts is explicitly out of scope), dose per day
   (from the plain-language schedule she already set), and dispense date.
2. **Estimate** — `days_remaining = pills_on_hand / pills_per_day`.
   The app never assumes she takes it perfectly; she can also log "took dose"
   taps, which the estimator uses to recompute. `doses_remaining` counts down
   from logged takes; if she never logs, the estimator falls back to the
   calendar estimate.
3. **Watch** — the worker cron evaluates every med daily (see §5) and emits
   notifications when a med crosses its threshold:
   - **"Running low"** (normal) — `days_remaining <= refill_lead_days`.
   - **"Almost out"** (high) — `days_remaining <= urgent_days` (default 3).
   - **"Out of stock"** (critical) — `days_remaining <= 0`.
4. **Act** — the notification and the med card carry a **TAP-TO-CALL**
   button that opens `tel:` to the *right* person, chosen by med type:
   - **Prescription with refills remaining** → pharmacy (Laurel Springs Publix).
   - **Prescription, no refills remaining / new script needed** → the
     prescribing doctor (e.g. modafinil → her psychiatrist).
   - **OTC / supplement** (iron, vitamin D, magnesium, l-theanine,
     multivitamin, Opill) → no call; the button becomes **"Reorder"**, which
     opens the last-purchase link (Orders tab / Gmail-detected order).
5. **Close the loop** — after the call/reorder she taps "Refill ordered" on
   the med card; the app starts a *pending-refill* timer using
   `typical_fulfillment_days` and nudges once if the refill hasn't arrived.

### Per-med data needed

Each med record needs (some already exist in the Meds tab; these fields are
the notification contract):

| Field | Example (modafinil) | Why |
|---|---|---|
| `dose_schedule` | "1/4 tablet after breakfast…" | pills_per_day → estimate |
| `pills_on_hand` + `counted_at` | 20, 2026-09-29 | anchor for the estimate |
| `pills_per_day` | 1 | derived from schedule |
| `med_kind` | `rx_refillable` \| `rx_new_script` \| `otc` | who the call button dials |
| `rx_refills_remaining` | 2 | flips `rx_refillable` → `rx_new_script` at 0 |
| `pharmacy_id` / `prescriber_id` | FK → care-team records | tap-to-call target |
| `refill_lead_days` | 10 | warn-before threshold |
| `urgent_days` | 3 | "almost out" threshold |
| `typical_fulfillment_days` | 2 | pending-refill watchdog |
| `last_reorder_url` | (orders tab ref) | OTC reorder button |
| `stock_snoozed_until` | nullable | manual override, see §4 |

### Thresholds (defaults; per-med adjustable)

- Prescription meds: `refill_lead_days = 10` — refills can need prior auth,
  doctor sign-off, or pharmacy lead time; she needs the runway.
- OTC / supplements: `refill_lead_days = 7` — shipping is the only lag.
- Controlled-titration meds (modafinil is titrated per her prescriber's plan):
  use the *prescription* threshold even if refills remain, because a dose
  change mid-titration can invalidate the estimate — the med card always
  shows "estimate, confirm at pickup".

Escalation is one-way until acknowledged: `low → almost out → out`, each
level pushes at most once. Crossing back up (after she logs a refill)
resets the state machine.

---

## 2. Appointment reminders

Source: the To-dos tab (doctor-finding list) and any confirmed appointment
records — the to-do team owns the data; notifications only consume it.

### Required appointment data

- `when` (datetime, her local tz), `provider_name`, `specialty`
- `address` (full street address) → renders a **Maps** link (Apple Maps on
  her iPhone: `maps://` / `https://maps.apple.com/?q=…`)
- `phone` → **tap-to-call** button
- `visit_type`: `confirmed` | `needs_booking` (from the find-a-doctor list)
- `prep_notes` (fasting? insurance card? labs to bring?) — shown in the
  reminder, not in the push.

### Reminder cadence

- **7 days before** (normal): "Book / confirm" — only fires for
  `needs_booking` items with high priority (new PCP, endocrinologist,
  cardiologist…); gentle, one push.
- **Day before** (high): "Tomorrow: Dr. X, 10:30 AM — 123 Main St. [Call]
  [Directions]". Prep notes shown in-app.
- **Morning of** (high, short): "Today at 10:30 — Dr. X. [Directions]".
- **After** (low, in-app only): "How did it go?" → one-tap visit-summary
  prompt feeding the Reports tab. Never pushed; quiet hours don't matter,
  but calm does.

Missed appointments (datetime passed, no "attended" log) generate one
in-app nudge: "Reschedule Dr. X?" with the call button — pushed at most
once, at normal priority, next morning.

---

## 3. Delivery

### 3a. Web Push (primary)

Reuse the sleep tracker's proven pattern verbatim — don't reinvent it:

- **Frontend**: a service worker (`sw.js`) with a `push` event listener that
  renders the notification (title, body, actions — e.g. Call / Directions /
  Dismiss) and a `notificationclick` handler that deep-links into the app
  (`/meds#modafinil`, `/todos#endo`) or opens `tel:` directly.
- **Subscription**: `PushManager.subscribe()` with the app's VAPID public
  key fetched from `GET /api/push/vapid-key`; POST the subscription to
  `/api/push/subscribe`; DELETE on `/api/push/unsubscribe`.
- **Worker**: VAPID private key as a P-256 JWK in a wrangler *secret*
  (never in code). The existing RFC 8291 aes128gcm + VAPID signing module
  from the sleep tracker ports over unchanged — only the sender identity
  (`sub: mailto:heliotrope@…`) changes.
- **Failure hygiene** (same as sleep tracker): on HTTP 404/410 from the
  push service, delete the subscription row — dead endpoints must not
  accumulate.

**iOS constraint (must tell her at onboarding):** Web Push on iPhone
requires iOS 16.4+ **and** the app added to the Home Screen (PWA install).
Push *will not work* from Safari alone. The app's push-permission screen
must detect `navigator.standalone` / `display-mode: standalone` and, if
not installed, show "Add to Home Screen to get refill & appointment
reminders" with the iOS share-sheet steps — not a raw browser permission
prompt that silently does nothing. Until she installs, fall back to the
in-app notification center (§3b) + an onboarding checklist item that stays
visible.

### 3b. In-app notification center

A calm **bell icon** in the header with a count badge (cap the badge at
"9+"; never show 47). Tapping it opens a panel:

- Sections by recency, not by type: Today / Earlier. No tab-bar clutter.
- Each item: one-line title, one-line detail, contextual actions inline
  (Call pharmacy · Directions · Mark done · Snooze 1 day). Actions don't
  require opening the item.
- Read state: tapping an item or its action marks it read. "Mark all read"
  at the top.
- Low-priority items (digest, "how did it go?") live **only** here — they
  never push.
- Design: matches her taste — dense but calm, distinct cards, tertiary
  palette, headers bigger than body text. The art/UI team owns the tokens;
  this doc owns the content contract.

### 3c. Payload contract

Push payloads are small and dumb — the service worker enriches from cache:

```json
{
  "id": "notif_abc123",
  "kind": "med_low_stock" | "med_almost_out" | "med_out" |
          "appt_reminder" | "appt_today" | "refill_overdue" | "digest",
  "priority": "critical" | "high" | "normal" | "low",
  "title": "Modafinil — running low",
  "body": "About 4 days left. Tap to call Laurel Springs Publix.",
  "deep_link": "/meds#modafinil",
  "actions": [
    { "id": "call", "label": "Call pharmacy", "href": "tel:+1…" },
    { "id": "open", "label": "View med", "href": "/meds#modafinil" }
  ]
}
```

`tel:` hrefs come from care-team records (pharmacy/doctor phones), never
hardcoded. `actions[].href` may be `tel:` — the SW `notificationclick`
handler opens it directly so she doesn't have to unlock → open app →
find the number.

---

## 4. Quiet hours + relevance (calm by design)

She said it herself: the app is "one calm place." The notification system
is a guest in her day. Rules:

### Priority levels

| Level | What | Behavior |
|---|---|---|
| **critical** | med at 0 days | push immediately, defers to end of quiet hours — except propranolol (physician whitelist: bypasses, activates if prescribed) |
| **high** | almost-out meds, appointment tomorrow/today | push, respects quiet hours (deferred to next open window) |
| **normal** | low-stock warning, 7-day appt nudge, refill-overdue | push, batched into windows, quiet-hours aware |
| **low** | digest, "how did it go?", snoozed items | in-app only, never pushed |

### Quiet hours

- Default **10:00 PM – 8:00 AM** local, configurable per device.
- Her schedule is irregular (sleep disorder — she sometimes sleeps 20h
  spans), so quiet hours are a *preference*, not a sleep detector. A later
  phase could sync to her sleep-tracker data; Phase 1 must not pretend to
  know when she's asleep.
- Standing rule: **supply-critical alerts defer to the end of quiet hours by default.** A 3 AM "you're out of meds" push is alarming with zero recourse — no pharmacy or prescriber is reachable, so she can't act on it. An alarm she can't act on is a waking alarm, not an actionable one. **Exception (physician whitelist): propranolol** supply-critical alerts bypass quiet hours — abrupt interruption is itself a clinical event (rebound chest pain, arrhythmia, ischemia risk), and "never stop suddenly" is the card's #1 rule. This is a standing rule that activates if/when a prescriber starts it; she is not taking propranolol now. No other current or incoming med justifies a bypass: modafinil has no abrupt-stop syndrome (a missed day = a missed day), hydroxyzine is as-needed, and the supplements are daily-habit where hours of alert delay change nothing.
  **coalesced**: if three normal items queued overnight, she gets ONE push
  ("3 things from overnight") that opens the notification center, not three.

### Batching & dedupe

- **One escalation per med per level.** A med that crosses "low" pushes
  once; it doesn't re-push daily until it crosses "almost out".
- **Daily cap**: max 3 pushes/day for normal priority. Overflow rolls into
  the low-priority digest (in-app only).
- **Morning digest** (optional, default ON, low priority, in-app): one calm
  card — "Today: 3 meds due, 1 appointment Thursday, iron running low."
  This is the default home for non-urgent info so pushes stay rare.
- **Snooze**: any notification can be snoozed (1 day / 1 week). Snoozing a
  med-low-stock alert sets `stock_snoozed_until` — the estimator keeps
  counting; snooze only mutes, never lies.
- **Relevance filter**: a med she's marked "not taking" (hydroxyzine,
  propranolol) never generates stock alerts. A med with no
  `pills_on_hand` anchor generates ONE gentle in-app nudge ("Add a bottle
  count to enable refill alerts") — never a push.

### Relevance over completeness

- No streaks, no "you missed a dose!" shaming. Missed-dose language is
  neutral and informational ("Dose not logged"), per her taste.
- Every push must pass the test: *can she act on this in under 10 seconds
  from the lock screen?* (Call / Directions / View.) If not, it's in-app
  only.
- Tone: short, plain, warm. No exclamation marks. No "URGENT". Example:
  "[Med name] — about 4 days left. Tap to call the pharmacy."

---

## 5. What the worker needs (cron + API)

### Cron triggers (`wrangler.toml`)

```toml
[triggers]
crons = [
  "*/15 * * * *",   # notification sweep (quiet-hours + priority aware)
  "0 7 * * *",      # daily refill/appointment evaluation (her morning-ish)
  "0 9 * * *",      # pending-refill watchdog + missed-appt nudge
]
```

Behavior:
- **15-min sweep** (`scheduled` handler): pulls due notifications from the
  `notifications` table (`send_at <= now`, not sent, priority respected),
  applies quiet-hours deferral per device, sends via the VAPID push module,
  marks sent. Dedupe: a `(kind, med_id|appt_id, level)` row exists → skip.
- **7 AM evaluation**: recompute `days_remaining` for all active meds
  from anchors + logged takes; insert notification rows for new threshold
  crossings; scan appointments for 7-day/1-day/today reminders; insert rows
  with `send_at` set appropriately (respecting quiet hours at insert).
- **9 AM watchdog**: refills marked "ordered" older than
  `typical_fulfillment_days + 2` with no new bottle count → one normal
  nudge ("Refill hasn't shown up yet?"); appointments in the past with no
  outcome → one reschedule nudge.

### API surface (architects team to implement)

- `GET /api/push/vapid-key` → `{ publicKey }`
- `POST /api/push/subscribe` / `DELETE /api/push/unsubscribe`
- `GET /api/notifications` (inbox list, paginated) / `POST /api/notifications/:id/read` / `POST /api/notifications/read-all`
- `POST /api/notifications/:id/snooze` → `{ until }`
- `POST /api/meds/:id/stock` → `{ pills_on_hand }` (new bottle count resets the estimator)
- `POST /api/meds/:id/refill-ordered` (starts pending-refill timer)

### Proposed D1 tables (data team owns the DDL; this is the contract)

```sql
CREATE TABLE push_subscriptions (
  endpoint TEXT PRIMARY KEY,
  p256dh TEXT NOT NULL, auth TEXT NOT NULL,
  device_label TEXT, quiet_start TEXT DEFAULT '22:00', quiet_end TEXT DEFAULT '08:00',
  created_at TEXT NOT NULL
);
CREATE TABLE notifications (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL, priority TEXT NOT NULL,
  title TEXT NOT NULL, body TEXT NOT NULL,
  deep_link TEXT, actions_json TEXT,
  med_id TEXT, appointment_id TEXT,
  send_at TEXT NOT NULL, sent_at TEXT, read_at TEXT, snoozed_until TEXT,
  dedupe_key TEXT UNIQUE, created_at TEXT NOT NULL
);
-- meds table gains (data team): pills_on_hand, counted_at, pills_per_day,
-- med_kind, rx_refills_remaining, pharmacy_id, prescriber_id,
-- refill_lead_days, urgent_days, typical_fulfillment_days,
-- last_reorder_url, stock_snoozed_until, stock_state
```

The worker never stores phone numbers in notification rows — `tel:` hrefs
resolve at send time from care-team records (single source of truth).

---

## 6. Blockers & open questions

1. **Pharmacy phone/address** — Laurel Springs Publix contact details are
   TBD (care-team/data teams or a lookup; seeded personally, not in git).
   Tap-to-call ships blocked until this is seeded.
2. **Prescriber → med mapping** — modafinil's prescriber (psychiatrist) and
   any other rx prescribers must be entered in the care-team directory;
   notifications need the FK.
3. **Home Screen install** — iOS push is impossible without it. Onboarding
   must teach the install; the in-app center is the fallback. Worth a
   coordinator-level check: does she already have the sleep tracker
   installed to Home Screen? (Same education applies to both apps.)
4. **Phase 2, not Phase 1**: pill-count OCR from the bottle photo; quiet
   hours synced to her actual sleep data; family-member notifications
   (security team: family accounts see only what she shares — notifications
   must respect the same scoping).
5. **Review board gates**: physician reviewer must approve all notification
   copy and the "estimate" framing before Phase 1 closes; psychologist
   reviewer checks the Mind-adjacent tone ("how did it go?" nudge).

## Decisions log

- Thresholds default to 10 days (rx) / 7 days (OTC); escalate low → almost
  out (3d) → out, one push per level.
- tap-to-call routes by `med_kind`: pharmacy (refills left) / prescriber
  (new script) / reorder link (OTC). Never hardcoded numbers.
- Quiet hours default 10 PM–8 AM, configurable; critical (0 days) defers to the end of quiet hours (see §4) — except propranolol supply-critical alerts (physician whitelist),
  everything else defers and coalesces.
- Push payloads are dumb; the SW enriches from cache. VAPID module ports
  unchanged from the sleep tracker; only the sender identity changes.
- Low-priority items never push — in-app notification center only.
- Snooze mutes; it never falsifies the estimate.
