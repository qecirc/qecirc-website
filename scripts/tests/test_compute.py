"""
Tests for compute.py — code-level computation.
"""

import tempfile
from pathlib import Path

import numpy as np
import pytest
import yaml

from scripts.add_circuit.compute import (
    _compute_logicals_css,
    _is_self_dual,
    compute_code_data,
    compute_code_data_h,
    slugify,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def steane_H():
    return np.array(
        [
            [1, 0, 1, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1],
        ]
    )


@pytest.fixture
def code_422():
    Hx = np.array([[1, 1, 1, 1]])
    Hz = np.array([[1, 1, 1, 1]])
    return Hx, Hz


# ---------------------------------------------------------------------------
# compute_code_data
# ---------------------------------------------------------------------------


class TestComputeCodeData:
    def test_steane_params(self, steane_H):
        result = compute_code_data(steane_H, steane_H, d=3, code_name="Steane Code")
        code = result["code"]
        assert code["n"] == 7
        assert code["k"] == 1
        assert code["d"] == 3

    def test_steane_tags(self, steane_H):
        result = compute_code_data(steane_H, steane_H, d=3)
        code = result["code"]
        tag_names = [t["name"] for t in code["tags"]]
        assert "CSS" in tag_names
        assert "self-dual" in tag_names

    def test_no_duplicate_tags(self, steane_H):
        result = compute_code_data(steane_H, steane_H, d=3)
        tag_names = [t["name"] for t in result["code"]["tags"]]
        assert len(tag_names) == len(set(tag_names))

    def test_logicals_shape(self, steane_H):
        result = compute_code_data(steane_H, steane_H, d=3)
        code = result["code"]
        # k=1, n=7, so symplectic logical has shape (2k, 2n) = (2, 14).
        logical = np.array(code["logical"])
        assert logical.shape == (2, 14)

    def test_canonical_hash_present(self, steane_H):
        result = compute_code_data(steane_H, steane_H, d=3)
        assert result["code"]["canonical_hash"]
        assert len(result["code"]["canonical_hash"]) == 64  # SHA256 hex

    def test_new_code_status(self, steane_H):
        result = compute_code_data(steane_H, steane_H, d=3)
        assert result["code"]["status"] == "new"
        assert result["code"]["id"] is None

    def test_slug(self, steane_H):
        result = compute_code_data(steane_H, steane_H, d=3, code_name="Steane Code")
        assert result["code"]["slug"] == "steane-code"

    def test_zoo_url(self, steane_H):
        result = compute_code_data(steane_H, steane_H, d=3, zoo_url="https://example.com")
        assert result["code"]["zoo_url"] == "https://example.com"

    def test_non_css_hash_is_deterministic(self):
        """compute_code_data_h returns a deterministic canonical_hash for a
        non-CSS code. canonical_hash_h is NOT invariant under qubit permutations
        of the input (see plan task 4 for permuted-submission handling)."""
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
        H = np.hstack([Hx, Hz])
        result1 = compute_code_data_h(H, n=5, d=3)
        result2 = compute_code_data_h(H, n=5, d=3)

        # Same input → same hash (deterministic)
        assert result1["code"]["canonical_hash"] == result2["code"]["canonical_hash"]
        assert len(result1["code"]["canonical_hash"]) == 64  # SHA256 hex

    def test_original_matrices_returned(self, steane_H):
        result = compute_code_data(steane_H, steane_H, d=3)
        om = result["original_matrices"]
        # Originals carry only the symplectic h/logical; the CSS view is
        # derived in the UI via splitHToCss.
        assert set(om.keys()) == {"h", "logical"}
        # h is the block-stack of the input Hx, Hz (Steane is self-dual).
        from scripts.add_circuit.code_identify import build_symplectic_h

        expected_h = build_symplectic_h(steane_H, steane_H).tolist()
        assert om["h"] == expected_h

    def test_original_logicals_from_pre_canonicalization(self):
        """Original logicals are computed from input matrices, not canonical ones."""
        # Non-CSS [[5,1,3]] code via H input.
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
        H = np.hstack([Hx, Hz])
        result = compute_code_data_h(H, n=5, d=3)
        om = result["original_matrices"]
        # Non-CSS originals carry only h/logical (no CSS view): h equals the
        # submitted H exactly, and logical commutes with H symplectically.
        assert set(om.keys()) == {"h", "logical"}
        assert np.array_equal(om["h"], H.tolist())
        orig_logical = np.array(om["logical"])
        # logical · Λ · Hᵀ = 0 mod 2  (commutes with all stabilizers)
        H_swap = np.hstack([H[:, 5:], H[:, :5]])
        assert np.all((orig_logical @ H_swap.T) % 2 == 0)

    def test_logicals_consistent_with_canonical_h(self):
        """For non-CSS codes, ``logical`` is a symplectic matrix that commutes
        with the canonical H and pairs as 1 X-bar + 1 Z-bar (k=1)."""
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
        H = np.hstack([Hx, Hz])
        result = compute_code_data_h(H, n=5, d=3)
        code = result["code"]
        n, k = code["n"], code["k"]
        assert (n, k, code["d"]) == (5, 1, 3)
        canon_H = np.array(code["h"])
        logical = np.array(code["logical"])
        # logical commutes with all stabilizers symplectically
        H_swap = np.hstack([canon_H[:, n:], canon_H[:, :n]])
        assert np.all((logical @ H_swap.T) % 2 == 0)
        # Symplectic pairing: L_X · Λ · L_Zᵀ = I_k
        log_swap = np.hstack([logical[:, n:], logical[:, :n]])
        gram = (logical @ log_swap.T) % 2
        # Off-anti-diagonal block: rows 0..k-1 (X-bars) vs rows k..2k-1 (Z-bars)
        # Pairing block must equal I_k.
        assert np.array_equal(gram[:k, k:], np.eye(k, dtype=int))
        assert np.array_equal(gram[k:, :k], np.eye(k, dtype=int))
        # X-bars commute with X-bars; Z-bars commute with Z-bars.
        assert np.all(gram[:k, :k] == 0)
        assert np.all(gram[k:, k:] == 0)

    def test_yaml_dedup_existing(self, steane_H):
        """When code exists in data_yaml/codes/, status is 'existing'."""
        from scripts.add_circuit.code_identify import build_symplectic_h, canonical_hash

        c_hash = canonical_hash(steane_H, steane_H)
        h = build_symplectic_h(steane_H, steane_H).tolist()

        with tempfile.TemporaryDirectory() as tmpdir:
            codes_dir = Path(tmpdir) / "codes"
            codes_dir.mkdir()
            code_yaml = {
                "name": "Steane Code",
                "n": 7,
                "k": 1,
                "d": 3,
                "canonical_hash": c_hash,
                "h": h,
            }
            (codes_dir / "steane-code.yaml").write_text(yaml.dump(code_yaml))

            result = compute_code_data(steane_H, steane_H, d=3, data_dir=tmpdir)
            assert result["code"]["status"] == "existing"
            # Identity permutation is normalized to None (no relabeling needed)
            assert result["qubit_permutation"] is None


# ---------------------------------------------------------------------------
# _is_self_dual
# ---------------------------------------------------------------------------


class TestIsSelfDual:
    def test_steane_is_self_dual(self, steane_H):
        assert _is_self_dual(steane_H, steane_H) is True

    def test_asymmetric_not_self_dual(self):
        Hx = np.array([[1, 1, 0, 0], [0, 0, 1, 1]])
        Hz = np.array([[1, 0, 1, 0]])
        assert _is_self_dual(Hx, Hz) is False

    def test_non_css_not_self_dual(self):
        Hx = np.array([[1, 0], [0, 0]])
        Hz = np.array([[0, 0], [1, 0]])
        assert _is_self_dual(Hx, Hz) is False


# ---------------------------------------------------------------------------
# _compute_logicals_css
# ---------------------------------------------------------------------------


class TestComputeLogicals:
    def test_steane_logicals_valid(self, steane_H):
        Lx, Lz = _compute_logicals_css(steane_H, steane_H, 3)
        # Lx in ker(Hz): Hz @ Lx.T = 0 mod 2
        assert np.all(steane_H @ Lx.T % 2 == 0)
        # Lz in ker(Hx): Hx @ Lz.T = 0 mod 2
        assert np.all(steane_H @ Lz.T % 2 == 0)
        # Lx @ Lz.T = I_k mod 2
        assert np.all(Lx @ Lz.T % 2 == np.eye(1, dtype=int))


# ---------------------------------------------------------------------------
# slugify
# ---------------------------------------------------------------------------


class TestSlugify:
    def test_basic(self):
        assert slugify("Steane Code") == "steane-code"

    def test_special_chars(self):
        assert slugify("[[7,1,3]] Code!") == "7-1-3-code"

    def test_already_slug(self):
        assert slugify("steane-code") == "steane-code"
