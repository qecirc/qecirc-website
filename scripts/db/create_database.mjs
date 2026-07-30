/**
 * Build the SQLite database from YAML source files in data_yaml/.
 *
 * Usage: node scripts/db/create_database.mjs
 *
 * Steps:
 *   1. Delete existing DB
 *   2. Run migrations
 *   3. Read YAML files (tools → papers → codes → circuits)
 *   4. Insert into DB
 */

import Database from "better-sqlite3";
import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import * as yaml from "js-yaml";
import { paperKey, paperLinks, isPaperSource } from "../paper-links.mjs";
import { decodeMatrix } from "../matrix-format.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const dbPath = path.join(root, "data", "qecirc.db");
const dataDir = path.join(root, "data_yaml");

// --- 1. Reset DB (delete + migrate) ---
execSync("node scripts/db/reset.mjs", { cwd: root, stdio: "inherit" });

// --- 3. Read YAML files ---
const db = new Database(dbPath);
db.pragma("journal_mode = WAL");
db.pragma("foreign_keys = ON");

// Prepared statements
const stmts = {
  insertTool: db.prepare(`
    INSERT INTO tools (name, slug, description, homepage_url, github_url, paper_urls, aliases)
    VALUES (?, ?, ?, ?, ?, ?, ?)`),
  insertPaper: db.prepare(`
    INSERT INTO papers (slug, title, authors, year, arxiv_id, doi, journal_ref, url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)`),
  insertCode: db.prepare(`
    INSERT INTO codes (name, slug, n, k, d, zoo_url, aliases, related, h, logical, canonical_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`),
  insertCircuit: db.prepare(`
    INSERT INTO circuits (qec_id, code_id, name, slug, notes, source, gate_count, two_qubit_gate_count, depth, qubit_count, weight, crumble_url, crumble_url_annotated, quirk_url, tool_id, paper_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`),
  insertBody: db.prepare(`
    INSERT INTO circuit_bodies (circuit_id, format, body)
    VALUES (?, ?, ?)`),
  insertOriginal: db.prepare(`
    INSERT INTO circuit_originals (circuit_id, original_stim, original_h, original_logical)
    VALUES (?, ?, ?, ?)`),
  insertTag: db.prepare(`INSERT OR IGNORE INTO tags (name) VALUES (?)`),
  getTagId: db.prepare(`SELECT id FROM tags WHERE name = ?`),
  insertTagging: db.prepare(`
    INSERT OR IGNORE INTO taggings (tag_id, taggable_id, taggable_type)
    VALUES (?, ?, ?)`),
};

/** Alias lists collapse to one space-joined string per entity.
 *
 * Stored verbatim, hyphens and all: FTS5's unicode61 splits "Reed-Muller" into
 * `reed`+`muller`, so both "reed muller" and "reed-muller" match it, while the
 * quick-search's LIKE is substring-based and matches either way too. Folding the
 * hyphens out would only break the LIKE path for a user who types one.
 */
function joinAliases(list) {
  const text = (list || []).join(" ").trim();
  return text === "" ? null : text;
}

function addTag(name, taggableId, taggableType) {
  stmts.insertTag.run(name);
  const { id } = stmts.getTagId.get(name);
  stmts.insertTagging.run(id, taggableId, taggableType);
}

/**
 * A shared matrix file, by the content address a circuit refers to. Missing is
 * an error rather than a silent skip: the circuit says it has originals, and
 * publishing it without them would quietly lose the provenance they exist for.
 */
function readMatrices(dir, digest, stem) {
  const file = path.join(dir, "matrices", `${digest}.yaml`);
  if (!fs.existsSync(file)) {
    throw new Error(`Circuit ${stem} references matrices ${digest}, which does not exist`);
  }
  return readYaml(file);
}

function readYaml(filePath) {
  return yaml.load(fs.readFileSync(filePath, "utf-8"));
}

function listYamlFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".yaml"))
    .sort();
}

// Body format extensions. `stim-annotated` is the canonical STIM body plus a
// reset prologue, a terminal readout and derived detectors/observables; the
// canonical `stim` body stays unitary because the derive/fit pipeline needs it.
const BODY_EXTENSIONS = new Set(["stim", "qasm", "cirq", "stim-annotated"]);

