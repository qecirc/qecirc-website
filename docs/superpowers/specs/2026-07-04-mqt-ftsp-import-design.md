# MQT QECC FT State-Prep Import — Design

**Date:** 2026-07-04
**Status:** Approved design, pending implementation

## Goal

Import the published fault-tolerant state-preparation circuits from the MQT QECC
repository (`munich-quantum-toolkit/qecc`, MIT) into the QECirc library:

- `scripts/ft_stateprep/eval/circuits` — non-deterministic FT prep,
  arXiv:2408.11894 (PRX Quantum 6, 020330)
- `scripts/ft_stateprep/eval_det/{circuits,results.csv}` — deterministic FT prep,
  arXiv:2501.05527

Both use flag-qubit verification to detect dangerous propagated errors; the first
post-selects (discard & retry on any −1 outcome), the second measures
outcome-dependent second-round stabilizers and applies a classically-selected
Pauli correction.

## Layout (follows the rlftqc pattern)

New `data-imports/mqt-ftsp/` containing `rebuild_all.py` (dataset-specific
driver) and `README.md`. The dataset is a clone of the `qecc` repo sitting
_beside_ the website repo (`../qecc`). All reusable logic stays in
`scripts.add_circuit` (`import_state_prep`: fitting, dedup, originals capture,
notes/tags). Driver supports classify-only (default) and `--write` modes and
prints a per-code report including deferred/failed circuits.

## Part 1: `eval/` — 53 `.stim` files (51 imported, 2 defective deferred)

- **Files:** 53 `.stim` (each has an identical `.qasm` sibling; the `.stim` is
  imported). Naming: `{zero|plus}_{ft|non_ft}_{prep}[_{verify}].stim` with
  `prep ∈ {opt, heuristic}`, `verify ∈ {opt, heuristic, naive, mixed}`.
- **Content:** `non_ft` = bare H+CX encoders on n qubits; `ft` = prep + inline
  flag-qubit verification measurements (`MR`, ancillas at indices ≥ n, reused).
  No noise, detectors, or classical control — post-selection is the protocol.
- **Codes (all 10 already stored):** steane‑code [[7,1,3]], shor‑code [[9,1,3]],
  rotated‑surface‑code‑d‑3 [[9,1,3]], rotated‑surface‑code‑d‑5 [[25,1,5]],
  15‑7‑3 Hamming [[15,7,3]], tetrahedral‑code [[15,1,3]], carbon‑code [[12,2,4]],
  17‑1‑5 [[17,1,5]], 19‑1‑5 [[19,1,5]], 31‑1‑7 [[31,1,7]].
- **Fitting (empirically verified 2026‑07‑04 against the cloned repo):**
  - `steane` (10/10) and `shor` (10/10) fit the stored codes under **identity**.
  - `hamming`, `cc_4_8_8`, `cc_6_6_6`, `cc_4_8_8_d7` resolve via **self-dual
    canonical-hash dedup** (derived hash == stored `canonical_hash`, verified).
  - `rotated_surface_d3` (n=9) resolves via the existing **exhaustive search**.
  - `tetrahedral`, `carbon`, `rotated_surface_d5` fit under **none** of the
    existing paths (identity fails, not self-dual-dedupable, n > search budget,
    and rlftqc's known σs do not apply — MQT uses a third labeling). These are
    fitted with the **new structural permutation finder** (below).
- **Two defective published files are deferred, not repaired** (decision):
  - `rotated_surface_d3/zero_non_ft_heuristic.stim` — truncated mid-verification
    (odd CX target count; the `.qasm` sibling is also broken: verification CXs
    onto an undeclared `z_anc` register).
  - `hamming/plus_ft_heuristic_opt.stim` — parses, but the prepared state
    violates one Z-stabilizer of [[15,7,3]] while all 9 sibling files pass.
  - Both are listed in the driver report and README; worth reporting upstream
    to mqt‑qecc. Net: **51 of 53** eval circuits import.

- **Metadata:** source `https://arxiv.org/abs/2408.11894`, tool `mqt-qecc`,
  tags `state-preparation`, `ft`/`non-ft`, `prep:<method>`,
  `verification:<method>` (ft only), plus the standard `logical-state:*` tag from
  `import_state_prep`. Notes carry the source path and method description.
- **Names:** per-code unique, rlftqc-style: `FT zero (opt/opt)`,
  `Non-FT plus (heuristic)`, `FT zero (naive)`, `FT zero (heuristic/mixed)`.

### New reusable component: structural permutation finder

`scripts/add_circuit/` gains a permutation finder that, given derived (Hx, Hz)
in the circuit's labeling and a stored code's `h`, finds a qubit permutation σ
(`sigma[new] = old`) mapping one row space onto the other — via Tanner-graph
isomorphism with backtracking, pure Python/numpy, **no new dependencies**.
Found σs are verified by the existing row-space equality check in
`add_circuit(..., qubit_permutation=σ)` (the finder never bypasses
verification). Used here for tetrahedral/carbon/surface-d5; as a follow-up it
also unblocks rlftqc's deferred [[25,1,5]] circuit (out of scope for this
import, noted in the README). If the finder fails on a circuit, that circuit is
deferred with a report — never guessed.

## Part 2: `eval_det/` — 18 worst-case circuits from `.qasm` + `results.csv`

### Inputs

