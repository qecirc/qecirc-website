# Tools Section Rework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the tools section with a `paper_urls` field, six new tool entries, corrected existing entries, and a two-section `/tools` page separating contributing tools from other circuit-synthesis tools.

**Architecture:** YAML in `data_yaml/tools/` is the source of truth; a SQLite DB is rebuilt from it (`npm run db:create`). `paper_urls` is stored as a JSON-encoded TEXT column (same convention as `codes.h`), parsed into `string[]` in the query layer so Astro components receive a ready array. The page split is pure presentation logic on the existing query result.

**Tech Stack:** Astro v7 (SSR pages), better-sqlite3, Tailwind CSS, plain Node scripts for validation/DB build. No JS test framework exists in this repo — verification is via `npm run validate:yaml`, `npm run db:create`, `npm run lint`, `npm run format:check`, and a dev-server check (this matches repo convention).

**Spec:** `docs/superpowers/specs/2026-07-04-tools-section-rework-design.md`

**Verified facts (do not re-research):** All URLs/papers below were verified against live repos and arXiv on 2026-07-04. Circuit-Synth has no public repository or paper — its entry intentionally has no links. The current Flag at Origin description is factually wrong (the tool/paper is about FT **state preparation**, not syndrome extraction) and is corrected in Task 6.

---

### Task 1: `paper_urls` schema — validator, migration, DB build, docs

**Files:**
- Modify: `scripts/validate-yaml.mjs` (tools schema ~line 41, `checkType` ~line 54)
- Create: `data/migrations/013_tool_paper_urls.sql`
- Modify: `scripts/db/create_database.mjs` (`insertTool` statement ~line 34, tool insert loop ~line 99)
- Modify: `docs/adding-circuits.md` (tool YAML reference ~line 314)
- Modify: `CLAUDE.md` (tools table in the Database Schema section)

- [ ] **Step 1: Add a failing-check exercise** — add `paper_urls` to one YAML before the schema knows it, to see validation fail:

Temporarily append to `data_yaml/tools/mqt-qecc.yaml`:

```yaml
paper_urls: [https://arxiv.org/abs/2408.11894]
```

Run: `npm run validate:yaml`
Expected: FAIL with `tools/mqt-qecc.yaml: unknown field "paper_urls"` (proves the validator actually checks this; leave the YAML line in place — Task 6 keeps it).

- [ ] **Step 2: Extend the validator**

In `scripts/validate-yaml.mjs`, add to the `tools` schema's `optional` block:

```js
  tools: {
    required: { name: "string" },
    optional: {
      description: "string",
      homepage_url: "string",
      github_url: "string",
      paper_urls: "urls",
      tags: "tags",
    },
  },
```

And add a `urls` type to `checkType` (after the `tags` case):

```js
  if (type === "urls")
    return (
      Array.isArray(value) && value.every((v) => typeof v === "string" && /^https?:\/\//.test(v))
    );
```

Run: `npm run validate:yaml`
Expected: PASS (exit 0, no output about tools).

- [ ] **Step 3: Create the migration**

Create `data/migrations/013_tool_paper_urls.sql`:

```sql
-- Migration: Add paper_urls (JSON-encoded array of paper URLs) to tools

ALTER TABLE tools ADD COLUMN paper_urls TEXT;
```

- [ ] **Step 4: Write the column in the DB build**

In `scripts/db/create_database.mjs`, change the `insertTool` prepared statement:

```js
  insertTool: db.prepare(`
    INSERT INTO tools (name, slug, description, homepage_url, github_url, paper_urls)
    VALUES (?, ?, ?, ?, ?, ?)`),
```

and the tool insert call in the tools loop:

```js
      const { lastInsertRowid } = stmts.insertTool.run(
        data.name,
        slug,
        data.description || "",
        data.homepage_url || null,
        data.github_url || null,
        Array.isArray(data.paper_urls) && data.paper_urls.length > 0
          ? JSON.stringify(data.paper_urls)
          : null,
      );
```

Run: `npm run db:create`
Expected: PASS — output lists all tools/codes/circuits, exit 0. Then check the column landed:

