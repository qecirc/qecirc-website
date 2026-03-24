-- Migration: Multi-format circuit bodies + external tool links
-- Moves circuit body/format into a separate table to support multiple formats.
-- Adds crumble_url and quirk_url columns for external tool links.

PRAGMA foreign_keys = OFF;

-- 1. Create circuit_bodies table
CREATE TABLE circuit_bodies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  circuit_id INTEGER NOT NULL REFERENCES circuits(id) ON DELETE CASCADE,
  format TEXT NOT NULL,
  body TEXT NOT NULL,
  UNIQUE(circuit_id, format)
);

CREATE INDEX idx_circuit_bodies_circuit ON circuit_bodies(circuit_id);

-- 2. Migrate existing body/format data (skip any rows with NULL body/format)
INSERT INTO circuit_bodies (circuit_id, format, body)
SELECT id, format, body FROM circuits
WHERE body IS NOT NULL AND format IS NOT NULL;

-- 3. Rebuild circuits table without body/format, adding external link columns
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
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(code_id, slug)
);

INSERT INTO circuits_new (id, code_id, name, slug, description, source, gate_count, depth, qubit_count, created_at)
SELECT id, code_id, name, slug, description, source, gate_count, depth, qubit_count, created_at
FROM circuits;

DROP TABLE circuits;
ALTER TABLE circuits_new RENAME TO circuits;

CREATE INDEX idx_circuits_code ON circuits(code_id);

PRAGMA foreign_keys = ON;
