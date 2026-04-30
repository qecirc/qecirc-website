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
        # Non-CSS codes carry no CSS view in the returned dict; the UI hides
        # the Hx/Hz tab when splitHToCss(h, n) returns null.
        for key in ("hx", "hz", "logical_x", "logical_z"):
            assert key not in code
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
        assert set(om.keys()) == {"h", "logical"}
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
        """Submitting Steane's block-diagonal H should auto-detect CSS,
        set the CSS tag, and store h/logical (Hx/Hz are derived in the UI)."""
        H = _steane_block_diagonal_H()
        result = compute_code_data_h(H, n=7, d=3)
        code = result["code"]
        assert code["is_css"] is True
        tag_names = [t["name"] for t in code["tags"]]
        assert "CSS" in tag_names
        assert np.array(code["h"]).shape == (6, 14)
        assert np.array(code["logical"]).shape == (2, 14)
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


class TestAddCircuitH:
    def test_dry_run_writes_expected_files(self, tmp_path):
        from pathlib import Path

        from scripts.add_circuit import add_circuit

        # Set up data_dir scaffolding (must exist for dedup to even attempt).
        (tmp_path / "codes").mkdir()
        (tmp_path / "circuits").mkdir()

        Hx, Hz = _five_qubit_matrices()
        H = np.hstack([Hx, Hz])

        # Trivial 5-qubit "circuit" — not a real encoder, just a stim placeholder.
        circuit_text = "I 0 1 2 3 4"

        result = add_circuit(
            circuit=circuit_text,
            circuit_name="Smoke Test",
            d=3,
            H=H,
            n=5,
            source="test://example",
            code_name="Five-Qubit",
            data_dir=str(tmp_path),
            dry_run=True,
        )

        assert result.dry_run is True
        assert result.code_status == "new"
        # Expect: code yaml + circuit yaml + at least one body + originals
        paths = [Path(p).name for p in result.files_written]
        assert any(p.endswith(".yaml") and "five-qubit" in p for p in paths)
        assert any(p.endswith(".stim") for p in paths)
        assert any(p.endswith(".original.yaml") for p in paths)
