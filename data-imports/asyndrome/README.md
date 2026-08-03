# AlphaSyndrome import (arXiv:2601.12509)

Imports syndrome-measurement schedules from
[acasta-yhliu/asyndrome](https://github.com/acasta-yhliu/asyndrome), the artifact of
_"AlphaSyndrome: Tackling the Syndrome Measurement Circuit Scheduling Problem for QEC Codes"_
([arXiv:2601.12509](https://arxiv.org/abs/2601.12509), ASPLOS '26, MIT-licensed).

These are the library's first `syndrome-extraction` circuits.

## Dataset

Clone the artifact repo next to this one so the layout is `…/asyndrome/` beside
`…/qecirc-website/`, or pass `--dataset PATH`. Two kinds of file matter:

- `qecc/<code>.json` — the code: `n`, `k`, `d`, `family`, and X/Z stabilizers and logicals as
  Pauli strings.
- `qecc/<code>/<method>.json` — a schedule: a list of ticks, each a list of
  `{data, ancilla, pauli}` checks that run in parallel.

Ancilla numbering is fixed by the dataset (`asyndrome/csscode.py`): data `0..n-1`, then the
X-check ancillas, then the Z-check ancillas.

Methods: `alpha-<decoder>` (the paper's MCTS scheduler, co-designed with a decoder — so the
same code has a different schedule per decoder), `baseline` (depth-optimal, by integer
program), and `google` / `trivial` (reference schedules for the surface codes).

## What one schedule becomes

One library circuit: **a single syndrome-extraction round**. `build_se_round`
(`scripts/add_circuit/syndrome_extraction.py`) turns the ticks into STIM, and the round count
is not baked in — the `stim-annotated` view repeats it `d` times into a memory experiment.

Two emitter choices worth knowing:

- **Ticks are preserved, never re-packed.** The tick assignment is the entire content of a
  scheduling result. (`compute_circuit_data` already skips compaction for circuits with TICKs.)
- **Hadamards go once per X-ancilla**, at its first and last active tick, where the dataset's
  own emitter wraps every individual check in an `H` pair. The two are equivalent — the inner
  pairs cancel — and the compact form keeps `gate_count` comparable with the rest of the
  library (surface-5x5 baseline: 160 → 104 gates; bbcode-72: 864 → 504). The dataset's noise
  model applies error per ancilla per _tick_, not per gate, so nothing about their evaluation
  depended on the extra Hadamards.

## Every import is gated on validation

`validate_syndrome_extraction_h` runs before anything is written: the round must measure
exactly the code's stabilizer group, and preserve every stabilizer and logical. Of the 69
schedules, **59 pass and 10 fail**, and the failures are systematic — every `google.json` and
every `trivial.json`. All 59 are imported.

The cause is a bad X-/Z-check interleaving. Pulling `Z_ancilla` back through one of these
rounds gives the intended stabilizer **times an X on a second ancilla**: two ancillas sharing
two data qubits whose CNOTs are ordered inconsistently come out entangled, so each outcome is
individually random. Every check is still applied exactly once, which is why nothing short of a
flow check notices.

It traces to the hard-coded tick tables in `asyndrome/special.py` — `GoogleScheduler`'s and
`TrivialScheduler`'s — and all three make the same mistake. Each table says which of the four
CNOTs of a 2x2 plaquette fires at which tick. Written out as the order the plaquette's corners
are visited:

| table                  | order          | shape                |
| ---------------------- | -------------- | -------------------- |
| Google `Z` `[0,1,3,2]` | NW, NE, SE, SW | **round the square** |
| Google `X` `[2,1,3,0]` | SE, NE, NW, SW | **round the square** |
| trivial `[1,2,4,3]`    | NW, NE, SE, SW | **round the square** |

A circular order is precisely what cannot work. Two neighbouring plaquettes share the two
qubits of one edge, and a loop travels _down_ that edge on one plaquette and _up_ it on the
other — so the two shared qubits get opposite relative orders, which is the odd number of
inversions that leaves the ancillas entangled. A **sweep** — row by row, or column by column —
crosses the shared edge the same way from both sides.

Brute-forcing all 576 (X, Z) table pairs against the dataset's own patch construction bears
that out exactly: **16 pairs are valid**, and every table appearing in one is a sweep; no loop
survives. The same 16 work for 3x3 and 5x5, so it is geometry-independent. Measuring each
valid pair's circuit-level Z-memory distance splits them again: **8 preserve the code distance**
(5 for surface-5x5) and 8 halve it (3), and the difference is whether the **X**-ancillas sweep
columns rather than rows — the usual hook-error argument about propagating parallel to the
logical operator.

stim's own `surface_code:rotated_memory_z` is one of those 8. Reading its first round back out,
one stabilizer type visits SE, SW, NE, NW (a row sweep, `[3,2,1,0]` in this convention) and the
other SE, NE, SW, NW (a column sweep, `[3,1,2,0]`). Same starting corner, one sweeping rows and
one columns.

The repair is therefore small and unambiguous — swap each table for a sweep starting at a
common corner, e.g. `X = [0,2,1,3]`, `Z = [0,1,2,3]` — but it is not a one-entry typo: the two
shipped tables also start from different corners, so the nearest valid pair differs in four
entries.

**Their pipeline cannot notice, by construction.** `asyndrome/scheduler.py`'s
`evaluate_circuit` builds its detectors from ideal `MPP` measurements before and after the
round and never reads the ancilla outcomes, and the residual term is ancilla-only — so the data
evolution their benchmark measures stays well defined even when the ancillas come out
entangled. The numbers they report are real measurements of the circuits they really ran.

**It does change one comparison, though.** The schedule still shapes how an ancilla fault
propagates into the data, which is exactly what their metric scores. Rebuilding their
evaluation circuit (ideal `MPP` before and after, per-tick `DEPOLARIZE1` on the ancillas at
their Brisbane rates, detectors comparing the two ideal rounds) and decoding with pymatching,
3M shots on surface-5x5 — logical error rate per round, X-memory + Z-memory combined:

| schedule                              | rate       |
| ------------------------------------- | ---------- |
| `google.json` as shipped (loop order) | 9.6 x 10⁻⁵ |
| the same, corrected to a sweep        | 3.2 x 10⁻⁵ |
| `alpha-pymatching`                    | 7.1 x 10⁻⁵ |
| `baseline` (depth-optimal)            | 1.5 x 10⁻³ |

So the real Google schedule is about **3x better** than the file standing in for it (44–152
events per cell, ~10σ), and that inverts the comparison: against the shipped stand-in
AlphaSyndrome looks ~1.4x better, against a corrected zig-zag the hand-crafted schedule is ~2x
better. The paper's headline claim is unaffected — that is measured against the _depth-optimal_
baseline, which is a valid schedule, and the ~20x gap over it reproduces here.

Two cross-checks that the corrected schedule is the right one and not a lucky pick: a second
sweep representative (stim's own, `X=[3,1,2,0]` `Z=[3,2,1,0]`) gives 3.8 x 10⁻⁵, consistent;
and a sweep with the **X**-ancillas on rows instead of columns gives 2.6 x 10⁻³, 80x worse —
which is the distance split above showing up as a rate.

Caveats: one code, one decoder, one noise model, and a reimplementation of their evaluation
circuit rather than their harness.

## Two data-file quirks the importer handles

- **`self-dual-bbcode.json` has its stabilizer fields swapped** — `x_stabilizers` holds
  Z-strings and vice versa. The dataset's own code reads the Pauli _character_, so everything
  downstream of it is self-consistent; `load_code` does the same. Reading the key would build
  silently wrong matrices.
- **The two defect codes each carry a qubit in no stabilizer** (index 12 and 20). The
  stabilizer group therefore gives `k = 3` where the file declares `k = 2`, and no logical
  touches the qubit. `load_code` drops it and renumbers, which is a relabeling of the schedule
  and nothing else — so they are stored on 24 and 40 qubits, not 25 and 41. Their distances are
  corrected too, for a separate reason: see below.

## Codes

59 circuits across 25 codes are imported. Seven of those codes were already in the library and
are matched by the dedup search (`bbcode-72` → `72-12-6`, both d=3 colour codes →
`steane-code`, `color-hex-5/7` → `19-1-5` / `37-1-7`, `color-oct-5/7` → `17-1-5` / `31-1-7`,
`surface-3x3` → `rotated-surface-code-d-3`).

Four more match on invariants but defeat that search's budget — the automorphism-rich case the
pipeline documents as `UncertainDedupError`. Their permutations live in
`sigma_precomputed.json`, computed by [`find_sigma.py`](find_sigma.py). The matcher itself is
`scripts.add_circuit.find_sigma`, shared with the qLDPC and QUITS imports, and it works on the
code's low-weight **codewords** rather than on puncture ranks. (Codewords, not a low-weight
basis: `sparsify_basis` gives both codes weight-4 generators but not the _same_ ones, so those
hypergraphs are incomparable. In RREF each row owns a private pivot column, so a codeword of
weight ≤ w is a sum of ≤ w rows — exhaustive and cheap.) `add_circuit` verifies every sigma by
row-space equality against the stored code, so a stale entry fails loudly rather than silently
mislabelling qubits.

```bash
uv run python data-imports/asyndrome/find_sigma.py --dataset PATH   # merges into the json
```

The other 14 are new, filed under the numeric `n-k-d` slug convention with the family's display
name: hyperbolic surface (6), hyperbolic colour (3), surface with defects (2), the [[61,1,9]]
6.6.6 colour code, the 5×9 rotated surface code [[45,1,5]], and the self-dual bivariate bicycle
code [[42,6,6]].

One of the new ones needs `assume_new`, because its cheap invariants line up with a stored code
it is not: the hyperbolic surface [[36,8,4]] against `36-8-4-bpc`, the balanced-product cyclic
code from the QUITS import. They share only `n` and `k`. The stored code's X- and Z-row-space
ranks are both 14 where this one's are 11 and 17, and rank is a permutation invariant — an
X↔Z swap gives 17/11, so no relabeling reconciles them. The exhaustive weight enumerators
disagree as well. `rebuild_all.py` records that refutation next to the flag and refuses to
write if the slug ever turns out to hold someone else's code, so `assume_new` cannot quietly
overwrite an entry.

Two dataset codes share one stored entry: at d=3 both colour-code lattices _are_ the Steane
code, so all six of their schedules land on `steane-code`. They are six distinct circuits, not
three duplicates — the lattices give different check bases and different tick structures — so
the circuit name carries the lattice (`… on the 6.6.6 lattice`). Without it the three names
collide and the second import silently overwrites the first.

## Distances the dataset does not give, or gets wrong

[`code_distance.py`](code_distance.py) computes the exact CSS distance — the minimum weight of
a non-trivial logical, by enumerating every stabilizer combination against every logical class.
Exhaustive, so the answers are distances and not bounds; affordable only because the budget is
`2^(rank + k) <= 2^26`, which is why it is a maintainer script and not part of the pipeline.
Its results are committed in `rebuild_all.py`'s `DISTANCE` map. It agrees with the declared `d`
for every dataset code it can reach, except:

- **`self-dual-bbcode`** ships `d: -1`. Computed: `d_X = d_Z = 6`, so [[42,6,6]].
- **`defect-5` / `defect-7`** declare 5 and 7. Both have `d_X = 2`, and the weight-2 X-logical
  is the file's own second `logical_xs` entry — supports {1,8} and {2,11}. Confirmed a second
  way by enumerating every weight-≤2 vector that commutes with the Z-checks and is not a
  stabilizer, and a third by checking the declared logicals pair symplectically (they do: the
  pairing matrix is invertible, so both really are logical qubits).

  The short operator is not a corruption — it is **what a defect does**. Puncturing a surface
  code adds a logical qubit whose operators are set by the puncture's geometry, and a puncture
  near a boundary buys you a short string. Per logical qubit:

  |             | defect-5     | defect-7     |
  | ----------- | ------------ | ------------ |
  | original q0 | X̄ 4, Z̄ 4     | X̄ 4, Z̄ 5     |
  | defect q1   | **X̄ 2**, Z̄ 6 | **X̄ 2**, Z̄ 6 |

  So the extra logical qubit is intended and its distance-2 operator comes with it. What the
  numbers do not support is the declared 5 and 7 — **neither logical qubit reaches them**, so
  they are not the code's distance under the usual definition (2) and not the surviving
  qubit's either (4). They are the distance of a base lattice that the shipped matrices no
  longer describe. Stored as [[24,2,2]] and [[40,2,2]], with the reason in each circuit's
  notes, because the library's `[[n,k,d]]` has to describe the `h` printed beside it.

  Two hypotheses ruled out along the way: the codes are not cyclic under the shift their
  logical strings suggest, and the weight-2 operator is not a check that went missing from the
  file — adding it and its shifts to the stabilizer group breaks commutation with `Hz`.

## Not imported

- **The 10 `google` / `trivial` schedules** — they do not measure their stabilizers; see above.

## Fault tolerance is deliberately not tagged

No circuit gets `ft` or `non-ft`. A bare-ancilla round is not automatically distance-preserving:
building the memory experiment for `color-hex-3` (Steane) and asking stim for the circuit-level
Z-memory distance gives **2**, not 3 — the familiar hook error on a weight-4 check, which is why
these codes are usually read out with flag qubits. The same computation gives 3 and 5 for
`surface-3x3` and `surface-5x5`, so it is genuinely code-dependent, and for the larger codes it
is not affordable. The paper's claim is about logical error rate under a named decoder and noise
model, which is not the same statement, so nothing here is tagged as if it were.

## Usage

```bash
python rebuild_all.py                                  # classify only
python rebuild_all.py --write                          # import
python rebuild_all.py --dataset ../../../asyndrome     # explicit dataset path
python rebuild_all.py --only surface                   # restrict
```

Then the standard follow-up:

```bash
uv run python scripts/annotate_circuits.py
uv run python scripts/measure_circuit_distance.py --write
npm run format && npm run validate:yaml && npm run validate:circuits && npm run db:create
```

## Re-running

The importer is idempotent for codes (dedup) and hardcodes `overwrite=True` for circuits,
so a re-import rewrites every circuit file in place. It carries over the `qec_id` — the
public `#N` — and nothing else that was added after the first import.

**What a re-import loses:** the measured `circuit-distance:<N>` tags. They are not the
code's distance and not derivable from the source; `scripts/measure_circuit_distance.py`
searches for them, and re-importing writes a fresh `tags:` list without them.

**What recovers it:** one command, which is why the loss is a documentation gap rather
than a data one. The script strips any existing tag and re-measures, so it is idempotent
and safe to run whether or not anything was lost:

```bash
uv run python scripts/measure_circuit_distance.py --write
```

**Not lost:** `crumble_url_annotated` and the `stim-annotated` bodies —
`scripts/annotate_circuits.py` regenerates them, and `test_url_edit_is_idempotent`
(`scripts/tests/test_annotate.py`) pins that re-running rewrites rather than duplicates.
Run it anyway, as above; it is cheap.