Run: `sqlite3 data/qecirc.db "SELECT slug, paper_urls FROM tools WHERE slug='mqt-qecc'"`
Expected: `mqt-qecc|["https://arxiv.org/abs/2408.11894"]`

- [ ] **Step 5: Update docs**

In `docs/adding-circuits.md`, extend the tool YAML example (~line 316) to:

```yaml
name: MQT QECC
description: Tools for quantum error correcting codes.
homepage_url: https://mqt.readthedocs.io/projects/qecc/en/latest/
github_url: https://github.com/munich-quantum-toolkit/qecc
paper_urls: [https://arxiv.org/abs/2408.11894]
tags: [Python, encoding, state-preparation]
```

In `CLAUDE.md`, Database Schema section, change the tools line to:

```
tools
  id, name, slug, description, homepage_url, github_url, paper_urls, created_at
  -- software tools used to create circuits
  -- paper_urls: JSON-encoded array of associated paper URLs
```

- [ ] **Step 6: Commit**

```bash
git add scripts/validate-yaml.mjs data/migrations/013_tool_paper_urls.sql scripts/db/create_database.mjs docs/adding-circuits.md CLAUDE.md data_yaml/tools/mqt-qecc.yaml
git commit -m "feat(tools): add paper_urls field to tool schema"
```

---

### Task 2: Type + query layer parsing

**Files:**
- Modify: `src/types/index.ts` (`Tool` interface ~line 42)
- Modify: `src/lib/queries/tools.ts`

- [ ] **Step 1: Extend the `Tool` type**

In `src/types/index.ts`:

```ts
export interface Tool {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  homepage_url: string | null;
  github_url: string | null;
  paper_urls: string[] | null;
}
```

- [ ] **Step 2: Parse JSON in the query layer**

In `src/lib/queries/tools.ts`, add a row type + parser near the top (after imports):

```ts
type ToolRow = Omit<Tool, "paper_urls"> & { paper_urls: string | null };

function parseToolRow(row: ToolRow): Tool {
  return { ...row, paper_urls: row.paper_urls ? (JSON.parse(row.paper_urls) as string[]) : null };
}
```

Update the four query functions:

```ts
function enrichTools(rows: ToolRow[]): ToolWithMeta[] {
  return withCircuitCounts(withTags(rows.map(parseToolRow), "tool"), "tool_id");
}

export function getAllTools(): ToolWithMeta[] {
  const db = getDb();
  const tools = db
    .prepare(
      `SELECT t.* FROM tools t
       LEFT JOIN circuits c ON c.tool_id = t.id
       GROUP BY t.id
       ORDER BY COUNT(c.id) DESC, t.name`,
    )
    .all() as ToolRow[];
  return enrichTools(tools);
}

export function getToolById(id: number): Tool | undefined {
  const db = getDb();
  const row = db.prepare("SELECT * FROM tools WHERE id = ?").get(id) as ToolRow | undefined;
  return row ? parseToolRow(row) : undefined;
}
```

In `filterTools`, change the cast and keep `enrichTools`:

```ts
    .all(...params) as ToolRow[];
  return enrichTools(tools);
```

In `getToolsForCircuits`, change the rows cast to `(ToolRow & { circuit_id: number })[]` and the map construction to:

```ts
  for (const row of rows) {
    result.set(row.circuit_id, {
      id: row.id,
      name: row.name,
      slug: row.slug,
      description: row.description,
      homepage_url: row.homepage_url,
      github_url: row.github_url,
      paper_urls: row.paper_urls ? (JSON.parse(row.paper_urls) as string[]) : null,
    });
  }
```

- [ ] **Step 3: Verify types compile and site builds**

Run: `npm run lint`
Expected: PASS (no errors; warnings unrelated to tools are acceptable if pre-existing).

Run: `npm run build`
Expected: PASS (astro build completes; this type-checks the .astro/.ts files that consume `Tool`).

- [ ] **Step 4: Commit**

```bash
git add src/types/index.ts src/lib/queries/tools.ts
git commit -m "feat(tools): parse paper_urls into Tool objects in query layer"
```

---

### Task 3: ToolCard — paper links and "no circuits yet"

**Files:**
- Modify: `src/components/ToolCard.astro`

