-- Migration: Compact code properties + check matrices
-- Removes description, adds zoo_url, hx, hz, logical_x, logical_z columns.

PRAGMA foreign_keys = OFF;

CREATE TABLE codes_new (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  n INTEGER NOT NULL,
  k INTEGER NOT NULL,
  d INTEGER,
  zoo_url TEXT,
  hx TEXT,
  hz TEXT,
  logical_x TEXT,
  logical_z TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT INTO codes_new (id, name, slug, n, k, d, created_at)
SELECT id, name, slug, n, k, d, created_at
FROM codes;

DROP TABLE codes;
ALTER TABLE codes_new RENAME TO codes;

PRAGMA foreign_keys = ON;
