import Database from "better-sqlite3";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const dbPath = path.join(root, "data", "qecirc.db");
const migrationsDir = path.join(root, "data", "migrations");

const db = new Database(dbPath);
db.pragma("journal_mode = WAL");
db.pragma("foreign_keys = ON");

db.exec(`
  CREATE TABLE IF NOT EXISTS _migrations (
    name TEXT PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
  );
`);

const applied = new Set(
  db.prepare("SELECT name FROM _migrations").all().map((r) => r.name),
);

const files = fs
  .readdirSync(migrationsDir)
  .filter((f) => f.endsWith(".sql"))
  .sort();

const applyMigration = db.transaction((file, sql) => {
  db.exec(sql);
  db.prepare("INSERT INTO _migrations (name) VALUES (?)").run(file);
});

for (const file of files) {
  if (applied.has(file)) continue;
  const sql = fs.readFileSync(path.join(migrationsDir, file), "utf-8");
  applyMigration(file, sql);
  console.log(`Applied: ${file}`);
}

db.close();
console.log("Migrations complete.");
