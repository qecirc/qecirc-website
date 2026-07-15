-- Alternative names for codes and tools.
--
-- Codes have many names and the catalogue stores one, so every other name a
-- reader might type was a dead query: "laflamme", "checkerboard", "toric" and
-- "kitaev" all returned nothing, and "bb codes" returned 824 of 833 circuits --
-- `bb` matched nothing, the AND found zero, and the OR fallback then matched
-- `codes` almost everywhere. None of these are typos, so migration 016's
-- spelling layer could not reach them: `correctTokens` only rewrites a token
-- that has a near neighbour in the dictionary, and `bb` is two characters, which
-- `editBudget` gives zero edits. This is a data gap, not a tuning problem.
--
-- Two fields, because two different claims:
--
--   aliases -- other names for THIS code. "Laflamme code" IS the five-qubit
--              code; the gross code IS a BB code. Matched silently.
--   related -- names of a DIFFERENT but adjacent code that people use loosely.
--              "toric" strictly means the k=2 code on a torus; ours are planar
--              (k=1). Matched only when nothing else does, and /search says so.
--
-- Names are hand-written, using errorcorrectionzoo.org (which every code already
-- links to via zoo_url) and the papers as reference. NOT imported: eczoo_data is
-- CC-BY-SA 4.0 and this repo is MIT, and a bulk import also drags in taxonomy
-- ancestors -- two hops up from the rotated surface code sits "Quantum Tanner
-- code", which is a parent in a classification, not another name for it.

-- Denormalised onto the entity for the header quick-search, which is LIKE over
-- columns of `codes`/`tools` and has no FTS index to consult. Space-joined text
-- rather than a child table: it is only ever matched as a whole, never queried
-- by individual alias, and `tags` already sets the precedent for the FTS side.
ALTER TABLE codes ADD COLUMN aliases TEXT;
ALTER TABLE codes ADD COLUMN related TEXT;
ALTER TABLE tools ADD COLUMN aliases TEXT;

-- FTS5 has no ALTER TABLE ADD COLUMN, so the index is recreated rather than
-- extended. Safe to drop: it holds no source data. create_database.mjs rebuilds
-- it from `codes`/`circuits` on every build (see 016 -- plain, not
-- external-content, tables), so this is a schema change only.
DROP TABLE circuit_search;

-- `related` is its own column, not folded into `aliases`, so a query can ask for
-- one without the other: /search first matches the strict columns and only
-- retries including `related` when that finds nothing. Column filter syntax
-- ({name code_name aliases tags notes} : ...) needs them separated to do that.
CREATE VIRTUAL TABLE circuit_search USING fts5(
  circuit_id UNINDEXED,
  name,
  code_name,
  aliases,
  related,
  tags,
  notes,
  tokenize = 'porter unicode61 remove_diacritics 2'
);
