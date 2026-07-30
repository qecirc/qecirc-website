"""Tests for circuit-level distance measurement."""

import numpy as np
import pytest
import stim

from scripts.add_circuit.circuit_distance import (
    UNIFORM_P,
    circuit_distance,
    round_circuit_distance,
    with_uniform_noise,
)
from scripts.add_circuit.syndrome_extraction import build_se_round
from scripts.tests.test_syndrome_extraction import (
    STEANE_H,
    STEANE_LOGICAL,
    N,
    TestBuildRound,
)


class TestNoiseModel:
    def test_every_kind_of_location_gets_a_fault(self):
        circ = stim.Circuit("R 0\nTICK\nH 0\nCX 0 1\nTICK\nM 0")
        text = str(with_uniform_noise(circ, 0.001))
        assert "X_ERROR(0.001) 0" in text  # the reset
        assert "DEPOLARIZE1(0.001) 0" in text  # the H
        assert "DEPOLARIZE2(0.001) 0 1" in text  # the CX, correlated across the pair
        assert "M(0.001) 0" in text  # the readout

    def test_an_idle_qubit_is_a_fault_location(self):
        """Leaving idle noise out is the usual reason a hand-rolled model reports
        too high a distance: a long round costs nothing extra without it."""
        # Qubit 1 sits out the second tick entirely. Counted rather than matched
        # on text, because stim fuses adjacent same-gate instructions and the
        # gate noise and the idle noise are the same instruction.
        noisy = with_uniform_noise(stim.Circuit("H 0\nH 1\nTICK\nH 0\nTICK"), 0.001)
        seen = {0: 0, 1: 0}
        for op in noisy:
            if op.name == "DEPOLARIZE1":
                for target in op.targets_copy():
                    seen[target.value] += 1
        assert seen[1] == seen[0], "an idle qubit must fault as often as a busy one"
        assert seen[1] >= 2

    def test_repeat_blocks_are_reached(self):
        circ = stim.Circuit("REPEAT 3 {\n  H 0\n  TICK\n}")
        assert "DEPOLARIZE1" in str(with_uniform_noise(circ, 0.001))

    def test_an_unmodelled_operation_is_refused_not_ignored(self):
        with pytest.raises(ValueError, match="no noise model"):
            with_uniform_noise(stim.Circuit("MR 0"), 0.001)

    def test_the_rate_does_not_change_the_distance(self):
        """The search counts mechanisms in the detector error model, and every
        location carries one at any p in (0, 1)."""
        body = str(build_se_round(TestBuildRound._TICKS, N))
        a = round_circuit_distance(body, STEANE_H, STEANE_LOGICAL, N, 3, p=1e-3)
        b = round_circuit_distance(body, STEANE_H, STEANE_LOGICAL, N, 3, p=1e-2)
        assert a == b


class TestRoundCircuitDistance:
    def test_the_steane_round_is_not_distance_preserving(self):
        """An unflagged round on a d=3 code loses a step to hook errors: one
        fault on an ancilla lands on two data qubits at once."""
        body = str(build_se_round(TestBuildRound._TICKS, N))
        assert round_circuit_distance(body, STEANE_H, STEANE_LOGICAL, N, 3) == 2

    def test_both_bases_are_measured_and_the_smaller_wins(self):
        """The point of measuring X memory too. Z alone is not even bounded by
        the code distance — its observable is flipped by X errors, so an
        asymmetric code can report more than `d`."""
        from scripts.add_circuit.annotate import build_annotated_se

        body = str(build_se_round(TestBuildRound._TICKS, N))
        both = []
        for basis in ("Z", "X"):
            experiment = build_annotated_se(body, STEANE_H, STEANE_LOGICAL, N, 3, basis=basis)
            both.append(circuit_distance(with_uniform_noise(experiment, UNIFORM_P), max_degree=3))
        assert round_circuit_distance(body, STEANE_H, STEANE_LOGICAL, N, 3) == min(both)

    def test_a_code_with_no_pure_basis_check_has_nothing_to_measure(self):
        """A non-CSS code has no experiment in either basis, so no number —
        `None`, which the driver records as "not measured" rather than as a
        distance of zero."""
        five_qubit_h = np.array(
            [
                [1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
                [0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
                [0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
            ]
        )
        body = "R 5\nCX 0 5\nM 5"
        assert (
            round_circuit_distance(body, five_qubit_h, np.zeros((0, 10), dtype=int), 5, 3) is None
        )
