-- Migration 012: Drop CSS-derived columns (hx, hz, logical_x, logical_z and
-- their original_* siblings). Symplectic h + logical from migration 011 are
-- now the sole source of truth; the CSS view is derived in TS at render time
-- via splitHToCss().

ALTER TABLE codes DROP COLUMN hx;
ALTER TABLE codes DROP COLUMN hz;
ALTER TABLE codes DROP COLUMN logical_x;
ALTER TABLE codes DROP COLUMN logical_z;

ALTER TABLE circuit_originals DROP COLUMN original_hx;
ALTER TABLE circuit_originals DROP COLUMN original_hz;
ALTER TABLE circuit_originals DROP COLUMN original_logical_x;
ALTER TABLE circuit_originals DROP COLUMN original_logical_z;
