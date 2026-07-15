"""Detectors and observables derived for state-prep and encoding circuits.

The load-bearing claim is that a derived detector is *deterministic*. Several
tests therefore assert the negative — a wrong-basis or corrupted check set must
be rejected — because a validator that accepts everything proves nothing.

Steane is the CSS workhorse here; the five-qubit code stands in for non-CSS,
whose mixed X/Z stabilizers no single terminal basis can read.
"""

import numpy as np
import stim

from scripts.add_circuit.annotate import (
    build_annotated,
    logical_input_qubits,
    map_original_h,
    sparsify_basis,
    validate_annotated,
)
from scripts.add_circuit.circuit_validate import extract_code
from scripts.add_circuit.code_identify import build_symplectic_h, build_symplectic_logical
from scripts.annotate_circuits import _with_annotated_url

# The Steane encoder from test_circuit_validate, which that module already
# asserts maps |0...0> into the code space. Deriving the check matrices from it
# with extract_code keeps circuit and matrices consistent by construction rather
# than by hand-transcription.
STEANE_STIM = """\
H 4 5 6
TICK
CX 5 1
TICK
CX 1 2 4 0
TICK
CX 6 4 5 3 2 0
TICK
CX 6 3 4 5 0 1
"""

_steane = extract_code(STEANE_STIM, circuit_type="encoding", k=1)
STEANE_HX, STEANE_HZ = _steane.Hx, _steane.Hz
STEANE_H = build_symplectic_h(STEANE_HX, STEANE_HZ)

# Steane is self-dual and its logical is the all-ones string in both bases
# (weight-7 overlaps every weight-4 check evenly, so it commutes).
STEANE_LX = np.array([[1] * 7], dtype=int)
STEANE_LZ = np.array([[1] * 7], dtype=int)
STEANE_LOGICAL = build_symplectic_logical(STEANE_LX, STEANE_LZ, 7, 1)

# An encoder run on |0...0> *is* a |0>_L prep, and build_annotated supplies the
# reset prologue itself — so the same text serves both fixtures.
STEANE_ZERO = STEANE_STIM


# Shor [[9,1,3]] encoder. Needed because Steane is SELF-DUAL: its Hx and Hz span
# the same row space, so Hx rows are perfectly valid Z-checks and a wrong-basis
# control against Steane would vacuously pass. Shor is asymmetric (six weight-2
# Z checks, two weight-6 X checks), so the halves are genuinely distinguishable.
SHOR_STIM = """\
CX 0 3 0 6
H 0 3 6
CX 0 1 0 2 3 4 3 5 6 7 6 8
"""

_shor = extract_code(SHOR_STIM, circuit_type="encoding", k=1)
SHOR_HX, SHOR_HZ = _shor.Hx, _shor.Hz
SHOR_H = build_symplectic_h(SHOR_HX, SHOR_HZ)


def _five_qubit_h():
    """The [[5,1,3]] code: every stabilizer mixes X and Z (XZZXI and cyclic)."""
    rows = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
    x = np.array([[1 if c in "XY" else 0 for c in r] for r in rows], dtype=int)
    z = np.array([[1 if c in "ZY" else 0 for c in r] for r in rows], dtype=int)
    return np.hstack([x, z])


# --- the derived annotation is actually correct -----------------------------


def test_zero_prep_detectors_are_deterministic():
    circ = build_annotated(
        STEANE_ZERO,
        STEANE_H,
        STEANE_LOGICAL,
        n=7,
        k=1,
        kind="state-preparation",
        logical_state="zero",
    )
    assert circ is not None
    assert validate_annotated(circ) is None
    assert circ.num_detectors == 3  # the Z half of the stabilizers
    assert circ.num_observables == 1


def test_zero_prep_observable_reads_zero():
    circ = build_annotated(
        STEANE_ZERO,
        STEANE_H,
        STEANE_LOGICAL,
        n=7,
        k=1,
        kind="state-preparation",
        logical_state="zero",
    )
    dets, obs = circ.compile_detector_sampler().sample(200, separate_observables=True)
    assert dets.sum() == 0  # no detector fires on a noiseless run
    assert obs.mean() == 0.0  # |0>_L has logical Z = 0


