# Heliotrope

My all-in-one health app. I was tired of having my meds in one place, my labs
in another, my doctors' numbers nowhere, and no single spot that actually knew
what was going on with my body — so I'm building it. Same family as my sleep
tracker.

## What's in it

- **Today** — what I need to take or do right now, nothing else
- **Body** — tap a body system, see what's going on with it
- **Meds** — every med with a photo of the bottle, a plain-language schedule,
  and refill reminders that tell me who to call
- **Labs** — all my bloodwork in one place, with trends I can send to a doctor
- **Care team** — doctors, pharmacy, insurance card, one tap away
- **To-dos** — the endless find-a-doctor list, with priorities and notes
- **Nourish** — food, such as it is
- **Cycle / Stress / Skin / Weight** — the body upkeep tabs
- **Mind** — patterns from my days and diary, not diagnoses
- **Orders** — health stuff I ordered, tracked from my inbox
- **Reports** — one-tap visit summaries for doctors

## Stack

- Frontend: iPhone-first web app
- Backend: Cloudflare Worker + D1 (photos in R2)

## Privacy

This repo is public, so zero personal data lives here — no meds, no labs, no
insurance details, nothing. All of that goes straight into my own database
through a local seed script that never gets committed. Schema, code, and docs
only.

## Layout

| Path | What it is |
|---|---|
| `apps/web` | the frontend |
| `worker` | the Cloudflare Worker API |
| `db` | D1 schema + migrations (no personal data, ever) |
| `docs` | architecture notes, design tokens |
| `assets` | icon, illustrations, ambient art |
| `scripts` | helpers (seed scripts live outside git — see Privacy) |
