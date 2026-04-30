# CLAUDE.md

## Project Overview

**QECirc** is a community-driven web library for quantum error correction (QEC) circuits.
Users can browse and discover circuits, and contribute new ones by opening a GitHub Issue.
Circuits are stored in STIM format and converted to QASM/Cirq for display.

---

## Data Model & Hierarchy

```
Code                          e.g. "Surface Code"
  └── Circuit                     e.g. "Standard Encoding"
```

Circuits belong directly to codes. Circuit type (e.g. `encoding`, `syndrome-extraction`)
is represented as a tag, not a separate entity.

Both levels support **tags** to aid discovery and filtering:

| Level   | Example tags                               |
| ------- | ------------------------------------------ |
| Code    | `CSS`, `topological`, `bosonic`            |
| Circuit | `encoding`, `fault-tolerant`, `distance:3` |

Tags can be either **structured** (`key:value`, e.g. `distance:3`) or **free-form strings**.

Circuits also have numeric **metrics** for filtering: `gate_count`, `depth`, `qubit_count`.

### Database Schema

```
codes
  id, name, slug, n, k, d, zoo_url,
  h, logical, canonical_hash, created_at
  -- n, k, d: code parameters [[n,k,d]] for direct querying/sorting
  -- zoo_url: optional link to QEC Zoo
  -- h: symplectic stabilizer matrix, shape (n−k) × 2n, JSON-encoded
  -- logical: symplectic logical operators, shape 2k × 2n, JSON-encoded
  -- For CSS codes, the Hx/Hz/Lx/Lz view is derived in the UI via splitHToCss
  -- canonical_hash: SHA256 of canonical form for dedup (indexed)

tools
  id, name, slug, description, homepage_url, github_url, created_at
  -- software tools used to create circuits

circuits
  id, qec_id, code_id → codes, name, slug, notes, source,
  gate_count, two_qubit_gate_count, depth, qubit_count,
  crumble_url, quirk_url, tool_id → tools, created_at
  -- qec_id: permanent globally unique circuit identifier (displayed as #N, never reused)
  -- source: provenance (DOI, URL, or citation)
  -- gate_count, two_qubit_gate_count, depth, qubit_count: numeric metrics for filtering
  -- crumble_url, quirk_url: optional external visualization links
  -- tool_id: optional link to tool used to create the circuit

circuit_bodies
  id, circuit_id → circuits, format, body
  -- format: circuit format identifier (e.g. 'stim', 'qasm', 'cirq')
  -- UNIQUE(circuit_id, format): one body per format per circuit

circuit_originals
  id, circuit_id → circuits (UNIQUE),
  original_stim, original_h, original_logical
  -- pre-canonicalization data as submitted by contributors
  -- matrix fields are JSON-encoded (same format as codes.h / codes.logical)
  -- populated from data_yaml/circuits/originals/

tags
  id, name                          -- e.g. "CSS", "distance:3", "encoding"

taggings
  tag_id → tags, taggable_id, taggable_type  -- taggable_type ∈ {code, circuit, tool}
  -- composite PK (tag_id, taggable_id, taggable_type)
```

---

## Circuit Format

Circuits are stored in STIM format and converted to QASM/Cirq for display.
The STIM body is the canonical source; QASM/Cirq are generated as alternate
views in `circuit_bodies`.

---

## Submission Workflow

Circuits are submitted by opening a GitHub Issue using the provided template.
A maintainer reviews the issue, then uses the ingestion pipeline to add the circuit.

- **[docs/adding-circuits-agent.md](docs/adding-circuits-agent.md)** — agent-assisted workflow (`/add-circuit` command)
- **[docs/adding-circuits.md](docs/adding-circuits.md)** — manual workflow (Python scripts + YAML editing)

---

## Tech Stack

| Layer     | Choice                      | Rationale                                      |
| --------- | --------------------------- | ---------------------------------------------- |
| Framework | Astro v6 (TypeScript)       | Static-first with SSR opt-in for dynamic pages |
| Database  | SQLite via `better-sqlite3` | Zero external services, file-based, simple     |
| Styling   | Tailwind CSS                | Standard utility-first, minimal custom CSS     |
| Hosting   | Self-hosted (agnostic)      | Avoid platform lock-in                         |

**Rendering strategy — Astro v6 (static default, SSR opt-in):**

- Static pages: landing page, 404 (pre-rendered at build time)
- SSR pages (`prerender = false`): all `/codes/...` and `/circuits/...` routes, `/api/search` (rendered on request, read from SQLite)
- Client-side JS: search bar (debounced fetch), circuit row expand/collapse, format switching, favorites (toggle/filter/export/import), CodeBlock copy/download, filter input validation + auto-submit

This keeps the site fast and simple while scaling comfortably to thousands of circuits.

---

## Repository Structure

