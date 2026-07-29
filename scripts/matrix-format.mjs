/**
 * Reading the two YAML encodings of a binary matrix.
 *
 * The Python side (`scripts/add_circuit/matrix_format.py`) decides which to
 * write: a plain list of rows below a size threshold, and nonzero column
 * indices per row above it, because a code's `h` is (n-k) x 2n and the large
 * qLDPC codes are megabytes of mostly-zero rows otherwise.
 *
 *     h:
 *       rows: 1244
 *       cols: 2856
 *       nonzero:
 *         - [3, 17, 402]
 *
 * The build only ever reads, so this is the decode half plus a shape check for
 * the validator. A list is dense, a mapping is sparse — no flag to keep in sync.
 */

/** True when a stored value looks like a matrix in either encoding. */
export function isMatrix(value) {
  if (Array.isArray(value)) {
    return value.every((row) => Array.isArray(row) && row.every((v) => typeof v === "number"));
  }
  if (value && typeof value === "object") {
    return (
      Number.isInteger(value.rows) &&
      Number.isInteger(value.cols) &&
      Array.isArray(value.nonzero) &&
      value.nonzero.length === value.rows &&
      value.nonzero.every(
        (indices) =>
          Array.isArray(indices) &&
          indices.every((c) => Number.isInteger(c) && c >= 0 && c < value.cols),
      )
    );
  }
  return false;
}

/**
 * A stored matrix as a dense array of 0/1 rows, whichever encoding was used.
 * Returns null for null/undefined so callers can pass optional fields straight
 * through.
 */
export function decodeMatrix(value) {
  if (value == null) return null;
  if (Array.isArray(value)) return value;
  const { cols, nonzero } = value;
  return nonzero.map((indices) => {
    const row = new Array(cols).fill(0);
    for (const c of indices) row[c] = 1;
    return row;
  });
}
