"""Tests for the non-CSS ingestion path (compute_code_data_h)."""

import numpy as np
import pytest

from scripts.add_circuit.compute import compute_code_data, compute_code_data_h


def _five_qubit_matrices():
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


def _steane_block_diagonal_H():
    Hx = np.array(
        [
            [1, 0, 1, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1],
        ]
    )
    Hz = Hx.copy()
    # Block-diagonal symplectic form
    n = 7
    top = np.hstack([Hx, np.zeros((Hx.shape[0], n), dtype=int)])
    bot = np.hstack([np.zeros((Hz.shape[0], n), dtype=int), Hz])
    return np.vstack([top, bot])


class TestComputeCodeDataHNonCss:
    def test_five_qubit_basic_shape(self):
        Hx, Hz = _five_qubit_matrices()
        H = np.hstack([Hx, Hz])
        result = compute_code_data_h(H, n=5, d=3)
        code = result["code"]
        assert code["is_css"] is False
        assert code["hx"] is None
        assert code["hz"] is None
        assert code["logical_x"] is None
        assert code["logical_z"] is None
        assert np.array(code["h"]).shape == (4, 10)
        assert np.array(code["logical"]).shape == (2, 10)
        assert (code["n"], code["k"], code["d"]) == (5, 1, 3)

    def test_no_css_tag_for_non_css(self):
        Hx, Hz = _five_qubit_matrices()
        H = np.hstack([Hx, Hz])
        result = compute_code_data_h(H, n=5, d=3)
        tag_names = [t["name"] for t in result["code"]["tags"]]
        assert "CSS" not in tag_names

    def test_originals_populated(self):
        Hx, Hz = _five_qubit_matrices()
        H = np.hstack([Hx, Hz])
        result = compute_code_data_h(H, n=5, d=3)
        om = result["original_matrices"]
        assert om["hx"] is None
        assert om["hz"] is None
        assert np.array_equal(om["h"], H.tolist())
        assert np.array(om["logical"]).shape == (2, 10)

    def test_canonical_hash_stable_across_qubit_relabel(self):
        """Same code submitted with permuted qubits hashes the same."""
        Hx, Hz = _five_qubit_matrices()
        H1 = np.hstack([Hx, Hz])
        col_order = [3, 1, 4, 0, 2]
        H2 = np.hstack([Hx[:, col_order], Hz[:, col_order]])
        r1 = compute_code_data_h(H1, n=5, d=3)
        r2 = compute_code_data_h(H2, n=5, d=3)
        assert r1["code"]["canonical_hash"] == r2["code"]["canonical_hash"]


class TestComputeCodeDataHCssAutoDetect:
    def test_steane_via_h_routes_to_css(self):
        """Submitting Steane's block-diagonal H should auto-detect CSS and
        populate hx/hz/lx/lz plus the CSS tag."""
        H = _steane_block_diagonal_H()
        result = compute_code_data_h(H, n=7, d=3)
        code = result["code"]
        assert code["is_css"] is True
        assert code["hx"] is not None
        assert code["hz"] is not None
        assert code["logical_x"] is not None
        assert code["logical_z"] is not None
        # h and logical are still populated (CSS path also fills them).
        assert np.array(code["h"]).shape[1] == 14  # 2n
        assert np.array(code["logical"]).shape[1] == 14
        tag_names = [t["name"] for t in code["tags"]]
        assert "CSS" in tag_names


class TestComputeCodeDataCssGuard:
    def test_non_css_hxhz_rejected(self):
        """compute_code_data with non-CSS Hx/Hz raises a clear ValueError."""
        Hx, Hz = _five_qubit_matrices()
        with pytest.raises(ValueError, match="CSS"):
            compute_code_data(Hx, Hz, d=3)

    def test_non_css_compute_logicals_rejected(self):
        """The legacy CSS-only _compute_logicals fails fast on non-CSS input."""
        from scripts.add_circuit.compute import _compute_logicals

        Hx, Hz = _five_qubit_matrices()
        with pytest.raises(AssertionError, match="(?i)non-css"):
            _compute_logicals(Hx, Hz, code_is_css=False, d=3)
