import fs from "node:fs";
import path from "node:path";
import * as yaml from "js-yaml";
import { paperKey, paperLinks, isPaperSource } from "./paper-links.mjs";
import { isMatrix } from "./matrix-format.mjs";

const DATA_DIR = path.join(process.cwd(), "data_yaml");

// `.stim-annotated` holds the detector/observable-annotated variant of the
// canonical `.stim` body; both are indexed as circuit_bodies formats.
const BODY_EXTENSIONS = [".stim", ".qasm", ".cirq", ".stim-annotated"];

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
      aliases: "tags",
      related: "tags",
      h: "matrix",
      logical: "matrix",
      tags: "tags",
    },
  },
  circuits: {
    required: { qec_id: "number", name: "string", source: "string" },
    optional: {
      tool: "string",
      notes: "string",
      // For logical-gate circuits: the claimed logical Clifford as a stim
      // circuit on the k logical qubits (e.g. "S 0"). Checked by
      // validate:circuits against the code's h/logical matrices.
      logical_action: "string",
      gate_count: "number",
      two_qubit_gate_count: "number",
      depth: "number",
      qubit_count: "number",
      weight: "number",
      crumble_url: "string",
      crumble_url_annotated: "string",
      quirk_url: "string",
      original_matrices: "string",
      tags: "tags",
    },
  },
  tools: {
    required: { name: "string" },
    optional: {
      description: "string",
      homepage_url: "string",
      github_url: "string",
      paper_urls: "urls",
      aliases: "tags",
      tags: "tags",
    },
  },
  papers: {
    required: { title: "string", authors: "names", url: "string" },
    optional: {
      year: "number",
      // Typed `string` deliberately, and the reason is a real trap: unquoted,
      // `arxiv_id: 2402.17761` is a YAML FLOAT, and 2601.05110 would silently
      // lose its trailing zero. The type check is what forces the quotes.
      arxiv_id: "string",
      doi: "string",
      journal_ref: "string",
    },
  },
};

// --- Validators ---

