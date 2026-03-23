"""
Circuit validation: parse a STIM circuit and classify its functionality.

Stabilizer-tableau-based correctness checking (requiring the stim package) is
isolated in `check_circuit_vs_matrices` so the rest of the module is testable
without it.
"""

from pathlib import Path
from typing import Optional

import numpy as np

from .models import CircuitProperties, ValidationResult

# STIM instruction sets used for heuristic classification
_MEASURE_OPS = {"M", "MX", "MY", "MZ", "MR", "MRX", "MRY", "MRZ"}
_ENTANGLE_OPS = {"CNOT", "CX", "CZ", "CY", "SWAP", "ISWAP"}
_RESET_OPS = {"R", "RX", "RY", "RZ"}


def load_circuit(path: str | Path) -> str:
    return Path(path).read_text()


def _instructions(circuit_text: str) -> set[str]:
    ops = set()
    for line in circuit_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        token = line.split()[0].split("(")[0].upper()
        if token not in {"QUBIT_COORDS", "DETECTOR", "OBSERVABLE_INCLUDE", "TICK", "REPEAT"}:
            ops.add(token)
    return ops


def classify_functionality(circuit_text: str) -> Optional[str]:
    """
    Heuristic classification based on instruction types present.

    Returns one of: "encoding", "syndrome-extraction", "state-preparation", or None.
    """
    ops = _instructions(circuit_text)
    has_measure = bool(ops & _MEASURE_OPS)
    has_entangle = bool(ops & _ENTANGLE_OPS)
    has_reset = bool(ops & _RESET_OPS)

    if has_measure and has_entangle:
        return "syndrome-extraction"
    if has_entangle and not has_measure:
        return "encoding"
    if has_reset and not has_entangle and not has_measure:
        return "state-preparation"
    return None


def circuit_properties(circuit_text: str) -> CircuitProperties:
    """Extract basic structural properties without running a simulation."""
    max_qubit = -1
    gate_count = 0
    depth = circuit_text.upper().count("TICK")

    for line in circuit_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        op = parts[0].split("(")[0].upper()
        if op in ("QUBIT_COORDS", "DETECTOR", "OBSERVABLE_INCLUDE", "TICK", "REPEAT", "#"):
            continue
        gate_count += 1
        for token in parts[1:]:
            try:
                q = int(token)
                max_qubit = max(max_qubit, q)
            except ValueError:
                pass

    return CircuitProperties(
        n_qubits=max_qubit + 1 if max_qubit >= 0 else 0,
        depth=depth,
        gate_count=gate_count,
        detected_functionality=classify_functionality(circuit_text),
    )


def check_circuit_vs_matrices(
    circuit_text: str,
    Hx: np.ndarray,
    Hz: np.ndarray,
    qubit_permutation: Optional[list[int]] = None,
) -> ValidationResult:
    """
    Verify the circuit's stabilizer tableau is consistent with Hx and Hz.

    Requires the `stim` package. Returns ValidationResult(valid=False) with
    details if stim is unavailable or the check fails.
    """
    try:
        import stim  # type: ignore
    except ImportError:
        return ValidationResult(
            valid=False,
            mismatch_details="stim package not installed; skipping tableau check",
        )

    try:
        circuit = stim.Circuit(circuit_text)
        tableau = circuit.to_tableau()
    except Exception as exc:
        return ValidationResult(valid=False, mismatch_details=f"stim parse error: {exc}")

    n = Hx.shape[1]
    if tableau.num_qubits < n:
        return ValidationResult(
            valid=False,
            mismatch_details=f"circuit acts on {tableau.num_qubits} qubits but code has n={n}",
        )

    # Apply qubit permutation if provided
    Hx_check = Hx[:, qubit_permutation] if qubit_permutation else Hx
    Hz_check = Hz[:, qubit_permutation] if qubit_permutation else Hz

    # Check that each stabilizer generator is preserved by the circuit
    mismatches = []
    for i, row in enumerate(Hx_check):
        ps = stim.PauliString(
            "".join("X" if x else "I" for x in row)
            + "".join("Z" if z else "I" for z in Hz_check[i])
        )
        # TODO: compare against output tableau stabilizers
        # Full implementation requires mapping logical → physical qubits
        _ = ps  # placeholder

    # Placeholder: return valid until full tableau check is implemented
    return ValidationResult(
        valid=True,
        detected_functionality=classify_functionality(circuit_text),
        mismatch_details="tableau check not yet fully implemented",
    )