// --- 4. Insert data ---
const toolSlugToId = new Map();
const codeSlugToId = new Map();
/** paperKey(link) → papers.id, for every link a paper answers to. */
const paperKeyToId = new Map();
/** Link-shaped circuit sources that matched no paper → how many circuits. Not
 *  fatal; reported after the build as a nudge to add the missing paper. */
const unmatchedSources = new Map();
const errors = [];

try {
  db.transaction(() => {
    // --- Tools ---
    const toolsDir = path.join(dataDir, "tools");
    for (const file of listYamlFiles(toolsDir)) {
      const slug = file.replace(/\.yaml$/, "");
      const data = readYaml(path.join(toolsDir, file));

      if (!data.name) {
        errors.push(`Tool ${file}: missing required field 'name'`);
        continue;
      }
      if (toolSlugToId.has(slug)) {
        errors.push(`Tool ${file}: duplicate slug '${slug}'`);
        continue;
      }

      const { lastInsertRowid } = stmts.insertTool.run(
        data.name,
        slug,
        data.description || "",
        data.homepage_url || null,
        data.github_url || null,
        Array.isArray(data.paper_urls) && data.paper_urls.length > 0
          ? JSON.stringify(data.paper_urls)
          : null,
        joinAliases(data.aliases),
      );
      toolSlugToId.set(slug, Number(lastInsertRowid));

      for (const tag of data.tags || []) {
        addTag(tag, Number(lastInsertRowid), "tool");
      }

      console.log(`  Tool: ${data.name} (${slug})`);
    }

    // --- Papers ---
    const papersDir = path.join(dataDir, "papers");
    for (const file of listYamlFiles(papersDir)) {
      const slug = file.replace(/\.yaml$/, "");
      const data = readYaml(path.join(papersDir, file));

      if (!data.title) {
        errors.push(`Paper ${file}: missing required field 'title'`);
        continue;
      }
      if (!Array.isArray(data.authors) || data.authors.length === 0) {
        errors.push(`Paper ${file}: 'authors' must be a non-empty list`);
        continue;
      }
      if (!data.url) {
        errors.push(`Paper ${file}: missing required field 'url'`);
        continue;
      }

      const { lastInsertRowid } = stmts.insertPaper.run(
        slug,
        data.title,
        JSON.stringify(data.authors),
        data.year ?? null,
        data.arxiv_id ? String(data.arxiv_id) : null,
        data.doi || null,
        data.journal_ref || null,
        data.url,
      );
      const paperId = Number(lastInsertRowid);

      for (const link of paperLinks(data)) {
        const key = paperKey(link);
        const claimed = paperKeyToId.get(key);
        if (claimed != null && claimed !== paperId) {
          errors.push(`Paper ${file}: link '${link}' is already claimed by another paper`);
          continue;
        }
        paperKeyToId.set(key, paperId);
      }

      console.log(`  Paper: ${data.title} (${slug})`);
    }

    // --- Codes ---
    const codesDir = path.join(dataDir, "codes");
    for (const file of listYamlFiles(codesDir)) {
      const slug = file.replace(/\.yaml$/, "");
      const data = readYaml(path.join(codesDir, file));

      if (!data.name) {
        errors.push(`Code ${file}: missing required field 'name'`);
        continue;
      }
      if (data.n == null || data.k == null) {
        errors.push(`Code ${file}: missing required fields 'n' and/or 'k'`);
        continue;
      }
      if (codeSlugToId.has(slug)) {
        errors.push(`Code ${file}: duplicate slug '${slug}'`);
        continue;
      }

      const { lastInsertRowid } = stmts.insertCode.run(
        data.name,
        slug,
        data.n,
        data.k,
        data.d || null,
        data.zoo_url || null,
        joinAliases(data.aliases),
        joinAliases(data.related),
        data.h == null ? null : JSON.stringify(decodeMatrix(data.h)),
        data.logical == null ? null : JSON.stringify(decodeMatrix(data.logical)),
        data.canonical_hash || null,
      );
      codeSlugToId.set(slug, Number(lastInsertRowid));

      for (const tag of data.tags || []) {
        addTag(tag, Number(lastInsertRowid), "code");
      }

      console.log(`  Code: ${data.name} (${slug})`);
    }

    // --- Circuits ---
    const circuitsDir = path.join(dataDir, "circuits");
    if (!fs.existsSync(circuitsDir)) return;

    // Group files by stem
    const circuitFiles = fs.readdirSync(circuitsDir).sort();
    const circuitStems = new Map(); // stem -> { yaml: path, bodies: { ext: path } }

    for (const file of circuitFiles) {
      const ext = path.extname(file).slice(1); // remove leading dot
      const stem = file.replace(/\.[^.]+$/, "");

      if (!circuitStems.has(stem)) {
        circuitStems.set(stem, { yaml: null, bodies: {} });
      }
      const entry = circuitStems.get(stem);

      if (ext === "yaml") {
        entry.yaml = path.join(circuitsDir, file);
      } else if (BODY_EXTENSIONS.has(ext)) {
        entry.bodies[ext] = path.join(circuitsDir, file);
      }
    }

    for (const [stem, { yaml: yamlPath, bodies }] of circuitStems) {
      if (!yamlPath) continue; // body file without yaml — skip

      // Parse code-slug and circuit-slug from stem
      const sepIdx = stem.indexOf("--");
      if (sepIdx === -1) {
        errors.push(`Circuit ${stem}: filename must use '<code-slug>--<circuit-slug>' format`);
        continue;
      }
      const codeSlug = stem.slice(0, sepIdx);
      const circuitSlug = stem.slice(sepIdx + 2);

      if (!codeSlug || !circuitSlug) {
        errors.push(`Circuit ${stem}: empty code or circuit slug`);
        continue;
      }

      const codeId = codeSlugToId.get(codeSlug);
      if (codeId == null) {
        errors.push(`Circuit ${stem}: code '${codeSlug}' not found in data_yaml/codes/`);
        continue;
      }

      const data = readYaml(yamlPath);

      if (!data.name) {
        errors.push(`Circuit ${stem}: missing required field 'name'`);
        continue;
      }
      if (!data.source) {
        errors.push(`Circuit ${stem}: missing required field 'source'`);
        continue;
      }
      if (data.qec_id == null || !Number.isInteger(data.qec_id) || data.qec_id < 1) {
        errors.push(`Circuit ${stem}: missing or invalid 'qec_id' (must be a positive integer)`);
        continue;
      }

      // Resolve tool
      let toolId = null;
      if (data.tool) {
        toolId = toolSlugToId.get(data.tool) ?? null;
        if (toolId == null) {
          errors.push(`Circuit ${stem}: tool '${data.tool}' not found in data_yaml/tools/`);
          continue;
        }
      }

      // Resolve paper from `source`. Only link-shaped sources are candidates:
      // the rest name a tool ("circuit-synth"), which is provenance but not a
      // paper. A link that matches no paper is NOT an error -- papers are
      // optional enrichment, and a circuit may cite a work we hold no record of
      // -- so the circuit keeps its bare `source` and is reported at the end.
      const source = data.source || "";
      let paperId = null;
      if (isPaperSource(source)) {
        paperId = paperKeyToId.get(paperKey(source)) ?? null;
        if (paperId == null) unmatchedSources.set(source, (unmatchedSources.get(source) ?? 0) + 1);
      }

      const { lastInsertRowid } = stmts.insertCircuit.run(
        data.qec_id,
        codeId,
        data.name,
        circuitSlug,
        data.notes || null,
        source,
        data.gate_count ?? null,
        data.two_qubit_gate_count ?? null,
        data.depth ?? null,
        data.qubit_count ?? null,
        data.weight ?? null,
        data.crumble_url || null,
        data.crumble_url_annotated || null,
        data.quirk_url || null,
        toolId,
        paperId,
      );
      const circuitId = Number(lastInsertRowid);

      // Insert body files
      for (const [ext, bodyPath] of Object.entries(bodies)) {
        const body = fs.readFileSync(bodyPath, "utf-8");
        stmts.insertBody.run(circuitId, ext, body);
      }

      // Original files (pre-canonicalization data).
      //
      // The original circuit sits beside the circuit; the original matrices are
      // shared — every circuit of one code was submitted against the same ones —
      // so they live once under data_yaml/matrices/ and the circuit names the
      // one it uses. Resolved and inlined here, so the database and everything
      // downstream of it see exactly what they saw before.
      const originalsDir = path.join(circuitsDir, "originals");
      const origStimPath = path.join(originalsDir, `${stem}.original.stim`);
      if (fs.existsSync(origStimPath)) {
        const origStim = fs.readFileSync(origStimPath, "utf-8");
        // A branch written before this format still carries the matrices in a
        // per-circuit `<stem>.original.yaml`. Merging it produces no conflict —
        // the file simply reappears — and without this the build would read no
        // reference, store null matrices and say nothing. Run
        // `scripts/migrate_matrix_storage.py --write`.
        const legacyPath = path.join(originalsDir, `${stem}.original.yaml`);
        if (!data.original_matrices && fs.existsSync(legacyPath)) {
          throw new Error(
            `Circuit ${stem} has ${stem}.original.yaml but no 'original_matrices' reference. ` +
              `Run: uv run python scripts/migrate_matrix_storage.py --write`,
          );
        }
        const origData = data.original_matrices
          ? readMatrices(dataDir, data.original_matrices, stem)
          : {};
        stmts.insertOriginal.run(
          circuitId,
          origStim,
          origData.h == null ? null : JSON.stringify(decodeMatrix(origData.h)),
          origData.logical == null ? null : JSON.stringify(decodeMatrix(origData.logical)),
        );
      }

      // Tags
      for (const tag of data.tags || []) {
        addTag(tag, circuitId, "circuit");
      }
      // Derived tag: every circuit with a tool is tagged `tool:<slug>` so it is
      // filterable in the Tools category (e.g. all MQT QECC circuits at once).
      // The `tool` field is the single source of truth — the tag is derived here
      // rather than stored in YAML, so it stays in sync with tool_id by
      // construction and applies to every current and future circuit.
      if (data.tool) {
        addTag(`tool:${data.tool}`, circuitId, "circuit");
      }

      const bodyFormats = Object.keys(bodies).join(", ") || "none";
      const hasOriginals = fs.existsSync(origStimPath);
      console.log(
        `  Circuit: ${data.name} (${codeSlug}/${circuitSlug}) [bodies: ${bodyFormats}]${hasOriginals ? " [originals]" : ""}`,
      );
    }

    // Abort transaction if there were validation errors
    if (errors.length > 0) {
      throw new Error("validation_errors");
    }
  })();
} catch (e) {
  if (e.message === "validation_errors") {
    console.error("\nValidation errors:");
    for (const err of errors) console.error(`  - ${err}`);
    db.close();
    process.exit(1);
  }
  throw e;
}

