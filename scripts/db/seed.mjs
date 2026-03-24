import Database from "better-sqlite3";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const dbPath = path.join(root, "data", "qecirc.db");

const db = new Database(dbPath);
db.pragma("foreign_keys = ON");

// --- Steane Code [[7,1,3]] ---

// Compact STIM format: gates on same tick grouped per line
const steaneStim = `# Steane [[7,1,3]] encoding circuit
H 4 5 6
CX 5 1
CX 1 2 4 0
CX 6 4 5 3 2 0
CX 6 3 4 5 0 1
`;

// Check matrices (Hx = Hz for CSS Steane code)
const steaneH = [[1,1,0,0,1,1,0],[1,0,1,0,1,0,1],[0,0,0,1,1,1,1]];

// Logical operators (all-ones for Steane code)
const steaneLx = [[1,1,1,1,1,1,1]];
const steaneLz = [[1,1,1,1,1,1,1]];

const insertCode = db.prepare(`
  INSERT INTO codes (name, slug, n, k, d, zoo_url, hx, hz, logical_x, logical_z)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`);

const insertCircuit = db.prepare(`
  INSERT INTO circuits (code_id, name, slug, description, source, gate_count, depth, qubit_count, crumble_url, quirk_url)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`);

const insertBody = db.prepare(`
  INSERT INTO circuit_bodies (circuit_id, format, body)
  VALUES (?, ?, ?)
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
    7, 1, 3,
    "https://errorcorrectionzoo.org/c/steane",
    JSON.stringify(steaneH),
    JSON.stringify(steaneH),  // Hx = Hz for the Steane code
    JSON.stringify(steaneLx),
    JSON.stringify(steaneLz),
  );

  // Circuit
  const { lastInsertRowid: circuitId } = insertCircuit.run(
    codeId,
    "Standard Encoding",
    "standard-encoding",
    "Encodes 1 logical qubit into 7 physical qubits preparing the logical |0\u27E9 state.",
    "https://doi.org/10.1098/rspa.1996.0136",
    12,  // gate_count: 3 H + 9 CX
    8,   // depth
    7,   // qubit_count
    "https://algassert.com/crumble#circuit=Q(0,0)0;Q(1,0)1;Q(2,0)2;Q(3,0)3;Q(4,0)4;Q(5,0)5;Q(6,0)6;H_4_5_6;TICK;CX_5_1;TICK;CX_1_2_4_0;TICK;CX_6_4_5_3_2_0;TICK;CX_6_3_4_5_0_1",
    "https://algassert.com/quirk",
  );

  // Circuit bodies (multi-format)
  insertBody.run(circuitId, "stim", steaneStim);

  // Code tags
  addTag("CSS", codeId, "code");
  addTag("stabilizer", codeId, "code");
  addTag("color-code", codeId, "code");

  // Circuit tags
  addTag("encoding", circuitId, "circuit");
  addTag("state-preparation", circuitId, "circuit");
  addTag("distance:3", circuitId, "circuit");
})();

db.close();
console.log("Seed complete.");
