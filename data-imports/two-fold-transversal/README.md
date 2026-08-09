# two-fold-transversal — depth-one two-local logical Clifford gates

Import of the certified circuit survey of **"Beyond transversality: structure
of Clifford circuits for CSS codes"**, V. V. Albert —
[arXiv:2608.05688](https://arxiv.org/abs/2608.05688) — from the paper's
companion repository ([valbert4/two-fold-transversal](https://github.com/valbert4/two-fold-transversal),
`data_yaml/tools/two-fold-transversal.yaml`).

A checkout of the companion repo is expected **next to the website repo**
(`../two-fold-transversal`, like the other dataset imports); `--dataset`
overrides. Import built against its initial 2026-08 state.

## Dataset

Two JSON files hold 136 CSS codes with stabilizers/logicals as Pauli strings
and 12,586 circuits as gate strings (grammar: the dataset's `data/README.md`):

| file                     | codes | claim                                                            |
| ------------------------ | ----- | ---------------------------------------------------------------- |
| `full_codes_depth1.json` | 78    | depth-one two-local circuits generate the **full** Sp(2k,2)      |
| `ldpc_codes_depth1.json` | 58    | generators realize a logical group of exactly the recorded order |

Every gate string is one **depth-one two-local** ("two-fold transversal")
circuit: a single layer in which each qubit is touched by at most one
two-qubit gate, optionally followed by a compensating qubit permutation.

**The generating-set policy** (the dataset ships raw search output — 12,586
gate strings with heavy redundancy at the logical level; the library keeps a
set that still generates each code's recorded logical group):

1. Generators whose logical action is the **identity** are dropped (21 across
   both files — they enact no gate; autqec precedent).
2. One circuit is kept per **distinct logical action** — dropping duplicate
   actions provably cannot change the generated logical group.
3. Full-group codes are further cut to the **certificate's verified generating
   prefix** (`C_generators_used`: the paper's exact Schreier–Sims certificate
   proved the first m distinct actions already generate Sp(2k,2); median 6,
   max 183 per code). The 10 codes certified by order-free methods have no
   such prefix and keep every distinct action, as do all QLDPC codes — the
   strongest reduction that provably preserves their recorded group.

`--all-circuits` disables step 3. Re-runs **reconcile**: two-fold circuits and
seeded codes that the current policy no longer keeps are pruned; files of
other tools are never touched.

## Gate map

| token      | STIM             | note                                  |
| ---------- | ---------------- | ------------------------------------- |
| `S<q>`     | `S q`            | Z-diagonal phase                      |
| `V<q>`     | `SQRT_X q`       | X-basis phase (HSH)                   |
| `CZ<i,j>`  | `CZ i j`         |                                       |
| `cz<i,j>`  | `XCX i j`        | X-basis CZ                            |
| `CX<i,j>`  | `CX i j`         | control i, target j                   |
| `H<q>`     | `H q`            |                                       |
| `(a,b,..)` | trailing `SWAP`s | cycle a→b→…, applied last             |
| `^`        | —                | layout separator (ZX-duality strings) |

The conversion was verified against the paper's own reference parser
(`data/certify/core.py::decode`) on **all 12,586 gate strings**: exact binary
symplectic equality, code preservation + logical image via the paper's `Code`
class, and a depth-one two-local audit of the emitted STIM (trailing SWAPs
exempt — free routing, as elsewhere in the library).

**Signs.** The dataset is binary-symplectic (sign-free), so each STIM circuit
is one Pauli frame of its gate. That is exactly the equivalence class the
sign-free `validate_logical_gate_h` checks — a logical gate is only defined up
to logical Paulis. Unlike autqec there is no Pauli-correction layer to replay,
because the dataset carries no sign information at all.

## Codes

All 136 codes are imported as **visible** entries (an explicit decision — no
`codetables`-style hiding), named per the paper's Table III families with the
`[[n,k,d]]` in the name, and tagged:

| source      | family (Table III)                       | family tags               | zoo link (fetch-verified) |
| ----------- | ---------------------------------------- | ------------------------- | ------------------------- |
| `se`        | self-dual even codes                     | —                         | —                         |
| `ml`        | self-dual doubly-even codes              | —                         | —                         |
| `eczoo`     | four individually named codes            | —                         | per code, see below       |
| `qecdb`     | qecdb.org (Simon Burton)                 | —                         | —                         |
| `2bga`      | two-block group-algebra                  | `two-block-group-algebra` | `/c/2bga`                 |
| `coset2bga` | coset 2BGA                               | `two-block-group-algebra` | —                         |
| `toricdir`  | bivariate bicycle                        | `bivariate-bicycle-code`  | `/c/qcga`                 |
| `kasai`     | affine block-circulant                   | —                         | —                         |
| `cc`        | clustered-cyclic                         | —                         | —                         |
| `copycup`   | abelian balanced-product                 | `balanced-product`        | `/c/balanced_product`     |
| `mm`        | multivariate multicycle                  | —                         | —                         |
| `dd422`     | [[4,2,2]]-concatenated symplectic double | `concatenated`            | —                         |
| `cons:*`    | the paper's own constructions            | per construction          | per construction          |

`CSS` and `self-dual` are auto-detected by the pipeline, never hand-added.
`LDPC` is added to every `ldpc_codes_depth1.json` entry (the paper's QLDPC
table), not derived from the check weights. The four `eczoo` codes: the
weight-4/degree-4 [[10,2,3]] is the **rotated toric code** (`/c/toric`), the
other [[10,2,3]] the **binarized Galois-qudit code** (`/c/stab_10_2_3`),
[[14,3,3]] the **constant-excitation phantom code** (`/c/constant_excitation`),
and [[12,2,4]] the **carbon code** (dedups onto the stored `carbon-code`).
A missing zoo link means no page was confirmed to exist at import time, not
that none exists.

### Dedup / fitting

Hash dedup first; when it misses, a **structural fit** tries every stored code
with the same [[n,k,d]] (`find_code_permutation`, verified by row-space
equality), plus the offline sigmas shared with the autqec import
(`data-imports/autqec/sigma_precomputed.json`) — which is how the
**gross code** `[[144,12,12]]cons:gross144` lands on the stored `144-12-12`
(the paper uses the common BB labeling; verified, never assumed). The
[[12,2,4]] carbon code fits structurally. The two [[16,2,4]] entries do
**not** fit the stored `16-2-4` (genuinely inequivalent row spaces) and
become their own entries with source-suffixed slugs.

Slug policy for new codes: `n-k-d`, suffixed with the source shorthand and
then the uuid octet only on collision (stored or within-run).

## Circuits

Per circuit: converted, relabeled to the stored code's canonical qubit order,
its logical action recomputed **in the stored code's logical basis** and
written as `logical_action`. At this volume the importer computes the action
with one batched GF(2) solve per circuit — numerically identical to the
pipeline's `induced_logical_action`, asserted against it on the first circuit
of every code — and refuses to write any circuit whose logical image leaves
the normalizer span. The authoritative per-circuit check is
`npm run validate:circuits`, which re-verifies every stored circuit with the
pipeline's own `validate_logical_gate_h`. Conversion fans out over worker
processes (`--workers`, default 8); all writes stay in the main process,
which also caches the stored-code dedup index instead of reloading the
library per code (together ~40× wall-clock over the naive loop).

**Naming and classification.** A circuit whose exact action is short is named
by it ("SWAP-transversal logical CNOT(4,5)·CNOT(11,10)"). For the rest, the
gate list of stim's elimination decomposition is an artifact of the
decomposition — naming by it made every circuit look alike — so the name
states the action's **structural class** in the paper's own layer taxonomy
(Z-diagonal S/CZ, X-diagonal √X/XX, CNOT circuit, qubit permutation,
Hadamard-type, general Clifford), classified from the 2k×2k action matrix,
plus its support: "Depth-one two-local logical Z-diagonal (S/CZ) gate on 8/12
qubits (gen 173)". Every circuit carries a `logical-class:*` tag for
filtering; `logical-op:*` tags are kept only where the exact decomposition is
short enough to be faithful.

Tags: `logical-gate`, `two-fold-transversal`, structure
(`transversal`+`ft` / `swap-transversal` / none for entangling depth-one, per
the autqec FT policy — entangling circuits make no FT claim), and the
class/op tags above. Names:
"Depth-one two-local logical S(0)·CZ(0,1)", falling back to
"(gen N)" provenance names when the action is long. The dataset's per-code
generator index and label are always in the notes.

The dataset-frame stabilizers/logicals are preserved as shared
content-addressed `original_matrices`; the pre-relabeling STIM goes to
`circuits/originals/`.

## Run

```bash
uv run python data-imports/two-fold-transversal/rebuild_all.py            # classify only
uv run python data-imports/two-fold-transversal/rebuild_all.py --write
```

Then the standard sequence: `npm run papers:add -- 2608.05688`,
`uv run python scripts/annotate_circuits.py`, `npm run format`,
`npm run validate:yaml && npm run validate:circuits`, `npm run db:create`.

## Provenance / certification

Nothing is taken on trust from this import's side: every stored circuit is
individually re-validated by `validate:circuits`. The _group-level_ claims
(full Sp(2k,2), exact orders) are the paper's, backed by its machine-checkable
certificates (`data/certify/` in the dataset repo) — the circuit notes cite
them but the website does not re-prove them.
