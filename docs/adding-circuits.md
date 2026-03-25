# Adding Circuits

Two-step workflow: **generate** (writes YAML + body files to `data_yaml/`) → **rebuild** the database.

Review changes via `git diff` before rebuilding.

There are two ways to generate: the **CLI** (for one-off additions) and the **Python API** (for programmatic use from your own code).

## Prerequisites

```bash
uv sync                # install Python dependencies
```

## What You Need

- **Hx, Hz matrices** — as JSON (CLI) or numpy arrays (Python API)
- **STIM circuit** — file path (CLI) or `stim.Circuit`/string (Python API)
- **Metadata**: code name, circuit name(s), source (DOI/URL), tool slug, code distance

## Option A: CLI

### Step 1: Generate

```bash
python -m scripts.add_circuit.generate \
  --hx path/to/hx.json \
  --hz path/to/hz.json \
  --stim circuit.stim \
  --code-name "Code Name" \
  --circuit-name "Circuit Name" \
  --source "https://doi.org/..." \
  --tool "tool-slug" \
  --zoo-url "https://errorcorrectionzoo.org/c/..." \
  --d 3
```

This computes all derived data and writes directly to `data_yaml/`:
- **Code YAML** (if new): `data_yaml/codes/<code-slug>.yaml`
- **Circuit YAML**: `data_yaml/circuits/<code-slug>--<circuit-slug>.yaml`
- **Body files**: `.stim`, `.qasm`, `.cirq` (same stem as the circuit YAML)

### Flags

| Flag | Required | Description |
|------|----------|-------------|
| `--hx` | yes | Hx matrix (JSON string or file path) |
| `--hz` | yes | Hz matrix (JSON string or file path) |
| `--stim` | yes | STIM circuit file(s), space-separated |
| `--code-name` | no | Human-readable code name |
| `--circuit-name` | no | Circuit name(s), positionally matched to `--stim` |
| `--source` | no | Provenance (DOI/URL) per circuit |
| `--tool` | no | Tool slug per circuit (must exist in `data_yaml/tools/`) |
| `--description` | no | Brief description per circuit |
| `--zoo-url` | no | QEC Zoo URL for the code |
| `--d` | no | Code distance (computed automatically if omitted) |
| `--data-dir` | no | Path to data_yaml directory (default: `data_yaml`) |

Multiple circuits per code: pass multiple `--stim` files and match with multiple `--circuit-name`, `--source`, `--tool`, `--description` values.

### What it computes

- Code parameters [[n,k,d]], CSS detection, self-dual detection
- Canonical check matrices and hash (for dedup)
- Logical operators (Lx, Lz)
- Circuit metrics (gate count, depth, qubit count)
- Encoding/state-prep validation against the code
- Compact STIM, QASM, and Cirq format conversions
- Crumble and Quirk visualization URLs
- Suggested tags with status (`confirmed`/`suggested`)
- Dedup: if the code already exists in `data_yaml/codes/`, status is `existing` and circuits are relabeled to match the stored qubit ordering

### Step 2: Review and rebuild

```bash
# Review what was generated
git diff

# Rebuild the database and restart the server
npm run db:create && npm run dev
```

## Option B: Python API

For programmatic use — e.g. adding circuits from a script, notebook, or automated pipeline.

