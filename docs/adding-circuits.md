# Adding Circuits (Manual)

How to add circuits to the QECirc library using the Python scripts directly, without any AI assistance.

For the agent-assisted workflow, see [adding-circuits-agent.md](adding-circuits-agent.md).

## Prerequisites

```bash
uv sync                # install Python dependencies
```

## What You Need

- **Stabilizer matrices** — provide either, _or_ derive them from the circuit (see [Which workflow?](#which-workflow)):
  - **`Hx, Hz`** — separate X-check and Z-check matrices. The pipeline rejects these unless they describe a CSS code (`Hx · Hzᵀ = 0 mod 2`); CSS detection is automatic and adds the `CSS` tag.
  - **`H, n`** — a single symplectic stabilizer matrix of shape `(n−k) × 2n` (X-half on the left, Z-half on the right) plus the qubit count `n`. CSS-decomposable `H` is auto-detected and routed through the CSS path so the `Hx`/`Hz` view and `CSS` tag are filled in automatically.
- **STIM circuit** — file path or string
- **Code distance `d`** — integer
- **Source** — DOI, URL, or citation

## Which workflow?

Pick the path that matches what you have — they all end at the same YAML files and the same `npm run db:create`.

| You have…                                                   | Use                                  | Section                                                               |
| ----------------------------------------------------------- | ------------------------------------ | --------------------------------------------------------------------- |
| An **encoding** circuit + check matrices (`Hx/Hz` or `H`)   | `add_circuit()`                      | [Steps 1–4](#step-1-inspect)                                          |
| A **state-preparation** circuit (matrices optional)         | `import_state_prep()`                | [State-preparation circuits](#adding-a-state-preparation-circuit)     |
| A **syndrome-extraction** round, or a check schedule        | `build_se_round()` + `add_circuit()` | [Syndrome-extraction circuits](#adding-a-syndrome-extraction-circuit) |
| A circuit whose qubit labeling differs from the stored code | either, with a _fit_                 | [Fitting to an existing code](#fitting-to-an-existing-code)           |
| **Many** circuits from one source/paper                     | a dataset importer                   | [Bulk / dataset imports](#bulk--dataset-imports)                      |

Only have a circuit? That's fine: [`extract_code`](#extract-code-from-circuit-optional) recovers `Hx/Hz` from an encoding circuit, and the [state-prep helpers](#get-the-check-matrices-from-the-circuit) derive them from a prep circuit. New here? See the [FAQ](#faq).

## Overview

1. Inspect your code and circuit with helper functions
2. Generate YAML files with `add_circuit()` or the CLI
3. Add tags manually to the generated YAML files
4. Rebuild the database

---

## Step 1: Inspect

### Check your code

CSS code via `Hx`/`Hz`:

```python
from scripts.add_circuit import check_code, find_existing_code

print(check_code(Hx, Hz, d=3))
# {'n': 7, 'k': 1, 'd': 3, 'is_css': True, 'is_self_dual': True, 'canonical_hash': '...'}

print(find_existing_code(Hx, Hz))
# 'steane-code' or None
```

Non-CSS (or general) code via a single symplectic `H`:

```python
from scripts.add_circuit import check_code_h, find_existing_code_h

print(check_code_h(H, n=5, d=3))
# {'n': 5, 'k': 1, 'd': 3, 'is_css': False, 'is_self_dual': False, 'canonical_hash': '<64-char SHA-256 hex>'}

print(find_existing_code_h(H, n=5))
# ExistingCodeMatch(slug='five-qubit-code', qubit_permutation=...) or None
```

### Inspect your circuit

```python
from scripts.add_circuit import summarize_circuit

print(summarize_circuit(circuit_text))
# {'qubit_count': 7, 'gate_count': 12, 'two_qubit_gate_count': 9, 'depth': 8, 'crumble_url': '...', 'quirk_url': '...'}
```

### Validate (optional)

```python
from scripts.add_circuit import (
    validate_encoding, validate_state_prep, validate_syndrome_extraction,
)

# For encoding circuits:
print(validate_encoding(circuit, Hx, Hz))   # 'passed' or 'failed: ...'

# For state-preparation circuits:
print(validate_state_prep(circuit, Hx, Hz)) # 'passed' or 'failed: ...'

# For syndrome-extraction circuits (one round):
print(validate_syndrome_extraction(circuit, Hx, Hz))  # 'passed' or 'failed: ...'
```

Validation uses your provided Hx/Hz (same source as the circuit). If the code already exists in the library with a different qubit ordering, `add_circuit()` handles the relabeling separately.

For a **non-CSS** code there is no Hx/Hz split; pass the symplectic `h` (shape
`(m, 2n)`, X-half then Z-half — the form stored in `codes.h`) instead:

```python
from scripts.add_circuit import (
    validate_encoding_h, validate_state_prep_h, validate_syndrome_extraction_h,
)

print(validate_encoding_h(circuit, h, n))    # 'passed' or 'failed: ...'
print(validate_state_prep_h(circuit, h, n))  # 'passed' or 'failed: ...'
print(validate_syndrome_extraction_h(circuit, h, n, logical=logical))
```

These are the general implementations — the Hx/Hz pair above is a thin wrapper —
so CSS codes may use either. Both check each stabilizer up to **sign** (`|⟨S⟩| = 1`,
not `⟨S⟩ = +1`): a sign-free binary `h` names a stabilizer group only up to a Pauli
frame, so a circuit preparing a codeword in a different frame is still valid.

**Syndrome extraction is checked differently**, because it acts on an
already-encoded state: there is no fixed input to simulate it on, and its resets
and measurements leave it with no tableau. `validate_syndrome_extraction_h` uses
stim's _stabilizer flows_ instead, and asks three things of one round: the group
it measures is exactly the code's stabilizer group, every stabilizer survives
(`S -> S`), and — when `logical` is passed — every logical does too (`L -> L`).
Which ancilla reads which stabilizer is **derived** from the circuit, never
assumed from the measurement order, since nothing in the stored data records it.
Data qubits are `0..n-1`; anything above is treated as an ancilla.

### Extract code from circuit (optional)

If you have a circuit but no check matrices, you can derive Hx/Hz directly:

```python
from scripts.add_circuit import extract_code

# For encoding circuits (first k qubits are data, rest ancilla):
result = extract_code(circuit, circuit_type="encoding", k=1)

# For state-preparation circuits:
result = extract_code(circuit, circuit_type="state_prep", k=1)

print(result.Hx, result.Hz, result.n, result.k, result.is_css)
```

Encoding extraction is exact. State-prep extraction derives Hx cleanly; Hz uses a RREF heuristic that may include logical Z for k >= 1. Prefer encoding circuits for guaranteed results.

---

## Step 2: Generate YAML files

### Option A: Python API

```python
from scripts.add_circuit import add_circuit, preview_circuit

# Preview first (dry run)
result = preview_circuit(
    Hx=Hx, Hz=Hz, circuit=circuit,
    circuit_name="Standard Encoding", d=3,
    code_name="Steane Code", source="https://doi.org/...",
    tool="mqt-qecc", zoo_url="https://errorcorrectionzoo.org/c/steane",
)
print(result.summary())

# Generate for real (CSS code)
result = add_circuit(
    Hx=Hx, Hz=Hz, circuit=circuit,
    circuit_name="Standard Encoding", d=3,
    code_name="Steane Code", source="https://doi.org/...",
    tool="mqt-qecc", zoo_url="https://errorcorrectionzoo.org/c/steane",
)
print(result.summary())

# Non-CSS code: pass the symplectic stabilizer matrix H instead of Hx/Hz.
# H has shape (n-k, 2n) — X-half on the left, Z-half on the right.
result = add_circuit(
    H=H, n=5, circuit=circuit,
    circuit_name="Standard Encoding", d=3,
    code_name="Five-Qubit Code", source="https://doi.org/...",
)
print(result.summary())
```

#### Parameters

| Parameter      | Required | Description                                                                 |
| -------------- | -------- | --------------------------------------------------------------------------- |
| `Hx`           | one path | X-check matrix (numpy array). CSS path; pass alongside `Hz`.                |
| `Hz`           | one path | Z-check matrix (numpy array). CSS path; pass alongside `Hx`.                |
| `H`            | one path | Symplectic stabilizer matrix `(n-k, 2n)`. General path; pass alongside `n`. |
| `n`            | with `H` | Number of physical qubits.                                                  |
| `circuit`      | yes      | STIM circuit (`stim.Circuit` or string)                                     |
| `circuit_name` | yes      | Human-readable circuit name                                                 |
| `d`            | yes      | Code distance                                                               |
| `source`       | no       | Provenance (DOI/URL)                                                        |
| `code_name`    | no       | Code name (optional if code already exists in `data_yaml/`)                 |
| `zoo_url`      | no       | QEC Zoo URL                                                                 |
| `tool`         | no       | Tool slug (must exist in `data_yaml/tools/`)                                |
| `notes`        | no       | Circuit notes                                                               |
| `data_dir`     | no       | Path to data_yaml directory (default: `"data_yaml"`)                        |
| `dry_run`      | no       | If `True`, preview without writing                                          |

#### Return value

| Field           | Type        | Description                           |
| --------------- | ----------- | ------------------------------------- |
| `code_name`     | `str`       | Code name                             |
| `code_slug`     | `str`       | Code slug                             |
| `code_status`   | `str`       | `"new"` or `"existing"`               |
| `circuit_name`  | `str`       | Circuit name                          |
| `circuit_slug`  | `str`       | Circuit slug                          |
| `qec_id`        | `int`       | Assigned circuit ID (displayed as #N) |
| `files_written` | `list[str]` | Paths of files written                |
| `dry_run`       | `bool`      | Whether this was a dry run            |

### Option B: CLI

```bash
python -m scripts.add_circuit.generate \
  --hx path/to/hx.json \
  --hz path/to/hz.json \
  --stim circuit.stim \
  --d 3 \
  --code-name "Code Name" \
  --circuit-name "Circuit Name" \
  --source "https://doi.org/..." \
  --tool "tool-slug" \
  --zoo-url "https://errorcorrectionzoo.org/c/..."
```

Add `--dry-run` to preview without writing. Multiple circuits per code: pass multiple `--stim` files with matching `--circuit-name`, `--source`, `--tool` values.

---

## Step 3: Add tags

The pipeline only auto-assigns mathematically verified code tags (`CSS`, `self-dual`). All other tags must be added — either by passing them to `add_circuit(..., tags=[...])` up front (circuit tags only), or by editing the generated YAML files afterwards. Fault tolerance (`ft` / `non-ft`) is never inferred, so always set it explicitly.

### Code tags (`data_yaml/codes/<slug>.yaml`)

Add a `tags:` list. Common code tags:

| Category   | Examples                                           |
| ---------- | -------------------------------------------------- |
| Type       | `CSS`, `stabilizer`                                |
| Family     | `color-code`, `surface-code`, `toric-code`, `LDPC` |
| Properties | `self-dual`, `concatenated`                        |

### Circuit tags (`data_yaml/circuits/<code-slug>--<circuit-slug>.yaml`)

Add a `tags:` list. Common circuit tags:

| Category        | Examples                                                                                       |
| --------------- | ---------------------------------------------------------------------------------------------- |
| Circuit type    | `encoding`, `state-preparation`, `syndrome-extraction`, `logical-state:zero`                   |
| Fault tolerance | `ft`, `non-ft`, `flag`, `deterministic`                                                        |
| Hardware        | `connectivity:2d-grid`, `device:tokyo`, `1D-AOD` (full connectivity is the default — untagged) |
| Method          | `prep:opt`, `prep:heuristic`, `verification:opt`                                               |
| Tools           | `tool:mqt-qecc` — **derived automatically, do not add** (see below)                            |

> **Tool tags are derived, not stored.** Every circuit with a `tool:` field is
> tagged `tool:<slug>` automatically when the database is built (see
> `scripts/db/create_database.mjs`), which powers the **Tools** filter category
> (e.g. all MQT QECC circuits at once). The `tool` field is the single source of
> truth, so never add a `tool:*` tag to a YAML `tags:` list — set `tool:` and the
> tag follows for every current and future circuit.

Check existing tags with:

```bash
grep -h '^tags:' data_yaml/codes/*.yaml data_yaml/circuits/*.yaml
```

Prefer reusing existing tags over inventing new ones.

---

## Step 4: Rebuild

```bash
npm run format                    # Prettier-format the generated YAML (CI gate)
git diff                          # Review changes
npm run db:create && npm run dev  # Rebuild database and restart
```

> The ingestion writes plain YAML, which is **not** Prettier-formatted. CI runs
> `format:check`, so run `npm run format` after generating (or editing) any
> `data_yaml/` files or the build will fail.

---

## Adding a state-preparation circuit

State-preparation circuits — the bulk of the library (e.g. the MQT QECC and RLFTQC imports) — prepare a logical basis state such as `|0⟩_L` or `|+⟩_L`. You usually **don't** have check matrices for them, and the circuit often includes flag/routing ancillas. `import_state_prep()` handles all of it: it derives (or is handed) the code, fits the circuit to it, validates codespace membership, and writes the same YAML as `add_circuit()`.

### Get the check matrices from the circuit

If you don't have `Hx/Hz`, derive them from the prep circuit itself:

```python
from scripts.add_circuit import (
    derive_matrices_self_dual, derive_matrices_two_circuit,
    strip_flags, symplectic_validate, logical_state_of,
)

# Self-dual CSS code (Hz == Hx) from a single |0⟩_L circuit:
Hx, Hz = derive_matrices_self_dual(zero_circuit, n)

# Or two circuits sharing a qubit labeling — Hx from |0⟩_L, Hz from |+⟩_L:
Hx, Hz = derive_matrices_two_circuit(zero_circuit, plus_circuit, n)
```

`n` is the number of **data** qubits; flag/ancilla qubits live at indices `≥ n` and are handled automatically (`strip_flags(circuit, n)` exposes the data-only sub-circuit if you need it). `logical_state_of(circuit, n, d, Hx=Hx, Hz=Hz)` reports which basis state the circuit prepares (`'zero'` / `'one'` / `'plus'` / `'minus'`), and `symplectic_validate(circuit, H, n)` checks the prepared state is a strict `+1` eigenstate of every stabilizer — use it when `H` is in a **known** sign frame (e.g. an importer's own matrices). Against a stored `codes.h`, whose frame is arbitrary, use the sign-tolerant `validate_state_prep_h` instead.

### Import

```python
from scripts.add_circuit import import_state_prep

result = import_state_prep(
    circuit=zero_circuit, n=7, d=3,
    method="self_dual",                  # or "two_circuit" / "anchor"
    code_name="Steane Code",
    circuit_name="FT |0⟩ prep (flag)",
    source="https://arxiv.org/abs/...", tool="mqt-qecc",
    tags=["state-preparation", "ft", "flag"],
    logical_state="zero",                # provenance → note + logical-state:zero tag
)
print(result.summary())
```

`method` picks how the code is obtained _in the circuit's own labeling_:

| `method`        | When                                                                                          |
| --------------- | --------------------------------------------------------------------------------------------- |
| `"self_dual"`   | Self-dual CSS code, from a single `\|0⟩_L` circuit                                            |
| `"two_circuit"` | CSS code, `Hx` from `\|0⟩_L` and `Hz` from `\|+⟩_L` (pass `plus_circuit=`)                    |
| `"anchor"`      | Non-CSS / non-self-dual, or a non-`\|0⟩` state — fit against a trusted symplectic `anchor_H=` |

The full circuit (flags included) is what gets stored; the pipeline dedups it to the canonical code, applies any qubit permutation, and preserves the original in `originals/`. Provenance you pass (`source_file`, `logical_state`, `connectivity`, `gate_set`, `device`, `qubit_placement`) is folded into the circuit notes, and the categorical ones also become `key:value` tags — nothing is dropped.

## Adding a syndrome-extraction circuit

A syndrome-extraction round is the odd one out, and in a way worth understanding before you
add one: it acts on an **already-encoded** state. There is no `|0…0⟩` input to simulate it on,
and its resets and measurements are the circuit rather than an annotation of it, so it has no
tableau. Nothing in the derive/fit machinery applies.

### From a check schedule

The reusable description of a round is a **schedule**: ticks of `(data, ancilla, pauli)` checks
that run in parallel. `build_se_round` turns one into STIM.

```python
from scripts.add_circuit import build_se_round, validate_syndrome_extraction_h

ticks = [
    [(0, 7, "X"), (1, 10, "Z")],   # tick 0: two checks, in parallel
    [(2, 7, "X"), (3, 10, "Z")],   # tick 1
]
circuit = build_se_round(ticks, n=7)          # hadamards="basis" | "per-check"
```

Data qubits are `0..n-1`; every ancilla must be `>= n`. The ticks are emitted **verbatim** — a
scheduling result _is_ its tick assignment, so nothing is re-packed — and the ancillas are
measured in ascending index order. A tick that uses the same qubit twice is rejected rather
than silently serialised.

### Validate

```python
print(validate_syndrome_extraction_h(circuit, h, n, logical=logical))  # 'passed' | 'failed: ...'
```

Three checks, on stabilizer flows: the group the round **measures** is exactly the code's, every
stabilizer is **preserved** (`S -> S`), and every logical is too (`L -> L`, when `logical` is
given). Which ancilla reads which check is _derived_ from the circuit, never assumed from the
measurement order.

Run it. The interesting failure is invisible to inspection: when an X-check and a Z-check share
two data qubits and their CNOTs are ordered inconsistently, the two ancillas come out entangled
and each outcome is random — with every check applied exactly once, on the right qubits, in a
conflict-free schedule. `measured_stabilizers` reports what the round actually measures, and
`round_check_matrix` the per-ancilla map, if you need to see why.

### Store

`add_circuit()` takes it from there unchanged — pass the symplectic `h`, tag it
`syndrome-extraction`, and run `scripts/annotate_circuits.py` afterwards to get the
`stim-annotated` memory experiment (reset the data, `REPEAT d` of the round, terminal readout,
detectors, observable).

```python
add_circuit(circuit=circuit, circuit_name="Depth-optimal schedule", d=3,
            H=h, n=n, source="https://arxiv.org/abs/...",
            tags=["syndrome-extraction", "schedule:depth-optimal"])
```

The importers under `data-imports/` are the worked examples.

## Fitting to an existing code

Published circuits rarely use the same qubit labeling as the stored code, so the circuit must be **fitted** by a qubit permutation (convention `σ[new] = old`). Both `add_circuit()` and `import_state_prep()` resolve this for you, trying in order:

1. **Identity** — small codes (e.g. `[[5,1,3]]`, `[[7,1,3]]`) often match as-is.
2. **Automatic dedup** — `find_existing_code_full()` / the canonical-hash search resolves the permutation for most codes (`n ≤ 9` is brute-forced).
3. **Structural finder** — `find_code_permutation()` recovers `σ` from the two codes' check matrices when the hash search can't (automorphism-rich codes, or `n` too large to brute-force).
4. **Explicit** — pass `qubit_permutation=σ` (`add_circuit`) or `permutation=σ` (`import_state_prep`). It is verified by row-space equality against the stored code — no search — so it works even where the canonical hash isn't a true permutation invariant.

If a submission's invariants match a stored code but no permutation can be confirmed within the search budget, `add_circuit` raises `UncertainDedupError`. Either supply `σ`, or pass `assume_new=True` to add it as a genuinely new code.

## Bulk / dataset imports

Importing a whole dataset (a paper's circuits, a tool's output) is a repeatable job, so it lives in its own script rather than the general pipeline. The split:

- **Reusable logic** — deriving/validating/fitting a code, capturing provenance — lives in `scripts/add_circuit/` and is imported.
- **Dataset-specific knowledge** — folder layout, which stored code each folder maps to, hardware metadata — lives in `data-imports/<dataset>/rebuild_all.py` with a README recording the decisions.

Worked examples to copy from:

- [`data-imports/mqt-ftsp/`](../data-imports/mqt-ftsp/README.md) — MQT QECC fault-tolerant state-prep circuits.
- [`data-imports/rlftqc/`](../data-imports/rlftqc/README.md) — RL-discovered fault-tolerant state-prep circuits.
- [`data-imports/flag-at-origin/`](../data-imports/flag-at-origin/README.md) — flag-at-origin FT preps (converts pytket circuits to STIM, fits via precomputed/`assume_new` strategies) **and** standalone flag gadgets collected under a placeholder `flag-gadgets` code (`n = k = 0`, no check matrices) for circuits that don't belong to a code.

Each `rebuild_all.py` classifies without writing by default and imports with `--write`, then you run the standard `npm run format && npm run validate:yaml && npm run validate:circuits && npm run db:create`.

---

## What the pipeline computes

- Code parameters [[n,k,d]], CSS detection, self-dual detection
- Canonical check matrices and hash (for dedup)
- Logical operators (Lx, Lz)
- Code extraction from circuits via Pauli propagation (`extract_code`)
- Circuit metrics (gate count, depth, qubit count)
- Compact STIM, QASM, and Cirq format conversions
- Crumble and Quirk visualization URLs
- **Circuit ID (`qec_id`)**: auto-assigned as `max(existing IDs) + 1` — permanent, never reused
- **Original submission data**: the pipeline always preserves the original (pre-canonicalization) STIM circuit and the contributor-provided symplectic stabilizer / logical matrices in `data_yaml/circuits/originals/`. These are displayed on the circuit detail page under "Original submission (before canonicalization)"; the Hx/Hz/Lx/Lz view is derived in the UI.
- Dedup: if the code already exists, the pipeline detects qubit ordering differences and relabels the circuit to match. Check `AddCircuitResult.qubit_permutation` to see if relabeling was applied (`None` = no relabeling, `list` = permutation applied)
- Use `find_existing_code_full()` to check for qubit permutations before generating files

## File formats

### Code (`data_yaml/codes/<slug>.yaml`)

```yaml
name: Steane Code
n: 7
k: 1
d: 3
zoo_url: https://errorcorrectionzoo.org/c/steane
aliases:
  - "[[7,1,3]]"
  - "seven-qubit code"
  - "6.6.6 color code"
related:
  - "triangular color code"
canonical_hash: d326fbcca125a5c717a7d4d1d0b4acc8da8e3b9d3ad123bfc705bc14d85f9ca4
h:
  - [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
  - [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
  - [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
  - [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1]
  - [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1]
  - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
logical:
  - [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
  - [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
tags: [CSS, stabilizer, color-code]
```

`aliases` are **other names for this same code** — every name a reader might type for it. They are matched silently, exactly as the stored `name` is, by both `/search` and the header quick-search. `tags` are code-level tags (`CSS`, `topological`, `LDPC`); these reach `/search` too, via the `code_tags` column.

`related` is **a different, adjacent code** people commonly mean by a name that is not strictly this code — `toric` for a planar surface code. It matches only when nothing else does, and `/search` tells the user the results are a related code. Do not put a true alias here, or a taxonomy ancestor there: two parents above the rotated surface code sits "Quantum Tanner code", which is neither.

Both are **hand-written**. The [Error Correction Zoo](https://errorcorrectionzoo.org) publishes `alternative_names` and is the right reference, but `eczoo_data` is CC-BY-SA 4.0 while this repo is MIT — use it to research, never add an import script. Only alias something the library actually holds: an alias for a concept with no circuits behind it resolves to nothing.

`h` is the symplectic stabilizer matrix of shape `(n−k) × 2n`: columns `0..n-1` are the X-half, columns `n..2n-1` are the Z-half. `logical` has shape `2k × 2n`; for CSS codes the top `k` rows are X-bar logicals (Z-half zero) and the bottom `k` rows are Z-bar logicals (X-half zero). The Hx/Hz/Lx/Lz view shown in the UI is derived from `h` and `logical` at render time.

### Circuit (`data_yaml/circuits/<code-slug>--<circuit-slug>.yaml`)

```yaml
qec_id: 1
name: Standard Encoding
tool: mqt-qecc
source: https://doi.org/10.1098/rspa.1996.0136
gate_count: 12
two_qubit_gate_count: 9
depth: 5
qubit_count: 7
crumble_url: "https://algassert.com/crumble#circuit=..."
quirk_url: "https://algassert.com/quirk#circuit=..."
tags: [encoding]
```

The `qec_id` is a **permanent, globally unique** integer identifier for the circuit (displayed as `#1` in the UI). It is auto-assigned by the generation pipeline (`max(existing IDs) + 1`). Once assigned, a `qec_id` must **never be reused or reassigned**, even if a circuit is removed.

Body files (`.stim`, `.qasm`, `.cirq`) share the same stem as the circuit YAML.

Circuits get one more, `.stim-annotated`, written by
`uv run python scripts/annotate_circuits.py` (idempotent — run it after adding
one). For a prep or encoder it restates the `|0…0⟩` input that the canonical
`.stim` body leaves implied and adds a terminal readout with detectors; for a
syndrome-extraction round it is the memory experiment (reset the data, `REPEAT d`,
readout, detectors, observable). Either way it is a view of the STIM body rather
than a display format, so it gets no format tab; the Detectors toggle derives both
views from it.

A prep or encoder's canonical `.stim` body must stay **reset-free** —
`to_tableau()` and the derive/fit machinery depend on that. A syndrome-extraction
body cannot be: its resets and measurements are the circuit.

### Original submission

The pipeline preserves what a circuit was submitted with, before any canonicalization or
qubit relabeling. It lives in two places, because the two halves have different owners:

- `data_yaml/circuits/originals/<code-slug>--<circuit-slug>.original.stim` — the STIM
  circuit as submitted. Per circuit, since every circuit has its own.
- `data_yaml/matrices/<digest>.yaml` — the contributor's symplectic stabilizer / logical
  matrices. **Shared**: every circuit of one code was submitted against the same matrices,
  so they are written once and named by a content digest, and the circuit YAML points at
  them with `original_matrices: <digest>`.

```yaml
# data_yaml/circuits/steane-code--standard-encoding.yaml
original_matrices: 4f9a1c02b7e3d518
```

```yaml
# data_yaml/matrices/4f9a1c02b7e3d518.yaml
h:
  - [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
  - ...
logical:
  - [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
  - [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
```

`npm run db:create` resolves the reference and inlines both halves into the
`circuit_originals` table, so the database, the API and the circuit detail page
(`/circuits/[qec_id]`) see exactly what they saw when every circuit carried its own copy.

### How a matrix is written (`h`, `logical`, and the files above)

A matrix is stored as a plain list of 0/1 rows, as above — until it gets big. Past
`SPARSE_MIN_ENTRIES` (`scripts/add_circuit/matrix_format.py`) it is written as the nonzero
column indices of each row instead:

```yaml
h:
  rows: 1244
  cols: 2856
  nonzero:
    - [3, 17, 402]
    - [1, 88]
```

`h` is (n−k) × 2n, so a dense encoding costs O(n²) characters however sparse the code is —
for the lifted product code [[1428,184,≤24]] that is 3.5M entries and 13.5 MB. Small codes
stay dense on purpose: they are the ones a person reads, and the threshold sits above every
code the library had before the qLDPC imports.

Nothing needs to know which was used. `matrix_format.decode` (Python) and `decodeMatrix`
(`scripts/matrix-format.mjs`, for the build) accept either — a list is dense, a mapping is
sparse.

### Tool (`data_yaml/tools/<slug>.yaml`)

```yaml
name: MQT QECC
description: Tools for quantum error correcting codes.
homepage_url: https://mqt.readthedocs.io/projects/qecc/en/latest/
github_url: https://github.com/munich-quantum-toolkit/qecc
paper_urls: [https://arxiv.org/abs/2408.11894]
aliases: ["mqt.qecc", "Munich Quantum Toolkit", "QECC"]
tags: [Python, encoding, state-preparation]
```

Tools must be added manually before circuits can reference them.

Tool `aliases` work like a code's, with one difference in how they are indexed: they ride in the low-weight `notes` column of `circuit_search`, because every circuit a tool produced would otherwise match every one of that tool's aliases as strongly as its own name. Tools have no `related`.

### Paper (`data_yaml/papers/<slug>.yaml`)

**Do not write these by hand — fetch them:**

```bash
npm run papers:add -- 2402.17761                 # arXiv id, DOI, or any abs/pdf/doi.org link
npm run papers:missing                           # every circuit source with no paper yet
npm run papers:missing -- --dry-run              # ...report without writing
npm run db:create                                # link circuits to the new papers
```

`papers:missing` is the one to reach for after a bulk import: it scans every
circuit's `source`, skips the ones already covered, and fetches the rest from
arXiv (or Crossref for a DOI-only source). It is idempotent, so running it again
costs nothing.

The result looks like this — `scripts/add_paper.py` writes it:

```yaml
title: Quantum Circuit Discovery for Fault-Tolerant Logical State Preparation with Reinforcement Learning
authors: [Remmy Zen, Jan Olle, Luis Colmenarez, Matteo Puviani, Markus Müller, Florian Marquardt]
year: 2024
arxiv_id: "2402.17761"
doi: 10.1103/gqpr-dgz7
url: https://arxiv.org/abs/2402.17761
```

Required: `title`, `authors` (a non-empty list, **in author order**), `url`.
Optional: `year`, `arxiv_id`, `doi`, `journal_ref`.

**Why fetched and not typed:** author lists are facts about real people, and a
wrong one is a misattribution that then renders on the page and in the circuit's
schema.org JSON-LD. They are also often newer than any given model's training
data, and second-hand sources drift — one import README in this repo paraphrases
its own paper's title inaccurately. If the script cannot fetch a work, add it by
hand from the publisher's page, not from memory.

The script refuses to write a paper with no authors rather than emit a half
record. Crossref genuinely lacks authors on some older DOIs (the 1996 Steane
paper among them) — pass the arXiv id instead, which has them.

This is the **only** part of the repo that touches the network, and it is a
maintainer tool whose output you commit. `npm run db:create` and the site itself
read committed YAML only, and build identically offline.

A paper makes its circuits findable on `/search` by title, author and arXiv id — none of
which appear anywhere else, since a circuit's `source` is just a link. It also turns the
bare URL in the UI into a real citation ("Zen et al. (2024)").

**Circuits do not reference papers.** There is no `paper:` key. `npm run db:create` matches
each circuit's `source` against every paper's `url`, `arxiv_id` and `doi`, tolerating
http/https, a trailing slash, `dx.doi.org`, `/pdf/` vs `/abs/`, and arXiv version suffixes
(`2402.17761v2`). So:

- To make an existing circuit's paper searchable, just add the paper file — nothing else.
- A `source` that matches no paper is fine, not an error. `npm run db:create` and
  `npm run validate:yaml` both list such sources so you know what is missing.

**Quote `arxiv_id`.** Unquoted, `arxiv_id: 2402.17761` is a YAML float, and an id ending in
`0` would silently lose it. `validate:yaml` rejects a non-string, so this fails loudly — but
quote it and save yourself the round trip.

## Notes

- **Restart the dev server** after `db:create` — the Astro process caches the DB connection.
- Running generate twice for the same code detects the existing entry via canonical hash.
- To edit existing data, modify the YAML files directly and run `npm run db:create`.
- **Existing codes: omit `code_name`.** On a dedup match the circuit files under the code's _stored_ slug (e.g. `23-1-7`); any `code_name` you pass is ignored for the slug. Passing a name that _doesn't_ resolve to the stored slug would otherwise orphan the circuit.
- **Overwrites are refused by default.** If a circuit with the same `<code>--<circuit>` slug already exists, `add_circuit` raises `FileExistsError`. Pass `overwrite=True` to replace it in place (the existing `qec_id` is preserved), or choose a distinct `circuit_name`.

## FAQ

**I only have a circuit, no check matrices. Can I still add it?**
Yes. For an encoding circuit use [`extract_code`](#extract-code-from-circuit-optional); for a state-prep circuit use the [derive-matrices helpers](#get-the-check-matrices-from-the-circuit). Both recover the code from the circuit.

**Encoding vs state-preparation vs syndrome extraction — which is my circuit?**
An _encoding_ circuit maps `k` data qubits (plus ancillas) into the codespace; the first `k` qubits carry the logical input. A _state-preparation_ circuit starts from `|0…0⟩` and outputs a fixed logical state (`|0⟩_L`, `|+⟩_L`, …). A _syndrome-extraction_ round acts on a state that is **already** encoded, and reads the checks into ancillas. Most library circuits are state-prep. The choice sets the `encoding` / `state-preparation` / `syndrome-extraction` tag, which routes `validate:circuits` — and the three are validated by genuinely different means, so tagging it wrong means checking the wrong property.

**My circuit uses different qubit indices than the stored code.**
Expected — see [Fitting to an existing code](#fitting-to-an-existing-code). You rarely need to work out the permutation by hand.

**How do I mark a circuit fault-tolerant?**
Explicitly, with the `ft` (or `non-ft`) tag — it is **never** inferred. Add `flag` if it uses flag qubits.

**Do I need to add a `tool:` tag?**
No. Set the circuit's `tool` field; the `tool:<slug>` tag is derived at build time (see [Step 3](#step-3-add-tags)).

**`add_circuit` raised `UncertainDedupError` or `FileExistsError`.**
`UncertainDedupError` — the code looks like a stored one but the permutation couldn't be confirmed; supply `qubit_permutation=σ` or `assume_new=True`. `FileExistsError` — a circuit with that `<code>--<circuit>` slug exists; pass `overwrite=True` (keeps the `qec_id`) or use a distinct `circuit_name`.

**The website didn't change after I rebuilt.**
Restart the dev server after `npm run db:create` — Astro caches the DB connection.

**I have many circuits from one paper/tool.**
See [Bulk / dataset imports](#bulk--dataset-imports).
