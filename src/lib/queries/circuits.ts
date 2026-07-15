import { getDb } from "../db";
import type {
  Circuit,
  CircuitBody,
  CircuitFilters,
  CircuitOriginalLight,
  CircuitSort,
  TagWithCount,
} from "../../types";
import {
  withTags,
  buildOrderBy,
  hasActiveFilters,
  addConditions,
  addTagConditions,
} from "./shared";

export function formatCircuitId(qecId: number): string {
  return `#${qecId}`;
}

export function getCircuitsForCode(
  codeId: number,
  sort?: CircuitSort,
): (Circuit & { tags: string[] })[] {
  const db = getDb();
  const orderBy = buildOrderBy(sort);
  const rows = db
    .prepare(`SELECT * FROM circuits c WHERE c.code_id = ? ${orderBy}`)
    .all(codeId) as Circuit[];
  return withTags(rows, "circuit");
}

export function countCircuitsForCode(codeId: number): number {
  const db = getDb();
  const row = db
    .prepare("SELECT COUNT(*) as count FROM circuits WHERE code_id = ?")
    .get(codeId) as { count: number };
  return row.count;
}

/** Whether any circuit under this code carries a stabiliser `weight` (only the
 * flag-gadget collector does) — gates showing the weight filter for that page. */
export function codeHasWeightedCircuits(codeId: number): boolean {
  const db = getDb();
  const row = db
    .prepare("SELECT 1 FROM circuits WHERE code_id = ? AND weight IS NOT NULL LIMIT 1")
    .get(codeId);
  return row !== undefined;
}

export function countAllCircuits(): number {
  const db = getDb();
  const row = db.prepare("SELECT COUNT(*) as count FROM circuits").get() as {
    count: number;
  };
  return row.count;
}

/** Distinct papers to cite when using these circuits.
 *
 * `circuits.source` is the work a circuit should be credited to — normally a
 * paper link. It is free-form, though, and some rows instead hold the tool that
 * generated the circuit: a bare name ("circuit-synth"), or a repo URL that is
 * literally a tool's own `github_url`. Those belong to the tool, which carries
 * its own homepage/github/paper links, so they are not counted here.
 *
 * Hence the rule: a source is a paper if it is a link and is not a tool's link.
 * Testing for arxiv.org/doi.org instead would be narrower AND wronger — it
 * would miss a paper published anywhere else (a journal, quantum-journal.org).
 *
 * Counts the circuits' own sources only: `tools.paper_urls` cites the tool, not
 * the circuit.
 */
export function countCircuitPapers(): number {
  const db = getDb();
  const row = db
    .prepare(
      `SELECT COUNT(DISTINCT source) AS count FROM circuits
       WHERE source LIKE 'http%'
         AND source NOT IN (SELECT homepage_url FROM tools WHERE homepage_url IS NOT NULL)
         AND source NOT IN (SELECT github_url FROM tools WHERE github_url IS NOT NULL)`,
    )
    .get() as { count: number };
  return row.count;
}

/** Most recently added circuits, for the landing page.
 *
 * Ordered by `qec_id DESC`, NOT `created_at`: create_database.mjs rebuilds the
 * DB from YAML on every build and omits `created_at` from its INSERT, so every
 * row carries the same build timestamp. `qec_id` is assigned max+1 at ingestion
 * and never reused, making it the only stable "added at" signal in the schema.
 */
export function getLatestCircuits(
  limit: number,
): (Circuit & { tags: string[]; code_slug: string; code_name: string })[] {
  const db = getDb();
  const rows = db
    .prepare(
      `SELECT c.*, co.slug AS code_slug, co.name AS code_name
       FROM circuits c JOIN codes co ON co.id = c.code_id
       ORDER BY c.qec_id DESC LIMIT ?`,
    )
    .all(limit) as (Circuit & { code_slug: string; code_name: string })[];
  return withTags(rows, "circuit") as (Circuit & {
    tags: string[];
    code_slug: string;
    code_name: string;
  })[];
}

export function getCircuitTagsForCode(codeId: number): TagWithCount[] {
  const db = getDb();
  return db
    .prepare(
      `SELECT t.name, COUNT(*) as count FROM tags t
       JOIN taggings tg ON t.id = tg.tag_id
       JOIN circuits c ON c.id = tg.taggable_id
       WHERE tg.taggable_type = 'circuit' AND c.code_id = ?
       GROUP BY t.name ORDER BY t.name`,
    )
    .all(codeId) as TagWithCount[];
}

