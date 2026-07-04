"""Tests for the structural permutation finder."""

import numpy as np

from scripts.add_circuit.perm_find import find_code_permutation

STEANE_H = np.array(
    [
        [0, 0, 0, 1, 1, 1, 1],
        [0, 1, 1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1],
    ]
)

# MQT carbon code (from mqt-qecc src/mqt/qecc/codes/carbon/{hx,hz}.npy)
CARBON_HX = np.array(
    [
        [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    ]
)
CARBON_HZ = np.array(
    [
        [0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    ]
)


def _rowspace_rref(m: np.ndarray) -> np.ndarray:
    from scripts.add_circuit.code_identify import gf2_rref

    r = gf2_rref(np.asarray(m) % 2)
    return r[~np.all(r == 0, axis=1)]


def _assert_maps(hx1, hz1, hx2, hz2, sigma):
    p = np.array(sigma)
    assert np.array_equal(_rowspace_rref(hx1[:, p]), _rowspace_rref(hx2))
    assert np.array_equal(_rowspace_rref(hz1[:, p]), _rowspace_rref(hz2))


def test_identity_on_steane():
    sigma = find_code_permutation(STEANE_H, STEANE_H, STEANE_H, STEANE_H)
    assert sigma is not None
    _assert_maps(STEANE_H, STEANE_H, STEANE_H, STEANE_H, sigma)


def test_relabeled_steane_roundtrip():
    rng = np.random.default_rng(42)
    perm = rng.permutation(7)
    hx1 = STEANE_H[:, perm]
    sigma = find_code_permutation(hx1, hx1, STEANE_H, STEANE_H)
    assert sigma is not None
    _assert_maps(hx1, hx1, STEANE_H, STEANE_H, sigma)


def test_relabeled_carbon_roundtrip():
    rng = np.random.default_rng(7)
    perm = rng.permutation(12)
    hx1, hz1 = CARBON_HX[:, perm], CARBON_HZ[:, perm]
    sigma = find_code_permutation(hx1, hz1, CARBON_HX, CARBON_HZ)
    assert sigma is not None
    _assert_maps(hx1, hz1, CARBON_HX, CARBON_HZ, sigma)


def test_inequivalent_returns_none():
    # Steane vs a code with an extra independent row: not equivalent.
    other = np.vstack([STEANE_H, np.array([[1, 1, 0, 0, 0, 0, 0]])])
    sigma = find_code_permutation(STEANE_H, STEANE_H, other, other)
    assert sigma is None
