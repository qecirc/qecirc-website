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

    def test_canonical_hash_is_deterministic(self):
        """canonical_hash_h is deterministic for a given input. It is NOT
        invariant under qubit permutations — non-CSS dedup matches only on
        exact canonical form. (See plan task 4 for permuted-submission handling.)"""
        Hx, Hz = _five_qubit_matrices()
        H = np.hstack([Hx, Hz])
        r1 = compute_code_data_h(H, n=5, d=3)
        r2 = compute_code_data_h(H, n=5, d=3)
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


class TestYamlDedupH:
    def test_identical_h_dedup_finds_existing(self, tmp_path):
        from scripts.add_circuit import find_existing_code_h

        Hx, Hz = _five_qubit_matrices()
        H = np.hstack([Hx, Hz])
        # Seed data_yaml with the five-qubit code via a dry-run-style write.
        codes_dir = tmp_path / "codes"
        codes_dir.mkdir(parents=True)
        result = compute_code_data_h(H, n=5, d=3, code_name="Five-Qubit", data_dir=str(tmp_path))
        from scripts.add_circuit.yaml_helpers import build_code_yaml, dump_yaml
        (codes_dir / "five-qubit.yaml").write_text(dump_yaml(build_code_yaml(result["code"])))

        match = find_existing_code_h(H, n=5, data_dir=str(tmp_path))
        assert match is not None
        assert match.slug == "five-qubit"

    def test_different_h_does_not_dedup(self, tmp_path):
        from scripts.add_circuit import find_existing_code_h
        from scripts.add_circuit.yaml_helpers import build_code_yaml, dump_yaml

        Hx, Hz = _five_qubit_matrices()
        H_a = np.hstack([Hx, Hz])
        codes_dir = tmp_path / "codes"
        codes_dir.mkdir(parents=True)
        seed = compute_code_data_h(H_a, n=5, d=3, code_name="A", data_dir=str(tmp_path))
        (codes_dir / "a.yaml").write_text(dump_yaml(build_code_yaml(seed["code"])))

        # n != 5 so they can't dedup by definition.
        H_b = np.array(
            [
                [1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1],
            ]
        )
        assert find_existing_code_h(H_b, n=4, data_dir=str(tmp_path)) is None

    def test_qubit_permutation_is_real_list_not_silent_none(self, tmp_path):
        """Regression for the bug where find_existing_code_h always returned
        qubit_permutation=None for non-CSS matches, silently wiring circuits
        to the wrong qubits."""
        from scripts.add_circuit import find_existing_code_h
        from scripts.add_circuit.yaml_helpers import build_code_yaml, dump_yaml

        Hx, Hz = _five_qubit_matrices()
        H = np.hstack([Hx, Hz])
        codes_dir = tmp_path / "codes"
        codes_dir.mkdir(parents=True)
        seed = compute_code_data_h(H, n=5, d=3, code_name="Five-Qubit", data_dir=str(tmp_path))
        (codes_dir / "five-qubit.yaml").write_text(dump_yaml(build_code_yaml(seed["code"])))

        # Resubmit the same H. Match must be found and the perm must be the
        # actual canonical_form_h relabel (not a silent None).
        match = find_existing_code_h(H, n=5, data_dir=str(tmp_path))
        assert match is not None
        assert match.slug == "five-qubit"
        # canonical_form_h(H) for this code yields a non-identity qubit_perm,
        # so dedup must return that list rather than silently dropping it.
        from scripts.add_circuit.code_identify import canonical_form_h

        _, expected_perm = canonical_form_h(H, n=5)
        if expected_perm == list(range(5)):
            assert match.qubit_permutation is None
        else:
            assert match.qubit_permutation == expected_perm
