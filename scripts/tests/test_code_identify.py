"""
Tests for code_identify.py.

Examples used:
  [[4,2,2]] CSS code   -- Hx = Hz = [[1,1,1,1]]
  [[7,1,3]] Steane     -- Hx = Hz = Hamming parity check matrix
  [[5,1,3]] 5-qubit    -- general stabilizer (not CSS)
"""

import numpy as np
import pytest

from scripts.add_circuit.code_identify import (
    canonical_form,
    canonical_hash,
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
    H = np.array(
        [
            [1, 0, 1, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1],
        ]
    )
    return H.copy(), H.copy()


@pytest.fixture
def code_513():
    """[[5,1,3]] 5-qubit perfect code -- general stabilizer, not CSS."""
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
    return Hx, Hz


# ---------------------------------------------------------------------------
# GF(2) linear algebra
# ---------------------------------------------------------------------------


class TestGf2Rref:
    def test_identity_stays_identity(self):
        eye = np.eye(3, dtype=int)
        assert np.array_equal(gf2_rref(eye), eye)

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
        # Two identical rows -> second row should vanish
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

    def test_rank_513_symplectic(self, code_513):
        Hx, Hz = code_513
        # Non-CSS: symplectic matrix [Hx | Hz] has rank 4 (4 independent generators)
        symplectic = np.hstack([Hx, Hz])
        assert gf2_rank(symplectic) == 4


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
# canonical_form
# ---------------------------------------------------------------------------


class TestCanonicalForm:
    def test_returns_rref_matrices(self, code_713):
        Hx, Hz = code_713
        canon_Hx, canon_Hz, perm = canonical_form(Hx, Hz)
        # RREF matrices should have no all-zero rows
        assert np.all(np.any(canon_Hx, axis=1))
        assert np.all(np.any(canon_Hz, axis=1))

    def test_permutation_length(self, code_713):
        Hx, Hz = code_713
        _, _, perm = canonical_form(Hx, Hz)
        assert len(perm) == Hx.shape[1]
        assert sorted(perm) == list(range(Hx.shape[1]))

    def test_column_permutation_gives_same_canonical(self, code_713):
        Hx, Hz = code_713
        # Permute columns
        p = [3, 1, 5, 0, 6, 2, 4]
        Hx_p = Hx[:, p]
        Hz_p = Hz[:, p]
        canon1_Hx, canon1_Hz, _ = canonical_form(Hx, Hz)
        canon2_Hx, canon2_Hz, _ = canonical_form(Hx_p, Hz_p)
        assert np.array_equal(canon1_Hx, canon2_Hx)
        assert np.array_equal(canon1_Hz, canon2_Hz)


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
        Hx_perm = Hx[[1, 0, 2], :]
        Hz_perm = Hz[[1, 0, 2], :]
        assert canonical_hash(Hx, Hz) == canonical_hash(Hx_perm, Hz_perm)

    def test_column_permutation_same_hash(self, code_713):
        Hx, Hz = code_713
        p = [3, 1, 5, 0, 6, 2, 4]
        assert canonical_hash(Hx, Hz) == canonical_hash(Hx[:, p], Hz[:, p])

    def test_column_permutation_same_hash_422(self, code_422):
        Hx, Hz = code_422
        p = [2, 0, 3, 1]
        assert canonical_hash(Hx, Hz) == canonical_hash(Hx[:, p], Hz[:, p])

    def test_column_permutation_same_hash_513(self, code_513):
        Hx, Hz = code_513
        p = [4, 2, 0, 3, 1]
        assert canonical_hash(Hx, Hz) == canonical_hash(Hx[:, p], Hz[:, p])


# ---------------------------------------------------------------------------
# find_qubit_permutation
# ---------------------------------------------------------------------------


class TestFindQubitPermutation:
    def test_identity_permutation(self, code_422):
        Hx, Hz = code_422
        perm = find_qubit_permutation(Hx, Hz, Hx, Hz)
        assert perm is not None
        assert np.array_equal(gf2_rref(Hx[:, perm]), gf2_rref(Hx))

    def test_known_permutation_recovered(self, code_713):
        Hx, Hz = code_713
        p = [3, 1, 5, 0, 6, 2, 4]
        Hx_p = Hx[:, p]
        Hz_p = Hz[:, p]
        perm = find_qubit_permutation(Hx_p, Hz_p, Hx, Hz)
        assert perm is not None
        assert np.array_equal(gf2_rref(Hx_p[:, perm]), gf2_rref(Hx))
        assert np.array_equal(gf2_rref(Hz_p[:, perm]), gf2_rref(Hz))

    def test_different_codes_no_permutation(self, code_422, code_713):
        Hx1, Hz1 = code_422
        Hx2, Hz2 = code_713
        assert find_qubit_permutation(Hx1, Hz1, Hx2, Hz2) is None

    def test_works_for_large_codes(self):
        """Canonicalization-based approach works for any n, not just n <= 12."""
        # Use a large CSS code (Hx @ Hz.T = 0 mod 2 trivially since Hz = Hx)
        n = 20
        rng = np.random.default_rng(42)
        Hx = rng.integers(0, 2, size=(5, n)).astype(int)
        Hz = Hx.copy()  # self-dual CSS: Hx @ Hx.T = 0 mod 2 for even-weight rows
        # Force even weight rows so Hx @ Hz.T = 0 mod 2
        for i in range(Hx.shape[0]):
            if Hx[i].sum() % 2 == 1:
                Hx[i, 0] ^= 1
                Hz[i, 0] ^= 1
        perm = find_qubit_permutation(Hx, Hz, Hx, Hz)
        assert perm is not None
        assert np.array_equal(gf2_rref(Hx[:, perm]), gf2_rref(Hx))

    def test_513_permutation(self, code_513):
        Hx, Hz = code_513
        p = [4, 2, 0, 3, 1]
        Hx_p = Hx[:, p]
        Hz_p = Hz[:, p]
        perm = find_qubit_permutation(Hx_p, Hz_p, Hx, Hz)
        assert perm is not None
        assert np.array_equal(gf2_rref(Hx_p[:, perm]), gf2_rref(Hx))
        assert np.array_equal(gf2_rref(Hz_p[:, perm]), gf2_rref(Hz))
