-- Code tags reach /search.
--
-- `circuit_search.tags` is built from taggings where taggable_type = 'circuit',
-- so tags attached to a CODE never entered the index at all. Every one of
-- `LDPC`, `topological`, `self-dual`, `surface-code` and `color-code` is a code
-- tag, and each matched exactly zero circuits -- while 4 codes are tagged LDPC
-- and 10 are tagged surface-code.
--
-- It failed silently rather than loudly: `search_terms` DOES index code tags
-- (create_database.mjs adds a row per code), so `correctTokens` sees
-- "topological" as a real term, declines to correct it, and the strict rung
-- returns nothing. A typo would have been rescued; a correct word was not.
--
-- A SEPARATE COLUMN, not folded into `tags`. Today no tag name is used on both a
-- code and a circuit, so folding would not actually double-count -- but nothing
-- enforces that, and the day someone tags a circuit `topological` the term would
-- appear twice in one column and inflate its own term frequency. A code tag also
-- is not the same claim as a circuit tag: it describes the code the circuit
-- belongs to, exactly like code_name does, and is weighted to match.
DROP TABLE circuit_search;

CREATE VIRTUAL TABLE circuit_search USING fts5(
  circuit_id UNINDEXED,
  name,
  code_name,
  aliases,
  related,
  tags,
  code_tags,
  paper,
  notes,
  tokenize = 'porter unicode61 remove_diacritics 2'
);
