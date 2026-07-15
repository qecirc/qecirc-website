// Typo tolerance for /search and the header quick-search (/api/search), built on
// the unstemmed search_vocab dictionary (data/migrations/016).
//
// Why not spellfix1/editdist3, SQLite's own fuzzy-match extensions: they are
// loadable C extensions, not part of the amalgamation better-sqlite3 ships, so
// using them would mean compiling and shipping a native artifact -- against
// CLAUDE.md's "hosting-agnostic, avoid platform-specific APIs". The dictionary
// is under a thousand terms, so scanning it in JS costs ~0.05 ms and needs
// nothing.

import { getDb } from "../db";

/** Dictionary is derived from the DB, which is baked at build time and
 *  immutable for the life of the process, so it is loaded once. */
let vocabCache: { term: string; doc: number }[] | null = null;

function vocab(): { term: string; doc: number }[] {
  if (vocabCache === null) {
    vocabCache = getDb().prepare("SELECT term, doc FROM search_vocab").all() as {
      term: string;
      doc: number;
    }[];
  }
  return vocabCache;
}

/** How many edits a token of this length may be off by.
 *
 * Mirrors Elasticsearch's "AUTO" fuzziness. Short tokens get no latitude at
 * all: at 2 characters nearly everything is within one edit of everything else,
 * so correcting them turns real queries into noise. */
function editBudget(token: string): number {
  if (token.length <= 2) return 0;
  if (token.length <= 5) return 1;
  return 2;
}

/** Damerau-Levenshtein (optimal string alignment) distance, abandoned as soon
 *  as the best possible result exceeds `max`.
 *
 * Damerau rather than plain Levenshtein because it counts a transposition
 * ("staene" for "steane") as one edit, not two -- transposition is among the
 * most common typing errors, and plain Levenshtein would price it out of a
 * 1-edit budget. */
export function editDistance(a: string, b: string, max: number): number {
  if (Math.abs(a.length - b.length) > max) return max + 1;
  if (a === b) return 0;

  const prev2: number[] = new Array(b.length + 1);
  let prev: number[] = new Array(b.length + 1);
  let curr: number[] = new Array(b.length + 1);
  for (let j = 0; j <= b.length; j++) prev[j] = j;

  let beforePrev: number[] = prev2;
  for (let i = 1; i <= a.length; i++) {
    curr[0] = i;
    let rowMin = curr[0];
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      let v = Math.min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost);
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
        v = Math.min(v, beforePrev[j - 2] + 1);
      }
      curr[j] = v;
      if (v < rowMin) rowMin = v;
    }
    // Every cell in this row is already over budget, and distance never
    // decreases as rows advance, so no completion can come in under it.
    if (rowMin > max) return max + 1;
    const spare = beforePrev;
    beforePrev = prev;
    prev = curr;
    curr = spare;
  }
  return prev[b.length];
}

/** Nearest dictionary word to `token`, or null if nothing is close enough.
 *  Ties go to the more common term -- with no other signal, the word that
 *  appears in more entries is the likelier intent. */
export function nearestTerm(token: string): string | null {
  const max = editBudget(token);
  if (max === 0) return null;

  let best: { term: string; d: number; doc: number } | null = null;
  for (const { term, doc } of vocab()) {
    const d = editDistance(token, term, max);
    if (d > max) continue;
    if (best === null || d < best.d || (d === best.d && doc > best.doc)) {
      best = { term, d, doc };
    }
  }
  return best?.term ?? null;
}

/** Whether the token finds anything as-is. This is the guard that stops us
 *  "correcting" queries that already work, so it has to ask both indexes.
 *
 * circuit_search is porter-stemmed, so "encodings" matches via the stem "encod"
 * even though the unstemmed dictionary holds only "encoding" — asking the
 * dictionary alone would call that a typo and rewrite a fine query.
 *
 * search_terms is unstemmed but covers every entity, including tools that have
 * contributed no circuits and so appear nowhere in circuit_search — asking
 * circuit_search alone would call those names typos and "fix" them into
 * something else.
 *
 * Neither index answers both cases, hence both.
 */
function matchesIndex(expr: string): boolean {
  const db = getDb();
  const inCircuits = db
    .prepare("SELECT 1 FROM circuit_search WHERE circuit_search MATCH ? LIMIT 1")
    .get(expr);
  if (inCircuits !== undefined) return true;
  const inTerms = db
    .prepare("SELECT 1 FROM search_terms WHERE search_terms MATCH ? LIMIT 1")
    .get(expr);
  return inTerms !== undefined;
}

/** Replace tokens that find nothing with their nearest dictionary word.
 *
 * Only such tokens are touched: under AND semantics a single unmatched token
 * empties the whole result set, so this fires exactly when the query is broken
 * and never second-guesses one that works.
 *
 * `isPrefix` marks the token that carries FTS5's `*`, whose findability test
 * has to allow a partial word ("encod" is not a term but does find "encoding").
 */
export function correctTokens(tokens: string[]): { tokens: string[]; changed: boolean } {
  const out: string[] = [];
  let changed = false;

  tokens.forEach((token, i) => {
    // Never touch a token containing a digit. Digits are identifiers and
    // parameters, not prose, and their near neighbours are different things
    // rather than different spellings: "#508" is one edit from "2508" (an arXiv
    // number in some notes), and "distance:3" is one edit from "distance:5".
    // Correcting those does not fix a typo, it answers a different question.
    if (/\d/.test(token)) {
      out.push(token);
      return;
    }
    const isPrefix = i === tokens.length - 1;
    if (matchesIndex(`"${token}"${isPrefix ? "*" : ""}`)) {
      out.push(token);
      return;
    }
    const fixed = nearestTerm(token.toLowerCase());
    if (fixed === null) {
      out.push(token);
      return;
    }
    out.push(fixed);
    changed = true;
  });

  return { tokens: out, changed };
}
