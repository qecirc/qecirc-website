import type { CircuitSortField, CodeSortField } from "../types";

export const CIRCUIT_SORT_FIELDS: readonly CircuitSortField[] = [
  "qubit_count",
  "depth",
  "gate_count",
  "two_qubit_gate_count",
  "weight",
];

export const CODE_SORT_FIELDS: readonly CodeSortField[] = ["n", "k", "d"];

export const FILTER_PART_REGEX = /^(!=|>=|<=|>|<|=)?\s*(\d+)$/;

// Codes carrying this tag are hidden by default: excluded from the /codes
// listing (until the tag is explicitly selected in the filter) and from every
// displayed code/circuit count. They stay fully searchable and their detail
// pages stay reachable — hiding governs discovery surfaces, not existence.
// Applied to the codetables.de best-known-distance sweep (mostly anonymous
// record-holder codes) so it doesn't drown the curated library.
export const HIDDEN_CODE_TAG = "codetables";

// Shared tab-toggle styling (FormatSwitcher, CodeMatrices). Compose with any
// component-specific base classes (e.g. `format-tab`, `code-matrix-toggle`,
// focus rings) at the call site. Both carry border-b-2 so switching tabs
// never shifts the layout: the active tab underlines, it does not fill —
// a solid ink block read heavier than the content it labelled.
export const TAB_ACTIVE_CLASS =
  "text-gray-900 dark:text-gray-100 border-b-2 border-gray-900 dark:border-gray-100";
export const TAB_INACTIVE_CLASS =
  "text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 border-b-2 border-transparent";

// Tag styling shared by the client-side filter (list-filter-client.ts, which
// swaps these at runtime) and the server-rendered markup (TagList.astro,
// TagFilterDropdowns.astro). Defined once here because /search renders the
// selected state on the server while /codes leaves it to the client -- the two
// must agree, and they previously only agreed by a comment asking them to.
export const TAG_SELECTED =
  "bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-700 dark:hover:bg-gray-300";
export const TAG_UNSELECTED =
  "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:underline";

export const DROPDOWN_ENTRY_SELECTED = TAG_SELECTED;
export const DROPDOWN_ENTRY_UNSELECTED =
  "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800";

export const SUMMARY_SELECTED = `${TAG_SELECTED} font-semibold`;
export const SUMMARY_UNSELECTED = `${TAG_UNSELECTED} font-medium`;

// Hard ceiling on how many circuit ids one `/api/circuits?ids=` request may
// name, and on the `IN (...)` list `getCircuitsByQecIds` builds from them.
//
// It was 200, "to prevent abuse", and it truncated in silence: a reader with
// more than 200 favourites saw the first 200 and nothing said so. That is not a
// URL-length guard -- 200 four-digit ids is ~1000 characters -- and the library
// already holds ~1000 circuits, so favouriting everything showed a fifth of it.
// The cap stays, because an unbounded id list is a real way to make the server
// build an arbitrarily large query, but it now sits above the whole library
// with room to grow. Truncation is reported (`X-Truncated`) rather than hidden.
//
// It is also below what would break the request itself: 2000 ids is ~10 KB of
// query string, inside Node's 16 KB header limit.
export const MAX_CIRCUIT_IDS_PER_REQUEST = 2_000;

export const HEART_PATH =
  "M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z";

// Above this many entries in the symplectic `h`, a code's matrices are offered
// as a download instead of being rendered inline. `h` is (n-k) x 2n, so the
// payload and the render cost both grow as n^2: the quasi-cyclic lifted product
// code [[1428,184]] is 3.6M entries and ~14 MB of JSON, which no browser should
// be asked to lay out inside a <pre>. The limit sits comfortably above the
// largest inline code the library had before qLDPC codes arrived (the
// unrotated surface code [[221,1,11]], ~97k entries).
export const MATRIX_INLINE_ENTRY_LIMIT = 300_000;

// Entries in the stored `h` for an [[n,k,d]] code, assuming the n-k independent
// stabilizer generators a stabilizer code has. Used only to choose between the
// inline and download views, so an estimate is enough — it never has to load
// the matrix it is sizing.
export function matrixEntryEstimate(n: number, k: number): number {
  return Math.max(0, n - k) * 2 * n;
}
