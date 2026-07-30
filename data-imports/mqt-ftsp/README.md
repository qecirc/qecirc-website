# MQT QECC FT state-prep → QECirc importer

Dataset-specific scripts for importing the published fault-tolerant
state-preparation circuits from the
[munich-quantum-toolkit/qecc](https://github.com/munich-quantum-toolkit/qecc)
repository (MIT) into the QECirc library. Two parts:

| Part        | Source dir (in the qecc repo)        | Paper                                                                                                                     | Circuits |
| ----------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | -------- |
| `eval/`     | `scripts/ft_stateprep/eval/circuits` | [arXiv:2408.11894](https://arxiv.org/abs/2408.11894) (PRX Quantum 6, 020330) — non-deterministic FT prep (post-selection) | 61 of 63 |
| `eval_det/` | `scripts/ft_stateprep/eval_det/`     | [arXiv:2501.05527](https://arxiv.org/abs/2501.05527) — deterministic FT prep (adaptive corrections)                       | 18 of 18 |

Reusable logic lives in `scripts.add_circuit` (`import_state_prep`,
`find_code_permutation`); this directory holds only dataset knowledge.

## Expected layout

```
qecirc/
├── qecirc-website/               # the repo (this dir inside it)
└── mqt-qecc/                     # clone of munich-quantum-toolkit/qecc
```

```bash
git clone https://github.com/munich-quantum-toolkit/qecc ../mqt-qecc
git -C ../mqt-qecc checkout 1685b87~1  # last commit with the old codes/ layout
```

The pin matters: #751 (2026-07-13) restructured `src/mqt/qecc/codes/` and
dropped the `rotated_surface_d5/` and `hamming_15/` `.npy` matrix dirs this
importer reads for its `perm_find` fits. The circuits themselves
(`scripts/ft_stateprep/`) are unchanged at HEAD.

## Run

```bash
python rebuild_all.py                 # classify only (no writes)
python rebuild_all.py --write         # import into the repo's data_yaml
python rebuild_all.py --write --overwrite  # data refresh: replace stored circuits, keep qec_ids
python rebuild_all.py --only det      # restrict to one part (eval|det)
```

After a real `--write`: `npm run format && npm run validate:yaml &&
npm run validate:circuits && npm run db:create`.

## Part 1 — `eval/` (non-deterministic FT prep)

63 `.stim` files (each with an identical `.qasm` sibling), named
`{zero|plus}_{ft|non_ft}_{prep}[_{verify}]`. `non_ft` files are bare H+CX
encoders; `ft` files include the inline flag-qubit verification measurements
(`MR`) — post-selection is the protocol (discard on any −1 outcome), so no
classical control. Imported as-is from the `.stim` files.

### Fit strategy per code (verified 2026-07-04)

| Dataset dir          | Stored code slug           | Fit                                    |
| -------------------- | -------------------------- | -------------------------------------- |
| `steane`             | `steane-code`              | identity                               |
| `shor`               | `shor-code`                | identity                               |
| `rotated_surface_d3` | `rotated-surface-code-d-3` | exhaustive search (n ≤ 9)              |
| `rotated_surface_d5` | `rotated-surface-code-d-5` | `find_code_permutation`                |
| `hamming`            | `15-7-3`                   | `find_code_permutation` (`hamming_15`) |
| `tetrahedral`        | `tetrahedral-code`         | `find_code_permutation`                |
| `carbon`             | `carbon-code`              | `find_code_permutation`                |
| `cc_4_8_8`           | `17-1-5`                   | self-dual hash dedup                   |
| `cc_6_6_6`           | `19-1-5`                   | self-dual hash dedup                   |
| `cc_4_8_8_d7`        | `31-1-7`                   | self-dual hash dedup                   |

σs are computed at import time from the code matrices shipped in the qecc repo
(`src/mqt/qecc/codes/<dir>/{hx,hz}.npy`) — MQT's labeling differs from the
stored codes' AND from the RL paper's (rlftqc) labeling for these codes.

### Deferred files (defective upstream — worth an issue on mqt-qecc)

- `rotated_surface_d3/zero_non_ft_heuristic.stim` — invalid stim (odd CX
  target count; truncated mid-verification). The `.qasm` sibling is also
  broken: it is named `non_ft` but contains verification CXs onto an
  undeclared `z_anc` register.
- `hamming/plus_ft_heuristic_opt.stim` — parses, but the prepared state
  violates one Z-stabilizer of [[15,7,3]] while all 9 sibling files pass.

## Part 2 — `eval_det/` (deterministic FT prep, worst-case bodies)

18 `.qasm` files containing only the bare non-FT encoders; the deterministic
verification + correction protocol lives in `results.csv`
(`verification_stabs_{0,1}`, `recovery_stabs_{0,1}`, `flags_{0,1}`).

**Stored-body convention:** the library entry linearizes the WORST-CASE branch
of the adaptive protocol — prep, then per layer the always-measured round-1
verification (with hook flags, ancilla/CX ordering ported verbatim from
`simulation_det.py::_create_stab_measurement_circuit`) and the most expensive
outcome branch's round-2 measurements. The outcome-dependent Pauli correction
is **not** part of the stored circuit — in practice it is absorbed into the
Pauli frame; the complete correction tables (all branches) are rendered into
each circuit's notes. Metrics are therefore an honest upper bound on the
quantum operations, the noiseless body stays in the codespace (validation
passes), and bodies contain only H/CX/MR so QASM and Cirq views generate.

- One entry per file; verification variant preference **global → optimal →
  heuristic** (only `carbon zero_heuristic` lacks a global row → optimal).
  Tagging: the library-default `global` variant gets no `verification:*` tag,
  and `optimal` is tagged `verification:opt` (matching the eval/rlftqc
  spelling); the chosen variant is always named in the notes.
- Procedure parsed with eval.py's rule: `"heuristic" in name` → heuristic,
  else opt (covers `hamming/zero_ft_heuristic_opt.qasm` etc.; the `ft_` infix
  there is vestigial — the files are bare encoders).
- Consistency gate: every constructed body must `symplectic_validate` against
  the code in MQT's own labeling before import; mismatches defer.

### New codes seeded (matrices from `eval_det/eval.py`, Hx = Hz)

| Slug     | Name             | [[n,k,d]]  | zoo_url                                      |
| -------- | ---------------- | ---------- | -------------------------------------------- |
| `11-1-3` | "[[11,1,3]]"     | [[11,1,3]] | —                                            |
| `16-2-4` | "[[16,2,4]]"     | [[16,2,4]] | —                                            |
| `16-6-4` | "Tesseract Code" | [[16,6,4]] | https://errorcorrectionzoo.org/c/stab_16_6_4 |

## Follow-up

`scripts/add_circuit/perm_find.py` (built for this import) can also unblock
the rlftqc importer's deferred `[[25,1,5]]` circuit
(`data-imports/rlftqc/README.md`).

## Deduplication (post-import)

The library keeps one entry per distinct circuit body. Nine eval entries were
removed as byte-identical to a kept sibling: in several published pairs the
`heuristic` and `opt` variants coincide (e.g. `tetrahedral Non-FT zero`), and
some `ft` files contain no verification and equal their `non_ft` sibling
(e.g. shor `plus` — its |+> preparation needs no verification). Two
`Circuit-Synth` entries (steane / 19-1-5 zero depth-optimized) were removed in
favor of the byte-identical MQT `Non-FT zero (heuristic)` entries.
`import_state_prep` now rejects originals that are byte-identical to a stored
circuit, so re-runs report these files as duplicates instead of re-adding them.
