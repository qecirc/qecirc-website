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

-- The spelling dictionary behind typo tolerance, kept SEPARATE from
-- circuit_search on two counts.
--
-- Unstemmed: fts5vocab reports the terms as indexed, and porter indexes stems
-- -- "steane" is stored as "stean", "preparation" as "prepar". Correcting a
-- typo against those would suggest non-words. Indexing the same text unstemmed
-- keeps candidates real words; porter then stems the corrected word at query
-- time anyway, so it still matches.
--
-- Wider than circuits: this also feeds the header quick-search (/api/search),
-- which covers codes and tools. Those appear in circuit_search only incidentally
-- (a code via code_name, a tool not at all), so a dictionary built from circuits
-- alone cannot fix "autqce" -> "autqec" for a tool that has contributed no
-- circuits. Every entity name and tag is indexed here.
--
-- content='' makes it contentless: FTS5 keeps only the term index and drops the
-- text, which is all a dictionary needs.
CREATE VIRTUAL TABLE search_terms USING fts5(
  text,
  tokenize = 'unicode61 remove_diacritics 2',
  content = ''
);

CREATE VIRTUAL TABLE search_vocab USING fts5vocab(search_terms, 'row');
