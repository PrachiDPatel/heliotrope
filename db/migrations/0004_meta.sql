-- 0004_meta.sql — orders, reports, chat_digests
PRAGMA foreign_keys = ON;

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
  summary    TEXT NOT NULL,
  r2_key     TEXT,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- chat_digests was superseded by the digests table (0005_auth.sql), which the
-- implemented POST /api/digest endpoint writes to. Single table, no duplication.

CREATE INDEX idx_orders_user  ON orders(user_id, status);
CREATE INDEX idx_reports_user ON reports(user_id, visit_date);