// --- 4. Populate the full-text search index (migrations 016 → 019) ---
// Derived entirely from the rows just inserted, so it is rebuilt from scratch
// here rather than maintained by triggers. `source` rides along in the notes
// column: it is provenance prose (DOI/citation) and shares its low weight.
//
// A circuit inherits its code's aliases and related names (migration 017), which
// is what lets "laflamme" or "bb codes" reach circuits whose own text says
// neither. Tool aliases ride in `notes`: they are weak evidence about a circuit
// (every circuit from a tool would otherwise match its every alias equally) and
// `notes` is the low-weight column for exactly that kind of term.
//
// `code_tags` (migration 019) carries the tags of the code the circuit belongs
// to. Without it `LDPC`, `topological` and `self-dual` -- all code-level tags --
// matched no circuit at all. Kept apart from `tags` so the two can be weighted
// separately and so a name used at both levels cannot double-count.
//
// `paper` (migration 018) carries the paper's title, authors and ids, which is
// the only place that text exists -- `source` is a bare link. json_each flattens
// papers.authors (a JSON array) back into words so an author surname is a term.
// The arXiv id is indexed as written: unicode61 splits "2402.17761" into "2402"
// and "17761", so both halves stay searchable.
const SEARCH_TEXT = `
  SELECT c.id AS circuit_id, c.name AS name, co.name AS code_name,
         COALESCE(co.aliases, '') AS aliases,
         COALESCE(co.related, '') AS related,
         COALESCE((SELECT group_concat(t.name, ' ')
                   FROM taggings tg JOIN tags t ON t.id = tg.tag_id
                   WHERE tg.taggable_id = c.id AND tg.taggable_type = 'circuit'), '') AS tags,
         COALESCE((SELECT group_concat(t.name, ' ')
                   FROM taggings tg JOIN tags t ON t.id = tg.tag_id
                   WHERE tg.taggable_id = co.id AND tg.taggable_type = 'code'), '') AS code_tags,
         COALESCE((SELECT TRIM(p.title || ' ' ||
                          COALESCE((SELECT group_concat(a.value, ' ')
                                    FROM json_each(p.authors) a), '') || ' ' ||
                          COALESCE(p.arxiv_id, '') || ' ' ||
                          COALESCE(p.doi, '') || ' ' ||
                          COALESCE(p.journal_ref, '') || ' ' ||
                          COALESCE(CAST(p.year AS TEXT), ''))
                   FROM papers p WHERE p.id = c.paper_id), '') AS paper,
         TRIM(COALESCE(c.notes, '') || ' ' || COALESCE(c.source, '') || ' '
              || COALESCE((SELECT tl.aliases FROM tools tl WHERE tl.id = c.tool_id), '')) AS notes
  FROM circuits c JOIN codes co ON co.id = c.code_id`;

