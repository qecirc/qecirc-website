# Changelog

All notable changes to this project will be documented here. Versioning follows
the source-of-truth `package.json` version.

## Unreleased

### Added

- Non-CSS stabilizer code support throughout the pipeline (symplectic representation).
  Submit codes via `add_circuit(H=..., n=...)` for non-CSS, or the existing
  `Hx`/`Hz` path for CSS.
- New `h` and `logical` columns on `codes`; `original_h` and `original_logical`
  on `circuit_originals` (migration `011_symplectic_storage.sql`).
- New `npm run backfill:symplectic` script for upgrading existing CSS YAMLs.
- Non-CSS code page renders stabilizers and logicals via a Pauli ↔ symplectic
  toggle; CSS pages keep the existing `Hx`/`Hz`/`Logical X`/`Logical Z` view.

### Changed

- **BREAKING:** `add_circuit()` matrix arguments (`Hx`, `Hz`, `H`, `n`) are now
  keyword-only. Migration: replace `add_circuit(Hx, Hz, circuit, name, d, ...)`
  with `add_circuit(circuit=circuit, circuit_name=name, d=d, Hx=Hx, Hz=Hz, ...)`.
- The non-CSS branch of `_compute_logicals` (now `_compute_logicals_css`) was
  mathematically wrong and is replaced by the new `_compute_symplectic_logicals`.
  This affects nobody in practice (the library contained no non-CSS codes), but
  any downstream code calling the old `_compute_logicals(_, _, code_is_css=False, _)`
  must switch to `_compute_symplectic_logicals(H, n, k)`.
