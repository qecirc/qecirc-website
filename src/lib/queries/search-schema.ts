// The two facts about `circuit_search` that must track its column list, derived
// from the table itself rather than restated by hand.
//
// Both were hand-maintained before, and both drifted -- in the same week, in two
// different branches, despite the comment on each shouting about it:
//
//   * BM25_WEIGHTS was left at 7 entries when an 8th column was added. FTS5
//     silently defaults the rest to 1.0 rather than erroring, so `paper` quietly
//     took the weight meant for `notes`. It only escaped notice because the two
//     happened to want the same number.
//   * STRICT_COLUMNS was missing `paper`, so an exact author match ("forlivesi")
//     failed the strict rung and got reported to the user as a loose `related`
//     fallback -- "no code goes by that name here" for a name that was right.
//
// A comment that is ignored twice is not a control. `PRAGMA table_info` returns
// the real columns in declaration order, which is exactly what BM25 wants, so
// the array is built from the table and a missing weight is a loud error naming
// the column instead of a silent mis-ranking.

import { getDb } from "../db";

/** Weight per column, BY NAME. Order here is irrelevant -- position comes from
 *  the table. Every column of circuit_search must appear, or building the array
 *  throws.
 *
 * `circuit_id` is UNINDEXED and scores nothing; it takes 0.0 because FTS5 still
 * counts it as a column.
 *
 * `name` dominates: a circuit's own name is the sharpest thing about it.
 * `tags` (6.0) beat `code_name`/`aliases`/`code_tags` (4.0): a circuit's own tag
 * distinguishes it from its siblings, while facts about its code are shared by
 * every circuit under that code. An alias IS a code name, so it matches
 * code_name exactly -- "laflamme" should rank a five-qubit circuit as
 * "five-qubit" does.
 *
 * `related` (0.5) sits lowest: it only ever decides a query nothing else
 * answered, and when it does every hit comes through it, so its weight orders
 * nothing. Low means a circuit matching real text still outranks a loose match.
 *
 * `paper` (1.0) is deliberately as low as `notes`, which is counter-intuitive --
 * a title looks like a stronger signal than boilerplate. It is not:
 *   1. the text is identical across every circuit from that paper (370 for the
 *      largest), so it never distinguishes between them; and
 *   2. it is a SHORT field (~25 tokens), and BM25 already normalizes term
 *      frequency by field length, so a hit there outscores the same hit in long
 *      `notes` before any weight applies. Weighting it up double-counts that.
 * Measured at 3.0: all 20 of the top 20 for "fault tolerant" were circuits
 * tagged `non-ft` -- baselines from papers whose TITLES say fault-tolerant,
 * beating the genuinely FT circuits whose notes say so. At 1.0: none. Weights
 * reorder, they never filter, so no title query loses a hit. Re-check that query
 * if you raise this.
 */
const COLUMN_WEIGHTS: Record<string, number> = {
  circuit_id: 0.0,
  name: 10.0,
  code_name: 4.0,
  aliases: 4.0,
  related: 0.5,
  tags: 6.0,
  code_tags: 4.0,
  paper: 1.0,
  notes: 1.0,
};

/** Columns matched only as a last resort, which `/search` then owns up to.
 *
 * `related` names a DIFFERENT, adjacent code ("toric" for a planar surface
 * code); treating a hit there as an exact answer would assert something untrue.
 * Everything else indexed is strict. New columns are strict BY DEFAULT, which is
 * the safe direction: the failure mode of wrongly-strict is a hit ranked
 * normally, while wrongly-loose tells the user their exact query found nothing.
 */
const LOOSE_COLUMNS = new Set(["related"]);

/** UNINDEXED, so FTS5 rejects it inside a column filter. */
const UNINDEXED_COLUMNS = new Set(["circuit_id"]);

let cache: { weights: number[]; strict: string } | null = null;

/** Read the columns as declared, in order. The DB is baked at build time and
 *  immutable for the life of the process, so this runs once. */
function columns(): string[] {
  return (getDb().prepare("PRAGMA table_info(circuit_search)").all() as { name: string }[]).map(
    (r) => r.name,
  );
}

function build(): { weights: number[]; strict: string } {
  const cols = columns();

  const missing = cols.filter((c) => !(c in COLUMN_WEIGHTS));
  if (missing.length > 0) {
    throw new Error(
      `circuit_search has column(s) with no BM25 weight: ${missing.join(", ")}. ` +
        `Add them to COLUMN_WEIGHTS in queries/search-schema.ts. (Left unset, FTS5 ` +
        `would silently score them 1.0 and mis-rank every result.)`,
    );
  }
  const stale = Object.keys(COLUMN_WEIGHTS).filter((c) => !cols.includes(c));
  if (stale.length > 0) {
    throw new Error(
      `COLUMN_WEIGHTS names column(s) that circuit_search does not have: ${stale.join(", ")}. ` +
        `Drop them, or fix the CREATE in the latest migration.`,
    );
  }

  // Positional, in declaration order -- which is what bm25() expects.
  const weights = cols.map((c) => COLUMN_WEIGHTS[c]);

  const strictCols = cols.filter((c) => !LOOSE_COLUMNS.has(c) && !UNINDEXED_COLUMNS.has(c));
  return { weights, strict: `{${strictCols.join(" ")}}` };
}

function schema(): { weights: number[]; strict: string } {
  if (cache === null) cache = build();
  return cache;
}

/** BM25 weights, one per column, in the table's own order. */
export function bm25Weights(): number[] {
  return schema().weights;
}

/** FTS5 column-filter for the strict rungs of resolveQuery, e.g.
 *  `{name code_name aliases tags code_tags paper notes}`. */
export function strictColumns(): string {
  return schema().strict;
}