def test_zero_prep_resets_every_qubit_and_reads_out_in_z():
    circ = build_annotated(
        STEANE_ZERO,
        STEANE_H,
        STEANE_LOGICAL,
        n=7,
        k=1,
        kind="state-preparation",
        logical_state="zero",
    )
    names = [op.name for op in circ]
    assert names[0] == "R"
    assert "M" in names and "MX" not in names


def test_plus_prep_uses_x_basis_readout():
    # Transversal H after the |0>_L prep gives |+>_L.
    circ = build_annotated(
        STEANE_ZERO + "H 0 1 2 3 4 5 6\n",
        STEANE_H,
        STEANE_LOGICAL,
        n=7,
        k=1,
        kind="state-preparation",
        logical_state="plus",
    )
    assert circ is not None
    assert validate_annotated(circ) is None
    assert "MX" in [op.name for op in circ]


# --- the negative controls: a validator that accepts everything is useless ---


def test_shor_halves_are_distinguishable():
    """Guards the control below: if Shor ever looked self-dual, it would vacuously pass."""
    assert sorted(int(r.sum()) for r in SHOR_HZ) == [2, 2, 2, 2, 2, 2]
    assert sorted(int(r.sum()) for r in SHOR_HX) == [6, 6]


def test_wrong_basis_detectors_are_rejected():
    """X-type checks are not deterministic under a Z-basis readout of |0>_L."""
    out = stim.Circuit()
    out.append("R", list(range(9)))
    for op in stim.Circuit(SHOR_STIM):
        out.append(op.name, op.targets_copy(), op.gate_args_copy())
    out.append("M", list(range(9)))
    for row in SHOR_HX:  # wrong half on purpose
        out.append("DETECTOR", [stim.target_rec(i - 9) for i in range(9) if row[i]])
    assert validate_annotated(out) is not None


def test_right_basis_detectors_are_accepted_on_the_same_code():
    """The other side of the control: Shor's Z half must pass where its X half failed."""
    out = stim.Circuit()
    out.append("R", list(range(9)))
    for op in stim.Circuit(SHOR_STIM):
        out.append(op.name, op.targets_copy(), op.gate_args_copy())
    out.append("M", list(range(9)))
    for row in SHOR_HZ:
        out.append("DETECTOR", [stim.target_rec(i - 9) for i in range(9) if row[i]])
    assert validate_annotated(out) is None


def test_build_annotated_picks_the_z_half_on_an_asymmetric_code():
    """End-to-end on the asymmetric code: it must choose Hz, not Hx.

    Uses the encoder shape so no observable is involved — this isolates the
    detector-half choice from the logical convention tested below.
    """
    circ = build_annotated(
        SHOR_STIM, SHOR_H, np.zeros((0, 18), dtype=int), n=9, k=1, kind="encoding"
    )
    assert circ is not None
    assert validate_annotated(circ) is None
    assert circ.num_detectors == 6  # the six weight-2 Z checks, not the two X ones


def test_a_non_deterministic_observable_is_rejected():
    """The observable is checked as strictly as the detectors.

    Worth pinning: the Pauli type of a logical is a property of the code's
    convention, not of the state's name. This fixture is Shor in the phase-flip
    -outer orientation, where the |0>_L-deterministic logical is X-type — so a
    Z-type logical is not a logical of this code at all, and must be caught.
    """
    logical = build_symplectic_logical(
        np.array([[1] * 9], dtype=int), np.array([[1, 0, 0, 1, 0, 0, 1, 0, 0]], dtype=int), 9, 1
    )
    circ = build_annotated(
        SHOR_STIM,
        SHOR_H,
        logical,
        n=9,
        k=1,
        kind="state-preparation",
        logical_state="zero",
    )
    assert circ is not None
    assert circ.num_detectors == 6  # detectors are still right ...
    assert validate_annotated(circ) is not None  # ... but the observable is not


