CREATE TABLE IF NOT EXISTS codes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  description TEXT,
  n INTEGER NOT NULL,
  k INTEGER NOT NULL,
  d INTEGER,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS functionalities (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code_id INTEGER NOT NULL REFERENCES codes(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  slug TEXT NOT NULL,
  description TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(code_id, slug)
);

CREATE TABLE IF NOT EXISTS circuits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  functionality_id INTEGER NOT NULL REFERENCES functionalities(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  slug TEXT NOT NULL,
  source TEXT NOT NULL,
  format TEXT NOT NULL DEFAULT 'stim',
  body TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(functionality_id, slug)
);

CREATE TABLE IF NOT EXISTS tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS taggings (
  tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  taggable_id INTEGER NOT NULL,
  taggable_type TEXT NOT NULL CHECK(taggable_type IN ('code', 'functionality', 'circuit')),
  PRIMARY KEY (tag_id, taggable_id, taggable_type)
);

CREATE INDEX idx_taggings_target ON taggings(taggable_type, taggable_id);
CREATE INDEX idx_functionalities_code ON functionalities(code_id);
CREATE INDEX idx_circuits_functionality ON circuits(functionality_id);
