# Adding Circuits

Three-step workflow: **generate** a YAML payload, **review** it, then **export** to `data_yaml/` source files.

## Prerequisites

```bash
uv sync                # install Python dependencies
npm run db:create      # ensure database is built (needed for dedup check)
```

## What You Need

- **Hx, Hz matrices** as JSON (inline string or file path)
- **STIM circuit file(s)** in [extended STIM format](https://github.com/QuEraComputing/tsim#supported-instructions)
- **Metadata**: code name, circuit name(s), source (DOI/URL), tool slug, code distance

## Step 1: Generate

The `generate` script computes all derived data from the matrices and circuit files:

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
  --d 3 \
  -o payload.yaml
```

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
| `-o` | no | Output path (default: `payload.yaml`) |

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

## Step 2: Review

Open the generated payload YAML and check:

- **`code.status`**: `new` (will create code file) or `existing` (code already in `data_yaml/`)
- **`validation`** per circuit: should be `passed`
- **`tags`**: remove unwanted suggestions, add missing tags
- **`slug`** values: these become URL paths and filenames
- **`bodies`**: verify format conversions look correct

## Step 3: Export

```bash
# Preview what files will be created
python -m scripts.add_circuit.export --dry-run payload.yaml

# Export to data_yaml/
python -m scripts.add_circuit.export payload.yaml

# Rebuild the database and restart the server
npm run db:create && npm run dev
```

This creates the following files in `data_yaml/`:
- **Code YAML** (if new): `data_yaml/codes/<code-slug>.yaml`
- **Circuit YAML**: `data_yaml/circuits/<code-slug>--<circuit-slug>.yaml`
- **Body files**: `data_yaml/circuits/<code-slug>--<circuit-slug>.stim` (and `.qasm`, `.cirq` if conversions succeeded)

## File Formats

### Tool (`data_yaml/tools/<slug>.yaml`)

```yaml
name: MQT QECC
description: Tools for quantum error correcting codes, part of the Munich Quantum Toolkit.
homepage_url: https://mqt.readthedocs.io/projects/qecc/en/latest/
github_url: https://github.com/munich-quantum-toolkit/qecc
tags: [Python, encoding, state-preparation]
```

The slug is derived from the filename (e.g., `mqt-qecc.yaml` -> slug `mqt-qecc`). Tools must be added manually before circuits can reference them.

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

The circuit slug and code reference are both derived from the filename. The double dash (`--`) separates the code slug from the circuit slug: `steane-code--standard-encoding.yaml`.

Body files share the same stem with a format-specific extension:
- `steane-code--standard-encoding.stim` — STIM circuit body
- `steane-code--standard-encoding.qasm` — OpenQASM body (optional)
- `steane-code--standard-encoding.cirq` — Cirq body (optional)

## Full Example: Steane Code [[7,1,3]]

Example input files are in `docs/examples/`.

### 1. Generate

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
  --d 3 \
  -o steane_payload.yaml
```

### 2. Review

```bash
cat steane_payload.yaml
```

### 3. Export and rebuild

```bash
python -m scripts.add_circuit.export --dry-run steane_payload.yaml
python -m scripts.add_circuit.export steane_payload.yaml
npm run db:create && npm run dev
```

## Notes

- **Tools** must exist as YAML files in `data_yaml/tools/` before circuits can reference them by slug.
- **Distance** (`--d`) is computed automatically using `ldpc` if omitted, but providing it is faster and avoids timeout issues for large codes.
- Running generate twice for the same code detects the existing entry in `data_yaml/codes/` and sets `status: existing`.
- To edit existing data, modify the YAML files directly and run `npm run db:create && npm run dev`.
