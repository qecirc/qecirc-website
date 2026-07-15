-- Crumble link for the `stim-annotated` body, which carries the reset prologue,
-- the terminal readout, and the derived DETECTOR/OBSERVABLE_INCLUDE annotations.
--
-- A second column rather than a second row: `crumble_url` belongs to the
-- canonical unitary body, and the two links are shown by the same UI control
-- (the Detectors toggle) swapping between them. NULL when the circuit has no
-- annotated body, or when it exceeds the width gate that already blanks
-- `crumble_url` (past ~40 qubits the URL is megabytes and unusable).
ALTER TABLE circuits ADD COLUMN crumble_url_annotated TEXT;