- **18 `.qasm` files** (h+cx only, exactly n qubits — the non-FT prep stage):
  `11_1_3` (1), `16_2_4` (1), `carbon` (2), `hamming` (2), `hypercube` (1),
  `shor` (2), `steane` (2), `surface_3` (4), `tetrahedral` (3). Filename
  `{state}_{procedure}.qasm` where procedure is parsed with `eval.py`'s rule:
  `"heuristic" in name` → heuristic, else opt (covers the hamming filenames
  `zero_ft_heuristic_opt` / `zero_ft_opt`).
- **`results.csv`** (52 rows): per (code, `zero_state`, verification ∈
  {heuristic, optimal, global}, procedure) — columns `verification_stabs_{0,1}`,
  `recovery_stabs_{0,1}`, `flags_{0,1}` as Python/numpy reprs (parseable).
  Semantics (`state_prep_det.py`): layer 0/1 = the two Pauli error types (for
  |0⟩: layer 0 measures Z-stabs); `Verification` = list of round-1 stab
  supports; `DeterministicCorrection` = {round‑1 outcome int → ([round‑2 stab
  supports], {round‑2 outcome → Pauli correction support})}; `flags_*` =
  analogous hook-flag correction branches.

### Fitting (verified)

All 18 files contain bare h+cx encoders (verified: 0 measurements each,
including the two hamming files whose vestigial `ft_` infix is historical).
Fitting mirrors Part 1: steane/shor under identity, surface_3 via n≤9 search,
hamming via self-dual dedup, tetrahedral/carbon via the structural permutation
finder; the three newly seeded codes fit under identity by construction.

### One library entry per file (18), canonical variant

Variant preference per file: **global → optimal → heuristic** (decision: the
jointly-optimized two-layer solution is canonical). A file whose (code, state,
procedure) has no CSV row for any variant is reported and skipped (not silently
imported). Verified: all 18 files have CSV rows; only `carbon zero_heuristic`
lacks a `global` row (its 'optimal' row is used).

### Worst-case execution body (the stored Stim circuit)

Constructed as: prep (from the qasm) → layer‑0 round‑1 verification incl. hook
flags → most expensive layer‑0 branch: its round‑2 measurements + its Pauli
correction (plain Pauli gates) → same for layer 1.

- **Worst branch** = maximize (round‑2 CNOT count, then correction weight),
  hook-correction branches included in the comparison. Deterministic given the
  CSV row, so re-imports are stable.
- **Verification sub-circuits** reproduce `simulation_det.py`'s
  `_create_stab_measurement_circuit` ancilla/CX ordering _verbatim_ (the CSV's
  hook corrections assume it). Ancillas sit at indices ≥ n and are reused via
  `MR`, so `qubit_count` matches the paper's "with reuse" ancilla accounting.
- **Consistency gate:** each constructed body's CNOT/ancilla counts are checked
  against `DeterministicVerification`'s worst-case stats recomputed from the CSV
  row; mismatch → defer that circuit with a report (never guess).

### Notes = the complete adaptive protocol

Readable rendering of the full protocol from the CSV row: layer‑0/1 round‑1
stabilizers, per-outcome branch tables (round‑2 stabs → outcome → Pauli
correction), hook corrections, chosen variant — preceded by an explicit
statement that the stored body and metrics show the _worst-case branch of an
adaptive protocol_ (fair-comparison convention) and that the actual protocol
branches on measurement outcomes.

### Metadata

Source `https://arxiv.org/abs/2501.05527`, tool `mqt-qecc`, tags
`state-preparation`, `ft`, `deterministic`, `prep:<procedure>`,
`verification:<variant>`.
Names: `Det FT zero (opt)`, `Det FT plus (heuristic)`, … (per-code unique).

### Three new codes seeded

From the Hx=Hz matrices hard-coded in `eval_det/eval.py`:

| Slug   | Name             | [[n,k,d]]  | zoo_url                                      |
| ------ | ---------------- | ---------- | -------------------------------------------- |
| 11-1-3 | "[[11,1,3]]"     | [[11,1,3]] | none (unless verified during implementation) |
| 16-2-4 | "[[16,2,4]]"     | [[16,2,4]] | none (unless verified during implementation) |
| 16-6-4 | "Tesseract Code" | [[16,6,4]] | https://errorcorrectionzoo.org/c/stab_16_6_4 |

Seeded via `import_state_prep`'s existing code-creation path (`self_dual`
method — all three are self-dual CSS), same as the codes once seeded from MQT.

## Import order & workflow

1. `eval/` first (existing codes only), then `eval_det/` (seeds the 3 new codes).
2. Classify-only run must be clean (all fits resolved or explicitly deferred)
   before `--write`.
3. After `--write`: `npm run format && npm run validate:yaml &&
npm run validate:circuits && npm run db:create`, spot-check circuits on the
   dev server (notes rendering, metrics, tags, tool links).
4. Feature branch → PR. Version bump not required (data-only, no schema change).

## Error handling

- Any fit failure, missing CSV row, or consistency-gate mismatch → circuit
  deferred, listed in the driver's final report (rlftqc convention). The import
  is considered successful with deferrals; deferrals are documented in the
  README.
- Originals (pre-canonicalization circuit + matrices) are always written to
  `data_yaml/circuits/originals/` by `import_state_prep`.

## Out of scope

- No schema changes; no branching/adaptive circuit format.
- No import of `eval/`'s `.qasm` siblings (redundant with `.stim`).
- No reconstruction beyond the published CSV data (no re-running SAT synthesis).
- rlftqc circuits are unrelated (different tool/source) — no interaction.
