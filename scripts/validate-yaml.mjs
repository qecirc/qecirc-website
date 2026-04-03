import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";

const DATA_DIR = path.join(process.cwd(), "data_yaml");

const BODY_EXTENSIONS = [".stim", ".qasm", ".cirq"];

// --- Schema definitions ---

const SCHEMAS = {
  codes: {
    required: {
      name: "string",
      n: "number",
      k: "number",
    },
    optional: {
      d: "number",
      canonical_hash: "string",
      zoo_url: "string",
      hx: "matrix",
      hz: "matrix",
      logical_x: "matrix",
      logical_z: "matrix",
      tags: "tags",
    },
  },
  circuits: {
    required: { name: "string", source: "string" },
    optional: {
      tool: "string",
      description: "string",
      gate_count: "number",
      two_qubit_gate_count: "number",
      depth: "number",
      qubit_count: "number",
      crumble_url: "string",
      quirk_url: "string",
      tags: "tags",
    },
  },
  tools: {
    required: { name: "string" },
    optional: {
      description: "string",
      homepage_url: "string",
      github_url: "string",
      tags: "tags",
    },
  },
};

// --- Validators ---

function checkType(value, type) {
  if (type === "string") return typeof value === "string";
  if (type === "number")
    return typeof value === "number" && Number.isFinite(value);
  if (type === "tags")
    return Array.isArray(value) && value.every((v) => typeof v === "string");
  if (type === "matrix")
    return (
      Array.isArray(value) &&
      value.every(
        (row) => Array.isArray(row) && row.every((v) => typeof v === "number"),
      )
    );
  return false;
}

function validate(file, data, schema) {
  const errors = [];

  if (typeof data !== "object" || data === null || Array.isArray(data)) {
    return [`${file}: expected a YAML mapping, got ${typeof data}`];
  }

  const allowedKeys = new Set([
    ...Object.keys(schema.required),
    ...Object.keys(schema.optional),
  ]);

  for (const key of Object.keys(schema.required)) {
    if (!(key in data)) {
      errors.push(`${file}: missing required field "${key}"`);
    } else if (!checkType(data[key], schema.required[key])) {
      errors.push(
        `${file}: field "${key}" should be ${schema.required[key]}, got ${typeof data[key]}`,
      );
    }
  }

  for (const key of Object.keys(data)) {
    if (!allowedKeys.has(key)) {
      errors.push(`${file}: unknown field "${key}"`);
    } else if (
      key in schema.optional &&
      !checkType(data[key], schema.optional[key])
    ) {
      errors.push(
        `${file}: field "${key}" should be ${schema.optional[key]}, got ${typeof data[key]}`,
      );
    }
  }

  return errors;
}

// --- Main ---

let allErrors = [];

for (const [dir, schema] of Object.entries(SCHEMAS)) {
  const dirPath = path.join(DATA_DIR, dir);
  if (!fs.existsSync(dirPath)) {
    allErrors.push(`Directory not found: ${dirPath}`);
    continue;
  }

  const files = fs.readdirSync(dirPath).filter((f) => f.endsWith(".yaml"));

  if (files.length === 0) continue;

  for (const file of files) {
    const filePath = path.join(dirPath, file);
    const relPath = path.join(dir, file);

    let data;
    try {
      data = yaml.load(fs.readFileSync(filePath, "utf8"));
    } catch (e) {
      allErrors.push(`${relPath}: invalid YAML — ${e.message}`);
      continue;
    }

    allErrors.push(...validate(relPath, data, schema));

    if (dir === "circuits") {
      const base = file.replace(/\.yaml$/, "");

      // Check filename convention: <code-slug>--<circuit-slug>
      const sep = base.indexOf("--");
      if (sep === -1) {
        allErrors.push(
          `${relPath}: filename must follow <code-slug>--<circuit-slug>.yaml`,
        );
      } else {
        const codeSlug = base.slice(0, sep);
        const codeFile = path.join(DATA_DIR, "codes", codeSlug + ".yaml");
        if (!fs.existsSync(codeFile)) {
          allErrors.push(
            `${relPath}: no matching code file codes/${codeSlug}.yaml`,
          );
        }
      }

      // Check that at least one body file exists
      const hasBody = BODY_EXTENSIONS.some((ext) =>
        fs.existsSync(path.join(dirPath, base + ext)),
      );
      if (!hasBody) {
        allErrors.push(
          `${relPath}: no body file found (expected ${BODY_EXTENSIONS.join(", ")})`,
        );
      }
    }
  }
}

if (allErrors.length > 0) {
  console.error("YAML validation failed:\n");
  for (const err of allErrors) {
    console.error(`  ✗ ${err}`);
  }
  process.exit(1);
} else {
  console.log("All YAML files valid.");
}
