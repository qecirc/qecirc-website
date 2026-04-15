# Adding Circuits (Manual)

How to add circuits to the QECirc library using the Python scripts directly, without any AI assistance.

For the agent-assisted workflow, see [adding-circuits-agent.md](adding-circuits-agent.md).

## Prerequisites

```bash
uv sync                # install Python dependencies
```

## What You Need

- **Hx, Hz matrices** — as JSON files or numpy arrays
- **STIM circuit** — file path or string
- **Code distance `d`** — integer
- **Source** — DOI, URL, or citation

## Overview

1. Inspect your code and circuit with helper functions
2. Generate YAML files with `add_circuit()` or the CLI
3. Add tags manually to the generated YAML files
4. Rebuild the database

---

## Step 1: Inspect

### Check your code

```python
from scripts.add_circuit import check_code, find_existing_code

# Quick summary
print(check_code(Hx, Hz, d=3))
# {'n': 7, 'k': 1, 'd': 3, 'is_css': True, 'is_self_dual': True, 'canonical_hash': '...'}

# Check if it already exists in data_yaml/
print(find_existing_code(Hx, Hz))
# 'steane-code' or None
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

# Generate for real
result = add_circuit(
    Hx=Hx, Hz=Hz, circuit=circuit,
    circuit_name="Standard Encoding", d=3,
    code_name="Steane Code", source="https://doi.org/...",
    tool="mqt-qecc", zoo_url="https://errorcorrectionzoo.org/c/steane",
)
print(result.summary())
```

#### Parameters

| Parameter      | Required | Description                                                 |
| -------------- | -------- | ----------------------------------------------------------- |
| `Hx`           | yes      | X-check matrix (numpy array)                                |
| `Hz`           | yes      | Z-check matrix (numpy array)                                |
| `circuit`      | yes      | STIM circuit (`stim.Circuit` or string)                     |
| `circuit_name` | yes      | Human-readable circuit name                                 |
| `d`            | yes      | Code distance                                               |
| `source`       | no       | Provenance (DOI/URL)                                        |
| `code_name`    | no       | Code name (optional if code already exists in `data_yaml/`) |
| `zoo_url`      | no       | QEC Zoo URL                                                 |
| `tool`         | no       | Tool slug (must exist in `data_yaml/tools/`)                |
| `notes`        | no       | Circuit notes                                               |
| `data_dir`     | no       | Path to data_yaml directory (default: `"data_yaml"`)        |
| `dry_run`      | no       | If `True`, preview without writing                          |

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

The pipeline only auto-assigns mathematically verified code tags (`CSS`, `self-dual`). All other tags must be added manually by editing the generated YAML files.

### Code tags (`data_yaml/codes/<slug>.yaml`)

Add a `tags:` list. Common code tags:

| Category   | Examples                                           |
| ---------- | -------------------------------------------------- |
| Type       | `CSS`, `stabilizer`                                |
| Family     | `color-code`, `surface-code`, `toric-code`, `LDPC` |
| Properties | `self-dual`, `concatenated`                        |

### Circuit tags (`data_yaml/circuits/<code-slug>--<circuit-slug>.yaml`)

Add a `tags:` list. Common circuit tags:

| Category        | Examples                                               |
| --------------- | ------------------------------------------------------ |
| Functionality   | `encoding`, `state-preparation`, `syndrome-extraction` |
| Fault tolerance | `ft`, `non-ft`                                         |
| Properties      | `gate-optimal`, `depth-optimal`, `flag`                |

Check existing tags with:

```bash
grep -h '^tags:' data_yaml/codes/*.yaml data_yaml/circuits/*.yaml
```

Prefer reusing existing tags over inventing new ones.

---

## Step 4: Rebuild

```bash
git diff                          # Review changes
npm run db:create && npm run dev  # Rebuild database and restart
```

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
- **Original submission data**: the pipeline always preserves the original (pre-canonicalization) STIM circuit and contributor-provided check matrices in `data_yaml/circuits/originals/`. These are displayed on the circuit detail page under "Original submission (before canonicalization)".
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
hx: [[1, 1, 0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 1, 1, 1, 1]]
hz: [[1, 1, 0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 1, 1, 1, 1]]
logical_x: [[1, 1, 1, 1, 1, 1, 1]]
logical_z: [[1, 1, 1, 1, 1, 1, 1]]
tags: [CSS, stabilizer, color-code]
```

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

### Original submission (`data_yaml/circuits/originals/`)

For each circuit, the pipeline generates two files preserving the original (pre-canonicalization) data:

- `<code-slug>--<circuit-slug>.original.stim` — the STIM circuit as submitted
- `<code-slug>--<circuit-slug>.original.yaml` — the contributor-provided check matrices:

```yaml
hx: [[1, 0, 1, 0, 1, 0, 1], ...]
hz: [[1, 0, 1, 0, 1, 0, 1], ...]
logical_x: [[1, 1, 1, 1, 1, 1, 1]]
logical_z: [[1, 1, 1, 1, 1, 1, 1]]
```

These files are loaded into the `circuit_originals` database table during `npm run db:create` and displayed on the circuit detail page (`/circuits/[qec_id]`).

### Tool (`data_yaml/tools/<slug>.yaml`)

```yaml
name: MQT QECC
description: Tools for quantum error correcting codes.
homepage_url: https://mqt.readthedocs.io/projects/qecc/en/latest/
github_url: https://github.com/munich-quantum-toolkit/qecc
tags: [Python, encoding, state-preparation]
```

Tools must be added manually before circuits can reference them.

## Notes

- **Restart the dev server** after `db:create` — the Astro process caches the DB connection.
- Running generate twice for the same code detects the existing entry via canonical hash.
- To edit existing data, modify the YAML files directly and run `npm run db:create`.
