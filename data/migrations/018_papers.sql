-- Papers as first-class entities, so a circuit taken from a paper is findable
-- by the paper's title, authors and arXiv id -- none of which existed anywhere
-- in the library before. `circuits.source` held only a bare URL, which made
-- "2402" a search token but "Zen" or "reinforcement learning" nothing at all.

PRAGMA foreign_keys = OFF;

CREATE TABLE papers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  authors TEXT NOT NULL,
  year INTEGER,
  arxiv_id TEXT,
  doi TEXT,
  journal_ref TEXT,
  url TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
  -- authors: JSON-encoded array of names IN AUTHOR ORDER (not a set) -- the
  --   citation line renders "<first author> et al.", so order is meaning.
  -- arxiv_id: bare id, no "arXiv:" prefix and no version suffix ("2402.17761",
  --   or an old-style "quant-ph/9601029").
  -- url: the canonical link, and the value a circuit's `source` is matched
  --   against. arXiv abs page where there is one, publisher DOI otherwise.
);

-- Nullable on purpose, and NOT a replacement for `source`: a circuit's
-- provenance is sometimes a tool rather than a paper (109 circuits carry
-- `source: circuit-synth`), and such a row has no paper to point at. `source`
-- stays the required, free-form provenance field; paper_id only enriches it
-- where the source resolves to a paper we hold.
--
-- Populated by scripts/db/create_database.mjs, which matches each circuit's
-- `source` against papers.url/arxiv_id/doi. Deliberately not declared in
-- circuit YAML: the link is derivable from `source`, which every circuit
-- already has, so duplicating it across 833 files would only add a second
-- thing to keep in sync.
ALTER TABLE circuits ADD COLUMN paper_id INTEGER REFERENCES papers(id);
CREATE INDEX idx_circuits_paper ON circuits(paper_id);

PRAGMA foreign_keys = ON;

-- circuit_search gains a `paper` column (title + authors + ids). Rebuilt from
-- scratch rather than altered: FTS5 has no ADD COLUMN, and create_database.mjs
-- repopulates the whole index on every build anyway (see migration 016), so
-- dropping it costs nothing. Carries forward 017's aliases/related columns.
--
-- `paper` is its own column rather than text appended to `notes` so it can be
-- weighted independently -- which turned out to matter more than expected. See
-- BM25_WEIGHTS in src/lib/queries/search.ts: it is weighted LOW (1.0), because
-- paper text is short and identical across every circuit from that paper, and a
-- higher weight let 140 `non-ft` circuits top a "fault tolerant" search purely
-- on their paper's title.
--
-- Column order is load-bearing: BM25_WEIGHTS is positional, and `paper` must
-- also be listed in STRICT_COLUMNS (queries/search.ts) or an author search would
-- miss the strict rung and be reported to the user as a `related` fallback.
DROP TABLE circuit_search;

CREATE VIRTUAL TABLE circuit_search USING fts5(
  circuit_id UNINDEXED,
  name,
  code_name,
  aliases,
  related,
  tags,
  paper,
  notes,
  tokenize = 'porter unicode61 remove_diacritics 2'
);
