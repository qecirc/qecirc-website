/**
 * Matching a circuit's `source` to a paper in data_yaml/papers/.
 *
 * Shared by scripts/db/create_database.mjs (which does the linking) and
 * scripts/validate-yaml.mjs (which reports sources that will not link). The two
 * MUST agree: if validation normalizes differently from the build, it would
 * pass a source the build then silently fails to resolve — the exact failure
 * this file exists to make impossible.
 */

/** Reduce a paper link to a comparison key.
 *
 * A circuit's `source` and a paper's declared `url` are written by different
 * hands at different times, so the same paper arrives spelled several ways:
 * http vs https, a trailing slash, `dx.doi.org` vs `doi.org`, a /pdf/ link
 * instead of /abs/, or an arXiv version suffix (`2402.17761v2`). All of those
 * are the same work and must collapse to one key.
 *
 * The version suffix is stripped for the same reason arXiv treats it as
 * optional: v1 and v2 are the same paper, and a source pinned to v1 should
 * still find it.
 */
export function paperKey(raw) {
  return String(raw)
    .trim()
    .toLowerCase()
    .replace(/^https?:\/\//, "")
    .replace(/^www\./, "")
    .replace(/^dx\.doi\.org\//, "doi.org/")
    .replace(/^arxiv\.org\/pdf\//, "arxiv.org/abs/")
    .replace(/\.pdf$/, "")
    .replace(/\/+$/, "")
    .replace(/^(arxiv\.org\/abs\/.+?)v\d+$/, "$1");
}

/** Every link a paper answers to: its canonical `url` plus the links implied by
 *  its ids. A circuit may cite the arXiv abs page while the paper declares its
 *  journal DOI as canonical (or vice versa), and both must resolve. */
export function paperLinks(data) {
  const links = [];
  if (data.url) links.push(data.url);
  if (data.arxiv_id) links.push(`https://arxiv.org/abs/${data.arxiv_id}`);
  if (data.doi) links.push(`https://doi.org/${data.doi}`);
  return links;
}

/** Whether a `source` is a candidate for paper linking at all. A source that is
 *  not a link names a tool ("circuit-synth"), which is provenance but not a
 *  paper. */
export function isPaperSource(source) {
  return /^https?:\/\//i.test(String(source ?? ""));
}
