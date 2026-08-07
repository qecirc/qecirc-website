# Database & Dev Server

The SQLite database is a **derived artifact** built from the YAML source files in `data_yaml/`. It is not committed to git.

## Setup

```bash
npm install              # install Node dependencies
uv sync                  # install Python dependencies (for ingestion scripts)
npm run db:create        # build database from YAML source files
npm run dev              # start dev server
```

## Rebuilding the Database

After changing any YAML files in `data_yaml/`, rebuild the database and restart the dev server:

```bash
npm run db:create && npm run dev
```

The dev server caches the database connection, so it **must be restarted** after `db:create` to pick up changes.

## Editing Data

All library data lives in `data_yaml/` as human-editable YAML files:

```
data_yaml/
├── tools/              # one YAML file per tool
├── papers/             # one YAML file per cited paper
├── codes/              # one YAML file per code
├── circuits/           # YAML metadata + body files per circuit
│   └── originals/      # original (pre-canonicalization) STIM, where one was submitted
└── matrices/           # submitted check matrices, content-addressed and shared
```

The two halves of a submission live apart because they have different owners: the
STIM is per circuit, while the matrices a circuit was submitted against are the same
for every circuit of one code, so they are written once as
`data_yaml/matrices/<digest>.yaml` and referenced by the circuit YAML's
`original_matrices: <digest>`.

To edit existing data, modify the YAML files directly and rebuild:

```bash
# edit a file, then:
npm run db:create && npm run dev
```

## Other Database Commands

```bash
npm run db:create                   # Build DB from data_yaml/ (full rebuild)
npm run db:reset                    # Drop DB, re-run migrations (empty DB, no data)
npm run db:migrate                  # Apply pending SQL migrations only
npm run db:clear -- --yes           # Remove codes + circuits from DB, keep tools
npm run db:clear:circuits -- --yes  # Remove circuits only from DB
npm run db:clear:tools -- --yes     # Remove tools only from DB
```

After any of these commands, run `npm run db:create` to restore data from YAML, then restart the dev server.

## Papers

`data_yaml/papers/` holds one file per published work the library's circuits are taken from.
Circuits are linked to them by **matching `circuits.source` against each paper's
`url`/`arxiv_id`/`doi`** during `npm run db:create` — circuit YAML carries no paper
reference, so adding a paper file is enough to enrich every circuit that cites it.

The build prints how many circuits linked, and lists any link-shaped `source` with no paper
behind it:

```
Papers: <n>, linked to <m> circuits.
```

Those unlinked circuits still render and still search by URL; they just cannot be found by
title or author. `npm run validate:yaml` reports the same thing as a warning.

## Original Circuit Data

The `circuit_originals` table stores pre-canonicalization data for the circuits that have
any. Not every circuit does — one written directly by the pipeline helpers, as the flag
gadgets are, was never submitted in some other form, and the detail page simply omits the
section for it.

| Column             | Description                                            |
| ------------------ | ------------------------------------------------------ |
| `circuit_id`       | FK to `circuits` (unique — one row per circuit)        |
| `original_stim`    | STIM circuit text as submitted                         |
| `original_h`       | JSON-encoded symplectic stabilizer matrix as submitted |
| `original_logical` | JSON-encoded symplectic logical operators as submitted |

The Hx/Hz/Lx/Lz CSS view is derived from `original_h` / `original_logical` at render time; it is not stored. `original_stim` is populated from `data_yaml/circuits/originals/` and the matrix columns from `data_yaml/matrices/<digest>.yaml` (resolved through the circuit YAML's `original_matrices` digest) during `npm run db:create`, and both are displayed on the circuit detail page (`/circuits/[qec_id]`) under "Original submission (before canonicalization)".
