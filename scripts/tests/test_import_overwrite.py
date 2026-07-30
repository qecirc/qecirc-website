"""Re-import (data refresh) semantics of import_state_prep.

A refresh resubmits every stored circuit, so the byte-identical-duplicate
guard — which exists to catch *distinct submissions* converging on the same
circuit — must yield to ``overwrite=True``, and the replacement must keep the
circuit's ``qec_id`` (via ``add_circuit``'s overwrite path).
"""

from pathlib import Path

import pytest
import stim

from scripts.add_circuit import import_state_prep
from scripts.add_circuit.yaml_helpers import load_yaml

# Non-FT Steane |0>_L prep: H on the Hx pivot qubits {0, 1, 3}, CX to spread
# each X generator. Steane is self-dual, so derive_matrices_self_dual recovers
# the code from this circuit alone. Normalized through stim so the re-import
# is byte-identical to the stored original — exactly what a rebuild_all
# re-run submits.
_STEANE_ZERO_PREP = str(stim.Circuit("H 0 1 3\nCX 0 2 0 4 0 6 1 2 1 5 1 6 3 4 3 5 3 6"))


def _import(tmp_path: Path, **extra):
    return import_state_prep(
        circuit=_STEANE_ZERO_PREP,
        n=7,
        d=3,
        code_name="Steane Code",
        circuit_name="Refresh Test Prep",
        method="self_dual",
        logical_state="zero",
        tags=["state-preparation", "non-ft"],
        data_dir=str(tmp_path),
        **extra,
    )


def _circuit_doc(tmp_path: Path, result) -> dict:
    path = tmp_path / "circuits" / f"{result.code_slug}--{result.circuit_slug}.yaml"
    return load_yaml(path.read_text())


def test_reimport_without_overwrite_rejected(tmp_path: Path) -> None:
    _import(tmp_path)
    with pytest.raises(ValueError, match="byte-identical"):
        _import(tmp_path)


def test_duplicate_detected_despite_trailing_newline(tmp_path: Path) -> None:
    """Raw dataset files carry a trailing newline; stored originals are
    stim-normalized without one. The guard must compare normalized forms —
    with a byte comparison, every duplicate removed in the 0.4.2 cleanup
    came back on a driver re-run."""
    _import(tmp_path)
    with pytest.raises(ValueError, match="byte-identical"):
        import_state_prep(
            circuit=_STEANE_ZERO_PREP + "\n",  # raw-file form of the same circuit
            n=7,
            d=3,
            code_name="Steane Code",
            circuit_name="Raw File Duplicate",
            method="self_dual",
            logical_state="zero",
            tags=["state-preparation", "non-ft"],
            data_dir=str(tmp_path),
        )


def test_overwrite_still_rejects_duplicate_under_other_name(tmp_path: Path) -> None:
    """Overwrite only exempts a circuit's *own* stored original. A distinct
    dataset file converging on the same circuit (different name) is still a
    duplicate — e.g. independent RL runs in the rlftqc dataset."""
    _import(tmp_path)
    with pytest.raises(ValueError, match="byte-identical"):
        import_state_prep(
            circuit=_STEANE_ZERO_PREP,
            n=7,
            d=3,
            code_name="Steane Code",
            circuit_name="A Different Name",
            method="self_dual",
            logical_state="zero",
            tags=["state-preparation", "non-ft"],
            data_dir=str(tmp_path),
            overwrite=True,
        )


def test_reimport_with_overwrite_keeps_qec_id(tmp_path: Path) -> None:
    first = _import(tmp_path)
    doc1 = _circuit_doc(tmp_path, first)

    second = _import(tmp_path, overwrite=True)
    doc2 = _circuit_doc(tmp_path, second)

    assert second.code_slug == first.code_slug
    assert second.circuit_slug == first.circuit_slug
    assert doc2["qec_id"] == doc1["qec_id"]
