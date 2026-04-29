import Database from "better-sqlite3";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const dbPath = path.join(root, "data", "qecirc.db");

const args = process.argv.slice(2);
const circuitsOnly = args.includes("--circuits-only");
const toolsOnly = args.includes("--tools-only");
const confirmed = args.includes("--yes");

const db = new Database(dbPath);
db.pragma("foreign_keys = ON");

function count(table) {
  return db.prepare(`SELECT COUNT(*) as n FROM ${table}`).get().n;
}

if (toolsOnly) {
  const nTools = count("tools");
  const nTaggings = db
    .prepare("SELECT COUNT(*) as n FROM taggings WHERE taggable_type = 'tool'")
    .get().n;
  const nLinked = db
    .prepare("SELECT COUNT(*) as n FROM circuits WHERE tool_id IS NOT NULL")
    .get().n;

  if (!confirmed) {
    console.log("Would delete:");
    console.log(`  ${nTools} tool(s)`);
    console.log(`  ${nTaggings} tool tagging(s)`);
    console.log(`  ${nLinked} circuit(s) would have tool_id set to NULL`);
    console.log("\nRun with --yes to confirm.");
    process.exit(0);
  }

  db.transaction(() => {
    db.prepare("UPDATE circuits SET tool_id = NULL WHERE tool_id IS NOT NULL").run();
    db.prepare("DELETE FROM taggings WHERE taggable_type = 'tool'").run();
    db.prepare("DELETE FROM tools").run();
    db.prepare("DELETE FROM tags WHERE id NOT IN (SELECT DISTINCT tag_id FROM taggings)").run();
  })();

  console.log(
    `Cleared ${nTools} tool(s), ${nTaggings} tagging(s), unlinked ${nLinked} circuit(s).`,
  );
} else if (circuitsOnly) {
  const nCircuits = count("circuits");
  const nBodies = count("circuit_bodies");
  const nTaggings = db
    .prepare("SELECT COUNT(*) as n FROM taggings WHERE taggable_type = 'circuit'")
    .get().n;

  if (!confirmed) {
    console.log("Would delete:");
    console.log(`  ${nCircuits} circuit(s)`);
    console.log(`  ${nBodies} circuit body/bodies`);
    console.log(`  ${nTaggings} circuit tagging(s)`);
    console.log("\nCodes and tools are preserved.");
    console.log("\nRun with --yes to confirm.");
    process.exit(0);
  }

  db.transaction(() => {
    db.prepare("DELETE FROM taggings WHERE taggable_type = 'circuit'").run();
    db.prepare("DELETE FROM circuits").run(); // cascades to circuit_bodies
    db.prepare("DELETE FROM tags WHERE id NOT IN (SELECT DISTINCT tag_id FROM taggings)").run();
  })();

  console.log(`Cleared ${nCircuits} circuit(s), ${nBodies} body/bodies, ${nTaggings} tagging(s).`);
} else {
  const nCodes = count("codes");
  const nCircuits = count("circuits");
  const nBodies = count("circuit_bodies");
  const nTaggings = db
    .prepare("SELECT COUNT(*) as n FROM taggings WHERE taggable_type IN ('code', 'circuit')")
    .get().n;

  if (!confirmed) {
    console.log("Would delete:");
    console.log(`  ${nCodes} code(s)`);
    console.log(`  ${nCircuits} circuit(s)`);
    console.log(`  ${nBodies} circuit body/bodies`);
    console.log(`  ${nTaggings} tagging(s)`);
    console.log("\nTools are preserved.");
    console.log("\nRun with --yes to confirm.");
    process.exit(0);
  }

  db.transaction(() => {
    db.prepare("DELETE FROM taggings WHERE taggable_type IN ('code', 'circuit')").run();
    db.prepare("DELETE FROM circuits").run(); // cascades to circuit_bodies
    db.prepare("DELETE FROM codes").run();
    db.prepare("DELETE FROM tags WHERE id NOT IN (SELECT DISTINCT tag_id FROM taggings)").run();
  })();

  console.log(
    `Cleared ${nCodes} code(s), ${nCircuits} circuit(s), ${nBodies} body/bodies, ${nTaggings} tagging(s).`,
  );
}

db.close();
