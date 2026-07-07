-- Stabiliser weight for flag-gadget circuits (the number of data qubits the
-- gadget's stabiliser acts on). NULL for ordinary circuits that belong to a
-- code — weight is only meaningful for the standalone gadgets, where it powers
-- a numeric range filter shown just on that listing.
ALTER TABLE circuits ADD COLUMN weight INTEGER;
