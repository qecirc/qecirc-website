"""Regression tests for the add_circuit() public Python API."""

from pathlib import Path

import numpy as np
import yaml

from scripts.add_circuit import add_circuit

# Steane [[7,1,3]] CSS code — minimal valid input
_STEANE_HX = np.array(
    [
        [1, 0, 0, 1, 0, 1, 1],
        [0, 1, 0, 1, 1, 0, 1],
        [0, 0, 1, 0, 1, 1, 1],
    ],
    dtype=int,
)
_STEANE_HZ = _STEANE_HX.copy()

_TRIVIAL_STIM = "QUBIT_COORDS(0, 0) 0\nH 0\nTICK\n"


def test_add_circuit_allocates_qec_id(tmp_path: Path) -> None:
    """add_circuit must populate qec_id in the circuit YAML."""
    result = add_circuit(
        circuit=_TRIVIAL_STIM,
        circuit_name="Trivial",
        d=3,
        Hx=_STEANE_HX,
        Hz=_STEANE_HZ,
        code_name="Steane Code",
        data_dir=tmp_path,
    )

    circ_yaml_path = next(
        p
        for p in result.files_written
        if p.endswith(".yaml") and "circuits" in Path(p).parts and "originals" not in Path(p).parts
    )
    data = yaml.safe_load(Path(circ_yaml_path).read_text(encoding="utf-8"))

    assert "qec_id" in data, f"qec_id missing from circuit YAML: {data}"
    assert isinstance(data["qec_id"], int)
    assert data["qec_id"] >= 1


def test_add_circuit_qec_id_increments(tmp_path: Path) -> None:
    """Adding two circuits must assign distinct, increasing qec_ids."""
    r1 = add_circuit(
        circuit=_TRIVIAL_STIM,
        circuit_name="First",
        d=3,
        Hx=_STEANE_HX,
        Hz=_STEANE_HZ,
        code_name="Steane Code",
        data_dir=tmp_path,
    )
    r2 = add_circuit(
        circuit=_TRIVIAL_STIM + "X 0\n",
        circuit_name="Second",
        d=3,
        Hx=_STEANE_HX,
        Hz=_STEANE_HZ,
        code_name="Steane Code",
        data_dir=tmp_path,
    )
    p1 = next(
        p
        for p in r1.files_written
        if p.endswith(".yaml") and "circuits" in Path(p).parts and "originals" not in Path(p).parts
    )
    p2 = next(
        p
        for p in r2.files_written
        if p.endswith(".yaml") and "circuits" in Path(p).parts and "originals" not in Path(p).parts
    )
    id1 = yaml.safe_load(Path(p1).read_text(encoding="utf-8"))["qec_id"]
    id2 = yaml.safe_load(Path(p2).read_text(encoding="utf-8"))["qec_id"]
    assert id2 == id1 + 1
