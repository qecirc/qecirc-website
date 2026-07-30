# QUITS import (arXiv:2504.02673)

Imports syndrome-extraction schedules from
[mkangquantum/quits](https://github.com/mkangquantum/quits) v1.1.0, the artifact of
_"QUITS: A modular Qldpc code circUIT Simulator"_ (Kang, Lin, Yao, Gökduman, Meinking, Brown —
[arXiv:2504.02673](https://arxiv.org/abs/2504.02673),
[Quantum 9, 1931 (2025)](https://doi.org/10.22331/q-2025-12-05-1931)). MIT-licensed.

These are the library's first circuits for balanced-product, hypergraph-product,
lifted-product and lift-connected-surface codes.

## Running it

QUITS needs `stim>=1.13` and this project pins `stim>=1.15,<2`, so there is no separate
environment and no lockfile change — `uv` layers the package on for one command:

```
uv run --with 'quits==1.1.0' python data-imports/quits/rebuild_all.py            # dry run
uv run --with 'quits==1.1.0' python data-imports/quits/rebuild_all.py --write
```

A clone of the artifact repo is only needed for the three classical parity-check matrices the
HGP codes are built from; everything else is constructed by the installed package. Put the
clone beside this one or pass `--dataset PATH`.

**The importer pins `PYTHONHASHSEED` and re-execs itself once.** QUITS' edge colourings
iterate over sets, so their order depends on Python's per-process string hash seed and the
same code and strategy produce a _different_ — equally valid — schedule on every run.
Verified: three runs of one command, three different circuits. QUITS' own `seed=1` covers the
`random` module and not this. Hash randomisation is fixed before the interpreter starts, so
pinning it from inside means re-exec'ing; without it the committed circuits could not be
regenerated from the recorded command, which is most of the point of keeping an importer.
(qLDPC's colourings were checked the same way and are reproducible as they stand.)

Useful flags: `--only bpc` restricts to catalogue keys containing a string, and `--max-n 300`
skips the large codes (see [Size](#size)).

## Dataset, and why this importer calls it

Unlike the asyndrome dataset, **QUITS ships no circuits** — not one `.stim` file is checked in.
It is a generator, so the importer constructs each code and calls
`code.build_circuit(strategy=..., num_rounds=2, basis="Z")`.

With no `error_model` the output is completely noiseless (no `DEPOLARIZE*`, no `*_ERROR`) — the
importer never has to strip noise.

The catalogue lives in [`codes.py`](codes.py), transcribed from the repo's own parameter tables
in `doc/01A_codes_basics.ipynb`. Nothing there is invented: `n` and `k` are asserted against the
constructed code on every run, so a mis-transcribed row fails loudly rather than importing a
mislabelled code.

## What one schedule becomes

One library circuit: **a single syndrome-extraction round**, taken from inside the memory
experiment's `REPEAT` block. Two normalisations, both identities on a steady-state round:

- **Qubit indices.** The library wants data `0..n-1` and ancillas `>= n`. Most strategies
  already do that, but `BbCode`'s `custom` schedule renumbers to X-checks, then data, then
  Z-checks (`BbCode._ensure_custom_qubit_indexing`), so the round is relabelled from the code
  object's own `data_qubits` / `check_qubits`. Skipping this does not corrupt anything quietly —
  the validator reports `measures a group of rank 0`.
- **Reset placement.** `custom` ends its round on `MR`; the library's round begins with `R` and
  ends with `M`. Rotating the reset from the end of one round to the start of the next is the
  same circuit repeated.

Detectors and the observable are dropped — they belong to the memory experiment, and the
`stim-annotated` view rebuilds them by repeating the round `d` times.

Ticks are preserved exactly. The tick assignment is the entire content of a scheduling result,
and `has_ticks()` already stops the pipeline from re-packing it.

## The four schedules

| Strategy          | Circuit name                   | Source of the schedule | Applies to         |
| ----------------- | ------------------------------ | ---------------------- | ------------------ |
| `cardinal`        | Cardinal schedule              | arXiv:2504.02673       | HGP, QLP, BPC, LCS |
| `cardinalNSmerge` | Cardinal schedule (N/S merged) | arXiv:2504.02673       | HGP, QLP, BPC, LCS |
| `zxcoloration`    | ZX-coloration schedule         | arXiv:2308.08648       | all                |
| `custom`          | Bivariate bicycle schedule     | arXiv:2308.07915       | BB only            |

**`source` is the paper that defines the schedule, not the one that defines the code.** Only
`cardinal` and its N/S-merged variant are QUITS' own contribution; the other two are QUITS'
implementations of other people's schedules, and a reader following the link should land on the
work being reproduced. The code's own construction paper is named in the circuit notes instead.

### Tags

`syndrome-extraction`, plus exactly one of:

- `schedule:interleaved` — some tick carries both an X- and a Z-check (`cardinal`,
  `cardinalNSmerge`, `custom`)
- `schedule:xz-separated` — X- and Z-checks run in separate passes (`zxcoloration`)

This is **measured, not assumed**: `interleaves_xz()` reads the check type off each two-qubit
gate (an ancilla is the control of an X-check and the target of a Z-check) and reports whether
any tick mixes them. The source's own vocabulary ("cardinal", "ZX-coloration") lives in the
circuit _name_, where a reader can match it against the paper, rather than in a tag.

No `ft` / `non-ft` tag, following the asyndrome circuits. No `distance-preserving` tag either:
the QUITS paper claims lower depth and better logical failure rate, not distance preservation,
and the library does not invent claims its sources do not make. (The repo ships
`examples/circuit_distance_search.py`, which would compute circuit-level distance directly —
that is the route if we ever want the claim as a measurement rather than a citation.)

## One view the ZX-coloration schedules do not get

Every circuit here is valid and validated, but the `zxcoloration` rounds get no
`stim-annotated` body — one per code, 25 in total. They are structurally two sub-rounds: reset
the Z-ancillas, run their checks, measure them, then reset the X-ancillas and do the same. A
reset _after_ a measurement is exactly what `round_check_matrix` refuses, deliberately — it only
reads a round shaped `reset → unitary → measure`, because that is the shape it can pull an
ancilla's operator back through.

Nothing is lost but the annotated memory-experiment view: validation never depends on that
function, and the schedule, metrics and circuit body are all unaffected. Generalising it to
sequential sub-rounds would recover them, and is worth doing if these circuits are wanted in
Crumble with detectors.

## Every import is gated on validation

`validate_syndrome_extraction_h` runs before anything is written: the round must measure exactly
the code's stabilizer group and preserve every stabilizer and logical, checked against the
**stored** code after any relabeling. **All 69 schedules pass.**

## Code identity

Three results needed care, and none of them was decided by the dedup search alone.

### Permutations onto stored codes

BB [[108,8,10]] and [[144,12,12]] already exist in the library under a different qubit order,
and the dedup permutation search exceeds its budget on them — these codes have enormous
automorphism groups. The permutations in [`sigma_precomputed.json`](sigma_precomputed.json) were
not recomputed here: **QUITS labels these codes exactly as autqec does** — identical X and Z row
spaces, verified, no X↔Z swap — so the σ derived by `data-imports/autqec/find_sigma.py` applies
unchanged. `add_circuit` re-verifies each one by row-space equality on every run, so a stale
entry fails loudly rather than silently.

### Three invariant collisions, all refuted

Three codes share `[[n,k,d]]` with an unrelated stored code, so the dedup screen offers a
candidate that is **not** the same code. All are refuted in `ASSUME_NEW`:

| Code            | Candidate                          | Refutation                                                                                                                                                                                  |
| --------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| BPC [[36,8,4]]  | `36-8-4` (Hyperbolic Surface Code) | Row-space ranks are 14/14 here and 11/17 there. Rank is a permutation invariant and an X↔Z swap gives 17/11, so no relabeling reconciles them.                                              |
| BPC [[108,8,8]] | `108-8-10` (Bivariate Bicycle)     | Distance 8 vs 10, and permutation-equivalent codes have equal distance. Independently, ISD sweeps find weight-8 codewords in this code's X row space and none in the stored one's.          |
| BB [[90,8,10]]  | `90-8-10` (Bivariate Bicycle)      | Enumerating every weight-4 vector against each X row space gives **0** codewords here and **90** there. The weight enumerator is a permutation invariant, so no relabeling reconciles them. |

They therefore get **distinct slugs** — `36-8-4-bpc`, `90-8-10-bpc` and `90-8-10-autqec`. This
matters more than it looks:
`assume_new` skips the dedup check, so nothing downstream would notice that the default
`n-k-d` slug belongs to an unrelated code, and `overwrite=True` would replace it. The importer
now **refuses** to import any assume-new code whose slug is already taken.

### The second [[90,8,10]], and its slug

BB [[90,8,10]] is the same code autqec imports, and autqec's PR (#127) files it as
`90-8-10-autqec`. **This import uses that slug deliberately**, so whichever of the two lands
first creates the single shared entry and the other deduplicates onto it — `add_circuit` files a
matched submission under the stored slug and ignores `code_slug`, so no duplicate can arise
either way.

Its name says what actually distinguishes it: **Bivariate Bicycle Code (Bravyi Table 3)**. The
polynomials here are Table 3's (15,3) entry verbatim — `A = x^9 + y + y^2`, `B = 1 + x^2 + x^7` —
and the stored `90-8-10` carries the alias "(15,3) BB6 code" while being a different code by the
weight-4 count above. Which of the two is mislabelled is a question for the stored entry, not for
this import.

## Size

`h` is (n−k) × 2n, so the stored footprint grows as n². The catalogue spans [[36,8,4]] to
[[1428,184,≤24]], and this import takes `data_yaml/` from **62 MB to 214 MB** — of which the
seven largest codes are ~93%. QLP [[1428,184]] alone is 56 MB, its code entry 14 MB of that.
`--max-n 300` drops those seven, keeping 47 of the 69 circuits for ~9 MB.

Most of that is duplication rather than data: 136 MB of the 171 MB under `circuits/` is
`originals/*.original.yaml`, which stores the submitted matrices once per _circuit_ — the copies
for one code are byte-identical (same md5). That is a pipeline property, not something this
import can fix, and it is the obvious place to look if the size ever matters.

The circuits themselves are small throughout: the [[1428,184,≤24]] round is a 112 KB `.stim`.

On the site itself the matrices are not sent unless asked for: they already load lazily from
`/api/codes/<slug>/matrices`, and above `MATRIX_INLINE_ENTRY_LIMIT` the code page offers a
download instead of rendering them — a 1244 × 2856 matrix is neither readable as text nor worth
shipping to every reader who expands the section.

## Distances

Distances come from the source tables, never from a computation done here:

- **BB** — Bravyi et al. arXiv:2308.07915, Table 3. [[360,12,≤24]] and [[756,16,≤34]] are the
  paper's **upper bounds**, and the circuit notes say so.
- **BPC** — Tiew and Breuckmann, arXiv:2411.03302.
- **HGP** — the classical code's distance, named in the shipped matrix's filename. HGP(C, C)
  has d = min(d_C, d_Cᵀ); each shipped matrix has full row rank, so k_Cᵀ = 0, d_Cᵀ is infinite
  and the quantum distance is the classical one. The `k` assertion is what confirms k_Cᵀ = 0 on
  every run.
- **LCS** — the closed form d = min(L, 2ℓ+1) of Old et al. arXiv:2401.02911, with QUITS'
  `length` = ℓ+1. The same paper's n = [(ℓ+1)² + ℓ²]L and k = L reproduce the constructed codes
  exactly, which is what makes the third formula safe to use.
- **QLP** — Xu et al. arXiv:2308.08648. All four are **upper bounds**.
