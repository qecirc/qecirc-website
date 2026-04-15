-- Migration: Original circuit data (pre-canonicalization)
-- Stores original STIM body and check matrices as submitted by contributors.

CREATE TABLE circuit_originals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  circuit_id INTEGER NOT NULL UNIQUE REFERENCES circuits(id) ON DELETE CASCADE,
  original_stim TEXT NOT NULL,
  original_hx TEXT NOT NULL,
  original_hz TEXT NOT NULL,
  original_logical_x TEXT NOT NULL,
  original_logical_z TEXT NOT NULL
);
