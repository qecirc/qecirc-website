-- Drop the stored Crumble links. Breaking: both columns go.
--
-- A Crumble URL is a pure string transform of the body it shows — join the
-- lines with `;`, abbreviate three instruction names, write spaces as `_` — so
-- storing it duplicated the circuit in a second, lossy encoding. It cost half a
-- megabyte across the library, it went stale whenever a body was regenerated
-- (76 of 725 links pointed at a body the page no longer displayed), and because
-- the string got unwieldy it was blanked past ~40 qubits, leaving the widest
-- circuits — the ones a layout view helps most — with no link at all.
--
-- `crumbleHref` in src/lib/stim-format.ts now derives it where it is shown: the
-- detail page server-renders it from the body it already has, and code pages
-- fill it in when the row's bodies are lazy-loaded. The Detectors switch picks
-- between the annotated body and that body minus its readout epilogue, which is
-- what `crumble_url_annotated` was for. The width gate is gone with the storage.
ALTER TABLE circuits DROP COLUMN crumble_url;
ALTER TABLE circuits DROP COLUMN crumble_url_annotated;
