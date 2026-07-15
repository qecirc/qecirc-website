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

| You have…                                                   | Use                   | Section                                                           |
| ----------------------------------------------------------- | --------------------- | ----------------------------------------------------------------- |
| An **encoding** circuit + check matrices (`Hx/Hz` or `H`)   | `add_circuit()`       | [Steps 1–4](#step-1-inspect)                                      |
| A **state-preparation** circuit (matrices optional)         | `import_state_prep()` | [State-preparation circuits](#adding-a-state-preparation-circuit) |
| A circuit whose qubit labeling differs from the stored code | either, with a _fit_  | [Fitting to an existing code](#fitting-to-an-existing-code)       |
| **Many** circuits from one source/paper                     | a dataset importer    | [Bulk / dataset imports](#bulk--dataset-imports)                  |

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
from scripts.add_circuit import validate_encoding, validate_state_prep

# For encoding circuits:
print(validate_encoding(circuit, Hx, Hz))   # 'passed' or 'failed: ...'

# For state-preparation circuits:
print(validate_state_prep(circuit, Hx, Hz)) # 'passed' or 'failed: ...'
```

Validation uses your provided Hx/Hz (same source as the circuit). If the code already exists in the library with a different qubit ordering, `add_circuit()` handles the relabeling separately.

For a **non-CSS** code there is no Hx/Hz split; pass the symplectic `h` (shape
`(m, 2n)`, X-half then Z-half — the form stored in `codes.h`) instead:

```python
from scripts.add_circuit import validate_encoding_h, validate_state_prep_h

print(validate_encoding_h(circuit, h, n))    # 'passed' or 'failed: ...'
print(validate_state_prep_h(circuit, h, n))  # 'passed' or 'failed: ...'
```

These are the general implementations — the Hx/Hz pair above is a thin wrapper —
so CSS codes may use either. Both check each stabilizer up to **sign** (`|⟨S⟩| = 1`,
not `⟨S⟩ = +1`): a sign-free binary `h` names a stabilizer group only up to a Pauli
frame, so a circuit preparing a codeword in a different frame is still valid.

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

State-prep and encoding circuits get one more, `.stim-annotated`, written by
`uv run python scripts/annotate_circuits.py` (idempotent — run it after adding
such a circuit). It restates the `|0…0⟩` input that the canonical `.stim` body
leaves implied, and adds a terminal readout with detectors where a readout basis
exists. It is a view of the STIM body rather than a display format, so it gets no
format tab; the Detectors toggle derives both views from it. The canonical
`.stim` body must stay reset-free — `to_tableau()` and the derive/fit machinery
depend on that.

### Original submission (`data_yaml/circuits/originals/`)

For each circuit, the pipeline generates two files preserving the original (pre-canonicalization) data:

- `<code-slug>--<circuit-slug>.original.stim` — the STIM circuit as submitted
- `<code-slug>--<circuit-slug>.original.yaml` — the contributor's symplectic stabilizer / logical matrices, before any canonicalization or qubit relabeling:

```yaml
h:
  - [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
  - ...
logical:
  - [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
  - [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
```

These files are loaded into the `circuit_originals` database table during `npm run db:create` and displayed on the circuit detail page (`/circuits/[qec_id]`).

### Tool (`data_yaml/tools/<slug>.yaml`)

```yaml
name: MQT QECC
description: Tools for quantum error correcting codes.
homepage_url: https://mqt.readthedocs.io/projects/qecc/en/latest/
github_url: https://github.com/munich-quantum-toolkit/qecc
paper_urls: [https://arxiv.org/abs/2408.11894]
tags: [Python, encoding, state-preparation]
```

Tools must be added manually before circuits can reference them.

## Notes

- **Restart the dev server** after `db:create` — the Astro process caches the DB connection.
- Running generate twice for the same code detects the existing entry via canonical hash.
- To edit existing data, modify the YAML files directly and run `npm run db:create`.
- **Existing codes: omit `code_name`.** On a dedup match the circuit files under the code's _stored_ slug (e.g. `23-1-7`); any `code_name` you pass is ignored for the slug. Passing a name that _doesn't_ resolve to the stored slug would otherwise orphan the circuit.
- **Overwrites are refused by default.** If a circuit with the same `<code>--<circuit>` slug already exists, `add_circuit` raises `FileExistsError`. Pass `overwrite=True` to replace it in place (the existing `qec_id` is preserved), or choose a distinct `circuit_name`.

## FAQ

**I only have a circuit, no check matrices. Can I still add it?**
Yes. For an encoding circuit use [`extract_code`](#extract-code-from-circuit-optional); for a state-prep circuit use the [derive-matrices helpers](#get-the-check-matrices-from-the-circuit). Both recover the code from the circuit.

**Encoding vs state-preparation — which is my circuit?**
An _encoding_ circuit maps `k` data qubits (plus ancillas) into the codespace; the first `k` qubits carry the logical input. A _state-preparation_ circuit starts from `|0…0⟩` and outputs a fixed logical state (`|0⟩_L`, `|+⟩_L`, …). Most library circuits are state-prep. The choice sets the `encoding` / `state-preparation` tag, which routes `validate:circuits`.

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
