# Skipped BB codes — matrices for external equivalence checking

Check matrices of the three bivariate bicycle codes whose autqec circuits are
**not** imported yet (see `../README.md`, "Deliberately skipped"). Regenerate
with `uv run python data-imports/autqec/dump_skipped_bb.py`.

Per code `<slug>` (`90-8-10`, `108-8-10`, `144-12-12`):

| file                               | contents                                                                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `<slug>.autqec.hx.txt` / `.hz.txt` | autqec's BB construction (`examples/bivariate_bicycle_codes/code_data/HX_*.npy`), the labeling the autqec circuits act on |
| `<slug>.stored.hx.txt` / `.hz.txt` | the QECirc library code (CSS split of `data_yaml/codes/<slug>.yaml`), the labeling circuits must be relabeled to          |

Format: dense 0/1 matrices, one stabilizer generator per row, entries
space-separated. All six codes are CSS, so `Hx`/`Hz` describe them fully.

Notes for the comparison:

- **Row counts differ by design.** The autqec matrices are the full redundant
  BB check matrices (n/2 rows each, rank (n−k)/2); the stored ones are
  rank-reduced. Row _spaces_ are what must match.
- **The question per code:** is there a qubit permutation σ (S_n acting on
  columns) with σ(rowspace(autqec Hx)) = rowspace(stored Hx) and likewise for
  Hz? Also worth trying σ composed with an X↔Z swap (Hx↔Hz), since BB codes
  are self-dual up to transposition.
- **What is already known** (computed during the import attempt):
  - `90-8-10`: **inequivalent as CSS codes.** The stored code's Hx row space
    has 90 weight-4 and 600 weight-6 codewords; autqec's has 0 weight-4 and
    45 weight-6 (weight enumerators are permutation invariants). Checking
    equivalence under something weaker (e.g. full symplectic equivalence) is
    the open question.
  - `108-8-10`, `144-12-12`: low-weight enumerators of all four spaces match
    (X and Z, both sides), so they are plausibly permutation-equivalent — the
    explicit σ is what's missing.
