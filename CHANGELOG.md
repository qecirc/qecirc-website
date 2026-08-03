# Changelog

All notable changes to this project will be documented here. Versioning follows
the source-of-truth `package.json` version.

## Unreleased

### Fixed

- **`/api/search` was cached at the edge for a week, keyed on `?q=`.** `middleware.ts`
  stamps `s-maxage=604800` on any response without its own `Cache-Control`, which is safe
  for a page whose output is fixed at deploy time and not for one whose key space anyone
  can enumerate. `/search` had set its own 600 s for exactly this reason since it was
  written; the quick-search behind it had not. It does now.
- **A zip download only type-checked by accident.** `/api/download` handed a Node `Buffer`
  straight to `Response`, whose `BodyInit` wants a view onto a plain `ArrayBuffer` and not
  the `ArrayBufferLike` union Node declares. The bytes were always right; the types said
  otherwise. It now copies into its own `Uint8Array`, which also stops `.buffer` meaning
  "Node's shared allocation pool" rather than "this zip".
- **Renovate could auto-merge a moving target.** `pyproject.toml` pins `mqt-qecc` to a git
  branch, and `lockFileMaintenance` runs with `automerge: true` — so a weekend lock refresh
  landed whatever that branch pointed at, unread, in the ingestion pipeline. It already had:
  f476ffa1. Git-sourced dependencies and `uv.lock` refreshes now need a human.
- **`.gitignore` ignored a directory nobody uses.** It listed `.worktrees/`, while agent
  worktrees are created under `.claude/worktrees/` — so every worktree showed up as
  untracked in the main checkout. Corrected, narrowly: `.claude/` itself stays tracked,
  because `.claude/agents/` and `.claude/commands/` are committed.
- **Six documentation defects, five of them the same defect: a maintained count.** CLAUDE.md
  said "1028 circuit files", "1019 of 1028" and "one paper backs up to 370 circuits"; each
  was right the day it was written and wrong within days, three times over as imports landed.
  Updating them would only reset the clock, so the counts are **gone** and the arguments they
  supported are stated without one — a paper backs "hundreds" of circuits, and widening
  `toric code` to "any term" matches "all but a handful" because "code" occurs in nearly every
  circuit's text. Same treatment for the stale counts in code comments
  (`index.astro`, `CircuitRow.astro`, `add_circuit/annotate.py`) and for the sample
  `Papers: N, linked to M circuits.` build output quoted in `docs/database.md` and
  `/add-circuit`.
- **CLAUDE.md's static/SSR page lists were wrong on the day they were written**, and read as
  an inventory: `/favorites` was missing from the static list, `/tools` and five `/api/*`
  routes from the SSR one. Replaced with the rule that actually decides it — a route that
  reads SQLite is `prerender = false` — plus examples marked as examples and a pointer to
  `grep -rn "prerender" src/pages/`, which cannot go stale.
- **The matrices lived in three places at once, on paper.** They moved to content-addressed
  `data_yaml/matrices/<digest>.yaml` and no `*.original.yaml` has existed since, but
  `docs/database.md` still omitted the directory from its tree and filed matrices under
  `circuits/originals/`, `/add-circuit` still named `*.original.yaml`, and
  `docs/adding-circuits.md` contradicted **itself** — line 444 against its own "Original
  submission" section. All four now match CLAUDE.md and the pipeline.
- **"The pipeline always preserves the original" was never true.** The flag gadgets are
  written directly with the pipeline helpers, so there is nothing earlier to preserve: they
  have no `circuit_originals` row and no "Original submission" section, which `index.astro`
  already knew and the docs did not. Corrected in `docs/adding-circuits.md`,
  `docs/adding-circuits-agent.md`, `docs/database.md` and CLAUDE.md's schema comment.
- **The QUITS README pointed at a file in an unmerged branch.**
  `data-imports/autqec/find_sigma.py` does not exist here — that import is still PR #127 —
  so a reader had no way to reproduce the two BB permutations. The README now says so
  outright and points at the matcher that _is_ in the repo
  (`scripts/add_circuit/find_sigma.py`, with `data-imports/qldpc/find_sigma.py` as the
  worked example of driving it); `sigma_precomputed.json`'s two provenance strings say the
  same. The permutations themselves are untouched, and `add_circuit` still re-verifies each
  by row-space equality on every run — which is what makes shipping them acceptable.
- **The agent doc's "Current tags" table listed about a third of the vocabulary.** It was
  missing seven code tags (`LDPC`, `topological`, `subsystem`, `bivariate-bicycle-code`, …)
  and six circuit tags and families (`gadget`, `partial-ft`, `x-type`/`z-type`, `distance:*`,
  `circuit-distance:*`, …) while telling the agent it may only use tags that already exist.
  A second copy of a table that imports extend was never going to hold, so it is replaced by
  the query against `tags`/`taggings` that returns the real vocabulary, plus the shape of it
  in prose.
