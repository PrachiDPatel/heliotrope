# Heliotrope — Local development

Prereqs: Node 18+ and npm. That's it — no Docker, no local Postgres.

## First run

```bash
cd worker
npm install          # installs wrangler (devDependency, gitignored via node_modules/)
npx wrangler dev     # → http://localhost:8787
```

`wrangler dev` spins up the Worker with **ephemeral local D1 and R2** — the
`DB` and `PHOTOS` bindings work out of the box with empty local state. Nothing
touches production.

Smoke test in a second terminal:

```bash
curl -s localhost:8787/api/health
# {"ok":true,"app":"heliotrope","phase":1}

# everything else needs a session → 401 without one
curl -s localhost:8787/api/meds -w '\n%{http_code}\n'
# {"error":"not implemented","phase":2,"route":"GET /api/meds"} ... with a session
# {"error":"unauthorized"} ... without one

# digest ingest needs the service secret
curl -s -X POST localhost:8787/api/digest \
  -H 'Content-Type: application/json' \
  -d '{"title":"t","date":"2026-09-29","summary_markdown":"hi"}' -w '\n%{http_code}\n'
# {"error":"unauthorized"}  401  (no secret configured — correct)
```

## Local secrets (`.dev.vars`)

Secrets are **never** committed (`.dev.vars` is gitignored). For local dev, create
`worker/.dev.vars`:

```bash
# worker/.dev.vars — gitignored, local only
DIGEST_INGEST_SECRET=dev-only-secret-change-me
```

`wrangler dev` loads it automatically. Production secrets are set with
`wrangler secret put DIGEST_INGEST_SECRET` by the coordinator at deploy time.

## Local D1

The ephemeral local DB resets when `wrangler dev` restarts — fine for Phase 1.
To apply the schema to it:

```bash
npx wrangler d1 execute DB --local --file=../db/schema.sql
```

To create a local test user (hash the password with the same PBKDF2 scheme —
use `node -e` with `worker/src/auth.js`'s `hashPassword`, or wait for the data
team's seed script; do **not** invent a different scheme):

```bash
node --input-type=module -e "
import { hashPassword } from './src/auth.js';
console.log(await hashPassword('pick-a-dev-password'));"
# then INSERT INTO users (username, password_hash, display_name, role)
# VALUES ('prachi','<hash>','Prachi','owner');
```

Reminder: this repo is public. Dev passwords are throwaway; the real seed script
(`scripts/seed.local/`, gitignored, data-team owned) is the only thing that ever
touches real data, and it never gets committed.

## Persisted local state (optional)

If you want the local DB to survive restarts:

```bash
npx wrangler dev --persist-to=.wrangler-state
```

`.wrangler/` is gitignored.

## Deploy (coordinator only)

Team branches do **not** deploy. When the coordinator merges to main:

```bash
npx wrangler d1 create heliotrope-db        # once; paste database_id into wrangler.toml
npx wrangler r2 bucket create heliotrope-photos  # once
npx wrangler d1 execute heliotrope-db --file=db/schema.sql   # remote
npx wrangler secret put DIGEST_INGEST_SECRET
npx wrangler deploy
```

Per her standing rule for the sleep tracker, deploys happen on her word —
local-first until she approves.