```
├── src/
│   ├── pages/             # Astro pages (routes)
│   ├── components/        # Reusable Astro/UI components
│   ├── lib/               # DB client, helpers, client-side scripts
│   │   └── queries/       # Domain-specific DB query modules
│   └── types/             # Shared TypeScript types
├── data/
│   ├── migrations/        # SQL migration files (e.g. 001_initial.sql)
│   └── qecirc.db          # SQLite database (gitignored, built from data_yaml/)
├── data_yaml/             # Source of truth for all library data (git-tracked)
│   ├── tools/             # One YAML per tool (e.g. mqt-qecc.yaml)
│   ├── codes/             # One YAML per code (e.g. steane-code.yaml)
│   └── circuits/          # YAML + body files per circuit (e.g. steane-code--standard-encoding.yaml/.stim)
│       └── originals/     # Original (pre-canonicalization) STIM and matrices per circuit
├── .github/
│   └── ISSUE_TEMPLATE/    # Circuit submission issue template
├── docs/
│   ├── adding-circuits-agent.md # Agent-assisted ingestion workflow (/add-circuit)
│   ├── adding-circuits.md       # Manual ingestion workflow + YAML format reference
│   └── database.md              # Database & dev server management
├── scripts/
│   ├── add_circuit/       # Circuit ingestion modules (Python)
│   ├── db/                # DB creation, migration, and reset scripts (Node)
│   └── tests/             # Python tests for ingestion scripts
└── public/
    ├── favicon.svg            # SVG favicon (light/dark mode via prefers-color-scheme)
    └── apple-touch-icon.png   # 180×180 PNG for iOS home screen
```

---

## Git Conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

**Format:** `<type>(<scope>): <description>`

| Type       | When to use                          |
| ---------- | ------------------------------------ |
| `feat`     | New user-facing feature              |
| `fix`      | Bug fix                              |
| `refactor` | Code change with no behaviour change |
| `chore`    | Deps, config, tooling                |
| `docs`     | Documentation only                   |
| `test`     | Adding or updating tests             |

**Examples:**

```
feat(browse): add tag filter to circuit listing
fix(parser): handle missing QUBIT_COORDS in extended STIM
docs(format): document REPEAT block extension
chore(deps): update astro to v5.5.0
```

---

## Versioning

The project version lives in `package.json` and follows a pre-1.0 SemVer
convention (currently `0.x.y`):

| Bump                              | When to use                                                                                          |
| --------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **minor** (`0.x.0` → `0.(x+1).0`) | Breaking changes — YAML schema changes, DB migrations that drop/rename columns, breaking API changes |
| **patch** (`0.x.y` → `0.x.(y+1)`) | Bug fixes, cosmetic UI changes, doc updates, non-breaking refactors                                  |

Bump the version in the same PR that ships the change.

---

## Licensing

This project uses a dual-license model:

| Scope                                   | License      | File           |
| --------------------------------------- | ------------ | -------------- |
| Code (`src/`, `scripts/`, config files) | MIT          | `LICENSE`      |
| Data (`data_yaml/`)                     | CC BY-SA 4.0 | `LICENSE-DATA` |

---

## Key Principles

- **YAML is the source of truth** — all library data in `data_yaml/`, SQLite is derived
- **Minimal dependencies** — exhaust built-ins and stdlib before adding a package
- **No external services** — SQLite only, no hosted DB, no third-party APIs
- **Hosting-agnostic** — use standard Node.js; avoid platform-specific APIs
- **Standard tooling** — no niche or experimental libraries

---

## Commands

```bash
npm run dev                         # Start local development server
npm run build                       # Production build
npm run preview                     # Preview production build locally
npm run lint                        # ESLint
npm run format:check                # Check Prettier formatting
npm run format                      # Auto-format with Prettier
npm run validate:yaml               # Validate data_yaml/ schemas
npm run validate:circuits           # Validate encoding/state-prep circuits against the code's check matrices (derived from h)
uv run ruff check scripts/          # Lint Python code
uv run ruff format scripts/          # Format Python code
npm run db:create                   # Build database from data_yaml/ (restart dev server after)
npm run db:migrate                  # Apply database migrations
npm run db:reset                    # Drop database and re-migrate (empty DB)
npm run db:clear -- --yes           # Remove codes + circuits, keep tools
npm run db:clear:circuits -- --yes  # Remove circuits only, keep codes + tools
npm run db:clear:tools -- --yes     # Remove tools, keep codes + circuits
```

### Dev Setup

```bash
npm install                         # Install Node dependencies
uv sync                             # Install Python dependencies
npm run db:create                   # Build database from YAML source files
npm run dev                         # Start dev server
```

After editing YAML files: `npm run db:create && npm run dev` (dev server caches the DB connection).

---

## Do Not

- Add npm dependencies without explicit justification in the PR description
- Use platform-specific deployment APIs
- Implement user authentication — submission is via GitHub Issues only
- Commit directly to `main` — all changes go through a pull request
- Store secrets or API tokens in code or committed `.env` files