- [ ] **Step 1: Update the circuit-count label**

Replace the count `<span>` (lines 16–18) with:

```astro
    <span class="text-xs text-gray-400 dark:text-gray-500">
      {tool.circuit_count === 0
        ? "no circuits yet"
        : `${tool.circuit_count} circuit${tool.circuit_count !== 1 ? "s" : ""}`}
    </span>
```

- [ ] **Step 2: Render paper links**

In the links `<div>` at the bottom, after the GitHub link block, add:

```astro
    {(tool.paper_urls ?? []).map((url, i) => (
      <a href={url} class="underline text-gray-500 hover:text-gray-900 dark:hover:text-gray-100" target="_blank" rel="noopener">
        {(tool.paper_urls ?? []).length > 1 ? `Paper ${i + 1}` : "Paper"} &#x2197;
      </a>
    ))}
```

- [ ] **Step 3: Verify in dev server**

Run: `npm run db:create && npm run dev` (background) and open `http://localhost:4321/tools`.
Expected: MQT QECC card shows a "Paper ↗" link (from the YAML line added in Task 1); CliffordOpt and Flag at Origin cards show "no circuits yet" instead of "0 circuits".

- [ ] **Step 4: Commit**

```bash
git add src/components/ToolCard.astro
git commit -m "feat(tools): show paper links and friendlier zero-circuit label on tool cards"
```

---

### Task 4: Two-section /tools page with contribute CTA

**Files:**
- Modify: `src/pages/tools/index.astro`

- [ ] **Step 1: Split the tool list**

In the frontmatter, after `const tools = ...`, add:

```ts
const contributed = tools.filter((t) => t.circuit_count > 0);
const others = tools
  .filter((t) => t.circuit_count === 0)
  .sort((a, b) => a.name.localeCompare(b.name));
```

- [ ] **Step 2: Render two sections + CTA**

Replace the existing `{tools.length === 0 ? ... : <div class="grid gap-3">...</div>}` block with:

```astro
  {tools.length === 0 ? (
    <div class="text-center py-8">
      <p class="text-gray-500 dark:text-gray-400 mb-2">No tools match your filters.</p>
      <a href="/tools" class="text-sm underline text-gray-500 hover:text-gray-900 dark:hover:text-gray-100">Clear filters</a>
    </div>
  ) : (
    <>
      {contributed.length > 0 && (
        <section class="mb-8">
          <h2 class="text-lg font-semibold mb-3">Tools contributed to QECirc</h2>
          <div class="grid gap-3">
            {contributed.map((tool) => (
              <ToolCard tool={tool} baseUrl={Astro.url} />
            ))}
          </div>
        </section>
      )}
      {others.length > 0 && (
        <section>
          <h2 class="text-lg font-semibold mb-3">More circuit-synthesis tools</h2>
          <div class="grid gap-3">
            {others.map((tool) => (
              <ToolCard tool={tool} baseUrl={Astro.url} />
            ))}
          </div>
        </section>
      )}
    </>
  )}

  <p class="mt-8 text-sm text-gray-500 dark:text-gray-400">
    Built a tool that generates QEC circuits? We'd love to include your circuits —
    <a href="/contribute" class="underline hover:text-gray-900 dark:hover:text-gray-100">see how to contribute</a>.
  </p>
```

- [ ] **Step 3: Verify in dev server**

Open `http://localhost:4321/tools`.
Expected: "Tools contributed to QECirc" lists Circuit-Synth (112) and MQT QECC (37); "More circuit-synthesis tools" lists CliffordOpt and Flag at Origin alphabetically; CTA line at the bottom links to `/contribute`.

Open `http://localhost:4321/tools?tag=Clifford`.
Expected: only matching tools shown, sections with no matches hide their headings; empty-state message when a bogus tag (`?tag=nope`) yields nothing.

- [ ] **Step 4: Commit**

```bash
git add src/pages/tools/index.astro
git commit -m "feat(tools): split tools page into contributed and other tools, add contribute CTA"
```

---

### Task 5: Update existing tool YAMLs (verified facts)

