"""ancilla_role: routing ancillas are not flag qubits.

The pipeline infers "this circuit has qubits at indices >= n" from the circuit
alone, but that does not say what they are *for*. Flag qubits carry a fault
tolerance claim; bridge qubits mediating gates under a restricted connectivity
do not. `ancilla_role` separates the two.
"""

import pytest

from scripts.add_circuit.state_prep import _augment_tags, _build_notes, _compact_ids

NOTES_KWARGS = dict(
    base_notes=None,
    source_file=None,
    logical_state=None,
    connectivity=None,
    gate_set=None,
    device=None,
    qubit_placement=None,
    permutation=None,
)


def test_flag_role_tags_flag():
    tags = _augment_tags(
        ["state-preparation"],
        connectivity=None,
        device=None,
        logical_state=None,
        has_flags=True,
    )
    assert "flag" in tags


def test_routing_role_does_not_tag_flag():
    # import_state_prep passes `has_flags and role == "flag"`, so a routing
    # circuit reaches _augment_tags with has_flags=False even though it has
    # qubits above n.
    tags = _augment_tags(
        ["state-preparation"],
        connectivity=None,
        device=None,
        logical_state=None,
        has_flags=False,
    )
    assert "flag" not in tags


def test_flag_tag_not_duplicated_when_already_present():
    tags = _augment_tags(
        ["state-preparation", "flag"],
        connectivity=None,
        device=None,
        logical_state=None,
        has_flags=True,
    )
    assert tags.count("flag") == 1


def test_notes_label_flag_role():
    notes = _build_notes(flag_qubits=[7, 8], ancilla_role="flag", **NOTES_KWARGS)
    assert "Flag/ancilla qubits: [7, 8]" in notes


def test_notes_label_routing_role():
    notes = _build_notes(flag_qubits=[7, 8], ancilla_role="routing", **NOTES_KWARGS)
    assert "Routing ancilla qubits: [7, 8]" in notes
    assert "Flag/ancilla" not in notes


def test_notes_default_role_is_flag():
    # Existing importers call _build_notes without ancilla_role; they must keep
    # the pre-change wording.
    notes = _build_notes(flag_qubits=[7], **NOTES_KWARGS)
    assert "Flag/ancilla qubits: [7]" in notes


def test_no_ancilla_qubits_yields_no_label():
    notes = _build_notes(flag_qubits=[], ancilla_role="routing", **NOTES_KWARGS)
    assert "ancilla qubits" not in notes


def test_compact_ids_keeps_short_runs_as_a_list():
    assert _compact_ids([7, 8]) == "[7, 8]"
    assert _compact_ids(list(range(9, 17))) == str(list(range(9, 17)))  # 8 = threshold


def test_compact_ids_collapses_long_contiguous_runs():
    assert _compact_ids(list(range(221, 441))) == "221-440 (220 qubits)"


def test_compact_ids_falls_back_when_not_contiguous():
    ids = [1, 2, 3, 4, 5, 6, 7, 8, 99]  # long but has a gap
    assert _compact_ids(ids) == str(ids)


def test_long_ancilla_run_is_compact_in_notes():
    notes = _build_notes(flag_qubits=list(range(221, 441)), ancilla_role="routing", **NOTES_KWARGS)
    assert "Routing ancilla qubits: 221-440 (220 qubits)" in notes
    assert "222" not in notes  # the run is not spelled out


def test_invalid_ancilla_role_rejected():
    from scripts.add_circuit import import_state_prep

    with pytest.raises(ValueError, match="ancilla_role"):
        import_state_prep(
            circuit="H 0\nCX 0 1",
            n=2,
            d=1,
            code_name="x",
            circuit_name="x",
            method="self_dual",
            ancilla_role="bridge",
        )
