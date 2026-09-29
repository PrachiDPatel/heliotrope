-- 0002_labs_todos.sql — labs, lab_panels, todos
PRAGMA foreign_keys = ON;

CREATE TABLE labs (
  id             TEXT PRIMARY KEY,
  user_id        TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  collected_date TEXT NOT NULL,
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
  value_text TEXT,
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

CREATE INDEX idx_labs_user_date ON labs(user_id, collected_date);
CREATE INDEX idx_panels_lab     ON lab_panels(lab_id);
CREATE INDEX idx_todos_user     ON todos(user_id, status);
CREATE INDEX idx_todos_priority ON todos(priority);
