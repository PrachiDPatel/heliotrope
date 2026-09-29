-- 0005_auth.sql — auth/session/share/digest tables (architects' design, merged Phase 1).
-- Users table itself is created in 0001_core.sql; auth columns are added here.
-- NO personal data in this repo, ever. Schema only.

-- Auth columns on users (nullable: family accounts can exist without a login).
-- (UNIQUE via separate index: SQLite cannot ADD a UNIQUE column.)
ALTER TABLE users ADD COLUMN username      TEXT;
ALTER TABLE users ADD COLUMN password_hash TEXT;
ALTER TABLE users ADD COLUMN role          TEXT NOT NULL DEFAULT 'family'
  CHECK (role IN ('owner','family'));
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Sessions: server-side opaque tokens. The cookie holds the raw token;
-- only its SHA-256 hash is stored here (a leaked DB dump can't be replayed).
CREATE TABLE sessions (
  token_hash   TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at   INTEGER NOT NULL,   -- epoch ms
  last_seen_at INTEGER NOT NULL,   -- epoch ms, for sliding expiry
  expires_at   INTEGER NOT NULL    -- epoch ms; 90d rolling "cached login"
);
CREATE INDEX idx_sessions_user ON sessions(user_id);

-- Shares: the owner grants a family member read access to her data.
-- Default-deny: family members see ONLY what has an unrevoked grant row.
CREATE TABLE shares (
  id         TEXT PRIMARY KEY,
  owner_id   TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  viewer_id  TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  scope      TEXT NOT NULL DEFAULT 'summary' CHECK (scope IN ('summary','full')),
  granted_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  revoked_at TEXT,                                 -- null = active
  UNIQUE (owner_id, viewer_id)
);

-- Digests: daily chat-summary payloads filed by the scheduled ingest job
-- (POST /api/digest, bearer service secret). Service-owned, append-only.
CREATE TABLE digests (
  id                TEXT PRIMARY KEY,
  title             TEXT NOT NULL,
  digest_date       TEXT NOT NULL,                   -- YYYY-MM-DD
  summary_markdown  TEXT NOT NULL,
  health_facts_json TEXT NOT NULL DEFAULT '[]',      -- [{fact, category, confidence}]
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  UNIQUE (digest_date, title)
);
CREATE INDEX idx_digests_date ON digests(digest_date);