**Files:**
- Modify: `data_yaml/tools/circuit-synth.yaml`
- Modify: `data_yaml/tools/cliffordopt.yaml`
- Modify: `data_yaml/tools/flag-at-origin.yaml`
- Modify: `data_yaml/tools/mqt-qecc.yaml`

- [ ] **Step 1: circuit-synth.yaml** — no public repository or paper exists, so it keeps no links; description unchanged:

```yaml
name: Circuit-Synth
description: Clifford and CNOT circuit synthesis via greedy elimination with rollout search, minimizing two-qubit gate count or depth.
tags: [Python, Rust, encoding, state-preparation]
```

(No change unless the file differs from the above — verify with `cat`.)

- [ ] **Step 2: cliffordopt.yaml** — add paper, sharpen description:

```yaml
name: CliffordOpt
description: Heuristic and optimal synthesis of CNOT and Clifford circuits from parity-check or symplectic matrices, minimizing two-qubit gate count or circuit depth.
github_url: https://github.com/m-webster/CliffordOpt
paper_urls: [https://arxiv.org/abs/2503.14660]
tags: [Python, optimization, Clifford, encoding]
```

- [ ] **Step 3: flag-at-origin.yaml** — **correct the description** (the paper is about FT state preparation, not syndrome extraction) and retag:

```yaml
name: Flag at Origin
description: Code and circuits for modular fault-tolerant state preparation of CSS codes using flag gadgets, with results on Quantinuum H2-1.
github_url: https://github.com/Quantinuum/flag_at_origin_paper
paper_urls: [https://arxiv.org/abs/2508.14200]
tags: [Python, fault-tolerant, state-preparation, flag]
```

- [ ] **Step 4: mqt-qecc.yaml** — add the three circuit-synthesis papers, extend description:

```yaml
name: MQT QECC
description: Tools for quantum error correcting codes, including automated synthesis of fault-tolerant state-preparation and encoding circuits; part of the Munich Quantum Toolkit.
homepage_url: https://mqt.readthedocs.io/projects/qecc/en/latest/
github_url: https://github.com/munich-quantum-toolkit/qecc
paper_urls:
  [
    https://arxiv.org/abs/2408.11894,
    https://arxiv.org/abs/2501.05527,
    https://arxiv.org/abs/2605.15266,
  ]
tags: [Python, encoding, state-preparation]
```

- [ ] **Step 5: Validate and rebuild**

Run: `npm run validate:yaml && npm run db:create`
Expected: both PASS; DB build lists all 4 tools.

- [ ] **Step 6: Commit**

```bash
git add data_yaml/tools/
git commit -m "fix(tools): correct flag-at-origin description, add verified paper links to existing tools"
```

---

### Task 6: Add six new tool YAMLs (verified facts)

**Files:**
- Create: `data_yaml/tools/rlftqc.yaml`
- Create: `data_yaml/tools/qldpc.yaml`
- Create: `data_yaml/tools/quits.yaml`
- Create: `data_yaml/tools/rustiq.yaml`
- Create: `data_yaml/tools/autqec.yaml`
- Create: `data_yaml/tools/stac.yaml`

- [ ] **Step 1: rlftqc.yaml**

```yaml
name: rlftqc
description: Reinforcement-learning discovery of fault-tolerant logical state preparation circuits for stabilizer codes, with customizable gate sets and qubit connectivity, producing Stim circuits.
homepage_url: https://remmyzen.github.io/rlftqc/
github_url: https://github.com/remmyzen/rlftqc
paper_urls: [https://arxiv.org/abs/2402.17761]
tags: [Python, state-preparation, fault-tolerant, reinforcement-learning]
```

- [ ] **Step 2: qldpc.yaml**

```yaml
name: qLDPC
description: Library for constructing qLDPC, stabilizer, and subsystem codes that generates Stim circuits for encoding, memory experiments, and SWAP-transversal logical Clifford gates.
homepage_url: https://qldpc.readthedocs.io/
github_url: https://github.com/qLDPCOrg/qLDPC
tags: [Python, encoding, syndrome-extraction, qLDPC]
```

(No `paper_urls` — verified: no standalone paper exists; the recommended citation is the repo.)

- [ ] **Step 3: quits.yaml**

