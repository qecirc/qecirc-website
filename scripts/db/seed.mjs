import Database from "better-sqlite3";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const dbPath = path.join(root, "data", "qecirc.db");

const db = new Database(dbPath);
db.pragma("foreign_keys = ON");

// --- Steane Code [[7,1,3]] ---

const steaneCircuit = `# Steane [[7,1,3]] encoding circuit
# Encodes 1 logical qubit into 7 physical qubits
H 4
H 5
H 6
CX 5 1
CX 1 2
CX 4 0
CX 6 4
CX 5 3
CX 2 0
CX 6 3
CX 4 5
CX 0 1
`;

const insertCode = db.prepare(`
  INSERT INTO codes (name, slug, description, n, k, d)
  VALUES (?, ?, ?, ?, ?, ?)
`);

const insertFunctionality = db.prepare(`
  INSERT INTO functionalities (code_id, name, slug, description)
  VALUES (?, ?, ?, ?)
`);

const insertCircuit = db.prepare(`
  INSERT INTO circuits (functionality_id, name, slug, source, format, body)
  VALUES (?, ?, ?, ?, ?, ?)
`);

const insertTag = db.prepare(`
  INSERT OR IGNORE INTO tags (name) VALUES (?)
`);

const insertTagging = db.prepare(`
  INSERT INTO taggings (tag_id, taggable_id, taggable_type)
  VALUES (?, ?, ?)
`);

const getTagId = db.prepare("SELECT id FROM tags WHERE name = ?");

function addTag(name, taggableId, taggableType) {
  insertTag.run(name);
  const { id } = getTagId.get(name);
  insertTagging.run(id, taggableId, taggableType);
}

db.transaction(() => {
  // Code
  const { lastInsertRowid: codeId } = insertCode.run(
    "Steane Code",
    "steane-code",
    "The [[7,1,3]] Steane code is a CSS code that encodes 1 logical qubit into 7 physical qubits with distance 3. It is the smallest code in the color code family and can correct any single-qubit error.",
    7, 1, 3,
  );

  // Functionality
  const { lastInsertRowid: funcId } = insertFunctionality.run(
    codeId,
    "Encoding",
    "encoding",
    "Prepares the logical |0\u27E9 state by encoding 1 logical qubit into 7 physical qubits.",
  );

  // Circuit
  const { lastInsertRowid: circuitId } = insertCircuit.run(
    funcId,
    "Standard Encoding",
    "standard-encoding",
    "https://doi.org/10.1098/rspa.1996.0136",
    "stim",
    steaneCircuit,
  );

  // Tags
  addTag("CSS", codeId, "code");
  addTag("stabilizer", codeId, "code");
  addTag("color-code", codeId, "code");

  addTag("state-preparation", funcId, "functionality");

  addTag("distance:3", circuitId, "circuit");
})();

db.close();
console.log("Seed complete.");