def test_corrupted_check_row_is_rejected():
    """One flipped bit must break determinism, or the check proves nothing."""
    bad = STEANE_HZ.copy()
    bad[0][0] ^= 1
    circ = stim.Circuit(STEANE_ZERO)
    out = stim.Circuit()
    out.append("R", list(range(7)))
    for op in circ:
        out.append(op.name, op.targets_copy(), op.gate_args_copy())
    out.append("M", list(range(7)))
    for row in bad:
        out.append("DETECTOR", [stim.target_rec(i - 7) for i in range(7) if row[i]])
    assert validate_annotated(out) is not None


# --- scope: what this refuses to annotate -----------------------------------


def test_non_css_code_is_refused():
    h = _five_qubit_h()
    logical = build_symplectic_logical(
        np.array([[1, 1, 1, 1, 1]], dtype=int), np.array([[1, 1, 1, 1, 1]], dtype=int), 5, 1
    )
    assert (
        build_annotated(
            "H 0\n", h, logical, n=5, k=1, kind="state-preparation", logical_state="zero"
        )
        is None
    )


def test_unsupported_logical_state_is_refused():
    assert (
        build_annotated(
            STEANE_ZERO,
            STEANE_H,
            STEANE_LOGICAL,
            n=7,
            k=1,
            kind="state-preparation",
            logical_state="magic",
        )
        is None
    )


def test_unknown_kind_is_refused():
    assert (
        build_annotated(STEANE_ZERO, STEANE_H, STEANE_LOGICAL, n=7, k=1, kind="syndrome-extraction")
        is None
    )


# --- encoders ---------------------------------------------------------------


def test_encoder_input_derived_from_tableau():
    """Z on an input propagates to a logical, not a stabilizer."""
    # Steane encoder: qubit 0 carries the logical, 1..6 are |0> ancillas.
    encoder = STEANE_STIM
    inputs = logical_input_qubits(stim.Circuit(encoder), STEANE_H, 7)
    assert inputs is not None and len(inputs) == 1


def test_encoder_input_derived_from_resets_when_no_tableau():
    """Reset-bearing encoders have no tableau; their free qubits are the inputs."""
    circ = stim.Circuit("R 1 2 3 4 5 6\nCX 0 1\n")
    assert logical_input_qubits(circ, STEANE_H, 7) == [0]


def test_encoder_leaves_inputs_unreset_and_emits_no_observable():
    encoder = STEANE_STIM
    circ = build_annotated(encoder, STEANE_H, STEANE_LOGICAL, n=7, k=1, kind="encoding")
    assert circ is not None
    assert validate_annotated(circ) is None
    # The logical is whatever the reader supplies, so nothing is deterministic.
    assert circ.num_observables == 0
    reset = next(op for op in circ if op.name == "R")
    assert len(reset.targets_copy()) == 6  # the input qubit is left free


def test_encoder_detectors_hold_for_any_input_state():
    """Hz is deterministic for every input, which is the whole basis of the design."""
    encoder = STEANE_STIM
    circ = build_annotated(encoder, STEANE_H, STEANE_LOGICAL, n=7, k=1, kind="encoding")
    inputs = logical_input_qubits(stim.Circuit(encoder), STEANE_H, 7)
    for prep in ([], [("X", inputs[0])], [("H", inputs[0])], [("H", inputs[0]), ("S", inputs[0])]):
        probe = stim.Circuit()
        for op in circ:
            probe.append(op.name, op.targets_copy(), op.gate_args_copy())
            if op.name == "R":
                for gate, q in prep:
                    probe.append(gate, [q])
        assert validate_annotated(probe) is None


# --- basis mapping ----------------------------------------------------------


def test_map_original_direct_when_labelings_match():
    mapped = map_original_h(STEANE_H, STEANE_H, 7)
    assert mapped is not None and mapped[1] == "direct"