```yaml
name: QUITS
description: Modular circuit-level simulator for qLDPC codes that constructs Stim syndrome-extraction circuits for hypergraph-product, lifted-product, balanced-product, and bivariate-bicycle codes.
github_url: https://github.com/mkangquantum/quits
paper_urls: [https://arxiv.org/abs/2504.02673]
tags: [Python, syndrome-extraction, qLDPC]
```

- [ ] **Step 4: rustiq.yaml**

```yaml
name: Rustiq
description: Rust-based synthesis engine for Clifford operators and isometries, stabilizer and graph states, and Pauli networks, producing gate-count- or depth-optimized circuits such as encoders from stabilizers.
github_url: https://github.com/qiskit-community/rustiq
paper_urls: [https://arxiv.org/abs/2212.06928, https://arxiv.org/abs/2404.03280]
tags: [Rust, Python, encoding, state-preparation, Clifford]
```

- [ ] **Step 5: autqec.yaml**

```yaml
name: autqec
description: Finds fault-tolerant logical Clifford gates of stabilizer codes from code automorphisms and converts them to physical Clifford circuits.
github_url: https://github.com/hsayginel/autqec
paper_urls: [https://arxiv.org/abs/2409.18175]
tags: [Python, logical-gates, Clifford, fault-tolerant]
```

- [ ] **Step 6: stac.yaml**

```yaml
name: Stac
description: Pedagogical library for constructing stabilizer codes that generates encoding, decoding, and syndrome-measurement circuits with export to QASM and Stim.
homepage_url: https://abdullahkhalid.com/qecft/
github_url: https://github.com/abdullahkhalids/stac
tags: [Python, encoding, syndrome-extraction]
```

(No `paper_urls` — verified: no standalone paper; the homepage is the author's companion book.)

- [ ] **Step 7: Validate, rebuild, visual check**

Run: `npm run validate:yaml && npm run db:create`
Expected: PASS; build output lists 10 tools.

Open `http://localhost:4321/tools` (restart dev server — it caches the DB connection).
Expected: section 2 now lists autqec, CliffordOpt, Flag at Origin, qLDPC, QUITS, rlftqc, Rustiq, Stac alphabetically, each with working links; paper links open arXiv pages.

- [ ] **Step 8: Commit**

```bash
git add data_yaml/tools/
git commit -m "feat(tools): add rlftqc, qLDPC, QUITS, Rustiq, autqec, and Stac tool entries"
```

---

### Task 7: Version bump and final verification

**Files:**
- Modify: `package.json` (version 0.3.2 → 0.4.0)
- Modify: `pyproject.toml` (version 0.3.2 → 0.4.0)
- Modify: `uv.lock`, `package-lock.json` (regenerated)

- [ ] **Step 1: Bump versions**

In `package.json`: `"version": "0.4.0",`
In `pyproject.toml`: `version = "0.4.0"`

- [ ] **Step 2: Regenerate lockfiles**

```bash
UV_NO_CONFIG=1 uv lock
npm install
```

Expected: `uv.lock` and (possibly) `package-lock.json` updated. **Never** let private-registry URLs into the lockfiles — `UV_NO_CONFIG=1` is required.

- [ ] **Step 3: Full verification suite**

```bash
npm run validate:yaml && npm run db:create && npm run lint && npm run format:check && npm run build
```

Expected: all PASS. If `format:check` fails, run `npm run format` and re-check.

- [ ] **Step 4: Commit**

```bash
git add package.json pyproject.toml uv.lock package-lock.json
git commit -m "chore(release): bump version to 0.4.0 for tool paper_urls schema change"
```

---

## Final state checklist (maps to spec)

- `paper_urls` in validator, migration 013, DB build, `Tool` type, query parsing — Tasks 1–2
- ToolCard paper links + "no circuits yet" — Task 3
- Two-section page ("Tools contributed to QECirc" / "More circuit-synthesis tools") + CTA — Task 4
- 4 existing entries rechecked/updated (incl. flag-at-origin correction; circuit-synth stays URL-less because the repo is internal) — Task 5
- 6 new entries with verified facts — Task 6
- Docs (adding-circuits.md, CLAUDE.md) — Task 1
- Minor version bump — Task 7
