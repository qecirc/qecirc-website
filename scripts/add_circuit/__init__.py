"""
Public API for adding circuits to the QECirc library.

Usage:
    from scripts.add_circuit import add_circuit

    result = add_circuit(
        Hx=Hx,
        Hz=Hz,
        circuit=stim_circuit,
        circuit_name="Standard Encoding",
        source="doi:10.xxxx/yyyy",
        code_name="Steane Code",
    )
    print(result.summary())
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

import numpy as np
import stim

from .compute import compute_code_data
from .compute_circuit import compute_circuit_data
from .yaml_helpers import build_circuit_yaml, build_code_yaml, dump_yaml, write_file


@dataclass
class AddCircuitResult:
    """Result of adding a circuit to the library."""

    code_name: str
    code_slug: str
    code_status: str  # "new" | "existing"
    circuit_name: str
    circuit_slug: str
    validation: str  # "passed" | "skipped" | "failed: ..."
    detected_functionality: Optional[str]
    files_written: list[str] = field(default_factory=list)
    dry_run: bool = False

    def summary(self) -> str:
        lines = [
            f"Code: {self.code_name} [{self.code_status}]",
            f"Circuit: {self.circuit_name}"
            f" ({self.detected_functionality or 'unknown'}) [{self.validation}]",
        ]
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
    Hx: np.ndarray,
    Hz: np.ndarray,
    circuit: Union[stim.Circuit, str],
    circuit_name: str,
    d: int,
    source: str = "",
    code_name: str = "",
    zoo_url: str = "",
    tool: str = "",
    description: str = "",
    data_dir: Union[str, Path] = "data_yaml",
    dry_run: bool = False,
) -> AddCircuitResult:
    """
    Add a circuit to the QECirc library by writing YAML files to data_yaml/.

    Args:
        Hx: X-check matrix as a numpy array.
        Hz: Z-check matrix as a numpy array.
        circuit: STIM circuit (stim.Circuit object or string).
        circuit_name: Name for the circuit (e.g. "Standard Encoding").
        d: Code distance.
        source: Provenance (DOI, URL, or citation).
        code_name: Name for the code. Optional if code already exists in data_yaml/.
        zoo_url: QEC Zoo URL for the code.
        tool: Tool slug (e.g. "mqt-qecc").
        description: Circuit description.
        data_dir: Path to data_yaml directory.
        dry_run: If True, report what would be written without writing.

    Returns:
        AddCircuitResult with code/circuit info and list of files written.
    """
    Hx = np.asarray(Hx, dtype=int)
    Hz = np.asarray(Hz, dtype=int)

    if isinstance(circuit, stim.Circuit):
        circuit_text = str(circuit)
    else:
        circuit_text = circuit

    data_dir = Path(data_dir)

    # Compute code data
    code_result = compute_code_data(
        Hx,
        Hz,
        d=d,
        code_name=code_name,
        zoo_url=zoo_url,
        data_dir=str(data_dir) if data_dir.exists() else None,
    )

    code = code_result["code"]
    perm = code_result["qubit_permutation"]
    code_params = {
        "n": code["n"],
        "k": code["k"],
        "d": code["d"],
        "is_css": code["is_css"],
    }

    # Compute circuit data
    circ_data = compute_circuit_data(
        circuit_text=circuit_text,
        Hx=Hx,
        Hz=Hz,
        code_params=code_params,
        qubit_permutation=perm,
        circuit_name=circuit_name,
        source=source,
        tool=tool,
        description=description,
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
        validation=circ_data["validation"],
        detected_functionality=circ_data["detected_functionality"],
        files_written=written_paths,
        dry_run=dry_run,
    )
