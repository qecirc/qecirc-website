"""Tests for symplectic logical operator computation (non-CSS support)."""

import numpy as np

from scripts.add_circuit.code_identify import (
    build_symplectic_h,
    build_symplectic_logical,
    canonical_form_h,
    canonical_hash_h,
    is_h_css,
    split_h_to_css,
)
from scripts.add_circuit.compute import _compute_symplectic_logicals


def _is_logical_basis(L: np.ndarray, H: np.ndarray, n: int, k: int) -> None:
    """Assert that L is a valid 2k×2n symplectic logical basis for stabilizer H."""
    assert L.shape == (2 * k, 2 * n)
    # Commutes with all stabilizers: H · Λ · Lᵀ = 0
    H_swap = np.hstack([H[:, n:], H[:, :n]])
    assert np.all((H_swap @ L.T) % 2 == 0), "logicals must commute with stabilizers"
    # Symplectic Gram matrix has the canonical anti-block-diagonal form
    L_swap = np.hstack([L[:, n:], L[:, :n]])
    gram = (L @ L_swap.T) % 2
    expected = np.zeros((2 * k, 2 * k), dtype=int)
    expected[:k, k:] = np.eye(k, dtype=int)
    expected[k:, :k] = np.eye(k, dtype=int)
    assert np.array_equal(gram, expected), f"logical Gram mismatch:\n{gram}"


def _five_qubit_H():
    Hx = np.array(
        [
            [1, 0, 0, 1, 0],
            [0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
        ]
    )
    Hz = np.array(
        [
            [0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1],
        ]
    )
    return np.hstack([Hx, Hz])


def _steane_H():
    Hx = np.array(
        [
            [1, 0, 1, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1],
        ]
    )
    Hz = Hx.copy()
    return build_symplectic_h(Hx, Hz)


class TestComputeSymplecticLogicals:
    def test_five_qubit_logicals_are_valid(self):
        H = _five_qubit_H()
        L = _compute_symplectic_logicals(H, n=5, k=1)
        _is_logical_basis(L, H, n=5, k=1)

    def test_steane_logicals_are_valid(self):
        H = _steane_H()
        L = _compute_symplectic_logicals(H, n=7, k=1)
        _is_logical_basis(L, H, n=7, k=1)

    def test_zero_logicals_when_k_zero(self):
        # Construct a code with k=0 (n=2, 2 stabilizers Z_0, Z_1).
        H = np.array(
            [
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
        L = _compute_symplectic_logicals(H, n=2, k=0)
        assert L.shape == (0, 4)


class TestSplitHToCss:
    def test_steane_is_css(self):
        H = _steane_H()
        result = split_h_to_css(H, n=7)
        assert result is not None
        Hx, Hz = result
        # Both halves match the Steane Hx (Steane is self-dual).
        steane_check = np.array(
            [
                [1, 0, 1, 0, 1, 0, 1],
                [0, 1, 1, 0, 0, 1, 1],
                [0, 0, 0, 1, 1, 1, 1],
            ]
        )
        # Same row space (RREF equality)
        from scripts.add_circuit.code_identify import gf2_rref

        assert np.array_equal(gf2_rref(Hx), gf2_rref(steane_check))
        assert np.array_equal(gf2_rref(Hz), gf2_rref(steane_check))

    def test_five_qubit_not_css(self):
        H = _five_qubit_H()
        assert split_h_to_css(H, n=5) is None
        assert is_h_css(H, n=5) is False

    def test_single_xz_not_css(self):
        # H = [[1, 0, 0, 1]] (n=2) is the 2-qubit stabilizer X⊗Z, which is non-CSS.
        H = np.array([[1, 0, 0, 1]])
        assert split_h_to_css(H, n=2) is None


class TestCanonicalHashH:
    def test_hash_is_deterministic_per_input(self):
        """canonical_hash_h is a function of H (deterministic), but is NOT
        invariant under qubit permutations of the input — non-CSS dedup matches
        only on exact canonical form. (See plan task 4 for permuted-submission
        handling.)"""
        H = _five_qubit_H()
        assert canonical_hash_h(H, n=5) == canonical_hash_h(H, n=5)

    def test_distinct_codes_distinct_hashes(self):
        h_5q = canonical_hash_h(_five_qubit_H(), n=5)
        # Steane via H goes through the CSS detection path; canonical_hash_h
        # only matches a CSS code if you pass it as Hx/Hz, so just compare
        # that the symplectic hash starts with the sym: prefix it advertises.
        # Construct a different non-CSS code: tweak a row.
        H2 = _five_qubit_H().copy()
        H2[0, 5] ^= 1  # flip one bit → different code
        h_2 = canonical_hash_h(H2, n=5)
        assert h_5q != h_2

    def test_does_not_crash_on_uneven_xz_ranks(self):
        # X-half rank 2, Z-half rank 1 → old halves-hash crashed.
        H = np.array([[1, 1, 0, 0], [1, 0, 0, 1]])
        h = canonical_hash_h(H, n=2)  # must not raise
        assert isinstance(h, str) and len(h) == 64

    def test_no_collision_between_distinct_rowspaces(self):
        # (X⊗Z, Z⊗X) vs (Y, Y) — both valid stabilizer codes, distinct rowspaces.
        H_a = np.array([[1, 0, 0, 1], [0, 1, 1, 0]])
        H_b = np.array([[1, 0, 1, 0], [0, 1, 0, 1]])
        assert canonical_hash_h(H_a, n=2) != canonical_hash_h(H_b, n=2)


class TestCanonicalFormH:
    def test_canonical_form_h_drops_zero_rows(self):
        H = np.vstack([_five_qubit_H(), np.zeros((1, 10), dtype=int)])
        canon, _ = canonical_form_h(H, n=5)
        assert canon.shape == (4, 10)
        assert np.all(canon.sum(axis=1) > 0)


class TestLogicalMinimumWeight:
    def test_five_qubit_logicals_are_weight_d(self):
        """For the [[5,1,3]] code, both X-bar and Z-bar minimum weights are
        the code distance d = 3 in symplectic weight (number of non-identity
        Paulis)."""
        H = _five_qubit_H()
        L = _compute_symplectic_logicals(H, n=5, k=1)

        def symplectic_weight(row, n):
            return int(sum(1 for i in range(n) if row[i] or row[i + n]))

        weights = sorted(symplectic_weight(row, 5) for row in L)
        assert weights == [3, 3], f"expected [3, 3], got {weights}"


class TestBuildSymplecticHelpers:
    def test_build_symplectic_h_block_diagonal(self):
        Hx = np.array([[1, 0], [0, 1]])
        Hz = np.array([[1, 1]])
        h = build_symplectic_h(Hx, Hz)
        assert h.shape == (3, 4)
        # Top rows: [Hx | 0]
        assert np.array_equal(h[:2, :2], Hx)
        assert np.array_equal(h[:2, 2:], np.zeros((2, 2), dtype=int))
        # Bottom row: [0 | Hz]
        assert np.array_equal(h[2:, :2], np.zeros((1, 2), dtype=int))
        assert np.array_equal(h[2:, 2:], Hz)

    def test_build_symplectic_logical_pairs(self):
        Lx = np.array([[1, 1, 1]])
        Lz = np.array([[1, 1, 1]])
        L = build_symplectic_logical(Lx, Lz, n=3, k=1)
        assert L.shape == (2, 6)
        assert np.array_equal(L[0], np.array([1, 1, 1, 0, 0, 0]))
        assert np.array_equal(L[1], np.array([0, 0, 0, 1, 1, 1]))
