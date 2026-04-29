export function safeParseMatrix(json: string | null): number[][] | null {
  if (!json) return null;
  try {
    return JSON.parse(json);
  } catch {
    return null;
  }
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

// True iff the code carries the CSS view (separate hx/hz). Used by pages to
// pick between MatrixDisplay (CSS) and StabilizerDisplay (general symplectic).
export function isCSSView(code: { hx: string | null; hz: string | null }): boolean {
  return code.hx !== null && code.hz !== null;
}

// Format a matrix as space-padded rows with brackets, e.g. "[ 1  0  1 ]".
// Returns an array of formatted row strings (no trailing newline). Used by
// MatrixDisplay and StabilizerDisplay.
export function formatMatrixRows(matrix: number[][]): string[] {
  const flat = matrix.flat();
  const colWidth = flat.length > 0 ? Math.max(...flat.map((v) => String(v).length)) : 1;
  return matrix.map((row) => `[ ${row.map((v) => String(v).padStart(colWidth, " ")).join("  ")} ]`);
}
