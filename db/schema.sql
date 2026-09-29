-- Heliotrope D1 schema (full, current) — merged Phase 1: data-team domain model
-- + architects' auth/session/share/digest tables. Conventions:
-- - TEXT UUID primary keys everywhere (no sequential IDs).
-- - Every personal-data table carries user_id -> users(id) for per-user scoping;
--   the auth middleware attaches readable user IDs for WHERE user_id IN (...) filtering.
-- - Times stored as ISO-8601 UTC text; epoch millis for session internals.
-- - Migrations are additive and numbered; never edit a shipped migration.
-- NO personal data in this repo, ever. Schema only.
-- This file is the consolidated view. Apply migrations in db/migrations/ instead;
-- schema.sql is regenerated from them and kept in sync.
-- NO personal data in this repo, ever. Schema only.

PRAGMA foreign_keys = ON;

-- ============ core ============

CREATE TABLE users (
  id            TEXT PRIMARY KEY,           -- UUID, no sequential IDs
  display_name  TEXT NOT NULL,
  relationship  TEXT NOT NULL DEFAULT 'self'
                CHECK (relationship IN ('self','spouse','partner','child','parent','sibling','other')),
  dob           TEXT,                       -- ISO date, nullable
  color         TEXT,                       -- UI accent for family accounts
  notes         TEXT,
  created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  -- auth columns (added by 0005_auth.sql; nullable = family account w/o login)
  username      TEXT UNIQUE,                -- lowercase login name
  password_hash TEXT,                       -- pbkdf2-sha256$iter$salt$hash
  role          TEXT NOT NULL DEFAULT 'family' CHECK (role IN ('owner','family'))
);

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
CREATE UNIQUE INDEX idx_users_username ON users(username);

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