def test_map_original_via_notes_permutation():
    perm = [6, 5, 4, 3, 2, 1, 0]
    idx = np.array(perm)
    permuted = np.hstack([STEANE_H[:, :7][:, idx], STEANE_H[:, 7:][:, idx]])
    notes = (
        "Canonicalization qubit permutation "
        f"(stored qubit i = original qubit permutation[i]): {perm}"
    )
    mapped = map_original_h(permuted, STEANE_H, 7, notes)
    assert mapped is not None
    # Applying the recorded permutation must land back on the stored row space.
    assert mapped[1] in ("notes", "recomputed")


def test_map_original_rejects_a_different_code():
    """Row-space verification is what makes a wrong permutation fail loudly."""
    other = build_symplectic_h(
        np.array([[1, 1, 0, 0, 0, 0, 0]], dtype=int),
        np.array([[0, 0, 0, 0, 0, 1, 1]], dtype=int),
    )
    assert map_original_h(other, STEANE_H, 7) is None


def test_map_original_rejects_wrong_width():
    assert map_original_h(np.zeros((3, 8), dtype=int), STEANE_H, 7) is None


def test_map_original_ignores_a_malformed_notes_permutation():
    notes = "permutation[i]): [0, 0, 0, 0, 0, 0, 0]"  # not a permutation
    mapped = map_original_h(STEANE_H, STEANE_H, 7, notes)
    assert mapped is not None and mapped[1] == "direct"


# --- sparsification ---------------------------------------------------------


def test_sparsify_preserves_rowspace_and_lowers_weight():
    from scripts.add_circuit.code_identify import gf2_rank

    dense = np.array(
        [[1, 1, 1, 1, 0, 0, 0], [0, 1, 1, 1, 1, 0, 0], [1, 0, 0, 0, 1, 0, 0]], dtype=int
    )
    out = sparsify_basis(dense)
    stacked = np.vstack([dense, out])
    assert gf2_rank(stacked) == gf2_rank(dense)  # same row space
    assert out.sum() <= dense.sum()  # no worse
    assert not np.any(~out.any(axis=1))  # no row collapsed to zero


def test_sparsify_handles_empty():
    empty = np.zeros((0, 7), dtype=int)
    assert sparsify_basis(empty).shape == (0, 7)


# --- the YAML edit in the backfill script ------------------------------------

_YAML = "qec_id: 1\ncrumble_url: https://a\nquirk_url: https://q\ntags: [encoding]\n"


def test_annotated_url_is_inserted_after_crumble_url():
    out = _with_annotated_url(_YAML, "https://b")
    lines = out.splitlines()
    assert lines[1] == "crumble_url: https://a"
    assert lines[2] == "crumble_url_annotated: https://b"
    assert lines[3] == "quirk_url: https://q"


def test_annotated_url_edit_is_idempotent():
    """The regression: a single-pass edit wrote the key twice on re-run, and the
    duplicate parsed to the same value — so a value-based change check missed it."""
    once = _with_annotated_url(_YAML, "https://b")
    twice = _with_annotated_url(once, "https://b")
    assert once == twice
    assert twice.count("crumble_url_annotated:") == 1


def test_annotated_url_replaces_a_stale_value():
    stale = _with_annotated_url(_YAML, "https://old")
    fresh = _with_annotated_url(stale, "https://new")
    assert "https://old" not in fresh
    assert fresh.count("crumble_url_annotated:") == 1


def test_empty_annotated_url_removes_the_key():
    """Wide circuits have no Crumble link; the key must not linger as an empty."""
    present = _with_annotated_url(_YAML, "https://b")
    removed = _with_annotated_url(present, "")
    assert "crumble_url_annotated" not in removed
    assert removed == _YAML


def test_annotated_url_appended_when_no_crumble_url_key():
    text = "qec_id: 1\ntags: [encoding]\n"
    out = _with_annotated_url(text, "https://b")
    assert out.count("crumble_url_annotated:") == 1
    assert out.startswith(text)


def test_sparsified_basis_still_validates():
    circ = build_annotated(
        STEANE_ZERO,
        STEANE_H,
        STEANE_LOGICAL,
        n=7,
        k=1,
        kind="state-preparation",
        logical_state="zero",
        original_h=STEANE_H,
    )
    assert circ is not None
    assert validate_annotated(circ) is None
