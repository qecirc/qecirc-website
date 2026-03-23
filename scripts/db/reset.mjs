import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const dbPath = path.join(root, "data", "qecirc.db");

// Remove existing database
for (const suffix of ["", "-wal", "-shm"]) {
  const file = dbPath + suffix;
  if (fs.existsSync(file)) fs.unlinkSync(file);
}

console.log("Database removed.");

execSync("node scripts/db/migrate.mjs", { cwd: root, stdio: "inherit" });
execSync("node scripts/db/seed.mjs", { cwd: root, stdio: "inherit" });

console.log("Reset complete.");