- **`scripts/annotate_circuits.py` described itself as state-prep/encoding-only** though it
  has dispatched to `build_annotated_se` for syndrome extraction since that landed. Its
  docstring now covers both branches and why a round cannot be reset-free.
- **The qLDPC rounds were never measured for circuit-level distance**, and the docs say an
  absent `circuit-distance:` tag means the search ran out of budget. It did not: 26 of the
  28 settle, 20 of them in under a second. `scripts/measure_circuit_distance.py` arrived in
  #137 and #136 had already merged, so nothing ever pointed it at them. Now tagged, which
  puts a number on the caveat those circuits already carry — the library states the
  strategy is not guaranteed distance-preserving, and **[[4,2,2]], [[6,2,2]] and
  [[15,7,3]] come out at `circuit-distance:1`**: one fault anywhere in the round flips a
  logical without firing a detector. Two circuits exceed even a 400 s budget and stay
  untagged.
- **Fifty-six flag gadgets were stored twice or more.** A gadget depends on the
  stabiliser's weight, not on the code distance it was verified at, so the same file ships
  at every distance from the one it first appears in up to 11 — the weight-4 X gadget is
  byte-identical at d=3, 5, 7, 9 and 11 and was five circuits, distinguishable only by the
  number in the title. The distances are the information, not the copies: 20 circuits now
  carry several `distance:` tags each, stay findable by filtering on any of them, and name
  the span (`X-type weight-4 FT gadget (d=3-11)`). 354 source files, 298 circuits.
- **Five pairs of qLDPC rounds were identical without saying so.** Colouring the X- and
  Z-check subgraphs separately returns the joint colouring, byte for byte, whenever the
  Tanner graph is small enough that the joint one already separates them — [[4,2,2]],
  [[6,2,2]], [[7,1,3]], [[15,7,3]] and the tetrahedral code, 5 of the 14 codes carrying
  both. Nothing on either page said so, which left two entries a reader had to diff by
  hand. Both are still stored: they are different algorithms, and on the other 9 codes
  they differ, the toric [[16,2,4]] by depth 4 against 9. Each now names the other
  strategy in its notes, so the agreement is a stated property of the code rather than an
  unexplained repeat.
- **The changelog claimed 61 of 127 circuits measured.** That count came from a branch that
  also held the AlphaSyndrome import when it was not yet merged, and counted 127 circuits
  that were never all on `main` at once. With every round in place it is 91 of 159.
  Corrected, along with how many preserve the code's distance.
- **`circuit-distance:` fell into the filter's "Other" group** while `distance:` sits under
  Fault tolerance. Same question, different number — they belong together.

### Added

- **`npm run typecheck`, because nothing in CI had ever read a TypeScript type.**
  `astro build` transpiles without checking and `eslint.config.mjs` uses the non-type-aware
  `tseslint.configs.recommended`, so all of `src/` was compiled and shipped on trust. The
  new script runs `astro check` as its own CI step, and found three errors on `main` — one
  of them a page whose keyboard shortcuts have simply never worked. Two of the three live
  in files owned by other open PRs and are excluded, individually and by name, in
  `tsconfig.check.json`; that file is a debt register with two entries, not an ignore list.
  `typescript` becomes a direct dev dependency in the process, instead of whichever major
  `astro` and `typescript-eslint` happened to hoist between them.
