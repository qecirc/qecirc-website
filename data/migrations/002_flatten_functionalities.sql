-- Migration: Flatten functionalities into circuit tags
-- Circuits now reference codes directly. Functionality names become circuit tags.
-- Adds gate_count, depth, qubit_count metric columns to circuits.

-- Disable FK checks for table rebuilds (DROP + RENAME pattern)
PRAGMA foreign_keys = OFF;

-- 1. Create new circuits table with correct schema
CREATE TABLE circuits_new (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code_id INTEGER NOT NULL REFERENCES codes(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  slug TEXT NOT NULL,
  description TEXT,
  source TEXT NOT NULL,
  format TEXT NOT NULL DEFAULT 'stim',
  body TEXT NOT NULL,
  gate_count INTEGER,
  depth INTEGER,
  qubit_count INTEGER,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(code_id, slug)
);

-- 2. Copy data, resolving code_id through functionalities
-- Carry over functionality description as circuit description
INSERT INTO circuits_new (id, code_id, name, slug, description, source, format, body, created_at)
SELECT c.id, f.code_id, c.name, c.slug, f.description, c.source, c.format, c.body, c.created_at
FROM circuits c
JOIN functionalities f ON c.functionality_id = f.id;

-- 3. Convert functionality names to circuit tags
-- Insert functionality names as tags (ignore if already exists)
INSERT OR IGNORE INTO tags (name)
SELECT LOWER(f.name) FROM functionalities f;

-- Create taggings linking each circuit to its functionality-name tag
INSERT OR IGNORE INTO taggings (tag_id, taggable_id, taggable_type)
SELECT t.id, c.id, 'circuit'
FROM circuits c
JOIN functionalities f ON c.functionality_id = f.id
JOIN tags t ON t.name = LOWER(f.name);

-- 4. Drop old circuits table and rename new one
DROP TABLE circuits;
ALTER TABLE circuits_new RENAME TO circuits;

-- 5. Rebuild taggings to remove 'functionality' type and clean up
-- First delete all functionality taggings
DELETE FROM taggings WHERE taggable_type = 'functionality';

-- Rebuild taggings table with updated CHECK constraint
CREATE TABLE taggings_new (
  tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  taggable_id INTEGER NOT NULL,
  taggable_type TEXT NOT NULL CHECK(taggable_type IN ('code', 'circuit')),
  PRIMARY KEY (tag_id, taggable_id, taggable_type)
);

INSERT INTO taggings_new SELECT * FROM taggings;
DROP TABLE taggings;
ALTER TABLE taggings_new RENAME TO taggings;

-- 6. Drop functionalities table
DROP TABLE functionalities;

-- 7. Recreate indexes
CREATE INDEX idx_taggings_target ON taggings(taggable_type, taggable_id);
CREATE INDEX idx_circuits_code ON circuits(code_id);

-- Re-enable FK checks
PRAGMA foreign_keys = ON;
