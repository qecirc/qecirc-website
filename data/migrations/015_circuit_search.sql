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
-- A plain (not external-content) FTS5 table: scripts/db/create_database.mjs
-- rebuilds the whole DB from YAML on every build and populates this at the end,
-- so there is no incremental sync to keep correct and no triggers are needed.
CREATE VIRTUAL TABLE circuit_search USING fts5(
  circuit_id UNINDEXED,
  name,
  code_name,
  tags,
  notes,
  tokenize = 'unicode61 remove_diacritics 2'
);
