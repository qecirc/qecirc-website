# CLAUDE.md

## Project Overview

**QECirc** is a community-driven web library for quantum error correction (QEC) circuits.
Users can browse and discover circuits, and contribute new ones by opening a GitHub Issue.
Circuits are stored in an extended STIM format (see [tsim](https://github.com/QuEraComputing/tsim#supported-instructions)).

---

## Data Model & Hierarchy

```
Code                          e.g. "Surface Code"
  └── Circuit Functionality       e.g. "Syndrome Extraction"
        └── Circuit                   e.g. "distance-3, single-shot"
```

**Circuit Functionality** is user-defined — any string is valid (e.g. `syndrome-extraction`,
`state-preparation`, `encoding`, `decoding`). There is no fixed enum.

Each level supports **tags** to aid discovery and filtering:

| Level                  | Example tags                              |
|------------------------|-------------------------------------------|
| Code                   | `CSS`, `topological`, `bosonic`           |
| Circuit Functionality  | `single-shot`, `fault-tolerant`           |
| Circuit                | `depth-optimal`, `distance:3`             |

Tags can be either **structured** (`key:value`, e.g. `distance:3`) or **free-form strings**.

### Database Schema

Each hierarchy level is its own table. Tags are stored in a shared `tags` table with a
polymorphic join so all three levels support tagging uniformly.

```
codes
  id, name, slug, description, n, k, d, created_at
  -- n, k, d: code parameters [[n,k,d]] for direct querying/sorting

functionalities
  id, code_id → codes, name, slug, description, created_at

circuits
  id, functionality_id → functionalities, name, slug,
  source, format (default 'stim'), body, created_at
  -- source: provenance (DOI, URL, or citation)
  -- format: circuit format identifier (e.g. 'stim')

tags
  id, name                          -- e.g. "CSS", "distance:3", "single-shot"

taggings
  tag_id → tags, taggable_id, taggable_type  -- taggable_type ∈ {code, functionality, circuit}
  -- composite PK (tag_id, taggable_id, taggable_type)
```

---

## Circuit Format

Circuits use an extended STIM format.
See the [tsim instruction reference](https://github.com/QuEraComputing/tsim#supported-instructions)
for supported instructions. Any extensions beyond tsim must be documented in `docs/circuit-format.md`.

---

## Submission Workflow

Circuits are submitted by opening a GitHub Issue using the provided template.
A maintainer reviews the issue, and if valid, manually adds the circuit to the data store
and closes the issue.

There is **no automation** in the ingestion pipeline for now.

---

## Tech Stack

| Layer      | Choice                        | Rationale                                          |
|------------|-------------------------------|----------------------------------------------------|
| Framework  | Astro v6 (TypeScript)         | Static-first with SSR opt-in for dynamic pages      |
| Database   | SQLite via `better-sqlite3`   | Zero external services, file-based, simple          |
| Styling    | Tailwind CSS                  | Standard utility-first, minimal custom CSS          |
| Hosting    | Self-hosted (agnostic)        | Avoid platform lock-in                              |

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
│   └── qecirc.db          # SQLite database (gitignored, seeded in dev)
├── .github/
│   └── ISSUE_TEMPLATE/    # Circuit submission issue template
├── docs/
│   └── circuit-format.md  # Extended STIM format spec (extensions beyond tsim only)
├── scripts/
│   ├── add_circuit/       # Circuit ingestion modules (Python)
│   ├── db/                # DB migration, seed, and reset scripts (Node)
│   └── tests/             # Python tests for ingestion scripts
└── public/
```

---

## Git Conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

**Format:** `<type>(<scope>): <description>`

| Type       | When to use                                      |
|------------|--------------------------------------------------|
| `feat`     | New user-facing feature                          |
| `fix`      | Bug fix                                          |
| `refactor` | Code change with no behaviour change             |
| `chore`    | Deps, config, tooling                            |
| `docs`     | Documentation only                               |
| `test`     | Adding or updating tests                         |

**Examples:**
```
feat(browse): add tag filter to circuit listing
fix(parser): handle missing QUBIT_COORDS in extended STIM
docs(format): document REPEAT block extension
chore(deps): update astro to v5.5.0
```

---

## Key Principles

- **Minimal dependencies** — exhaust built-ins and stdlib before adding a package
- **No external services** — SQLite only, no hosted DB, no third-party APIs
- **Hosting-agnostic** — use standard Node.js; avoid platform-specific APIs
- **Standard tooling** — no niche or experimental libraries

---

## Commands

```bash
npm run dev          # Start local development server
npm run build        # Production build
npm run preview      # Preview production build locally
npm run lint         # ESLint
npm run test         # Run test suite
npm run db:migrate   # Apply database migrations
npm run db:seed      # Seed database with example circuits (dev only)
npm run db:reset     # Drop database, re-migrate, and re-seed
```

---

## Do Not

- Add npm dependencies without explicit justification in the PR description
- Use platform-specific deployment APIs
- Implement user authentication — submission is via GitHub Issues only
- Modify the STIM parser without updating `docs/circuit-format.md`
- Commit directly to `main` — all changes go through a pull request
- Store secrets or API tokens in code or committed `.env` files
