# Original Circuit Data Storage & Circuit Detail Page

## Context

When circuits are added to QECirc, they may undergo qubit permutation/canonicalization to match the code's canonical form. The original submission data (pre-permutation STIM circuit and contributor-provided check matrices) is currently discarded. Users should be able to access this original data for verification and debugging — if something looks wrong, they can compare the canonical form against the original submission.

This feature also introduces a dedicated circuit detail page (`/circuits/[qec_id]`), giving each circuit a shareable URL.

---

## Data Model

### New DB table: `circuit_originals`

Migration `010_circuit_originals.sql`:

```sql
CREATE TABLE circuit_originals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  circuit_id INTEGER NOT NULL UNIQUE REFERENCES circuits(id) ON DELETE CASCADE,
  original_stim TEXT NOT NULL,
  original_hx TEXT NOT NULL,
  original_hz TEXT NOT NULL,
  original_logical_x TEXT NOT NULL,
  original_logical_z TEXT NOT NULL
);

```

- One row per circuit (always populated, even when no permutation was applied).
- The UNIQUE constraint on `circuit_id` implicitly creates an index; no separate index needed.
- Matrix fields store JSON-encoded 2D arrays (same format as `codes.hx`/`codes.hz`).
- `original_stim` stores the full STIM circuit text as submitted.

### YAML storage

New subdirectory: `data_yaml/circuits/originals/`

Per circuit:

- `<code-slug>--<circuit-slug>.original.stim` — original STIM body
- `<code-slug>--<circuit-slug>.original.yaml` — original matrices:

```yaml
hx: [[1, 0, 1, ...], ...]
hz: [[0, 1, 0, ...], ...]
logical_x: [[1, 1, 0, ...], ...]
logical_z: [[0, 0, 1, ...], ...]
```

---

## Ingestion Pipeline Changes

### `scripts/add_circuit/compute_circuit.py`

- Currently only captures `original_stim` when a permutation is applied (line 28-32). Change to always capture the input STIM text as `original_stim`, regardless of whether permutation is applied.

### `scripts/add_circuit/generate.py`

- The `--hx`/`--hz` args are the as-submitted matrices (before `canonical_form()` in `compute.py`). `generate.py` writes these directly as `originals/<stem>.original.yaml`.
- Writes `originals/<stem>.original.stim` from the `original_stim` field returned by `compute_circuit_data`.
- When no permutation is applied, original STIM = canonical STIM. Original matrices = the input matrices.

### `scripts/add_circuit/yaml_helpers.py`

- Add `build_original_yaml(data)` helper for the original matrices YAML.

### `scripts/db/create_database.mjs`

- After inserting a circuit, check for matching files in `data_yaml/circuits/originals/`.
- Add prepared statement `insertOriginal` for `circuit_originals`.
- Read `<stem>.original.stim` and `<stem>.original.yaml`, insert into `circuit_originals`.

---

## Circuit Detail Page

### Route: `/circuits/[qec_id].astro`

SSR page (`prerender = false`).

### Layout

1. **Back-link**: Simple link back to the parent code page (e.g. "< Steane Code")
2. **Header**: Circuit name, `#N` ID badge, metrics grid (same color-coded badges as CircuitRow)
3. **Metadata row**: Source, Tool, Crumble/Quirk links
4. **Notes**: Full notes text (no truncation needed on a detail page)
5. **Tags**: Tag badges
6. **Canonical circuit bodies**: Format tabs (STIM/QASM/Cirq) with CodeBlock component, copy/download
7. **Collapsible "Original submission" section** (collapsed by default):
   - Original STIM body (CodeBlock with copy/download)
   - Original matrices displayed with the existing `MatrixDisplay` component (Hx, Hz, Logical X, Logical Z)
   - Label: "Original submission (before canonicalization)"

### Query functions (`src/lib/queries.ts`)

- `getCircuitByQecId(qecId)` — fetch circuit + code info by qec_id
- `getOriginalForCircuit(circuitId)` — fetch from `circuit_originals`

### Types (`src/types/index.ts`)

```typescript
interface CircuitOriginal {
  original_stim: string;
  original_hx: string; // JSON string
  original_hz: string;
  original_logical_x: string;
  original_logical_z: string;
}
```

---

## Link from Code Page

In `CircuitRow.astro`, the circuit name becomes a link:

```html
<a href={`/circuits/${circuit.qec_id}`} class="font-medium text-sm truncate hover:underline">
  {circuit.name}
</a>
```

This replaces the plain `<span>` currently used for the name.

---

## Files to Modify

| File                                        | Change                                           |
| ------------------------------------------- | ------------------------------------------------ |
| `data/migrations/010_circuit_originals.sql` | New migration                                    |
| `scripts/add_circuit/compute_circuit.py`    | Pass through original matrices                   |
| `scripts/add_circuit/generate.py`           | Write original files to `originals/`             |
| `scripts/add_circuit/yaml_helpers.py`       | Add `build_original_yaml`                        |
| `scripts/db/create_database.mjs`            | Read originals, insert into DB                   |
| `src/types/index.ts`                        | Add `CircuitOriginal` type                       |
| `src/lib/queries.ts`                        | Add `getCircuitByQecId`, `getOriginalForCircuit` |
| `src/pages/circuits/[qec_id].astro`         | New circuit detail page                          |
| `src/components/CircuitRow.astro`           | Link circuit name to detail page                 |

### Existing components reused (no changes needed)

- `MatrixDisplay.astro` — for original matrices
- `CodeBlock.astro` — for original STIM body
- `Layout.astro` — page wrapper

---

## Verification

1. Run `npm run db:create` — verify `circuit_originals` table is populated
2. Run `npm run dev` and visit `/circuits/1` — verify full detail page renders
3. Verify original submission section shows original STIM and matrices
4. Verify circuit name on code page links to detail page
5. Run `npm run lint` and `npm run format:check`
6. Run `npm run validate:yaml` to ensure original YAML files pass schema validation
