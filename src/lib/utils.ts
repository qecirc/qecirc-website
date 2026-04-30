/**
 * Parse a JSON-encoded 2D integer matrix.
 *
 * Optional `expectedRows` / `expectedCols` enforce shape. Values are also
 * checked to be finite numbers; symplectic matrices should additionally pass
 * 0/1 — caller can verify post-parse.
 */
export function safeParseMatrix(
  json: string | null | undefined,
  expectedRows?: number,
  expectedCols?: number,
): number[][] | null {
  if (!json) return null;
  let parsed: unknown;
  try {
    parsed = JSON.parse(json);
  } catch {
    return null;
  }
  if (!Array.isArray(parsed)) return null;
  if (expectedRows !== undefined && parsed.length !== expectedRows) return null;
  for (const row of parsed) {
    if (!Array.isArray(row)) return null;
    if (expectedCols !== undefined && row.length !== expectedCols) return null;
    for (const v of row) {
      if (typeof v !== "number" || !Number.isFinite(v)) return null;
    }
  }
  return parsed as number[][];
}

// Convert a symplectic stabilizer matrix (rows × 2n) to Pauli strings.
// Column i is the X-part for qubit i; column i+n is the Z-part for qubit i.
// Each row becomes a string like "X Z Z X I" of length n (single-spaced).
export function symplecticToPauli(matrix: number[][], n: number): string[] {
  return matrix.map((row) => {
    const chars: string[] = [];
    for (let i = 0; i < n; i++) {
      const x = row[i] ?? 0;
      const z = row[i + n] ?? 0;
      chars.push(x && z ? "Y" : x ? "X" : z ? "Z" : "I");
    }
    return chars.join(" ");
  });
}

// Format a matrix as space-padded rows with brackets, e.g. "[ 1  0  1 ]".
// Returns an array of formatted row strings (no trailing newline).
export function formatMatrixRows(matrix: number[][]): string[] {
  const flat = matrix.flat();
  const colWidth = flat.length > 0 ? Math.max(...flat.map((v) => String(v).length)) : 1;
  return matrix.map((row) => `[ ${row.map((v) => String(v).padStart(colWidth, " ")).join("  ")} ]`);
}

// Split a symplectic h (rows × 2n) into (Hx, Hz) when every row is pure-X or
// pure-Z. Returns null if any row mixes X and Z (= not row-CSS). Zero rows are
// dropped. Preserves contributor row order — the ingestion pipeline always
// produces row-CSS h for CSS codes via build_symplectic_h's block stacking.
export function splitHToCss(h: number[][], n: number): { hx: number[][]; hz: number[][] } | null {
  const hx: number[][] = [];
  const hz: number[][] = [];
  for (const row of h) {
    if (row.length !== 2 * n) return null;
    const xPart = row.slice(0, n);
    const zPart = row.slice(n, 2 * n);
    const xZero = xPart.every((v) => v === 0);
    const zZero = zPart.every((v) => v === 0);
    if (xZero && zZero) continue;
    if (zZero) hx.push(xPart);
    else if (xZero) hz.push(zPart);
    else return null;
  }
  return { hx, hz };
}

// Split a 2k × 2n logical matrix produced by build_symplectic_logical into
// (Lx, Lz). Top k rows must be pure-X, bottom k must be pure-Z; returns null
// otherwise (e.g. for non-CSS codes whose logicals carry mixed support).
export function splitLogicalToCss(
  logical: number[][],
  n: number,
  k: number,
): { logicalX: number[][]; logicalZ: number[][] } | null {
  if (logical.length !== 2 * k) return null;
  const logicalX: number[][] = [];
  const logicalZ: number[][] = [];
  for (let i = 0; i < k; i++) {
    const row = logical[i];
    if (row.length !== 2 * n) return null;
    if (!row.slice(n, 2 * n).every((v) => v === 0)) return null;
    logicalX.push(row.slice(0, n));
  }
  for (let i = k; i < 2 * k; i++) {
    const row = logical[i];
    if (row.length !== 2 * n) return null;
    if (!row.slice(0, n).every((v) => v === 0)) return null;
    logicalZ.push(row.slice(n, 2 * n));
  }
  return { logicalX, logicalZ };
}
