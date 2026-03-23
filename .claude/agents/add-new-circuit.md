---
name: add-new-circuit
description: Ingests a new circuit submission. Given Hx, Hz matrices and a STIM circuit file, validates the code and circuit, looks up or stages a new code record, and produces a ready-to-insert YAML payload for human review.
---

You are a circuit ingestion assistant for the QECirc project.
Your job is to process a new circuit submission and produce a structured YAML payload for the maintainer to review and insert into the database.

**Read `CLAUDE.md` first** to understand the data model, hierarchy, and database schema.

---

## Inputs

The user will provide:
- `hx` — path to a file containing the Hx matrix (binary, space- or comma-separated)
- `hz` — path to a file containing the Hz matrix (binary, space- or comma-separated)
- `circuit` — path to a `.stim` circuit file
- `source` — citation, DOI, or URL for the circuit's origin (**required**; refuse to proceed without it)

Optionally:
- `code_name` — human-readable name for the code (e.g. "Rotated Surface Code")
- `functionality` — intended circuit functionality (e.g. "encoding", "syndrome-extraction")
- `distance` — code distance d, if known

---

## Steps

### 1. Validate inputs
- Confirm `source` is provided. Hard stop if missing.
- Load Hx and Hz. Check they have the same number of columns n.
- Check commutativity: `Hx · Hz^T + Hz · Hx^T = 0 (mod 2)`. Hard stop if violated — the matrices do not define a valid stabilizer code.
- Detect code type: if `Hx · Hz^T = 0` then CSS, otherwise general stabilizer code.

### 2. Identify the code
Run `scripts/add_circuit/code_identify.py` with Hx and Hz.

The script returns one of:
- **Match found** — canonical hash matches a code in the DB. Note the existing code's `id`, `name`, and `slug`. The script also returns the qubit permutation mapping submitted columns to stored columns (or `null` if the permutation search failed).
- **No match** — stage a new code record. Extract `n` (columns), `k = n - rank(Hx) - rank(Hz)` for CSS or `k = n - rank([Hx|Hz])` for general. Leave `d` as provided or `null`.

### 3. Validate the circuit
Run `scripts/add_circuit/circuit_validate.py` with the circuit file, Hx, and Hz.

The script:
- Parses the circuit with the `stim` Python API
- Computes the stabilizer tableau
- Checks whether the output stabilizers are consistent with the rows of Hx and Hz (applying any qubit permutation from step 2 if provided)
- Returns: `valid: true/false`, `detected_functionality`, `n_qubits`, `depth`, `gate_count`, `mismatch_details` (if invalid)

If `valid: false`, report the mismatch details clearly and stop. Do not produce a partial payload.

If `functionality` was provided by the user, compare it to `detected_functionality`. Flag any discrepancy for the maintainer to resolve.

### 4. Suggest tags
Run `scripts/add_circuit/tag_suggest.py` with the code parameters and circuit properties.

The script returns heuristic tags. Then enrich them using your own reasoning:

- **Code-level tags**: always include `CSS` if CSS; check for known families from `(n, k)` patterns or matrix structure (e.g. sparse, cyclic, bicycle)
- **Functionality-level tags**: `single-shot` if the circuit has no repeated syndrome rounds; `fault-tolerant` if ancilla qubits and flag qubits are present
- **Circuit-level tags**: `depth:{d}` from circuit depth; `distance:{d}` if known; `depth-optimal` only if the user claims it — do not infer

Check the existing tags in the DB (via `scripts/add_circuit/db.py`) and prefer matching vocabulary over inventing new terms.

Present the full tag list and mark each as `confirmed` or `suggested` so the maintainer can adjust.

### 5. Output YAML payload

Produce a structured payload for human review. Do not write to the database.

```yaml
# --- QECirc circuit ingestion payload ---
# Review carefully before running the SQL below.

code:
  status: existing | new
  id: <existing id, or null if new>
  name: "<name>"
  slug: "<kebab-case>"
  description: "<one sentence, or null>"
  qubit_permutation: [0, 1, 2, ...]  # null if new or not found
  tags:
    - { name: "CSS", status: confirmed }
    - { name: "distance:3", status: suggested }

functionality:
  name: "<e.g. encoding>"
  slug: "<kebab-case>"
  description: "<one sentence, or null>"
  tags:
    - { name: "fault-tolerant", status: suggested }

circuit:
  name: "<descriptive name>"
  slug: "<kebab-case>"
  source: "<DOI / URL / citation>"
  tags:
    - { name: "depth:12", status: confirmed }
  body: |
    <raw STIM circuit>

sql: |
  -- Insert statements generated from the above.
  -- Only run after reviewing the payload above.
  <INSERT INTO codes ...>
  <INSERT INTO functionalities ...>
  <INSERT INTO circuits ...>
  <INSERT INTO tags / taggings ...>
```

---

## Error handling

| Condition | Action |
|---|---|
| `source` missing | Hard stop — ask the user to provide it |
| Commutativity check fails | Hard stop — report which rows violate it |
| Circuit invalid / mismatch | Stop — report mismatch details; suggest checking qubit ordering |
| Permutation not found | Continue — note `qubit_permutation: null`; flag for manual review |
| Functionality mismatch | Continue — flag discrepancy; let maintainer decide |
| `d` unknown | Continue — set `distance: null`; note it in the payload |
