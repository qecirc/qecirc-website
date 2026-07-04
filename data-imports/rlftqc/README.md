# RLFTQC → QECirc importer

Dataset-specific scripts for importing the **"RLFTQC Circuits"** dataset
(from _Quantum Circuit Discovery for Fault-Tolerant Logical State Preparation
with Reinforcement Learning_, [arXiv:2402.17761](https://arxiv.org/abs/2402.17761))
into the QECirc website library.

This lives in the repo (`data-imports/rlftqc/`) but is kept apart from the
reusable code: everything general — deriving a code from a state-prep circuit,
validating it, identifying the logical state, fitting a circuit to a stored code,
capturing provenance — lives in `scripts/add_circuit/state_prep.py` (re-exported
from `scripts.add_circuit`). What remains here is only the knowledge specific to
_this_ dataset: its folder layout, which stored code each folder maps to, and the
hardware metadata each section implies.

## Expected layout

```
qecirc/
├── qecirc-website/                  # the repo (reusable code + this dir)
│   └── data-imports/rlftqc/         # this directory
└── RLFTQC Circuits/                 # the dataset (sits beside the repo)
```

## Files

- `rebuild_all.py` — the importer. Anchors each of the 239 circuits (excludes
  `*_flag.stim`) to a stored code in `data_yaml` and fits it by qubit permutation.

## Run

```bash
python rebuild_all.py                       # classify only (no writes)
python rebuild_all.py --write               # import into the repo's data_yaml
python rebuild_all.py --write --data-dir /tmp/dt   # write to a scratch copy
```

After a real `--write`: in the repo, `npm run format && npm run validate:yaml &&
npm run validate:circuits && npm run db:create` (see `docs/adding-circuits.md`).

## The dataset

Four sections, all state-preparation circuits given as bare STIM gate lists (no
check matrices):

| Section                                    | What                         | Notes                                                              |
| ------------------------------------------ | ---------------------------- | ------------------------------------------------------------------ |
| `logical-state-preparation/`               | non-FT `\|0⟩`/`\|+⟩` preps   | `fully-connected/` (H,S,CNOT) and `ibm/` (native gates)            |
| `verification-circuit-synthesis/`          | flag/verification circuits   | ships as `_combined` (prep+flag) and `_flag` (flag only) pairs     |
| `integrated-ft-logical-state-preparation/` | full FT preps                | `fully-connected/`, `2d-grid/`, `ibm/`; flags at qubit indices ≥ n |
| `distance-5/`                              | d=5 CSS `_combined` circuits | `[[17,1,5]]`, `[[19,1,5]]`, `[[25,1,5]]`                           |

## Per-code fit

Every code is already in `data_yaml` — the 4 once seeded from MQT were added
upstream in **#78** (`shor-code`, `tetrahedral-code`, `rotated-surface-code-d-3`,
`rotated-surface-code-d-5`). So each circuit is anchored to the stored code and
fitted by a qubit permutation (`identity` → a supplied `known_perms` σ →
exhaustive search for `n ≤ 9`).

| Dataset folder  | Anchored to (slug)         | Fit                             | Status                 |
| --------------- | -------------------------- | ------------------------------- | ---------------------- |
| `5-1-3`         | `five-qubit-code`          | identity                        | ✅ 56                  |
| `7-1-3`         | `steane-code`              | identity / self-dual auto-dedup | ✅ 58                  |
| `17-1-5`        | `17-1-5`                   | supplied σ (4) + auto-dedup (1) | ✅ 5                   |
| `19-1-5`        | `19-1-5`                   | self-dual auto-dedup            | ✅ 4                   |
| `23-1-7`        | `23-1-7`                   | self-dual auto-dedup            | ✅ 1                   |
| `15-1-3`        | `tetrahedral-code`         | identity                        | ✅ 40                  |
| `9-1-3-shor`    | `shor-code`                | identity                        | ✅ 41                  |
| `9-1-3-surface` | `rotated-surface-code-d-3` | n≤9 search                      | ✅ 33                  |
| `25-1-5`        | `rotated-surface-code-d-5` | —                               | ⏳ 1 deferred (n=25 σ) |

**238 / 239 import.** The single `[[25,1,5]]` circuit is deferred: n=25 is too
large to brute-search and `find_qubit_permutation` can't confirm the σ into main's
labeling — it needs the structural permutation-finder (see below).

### `17-1-5` (qubit-permutation search) — RESOLVED

The paper's circuits use a **different qubit labeling** than the stored codes, so
each circuit must be fitted to the canonical code by a qubit permutation. For
small codes this is trivial (`5-1-3`, `7-1-3` fit under the identity) and for
`19-1-5` / `23-1-7` the canonical-form hash still matches, so `add_circuit`'s
dedup resolves the permutation directly. `[[17,1,5]]` is automorphism-rich: its
canonical hash differs between the two labelings, so the automatic search could
not confirm equivalence.

This is now handled by supplying the permutation explicitly:
`add_circuit(..., qubit_permutation=σ)` (and `import_state_prep(..., permutation=σ)`)
adopts a caller-provided permutation, verifying it by **row-space equality**
against the stored code (no search) and applying it to the circuit. The
permutation for the 4 paper-labeled `17-1-5` circuits is

```
σ = [0, 1, 4, 8, 12, 6, 7, 9, 13, 2, 3, 5, 16, 10, 11, 14, 15]   # sigma[new] = old
```

The 5th circuit (`distance-5/17-1-5/17_3_5_combined.stim`) is already in the
stored labeling and dedups automatically (no permutation needed). All 5 import
and validate. A general structural permutation-finder (Tanner-graph isomorphism)
would remove the need to supply σ by hand, but is no longer blocking.

## Decisions baked in

- **Verification circuits: store `_combined`, never `_flag` alone.** The flag part
  without the prep is not a meaningful standalone circuit.
- **Flags are preserved.** Flag/ancilla qubits (indices ≥ n) are stripped only to
  _derive_ the code; the full circuit is stored and tagged `ft` / `flag`.
- **One canonical code, originals kept.** Each circuit is fitted (by qubit
  permutation) to a single stored code definition. The untouched original circuit
  and pre-canonicalization matrices are always written to `data_yaml/circuits/
originals/` so any fitting error can be corrected later.
- **Provenance captured, nothing dropped.** Source file, logical state,
  connectivity, gate set, device, flag-qubit indices, device qubit placement, and
  the applied canonicalization permutation go into the circuit `notes`; the
  categorical ones also become `key:value` tags (`connectivity:*`, `device:*`,
  `logical-state:*`, `flag`).
- **Logical-state label.** For CSS codes the _basis_ (Z vs X) is derived from the
  check matrices: the source's exact label is kept when its basis agrees, else the
  library basis is used (Z→`zero`, X→`plus`) and the source label recorded in a
  note (this handles Shor, whose X/Z convention is opposite MQT's). For the
  non-CSS 5-qubit code the logical X̄/Z̄ ordering is not canonical, so the source's
  folder label is used directly.

## Status

**238 / 239 circuits import** (`rebuild_all.py --write`) in ~80s, anchored to the
codes already in `data_yaml` (no new codes seeded — all 9 are present, the 4
formerly-missing ones via #78). Validator: all circuits pass, non-CSS circuits
skipped (the CSS validator can't check them). The one deferred circuit is the
`[[25,1,5]]` rotated surface (n=25 permutation into main's labeling — needs the
structural finder). See `TODO.md` for the apply-to-real + commit steps.
