export function safeParseMatrix(json: string | null): number[][] | null {
  if (!json) return null;
  try {
    return JSON.parse(json);
  } catch {
    return null;
  }
}
