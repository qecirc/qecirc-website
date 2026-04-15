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
├── codes/              # one YAML file per code
└── circuits/           # YAML metadata + body files per circuit
    └── originals/      # original (pre-canonicalization) STIM and matrices
```

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

## Original Circuit Data

The `circuit_originals` table stores pre-canonicalization data for each circuit:

| Column               | Description                                     |
| -------------------- | ----------------------------------------------- |
| `circuit_id`         | FK to `circuits` (unique — one row per circuit) |
| `original_stim`      | STIM circuit text as submitted                  |
| `original_hx`        | JSON-encoded Hx matrix as submitted             |
| `original_hz`        | JSON-encoded Hz matrix as submitted             |
| `original_logical_x` | JSON-encoded logical X operators as submitted   |
| `original_logical_z` | JSON-encoded logical Z operators as submitted   |

This data is populated from `data_yaml/circuits/originals/` during `npm run db:create` and displayed on the circuit detail page (`/circuits/[qec_id]`) under "Original submission (before canonicalization)".
