-- 0003_wellness.sql — diet, cycle, stress, skincare, bodycare, weight, mind, diary
PRAGMA foreign_keys = ON;

CREATE TABLE diet_entries (
  id           TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  logged_at    TEXT NOT NULL,
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
  date           TEXT NOT NULL,
  flow           TEXT NOT NULL DEFAULT 'none'
                 CHECK (flow IN ('none','spotting','light','medium','heavy')),
  symptoms_json  TEXT,
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
  date         TEXT NOT NULL,
  weight_lb    REAL NOT NULL,
  body_fat_pct REAL,
  notes        TEXT,
  UNIQUE (user_id, date)
);

CREATE TABLE mind_entries (
  id            TEXT PRIMARY KEY,
  user_id       TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date          TEXT NOT NULL,
  mood          INTEGER CHECK (mood BETWEEN 1 AND 5),
  energy        INTEGER CHECK (energy BETWEEN 1 AND 5),
  anxiety       INTEGER CHECK (anxiety BETWEEN 1 AND 5),
  focus         INTEGER CHECK (focus BETWEEN 1 AND 5),
  sleep_quality INTEGER CHECK (sleep_quality BETWEEN 1 AND 5),
  notes         TEXT,
  UNIQUE (user_id, date)
);

CREATE TABLE diary_entries (
  id         TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  date       TEXT NOT NULL,
  title      TEXT,
  body       TEXT NOT NULL,
  tags_json  TEXT,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

CREATE INDEX idx_diet_user_time   ON diet_entries(user_id, logged_at);
CREATE INDEX idx_cycle_user_date  ON cycle_entries(user_id, date);
CREATE INDEX idx_stress_user_time ON stress_entries(user_id, logged_at);
CREATE INDEX idx_skincare_user    ON skincare_routine(user_id, step_order);
CREATE INDEX idx_bodycare_user    ON bodycare_routine(user_id, step_order);
CREATE INDEX idx_weight_user_date ON weight_entries(user_id, date);
CREATE INDEX idx_mind_user_date    ON mind_entries(user_id, date);
CREATE INDEX idx_diary_user_date   ON diary_entries(user_id, date);
