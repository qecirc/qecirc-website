import { getDb } from "../db";
import type { Circuit, CodeListItem, TagWithCount, Tool } from "../../types";
import { withTags, addTagConditions } from "./shared";
import { correctTokens } from "./spelling";
import { bm25Weights, strictColumns } from "./search-schema";
import { parseToolRow, type ToolRow } from "./tools";

/** Shortest query we will run. Below this, LIKE/FTS scans match near-everything
 *  and the result list is noise. Mirrored by /api/search and /search. */
export const MIN_QUERY_LENGTH = 2;

/** Split raw user input into safe search tokens.
 *
 * Raw input CANNOT be passed to MATCH: bare `AND`/`OR`/`NOT`/`NEAR`, `*`, `^`,
 * `:`, `-` and `"` are query syntax, so a search for `code-capacity` or a lone
 * `*` would either throw or silently mean something else. Tokens are quoted
 * into literal phrases by buildFtsExpr below.
 */
export function tokenizeQuery(raw: string): string[] {
  return (
    raw
      .trim()
      .split(/\s+/)
      // Drop `"` outright: escaping it by doubling would let a crafted query
      // reopen a phrase. Tokens must retain a letter or digit to be meaningful --
      // FTS5 rejects an empty phrase ("").
      .map((t) => t.replace(/"/g, ""))
      .filter((t) => /[\p{L}\p{N}]/u.test(t))
  );
}

/** Quote each token as a literal phrase and join them. The final token gets a
 *  `*` so partial words still match ("encod" -> "encoding").
 *
 * `scope` restricts the whole expression to a column set. Applied around the
 * group rather than per token so that AND/OR still range over the expression:
 * `{a b} : (x AND y)` means "x and y, each in a or b", whereas repeating the
 * filter per token would nest filters and change what the operators bind to.
 */
function buildFtsExpr(tokens: string[], op: "AND" | "OR", scope?: string): string {
  const expr = tokens.map((t, i) => `"${t}"${i === tokens.length - 1 ? "*" : ""}`).join(` ${op} `);
  return scope ? `${scope} : (${expr})` : expr;
}

function countMatches(expr: string): number {
  const row = getDb()
    .prepare("SELECT COUNT(*) AS n FROM circuit_search WHERE circuit_search MATCH ?")
    .get(expr) as { n: number };
  return row.n;
}

/** A query worked out into the expression we will actually run, plus what to
 *  tell the user we did. Results and facets MUST be built from the same one, or
 *  the filter counts describe a different search than the list. */
export interface ResolvedQuery {
  /** Exactly what the user typed. */
  raw: string;
  /** What we searched for -- differs from `raw` only when spelling was fixed. */
  display: string;
  /** The FTS5 MATCH expression. */
  match: string;
  /** Spelling was corrected; the page should say so and offer the literal. */
  corrected: boolean;
  /** No circuit had every term, so we matched any term instead. */
  partial: boolean;
  /** Nothing matched by name/alias, so we fell back to `related` -- these
   *  circuits are a DIFFERENT code to the one asked for (a planar surface code
   *  for "toric"). The page must say so; silently equating them would assert
   *  something untrue. */
  relatedOnly: boolean;
}

/** Returns null when nothing searchable remains (e.g. input was all
 *  punctuation), which callers must treat as "no results" rather than
 *  "match everything". */
export function resolveQuery(raw: string, opts: { literal?: boolean } = {}): ResolvedQuery | null {
  const tokens = tokenizeQuery(raw);
  if (tokens.length === 0) return null;

  const { tokens: fixed, changed } = opts.literal
    ? { tokens, changed: false }
    : correctTokens(tokens);

  // Widening is a last resort, and the order below is the whole design: each
  // step gives up less than the one after it.
  //
  //   1. every term, by name/alias        -- what was asked for
  //   2. every term, allowing `related`   -- a neighbouring code, flagged
  //   3. any term, by name/alias          -- a weaker answer to the question
  //   4. any term, allowing `related`
  //
  // (2) precedes (3) because dropping to "any term" is the bigger concession:
  // "toric code" widened to ANY term matches every circuit with "code" in it
  // (824 of 833), while allowing `related` returns surface codes -- which is
  // what the user meant. Ranking (3) first would answer a precise query with the
  // catalogue.
  //
  // Decided on the query alone, before code/tag filters, so that narrowing a
  // filter to zero cannot silently widen the query underneath it.
  const attempts: { match: string; partial: boolean; relatedOnly: boolean }[] = [
    { match: buildFtsExpr(fixed, "AND", strictColumns()), partial: false, relatedOnly: false },
    { match: buildFtsExpr(fixed, "AND"), partial: false, relatedOnly: true },
  ];
  if (fixed.length > 1) {
    attempts.push(
      { match: buildFtsExpr(fixed, "OR", strictColumns()), partial: true, relatedOnly: false },
      { match: buildFtsExpr(fixed, "OR"), partial: true, relatedOnly: true },
    );
  }

  const base = { raw, display: fixed.join(" "), corrected: changed };
  for (const attempt of attempts) {
    if (countMatches(attempt.match) > 0) return { ...base, ...attempt };
  }
  // Nothing matched anywhere. Return the strictest expression so the page
  // reports "no results" for what was actually asked, not for a widened query.
  return { ...base, ...attempts[0] };
}

function rawTokenize(query: string): string[] {
  return query
    .trim()
    .split(/\s+/)
    .filter((t) => t.length > 0);
}

function tokenize(query: string): string[] {
  return rawTokenize(query).map((t) => `%${t.replace(/[%_\\]/g, "\\$&")}%`);
}

function searchByType<T extends { id: number }>(
  table: string,
  taggableType: "code" | "circuit" | "tool",
  query: string,
  limit: number,
  columns: string = "c.*",
): (T & { tags: string[] })[] {
  const patterns = tokenize(query);
  if (patterns.length === 0) return [];

  // `aliases` is matched here but `related` deliberately is not: the quick-search
  // is a jump-to-a-known-thing list with no room to explain itself, and offering
  // "Rotated Surface Code" under the heading of a `toric` search would read as a
  // claim that they are the same code. /search has the space to say otherwise.
  const db = getDb();
  const tokenClauses = patterns.map(
    () =>
      `(c.name LIKE ? ESCAPE '\\' OR c.aliases LIKE ? ESCAPE '\\' OR EXISTS (
        SELECT 1 FROM taggings tg JOIN tags t ON t.id = tg.tag_id
        WHERE tg.taggable_id = c.id AND tg.taggable_type = ? AND t.name LIKE ? ESCAPE '\\'
      ))`,
  );
  const params: string[] = [];
  for (const p of patterns) params.push(p, p, taggableType, p);

  const rows = db
    .prepare(
      `SELECT ${columns} FROM ${table} c
       WHERE ${tokenClauses.join(" AND ")}
       ORDER BY c.name
       LIMIT ?`,
    )
    .all(...params, limit) as T[];
  return withTags(rows, taggableType);
}

// Match CODE_LIST_COLUMNS in queries/codes.ts — skip the large h/logical
// JSON blobs since the search dropdown never renders matrices.
const CODE_SEARCH_COLUMNS = "c.id, c.name, c.slug, c.n, c.k, c.d, c.zoo_url, c.canonical_hash";

export function searchCodes(query: string): (CodeListItem & { tags: string[] })[] {
  return searchByType<CodeListItem>("codes", "code", query, 20, CODE_SEARCH_COLUMNS);
}

export function searchCircuits(
  query: string,
): (Circuit & { tags: string[]; code_slug: string; code_name: string })[] {
  const rawTokens = rawTokenize(query);
  if (rawTokens.length === 0) return [];

  const db = getDb();
  const tokenClauses: string[] = [];
  const params: (string | number)[] = [];

  for (const raw of rawTokens) {
    const p = `%${raw.replace(/[%_\\]/g, "\\$&")}%`;
    const stripped = raw.replace(/^#/, "");
    const asInt = /^\d+$/.test(stripped) ? parseInt(stripped, 10) : null;

    // As in searchByType: code aliases match, code `related` names do not.
    if (asInt !== null) {
      tokenClauses.push(
        `(ci.qec_id = ? OR ci.name LIKE ? ESCAPE '\\' OR co.name LIKE ? ESCAPE '\\'
          OR co.aliases LIKE ? ESCAPE '\\'
          OR EXISTS (
            SELECT 1 FROM taggings tg JOIN tags t ON t.id = tg.tag_id
            WHERE tg.taggable_id = ci.id AND tg.taggable_type = 'circuit' AND t.name LIKE ? ESCAPE '\\'
          )
          OR EXISTS (
            SELECT 1 FROM tools tl WHERE tl.id = ci.tool_id
              AND (tl.name LIKE ? ESCAPE '\\' OR tl.aliases LIKE ? ESCAPE '\\')
          ))`,
      );
      params.push(asInt, p, p, p, p, p, p);
    } else {
      tokenClauses.push(
        `(ci.name LIKE ? ESCAPE '\\' OR co.name LIKE ? ESCAPE '\\'
          OR co.aliases LIKE ? ESCAPE '\\'
          OR EXISTS (
            SELECT 1 FROM taggings tg JOIN tags t ON t.id = tg.tag_id
            WHERE tg.taggable_id = ci.id AND tg.taggable_type = 'circuit' AND t.name LIKE ? ESCAPE '\\'
          )
          OR EXISTS (
            SELECT 1 FROM tools tl WHERE tl.id = ci.tool_id
              AND (tl.name LIKE ? ESCAPE '\\' OR tl.aliases LIKE ? ESCAPE '\\')
          ))`,
      );
      params.push(p, p, p, p, p, p);
    }
  }

  const rows = db
    .prepare(
      `SELECT ci.*, co.slug AS code_slug, co.name AS code_name
       FROM circuits ci
       JOIN codes co ON co.id = ci.code_id
       WHERE ${tokenClauses.join(" AND ")}
       ORDER BY ci.name
       LIMIT 10`,
    )
    .all(...params) as (Circuit & { code_slug: string; code_name: string })[];

  return withTags(rows, "circuit") as (Circuit & {
    tags: string[];
    code_slug: string;
    code_name: string;
  })[];
}

export function searchTools(query: string): (Tool & { tags: string[] })[] {
  return searchByType<ToolRow & { id: number }>("tools", "tool", query, 10).map((row) => ({
    ...parseToolRow(row),
    tags: row.tags,
  }));
}

/** A search hit carries its code's [[n,k,d]] because CODE NAMES ARE NOT UNIQUE:
 *  "Rotated Surface Code" is 5 distinct codes ([[9,1,3]], [[25,1,5]], ...).
 *  Rendering a result by name alone produces indistinguishable rows. */
export type RankedCircuit = Circuit & {
  tags: string[];
  code_slug: string;
  code_name: string;
  code_n: number;
  code_k: number;
  code_d: number | null;
};

const RANKED_COLUMNS = `c.*, co.slug AS code_slug, co.name AS code_name,
       co.n AS code_n, co.k AS code_k, co.d AS code_d`;

export interface CircuitSearchOptions {
  /** Restrict to one code (the /search "code" filter). */
  codeId?: number;
  /** Circuit must carry every one of these tags (AND, matching the rest of the site). */
  tags?: string[];
  limit?: number;
}

/** The codes and tags actually present in a query's matches, for building
 *  filter controls that only offer choices which lead somewhere.
 *
 * Computed from the query alone, NOT from the query plus active filters:
 * facets narrowed by the current selection would drop every other tag the
 * moment you picked one, making a second tag unselectable. Counts are
 * therefore "matches for this query", independent of what is selected.
 *
 * Tags come back in name order to match the circuit tag dropdowns on a code
 * page (getCircuitTagsForCode), which /search reuses.
 *
 * Also computed over ALL matches, not the capped result page -- "codes in the
 * results" must not mean "codes in the first 100".
 */
export interface SearchFacets {
  codes: {
    id: number;
    slug: string;
    name: string;
    n: number;
    k: number;
    d: number | null;
    count: number;
  }[];
  tags: TagWithCount[];
}

export function searchCircuitFacets(query: ResolvedQuery): SearchFacets {
  const match = query.match;
  const db = getDb();
  const codes = db
    .prepare(
      `SELECT co.id, co.slug, co.name, co.n, co.k, co.d, COUNT(*) AS count
       FROM circuit_search
       JOIN circuits c ON c.id = circuit_search.circuit_id
       JOIN codes co ON co.id = c.code_id
       WHERE circuit_search MATCH ?
       GROUP BY co.id
       ORDER BY co.name, co.n`,
    )
    .all(match) as SearchFacets["codes"];

  const tags = db
    .prepare(
      `SELECT t.name, COUNT(*) AS count
       FROM circuit_search
       JOIN circuits c ON c.id = circuit_search.circuit_id
       JOIN taggings tg ON tg.taggable_id = c.id AND tg.taggable_type = 'circuit'
       JOIN tags t ON t.id = tg.tag_id
       WHERE circuit_search MATCH ?
       GROUP BY t.name
       ORDER BY t.name`,
    )
    .all(match) as TagWithCount[];

  return { codes, tags };
}

/** Circuit search for /search: full-text over name/code name/tags/notes,
 *  ranked by relevance, optionally restricted to one code.
 *
 * Distinct from `searchCircuits` (which backs the header quick-search dropdown
 * with LIKE matching over names/tags only). This one reads `notes` too and
 * orders by BM25 rather than alphabetically.
 *
 * A query of `42` or `#42` additionally pins circuit #42 to the top. That lookup
 * runs SEPARATELY from the FTS match rather than as an ORDER BY case: qec_id is
 * UNINDEXED, so #42's text need not contain "42" anywhere and the MATCH would
 * never surface it. FTS5 also cannot OR a MATCH against a plain column.
 */
export function searchCircuitsRanked(
  query: ResolvedQuery,
  opts: CircuitSearchOptions = {},
): RankedCircuit[] {
  const limit = opts.limit ?? 100;

  const db = getDb();
  const conditions: string[] = ["circuit_search MATCH ?"];
  const params: (number | string)[] = [query.match];

  if (opts.codeId != null) {
    conditions.push("c.code_id = ?");
    params.push(opts.codeId);
  }
  addTagConditions(opts.tags, "circuit", conditions, params);

  // bm25() returns 0 or negative, better matches being MORE negative, so
  // ascending order is best-first. c.name breaks ties deterministically.
  const rows = db
    .prepare(
      `SELECT ${RANKED_COLUMNS}
       FROM circuit_search
       JOIN circuits c ON c.id = circuit_search.circuit_id
       JOIN codes co ON co.id = c.code_id
       WHERE ${conditions.join(" AND ")}
       ORDER BY bm25(circuit_search, ${bm25Weights().join(", ")}), c.name
       LIMIT ?`,
    )
    .all(...params, limit) as Omit<RankedCircuit, "tags">[];

  const ranked = withTags(rows, "circuit") as RankedCircuit[];

  // Strict: parseInt("42abc") would yield 42, making "42abc" an id lookup.
  // Against `raw`, not the corrected text: an id is never a misspelling.
  const idMatch = /^#?(\d+)$/.exec(query.raw.trim());
  if (!idMatch) return ranked;

  // The id hit bypasses the SQL above, so it must honour the active filters too
  // -- otherwise a filter would appear to leak.
  const exact = getRankedByQecId(parseInt(idMatch[1], 10));
  if (!exact) return ranked;
  if (opts.codeId != null && exact.code_id !== opts.codeId) return ranked;
  if (!(opts.tags ?? []).every((t) => exact.tags.includes(t))) return ranked;

  return [exact, ...ranked.filter((c) => c.id !== exact.id)].slice(0, limit);
}

function getRankedByQecId(qecId: number): RankedCircuit | null {
  const db = getDb();
  const row = db
    .prepare(
      `SELECT ${RANKED_COLUMNS} FROM circuits c
       JOIN codes co ON co.id = c.code_id WHERE c.qec_id = ?`,
    )
    .get(qecId) as Omit<RankedCircuit, "tags"> | undefined;
  return row ? ((withTags([row], "circuit")[0] ?? null) as RankedCircuit | null) : null;
}
