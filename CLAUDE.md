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

| Level   | Example tags                                                                            |
| ------- | --------------------------------------------------------------------------------------- |
| Code    | `CSS`, `topological`, `bosonic`                                                         |
| Circuit | `encoding`, `syndrome-extraction`, `fault-tolerant`, `distance:3`, `circuit-distance:2` |

Tags can be either **structured** (`key:value`, e.g. `distance:3`) or **free-form strings**.

Circuits also have numeric **metrics** for filtering: `gate_count`, `depth`, `qubit_count`.

A circuit taken from a published work also links to a **paper**, which is what makes it
findable by title, author or arXiv id. The link is **derived, not declared**: `circuits.source`
already holds the provenance link, so `create_database.mjs` matches it against each paper's
`url`/`arxiv_id`/`doi` rather than making every circuit file repeat it. Add a paper and every
circuit citing it is enriched at the next build; a source with no paper is not an error
(`source: circuit-synth` names a tool, not a work), it just leaves the circuit searchable by
URL alone. Both the build and `validate:yaml` report such sources.

### Database Schema

```
codes
  id, name, slug, n, k, d, zoo_url, aliases, related,
  h, logical, gauge, gauge_qubits, canonical_hash, created_at
  -- n, k, d: code parameters [[n,k,d]] for direct querying/sorting
  -- zoo_url: optional link to QEC Zoo
  -- aliases: other names for THIS code, space-joined (e.g. "Laflamme code")
  -- related: names of a DIFFERENT, adjacent code people use loosely (e.g.
     "toric code" for a planar surface code). Matched only as a last resort,
     and /search says so. See "Search" below.
  -- h: symplectic stabilizer matrix, shape (n−k) × 2n, JSON-encoded
  -- logical: symplectic logical operators, shape 2k × 2n, JSON-encoded
  -- For CSS codes, the Hx/Hz/Lx/Lz view is derived in the UI via splitHToCss
  -- gauge: subsystem codes only — the gauge group a decoder may measure,
  --   symplectic, JSON-encoded. NULL when it coincides with `h`.
  -- gauge_qubits: (rank(gauge) - rank(h)) / 2. Qubits that carry no
  --   information and are not corrected, so k = n - rank(h) - gauge_qubits.
  --   Reading k off `h` alone stored Bacon-Shor [[9,1,3]] as [[9,5,3]].
  -- canonical_hash: SHA256 of canonical form for dedup (indexed) — of the
  --   gauge group when there is one, since two subsystem codes can share a
  --   stabilizer group and differ in what a decoder may measure

tools
  id, name, slug, description, homepage_url, github_url, paper_urls, aliases, created_at
  -- software tools used to create circuits
  -- paper_urls: JSON-encoded array of associated paper URLs
  -- aliases: other names, space-joined (e.g. "Munich Quantum Toolkit")

papers
  id, slug, title, authors, year, arxiv_id, doi, journal_ref, url, created_at
  -- published works circuits are taken from; the ONLY place titles/authors exist
  -- authors: JSON-encoded array of names, in author order
  -- arxiv_id: bare id, no "arXiv:" prefix, no version suffix ("2402.17761")
  --   MUST be quoted in YAML — unquoted it parses as a float and loses digits
  -- url: canonical link, and the value circuits.source is matched against

circuits
  id, qec_id, code_id → codes, name, slug, notes, source,
  gate_count, two_qubit_gate_count, depth, qubit_count,
  crumble_url, quirk_url, tool_id → tools, paper_id → papers, created_at
  -- paper_id: resolved from `source` at build time, NOT declared in YAML.
  --   NULL when the source names a tool or cites an uncatalogued work.
  -- qec_id: permanent globally unique circuit identifier (displayed as #N, never reused)
  -- source: provenance (DOI, URL, or citation)
  -- gate_count, two_qubit_gate_count, depth, qubit_count: numeric metrics for filtering
  -- crumble_url, quirk_url: optional external visualization links
  -- crumble_url_annotated: Crumble link for the 'stim-annotated' body (NULL if none)
  -- tool_id: optional link to tool used to create the circuit

circuit_bodies
  id, circuit_id → circuits, format, body
  -- format: circuit format identifier (e.g. 'stim', 'qasm', 'cirq', 'stim-annotated')
  -- UNIQUE(circuit_id, format): one body per format per circuit
  -- 'stim-annotated' is a *view* of the stim body, not a display format: it adds an
     explicit reset prologue and (for CSS codes) a terminal readout with detectors.
     It gets no format tab; the Detectors toggle derives both views from it.

circuit_originals
  id, circuit_id → circuits (UNIQUE),
  original_stim, original_h, original_logical
  -- pre-canonicalization data as submitted by contributors — NOT every
  --   circuit has a row: a circuit written directly by the pipeline helpers
  --   (the flag gadgets) was never submitted in some other form
  -- matrix fields are JSON-encoded (same format as codes.h / codes.logical)
  -- original_stim from data_yaml/circuits/originals/, one file per circuit
  --   that has one; matrices from data_yaml/matrices/<digest>.yaml, shared by every circuit
  --   of a code and referenced by the circuit YAML's `original_matrices`.
  --   create_database.mjs resolves the reference, so this table is unchanged.

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

**Matrices are stored once, and sparsely when large.** A code's `h`/`logical` and the
matrices a circuit was submitted against are written as plain 0/1 rows up to
`SPARSE_MIN_ENTRIES` (`scripts/add_circuit/matrix_format.py`) and as nonzero column
indices above it — `h` is (n−k) × 2n, so a dense encoding costs O(n²) characters whatever
the code's density. Submitted matrices are shared: they live once in
`data_yaml/matrices/<digest>.yaml` and circuits reference them by digest. Readers call
`matrix_format.decode` / `decodeMatrix` and never need to know which encoding was used.

The canonical STIM body of a **prep or encoding** circuit is **reset-free** —
`to_tableau()` and the derive/fit machinery need a circuit with no resets — so it
leaves the `|0…0⟩` input implied. Those circuits therefore also carry a
`stim-annotated` body that states it explicitly, plus a terminal readout and
detectors where a readout basis exists.

**Syndrome extraction is the exception, and has to be.** A round _is_ reset,
gates, measure — the resets and measurements are the circuit, not an annotation
of it. So those bodies are not reset-free and have no tableau, and none of the
derive/fit machinery may be pointed at them. They are checked by stabilizer flows
instead (`validate_syndrome_extraction_h`), and their `stim-annotated` body is the
memory experiment the round belongs to: reset the data, `REPEAT d` of the round,
terminal readout, detectors, observable.

Generate both with `uv run python scripts/annotate_circuits.py` (idempotent).

**`distance:<N>` and `circuit-distance:<N>` are different numbers.** The first is the
code's, and it is carried over from the source. The second is the _schedule's_ — the
fewest faults anywhere in the round that flip a logical while firing no detector — and
it is measured, by `scripts/measure_circuit_distance.py`, over both the Z and the X
memory experiment under uniform circuit-level depolarizing noise. It is never larger
than the code's and usually smaller: a fault on an ancilla can land on several data
qubits at once. An absent tag means the search did not finish in its budget, not that
the circuit is fault-free.

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

- **The rule: a route that reads SQLite is `prerender = false`; everything else stays static.** `grep -rn "prerender" src/pages/` is the authoritative list — an enumeration here goes stale the day a page is added, so what follows is examples only.
  - Static (pre-rendered at build time): the prose pages (`/about`, `/contribute`, `/privacy`, `/legal`), `/404`, and `/favorites`, which reads `localStorage` and nothing else.
  - SSR (`prerender = false`, rendered on request): `/`, `/codes/...`, `/circuits/...`, `/tools`, `/search`, every `/api/*` endpoint, and the machine-facing `sitemap.xml` / `llms.txt` / `robots.txt`.
  - **`/` must stay SSR.** `@astrojs/node` serves pre-rendered pages straight from disk without running middleware, so a static `/` would silently lose the `s-maxage` edge caching (see below). The DB is baked at build time either way, so pre-rendering buys nothing here.
- **Unknown id/slug → `return notFound()`** (`src/lib/not-found.ts`), which returns a bodiless 404; Astro fills the body with the prerendered /404 page. Never `Astro.rewrite("/404")` from an SSR page — /404 is prerendered, so the rewrite finds no component instance and 500s (`scripts/smoke.sh` guards this).
- Client-side JS: search bar (debounced fetch), circuit row expand/collapse, format switching, favorites (toggle/filter/export/import), CodeBlock copy/download, lazy-loaded circuit bodies on code pages (fetched from `/api/circuits/[qec_id]/bodies` on first row expand), and filtering/sorting on the listing pages (`list-filter-client.ts` over `data-metrics`/`data-tags` row attributes — the server always renders the canonical full list and ignores filter params; `/api/download` still parses them)
- **`/search` is the exception: it filters on the server.** That convention's justification — every visit shares one cached document — cannot hold for free-text search, and `list-filter-client.ts` has no text matching and only filters rows already in the DOM. Consequences: `/search` sets its own shorter `Cache-Control` (the `?q=` key space is unbounded) and is `Disallow`ed in `robots.txt`.

**Caching:** `src/middleware.ts` stamps `s-maxage=604800` on every response lacking its own `Cache-Control`; safe only because rendered output is immutable between deploys and each deploy purges Cloudflare (`src/lib/cache-purge.ts`). A page that varies by query string must set its own shorter value.

**Search — two engines, on purpose.** They share a spelling dictionary, nothing else.

|          | header quick-search (`/api/search`)            | `/search`                                                  |
| -------- | ---------------------------------------------- | ---------------------------------------------------------- |
| Job      | jump to a known thing                          | find things                                                |
| Scope    | codes, circuits, tools                         | circuits only                                              |
| Matching | LIKE, **substring** — names, aliases, and tags | FTS5 tokens, plus `code_tags`, `paper`, `notes`, `related` |
| Order    | alphabetical, grouped by type                  | BM25 relevance                                             |

**Do not "unify" these by pointing the quick-search at the FTS index.** LIKE matches mid-word (`ycle` → Bivariate Bicycle Code), which token-based FTS cannot — that is what makes a type-ahead usable. There is also no FTS index for codes or tools, and pulling `notes` into a 10-item navigation list would surface circuits that merely mention the term. Enter with nothing highlighted hands over to `/search`; that is where the two meet.

**Paper text is `/search`-only, for the same reason.** A single paper can back hundreds of circuits, so matching a title in a 10-item navigation dropdown would fill it with near-identical rows and bury the code or tool the user was actually jumping to. A paper is something you _find circuits by_, not something you navigate to — there is no paper page to land on.

`/search` ranks by BM25 over the `circuit_search` FTS5 table (migrations `016`–`019`), which `scripts/db/create_database.mjs` repopulates on every build. Its **nine columns** are `circuit_id, name, code_name, aliases, related, tags, code_tags, paper, notes` — and that order is load-bearing (see `BM25_WEIGHTS` below).

What a circuit is findable by, and where each comes from:

| column      | holds                                     | so that                                       |
| ----------- | ----------------------------------------- | --------------------------------------------- |
| `aliases`   | the **code's** other names (017)          | `laflamme` reaches the five-qubit code        |
| `related`   | a **different, adjacent** code's name     | `toric` reaches planar surface codes, flagged |
| `tags`      | the **circuit's** own tags                | `flag`, `distance:3`                          |
| `code_tags` | the **code's** tags (019)                 | `LDPC`, `topological`, `self-dual`            |
| `paper`     | title, authors, ids of its source (018)   | `reinforcement learning`, `forlivesi`         |
| `notes`     | prose + `source` + the **tool's** aliases | everything else                               |

`/search` is forgiving in layers, applied in this order (`src/lib/queries/search.ts` → `resolveQuery`):

1. **Stemming** — `circuit_search` uses the `porter` tokenizer, so `encodings`/`encode`/`encoding` meet at one term.
2. **Spelling correction** — `src/lib/queries/spelling.ts` maps a token that matches _nothing_ to its nearest word in the `search_vocab` dictionary (Damerau-Levenshtein, Elasticsearch "AUTO" edit budget). Shared with the quick-search, so the two agree on what exists. Only unmatched tokens are touched, so a query that already works is never rewritten. Tokens containing digits are never corrected: `#508` is one edit from an arXiv `2508`, and `distance:3` from `distance:5`. `?literal=1` opts out.
3. **The resolution ladder** — `resolveQuery` tries four expressions and stops at the first with hits. Each rung concedes more than the one above it:
   1. every term, over `STRICT_COLUMNS` — what was asked for
   2. every term, allowing `related` — a neighbouring code, **flagged to the user**
   3. any term, `STRICT_COLUMNS` — `partial`
   4. any term, allowing `related`

   (2) precedes (3) deliberately: widening `toric code` to "any term" matches all but a handful of circuits in the library — "code" occurs in nearly every one's text — whereas allowing `related` returns only the surface codes actually meant.

**Column weights and the strict column set are DERIVED, not restated** (`src/lib/queries/search-schema.ts`). Both used to be hand-maintained constants, and both drifted from the table within a week despite shouty comments. `PRAGMA table_info(circuit_search)` returns the real columns in declaration order — which is exactly what `bm25()` wants — so:

- **To add a column:** put it in the migration's `CREATE`, then give it a weight in `COLUMN_WEIGHTS` (keyed by name; order there is irrelevant). That is the whole checklist.
- **Forget the weight and it throws**, naming the column, instead of FTS5 silently scoring it 1.0 and mis-ranking everything.
- **The strict set needs no upkeep**: it is every column minus `circuit_id` (UNINDEXED — naming it in a filter is an FTS5 error) and minus `LOOSE_COLUMNS`. New columns are strict by default, which is the safe direction — wrongly-loose tells a user their exact query found nothing.

**Aliases — a data layer, not a forgiveness layer** (`data/migrations/017`). Codes and tools carry optional `aliases:` (and codes, `related:`) in their YAML; a circuit inherits its code's. The layers above cannot substitute for it: `bb` is two characters, so `editBudget` allows it zero edits, and before this existed `bb codes` returned almost every circuit — the OR fallback firing on `codes`.

- `aliases` = **another name for this code**. Matched silently; the gross code _is_ a BB code.
- `related` = **a different, adjacent code** people reach for loosely. Matched only as a last resort, and `/search` says so. The quick-search ignores `related` entirely: a dropdown has no room to explain itself.
- **Hand-written, not imported.** [errorcorrectionzoo.org](https://errorcorrectionzoo.org) publishes `alternative_names`, but `eczoo_data` is CC-BY-SA 4.0 and this repo is MIT. Use it as reference; do not add an import script. Its taxonomy is not an alias source either — two parents above the rotated surface code sits "Quantum Tanner code".
- **Only alias what exists here.** An alias for a concept with no circuits behind it (`MWPM`, `lattice surgery`) resolves to nothing.
- **Tool aliases ride in `notes`**, not `aliases`: every circuit from a tool would otherwise match its every alias at `code_name` weight.

Gotchas if you touch this:

- `search_vocab` must stay **unstemmed** (it indexes `search_terms`, not `circuit_search`) or suggestions become stems — porter stores "steane" as "stean".
- `search_terms` must keep covering **codes, tools and papers**, not just circuits: an entity with no circuits appears in no circuit text, so a circuit-only dictionary cannot fix `autqce` → `autqec`. It indexes aliases too, which is what stops a known alias being "corrected" into something else (`msd` → `msb`).
- **A short, repeated column wants a LOW weight, not a high one.** This is the one thing `search-schema.ts` cannot check for you. BM25 normalizes term frequency by field length, so a hit in a ~25-token `paper` already outscores the same hit in long `notes` before any weight applies. `paper` at 3.0 put 140 `non-ft` circuits at the top of "fault tolerant" — matched on their paper's _title_ — above the genuinely FT circuits whose notes say so. It is 1.0 for that reason. The same trap awaits any future short column.
- Adding a column to `circuit_search` means **dropping and recreating** it in a migration — FTS5 has no `ADD COLUMN`. That is cheap here because `create_database.mjs` repopulates the index on every build.
- **Code tags are not circuit tags.** `taggings` keys on `taggable_type`, and `circuit_search.tags` only ever held `'circuit'` rows — so `LDPC`/`topological`/`self-dual` matched nothing until `code_tags` (019). They are kept in separate columns so a name used at both levels cannot double-count its own term frequency.
- Diacritics fold, **`ß` does not**: `remove_diacritics 2` turns `Müller` into `muller`, but `Heußen` indexes as `heußen`, and `Mueller` is not `Müller` either. Both still resolve — via spelling correction, not the tokenizer (`heussen` is 2 edits from `heußen`, `mueller` 1 from `muller`) — so they show the "showing results for" banner. If you ever tighten the edit budget, check these still land.
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
│   ├── papers/            # One YAML per cited paper (e.g. zen-2024-rl-state-prep.yaml)
│   ├── codes/             # One YAML per code (e.g. steane-code.yaml)
│   ├── circuits/          # YAML + body files per circuit (e.g. steane-code--standard-encoding.yaml/.stim)
│   │   └── originals/     # Original (pre-canonicalization) STIM, where one was submitted
│   └── matrices/          # Submitted check matrices, stored once, content-addressed
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
- **No external services** — SQLite only, no hosted DB, no third-party APIs. This governs the
  **site**: every build (`db:create`) and every request reads committed YAML, and both work
  offline. The one exception is `scripts/add_paper.py`, a maintainer tool that fetches paper
  metadata from arXiv/Crossref once and writes YAML you commit — the same shape as
  `annotate_circuits.py`. Nothing at build or request time depends on it. Do not let a fetch
  creep into the build.
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
npm run papers:add -- 2402.17761    # Fetch a paper (arXiv id/DOI/link) into data_yaml/papers/
npm run papers:missing              # Fetch every circuit source that has no paper yet
npm run validate:yaml               # Validate data_yaml/ schemas
npm run validate:circuits           # Validate encoding/state-prep circuits against the code's symplectic h (CSS and non-CSS alike)
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
