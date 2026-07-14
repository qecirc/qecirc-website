"""QUBIT_COORDS survive ingestion.

STIM places qubits at coordinates via QUBIT_COORDS. That geometry is the code's
layout for topological codes, and locality information for hardware-targeted
circuits, so it has to reach the stored body intact.

The compaction path is the one that used to lose it: `compact_stim_circuit`
keeps the instruction but drops its arguments, so `QUBIT_COORDS(3, 7) 0` came
out as a bare, meaningless `QUBIT_COORDS 0`. Compaction runs for TICK-less
circuits, which is most of the library.
"""

import stim

from scripts.add_circuit.compute_circuit import _restore_coords, compute_circuit_data

COORDS_TICKS = "QUBIT_COORDS(3, 7) 0\nQUBIT_COORDS(1, 2) 1\nH 0\nTICK\nCX 0 1\n"
# No TICK -> compaction runs.
COORDS_NO_TICKS = "QUBIT_COORDS(3, 7) 0\nQUBIT_COORDS(1, 2) 1\nH 0\nCX 0 1\n"


def _coords_of(text, permutation=None):
    data = compute_circuit_data(text, qubit_permutation=permutation, circuit_name="t")
    body = data["bodies"][0]["body"]
    return stim.Circuit(body).get_final_qubit_coordinates(), body


def test_coords_preserved_when_ticks_prevent_compaction():
    coords, _ = _coords_of(COORDS_TICKS)
    assert coords == {0: [3.0, 7.0], 1: [1.0, 2.0]}


def test_coords_preserved_through_compaction():
    coords, body = _coords_of(COORDS_NO_TICKS)
    assert coords == {0: [3.0, 7.0], 1: [1.0, 2.0]}
    # The regression: a coordinate-less QUBIT_COORDS left behind by compaction.
    assert "QUBIT_COORDS 0" not in body
    assert "QUBIT_COORDS 1" not in body


def test_coords_follow_the_qubit_permutation():
    # permutation[new] = old, so new qubit 0 takes old qubit 1's coordinate.
    for text in (COORDS_TICKS, COORDS_NO_TICKS):
        coords, _ = _coords_of(text, permutation=[1, 0])
        assert coords == {0: [1.0, 2.0], 1: [3.0, 7.0]}, text


def test_circuit_without_coords_gains_none():
    coords, body = _coords_of("H 0\nCX 0 1\n")
    assert coords == {}
    assert "QUBIT_COORDS" not in body


def test_coords_do_not_affect_metrics():
    with_coords = compute_circuit_data(COORDS_NO_TICKS, circuit_name="t")
    without = compute_circuit_data("H 0\nCX 0 1\n", circuit_name="t")
    for key in ("gate_count", "two_qubit_gate_count", "depth", "qubit_count"):
        assert with_coords[key] == without[key], key


def test_three_dimensional_coords_survive():
    coords, _ = _coords_of("QUBIT_COORDS(1, 2, 3) 0\nH 0\n")
    assert coords == {0: [1.0, 2.0, 3.0]}


def test_partial_coords_survive_compaction():
    # Only some qubits carry a coordinate; the rest must not gain a bogus one.
    coords, _ = _coords_of("QUBIT_COORDS(5, 5) 1\nH 0\nCX 0 1\n")
    assert coords == {1: [5.0, 5.0]}


def test_restore_coords_keeps_repeat_blocks():
    # _restore_coords rebuilds the circuit instruction by instruction; a REPEAT
    # block is not a CircuitInstruction and must be passed through whole.
    circ = stim.Circuit("QUBIT_COORDS(1, 2) 0\nREPEAT 2 {\n    H 0\n    TICK\n}\nCX 0 1\n")
    out = _restore_coords(circ, circ.get_final_qubit_coordinates())
    assert "REPEAT 2 {" in str(out)
    assert out.get_final_qubit_coordinates() == {0: [1.0, 2.0]}


def test_restore_coords_is_a_noop_without_coords():
    circ = stim.Circuit("H 0\nCX 0 1\n")
    assert _restore_coords(circ, circ.get_final_qubit_coordinates()) == circ
