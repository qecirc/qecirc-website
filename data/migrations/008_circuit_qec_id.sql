-- qec_id is always populated from YAML via db:create; use db:create to rebuild.
ALTER TABLE circuits ADD COLUMN qec_id INTEGER NOT NULL DEFAULT 0;
-- Unique index enforces no duplicate IDs at the DB level.
CREATE UNIQUE INDEX idx_circuits_qec_id ON circuits(qec_id);
