-- Migration: Add tools table, link circuits to tools, extend taggings

PRAGMA foreign_keys = OFF;

-- 1. Create tools table
CREATE TABLE tools (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  description TEXT,
  homepage_url TEXT,
  github_url TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 2. Add tool_id to circuits (table rebuild)
CREATE TABLE circuits_new (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code_id INTEGER NOT NULL REFERENCES codes(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  slug TEXT NOT NULL,
  description TEXT,
  source TEXT NOT NULL,
  gate_count INTEGER,
  depth INTEGER,
  qubit_count INTEGER,
  crumble_url TEXT,
  quirk_url TEXT,
  tool_id INTEGER REFERENCES tools(id),
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(code_id, slug)
);

INSERT INTO circuits_new (id, code_id, name, slug, description, source, gate_count, depth, qubit_count, crumble_url, quirk_url, created_at)
SELECT id, code_id, name, slug, description, source, gate_count, depth, qubit_count, crumble_url, quirk_url, created_at
FROM circuits;

DROP TABLE circuits;
ALTER TABLE circuits_new RENAME TO circuits;
CREATE INDEX idx_circuits_code ON circuits(code_id);

-- 3. Extend taggings to support 'tool' type
CREATE TABLE taggings_new (
  tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  taggable_id INTEGER NOT NULL,
  taggable_type TEXT NOT NULL CHECK(taggable_type IN ('code', 'circuit', 'tool')),
  PRIMARY KEY (tag_id, taggable_id, taggable_type)
);

INSERT INTO taggings_new SELECT * FROM taggings;
DROP TABLE taggings;
ALTER TABLE taggings_new RENAME TO taggings;
CREATE INDEX idx_taggings_target ON taggings(taggable_type, taggable_id);

PRAGMA foreign_keys = ON;
