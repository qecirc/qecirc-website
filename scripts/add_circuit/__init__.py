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
    validate_state_prep,
    validate_syndrome_extraction,
)
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
from .models import ExtractedCode  # noqa: F401
from .yaml_helpers import (
    build_circuit_yaml,
    build_code_yaml,
    build_original_yaml,
    dump_yaml,
    write_file,
)


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
    data_dir: Union[str, Path] = "data_yaml",
    dry_run: bool = False,
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
        data_dir: Path to data_yaml directory.
        dry_run: If True, report what would be written without writing.

    Returns:
        AddCircuitResult with code/circuit info and list of files written.
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

    # Compute code data
    if css_path:
        code_result = compute_code_data(
            np.asarray(Hx, dtype=int),
            np.asarray(Hz, dtype=int),
            d=d,
            code_name=code_name,
            zoo_url=zoo_url,
            data_dir=data_dir_arg,
        )
    else:
        code_result = compute_code_data_h(
            np.asarray(H, dtype=int),
            n=n,
            d=d,
            code_name=code_name,
            zoo_url=zoo_url,
            data_dir=data_dir_arg,
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
    )

    # Collect files to write
    code_slug = code["slug"]
    circ_slug = circ_data["slug"]
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

    files_to_write.append(
        (
            circuits_dir / f"{stem}.yaml",
            dump_yaml(build_circuit_yaml(circ_data)),
        )
    )

    for body in circ_data.get("bodies", []):
        if body.get("body"):
            files_to_write.append((circuits_dir / f"{stem}.{body['format']}", body["body"]))

    # Original files (pre-canonicalization)
    originals_dir = circuits_dir / "originals"
    if circ_data.get("original_stim"):
        files_to_write.append((originals_dir / f"{stem}.original.stim", circ_data["original_stim"]))
    files_to_write.append(
        (
            originals_dir / f"{stem}.original.yaml",
            dump_yaml(build_original_yaml(original_matrices)),
        )
    )

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
