# Adding Circuits

Two-step workflow: **generate** a YAML payload, **review** it, then **insert** into the database.

## Prerequisites

```bash
uv sync                # install Python dependencies
npm run db:migrate     # ensure DB schema is up to date
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
| `--tool` | no | Tool slug per circuit (must exist in DB) |
| `--description` | no | Brief description per circuit |
| `--zoo-url` | no | QEC Zoo URL for the code |
| `--d` | no | Code distance (computed automatically if omitted) |
| `--db` | no | SQLite DB path (default: `data/qecirc.db`) |
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
- DB dedup: if the code already exists, status is `existing` and circuits are relabeled to match the stored qubit ordering

## Step 2: Review YAML

Open the generated YAML and check:

- **`code.status`**: `new` (will insert) or `existing` (code already in DB)
- **`validation`** per circuit: should be `passed`
- **`tags`**: remove unwanted suggestions, add missing tags
- **`slug`** values: these become URL paths
- **`bodies`**: verify format conversions look correct

## Step 3: Insert

```bash
python -m scripts.add_circuit.insert payload.yaml
```

This inserts the code (if new), circuits, circuit bodies, and tags into the database.

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

### Review and insert

```bash
# Review the generated YAML
cat steane_payload.yaml

# Insert into the database
python -m scripts.add_circuit.insert steane_payload.yaml
```

## Notes

- **Tools** must exist in the database before you can reference them by slug. Add them via SQL or the seed script.
- **Distance** (`--d`) is computed automatically using `ldpc` if omitted, but providing it is faster and avoids timeout issues for large codes.
- Running generate twice for the same code detects the existing entry and sets `status: existing`.
