-- Migration: Symplectic stabilizer matrices
-- Adds h (always populated) and logical (always populated) columns to codes,
-- and the matching original_h, original_logical columns to circuit_originals.
-- For CSS codes the legacy hx/hz/logical_x/logical_z fields remain populated
-- as a convenient view. For non-CSS codes only h and logical are populated.

ALTER TABLE codes ADD COLUMN h TEXT;
ALTER TABLE codes ADD COLUMN logical TEXT;

ALTER TABLE circuit_originals ADD COLUMN original_h TEXT;
ALTER TABLE circuit_originals ADD COLUMN original_logical TEXT;
