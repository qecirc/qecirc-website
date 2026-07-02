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


def _circuit_yaml(result):
    p = next(
        p
        for p in result.files_written
        if p.endswith(".yaml") and "circuits" in Path(p).parts and "originals" not in Path(p).parts
    )
    return Path(p), yaml.safe_load(Path(p).read_text(encoding="utf-8"))


def test_tags_written_to_yaml(tmp_path: Path) -> None:
    """The tags param is persisted to the circuit YAML."""
    result = add_circuit(
        circuit=_TRIVIAL_STIM,
        circuit_name="Tagged",
        d=3,
        Hx=_STEANE_HX,
        Hz=_STEANE_HZ,
        code_name="Steane Code",
        tags=["encoding", "non-ft"],
        data_dir=tmp_path,
    )
    _, data = _circuit_yaml(result)
    assert data["tags"] == ["encoding", "non-ft"]


def test_existing_code_match_uses_stored_slug(tmp_path: Path) -> None:
    """A second circuit for the same code files under the stored slug even when
    a different code_name is passed (code_name must not orphan the circuit)."""
    add_circuit(
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
        code_name="A Totally Different Name",  # must be ignored on a dedup match
        data_dir=tmp_path,
    )
    assert r2.code_status == "existing"
    assert r2.code_slug == "steane-code"
    # no orphan code YAML created for the second name
    assert not (tmp_path / "codes" / "a-totally-different-name.yaml").exists()


def test_overwrite_guard_raises(tmp_path: Path) -> None:
    """Re-adding the same <code>--<circuit> slug raises unless overwrite=True."""
    import pytest

    kw = dict(
        circuit=_TRIVIAL_STIM,
        circuit_name="Dup",
        d=3,
        Hx=_STEANE_HX,
        Hz=_STEANE_HZ,
        code_name="Steane Code",
        data_dir=tmp_path,
    )
    add_circuit(**kw)
    with pytest.raises(FileExistsError):
        add_circuit(**kw)


def test_overwrite_preserves_qec_id(tmp_path: Path) -> None:
    """overwrite=True replaces in place and keeps the original qec_id."""
    kw = dict(
        circuit_name="Dup",
        d=3,
        Hx=_STEANE_HX,
        Hz=_STEANE_HZ,
        code_name="Steane Code",
        data_dir=tmp_path,
    )
    r1 = add_circuit(circuit=_TRIVIAL_STIM, **kw)
    _, d1 = _circuit_yaml(r1)
    r2 = add_circuit(circuit=_TRIVIAL_STIM + "X 0\n", overwrite=True, **kw)
    _, d2 = _circuit_yaml(r2)
    assert d2["qec_id"] == d1["qec_id"]
