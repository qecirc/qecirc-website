/**
 * Build the SQLite database from YAML source files in data_yaml/.
 *
 * Usage: node scripts/db/create_database.mjs
 *
 * Steps:
 *   1. Delete existing DB
 *   2. Run migrations
 *   3. Read YAML files (tools → codes → circuits)
 *   4. Insert into DB
 */

import Database from "better-sqlite3";
import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const root = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../..",
);
const dbPath = path.join(root, "data", "qecirc.db");
const dataDir = path.join(root, "data_yaml");

// --- 1. Delete existing DB ---
for (const suffix of ["", "-wal", "-shm"]) {
  const file = dbPath + suffix;
  if (fs.existsSync(file)) fs.unlinkSync(file);
}
console.log("Database removed.");

// --- 2. Run migrations ---
execSync("node scripts/db/migrate.mjs", { cwd: root, stdio: "inherit" });

// --- 3. Read YAML files ---
const db = new Database(dbPath);
db.pragma("journal_mode = WAL");
db.pragma("foreign_keys = ON");

// Prepared statements
const stmts = {
  insertTool: db.prepare(`
    INSERT INTO tools (name, slug, description, homepage_url, github_url)
    VALUES (?, ?, ?, ?, ?)`),
  insertCode: db.prepare(`
    INSERT INTO codes (name, slug, n, k, d, zoo_url, hx, hz, logical_x, logical_z, canonical_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`),
  insertCircuit: db.prepare(`
    INSERT INTO circuits (code_id, name, slug, description, source, gate_count, depth, qubit_count, crumble_url, quirk_url, tool_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`),
  insertBody: db.prepare(`
    INSERT INTO circuit_bodies (circuit_id, format, body)
    VALUES (?, ?, ?)`),
  insertTag: db.prepare(`INSERT OR IGNORE INTO tags (name) VALUES (?)`),
  getTagId: db.prepare(`SELECT id FROM tags WHERE name = ?`),
  insertTagging: db.prepare(`
    INSERT OR IGNORE INTO taggings (tag_id, taggable_id, taggable_type)
    VALUES (?, ?, ?)`),
};

function addTag(name, taggableId, taggableType) {
  stmts.insertTag.run(name);
  const { id } = stmts.getTagId.get(name);
  stmts.insertTagging.run(id, taggableId, taggableType);
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

// Body format extensions
const BODY_EXTENSIONS = new Set(["stim", "qasm", "cirq"]);

// --- 4. Insert data ---
const toolSlugToId = new Map();
const codeSlugToId = new Map();
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
      );
      toolSlugToId.set(slug, Number(lastInsertRowid));

      for (const tag of data.tags || []) {
        addTag(tag, Number(lastInsertRowid), "tool");
      }

      console.log(`  Tool: ${data.name} (${slug})`);
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
        JSON.stringify(data.hx),
        JSON.stringify(data.hz),
        JSON.stringify(data.logical_x),
        JSON.stringify(data.logical_z),
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
        errors.push(
          `Circuit ${stem}: filename must use '<code-slug>--<circuit-slug>' format`,
        );
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
        errors.push(
          `Circuit ${stem}: code '${codeSlug}' not found in data_yaml/codes/`,
        );
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

      // Resolve tool
      let toolId = null;
      if (data.tool) {
        toolId = toolSlugToId.get(data.tool) ?? null;
        if (toolId == null) {
          errors.push(
            `Circuit ${stem}: tool '${data.tool}' not found in data_yaml/tools/`,
          );
          continue;
        }
      }

      const { lastInsertRowid } = stmts.insertCircuit.run(
        codeId,
        data.name,
        circuitSlug,
        data.description || "",
        data.source || "",
        data.gate_count ?? null,
        data.depth ?? null,
        data.qubit_count ?? null,
        data.crumble_url || null,
        data.quirk_url || null,
        toolId,
      );
      const circuitId = Number(lastInsertRowid);

      // Insert body files
      for (const [ext, bodyPath] of Object.entries(bodies)) {
        const body = fs.readFileSync(bodyPath, "utf-8");
        stmts.insertBody.run(circuitId, ext, body);
      }

      // Tags
      for (const tag of data.tags || []) {
        addTag(tag, circuitId, "circuit");
      }

      const bodyFormats = Object.keys(bodies).join(", ") || "none";
      console.log(
        `  Circuit: ${data.name} (${codeSlug}/${circuitSlug}) [bodies: ${bodyFormats}]`,
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

db.close();
console.log("\nDatabase created successfully.");