- **AlphaSyndrome syndrome-measurement schedules** (59 of them), imported from
  [acasta-yhliu/asyndrome](https://github.com/acasta-yhliu/asyndrome)
  ([arXiv:2601.12509](https://arxiv.org/abs/2601.12509), ASPLOS '26) by
  [data-imports/asyndrome/](data-imports/asyndrome/README.md). 14 new codes come with
  them — hyperbolic surface ×6, hyperbolic colour ×3, surface-with-defects ×2, plus the
  [[61,1,9]] colour code, the 5×9 rotated surface code and a self-dual bivariate bicycle
  code. Every schedule is scored against a named decoder, so `decoder:` is what separates
  two otherwise identical rounds for one code.
  - **10 of the dataset's 69 schedules do not survive validation and are left out** —
    every `google.json` and every `trivial.json`. Their X- and Z-checks interleave so
    that two ancillas sharing two data qubits come out entangled, which makes each
    outcome individually random even though every check is applied exactly once. The
    import README traces it to the hard-coded tick tables in `asyndrome/special.py` and
    measures what it costs in the paper's own metric.
  - **Three codes are stored with a distance the dataset does not give.**
    `code_distance.py` computes the exact CSS distance by exhaustive enumeration, so
    these are distances rather than bounds. The self-dual bivariate bicycle code ships
    `d: -1` and is [[42,6,6]]. The two defect surface codes declare 5 and 7 but each
    carry a **weight-2 X-logical** — the dataset's own second `logical_xs` entry — so
    they are stored as [[24,2,2]] and [[40,2,2]]. A stored `[[n,k,d]]` has to describe
    the `h` printed beside it.
  - The hyperbolic surface [[36,8,4]] shares `n` and `k` with the QUITS balanced-product
    `36-8-4-bpc` and nothing else: row-space ranks 11/17 against 14/14, which no
    relabeling reconciles. It gets its own entry, with the refutation recorded next to
    the `assume_new` that allows it.
- **Syndrome-extraction circuits are a supported kind.** The pipeline could describe an
  encoder and a state prep; a round of syndrome extraction fitted neither, and there was
  nothing to check one against.
  - **`validate_syndrome_extraction_h`** (`scripts/add_circuit/circuit_validate.py`) — a
    round must measure exactly the stabilizer group and leave the encoded state, logicals
    included, alone. It cannot be a codespace test the way the prep and encoder checks
    are: a round acts on an already-encoded state, so there is nothing to simulate it on.
    It is a **stabilizer-flow** check instead, and the ancilla-to-check correspondence is
    derived rather than assumed.
  - **`build_se_round`** (`scripts/add_circuit/syndrome_extraction.py`) — ticks of
    (data, ancilla, basis) into one canonical round, refusing a tick that reuses a qubit
    or an ancilla asked to carry both bases.
  - **`round_check_matrix`** — which operator each measurement reads, which is what
    placing detectors needs. Deliberately narrow: no map is better than a wrong one, and
    nothing in validation depends on it.
  - **A round's `stim-annotated` body is the memory experiment it belongs to** — reset the
    data, `REPEAT d` of the round, terminal readout, detectors, observable. Unlike a prep
    or an encoder, a round is not reset-free and has no tableau, so none of the derive/fit
    machinery may be pointed at it.
  - `schedule:` and `decoder:` join the `method` tag category. They pair up: a schedule
    found by search is co-designed with the decoder it was scored against, so two rounds
    for one code can differ only by `decoder:`.
  - **`scripts/add_circuit/find_sigma.py`** — the codeword-based permutation matcher,
    for codes that match a stored one on every cheap invariant but defeat
    `find_code_permutation`'s budget. Written for the asyndrome import; three importers
    need it, so it lives in the shared package rather than in one of them.

### Added

- **Bacon-Shor [[9,1,3]], [[16,1,4]] and SHYPS [[49,9,4]]**, the library's first subsystem
  codes, now that #144 gives them somewhere to live. `code.matrix` is qLDPC's _gauge_
  group, so the importer passes the stabilizer group (`get_stabilizer_ops()`) as `h` and
  the gauge group alongside it; k comes out `n - rank(h) - gauge_qubits` rather than
  `n - rank(h)`, which is the difference between [[9,1,3]] and [[9,5,3]].
  - An encoder and a |0> prep each. qLDPC's memory experiments do not support subsystem
    codes, so the two syndrome-extraction strategies report `unsupported` for them rather
    than silently producing nothing.
  - **A subsystem encoder exposes `k + gauge_qubits` free inputs**, not `k` — five for
    Bacon-Shor, one logical and four gauge. `logical_input_count` and the annotator both
    compared against `k` alone and refused every such circuit. Both now add the stored
    gauge count. Deliberately _added to the stored k_ rather than derived from `h`: the
    latter is the same number but would compare the circuit against itself and stop
    catching a stored k that disagrees with the code, which is what the check is for.
  - `add_circuit(gauge=...)` passes the group through; #144 stopped at
    `compute_code_data_h`.

- **Subsystem codes can be stored** (`data/migrations/020`). A subsystem code is described
  by two groups, not one: the **gauge** group a decoder may measure, and the **stabilizer**
  group — its centre — whose outcomes are deterministic. The difference between them is
  real qubits, `(rank(G) − rank(S)) / 2` of them, which carry no information and are not
  corrected.

  The library read k off a single check matrix as `n − rank(h)`, which counts those gauge
  qubits as logical ones: Bacon-Shor [[9,1,3]] would have been stored as **[[9,5,3]]** and
  SHYPS [[49,9,4]] as **[[49,25,4]]**, so both were excluded rather than recorded wrongly.
  Codes now carry an optional `gauge` matrix and `gauge_qubits` count, and

      k = n − rank(S) − (rank(G) − rank(S)) / 2

  which for a stabilizer code has a zero gauge term and is the formula already in use — one
  implementation, not two.
  - **`h` still means the stabilizer group**, for every code. Validators, dedup, the CSS
    split and the matrices view are untouched: a circuit is checked against the operators
    that are actually deterministic, which is what those checks want. Stabilizer codes gain
    no fields at all.
  - **Logicals are the bare ones.** `_compute_symplectic_logicals` takes the kernel of the
    gauge group rather than of `h` when there is one, so they commute with everything a
    decoder may measure, while still quotienting by the stabilizers.
  - **Identity is the gauge group's.** Two subsystem codes can share a stabilizer group and
    differ in gauge group, so `canonical_hash` is computed over the gauge group when there
    is one — it determines the stabilizer group as its centre, so it is the more
    informative of the two.
  - Tagged `subsystem`, so a reader who sees [[9,1,3]] over a rank-4 `h` is told why rather
    than left to think it a bug.

  Verified against qLDPC's own `get_code_params()` on Bacon-Shor(3), Bacon-Shor(4),
  SHYPS(3) and Steane. Importing the codes themselves is a follow-up.

### Changed

- **Submitted check matrices are stored once instead of once per circuit.** They are a
  property of the code and the labelling it was submitted in, so every circuit of one
  code wrote the same bytes — 479 files collapse to **68**. They now live in
  `data_yaml/matrices/<digest>.yaml`, content addressed, with the circuit YAML naming
  the one it uses via `original_matrices`. The original _circuit_ stays beside the
  circuit, since that genuinely differs. `db:create` resolves the reference and inlines
  both halves, so `circuit_originals`, the API and the circuit page are unchanged.
- **Large matrices are written sparsely.** Above `SPARSE_MIN_ENTRIES` a matrix is stored
  as the nonzero column indices of each row rather than dense 0/1 rows. `h` is
  (n-k) x 2n, so a dense encoding costs O(n^2) characters however sparse the code is.
  Small codes stay dense deliberately — they are the ones a person reads, and the
  threshold sits above every code the library had before the qLDPC imports, so no
  existing small file is rewritten. Readers call `matrix_format.decode` (Python) or
  `decodeMatrix` (`scripts/matrix-format.mjs`) and cannot tell which was used.

  On the current data `data_yaml/` goes **35.2 MB to 24.2 MB**, all of it from sharing:
  `circuits/originals/` drops 15.7 MB to 0.3 MB and the shared `matrices/` costs 4.3 MB
  back. The sparse encoding saves **nothing today** and is meant to — no code the library
  has reaches the threshold, and rewriting the small files a person reads would be a cost
  with no benefit. It is what makes the qLDPC codes affordable when they land: on a single
  [[1428,184]] code it is worth more than this whole repository.

  `db:create` refuses to build a circuit that still carries a per-circuit
  `originals/<stem>.original.yaml` with no `original_matrices` reference. Merging a
  branch written before this format produces no git conflict — the old file simply
  reappears — and the build would otherwise store null matrices and say nothing.
  `scripts/migrate_matrix_storage.py --write` converts such a branch.

### Fixed

- **Importing a circuit no longer costs a full re-read of the library.** Dedup compares a
  submission against every stored code, and re-parsed all of them from YAML on _every_
  call — so a bulk import paid O(library) per circuit and got slower as the library grew.
  Measured on the 74-code, 43 MB library the qLDPC imports produce: **29.3 s per
  circuit**. Parsed codes are now cached across calls, keyed on each file's
  (mtime, size) so a code written mid-import is still picked up — `add_circuit` creates
  code files as it goes, and a cache that could not see them would be worse than none.
  Every circuit after the first now pays a `stat`. Sparse storage compounds it: the same
  first parse drops to 3.6 s.
- **The submitted-order logical operators are no longer recomputed from scratch.**
  `canonical_form` only permutes columns and row-reduces, neither of which changes the
  code, so the canonical logicals permuted back _are_ the originals — worth ~25 s per
  circuit on a [[544,80]] code, and it makes the two sets agree about which logical qubit
  is which, where a second independent computation would pick some other equally valid
  basis. The permuted operators are verified against the submitted matrices before use,
  with recomputation as the fallback.
- **A non-CSS circuit for an existing code is filed under that code's slug.** On a dedup
  match the CSS path has always used the stored slug; the non-CSS path only used it when
  nothing else had set one, so `code_slug` — or a slug derived from `code_name` — won
  instead. A five-qubit-code circuit submitted with
  `code_name="Five-Qubit Perfect Code"` was written as
  `five-qubit-perfect-code--<circuit>.yaml` while the code itself lives at
  `five-qubit-code`; no code YAML was written under that name, because there was no new
  code, so the circuit referenced an entry that does not exist —
  `annotate_circuits.py` reported `code '...' not found` and `db:create` rejected it.
  `code_slug` is documented as naming a _new_ code, and on a match there is no new code
  to name.

### Added

- **Every qLDPC circuit records the one-liner that rebuilds it**, at the end of its notes:
  `Reproduce with: qldpc.circuits.get_encoding_circuit(qldpc.codes.ToricCode(4), only_zero=True)`.
  Asked for by the library's author
  ([qLDPCOrg/qLDPC#554](https://github.com/qLDPCOrg/qLDPC/issues/554)) — a reader who wants
  to rebuild one should not have to reverse-engineer the constructor from `[[n,k,d]]`.
  The snippet cannot drift from the circuit, because the constructor string **is** what the
  importer evaluates: `CodeSpec.constructor` replaced the lambda it used to hold, and
  `CodeSpec.build()` evaluates it. A snippet that stopped building the code would fail the
  import rather than mislead a reader.

- **qLDPC circuits** (58 of them), imported from
  [qLDPC](https://github.com/qLDPCOrg/qLDPC) by [data-imports/qldpc/](data-imports/qldpc/README.md):
  28 syndrome-extraction rounds in two edge-colouring schedules
  ([arXiv:2109.14609](https://arxiv.org/abs/2109.14609)), plus a tableau encoder and a
  tableau |0> preparation for each of 15 codes. Six new codes come with them — the
  Iceberg codes [[4,2,2]] and [[6,2,2]], toric d=6, two hypergraph product codes
  [[58,16,3]] and [[241,121,3]], and a toric [[16,2,4]] that is **not** the stored
  one (its X row space has 16 weight-6 codewords where the stored code has none, and
  weight enumerators are permutation invariants).
  - Upstream states both syndrome-extraction strategies are **not guaranteed
    distance-preserving or fault-tolerant**, and that its encoders are not
    fault-tolerant. That claim is reproduced in each circuit's notes rather than
    dropped: the library tags what its sources claim, and here the source claims the
    opposite.
  - Subsystem codes are excluded, not broken. `BaconShorCode` and `SHYPSCode` validate
    fine against their stabilizer group, but the library derives k as n - rank(h),
    which is only correct for stabilizer codes — Bacon-Shor [[9,1,3]] would be stored
    as [[9,5,3]]. They need a gauge-group field and a k that is not derived.

### Fixed

- **`round_check_matrix` reads rounds that hold their ancillas in the X basis**
  (`RX` ... `MX`, with Z-checks as `CZ`), not only the Z-basis form. The two are the
  same construction in different frames; before this, every X-basis round returned no
  check map and silently lost its annotated memory experiment. It now tracks the basis
  each ancilla is prepared in, pulls back that operator rather than always `Z`, and
  requires the measurement basis to match the reset basis — a round reset in X and read
  in Z has a random outcome however correct its check pattern looks.
- **QUITS syndrome-extraction schedules** (72 of them), imported from
  [QUITS](https://github.com/mkangquantum/quits)
  ([arXiv:2504.02673](https://arxiv.org/abs/2504.02673), Quantum 9, 1931 (2025)) by
  [data-imports/quits/](data-imports/quits/README.md). These are the library's first
  circuits for **balanced-product, hypergraph-product, lifted-product and
  lift-connected-surface codes** — 23 new codes, from [[36,8,4]] to
  [[1428,184,<=24]] — and its first competing schedules for the same code from an
  independent source: a bivariate bicycle round is 7 CX layers under the code's own
  schedule and 12 under ZX-coloration.
  - QUITS ships no circuits; it is a generator, so the importer calls it. One stored
    circuit is one round, lifted out of the memory experiment's `REPEAT` block. The
    `custom` bivariate bicycle schedule needed two normalisations, both identities on
    a steady-state round: it renumbers the qubits (X-checks first) and ends on `MR`.
  - Source is the paper that defines the **schedule**, not the code: only `cardinal`
    and its N/S-merged variant are QUITS' own, while ZX-coloration is
    [arXiv:2308.08648](https://arxiv.org/abs/2308.08648) and the bivariate bicycle
    schedule is [arXiv:2308.07915](https://arxiv.org/abs/2308.07915).
  - Schedules are tagged `schedule:interleaved` or `schedule:xz-separated` by
    **measuring** the emitted circuit — reading the check type off each two-qubit gate
    and asking whether any tick mixes them — rather than by trusting the strategy's
    name. The source's own vocabulary lives in the circuit name instead.
  - **One extra seed is imported, and only one.** QUITS' cardinal strategies take a
    `seed` that reorders the schedule at identical depth and gate count, and its author
    suggested varying it. Sweeping 12 seeds over the five cardinal-family codes whose
    circuit distance is measurable found the default already at the best distance
    available everywhere but one — and the two lift-connected-surface codes emit only
    two distinct schedules however it is set. So the import adds exactly the
    improvement: BPC [[36,8,4]] cardinal at seed 2, circuit distance **4** against
    seed 1's 3, same depth and same 216 two-qubit gates. `EXTRA_SEEDS` in the importer
    records it; a variant that measures the same as one already stored earns a reader
    nothing and costs them a row.
  - Three codes share [[n,k,d]] with an unrelated stored code and are refuted rather
    than merged into it: BPC [[36,8,4]] against the hyperbolic surface code (row-space
    ranks 14/14 against 11/17), BPC [[108,8,8]] against the bivariate bicycle
    [[108,8,10]] (different distance), and BB [[90,8,10]] against the stored
    `90-8-10` — enumerating every weight-4 vector against each X row space gives 0
    codewords here and 90 there, and the weight enumerator is a permutation invariant.
    All three get distinct slugs. The last is filed as `90-8-10-autqec`, the slug
    autqec's import (#127) gives the same code, so whichever lands first creates the
    single shared entry; its name, **Bivariate Bicycle Code (Bravyi Table 3)**, says
    what distinguishes it from the stored entry carrying the "(15,3) BB6 code" alias.

### Added

- **`circuit-distance:<N>` on syndrome-extraction circuits** — the fewest faults
  _anywhere in the round_ (gate, idle, reset or readout) that flip a logical while
  firing no detector, measured rather than cited. It sits next to `distance:<N>`,
  which is the **code's** distance and usually a larger number: 17 of the 91 circuits
  measured so far preserve it, the rest lose at least one step to hook errors. Filter
  on it like any other tag.
  - `scripts/measure_circuit_distance.py` writes it;
    `scripts/add_circuit/circuit_distance.py` is the measurement. The search is stim's
    `search_for_undetectable_logical_errors` over a `d`-round memory experiment under
    uniform circuit-level depolarizing noise — every gate, **every idle qubit each
    tick**, every reset and every measurement. Cross-checked against QUITS'
    `examples/circuit_distance_search.py`, which computes the same number the same way:
    identical answers on BPC [[36,8,4]] across seeds.
  - **Both memories are measured and the smaller wins.** A CSS code's Z and X
    experiments fail at different weights — the rotated surface code d=5 under the
    depth-optimal schedule survives 5 faults in Z and 3 in X — and the Z number is not
    even bounded by `d`, since a Z observable is flipped by X errors. Measuring Z alone
    would have called that schedule distance-preserving and put `circuit-distance:6` on
    a `distance:5` code. `build_annotated_se` gained a `basis` argument for this; the
    stored Z bodies are byte-identical.
  - The search cost grows with `n` and, harder, with `d`: 91 of the library's 159 rounds
    settle inside a 120 s budget. `d` is what hurts — [[241,121,3]] takes 3 s and
    [[49,1,7]] runs out. An **absent tag means not measured**, never "no faults found".

### Fixed

- **A round built from two sequential sub-rounds gets its annotated view.**
  `round_check_matrix` answers which operator each measurement reads, and it pulled
  every measurement back through the _same_ whole-round unitary — so a round that
  resets and reads the Z-ancillas and only then the X-ancillas was refused outright,
  costing all 25 ZX-coloration circuits their `stim-annotated` body and Crumble
  detector view. Each measurement is now pulled back through the gates that precede
  _it_. A later sub-round's operator picks up support on the earlier sub-round's
  ancillas unless it cancels — which it does exactly when the checks commute — so a
  schedule where they do not is still refused rather than given a wrong detector.
  Requiring each ancilla to be reset before any gate touches it is what makes the
  pull-back past the reset legitimate.

### Changed

- **A code too large to display offers its matrices as a download** instead of
  rendering them. The stored `h` is (n-k) x 2n, so the lifted product code
  [[1428,184,<=24]] is 3.6M entries and ~14 MB of JSON — neither readable as text nor
  worth sending to everyone who expands the section. Below
  `MATRIX_INLINE_ENTRY_LIMIT` nothing changes; matrices were already fetched lazily,
  so no page ever shipped them in its HTML.

### Added

- **Search aliases** (`data/migrations/017`). Codes and tools gain optional
  `aliases:`, and codes `related:`, hand-written with the Error Correction Zoo as
  reference. `laflamme` → the five-qubit code, `kitaev` → surface codes,
  `bb codes` → 28 circuits instead of 824. `related` names a _different, adjacent_
  code (`toric` → planar surface codes) and `/search` says so rather than
  silently equating them. See
  [docs/superpowers/plans/2026-07-15-search-aliases.md](docs/superpowers/plans/2026-07-15-search-aliases.md).
- **Code tags reach `/search`** (`data/migrations/019`). `circuit_search.tags`
  was built only from `taggable_type = 'circuit'`, so every code-level tag was
  invisible: `LDPC`, `topological`, `self-dual`, `surface-code` and `color-code`
  each matched zero circuits despite 4 codes being tagged LDPC and 10
  surface-code. They now ride in their own `code_tags` column — separate from
  `tags` so a name used at both levels cannot double-count. It failed silently
  because `search_terms` already indexed code tags, so spelling correction
  considered `topological` a real word and left the dead query alone.
- **`scripts/add_paper.py`** — fetches paper metadata from arXiv/Crossref into
  `data_yaml/papers/`, so it is never hand-written or recalled from memory.
  `npm run papers:add -- <arXiv id | DOI | link>` for one;
  `npm run papers:missing` scans every circuit `source` and fetches whatever has
  no paper yet (idempotent — the one to run after a bulk import). Refuses to
  write a record with no authors rather than emit a half-citation. Stdlib only,
  no new dependency.
  - This is the **only** part of the repo that touches the network, and it is a
    maintainer tool whose output is committed — the same shape as
    `annotate_circuits.py`. `db:create` and the site read committed YAML only and
    build identically offline.
- **Papers are searchable.** A circuit taken from a paper can now be found on
  `/search` by the paper's title, authors and arXiv id — none of which existed
  anywhere in the library before, since `circuits.source` holds only a link.
  Searching `reinforcement learning`, `Forlivesi` or `boolean satisfiability`
  now finds the circuits from those papers.
  - New `data_yaml/papers/` (7 files) and a `papers` table, with `circuits.paper_id`.
  - **Circuits do not declare their paper.** `db:create` resolves `source` against
    each paper's `url`/`arxiv_id`/`doi`, tolerating http/https, trailing slashes,
    `dx.doi.org`, `/pdf/` vs `/abs/`, and arXiv version suffixes. Adding a paper file
    enriches every circuit citing it; no circuit YAML changes. 724 of 833 circuits
    link; the remaining 109 carry `source: circuit-synth`, a tool rather than a work.
  - `circuit_search` gains a weighted `paper` column (migration 017 recreates the
    FTS5 table — it has no `ADD COLUMN`), and `search_terms` indexes paper titles and
    authors so spelling correction knows author names.
  - Paper text is `/search`-only. The header quick-search is for jumping to a known
    thing, and one paper backs up to 370 circuits.

### Changed

- **BM25 weights and the strict column set are derived from the table**
  (`src/lib/queries/search-schema.ts`), not restated by hand. Both drifted from
  `circuit_search` while this branch was being built — a 7-entry weight array for
  8 columns (silently scoring `paper` as `notes`), and a strict set missing
  `paper` (which announced "no code goes by that name" for an exact author
  match). Weights are now keyed by column name and ordered from
  `PRAGMA table_info`; a column with no weight throws and names itself instead of
  being silently scored 1.0. `scripts/smoke.sh` additionally asserts that a query
  reaching each of `aliases`, `code_tags` and `paper` still returns circuits.
- A circuit's source now renders as a citation ("Zen et al. (2024) · arXiv:2402.17761")
  instead of a bare URL, on circuit rows, detail pages and the cite toast. Detail pages
  emit the paper as a schema.org `ScholarlyArticle` with its real authors, rather than a
  URL string.
- The landing page's "Papers" stat counts the `papers` table instead of inferring papers
  from distinct `source` values that are not a tool's own links. Same number today, but
  it no longer guesses.

### Removed

- The `Circuit-Synth Encoding (Gate-Optimized)` circuit for the Gottesman
  [[8,3,3]] code (`#134`) — it did not encode the code it was filed under.
  Propagating `Z` through it landed only 1 of 8 single-qubit operators inside the
  code's stabilizer group where 5 (`n−k`) were expected, and 2 of its 5 stored
  stabilizers came out genuinely random on the `|0…0⟩` run — checked sign-free,
  so not a Pauli-frame difference. Its three sibling encoders are correct and
  remain. `#134` is retired, not reused. Surfaced by the detector work: the
  logical-input derivation is basis-independent, so it can check non-CSS codes
  that `validate:circuits` skips (see below).

### Fixed

- Qubit coordinates survive ingestion
  ([#107](https://github.com/qecirc/qecirc-website/issues/107)). `QUBIT_COORDS`
  reached the stored body intact only when a circuit had TICKs; otherwise
  compaction kept the instruction and dropped its arguments, turning
  `QUBIT_COORDS(3, 7) 0` into a meaningless bare `QUBIT_COORDS 0`. That path runs
  for TICK-less circuits — most of the library. Nothing stored was corrupted,
  because no body carried coordinates yet.

### Added

- Detectors and observables for state-preparation and encoding circuits
  ([#108](https://github.com/qecirc/qecirc-website/issues/108)), shown with a
  **Detectors toggle** next to Coords and hidden by default. Switching it on
  swaps in a new `stim-annotated` body — reset prologue, terminal readout, the
  deterministic stabilizer outcomes as `DETECTOR`s, and the logical as an
  `OBSERVABLE_INCLUDE` — and repoints the Crumble link at the matching URL. The
  canonical `stim` body stays unitary and untouched, because `to_tableau()` and
  the derive/fit pipeline depend on it. 418 of 834 circuits are annotated (357
  state prep, 61 encoders); the 62 five-qubit-code circuits are excluded,
  because non-CSS stabilizers mix X and Z on the same qubit and no single
  terminal readout basis reads them — but they still get the reset prologue,
  since being non-CSS blocks the readout, not the initialisation.
- State-prep and encoding circuits now state their `|0…0⟩` input explicitly with
  a reset prologue, in both toggle states, instead of leaving it implied.
  Encoders reset only their non-input qubits, since those are the ones actually
  fixed in `|0⟩`. Circuits that act on an already-encoded state (syndrome
  extraction, gadgets) get no prologue — a reset there would be wrong, not
  merely unhelpful.
- Encoders are annotated differently from state preps: only their ancillas are
  reset, leaving the k logical inputs free, and they get detectors but no
  observable. Hz is deterministic for any input, so the detectors hold whatever
  the reader supplies; the logical is input-dependent. The input qubits are
  unrecorded and canonicalization moves them, so they are derived from the
  circuit.
- Coordinates are now displayed with a **Coords toggle** on circuit bodies,
  hidden by default: a d=11 unrotated prep opens with 221 `QUBIT_COORDS` lines
  before its first gate. Copy and download follow the toggle, so what you take
  away is what you see. The toggle only appears on bodies that have
  coordinates. Crumble links always keep them — that is where the layout is the
  point.
- The 20 unrotated surface code circuits now carry their lattice layout, and
  their Crumble links render it. Only coordinates for qubits the circuit
  actually uses are kept: a `QUBIT_COORDS` target counts towards stim's
  `num_qubits`, so importing every declared grid site would inflate
  `qubit_count`.

- Surface code unitary Pauli-state encodings from
  [arXiv:2601.05113](https://arxiv.org/abs/2601.05113) — 40 circuits across 10
  codes (`data-imports/surface-code-encodings/`). Each code gets four circuits:
  `Ancilla-mediated` / `Direct` × `zero` / `plus`, the two variants differing in
  whether intra-plaquette gates are routed through bridge ancillas
  (nearest-neighbour) or run directly between data qubits
  (next-nearest-neighbour).
- Six new codes: `unrotated-surface-code-d-{3,5,7,9,11}` — the unrotated
  (planar) surface code family, `[[13,1,3]]` through `[[221,1,11]]`, new to the
  library — and `rotated-surface-code-d-11` (`[[121,1,11]]`), completing the
  rotated family from d=3 to d=11.
- New `partial-ft` circuit tag, for schemes that preserve the fault distance for
  only one error type. The surface code encodings preserve it for the error that
  flips the codeword (X for `|0>_L`, Z for `|+>_L`) but not the complementary
  one, which `ft` / `non-ft` cannot express. Which type is protected follows from
  the `logical-state:*` tag.
- `import_state_prep(ancilla_role=...)` distinguishes flag qubits from routing
  ancillas. Previously the `flag` tag was inferred from `num_qubits > n` alone,
  which mis-tags circuits whose ancillas only bridge gates under a restricted
  connectivity and carry no fault-tolerance role. Defaults to `"flag"`, so
  existing importers are unaffected; pass `"routing"` to opt out.
- Circuit notes render a long contiguous ancilla run as `221-440 (220 qubits)`
  instead of spelling out every index. Ancilla indices are always contiguous
  (`range(n, num_qubits)`), so the list was pure noise once a code got large.
  Runs of 8 or fewer, and any non-contiguous set, are unchanged.

- Edge caching: `s-maxage` raised from 10 minutes to 7 days (pages and API),
  paired with an automatic Cloudflare purge-everything on each deploy
  (`src/lib/cache-purge.ts`, activated by the `CLOUDFLARE_ZONE_ID` /
  `CLOUDFLARE_API_TOKEN` env vars; logged no-op without them).

- Social-share card: static `og:image` / `twitter:image` (1200×630, generated
  by `scripts/icons/generate.mjs`) on all pages; Twitter card upgraded to
  `summary_large_image`.

- Non-CSS stabilizer code support throughout the pipeline (symplectic representation).
  Submit codes via `add_circuit(H=..., n=...)` for non-CSS, or the existing
  `Hx`/`Hz` path for CSS.
- New `h` and `logical` columns on `codes`; `original_h` and `original_logical`
  on `circuit_originals` (migration `011_symplectic_storage.sql`).
- New `npm run backfill:symplectic` script for upgrading existing CSS YAMLs.
- Non-CSS code page renders stabilizers and logicals via a Pauli ↔ symplectic
  toggle; CSS pages keep the existing `Hx`/`Hz`/`Logical X`/`Logical Z` view.

### Changed

- Circuit results in the search dropdown now link to the circuit's own page
  (`/circuits/<id>`) instead of the anchored code list.
- Filtering and sorting on the codes index and code pages now run client-side
  over the rendered rows: filter changes apply instantly (no page reload) and
  every visit shares one canonical cached document. The URL contract is
  unchanged (old filter links still work, applied on load); `/api/download`
  still parses the same params server-side.
- Code pages no longer embed circuit bodies in the initial HTML; bodies load
  on first row expand via the new `/api/circuits/[qec_id]/bodies` endpoint.
  Largest page (`/codes/flag-gadgets`) drops from ~15 MB to ~3 MB HTML and
  from ~39k to ~20k DOM nodes.
- **BREAKING:** `add_circuit()` matrix arguments (`Hx`, `Hz`, `H`, `n`) are now
  keyword-only. Migration: replace `add_circuit(Hx, Hz, circuit, name, d, ...)`
  with `add_circuit(circuit=circuit, circuit_name=name, d=d, Hx=Hx, Hz=Hz, ...)`.
- The non-CSS branch of `_compute_logicals` (now `_compute_logicals_css`) was
  mathematically wrong and is replaced by the new `_compute_symplectic_logicals`.
  This affects nobody in practice (the library contained no non-CSS codes), but
  any downstream code calling the old `_compute_logicals(_, _, code_is_css=False, _)`
  must switch to `_compute_symplectic_logicals(H, n, k)`.
