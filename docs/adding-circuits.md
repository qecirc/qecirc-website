# Adding Circuits

Three-step workflow: **generate** a YAML payload, **review** it, then **export** to `data_yaml/` source files.

The SQLite database is a derived artifact — rebuild it with `npm run db:create` after exporting.

## Prerequisites

```bash
uv sync                # install Python dependencies
```

## What You Need

- **Hx, Hz matrices** as JSON (inline string or file path)
- **STIM circuit file(s)** in [extended STIM format](https://github.com/QuEraComputing/tsim#supported-instructions)
- **Metadata**: code name, circuit name(s), source (DOI/URL), tool slug, code distance

## Step 1: Generate YAML

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
- YAML dedup: if the code already exists in `data_yaml/codes/`, status is `existing` and circuits are relabeled to match the stored qubit ordering

## Step 2: Review YAML

Open the generated YAML and check:

- **`code.status`**: `new` (will export) or `existing` (code already in `data_yaml/`)
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

# Rebuild the database
npm run db:create
```

This writes YAML + body files to `data_yaml/`. For new codes, a code YAML file is created. For each circuit, a `.yaml` metadata file and body files (`.stim`, `.qasm`, `.cirq`) are created.

### File naming

Files use the convention `<code-slug>--<circuit-slug>.<ext>`:
```
data_yaml/circuits/steane-code--standard-encoding.yaml
data_yaml/circuits/steane-code--standard-encoding.stim
data_yaml/circuits/steane-code--standard-encoding.qasm
```

## Example: Steane Code [[7,1,3]]

Example files are in `docs/examples/`.

**`steane_hx.json`** and **`steane_hz.json`** (identical for the self-dual Steane code):
```json
[[1,0,1,0,1,0,1],[0,1,1,0,0,1,1],[0,0,0,1,1,1,1]]
```

**`steane_encoding.stim`**:
```
H 4 5 6
TICK
CX 5 1
TICK
CX 1 2 4 0
TICK
CX 6 4 5 3 2 0
TICK
CX 6 3 4 5 0 1
```

### Generate

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

### Review and export

```bash
# Review the generated YAML
cat steane_payload.yaml

# Preview export
python -m scripts.add_circuit.export --dry-run steane_payload.yaml

# Export to data_yaml/
python -m scripts.add_circuit.export steane_payload.yaml

# Rebuild the database
npm run db:create
```

## Database Management

The database is rebuilt from `data_yaml/` source files:

```bash
npm run db:create                   # Build DB from data_yaml/ (deletes and recreates)
npm run db:reset                    # Drop DB, re-run migrations (empty DB)
npm run db:clear -- --yes           # Remove codes + circuits, keep tools
npm run db:clear:circuits -- --yes  # Remove circuits only, keep codes + tools
npm run db:clear:tools -- --yes     # Remove tools, keep codes + circuits
npm run db:migrate                  # Apply pending migrations
```

## Notes

- **Tools** must exist as YAML files in `data_yaml/tools/` before circuits can reference them.
- **Distance** (`--d`) is computed automatically using `ldpc` if omitted, but providing it is faster and avoids timeout issues for large codes.
- Running generate twice for the same code detects the existing entry in `data_yaml/codes/` and sets `status: existing`.
- To edit existing data, modify the YAML files directly in `data_yaml/` and run `npm run db:create`.
