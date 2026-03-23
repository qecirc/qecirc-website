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
  id, name, slug, description, created_at

functionalities
  id, code_id → codes, name, slug, description, created_at

circuits
  id, functionality_id → functionalities, name, slug,
  source, body (extended STIM text), created_at

tags
  id, name                          -- e.g. "CSS", "distance:3", "single-shot"

taggings
  tag_id → tags, taggable_id, taggable_type  -- taggable_type ∈ {code, functionality, circuit}
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
| Framework  | Astro (TypeScript, hybrid)    | Static-first with SSR islands for dynamic filtering |
| Database   | SQLite via `better-sqlite3`   | Zero external services, file-based, simple          |
| Styling    | Tailwind CSS                  | Standard utility-first, minimal custom CSS          |
| Hosting    | Self-hosted (agnostic)        | Avoid platform lock-in                              |

**Rendering strategy — Astro hybrid mode:**

- Static pages: landing, code/functionality index pages (pre-rendered at build time)
- SSR + API endpoints: search, tag filtering, circuit detail (rendered on request)
- Interactive islands: filter UI, circuit viewer (client-side JS, minimal scope)

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
│   └── qecirc.db          # SQLite database (gitignored in prod, seeded in dev)
├── .github/
│   └── ISSUE_TEMPLATE/    # Circuit submission issue template
├── docs/
│   └── circuit-format.md  # Extended STIM format spec (extensions beyond tsim only)
├── scripts/               # One-off data and migration scripts
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
```

---

## Do Not

- Add npm dependencies without explicit justification in the PR description
- Use platform-specific deployment APIs
- Implement user authentication — submission is via GitHub Issues only
- Modify the STIM parser without updating `docs/circuit-format.md`
- Commit directly to `main` — all changes go through a pull request
- Store secrets or API tokens in code or committed `.env` files
