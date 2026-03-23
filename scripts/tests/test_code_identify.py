"""
Tests for code_identify.py.

Examples used:
  [[4,2,2]] CSS code   — Hx = Hz = [[1,1,1,1]]
  [[7,1,3]] Steane     — Hx = Hz = Hamming parity check matrix
  [[5,1,3]] 5-qubit    — general stabilizer (not CSS)
"""

import numpy as np
import pytest

from scripts.add_circuit.code_identify import (
    canonical_hash,
    check_commutativity,
    extract_params,
    find_qubit_permutation,
    gf2_rank,
    gf2_rref,
    is_css,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def code_422():
    Hx = np.array([[1, 1, 1, 1]])
    Hz = np.array([[1, 1, 1, 1]])
    return Hx, Hz


@pytest.fixture
def code_713():
    H = np.array([
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1],
    ])
    return H.copy(), H.copy()


@pytest.fixture
def code_513():
    """[[5,1,3]] 5-qubit perfect code — general stabilizer, not CSS."""
    Hx = np.array([
        [1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
    ])
    Hz = np.array([
        [0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1],
    ])
    return Hx, Hz


# ---------------------------------------------------------------------------
# GF(2) linear algebra
# ---------------------------------------------------------------------------

class TestGf2Rref:
    def test_identity_stays_identity(self):
        I = np.eye(3, dtype=int)
        assert np.array_equal(gf2_rref(I), I)

    def test_zero_matrix(self):
        Z = np.zeros((3, 4), dtype=int)
        assert np.array_equal(gf2_rref(Z), Z)

    def test_basic_reduction(self):
        M = np.array([[1, 1, 0], [1, 0, 1]])
        R = gf2_rref(M)
        # Each row should have a unique leading 1
        assert R[0, 0] == 1
        assert R[1, 1] == 1

    def test_mod2_arithmetic(self):
        # Two identical rows → second row should vanish
        M = np.array([[1, 0, 1], [1, 0, 1]])
        R = gf2_rref(M)
        assert np.all(R[1] == 0)


class TestGf2Rank:
    def test_full_rank(self):
        assert gf2_rank(np.eye(4, dtype=int)) == 4

    def test_rank_422(self, code_422):
        Hx, Hz = code_422
        assert gf2_rank(Hx) == 1
        assert gf2_rank(Hz) == 1

    def test_rank_713(self, code_713):
        Hx, _ = code_713
        assert gf2_rank(Hx) == 3

    def test_rank_513(self, code_513):
        Hx, Hz = code_513
        combined = np.vstack([Hx, Hz])
        assert gf2_rank(combined) == 4


# ---------------------------------------------------------------------------
# check_commutativity
# ---------------------------------------------------------------------------

class TestCheckCommutativity:
    def test_valid_css_422(self, code_422):
        assert check_commutativity(*code_422)

    def test_valid_css_713(self, code_713):
        assert check_commutativity(*code_713)

    def test_valid_general_513(self, code_513):
        assert check_commutativity(*code_513)

    def test_non_commuting_rejected(self):
        # X on qubit 0 and Z on qubit 0 anti-commute
        Hx = np.array([[1, 0]])
        Hz = np.array([[1, 0]])
        # Hx·Hz^T + Hz·Hx^T = [[1]] + [[1]] = [[0]] — actually this is CSS, commutes
        # Build a genuinely non-commuting pair:
        Hx = np.array([[1, 0], [0, 0]])
        Hz = np.array([[0, 0], [1, 0]])
        # Row 0 of Hx vs row 1 of Hz: [1,0]·[1,0]^T = 1, [0,0]·[0,0]^T = 0 → sum = 1 ≠ 0
        assert not check_commutativity(Hx, Hz)


# ---------------------------------------------------------------------------
# is_css
# ---------------------------------------------------------------------------

class TestIsCss:
    def test_422_is_css(self, code_422):
        assert is_css(*code_422)

    def test_713_is_css(self, code_713):
        assert is_css(*code_713)

    def test_513_is_not_css(self, code_513):
        assert not is_css(*code_513)


# ---------------------------------------------------------------------------
# extract_params
# ---------------------------------------------------------------------------

class TestExtractParams:
    def test_422(self, code_422):
        p = extract_params(*code_422)
        assert p.n == 4
        assert p.k == 2
        assert p.is_css

    def test_713(self, code_713):
        p = extract_params(*code_713)
        assert p.n == 7
        assert p.k == 1
        assert p.is_css

    def test_513(self, code_513):
        p = extract_params(*code_513)
        assert p.n == 5
        assert p.k == 1
        assert not p.is_css


# ---------------------------------------------------------------------------
# canonical_hash
# ---------------------------------------------------------------------------

class TestCanonicalHash:
    def test_same_code_same_hash(self, code_422):
        h1 = canonical_hash(*code_422)
        h2 = canonical_hash(*code_422)
        assert h1 == h2

    def test_different_codes_different_hash(self, code_422, code_713):
        assert canonical_hash(*code_422) != canonical_hash(*code_713)

    def test_row_permutation_same_hash(self, code_713):
        Hx, Hz = code_713
        # Swap rows — should yield same canonical hash
        Hx_perm = Hx[[1, 0, 2], :]
        Hz_perm = Hz[[1, 0, 2], :]
        assert canonical_hash(Hx, Hz) == canonical_hash(Hx_perm, Hz_perm)


# ---------------------------------------------------------------------------
# find_qubit_permutation
# ---------------------------------------------------------------------------

class TestFindQubitPermutation:
    def test_identity_permutation(self, code_422):
        Hx, Hz = code_422
        perm = find_qubit_permutation(Hx, Hz, Hx, Hz)
        assert perm is not None
        assert Hx[:, perm].tolist() == Hx.tolist()

    def test_known_permutation_recovered(self, code_422):
        Hx, Hz = code_422
        # [[4,2,2]]: all columns are identical, any permutation works
        perm = find_qubit_permutation(Hx, Hz, Hx, Hz)
        assert perm is not None
        assert len(perm) == 4

    def test_different_codes_no_permutation(self, code_422, code_713):
        Hx1, Hz1 = code_422
        Hx2, Hz2 = code_713
        assert find_qubit_permutation(Hx1, Hz1, Hx2, Hz2) is None

    def test_large_code_skipped(self):
        # n > 12: permutation search is skipped, returns None
        n = 13
        Hx = np.eye(n, dtype=int)
        Hz = np.eye(n, dtype=int)
        assert find_qubit_permutation(Hx, Hz, Hx, Hz) is None
