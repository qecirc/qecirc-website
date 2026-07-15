-- Full-text search index backing /search, ranked by BM25.
--
-- Circuits only: with 38 codes and 10 tools, the header quick-search already
-- covers those; circuits are the only entity numerous enough to need ranking.
--
-- BM25 (rather than hand-rolled LIKE + CASE scoring) because `notes` is largely
-- repeated boilerplate -- e.g. "Created using the `synthesize_encoding_circuit`
-- function in mqt.qecc" recurs across many circuits. BM25's inverse document
-- frequency demotes such common terms automatically, which weighted rules
-- cannot do. Circuit names also collide heavily across codes ("QECC Encoding"),
-- so ties need code_name/notes to break them.
--
-- Plain (not external-content) FTS5 tables: scripts/db/create_database.mjs
-- rebuilds the whole DB from YAML on every build and populates these at the
-- end, so there is no incremental sync to keep correct and no triggers.

-- `porter` stems on both sides of the match, so "encodings", "encode" and
-- "encoding" all meet at one term, as do "preparing"/"preparation".
CREATE VIRTUAL TABLE circuit_search USING fts5(
  circuit_id UNINDEXED,
  name,
  code_name,
  tags,
  notes,
  tokenize = 'porter unicode61 remove_diacritics 2'
);

-- The spelling dictionary for /search's "did you mean", kept SEPARATE from
-- circuit_search on purpose: fts5vocab reports the terms as indexed, and
-- porter indexes stems -- "steane" is stored as "stean", "preparation" as
-- "prepar". Correcting a typo against those would suggest non-words. This twin
-- indexes the same text unstemmed, so candidates are real words; porter then
-- stems the corrected word at query time anyway, so it still matches.
--
-- content='' makes it contentless: FTS5 keeps only the term index and drops the
-- text, which is all a dictionary needs.
CREATE VIRTUAL TABLE circuit_terms USING fts5(
  text,
  tokenize = 'unicode61 remove_diacritics 2',
  content = ''
);

CREATE VIRTUAL TABLE circuit_vocab USING fts5vocab(circuit_terms, 'row');
