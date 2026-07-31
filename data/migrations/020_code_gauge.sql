-- Subsystem codes: the gauge group, and the qubit count it implies.
--
-- `codes.h` keeps meaning the *stabilizer* group for every code, so validators,
-- dedup, the CSS split and the matrices view are untouched. A subsystem code
-- additionally has a gauge group — the operators a decoder may measure, whose
-- outcomes are not all deterministic — and the difference between the two is
-- `gauge_qubits` real qubits that carry no information and are not corrected.
--
-- Without this the library read k off the stabilizer group alone, as
-- n - rank(h), which counts gauge qubits as logical ones: Bacon-Shor [[9,1,3]]
-- came out [[9,5,3]] and SHYPS [[49,9,4]] came out [[49,25,4]]. Both columns are
-- NULL for a stabilizer code, where the two groups coincide.

ALTER TABLE codes ADD COLUMN gauge TEXT;
ALTER TABLE codes ADD COLUMN gauge_qubits INTEGER;
