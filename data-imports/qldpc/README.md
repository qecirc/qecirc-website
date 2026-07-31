# qLDPC import

Imports circuits from [qLDPCOrg/qLDPC](https://github.com/qLDPCOrg/qLDPC) v0.3.2, a library for
constructing and analysing quantum LDPC, stabilizer and subsystem codes. Apache-2.0.

qLDPC is a **generator, not a dataset** — it ships no circuits — so this importer constructs
each code and calls it. Three kinds of circuit come out:

| Kind                | From                                          | Count |
| ------------------- | --------------------------------------------- | ----- |
| Syndrome extraction | `get_memory_experiment_parts`, two strategies | 28    |
| Encoding            | `get_encoding_circuit`                        | 15    |
| \|0⟩ preparation    | `get_encoding_circuit(only_zero=True)`        | 15    |

## Running it

qLDPC needs `stim>=1.16` and this project pins `stim>=1.15,<2`, so there is no separate
environment and no lockfile change:

```
uv run --with 'qldpc==0.3.2' python data-imports/qldpc/rebuild_all.py            # dry run
uv run --with 'qldpc==0.3.2' python data-imports/qldpc/rebuild_all.py --write
```

`--only surface` restricts to catalogue keys containing a string; `--kinds se` restricts to
circuit kinds. Re-running is idempotent — `qec_id`s are kept.

## What is covered, and what is not

The catalogue ([`codes.py`](codes.py)) is a choice rather than a transcription, because these
circuits work on essentially every CSS code qLDPC can build. It is drawn along two lines: codes
**already in the library**, so the circuits attach to existing entries and become comparable
with the schedules and encoders already stored for them; and a few qLDPC constructions the
library has no entry for at all (the Iceberg codes [[4,2,2]] and [[6,2,2]], toric d=6, and two
hypergraph product codes).

`n` and `k` are asserted against the constructed code on every run. So is `d`, against qLDPC's
own exact distance — except for the bivariate bicycle code, where that search is a hard
combinatorial problem that does not terminate; its distance comes from Bravyi et al.
arXiv:2308.07915 Table 3 instead, and `verify_d=False` records that.

**Two things are deliberately excluded.**

- **Subsystem codes.** `BaconShorCode` and `SHYPSCode` build, and their circuits validate
  cleanly against `get_stabilizer_ops()`. The blocker is the data model: the library derives
  k as n − rank(h), which is only correct for stabilizer codes, so Bacon-Shor [[9,1,3]] would
  be stored as **[[9,5,3]]** and SHYPS [[49,9,4]] as **[[49,25,4]]**. Storing them needs a
  gauge-group field and a k that is not derived. (Note the failure is _not_ in the validators:
  `code.matrix` on a subsystem code is the **gauge** group, and validating against that
  correctly fails.)
- **Transversal logical Clifford gates.** `transversal.py` is an independent implementation of
  arXiv:2409.18175 and maps exactly onto the `logical-gate` type — but that type is not on this
  branch, and `get_transversal_ops` requires GAP/GUAVA: without it the call drops into an
  interactive prompt and blocks forever, and only the five-qubit and C4 codes complete from
  hard-coded groups.

## Provenance

Two different `source` values, because these circuits have two different origins:

- **Syndrome extraction → [arXiv:2109.14609](https://arxiv.org/abs/2109.14609)** (Tremblay,
  Delfosse, Beverland). Both `EdgeColoring` and `EdgeColoringXZ` implement Algorithm 1 of that
  paper, so the paper is the source and the library is the tool.
- **Encoders and |0⟩ preps → `qldpc`**, naming the tool rather than a work, as
  `source: circuit-synth` already does. They are tableau syntheses and reproduce no published
  construction.

## Each circuit records how to rebuild it

Every circuit's notes end with the qLDPC expression that produces it, for example

```
Reproduce with: qldpc.circuits.get_encoding_circuit(qldpc.codes.ToricCode(4), only_zero=True)
```

Asked for by qLDPC's author ([qLDPCOrg/qLDPC#554](https://github.com/qLDPCOrg/qLDPC/issues/554)),
and worth doing on its own terms: a reader who wants to rebuild one should not have to
reverse-engineer the constructor from `[[n,k,d]]`.

It cannot drift from the circuit, because the constructor string **is** what the importer
evaluates — `CodeSpec.constructor` replaced the lambda that used to sit there, and
`CodeSpec.build()` is `eval` over it. A snippet that no longer built the code would fail the
import rather than mislead a reader. For a syndrome-extraction round the line also says what
`se_round` takes off, since the stored body is the cycle's `REPEAT` block without its detectors.

## Tags

- SE: `syndrome-extraction` plus `schedule:xz-separated` — both strategies run the X- and
  Z-checks in separate passes. That is **measured** per circuit by `interleaves_xz()`, which
  reads the check type off each two-qubit gate, not asserted from the strategy name.
- Encoders: `encoding`, `non-ft`. Preps: `state-preparation`, `logical-state:zero`, `non-ft`.

**No `distance-preserving` tag, and the reason is on the circuit page.** qLDPC states plainly,
in both strategy docstrings, that they are _not_ guaranteed distance-preserving or
fault-tolerant, and both encoders are documented as non-FT (FT encoding is upstream issue
#327). The library tags claims its sources make; here the source makes the opposite claim, so
it goes in the notes where a reader will see it.

Consistent with the asyndrome circuits, SE circuits carry no `ft`/`non-ft` tag at all.

## Code identity

Three codes are the same code as a stored entry under a different qubit order, and the dedup
permutation search runs out of budget on all three — they are topological codes with large
automorphism groups, exactly the case its column invariants cannot separate.
[`find_sigma.py`](find_sigma.py) settles two of them, reusing
`data-imports/asyndrome/find_sigma.py`'s matcher rather than keeping a second copy of it:

| Code                  | Stored entry                 | Result      |
| --------------------- | ---------------------------- | ----------- |
| rotated surface d=7   | `rotated-surface-code-d-7`   | σ verified  |
| unrotated surface d=3 | `unrotated-surface-code-d-3` | σ verified  |
| toric d=4             | `16-2-4`                     | **refuted** |

The toric code is **not** the stored [[16,2,4]]. Its X row space has 8 codewords of weight 4
and 16 of weight 6; the stored code has 12 of weight 4 and none of weight 6. Weight enumerators
are permutation invariants and the Z spaces differ the same way, so no relabeling reconciles
them — it is imported as a distinct code, `16-2-4-toric`.

That last case needed a guard. `assume_new` skips the dedup check, so nothing downstream would
notice that the default `n-k-d` slug belongs to an unrelated code, and `overwrite=True` would
replace it. `owns_slug()` refuses in that case — while still recognising an entry this import
wrote on an earlier run, by canonical hash, so re-running stays idempotent.

## Two changes outside this directory

- **`round_check_matrix` now reads X-basis rounds** (`scripts/add_circuit/circuit_validate.py`).
  qLDPC holds its ancillas in X — `RX` … `MX`, with Z-checks applied as `CZ` — where the
  existing SE circuits hold them in Z. The two are the same construction in different frames,
  but the helper only knew `R`/`M`, so all 28 rounds returned no check map and silently lost
  their annotated memory experiment. It now tracks the basis each ancilla is prepared in, pulls
  back that operator, and requires the measurement basis to match the reset basis. Covered by
  two new tests in `scripts/tests/test_syndrome_extraction.py`.
- The importer passes the **CSS pair** (`Hx=`/`Hz=`) rather than the symplectic `H=`. Both name
  the same code and give the same canonical form and hash, but `H=` routes through
  `split_h_to_css`, which row-reduces to _detect_ CSS structure — and that RREF basis, not the
  submitted one, is then stored as the circuit's original matrices. For an LDPC code that
  replaces weight-6 checks with dense rows, losing the structure the code is defined by. See
  qecirc/qecirc-website#138; non-CSS codes have no pair, so the five-qubit code keeps `H=`.
