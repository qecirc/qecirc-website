# Syndrome-extraction circuits — investigation & design notes

**Status:** implemented. 59 circuits and 14 codes imported; validator, emitter and
annotated view are in `scripts/add_circuit/`, where they shipped ahead of this data as
#145 so the qLDPC and QUITS imports could use them. This document is kept as the record
of why each choice was made — see the import README for the operational detail.
**Date:** 2026-07-28
**Dataset under consideration:** [acasta-yhliu/asyndrome](https://github.com/acasta-yhliu/asyndrome) —
_AlphaSyndrome: Tackling the Syndrome Measurement Circuit Scheduling Problem for QEC Codes_,
ASPLOS '26 ([arXiv:2601.12509](https://arxiv.org/abs/2601.12509),
[doi:10.1145/3779212.3790123](https://doi.org/10.1145/3779212.3790123)). MIT-licensed.

---

## 1. What the library already assumes, and where it breaks

`syndrome-extraction` is already a first-class tag (`src/lib/tag-categories.ts:18`), the
landing page names it as scope ("still to come", `src/pages/index.astro:190`), and
`validate_syndrome_extraction()` exists as a `NotImplementedError` stub
(`scripts/add_circuit/circuit_validate.py:360`). Zero circuits carry the tag today.

Three load-bearing invariants were written for prep/encoding circuits and do **not** hold here:

| Invariant                                                      | Why SE breaks it                                                                                                    | Consequence                                                                               |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Canonical `.stim` body is **reset-free** (`CLAUDE.md`)         | An SE round is `R` ancillas → CX ladder → `M` ancillas. Resets and measurements are the circuit, not an annotation. | `to_tableau()` is unavailable. The fit/derive machinery must not be pointed at SE bodies. |
| Circuit input is `\|0…0⟩`                                      | SE acts on an **already-encoded** state; the data qubits are arbitrary codewords.                                   | No reset prologue. `annotate.py` already knows this (CHANGELOG line ~111) and skips them. |
| `validate:circuits` routes on `encoding` / `state-preparation` | SE circuits fall through to `circuit_type="skipped"`.                                                               | They would be silently unvalidated — the worst outcome.                                   |

Good news: the **compute** half of the pipeline already copes. Feeding a generated SE round
through `compute_circuit_data()` produced correct metrics, QASM (with a `creg rec[…]`), Cirq,
Crumble and Quirk links with no changes. `has_ticks()` correctly suppresses MQT compaction, so
a submitted TICK schedule survives — which matters enormously here, since the _schedule_ is the
entire scientific content of these circuits.

## 2. The validator: stabilizer flows

There is a clean, general, decoder-free correctness criterion for one SE round, and stim 1.15
(already pinned) implements it via `Circuit.has_flow`. For every stabilizer row `S` of the
code's symplectic `h`, with ancilla `j`:

```python
# the ancilla is reset, so its input is trivial: the round MEASURES S
circ.has_flow(stim.Flow(f"{ident} -> {S} xor rec[{j - m}]"), unsigned=True)
# and S must survive the round untouched
circ.has_flow(stim.Flow(f"{S} -> {S}"), unsigned=True)
```

plus `L -> L` for every logical operator. `unsigned=True` matches the repo's existing
sign-free posture (`codes.h` names the group only up to a Pauli frame).

This is exactly the right check, and it is **not** implied by the schedule being conflict-free:
it is what catches a bad _interleaving_ of X- and Z-checks that share data qubits, which is the
whole subject of the paper.

An independent cross-check (3 noiseless rounds, `DETECTOR`s comparing round 2 vs round 3, then
`detector_error_model()` — which throws on non-deterministic detectors) agrees with the flow
check on all 69 schedules. Worth keeping both: the flow check additionally pins down _which_
stabilizer each ancilla measures, whereas repeatability would accept an ancilla that
deterministically measures `S₁S₂`.

**Recommendation:** implement `validate_syndrome_extraction_h(circuit, h, n, ancillas)` in
`circuit_validate.py` on the flow criterion, add a third branch to
`scripts/validate_circuits.py`, and make the ancilla↔stabilizer correspondence explicit
(see §5 — it has to be stored somewhere).

## 3. The dataset

30 code files, 26 with schedules, **69 schedule files** total. Schedules are stored as JSON:
a list of ticks, each tick a list of `{data, ancilla, pauli}` triples. Ancilla numbering is
fixed by `asyndrome/csscode.py`: data `0..n-1`, X-ancillas `n..n+|Sx|-1`, Z-ancillas after that.
Converting a schedule to STIM is ~30 lines.

Methods present: `alpha-<decoder>` (MCTS, the paper's contribution — decoders `pymatching`,
`bp_osd`, `hypergraph_union_find`, `bp_lsd`), `baseline` (depth-optimal ILP via `pulp`),
`google` (hand-crafted zig-zag), `trivial`.

Code families: rotated surface (3×3, 5×5, 5×9, 7×7, 9×9), hexagonal and square-octagon color
(d=3,5,7,9), bivariate bicycle (72 only, of five code files), defect surface, hyperbolic surface
(6), hyperbolic color (3), self-dual BB.

### 3.1 Ten of 69 schedules fail validation — one root cause, and it is fixable

I ran both checks over all 69. **59 pass, 10 fail**: every `google.json` and every
`trivial.json` (surface 3×3 … 9×9). Every `baseline` and every `alpha-*` passes.

Root cause, diagnosed by pulling `Z_ancilla` back through the round's unitary part: for a
failing schedule the measured operator is the intended stabilizer **times an X on a second
ancilla** — e.g. surface-3x3 `google`, ancilla 9 measures `S₀ ⊗ X₁₄`. The data part is always
correct (so the round still preserves the code state, and `S -> S` passes), but the two
ancillas end up entangled, so the outcome is individually random and no syndrome is extracted.
This is the classic X-/Z-check interleaving failure: two ancillas sharing two data qubits whose
CNOTs are ordered inconsistently between them.

It is a one-line bug in `asyndrome/special.py`'s `GoogleScheduler.reorder_table`. Brute-forcing
all 576 (X-order, Z-order) tick tables through the same patch construction: **16 are valid**,
including the textbook `X=[0,1,2,3] / Z=[0,2,1,3]` transposed pair — the shipped
`X=[2,1,3,0] / Z=[0,1,3,2]` is not among them. The same 16 work for 3×3 and 5×5, so the fix is
geometry-independent.

Note this does **not** impeach the paper's numbers. `asyndrome/scheduler.py`'s
`evaluate_circuit` builds its detectors from ideal `MPP` measurements before and after the
round and never uses the ancilla outcomes, and the residual term is ancilla-only — so the data
evolution their benchmark measures is unaffected. The schedules are unusable as _syndrome
extraction_, which is exactly what this library publishes.

Options: (a) import the 59 valid ones and leave the baselines out; (b) regenerate corrected
Google/trivial schedules ourselves with a valid reorder table — then they are our circuits, not
the paper's, and must be sourced as such. I lean (a) now, (b) later if we want the comparison
in the library, and either way it is worth reporting upstream.

### 3.1b Two data-file issues in `qecc/*.json`

- **`self-dual-bbcode.json` has its two stabilizer fields swapped**: `x_stabilizers` holds
  Z-strings and `z_stabilizers` holds X-strings. Everything downstream is self-consistent
  because `PauliCheck.from_stabilizer` reads the _character_, not the field name — and once the
  importer does the same, its `alpha-bp_lsd` schedule validates 42/42. **The importer must
  derive the Pauli type from the string, never from the key.** (An earlier count of 11 failures
  included this file; it was my bug, not theirs.) It also carries `d: -1` (unknown distance),
  so it needs a distance from elsewhere before it can be a library code.
- **`defect-5` / `defect-7` each contain one qubit in no stabilizer at all** (index 12 and 20).
  So the stabilizer group gives `k = 3`, not the declared `k = 2`, and only 2 logical pairs are
  listed — the defect is modelled as a disconnected qubit. Decide explicitly: drop the qubit
  (→ [[24,2,5]] / [[40,2,7]]) or keep it and record why. All other 24 codes are internally
  consistent (CSS, `k` matches, logicals commute with the checks and are independent of them).

### 3.2 Code coverage vs. the library

Run through `find_existing_code_h()`:

| asyndrome code                                                                       | stored code                                                                                                                              |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `bbcode-72`                                                                          | `72-12-6` (needs permutation)                                                                                                            |
| `color-hex-3`, `color-oct-3`                                                         | `steane-code` (needs permutation)                                                                                                        |
| `color-hex-5` → `19-1-5`, `-7` → `37-1-7`; `color-oct-5` → `17-1-5`, `-7` → `31-1-7` | existing, permutation needed                                                                                                             |
| `surface-3x3`                                                                        | `rotated-surface-code-d-3`                                                                                                               |
| `surface-5x5`, `-7x7`, `-9x9`, `color-oct-9`                                         | invariants match but the permutation search is **inconclusive** — the documented `UncertainDedupError` path                              |
| everything else (13 codes)                                                           | **new**: defect surface ×2, hyperbolic surface ×6, hyperbolic color ×3, `color-hex-9` [[61,1,9]], `surface-5x9` [[45,1,5]], self-dual BB |

So the import is ~13 new code entries plus a permutation-fitting job on ~9 existing ones. The
permutation matters more than usual here: a schedule is a statement about _specific_ qubit
indices, so a wrong fit silently publishes a schedule for a different qubit layout. The flow
validator run against the **stored** `h` after relabeling is the guard — it fails loudly.

## 4. Open decisions (my recommendations)

1. **What is one stored circuit — one round or d rounds?** Recommendation: canonical body =
   **one round** (`R` ancillas → tick-scheduled CX ladder → `M` ancillas); the
   **`stim-annotated` body = the full `REPEAT d { … }` memory experiment** with detectors and
   an observable; and a `rounds:d` tag so round count is filterable and the spacetime cost is a
   multiplication away.
   - The round is what the paper actually evaluates and what the flow criterion validates;
     d rounds is a _use_ (memory, lattice surgery, single-shot), not a property of the schedule.
   - `REPEAT` is not an obstacle either way: `_compute_depth_and_gates` and
     `_entangling_depth_from_ticks` already multiply through repeat blocks, so a d-round body
     would report correct metrics and stay compact.
   - The counter-argument (single-shot vs d-round codes only become comparable at full protocol
     cost) is real, but is better served by `rounds:d` + per-round metrics than by baking a
     round count into the stored body — especially for `self-dual-bbcode`, whose d is unknown.
2. **Where do the Hadamards go?** asyndrome emits `H a; CX a d; H a` around _every_ X-check,
   so an ancilla with w checks costs 2w Hadamards. The equivalent compact form puts one `H` at
   the ancilla's first active tick and one at its last — the intermediate pairs cancel, since
   the ancilla is idle in between. Measured with `circuit_properties`: surface-5x5 baseline
   160 → 104 gates, bbcode-72 alpha 864 → 504; `two_qubit_gate_count` and `depth` are identical.
   Both validate. Store the compact form: the schedule is the paper's content, the per-check
   wrapping is an artifact of their emitter, and their own noise model puts error per ancilla
   per _tick_ (not per gate), so the extra Hadamards are noise-free in their evaluation anyway.
3. **Are these fault-tolerant?** Tag `ft` only where we can say so. The paper's claim is about
   _logical error rate under a specific decoder and noise model_, not a distance-preservation
   proof. Safest: tag `ft` (a d-round SE circuit for a distance-d code is the standard FT
   construction) but do **not** invent a `distance:N` tag from the paper's numbers.
4. **New tags.** `schedule:alpha` / `schedule:depth-optimal` / `schedule:google` /
   `schedule:trivial`, and `decoder:bp-osd` / `decoder:pymatching` / … (the alpha schedules are
   co-designed with a decoder — that is the paper's point, and two circuits for the same code
   differ _only_ by it). Both need a prefix rule in `categorizeTag()`; `schedule:` → `method`,
   `decoder:` → `method`. Also `connectivity:` — the noise model is IBM Brisbane, i.e. heavy-hex,
   though the schedules themselves assume all-to-all ancilla–data connectivity.
5. **Naming.** `<code-slug>--alpha-schedule-bp-osd`, `<code-slug>--depth-optimal-schedule`.
   Circuit **names** should read like the other 833 ("AlphaSyndrome schedule (BP-OSD)").

## 5. The ingestion flow, and the two layers

The split follows the one `docs/adding-circuits.md` already prescribes for dataset imports:
**reusable logic in `scripts/add_circuit/`, dataset knowledge in `data-imports/<dataset>/`.**
`add_circuit()` itself needs no change — it is circuit-type agnostic, and `_relabel_qubits`
already leaves qubits `>= n` (our ancillas) alone while permuting the data columns.

End-to-end, one asyndrome schedule becomes one library circuit like this:

```
qecc/<code>.json  ─┐
qecc/<code>/<m>.json ┴─▶  parse            (data-imports/asyndrome)   ── level 2
                          ▶  build_se_round(checks_by_tick, n)        ── level 1
                          ▶  validate_syndrome_extraction_h(...)      ── level 1  ✅ built
                          ▶  add_circuit(circuit, H=h, n=n, ...)      ── level 1  (unchanged)
                             └ dedup / permutation fit / metrics / YAML
                          ▶  annotate (REPEAT-d memory experiment)    ── level 1
```

### Level 1 — general, `scripts/add_circuit/`

| piece                                            | status                                                                                                                                                                                                                                     |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `validate_syndrome_extraction_h` / `_extraction` | **done** — flow criterion, replaces the `NotImplementedError` stub                                                                                                                                                                         |
| `measured_stabilizers`                           | **done** — derives what a round measures; no ancilla bookkeeping stored                                                                                                                                                                    |
| third branch in `scripts/validate_circuits.py`   | **done** — SE circuits are checked, not skipped                                                                                                                                                                                            |
| `build_se_round(checks_by_tick, n, style=...)`   | to do — "layers of (data, ancilla, pauli)" is the general SE schedule form, so the emitter belongs here, not in the importer; `style` picks per-check vs first/last-tick Hadamards (§4.2)                                                  |
| `annotate.build_annotated_se()`                  | to do — R data, `REPEAT d { round }`, terminal readout, consecutive-round detectors, observable. A different builder from `build_annotated()`; the existing "emit only if the DEM builds" gate in `annotate_circuits.py` applies unchanged |

### Level 2 — dataset-specific, `data-imports/asyndrome/`

Done: `rebuild_all.py`, `find_sigma.py`, `sigma_precomputed.json` and `README.md`,
following `data-imports/flag-at-origin/`:

- parse `qecc/*.json` → `h`, `logical` (**Pauli from the string, not the field name**, §3.1b)
- parse `qecc/<code>/<method>.json` → ticks of checks
- the code→stored-slug map, with explicit permutations for the four inconclusive fits
  (surface 5×5/7×7/9×9, `color-oct-9`), and `assume_new=True` for the one new code whose
  invariants collide with a stored code it is not (hyperbolic surface [[36,8,4]] against
  `36-8-4-bpc`); the other 13 take free slugs and need no flag
- the exclusion list — 10 google/trivial schedules — recorded in the README with the reason
- naming, notes and tags (§4.4, §4.5); classify-only by default, `--write` to import

All done, along with `data_yaml/tools/asyndrome.yaml`, the paper record, the
`schedule:`/`decoder:` prefixes in `categorizeTag()`, and dropping "still to come" from
`index.astro`.

### Still open

All 59 valid schedules are imported. What remains is the 10 `google` / `trivial` ones of
§3.1, left out because they do not measure their stabilizers. The cause is now pinned
down to a single mistake shared by all three tick tables in `asyndrome/special.py`: they
visit a plaquette's four corners **in a loop** rather than sweeping it row-wise or
column-wise, and a loop necessarily reverses the relative order on the two qubits a
neighbouring plaquette shares. Of the 576 possible tables 16 are valid, all of them
sweeps; 8 of those also preserve the code distance, and stim's canonical rotated surface
code is one of them. So a corrected schedule is identifiable — but it would be our
circuit rather than the paper's, and the surface codes' `baseline` and `alpha` schedules
already reach the same circuit-level distance. Reporting the bug upstream is the useful
move.

## 6. What the verification actually does

`validate_syndrome_extraction_h(circuit, h, n, logical=None)` returns `'passed'` or
`'failed: <reason>'`, like its siblings. Three checks:

1. **measured** — `measured_stabilizers()` reads `stim.Circuit.flow_generators()`, keeps the
   flows with a trivial input, eliminates those with residual ancilla support, and requires the
   remainder (restricted to qubits `< n`, and carrying a measurement record) to span exactly the
   stabilizer group. Both inclusions are enforced: too little means the syndrome is incomplete,
   too much means an operator outside the group is being measured.
2. **preserved** — `S -> S` for every stabilizer.
3. **logical** — `L -> L` for every logical, when `codes.logical` is available.

All unsigned, matching the sign-free `h` used everywhere else.

Deriving the measured group instead of assuming the measurement order is what makes the check
worth having: it needs no schema change, works on third-party submissions, and catches the
interleaving failure of §3.1 — where every check is applied exactly once, on the right qubits,
and the round still measures nothing.

Cost: 2.6 s for all 69 asyndrome schedules, worst case 0.1 s (bbcode-72, 144 qubits).

Coverage: `scripts/tests/test_syndrome_extraction.py` (13 tests — sequential Steane round;
dropped stabilizer; operator outside the group; no measurements; an unpreserved operator; and
an X/Z pair whose CNOT order is inverted on an odd vs even number of shared qubits) and three
end-to-end tests in `test_validate_circuits.py`. Run against the dataset it reproduces the
59/10 split exactly.
