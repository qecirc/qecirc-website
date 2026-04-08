# CLAUDE.md

## Project Overview

**QECirc** is a community-driven web library for quantum error correction (QEC) circuits.
Users can browse and discover circuits, and contribute new ones by opening a GitHub Issue.
Circuits are stored in an extended STIM format (see `docs/circuit-format.md`).

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
  hx, hz, logical_x, logical_z, canonical_hash, created_at
  -- n, k, d: code parameters [[n,k,d]] for direct querying/sorting
  -- zoo_url: optional link to QEC Zoo
  -- hx, hz, logical_x, logical_z: JSON-encoded matrices (e.g. [[1,0],[0,1]])
  -- canonical_hash: SHA256 of canonical form for dedup (indexed)

tools
  id, name, slug, description, homepage_url, github_url, created_at
  -- software tools used to create circuits

circuits
  id, qec_id, code_id → codes, name, slug, description, source,
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

tags
  id, name                          -- e.g. "CSS", "distance:3", "encoding"

taggings
  tag_id → tags, taggable_id, taggable_type  -- taggable_type ∈ {code, circuit, tool}
  -- composite PK (tag_id, taggable_id, taggable_type)
```

---

## Circuit Format

Circuits use an extended STIM format.
See `docs/circuit-format.md` for supported instructions and any extensions.

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
- SSR pages (`prerender = false`): all `/codes/...` routes, `/api/search` (rendered on request, read from SQLite)
- Client-side JS (minimal): search bar (debounced fetch), CodeBlock copy button, filter input validation + auto-submit

This keeps the site fast and simple while scaling comfortably to thousands of circuits.

---

## Repository Structure

```
├── src/
│   ├── pages/             # Astro pages (routes)
│   ├── components/        # Reusable Astro/UI components
│   ├── lib/               # DB client, STIM parser, helpers
│   └── types/             # Shared TypeScript types
├── data/
│   ├── migrations/        # SQL migration files (e.g. 001_initial.sql)
│   └── qecirc.db          # SQLite database (gitignored, built from data_yaml/)
├── data_yaml/             # Source of truth for all library data (git-tracked)
│   ├── tools/             # One YAML per tool (e.g. mqt-qecc.yaml)
│   ├── codes/             # One YAML per code (e.g. steane-code.yaml)
│   └── circuits/          # YAML + body files per circuit (e.g. steane-code--standard-encoding.yaml/.stim)
├── .github/
│   └── ISSUE_TEMPLATE/    # Circuit submission issue template
├── docs/
│   ├── database.md        # Database & dev server management
│   ├── adding-circuits.md # Circuit ingestion workflow + YAML format reference
│   └── circuit-format.md  # Extended STIM format spec (extensions beyond tsim only)
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
npm run validate:circuits           # Validate encoding/state-prep circuits against stored Hx/Hz
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
- Modify the STIM parser without updating `docs/circuit-format.md`
- Commit directly to `main` — all changes go through a pull request
- Store secrets or API tokens in code or committed `.env` files