CREATE TABLE meds (
  id                TEXT PRIMARY KEY,
  user_id           TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name              TEXT NOT NULL,          -- display name
  generic_name      TEXT,                   -- e.g. "norgestrel"
  strength          TEXT,                   -- e.g. "0.075 mg"; NULL when unknown
  form              TEXT,                   -- tablet / capsule / gummy / liquid ...
  directions        TEXT,                   -- plain-language how/when, prescriber plan
  schedule_json     TEXT,                   -- JSON: {"anchor":"wake","times":[...],"with_food":true}
  status            TEXT NOT NULL DEFAULT 'current'
                    CHECK (status IN ('current','incoming','on_hand','inactive','discontinued')),
  prescribed_by     TEXT,                   -- free text prescriber name
  indication        TEXT,                   -- why she takes it
  pharmacy_id       TEXT REFERENCES pharmacy(id) ON DELETE SET NULL,
  refill_lead_days  INTEGER,
  last_refill_date  TEXT,
  photo_r2_key      TEXT,                   -- bottle photo in R2
  notes             TEXT,
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  updated_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE med_wisdom_cards (
  id         TEXT PRIMARY KEY,
  med_id     TEXT REFERENCES meds(id) ON DELETE SET NULL,
  title      TEXT NOT NULL,
  body       TEXT NOT NULL,                 -- plain-language card text
  category   TEXT NOT NULL DEFAULT 'tip'
             CHECK (category IN ('interaction','timing','food','side_effect','tip','experience')),
  source     TEXT,                          -- prescriber note / own experience / label
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE doctors (
  id         TEXT PRIMARY KEY,
  name       TEXT NOT NULL,
  specialty  TEXT NOT NULL,
  role       TEXT,                          -- pcp / psychiatrist / therapist / ...
  practice   TEXT,
  phone      TEXT,
  address    TEXT,
  portal_url TEXT,
  status     TEXT NOT NULL DEFAULT 'current'
             CHECK (status IN ('current','seeking','former','to_find')),
  last_visit TEXT,                          -- ISO date
  notes      TEXT,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE pharmacy (
  id      TEXT PRIMARY KEY,
  name    TEXT NOT NULL,
  address TEXT,
  phone   TEXT,
  fax     TEXT,
  hours   TEXT,
  notes   TEXT
);

CREATE TABLE insurance_docs (
  id                   TEXT PRIMARY KEY,
  user_id              TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  label                TEXT NOT NULL,       -- e.g. "Primary insurance"
  insurer              TEXT NOT NULL,
  plan_name            TEXT,
  member_id            TEXT,
  group_number         TEXT,
  plan_code            TEXT,
  rx_bin               TEXT,
  rx_pcn               TEXT,
  rx_grp               TEXT,
  effective_date       TEXT,                -- ISO date
  copay_primary        TEXT,
  copay_specialist     TEXT,
  copay_er             TEXT,
  copay_urgent         TEXT,
  rx_retail_tiers      TEXT,                -- e.g. "$10/$25/$40"
  rx_mail_tiers        TEXT,
  deductible_ind       TEXT,
  deductible_fam       TEXT,
  coinsurance          TEXT,
  employer             TEXT,
  member_services_phone TEXT,
  r2_key_front         TEXT,                -- card scan in R2
  r2_key_back          TEXT,
  notes                TEXT,
  created_at           TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- ============ labs + todos ============

CREATE TABLE labs (
  id             TEXT PRIMARY KEY,
  user_id        TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  collected_date TEXT NOT NULL,             -- ISO date
  ordered_by     TEXT,
  performed_by   TEXT,
  note           TEXT,
  created_at     TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- one row per analyte; panel_name groups rows (CMP, Hemoglobin A1c, Iron panel...)
CREATE TABLE lab_panels (
  id         TEXT PRIMARY KEY,
  lab_id     TEXT NOT NULL REFERENCES labs(id) ON DELETE CASCADE,
  panel_name TEXT NOT NULL,
  analyte    TEXT NOT NULL,
  value_num  REAL,
  value_text TEXT,                          -- when value isn't numeric
  unit       TEXT,
  ref_low    REAL,
  ref_high   REAL,
  flag       TEXT NOT NULL DEFAULT 'normal'
             CHECK (flag IN ('low','normal','high','critical')),
  notes      TEXT
);

CREATE TABLE todos (
  id                TEXT PRIMARY KEY,
  user_id           TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title             TEXT NOT NULL,
  detail            TEXT,
  category          TEXT NOT NULL DEFAULT 'other'
                    CHECK (category IN ('doctor','appointment','refill','lab','insurance','other')),
  priority          INTEGER NOT NULL DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
  due_date          TEXT,
  status            TEXT NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open','in_progress','done','snoozed')),
  completed_at      TEXT,
  related_doctor_id TEXT REFERENCES doctors(id) ON DELETE SET NULL,
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  updated_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- ============ wellness ============

CREATE TABLE diet_entries (
  id           TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  logged_at    TEXT NOT NULL,               -- ISO datetime
  meal_type    TEXT CHECK (meal_type IN ('breakfast','lunch','dinner','snack')),
  description  TEXT,
  calories     INTEGER,
  protein_g    REAL,
  photo_r2_key TEXT,
  notes        TEXT
);

CREATE TABLE cycle_entries (
  id             TEXT PRIMARY KEY,
  user_id        TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date           TEXT NOT NULL,             -- ISO date
  flow           TEXT NOT NULL DEFAULT 'none'
                 CHECK (flow IN ('none','spotting','light','medium','heavy')),
  symptoms_json  TEXT,                      -- JSON array
  notes          TEXT,
  UNIQUE (user_id, date)
);

CREATE TABLE stress_entries (
  id        TEXT PRIMARY KEY,
  user_id   TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  logged_at TEXT NOT NULL,
  level     INTEGER NOT NULL CHECK (level BETWEEN 1 AND 10),
  triggers  TEXT,
  notes     TEXT
);

CREATE TABLE skincare_routine (
  id         TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  step_order INTEGER NOT NULL,
  name       TEXT NOT NULL,
  product    TEXT,
  frequency  TEXT CHECK (frequency IN ('am','pm','both','weekly','as_needed')),
  active     INTEGER NOT NULL DEFAULT 1,
  notes      TEXT
);

CREATE TABLE bodycare_routine (
  id         TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  step_order INTEGER NOT NULL,
  name       TEXT NOT NULL,
  product    TEXT,
  frequency  TEXT CHECK (frequency IN ('am','pm','both','weekly','as_needed')),
  active     INTEGER NOT NULL DEFAULT 1,
  notes      TEXT
);

CREATE TABLE weight_entries (
  id           TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date         TEXT NOT NULL,               -- ISO date
  weight_lb    REAL NOT NULL,
  body_fat_pct REAL,
  notes        TEXT,
  UNIQUE (user_id, date)
);

CREATE TABLE mind_entries (
  id           TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date         TEXT NOT NULL,               -- ISO date
  mood         INTEGER CHECK (mood BETWEEN 1 AND 5),
  energy       INTEGER CHECK (energy BETWEEN 1 AND 5),
  anxiety      INTEGER CHECK (anxiety BETWEEN 1 AND 5),
  focus        INTEGER CHECK (focus BETWEEN 1 AND 5),
  sleep_quality INTEGER CHECK (sleep_quality BETWEEN 1 AND 5),
  notes        TEXT,                        -- patterns, not diagnoses
  UNIQUE (user_id, date)
);

CREATE TABLE diary_entries (
  id         TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date       TEXT NOT NULL,                 -- ISO date
  title      TEXT,
  body       TEXT NOT NULL,
  tags_json  TEXT,                          -- JSON array
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- ============ orders / reports / digests ============

CREATE TABLE orders (
  id           TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  item         TEXT NOT NULL,
  vendor       TEXT,
  order_number TEXT,
  order_date   TEXT,
  status       TEXT NOT NULL DEFAULT 'ordered'
               CHECK (status IN ('ordered','shipped','delivered','cancelled')),
  expected_date TEXT,
  tracking_url TEXT,
  cost_cents   INTEGER,
  notes        TEXT
);

CREATE TABLE reports (
  id         TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title      TEXT NOT NULL,
  kind       TEXT NOT NULL DEFAULT 'visit_summary'
             CHECK (kind IN ('visit_summary','lab_summary','custom')),
  doctor_id  TEXT REFERENCES doctors(id) ON DELETE SET NULL,
  visit_date TEXT,
  summary    TEXT NOT NULL,                 -- one-tap doctor-ready summary
  r2_key     TEXT,                          -- PDF/photo in R2
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- NOTE: digests live in the table defined above (auth section), written by
-- POST /api/digest. No separate chat_digests table.

-- ============ indexes ============

CREATE INDEX idx_meds_user       ON meds(user_id);
CREATE INDEX idx_meds_status     ON meds(status);
CREATE INDEX idx_wisdom_med      ON med_wisdom_cards(med_id);
CREATE INDEX idx_doctors_status  ON doctors(status);
CREATE INDEX idx_insurance_user   ON insurance_docs(user_id);
CREATE INDEX idx_labs_user_date  ON labs(user_id, collected_date);
CREATE INDEX idx_panels_lab      ON lab_panels(lab_id);
CREATE INDEX idx_todos_user      ON todos(user_id, status);
CREATE INDEX idx_todos_priority  ON todos(priority);
CREATE INDEX idx_diet_user_time  ON diet_entries(user_id, logged_at);
CREATE INDEX idx_cycle_user_date ON cycle_entries(user_id, date);
CREATE INDEX idx_stress_user_time ON stress_entries(user_id, logged_at);
CREATE INDEX idx_skincare_user   ON skincare_routine(user_id, step_order);
CREATE INDEX idx_bodycare_user   ON bodycare_routine(user_id, step_order);
CREATE INDEX idx_weight_user_date ON weight_entries(user_id, date);
CREATE INDEX idx_mind_user_date  ON mind_entries(user_id, date);
CREATE INDEX idx_diary_user_date ON diary_entries(user_id, date);
CREATE INDEX idx_orders_user     ON orders(user_id, status);
CREATE INDEX idx_reports_user    ON reports(user_id, visit_date);