function checkType(value, type) {
  if (type === "string") return typeof value === "string";
  if (type === "number") return typeof value === "number" && Number.isFinite(value);
  if (type === "tags") return Array.isArray(value) && value.every((v) => typeof v === "string");
  if (type === "names")
    return (
      Array.isArray(value) &&
      value.length > 0 &&
      value.every((v) => typeof v === "string" && v.trim() !== "")
    );
  if (type === "urls")
    return (
      Array.isArray(value) && value.every((v) => typeof v === "string" && /^https?:\/\//.test(v))
    );
  if (type === "matrix") return isMatrix(value);
  return false;
}

function validate(file, data, schema) {
  const errors = [];

  if (typeof data !== "object" || data === null || Array.isArray(data)) {
    return [`${file}: expected a YAML mapping, got ${typeof data}`];
  }

  const allowedKeys = new Set([...Object.keys(schema.required), ...Object.keys(schema.optional)]);

  for (const key of Object.keys(schema.required)) {
    if (!(key in data)) {
      errors.push(`${file}: missing required field "${key}"`);
    } else if (!checkType(data[key], schema.required[key])) {
      errors.push(
        `${file}: field "${key}" should be ${schema.required[key]}, got ${typeof data[key]}`,
      );
    } else if (schema.required[key] === "string" && data[key].trim() === "") {
      // Required string fields must be non-empty. The DB build
      // (create_database.mjs) treats an empty string as missing (falsy), so
      // rejecting it here keeps the two validators consistent and catches it in
      // CI before the build (e.g. an empty `source` — provenance is required).
      errors.push(`${file}: required field "${key}" must not be empty`);
    }
  }

  for (const key of Object.keys(data)) {
    if (!allowedKeys.has(key)) {
      errors.push(`${file}: unknown field "${key}"`);
    } else if (key in schema.optional && !checkType(data[key], schema.optional[key])) {
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

      // qec_id must be a positive integer
      if (
        data &&
        typeof data.qec_id === "number" &&
        (!Number.isInteger(data.qec_id) || data.qec_id < 1)
      ) {
        allErrors.push(`${relPath}: qec_id must be a positive integer, got ${data.qec_id}`);
      }

      // Check filename convention: <code-slug>--<circuit-slug>
      const sep = base.indexOf("--");
      if (sep === -1) {
        allErrors.push(`${relPath}: filename must follow <code-slug>--<circuit-slug>.yaml`);
      } else {
        const codeSlug = base.slice(0, sep);
        const codeFile = path.join(DATA_DIR, "codes", codeSlug + ".yaml");
        if (!fs.existsSync(codeFile)) {
          allErrors.push(`${relPath}: no matching code file codes/${codeSlug}.yaml`);
        }
      }

      // Check that at least one body file exists
      const hasBody = BODY_EXTENSIONS.some((ext) => fs.existsSync(path.join(dirPath, base + ext)));
      if (!hasBody) {
        allErrors.push(`${relPath}: no body file found (expected ${BODY_EXTENSIONS.join(", ")})`);
      }

      // Check tool reference
      if (data && data.tool) {
        const toolFile = path.join(DATA_DIR, "tools", data.tool + ".yaml");
        if (!fs.existsSync(toolFile)) {
          allErrors.push(`${relPath}: tool '${data.tool}' not found in data_yaml/tools/`);
        }
      }
    }

    if (dir === "papers") {
      if (typeof data?.url === "string" && !/^https?:\/\//.test(data.url)) {
        allErrors.push(`${relPath}: url must be an http(s) link, got '${data.url}'`);
      }
      // The id is the match key, so its shape is load-bearing: "arXiv:2402.17761"
      // or "2402.17761v2" would build a link no circuit source equals.
      if (typeof data?.arxiv_id === "string") {
        if (/^arxiv:/i.test(data.arxiv_id)) {
          allErrors.push(`${relPath}: arxiv_id must not carry an 'arXiv:' prefix`);
        }
        if (/v\d+$/.test(data.arxiv_id)) {
          allErrors.push(`${relPath}: arxiv_id must not carry a version suffix`);
        }
      }
      if (typeof data?.doi === "string" && /^https?:\/\//.test(data.doi)) {
        allErrors.push(`${relPath}: doi must be a bare DOI, not a link (use url for the link)`);
      }
    }
  }
}

// --- Papers: link collisions, and circuit sources that will not resolve ---
//
// Both are warnings, not errors: a source with no paper still renders and still
// searches by URL, it just cannot be found by title or author. Failing the build
// over it would make adding a circuit depend on cataloguing its paper first.
const warnings = [];
{
  const papersDir = path.join(DATA_DIR, "papers");
  const circuitsDir = path.join(DATA_DIR, "circuits");
  const claimed = new Map(); // paperKey -> paper file

  if (fs.existsSync(papersDir)) {
    for (const file of fs.readdirSync(papersDir).filter((f) => f.endsWith(".yaml"))) {
      let data;
      try {
        data = yaml.load(fs.readFileSync(path.join(papersDir, file), "utf8"));
      } catch {
        continue; // parse error already reported above
      }
      if (!data) continue;
      for (const link of paperLinks(data)) {
        const key = paperKey(link);
        if (claimed.has(key) && claimed.get(key) !== file) {
          allErrors.push(
            `papers/${file}: link '${link}' is also claimed by papers/${claimed.get(key)}`,
          );
        } else {
          claimed.set(key, file);
        }
      }
    }
  }

  if (fs.existsSync(circuitsDir)) {
    const unmatched = new Map(); // source -> circuit count
    for (const file of fs.readdirSync(circuitsDir).filter((f) => f.endsWith(".yaml"))) {
      let data;
      try {
        data = yaml.load(fs.readFileSync(path.join(circuitsDir, file), "utf8"));
      } catch {
        continue;
      }
      if (!data || !isPaperSource(data.source)) continue;
      if (!claimed.has(paperKey(data.source))) {
        unmatched.set(data.source, (unmatched.get(data.source) ?? 0) + 1);
      }
    }
    for (const [source, count] of [...unmatched].sort((a, b) => b[1] - a[1])) {
      warnings.push(
        `${count} circuit${count === 1 ? "" : "s"} cite '${source}', which has no file in ` +
          `data_yaml/papers/ — they are searchable by URL but not by title or author`,
      );
    }
  }
}

// --- Cross-file uniqueness check for circuit qec_id ---
{
  const circuitsDir = path.join(DATA_DIR, "circuits");
  if (fs.existsSync(circuitsDir)) {
    const seen = new Map(); // qec_id -> filename
    for (const file of fs.readdirSync(circuitsDir).filter((f) => f.endsWith(".yaml"))) {
      let data;
      try {
        data = yaml.load(fs.readFileSync(path.join(circuitsDir, file), "utf8"));
      } catch {
        continue; // parse error already reported above
      }
      if (data && typeof data.qec_id === "number") {
        if (seen.has(data.qec_id)) {
          allErrors.push(
            `circuits/${file}: duplicate qec_id ${data.qec_id} (also in ${seen.get(data.qec_id)})`,
          );
        } else {
          seen.set(data.qec_id, file);
        }
      }
    }
  }
}

if (warnings.length > 0) {
  console.warn("Warnings:\n");
  for (const w of warnings) {
    console.warn(`  ! ${w}`);
  }
  console.warn("");
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