```python
import numpy as np
import stim
from scripts.add_circuit import add_circuit

Hx = np.array([[1,1,0,0,1,1,0],[1,0,1,0,1,0,1],[0,0,0,1,1,1,1]])
Hz = np.array([[1,1,0,0,1,1,0],[1,0,1,0,1,0,1],[0,0,0,1,1,1,1]])

circuit = stim.Circuit.from_file("circuit.stim")  # or a stim string

result = add_circuit(
    Hx=Hx,
    Hz=Hz,
    circuit=circuit,
    circuit_name="Standard Encoding",
    source="https://doi.org/10.1098/rspa.1996.0136",
    code_name="Steane Code",
    zoo_url="https://errorcorrectionzoo.org/c/steane",
    d=3,
    tool="mqt-qecc",
)

print(result.summary())
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `Hx` | yes | X-check matrix (numpy array) |
| `Hz` | yes | Z-check matrix (numpy array) |
| `circuit` | yes | STIM circuit (`stim.Circuit` or string) |
| `circuit_name` | yes | Human-readable circuit name |
| `source` | no | Provenance (DOI/URL) |
| `code_name` | no | Code name (optional if code already exists in `data_yaml/`) |
| `zoo_url` | no | QEC Zoo URL for the code |
| `d` | no | Code distance (computed automatically if omitted) |
| `tool` | no | Tool slug (must exist in `data_yaml/tools/`) |
| `description` | no | Circuit description |
| `data_dir` | no | Path to data_yaml directory (default: `"data_yaml"`) |
| `dry_run` | no | If `True`, report what would be written without writing |

### Return value

`add_circuit()` returns an `AddCircuitResult` dataclass:

| Field | Type | Description |
|-------|------|-------------|
| `code_name` | `str` | Code name |
| `code_slug` | `str` | Code slug |
| `code_status` | `str` | `"new"` or `"existing"` |
| `circuit_name` | `str` | Circuit name |
| `circuit_slug` | `str` | Circuit slug |
| `validation` | `str` | `"passed"`, `"skipped"`, or `"failed: ..."` |
| `detected_functionality` | `str \| None` | e.g. `"encoding"`, `"syndrome-extraction"` |
| `files_written` | `list[str]` | Paths of files written (or would-be-written if dry run) |
| `dry_run` | `bool` | Whether this was a dry run |

Call `result.summary()` for a human-readable string.

### Dry run

Preview what would be written without creating any files:

```python
result = add_circuit(..., dry_run=True)
print(result.summary())
```

### After generating

Review and rebuild, same as the CLI workflow:

```bash
git diff
npm run db:create && npm run dev
```

## File Formats

### Tool (`data_yaml/tools/<slug>.yaml`)

```yaml
name: MQT QECC
description: Tools for quantum error correcting codes, part of the Munich Quantum Toolkit.
homepage_url: https://mqt.readthedocs.io/projects/qecc/en/latest/
github_url: https://github.com/munich-quantum-toolkit/qecc
tags: [Python, encoding, state-preparation]
```

The slug is derived from the filename. Tools must be added manually before circuits can reference them.

### Code (`data_yaml/codes/<slug>.yaml`)

```yaml
name: Steane Code
n: 7
k: 1
d: 3
zoo_url: https://errorcorrectionzoo.org/c/steane
canonical_hash: 96e2839c10016a17c64d18ae3b43d6e90e93e1a0a3934c0f16b3277c02cd8dcf
hx: [[1,1,0,0,1,1,0],[1,0,1,0,1,0,1],[0,0,0,1,1,1,1]]
hz: [[1,1,0,0,1,1,0],[1,0,1,0,1,0,1],[0,0,0,1,1,1,1]]
logical_x: [[1,1,1,1,1,1,1]]
logical_z: [[1,1,1,1,1,1,1]]
tags: [CSS, stabilizer, color-code]
```

The slug is derived from the filename. The `canonical_hash` is computed by the `generate` script and used for deduplication.

### Circuit (`data_yaml/circuits/<code-slug>--<circuit-slug>.yaml`)

```yaml
name: Standard Encoding
tool: mqt-qecc
description: "Encodes 1 logical qubit into 7 physical qubits preparing the logical |0⟩ state."
source: https://doi.org/10.1098/rspa.1996.0136
gate_count: 12
depth: 8
qubit_count: 7
crumble_url: "https://algassert.com/crumble#circuit=..."
quirk_url: https://algassert.com/quirk
tags: [encoding, state-preparation]
```

The circuit slug and code reference are derived from the filename (double dash `--` separator). Body files share the same stem with format-specific extensions (`.stim`, `.qasm`, `.cirq`).

## Full Example: Steane Code [[7,1,3]]

Example input files are in `docs/examples/`.

### CLI

```bash
python -m scripts.add_circuit.generate \
  --hx docs/examples/steane_hx.json \
  --hz docs/examples/steane_hz.json \
  --stim docs/examples/steane_encoding.stim \
  --code-name "Steane Code" \
  --circuit-name "Standard Encoding" \
  --source "https://doi.org/10.1098/rspa.1996.0136" \
  --tool "mqt-qecc" \
  --zoo-url "https://errorcorrectionzoo.org/c/steane" \
  --d 3

# Review and rebuild
git diff
npm run db:create && npm run dev
```

### Python API

```python
import numpy as np
from scripts.add_circuit import add_circuit

Hx = np.array([[1,1,0,0,1,1,0],[1,0,1,0,1,0,1],[0,0,0,1,1,1,1]])
Hz = np.array([[1,1,0,0,1,1,0],[1,0,1,0,1,0,1],[0,0,0,1,1,1,1]])

circuit_text = open("docs/examples/steane_encoding.stim").read()

result = add_circuit(
    Hx=Hx,
    Hz=Hz,
    circuit=circuit_text,
    circuit_name="Standard Encoding",
    source="https://doi.org/10.1098/rspa.1996.0136",
    code_name="Steane Code",
    zoo_url="https://errorcorrectionzoo.org/c/steane",
    d=3,
    tool="mqt-qecc",
)

print(result.summary())
# Code: Steane Code [new]
# Circuit: Standard Encoding (encoding) [passed]
# 5 file(s) written:
#   data_yaml/codes/steane-code.yaml
#   data_yaml/circuits/steane-code--standard-encoding.yaml
#   data_yaml/circuits/steane-code--standard-encoding.stim
#   data_yaml/circuits/steane-code--standard-encoding.qasm
#   data_yaml/circuits/steane-code--standard-encoding.cirq
```

## Notes

- **Restart the dev server** after `db:create` — the Astro process caches the DB connection.
- **Tools** must exist as YAML files in `data_yaml/tools/` before circuits can reference them by slug.
- **Distance** (`--d`) is computed automatically using `ldpc` if omitted, but providing it is faster and avoids timeout issues for large codes.
- Running generate twice for the same code detects the existing entry and sets status to `existing`.
- To edit existing data, modify the YAML files directly and run `npm run db:create && npm run dev`.