const indexed = db
  .prepare(
    `INSERT INTO circuit_search (circuit_id, name, code_name, aliases, related, tags, code_tags, paper, notes)
     SELECT circuit_id, name, code_name, aliases, related, tags, code_tags, paper, notes
     FROM (${SEARCH_TEXT})`,
  )
  .run();

// The unstemmed spelling dictionary (see migration 015). Covers every entity,
// not just circuits: it also backs the header quick-search, which looks up codes
// and tools. A tool that has contributed no circuits appears in no circuit text,
// so without these rows its name could never be offered as a correction.
const TAGS_OF = (type) => `
  COALESCE((SELECT group_concat(t.name, ' ')
            FROM taggings tg JOIN tags t ON t.id = tg.tag_id
            WHERE tg.taggable_id = e.id AND tg.taggable_type = '${type}'), '')`;

// Aliases are indexed here too, so the dictionary learns their vocabulary and
// "bivarient bicycle" or "laflame" correct like any other term. This also stops
// an alias being "corrected" into something else: correctTokens only rewrites a
// token that matches NOTHING, so a known alias is now left alone -- which is
// what fixes `msd` silently becoming `msb`.
db.prepare(
  `INSERT INTO search_terms (text)
   SELECT name || ' ' || code_name || ' ' || aliases || ' ' || related || ' '
          || tags || ' ' || code_tags || ' ' || paper || ' ' || notes
   FROM (${SEARCH_TEXT})`,
).run();
db.prepare(
  `INSERT INTO search_terms (text)
   SELECT e.name || ' ' || COALESCE(e.aliases, '') || ' ' || COALESCE(e.related, '')
          || ' ' || ${TAGS_OF("code")} FROM codes e`,
).run();
db.prepare(
  `INSERT INTO search_terms (text)
   SELECT e.name || ' ' || COALESCE(e.aliases, '') || ' ' || ${TAGS_OF("tool")} FROM tools e`,
).run();
// Papers get their own rows for the same reason tools do: a paper whose circuits
// are not yet in the library appears in no circuit text, so a dictionary built
// from circuits alone could never offer "Colmenarez" as a correction for
// "Colmenraez". Title and authors only -- ids and years are digit tokens, which
// correctTokens refuses to correct anyway (see queries/spelling.ts).
db.prepare(
  `INSERT INTO search_terms (text)
   SELECT p.title || ' ' ||
          COALESCE((SELECT group_concat(a.value, ' ') FROM json_each(p.authors) a), '')
   FROM papers p`,
).run();

const vocabSize = db.prepare("SELECT COUNT(*) AS n FROM search_vocab").get().n;
const linked = db.prepare("SELECT COUNT(*) AS n FROM circuits WHERE paper_id IS NOT NULL").get().n;
const paperCount = db.prepare("SELECT COUNT(*) AS n FROM papers").get().n;

db.close();
console.log(`\nSearch index: ${indexed.changes} circuits, ${vocabSize} dictionary terms.`);
console.log(`Papers: ${paperCount}, linked to ${linked} circuits.`);

// A link-shaped source with no paper behind it is the one way this feature
// quietly under-delivers: the circuit still renders and still searches, it just
// has no title or authors to find it by. Say so rather than let it pass.
if (unmatchedSources.size > 0) {
  console.log(`\nSources with no paper in data_yaml/papers/ (searchable by URL only):`);
  for (const [source, count] of [...unmatchedSources].sort((a, b) => b[1] - a[1])) {
    console.log(`  - ${source} (${count} circuit${count === 1 ? "" : "s"})`);
  }
}

console.log("\nDatabase created successfully.");
