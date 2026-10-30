# autqec — logical Clifford gates from code automorphisms

Import of the example circuits of **"Fault-Tolerant Logical Clifford Gates
from Code Automorphisms"**, Sayginel, Koutsioumpas, Webster, Rajput, Browne —
[arXiv:2409.18175](https://arxiv.org/abs/2409.18175) — computed with the
authors' [autqec](https://github.com/hsayginel/autqec) package
(`data_yaml/tools/autqec.yaml`).

These are the library's first **logical-gate** circuits: unitary circuits that
preserve a code's stabilizer group while enacting a non-trivial logical
Clifford on its encoded qubits. They introduced the `logical-gate` type tag,
the `logical_action` circuit-YAML field, and the `validate_logical_gate_h`
check (see below).

## Dataset

A checkout of `hsayginel/autqec` is expected **next to the website repo**
(`../autqec`, like the other dataset imports); `--dataset` overrides. Import
built against commit `db614a9` (2025-04-29).

The expensive step of the paper's pipeline — finding the automorphism groups
with MAGMA/Bliss — is already done: the repo commits the generators as
pickles. This importer replays only the cheap deterministic synthesis, per
code and per symmetry family:

| family       | pickle                               | physical gate set |
| ------------ | ------------------------------------ | ----------------- |
| automorphism | `examples/auts_data/auts_<code>.pkl` | ⟨H,S⟩ + SWAP      |
| ZX-duality   | `ZX_dualities_<code>.pkl`            | H + SWAP          |
| XY-duality   | `XY_dualities_<code>.pkl`            | S + SWAP          |
| YZ-duality   | `YZ_dualities_<code>.pkl`            | √X + SWAP         |

For each group **generator**: build the physical circuit
(`circ_from_aut` / `circ_from_*_duality`), apply the Pauli corrections that
fix the stabilizer signs (`logical_circ_and_pauli_correct`), convert to STIM,
and relabel to the stored code's canonical qubit order.

## Codes covered

| paper code                            | stored slug       | status                                                                                            |
| ------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------- |
| [[4,2,2]]                             | `4-2-2`           | seeded by this import                                                                             |
| [[5,1,3]] perfect code                | `five-qubit-code` | existing (fitted, perm `[3,2,1,0,4]`)                                                             |
| [[7,1,3]] Steane                      | `steane-code`     | existing (fitted, perm `[2,1,4,0,5,3,6]`)                                                         |
| [[17,1,7]] (codetables best-distance) | `17-1-7`          | seeded by this import (its `H_symp_n17k1.npy` ships in the dataset's `codetables/parity_checks/`) |
| [[72,12,6]] bivariate bicycle         | `72-12-6`         | existing (autqec's labeling matches the stored code, so the hash dedup fits it directly)          |
| [[108,8,10]] bivariate bicycle        | `108-8-10`        | existing (fitted via `sigma_precomputed.json`, see below)                                         |
| [[144,12,12]] Gross code              | `144-12-12`       | existing (fitted via `sigma_precomputed.json`, see below)                                         |

### Precomputed qubit permutations (`sigma_precomputed.json`)

For `108-8-10` and `144-12-12` the canonical-hash dedup misses and the
structural permutation finder exceeds its budget (automorphism-rich BB
codes), so their σ was computed offline: enumerate **all** weight-6 codewords
of each X/Z row space (ISD sweeps until stable; they span the full spaces and
counts match across sides — 54 each for n=108, 72 each for n=144), build the
colored qubit/codeword incidence graphs, and extract the isomorphism by
composing BLISS canonical permutations. Each σ is verified by exact
symplectic row-space equality — both offline and again by `rebuild_all.py` on
every run before it is used (`sigma_verifies`), so a stale or wrong entry
fails loudly. Convention: `sigma[new] = old`, matching
`compute_circuit_data(qubit_permutation=...)`.

### The two [[90,8,10]] codes

autqec's [[90,8,10]] is a **genuinely different construction** than the
stored `90-8-10`: the stored code's X-space has 90 weight-4 + 600 weight-6
codewords, while autqec's has exactly 45 weight-6 and none of weight 4.
Low-weight enumerators are permutation invariants, so no relabeling can
reconcile them — this is a proof of inequivalence, not a search failure.
autqec's version is therefore imported as its own visible code entry,
`90-8-10-autqec` ("Bivariate Bicycle Code (autqec)"), with circuit notes
spelling out the distinction. The check matrices of both stay dumped under
`skipped_bb_codes/` for independent verification.

Also not yet imported: the two-block embedded-code gates
(`examples/embedded_codes/` — circuits act on an embedded larger code, needs a
data-model decision).

## The codetables section (`--section codetables`)

The paper's n ≤ 28 sweep over the **best-known-distance [[n,k]] stabilizer
codes** from Grassl's [codetables.de](https://codetables.de). Unlike the
examples, the dataset commits _finished circuits_ (Pauli corrections included)
in `codetables/logical_gates/gates_n{n}k{k}.pkl` (automorphism family) and
`codetables/ZX_dualities/logical_gates/` (ZX family); parity checks ship as
`codetables/parity_checks/H_symp_n{n}k{k}.npy`.

Curation decisions (all deliberate):

- **Only d ≥ 3 codes are imported.** Distances are not in the dataset; they
  are fetched once from codetables.de by `fetch_codetables_distances.py` into
  the committed cache `codetables_distances.json` (`d_lower` = best known
  construction; 31 of 214 pairs have non-tight bounds). The d ≤ 2 tail (95
  codes, 82% of the circuits) is detection-only-or-worse and stays out.
- **Hidden by default.** These are mostly anonymous record-holders (103 of
  119 root in an unnamed "stored generator matrix" on codetables.de), so
  their code entries get the `codetables` tag: excluded from the /codes
  listing until the tag is selected in the filter, excluded from every
  displayed count, fully searchable (see `HIDDEN_CODE_TAG` in
  `src/lib/constants.ts`). Slugs are prefixed `ct-` (`ct-15-7-3`) because
  four parameter-twins of _different_ stored codes exist (`15-7-3`,
  `16-6-4`, `20-2-6`, and the [[5,1,3]] frame twin below).
- **Identified codes are imported as normal, visible codes** (see
  `CT_IDENTIFIED` in `rebuild_all.py`): [[7,1,3]] _is_ the Steane code and
  [[8,3,3]] _is_ the Gottesman code (verified permutation-equivalent via the
  site's dedup machinery — their codetables circuits attach to the existing
  entries); [[17,1,7]] is the same dataset code as the examples section;
  [[6,1,3]] is THE six-qubit code (unique up to equivalence) and seeds the
  normal code `6-1-3`.
- **Two near-identifications stay hidden:** the codetables [[5,1,3]] is
  local-Clifford-equivalent to `five-qubit-code` (the code is unique) but not
  permutation-equivalent, so its circuits cannot be relabeled onto the stored
  entry — it lives as `ct-5-1-3`. The [[11,1,5]] is plausibly the quantum
  dodecacode (Gottesman thesis, Table 8.5) but no machine-readable reference
  tableau was available to verify; identification welcome (`ct-11-1-5`).

## Gate translation (verified, not assumed)

autqec circuits are lists of 1-indexed gate tuples over
`{H, S, Xsqrt, GammaXYZ, GammaXZY, SWAP, CNOT, CZ, C(X,X), X, Y, Z}`. The STIM
mapping (`GATE_MAP`) was verified against autqec's own
`clifford_circ_stab_update` on every 1-/2-qubit Pauli input, **including
signs** (autqec tracks phases in units of i with Y stored as XZ):
`Xsqrt → SQRT_X`, `GammaXYZ → C_XYZ` (X→Y→Z→X), `GammaXZY → C_ZYX`,
`CNOT → CX` (control first), `C(X,X) → XCX`.

## What is claimed, and how it is checked

Each circuit YAML carries a `logical_action` field: the induced logical
Clifford as a STIM circuit on the code's k logical qubits (e.g. `S 0`),
**stated in the stored code's logical basis** (`codes.logical`), not the
paper's — the bases differ, so the action is recomputed after relabeling
(binary symplectic action mod stabilizers, decomposed back into gates with
autqec's `circ_from_symp_mat`).

`npm run validate:circuits` routes the `logical-gate` tag to
`validate_logical_gate_h`, which recomputes both properties from the `.stim`
body: (1) the circuit preserves the stabilizer group of `codes.h`; (2) it
induces exactly the claimed `logical_action`. Checks are at the binary
symplectic level (mod logical Paulis) since the stored matrices are
sign-free. The importer runs the same check before writing anything.

Generators whose induced action is the identity mod logical Paulis (most of
them) are skipped — they permute stabilizers without touching the logical
qubits. Duplicate circuits arising in several families are deduped on the
canonical STIM body.

## Tagging decisions

- `logical-gate` — the type tag (added to `TYPE_TAGS` in
  `src/lib/tag-categories.ts`).
- `logical-op:<STIM-gate>` — one per distinct gate in the logical action
  (e.g. `logical-op:S`, `logical-op:CX`), mirroring `logical-state:*`.
- `transversal` + `ft` — physical circuit uses single-qubit gates only;
  inherently fault-tolerant (errors cannot spread).
- `swap-transversal` (no `ft`) — single-qubit gates + SWAPs; fault-tolerant
  only where SWAPs are error-benign (shuttling ion traps, atom arrays), so no
  unconditional `ft` claim. The circuit notes say this.
- Circuits with entangling gates would get neither (none in v1).

Note on [[4,2,2]]: k=2, so a _transversal_ physical circuit can still enact an
_entangling logical_ gate (e.g. S⊗4 ↦ logical CZ) — the `transversal` tag
describes the physical circuit, the `logical-op:*` tags the logical action.

## Rebuild

```bash
uv run python data-imports/autqec/rebuild_all.py            # classify (dry run)
uv run python data-imports/autqec/rebuild_all.py --write
npm run format && npm run validate:yaml && npm run validate:circuits && npm run db:create
```

Re-running preserves previously assigned `qec_id`s (matched on the
`<code>--<circuit>` stem).
