"""
Public API for adding circuits to the QECirc library.

Usage:
    from scripts.add_circuit import add_circuit, check_code, summarize_circuit

    # Inspect your code
    print(check_code(Hx, Hz, d=3))

    # Inspect your circuit
    print(summarize_circuit(stim_circuit))

    # Add to library
    result = add_circuit(
        Hx=Hx, Hz=Hz, circuit=stim_circuit,
        circuit_name="Standard Encoding", d=3,
        code_name="Steane Code",
    )
    print(result.summary())
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

import numpy as np
import stim

from .circuit_validate import (  # noqa: F401
    extract_code,
    validate_encoding,
    validate_encoding_h,
    validate_state_prep,
    validate_state_prep_h,
    validate_syndrome_extraction,
)
from .code_identify import gf2_row_basis
from .compute import compute_code_data, compute_code_data_h
from .compute_circuit import compute_circuit_data
from .helpers import (  # noqa: F401
    ExistingCodeMatch,
    check_code,
    check_code_h,
    find_existing_code,
    find_existing_code_full,
    find_existing_code_h,
    preview_circuit,
    summarize_circuit,
)
from .ids import next_qec_id
from .matrix_format import decode as decode_matrix
from .models import ExtractedCode  # noqa: F401
from .yaml_helpers import (
    build_circuit_yaml,
    build_code_yaml,
    build_original_yaml,
    dump_yaml,
    load_yaml,
    matrices_digest,
    write_file,
)


class UncertainDedupError(Exception):
    """Raised by :func:`add_circuit` when the submission's invariants match
    one or more stored codes but permutation-equivalence could not be
    confirmed within the search budget.

    To proceed, the caller can either:
      - pass ``assume_new=True`` to add the submission as a new code, or
      - reformulate Hx/Hz (or H) to match the stored form of one of the
        candidate slugs.
    """

    def __init__(self, candidates: list[str], n: int, k: int):
        self.candidates = list(candidates)
        self.n = n
        self.k = k
        super().__init__(
            f"Submission has [[{n},{k}]] parameters and invariants matching "
            f"stored code(s) {self.candidates}, but a qubit permutation could "
            f"not be confirmed within the search budget. Either pass "
            f"`assume_new=True` to add as a new code, or reformulate the "
            f"matrices to match the stored form of one of the candidates."
        )


def _rowspace(M: np.ndarray) -> np.ndarray:
    return gf2_row_basis(np.asarray(M, dtype=int) % 2)


def _find_code_by_matrices(data_dir: Optional[str], n: int, H_perm: np.ndarray) -> Optional[str]:
    """Return the slug of the stored ``[[n,...]]`` code whose stabilizer group has
    the same GF(2) row space as ``H_perm`` (a symplectic ``(m, 2n)`` matrix in the
    stored labeling), or ``None``. A direct code-equality test in a fixed
    labeling — no permutation search, and independent of how the stored
    ``canonical_hash`` was computed."""
    if not data_dir:
        return None

    target = _rowspace(H_perm)
    for path in sorted((Path(data_dir) / "codes").glob("*.yaml")):
        doc = load_yaml(path.read_text())
        if not doc or doc.get("n") != n:
            continue
        stored_h = decode_matrix(doc["h"])
        if stored_h.shape[1] != 2 * n:
            continue
        if target.shape == _rowspace(stored_h).shape and np.array_equal(
            target, _rowspace(stored_h)
        ):
            return path.stem
    return None


def _resolve_with_permutation(
    code_result: dict,
    sigma: list[int],
    *,
    css_path: bool,
    Hx,
    Hz,
    H,
    n: Optional[int],
    data_dir: Optional[str],
) -> None:
    """Adopt a caller-supplied qubit permutation ``sigma`` (convention
    ``sigma[new] = old``) instead of the dedup search.

    Relabels the submission's columns by ``sigma`` and checks the result is the
    same stabilizer code (equal GF(2) row space) as a stored code — a direct
    equality test in the fixed stored labeling, so it works even for
    automorphism-rich codes whose ``canonical_hash`` is not a true permutation
    invariant. Rewrites ``code_result`` in place to a confirmed match under that
    code's slug. Raises ``ValueError`` if ``sigma`` is not a valid permutation or
    does not land on any stored code.
    """
    nn = code_result["code"]["n"]
    if sorted(sigma) != list(range(nn)):
        raise ValueError(f"qubit_permutation must be a permutation of 0..{nn - 1}, got {sigma!r}.")

    if css_path:
        pHx = np.asarray(Hx, dtype=int)[:, sigma]
        pHz = np.asarray(Hz, dtype=int)[:, sigma]
        from .code_identify import build_symplectic_h

        H_perm = build_symplectic_h(pHx, pHz)
    else:
        cols = list(sigma) + [s + nn for s in sigma]
        H_perm = np.asarray(H, dtype=int)[:, cols]

    slug = _find_code_by_matrices(data_dir, nn, H_perm)
    if slug is None:
        raise ValueError(
            "supplied qubit_permutation does not map the submission onto any "
            "stored code. Check the permutation, its orientation (sigma[new] = "
            "old), or seed the code."
        )

    code_result["code"]["status"] = "existing"
    code_result["code"]["slug"] = slug
    code_result["qubit_permutation"] = sigma
    code_result["dedup_status"] = "match"
    code_result["uncertain_candidates"] = []


@dataclass
class AddCircuitResult:
    """Result of adding a circuit to the library."""

    code_name: str
    code_slug: str
    code_status: str  # "new" | "existing"
    circuit_name: str
    circuit_slug: str
    files_written: list[str] = field(default_factory=list)
    dry_run: bool = False
    qubit_permutation: list[int] | None = None

    def summary(self) -> str:
        lines = [
            f"Code: {self.code_name} [{self.code_status}]",
            f"Circuit: {self.circuit_name}",
        ]
        if self.qubit_permutation is not None:
            lines.append(f"Qubit permutation applied: {self.qubit_permutation}")
        if self.dry_run:
            lines.append(f"Dry run — {len(self.files_written)} file(s) would be written:")
        else:
            lines.append(f"{len(self.files_written)} file(s) written:")
        for f in self.files_written:
            lines.append(f"  {f}")
        if not self.dry_run:
            lines.append("\nRun 'npm run db:create && npm run dev' to rebuild the database.")
        return "\n".join(lines)


def add_circuit(
    circuit: Union[stim.Circuit, str],
    circuit_name: str,
    d: int,
    *,
    Hx: Optional[np.ndarray] = None,
    Hz: Optional[np.ndarray] = None,
    H: Optional[np.ndarray] = None,
    n: Optional[int] = None,
    source: str = "",
    code_name: str = "",
    zoo_url: str = "",
    tool: str = "",
    notes: str = "",
    tags: Optional[list[str]] = None,
    data_dir: Union[str, Path] = "data_yaml",
    dry_run: bool = False,
    assume_new: bool = False,
    overwrite: bool = False,
    qubit_permutation: Optional[list[int]] = None,
    code_slug: str = "",
    code_tags: Optional[list[str]] = None,
) -> AddCircuitResult:
    """
    Add a circuit to the QECirc library by writing YAML files to data_yaml/.

    Two ways to specify the code (convenience only — both paths reduce to the
    symplectic ``h`` and ``logical`` matrices that are persisted to YAML):
      * CSS path: pass ``Hx`` and ``Hz`` (must satisfy Hx · Hzᵀ = 0 mod 2). The
        pipeline builds h via :func:`build_symplectic_h` before storage.
      * General path: pass ``H`` (symplectic stabilizer matrix of shape
        ``(m, 2n)``) along with ``n``. CSS-decomposable H is auto-detected
        and the ``CSS`` tag is set; the Hx/Hz view is reconstructed in the UI.

    Args:
        circuit: STIM circuit (stim.Circuit object or string).
        circuit_name: Name for the circuit (e.g. "Standard Encoding").
        d: Code distance.
        Hx: X-check matrix (CSS path).
        Hz: Z-check matrix (CSS path).
        H: Symplectic stabilizer matrix (general path).
        n: Number of physical qubits (required with H).
        source: Provenance (DOI, URL, or citation).
        code_name: Name for the code. Optional if code already exists in data_yaml/.
        zoo_url: QEC Zoo URL for the code.
        tool: Tool slug (e.g. "mqt-qecc").
        notes: Circuit notes.
        tags: Circuit tags written to the YAML (e.g. ``["encoding", "non-ft"]``).
            The functionality tag (``encoding`` / ``state-preparation``) drives
            circuit-type routing in ``validate:circuits``; fault tolerance
            (``ft`` / ``non-ft``) is never inferred, so pass it explicitly.
        data_dir: Path to data_yaml directory.
        dry_run: If True, report what would be written without writing.
        assume_new: If True, suppress :exc:`UncertainDedupError` and add as a
            new code even when invariants align with stored candidates.
        overwrite: If a circuit with the same ``<code>--<circuit>`` slug already
            exists, ``False`` (the default) raises :exc:`FileExistsError` rather
            than silently clobbering it; ``True`` replaces it in place, keeping
            the existing ``qec_id`` so the public ``#N`` identifier is stable.
        code_slug: Explicit slug for a *new* code, overriding
            ``slugify(code_name)``. Lets new codes follow the numeric ``n-k-d``
            convention (e.g. ``9-1-3-surface``) while the display ``name`` may
            repeat across sizes. Ignored for existing codes (the stored slug is
            authoritative).
        code_tags: Family tags for a *new* code (e.g. ``["surface-code"]``),
            merged with the auto-derived ``CSS`` / ``self-dual`` tags. Ignored for
            existing codes.
        qubit_permutation: A caller-supplied permutation (convention
            ``sigma[new] = old``) that relabels the submission onto a stored
            code. When given, it replaces the automatic dedup search: the
            permutation is verified by row-space equality against the stored code
            (so it works for automorphism-rich codes where the search times out)
            and applied to the circuit. Raises :exc:`ValueError` if it is not a
            valid permutation or does not land on a stored code.

    Returns:
        AddCircuitResult with code/circuit info and list of files written.

    Raises:
        UncertainDedupError: when invariants match one or more stored codes
            but a qubit permutation cannot be confirmed within the search
            budget, and ``assume_new`` is False.
    """
    css_path = Hx is not None and Hz is not None
    h_path = H is not None and n is not None
    if css_path == h_path:
        raise ValueError("Provide exactly one of (Hx, Hz) or (H, n) to specify the code.")

    if isinstance(circuit, stim.Circuit):
        circuit_text = str(circuit)
    else:
        circuit_text = circuit

    data_dir = Path(data_dir)
    data_dir_arg = str(data_dir) if data_dir.exists() else None
    # When a permutation is supplied, _resolve_with_permutation does its own
    # (single) code scan, so skip compute_code_data's dedup scan entirely.
    dedup_dir = None if qubit_permutation is not None else data_dir_arg

    # Compute code data
    if css_path:
        code_result = compute_code_data(
            np.asarray(Hx, dtype=int),
            np.asarray(Hz, dtype=int),
            d=d,
            code_name=code_name,
            zoo_url=zoo_url,
            data_dir=dedup_dir,
            code_slug=code_slug,
            code_tags=code_tags,
        )
    else:
        code_result = compute_code_data_h(
            np.asarray(H, dtype=int),
            n=n,
            d=d,
            code_name=code_name,
            zoo_url=zoo_url,
            data_dir=dedup_dir,
            code_slug=code_slug,
            code_tags=code_tags,
        )

    # A caller-supplied qubit permutation short-circuits the (possibly
    # budget-limited) automatic dedup search: verify it maps the submission onto
    # a stored code and adopt it directly. Useful for automorphism-rich codes
    # where find_qubit_permutation cannot confirm equivalence in time.
    if qubit_permutation is not None:
        _resolve_with_permutation(
            code_result,
            list(qubit_permutation),
            css_path=css_path,
            Hx=Hx,
            Hz=Hz,
            H=H,
            n=n,
            data_dir=data_dir_arg,
        )

    # Surface uncertain dedup to the caller before doing any further work.
    if code_result.get("dedup_status") == "uncertain" and not assume_new:
        raise UncertainDedupError(
            candidates=code_result.get("uncertain_candidates", []),
            n=code_result["code"]["n"],
            k=code_result["code"]["k"],
        )

    code = code_result["code"]
    perm = code_result["qubit_permutation"]
    original_matrices = code_result["original_matrices"]

    # Compute circuit data
    circ_data = compute_circuit_data(
        circuit_text=circuit_text,
        qubit_permutation=perm,
        circuit_name=circuit_name,
        source=source,
        tool=tool,
        notes=notes,
        tags=tags,
    )

    # Collect files to write
    code_slug = code["slug"]
    circ_slug = circ_data["slug"]
    circ_yaml_path = data_dir / "circuits" / f"{code_slug}--{circ_slug}.yaml"

    # Guard against silently overwriting a different circuit that shares the
    # same <code>--<circuit> slug (e.g. two distinct constructions of the same
    # code submitted under the same circuit name). On a real write we refuse
    # unless `overwrite=True`; when overwriting we reuse the existing qec_id so
    # the public #N identifier is stable rather than being reallocated.
    existing_qec_id = None
    if circ_yaml_path.exists():
        if not dry_run and not overwrite:
            raise FileExistsError(
                f"circuit '{code_slug}--{circ_slug}' already exists at "
                f"{circ_yaml_path}. Pass overwrite=True to replace it, or use a "
                f"distinct circuit_name."
            )
        prev = load_yaml(circ_yaml_path.read_text())
        if prev and isinstance(prev.get("qec_id"), int):
            existing_qec_id = prev["qec_id"]
    circ_data["qec_id"] = existing_qec_id or next_qec_id(data_dir)

    files_to_write: list[tuple[Path, str]] = []

    if code.get("status") == "new":
        files_to_write.append(
            (
                data_dir / "codes" / f"{code_slug}.yaml",
                dump_yaml(build_code_yaml(code)),
            )
        )

    stem = f"{code_slug}--{circ_slug}"
    circuits_dir = data_dir / "circuits"
    matrices_dir = data_dir / "matrices"

    # Built before the originals block so the matrices reference can be added to
    # it, and dumped after, once that reference is known.
    circuit_yaml = build_circuit_yaml(circ_data)

    for body in circ_data.get("bodies", []):
        if body.get("body"):
            files_to_write.append((circuits_dir / f"{stem}.{body['format']}", body["body"]))

    # Original files (pre-canonicalization).
    #
    # The original *circuit* is per circuit, so it stays beside it. The original
    # *matrices* are a property of the code and the labelling it was submitted
    # in, so every circuit of one code writes the same bytes — and for a large
    # qLDPC code those bytes are megabytes. They are stored once, content
    # addressed, and referenced from the circuit YAML instead.
    originals_dir = circuits_dir / "originals"
    if circ_data.get("original_stim"):
        files_to_write.append((originals_dir / f"{stem}.original.stim", circ_data["original_stim"]))

    original_yaml = build_original_yaml(original_matrices)
    if original_yaml:
        digest = matrices_digest(original_yaml)
        circuit_yaml["original_matrices"] = digest
        files_to_write.append((matrices_dir / f"{digest}.yaml", dump_yaml(original_yaml)))

    files_to_write.append((circuits_dir / f"{stem}.yaml", dump_yaml(circuit_yaml)))

    # Write or dry-run
    written_paths: list[str] = []
    for fpath, content in files_to_write:
        written_paths.append(str(fpath))
        if not dry_run:
            write_file(fpath, content, quiet=True)

    return AddCircuitResult(
        code_name=code["name"],
        code_slug=code_slug,
        code_status=code["status"],
        circuit_name=circ_data["name"],
        circuit_slug=circ_slug,
        files_written=written_paths,
        dry_run=dry_run,
        qubit_permutation=perm,
    )


# State-preparation ingestion helpers (derive/validate/fit a code from a prep
# circuit). Imported at the end so `add_circuit` is already defined for the
# lazy import inside `import_state_prep`.
from .perm_find import find_code_permutation  # noqa: E402
from .state_prep import (  # noqa: E402
    FitResult,
    anchor_h_in_circuit_labeling,
    derive_matrices_self_dual,
    derive_matrices_two_circuit,
    fit_circuit_to_anchor,
    fit_circuit_to_anchor_h,
    fit_circuit_to_candidates,
    import_state_prep,
    logical_basis_of,
    logical_state_of,
    strip_flags,
    symplectic_validate,
)

__all__ = [  # noqa: F822  (names defined above / re-exported)
    "add_circuit",
    "AddCircuitResult",
    "UncertainDedupError",
    "check_code",
    "check_code_h",
    "find_existing_code",
    "find_existing_code_full",
    "find_existing_code_h",
    "preview_circuit",
    "summarize_circuit",
    "validate_encoding",
    "validate_encoding_h",
    "validate_state_prep",
    "validate_state_prep_h",
    "validate_syndrome_extraction",
    "extract_code",
    "ExtractedCode",
    "ExistingCodeMatch",
    # state_prep re-exports
    "strip_flags",
    "derive_matrices_self_dual",
    "derive_matrices_two_circuit",
    "symplectic_validate",
    "logical_state_of",
    "logical_basis_of",
    "fit_circuit_to_anchor",
    "fit_circuit_to_anchor_h",
    "fit_circuit_to_candidates",
    "anchor_h_in_circuit_labeling",
    "FitResult",
    "import_state_prep",
    # perm_find re-exports
    "find_code_permutation",
]
