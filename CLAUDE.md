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
  id, name, slug, description, homepage_url, github_url, paper_urls, created_at
  -- software tools used to create circuits
  -- paper_urls: JSON-encoded array of associated paper URLs

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
| Framework | Astro v7 (TypeScript)       | Static-first with SSR opt-in for dynamic pages |
| Database  | SQLite via `better-sqlite3` | Zero external services, file-based, simple     |
| Styling   | Tailwind CSS                | Standard utility-first, minimal custom CSS     |
| Hosting   | Self-hosted (agnostic)      | Avoid platform lock-in                         |

**Rendering strategy — Astro v7 (static default, SSR opt-in):**

- Static pages: 404, `/about`, `/contribute`, `/privacy`, `/legal` (pre-rendered at build time)
- SSR pages (`prerender = false`): the landing page `/`, all `/codes/...` and `/circuits/...` routes, `/search`, `/api/search` (rendered on request, read from SQLite)
  - **`/` must stay SSR.** `@astrojs/node` serves pre-rendered pages straight from disk without running middleware, so a static `/` would silently lose the `s-maxage` edge caching (see below). The DB is baked at build time either way, so pre-rendering buys nothing here.
- Client-side JS: search bar (debounced fetch), circuit row expand/collapse, format switching, favorites (toggle/filter/export/import), CodeBlock copy/download, lazy-loaded circuit bodies on code pages (fetched from `/api/circuits/[qec_id]/bodies` on first row expand), and filtering/sorting on the listing pages (`list-filter-client.ts` over `data-metrics`/`data-tags` row attributes — the server always renders the canonical full list and ignores filter params; `/api/download` still parses them)
- **`/search` is the exception: it filters on the server.** That convention's justification — every visit shares one cached document — cannot hold for free-text search, and `list-filter-client.ts` has no text matching and only filters rows already in the DOM. Consequences: `/search` sets its own shorter `Cache-Control` (the `?q=` key space is unbounded) and is `Disallow`ed in `robots.txt`.

**Caching:** `src/middleware.ts` stamps `s-maxage=604800` on every response lacking its own `Cache-Control`; safe only because rendered output is immutable between deploys and each deploy purges Cloudflare (`src/lib/cache-purge.ts`). A page that varies by query string must set its own shorter value.

**Search — two engines, on purpose.** They share a spelling dictionary, nothing else.

|          | header quick-search (`/api/search`)  | `/search`                 |
| -------- | ------------------------------------ | ------------------------- |
| Job      | jump to a known thing                | find things               |
| Scope    | codes, circuits, tools               | circuits only             |
| Matching | LIKE, **substring** — names and tags | FTS5 tokens, plus `notes` |
| Order    | alphabetical, grouped by type        | BM25 relevance            |

**Do not "unify" these by pointing the quick-search at the FTS index.** LIKE matches mid-word (`ycle` → Bivariate Bicycle Code), which token-based FTS cannot — that is what makes a type-ahead usable. There is also no FTS index for codes or tools, and pulling `notes` into a 10-item navigation list would surface circuits that merely mention the term. Enter with nothing highlighted hands over to `/search`; that is where the two meet.

`/search` ranks by BM25 over the `circuit_search` FTS5 table (`data/migrations/015`), which `scripts/db/create_database.mjs` repopulates on every build, and is forgiving in three layers, applied in this order (`src/lib/queries/search.ts` → `resolveQuery`):

1. **Stemming** — `circuit_search` uses the `porter` tokenizer, so `encodings`/`encode`/`encoding` meet at one term.
2. **Spelling correction** — `src/lib/queries/spelling.ts` maps a token that matches _nothing_ to its nearest word in the `search_vocab` dictionary (Damerau-Levenshtein, Elasticsearch "AUTO" edit budget). Shared with the quick-search, so the two agree on what exists. Only unmatched tokens are touched, so a query that already works is never rewritten. Tokens containing digits are never corrected: `#508` is one edit from an arXiv `2508`, and `distance:3` from `distance:5`. `?literal=1` opts out.
3. **OR fallback** — if no circuit matches _every_ term, the query is retried as "any term" and the page says so.

Gotchas if you touch this:

- `search_vocab` must stay **unstemmed** (it indexes `search_terms`, not `circuit_search`) or suggestions become stems — porter stores "steane" as "stean".
- `search_terms` must keep covering **codes and tools**, not just circuits: a tool with no circuits appears in no circuit text, so a circuit-only dictionary cannot fix `autqce` → `autqec`.
- The findability probe asks **both** indexes. `circuit_search` alone would call a tool name a typo; `search_terms` alone is unstemmed and would "correct" `encodings` → `encoding`. Neither answers both cases.
- Results and facets must be built from the _same_ `ResolvedQuery`, or the filter counts describe a different search than the list.

This keeps the site fast and simple while scaling comfortably to thousands of circuits.

**SEO & AI discoverability** (goal: be cited/linked by search and AI answer engines, without inviting training crawlers):

- **Structured data** — schema.org JSON-LD. `Layout.astro` emits a site-wide graph (`Organization` + `WebSite`) on every page and takes a `jsonLd` prop for per-page entities. Circuit pages pass `SoftwareSourceCode` + `BreadcrumbList`; code pages pass `CollectionPage` (+ an `ItemList` of circuits) + `BreadcrumbList`. **When adding a new entity page type, pass matching `jsonLd`.**
- **Machine-facing routes, all `prerender = false` and generated from the live DB** (no manual upkeep — new codes/circuits appear automatically): `sitemap.xml`, `llms.txt` (see [llmstxt.org](https://llmstxt.org/)), and `robots.txt`.
- **`robots.txt` policy** — allow search/answer bots (Googlebot, OAI-SearchBot, PerplexityBot, Claude-User/SearchBot, …) but `Disallow: /` the AI-**training** crawlers (GPTBot, ClaudeBot, CCBot, Google-Extended, …). Keep new AI-training user-agents out; leave search/answer agents in.

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

**Files to update together with `package.json` `version`:**

- `pyproject.toml` `version` field
- `uv.lock` (run `UV_NO_CONFIG=1 uv lock`)
- `package-lock.json` (npm syncs this on `npm install`; commit if it drifted)

**When bumping `engines.node` in `package.json`** (Node major version),
also update `railpack.json` `packages.node` to the same major.

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
