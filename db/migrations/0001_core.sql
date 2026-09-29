-- 0001_core.sql — users, meds, med_wisdom_cards, doctors, pharmacy, insurance_docs
PRAGMA foreign_keys = ON;

CREATE TABLE users (
  id            TEXT PRIMARY KEY,
  display_name  TEXT NOT NULL,
  relationship  TEXT NOT NULL DEFAULT 'self'
                CHECK (relationship IN ('self','spouse','partner','child','parent','sibling','other')),
  dob           TEXT,
  color         TEXT,
  notes         TEXT,
  created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE meds (
  id                TEXT PRIMARY KEY,
  user_id           TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name              TEXT NOT NULL,
  generic_name      TEXT,
  strength          TEXT,
  form              TEXT,
  directions        TEXT,
  schedule_json     TEXT,
  status            TEXT NOT NULL DEFAULT 'current'
                    CHECK (status IN ('current','incoming','on_hand','inactive','discontinued')),
  prescribed_by     TEXT,
  indication        TEXT,
  pharmacy_id       TEXT REFERENCES pharmacy(id) ON DELETE SET NULL,
  refill_lead_days  INTEGER,
  last_refill_date  TEXT,
  photo_r2_key      TEXT,
  notes             TEXT,
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  updated_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE med_wisdom_cards (
  id         TEXT PRIMARY KEY,
  med_id     TEXT REFERENCES meds(id) ON DELETE SET NULL,
  title      TEXT NOT NULL,
  body       TEXT NOT NULL,
  category   TEXT NOT NULL DEFAULT 'tip'
             CHECK (category IN ('interaction','timing','food','side_effect','tip','experience')),
  source     TEXT,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE TABLE doctors (
  id         TEXT PRIMARY KEY,
  name       TEXT NOT NULL,
  specialty  TEXT NOT NULL,
  role       TEXT,
  practice   TEXT,
  phone      TEXT,
  address    TEXT,
  portal_url TEXT,
  status     TEXT NOT NULL DEFAULT 'current'
             CHECK (status IN ('current','seeking','former','to_find')),
  last_visit TEXT,
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
  label                TEXT NOT NULL,
  insurer              TEXT NOT NULL,
  plan_name            TEXT,
  member_id            TEXT,
  group_number         TEXT,
  plan_code            TEXT,
  rx_bin               TEXT,
  rx_pcn               TEXT,
  rx_grp               TEXT,
  effective_date       TEXT,
  copay_primary        TEXT,
  copay_specialist     TEXT,
  copay_er             TEXT,
  copay_urgent         TEXT,
  rx_retail_tiers      TEXT,
  rx_mail_tiers        TEXT,
  deductible_ind       TEXT,
  deductible_fam       TEXT,
  coinsurance          TEXT,
  employer             TEXT,
  member_services_phone TEXT,
  r2_key_front         TEXT,
  r2_key_back          TEXT,
  notes                TEXT,
  created_at           TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE INDEX idx_meds_user      ON meds(user_id);
CREATE INDEX idx_meds_status    ON meds(status);
CREATE INDEX idx_wisdom_med     ON med_wisdom_cards(med_id);
CREATE INDEX idx_doctors_status ON doctors(status);
CREATE INDEX idx_insurance_user  ON insurance_docs(user_id);
