# MQT QECC front-search FT state-prep → QECirc importer

Imports the fault-tolerant circuits for the logical all-zero state that MQT
QECC's front search (`mqt.qecc.circuit_synthesis.ft_search`) found. The dataset
lives in the [munich-quantum-toolkit/qecc](https://github.com/munich-quantum-toolkit/qecc)
repository (MIT) under `scripts/ft_stateprep/front_search/`; at the time of
import that directory is on the `ft-front-search` branch, not yet on `main`.

For each code the dataset holds a **front**: per two-qubit depth, the circuit
with the fewest operations (CNOTs + measurements) the search found, kept only if
it beats every shallower circuit — plus a few circuits kept on purpose although
another circuit beats them (five at the time of import). Each circuit's notes say
whether it is on its code's front, computed from `index.csv` (`on_front`). A
circuit for a code of distance `d` tolerates `t = (d − 1) // 2` faults under
post-selection on all detectors, and every circuit passed MQT QECC's exact
fault-tolerance check, which enumerates every set of up to `t` faults.

For the even distance of `sd_20_2_6`, the dataset also has a second front of
circuits that tolerate `t = d/2 = 3` faults (column `t` of `index.csv`). Their
names carry the `t` (`FT zero (front search, t = 3, depth 16, 149 ops)`), their
notes explain it, and `on_front` compares only circuits of the same `t`. The
library has no tag for `t`, so none is added.

Reusable logic lives in `scripts.add_circuit` (`import_state_prep`,
`find_sigma`); this directory holds only dataset knowledge.

## Run

```bash
python rebuild_all.py --dataset PATH/TO/front_search            # classify only
python rebuild_all.py --dataset PATH/TO/front_search --write    # import new rows
python rebuild_all.py --dataset ... --write --overwrite         # refresh, keep qec_ids
python rebuild_all.py --dataset ... --only color_17_1_5         # one dataset code
```

`--dataset` defaults to `../mqt-qecc/scripts/ft_stateprep/front_search` (a qecc
clone next to this repo). Then, as for every import:

```bash
uv run python scripts/annotate_circuits.py
npm run format && npm run validate:yaml && npm run validate:circuits && npm run db:create
```

**Re-runnable.** `index.csv` is the manifest: one row per circuit. A re-run
imports the rows not yet in the library and reports the rest as
`already-present` (matched through the `Source file:` in each circuit's notes).
A circuit stored earlier whose file has left the index — the front moved — is
reported as `STALE`, never deleted: `qec_id`s are permanent, so removing one is
a maintainer decision. Circuits are named by depth **and** operation count
(`FT zero (front search, depth 7, 70 ops)`), the same pair the dataset's file
names carry, so every file gets its own slug and a better circuit at an
existing depth is a new entry next to the one it supersedes, not a collision.

## Superseded circuits (extra)

On request, the import also holds 13 circuits that an earlier version of the
collection had and that a later circuit beats — at most as many operations at no
greater depth, and better in one of the two — so the collection dropped them:
one for `color_17_1_5`, one for `bga_24_4_5` and eleven for `color_31_1_7`. The
dataset no longer has them, so [`superseded/`](superseded/) holds a copy of each
file and its `index.csv` row, unchanged. Their notes say they are not in the
current collection and point to that copy. A file that comes back into the
dataset's `index.csv` is read from there instead.

## Codes

| Dataset code     | Stored code slug           | Fit                        |
| ---------------- | -------------------------- | -------------------------- |
| `surface_9_1_3`  | `rotated-surface-code-d-3` | `find_sigma`               |
| `surface_25_1_5` | `rotated-surface-code-d-5` | `find_sigma`               |
| `surface_49_1_7` | `rotated-surface-code-d-7` | `find_sigma`               |
| `color_17_1_5`   | `17-1-5`                   | `find_sigma`               |
| `color_31_1_7`   | `31-1-7`                   | `find_sigma`               |
| `golay_23_1_7`   | `23-1-7`                   | `find_sigma`               |
| `sd_20_2_6`      | `20-2-6`                   | `find_sigma`               |
| `bga_24_4_5`     | `24-4-5` (**new**, 2BGA)   | seeded from `codes/*.json` |

No dataset code uses the stored code's qubit order, so every circuit is
relabeled; the permutation is in each circuit's notes. `circuits/originals/`
keeps each circuit in the dataset's qubit labeling, after the reset rewrite and
ancilla compaction below (so not byte-for-byte the dataset file, which each
circuit's notes name). `find_sigma` is used rather than
`find_code_permutation` because the latter does not finish on the d=7 rotated
surface code (same finding as `surface-code-encodings`). σ is recomputed on each
run (well under a second per code) and verified by row-space equality inside
`add_circuit`.

## Decisions baked in

- **Consistency gate, in the dataset's own labeling, before anything is
  written:** CNOT, measurement and qubit counts equal `index.csv`; stim builds a
  noiseless detector error model (so every detector is deterministic); and on
  four random measurement records the data qubits are a `+1` eigenstate of every
  row of `Hx`, `Hz` and `Lz` from `codes/<code>.json` — i.e. they hold
  `|0…0⟩_L`, sign included.
- **Detectors kept in the stored body.** They are what the circuit's fault
  tolerance is defined against: a detector is the parity of one or more
  verification measurements, and a shot is accepted only if all are 0. Dropping
  them (as the readout-only detectors of other imports were) would lose the
  post-selection condition, which the bare measurements do not determine. This
  is the first stored body with `DETECTOR`s; the QASM view drops them
  (`skip_dets_and_obs`), as OpenQASM cannot express them. On the site they show
  in both positions of the Detectors switch, which adds and removes only the
  readout the annotator appends (`stripReadout`).
- **Resets rewritten to library convention** where exact: a first-touch `R` is
  dropped and a first-touch `RX` becomes `H`. A reset of an ancilla reused after
  its measurement is a real operation and stays. Measurements (`M`, `MX`) stay.
- **Ancilla indices compacted** to `n, n+1, …` in order. The files leave gaps in
  the ancilla numbering, which would inflate the stored `qubit_count` above the
  dataset's own count. Data qubits are untouched by this step.
- **Tags:** `state-preparation`, `ft`, `verification:front-search`,
  `distance:<d>`, plus the derived `logical-state:zero` and `flag` (the ancillas
  are verification qubits) and `tool:mqt-qecc`. The method tag joins the
  existing `verification:*` family. It names the search rather than a structure:
  the circuits mix bare checks, flags and ancilla blocks (the [[9,1,3]] circuit
  is a single bare check), so a structural tag such as "block" would not hold
  for all of them.
- **Notes** state the fault-tolerance definition, the post-selection protocol,
  the exact check, and the dataset's counts.
- **Metrics** are the pipeline's own. `two_qubit_gate_count` and `depth` equal
  the dataset's `cnots` and `depth`; `gate_count` also counts the `H` gates the
  reset rewrite introduces, and does not count measurements.

## Source

`source` is plain text, `MQT QECC, scripts/ft_stateprep/front_search`, not a
link, because the dataset has no stable public link yet and the library requires
a non-empty source. To switch to a link later, set `SOURCE`, re-run with
`--write --overwrite` (qec_ids are kept), and, for an arXiv link, run
`npm run papers:add -- <id>`.

## New code: `24-4-5`

The two-block group algebra (2BGA) code [[24,4,5]] of Lin & Pryadko, with
weight-8 checks. Seeded as "Two-Block Group Algebra Code" with tags `CSS`,
`LDPC` (the convention of the library's other qLDPC codes), the QEC Zoo 2BGA
page, and aliases `[[24,4,5]]` and `2BGA code`. The pipeline has no argument for
aliases, so `add_aliases` writes them into the code YAML after seeding, and only
when the file has none.