export function filterCircuitsForCode(
  codeId: number,
  filters: CircuitFilters,
  sort?: CircuitSort,
): (Circuit & { tags: string[] })[] {
  const db = getDb();
  const conditions: string[] = ["c.code_id = ?"];
  const params: (number | string)[] = [codeId];

  addConditions("gate_count", filters.gate_count, conditions, params);
  addConditions("two_qubit_gate_count", filters.two_qubit_gate_count, conditions, params);
  addConditions("depth", filters.depth, conditions, params);
  addConditions("qubit_count", filters.qubit_count, conditions, params);
  addConditions("weight", filters.weight, conditions, params);
  addTagConditions(filters.tags, "circuit", conditions, params);

  const where = `WHERE ${conditions.join(" AND ")}`;
  const orderBy = buildOrderBy(sort);
  const circuits = db
    .prepare(`SELECT * FROM circuits c ${where} ${orderBy}`)
    .all(...params) as Circuit[];
  return withTags(circuits, "circuit");
}

export function getCircuitsWithBodies(
  codeId: number,
  filters: CircuitFilters,
  sort?: CircuitSort,
): {
  circuits: (Circuit & { tags: string[] })[];
  bodiesMap: Map<number, CircuitBody[]>;
} {
  const circuits = hasActiveFilters(filters)
    ? filterCircuitsForCode(codeId, filters, sort)
    : getCircuitsForCode(codeId, sort);
  const bodiesMap = getBodiesForCircuits(circuits.map((c) => c.id));
  return { circuits, bodiesMap };
}

const FORMAT_ORDER = ["stim", "qasm", "cirq"];

export function getBodiesForCircuits(circuitIds: number[]): Map<number, CircuitBody[]> {
  const db = getDb();
  const result = new Map<number, CircuitBody[]>();
  if (circuitIds.length === 0) return result;

  const placeholders = circuitIds.map(() => "?").join(",");
  const rows = db
    .prepare(
      `SELECT circuit_id, format, body FROM circuit_bodies
       WHERE circuit_id IN (${placeholders})`,
    )
    .all(...circuitIds) as (CircuitBody & { circuit_id: number })[];

  for (const row of rows) {
    const list = result.get(row.circuit_id) ?? [];
    list.push({ format: row.format, body: row.body });
    result.set(row.circuit_id, list);
  }

  // Sort each circuit's bodies by preferred format order
  for (const [, bodies] of result) {
    bodies.sort((a, b) => {
      const ai = FORMAT_ORDER.indexOf(a.format);
      const bi = FORMAT_ORDER.indexOf(b.format);
      return (ai === -1 ? Infinity : ai) - (bi === -1 ? Infinity : bi);
    });
  }

  return result;
}

/** Bodies for a single circuit looked up by its public qec_id, in preferred
 * format order. Returns [] when the circuit doesn't exist. */
export function getBodiesForCircuitByQecId(qecId: number): CircuitBody[] {
  const db = getDb();
  const row = db.prepare("SELECT id FROM circuits WHERE qec_id = ?").get(qecId) as
    { id: number } | undefined;
  if (!row) return [];
  return getBodiesForCircuits([row.id]).get(row.id) ?? [];
}

export function getCircuitByQecId(
  qecId: number,
): (Circuit & { tags: string[]; code_slug: string; code_name: string }) | null {
  const db = getDb();
  const row = db
    .prepare(
      `SELECT c.*, co.slug AS code_slug, co.name AS code_name
       FROM circuits c
       JOIN codes co ON co.id = c.code_id
       WHERE c.qec_id = ?`,
    )
    .get(qecId) as (Circuit & { code_slug: string; code_name: string }) | undefined;
  if (!row) return null;
  const [enriched] = withTags([row], "circuit");
  return {
    ...enriched,
    code_slug: row.code_slug,
    code_name: row.code_name,
  };
}

export function getCircuitsByQecIds(
  qecIds: number[],
): (Circuit & { tags: string[]; code_slug: string; code_name: string })[] {
  if (qecIds.length === 0) return [];
  const capped = qecIds.slice(0, 200);
  const db = getDb();
  const placeholders = capped.map(() => "?").join(",");
  const rows = db
    .prepare(
      `SELECT c.*, co.slug AS code_slug, co.name AS code_name
       FROM circuits c
       JOIN codes co ON co.id = c.code_id
       WHERE c.qec_id IN (${placeholders})
       ORDER BY co.name, c.name`,
    )
    .all(...capped) as (Circuit & { code_slug: string; code_name: string })[];
  return withTags(rows, "circuit") as (Circuit & {
    tags: string[];
    code_slug: string;
    code_name: string;
  })[];
}

export function getAllCircuitQecIds(): number[] {
  const db = getDb();
  const rows = db.prepare(`SELECT qec_id FROM circuits ORDER BY qec_id`).all() as {
    qec_id: number;
  }[];
  return rows.map((r) => r.qec_id);
}

export function getOriginalForCircuit(circuitId: number): CircuitOriginalLight | null {
  const db = getDb();
  return (
    (db
      .prepare(
        `SELECT original_stim,
                (original_h IS NOT NULL AND original_logical IS NOT NULL) AS has_original_matrices
         FROM circuit_originals WHERE circuit_id = ?`,
      )
      .get(circuitId) as CircuitOriginalLight | undefined) ?? null
  );
}
