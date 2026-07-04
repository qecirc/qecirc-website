# Tools Section Rework — Design

**Date:** 2026-07-04
**Status:** Approved design, pending implementation

## Goal

Extend the `/tools` section to list circuit-synthesis software tools even if they have
not (yet) contributed circuits to the database, add paper links to tool entries, and
recheck/update the four existing entries. The underlying motive is outreach: the page
should double as an implicit invitation for tool authors to contribute circuits.

## Scope decisions (agreed with maintainer)

- **Strictly software tools** — no papers-without-code, datasets, or benchmarks as entries.
- **Only circuit-producing tools** — tools that create (or could create) circuits of the
  kind stored in the database. QEC frameworks/simulators that merely consume circuits
  (qiskit-qec, CUDA-Q QEC, PECOS, qecsim) are excluded. Stim itself is excluded
  (primarily a simulator).
- **Paper links as a list field** (`paper_urls`), not prose — tools can have multiple
  papers; links must be clickable.
- **No `license` field** — visible on GitHub, only relevant at ingestion time.
- **Two-section page layout** — contributed tools on top, other tools below.
- **One-line contribute CTA** under the second section.

## 1. Schema extension: `paper_urls`

- Tool YAML gains an optional `paper_urls` field: a list of URL strings
  (arXiv/DOI/journal links).
- `scripts/validate-yaml.mjs`: add `paper_urls` to the tools schema as an optional
  list-of-strings field.
- New SQL migration in `data/migrations/`: `ALTER TABLE tools ADD COLUMN paper_urls TEXT`
  (JSON-encoded array, same convention as `codes.h`).
- `scripts/db/create_database.mjs`: write `paper_urls` (JSON-encoded) on insert.
- `src/types/index.ts`: `Tool` gains `paper_urls: string[] | null`; JSON parsing happens
  in the query layer (`src/lib/queries/tools.ts`) so components receive a parsed array.
- **Versioning:** YAML schema change → minor version bump (`0.x.0 → 0.(x+1).0`) in
  `package.json`, `pyproject.toml`, `uv.lock` (`UV_NO_CONFIG=1 uv lock`), and
  `package-lock.json`.

## 2. Data: new and updated tool entries

All facts (URLs, descriptions, paper references) are verified against the live GitHub
repos and papers during implementation — not copied blindly from the outreach research
document.

### New tool YAMLs (6)

| Tool   | Repo                                   | Notes |
| ------ | -------------------------------------- | ----- |
| rlftqc | github.com/remmyzen/rlftqc             | RL-based FT logical state prep; Stim-native; circuits already in `data-imports/rlftqc/` |
| qLDPC  | github.com/qLDPCOrg/qLDPC              | Encoding/SE/memory circuits from code objects; Stim-native |
| QUITS  | github.com/mkangquantum/quits          | SE circuits for HGP/QLP/BPC qLDPC families; Stim-based |
| Rustiq | github.com/smartiel/rustiq             | Clifford/stabilizer synthesis engine (Rust, Qiskit plugin) |
| autqec | github.com/hsayginel/autqec            | Logical Cliffords from code automorphisms |
| Stac   | github.com/abdullahkhalids/stac        | Pedagogical stabilizer-code circuits |

Each entry gets: `name`, `description` (what it produces), `homepage_url` where one
exists, `github_url`, `paper_urls`, and tags following existing conventions
(language tags such as `Python`/`Rust`, task tags such as `state-preparation`,
`syndrome-extraction`, `encoding`).

### Updated existing YAMLs (4)

- **Circuit-Synth** — currently has no URLs at all; research and add
  `github_url`/`homepage_url`/`paper_urls`.
- **CliffordOpt**, **Flag at Origin**, **MQT QECC** — add `paper_urls`, recheck
  descriptions, URLs, and tags.

## 3. UI: two-section /tools page

`src/pages/tools/index.astro` splits the existing single query result (no new query;
`circuit_count` is already returned by `getAllTools`/`filterTools`):

- **Section 1: "Tools contributed to QECirc"** — tools with `circuit_count > 0`,
  sorted by circuit count descending (current behaviour).
- **Section 2: "More circuit-synthesis tools"** — tools with `circuit_count === 0`,
  sorted alphabetically. Their cards show "no circuits yet" instead of "0 circuits".
- Tag filters apply across both sections. A section with no tools hides its heading.
- CTA under section 2: *"Built a tool that generates QEC circuits? We'd love to include
  your circuits — see how to contribute."* linking to `/contribute`.

`src/components/ToolCard.astro`:

- Render paper links alongside Homepage/GitHub: one paper → "Paper ↗"; several →
  "Paper 1 ↗ Paper 2 ↗ …".
- Circuit-count label: `circuit_count === 0` → "no circuits yet".

## 4. Verification

- `npm run validate:yaml`
- `npm run db:create` (rebuild from YAML)
- `npm run lint`, `npm run format:check`
- Visual check of `/tools` in the dev server: both sections render, paper links work,
  tag filtering works across sections, CTA links to `/contribute`.

## Out of scope

- Per-tool detail pages.
- A `license` field.
- Papers, datasets, benchmarks, or simulator frameworks as tool entries.
- Changes to circuit↔tool linking or ingestion scripts.
- Ingesting the `data-imports/rlftqc/` circuits (separate task; once ingested, rlftqc
  moves to section 1 automatically).
