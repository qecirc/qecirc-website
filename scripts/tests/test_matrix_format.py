"""The two YAML encodings of a stored matrix.

The point of the sparse form is that it is invisible: a reader calls `decode`
and cannot tell which was written. So most of these tests are round-trips, and
the ones that are not are about the boundary — which encoding gets chosen, and
what happens when a file claims something the data does not support.
"""

import numpy as np
import pytest
import yaml

from scripts.add_circuit.matrix_format import (
    decode,
    encode,
    is_sparse,
)
from scripts.add_circuit.yaml_helpers import dump_yaml, load_yaml, matrices_digest


def _random(rows: int, cols: int, density: float, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return (rng.random((rows, cols)) < density).astype(int)


class TestChoosingAnEncoding:
    def test_small_matrices_stay_dense(self):
        """Small codes are the ones a person reads; leaving them alone also
        means introducing the sparse form rewrites no existing small file."""
        m = _random(7, 14, 0.5)
        assert encode(m) == m.tolist()
        assert not is_sparse(encode(m))

    def test_large_matrices_go_sparse(self):
        m = _random(400, 800, 0.02)  # 320k entries, past the threshold
        assert is_sparse(encode(m))

    def test_the_threshold_is_on_size_not_density(self):
        """A big *dense* matrix still encodes sparsely. The threshold is about
        how much text a dense row costs, which density does not change."""
        dense = np.ones((400, 800), dtype=int)
        assert is_sparse(encode(dense))

    def test_threshold_is_configurable(self):
        m = _random(7, 14, 0.5)
        assert is_sparse(encode(m, threshold=10))


class TestRoundTrip:
    @pytest.mark.parametrize(
        "rows,cols,density",
        [(7, 14, 0.5), (400, 800, 0.02), (400, 800, 0.9), (1, 1, 0.0), (3, 5, 1.0)],
    )
    def test_decode_inverts_encode(self, rows, cols, density):
        m = _random(rows, cols, density)
        assert np.array_equal(decode(encode(m)), m)

    def test_survives_a_yaml_round_trip(self):
        """Encoding is only useful if it survives the writer and reader we
        actually use, flow-style lists and all."""
        m = _random(400, 800, 0.02)
        restored = load_yaml(dump_yaml({"h": encode(m)}))["h"]
        assert np.array_equal(decode(restored), m)

    def test_an_all_zero_row_round_trips(self):
        m = np.zeros((400, 800), dtype=int)
        m[0, 0] = 1
        out = encode(m)
        assert out["nonzero"][1] == []
        assert np.array_equal(decode(out), m)

    def test_decode_accepts_a_dense_list(self):
        assert np.array_equal(decode([[1, 0], [0, 1]]), np.eye(2, dtype=int))

    def test_values_are_reduced_mod_two(self):
        assert np.array_equal(decode(encode([[2, 3]])), np.array([[0, 1]]))


class TestRefusals:
    def test_rejects_a_non_matrix(self):
        with pytest.raises(ValueError, match="2-D"):
            encode([1, 0, 1])

    def test_rejects_a_row_count_that_disagrees_with_the_data(self):
        with pytest.raises(ValueError, match="rows"):
            decode({"rows": 3, "cols": 4, "nonzero": [[0], [1]]})

    def test_rejects_a_column_index_out_of_range(self):
        with pytest.raises(ValueError, match="out of range"):
            decode({"rows": 1, "cols": 4, "nonzero": [[9]]})


class TestDigest:
    def test_same_matrices_give_the_same_address(self):
        m, ell = _random(9, 18, 0.4, seed=1), _random(2, 18, 0.4, seed=2)
        a = {"h": encode(m), "logical": encode(ell)}
        b = {"h": encode(m.copy()), "logical": encode(ell.copy())}
        assert matrices_digest(a) == matrices_digest(b)

    def test_different_matrices_give_different_addresses(self):
        a = {"h": encode(_random(9, 18, 0.4, seed=1))}
        b = {"h": encode(_random(9, 18, 0.4, seed=2))}
        assert matrices_digest(a) != matrices_digest(b)

    def test_the_address_names_the_file_that_was_written(self):
        """Hashing the rendered YAML rather than the arrays is what keeps the
        address in step with the bytes on disk."""
        payload = {"h": encode(_random(9, 18, 0.4))}
        digest = matrices_digest(payload)
        assert matrices_digest(yaml.safe_load(dump_yaml(payload))) == digest

    def test_the_address_never_reads_back_as_a_number(self):
        """An all-digit address is a YAML scalar js-yaml reads as an int, losing
        any leading zero. `matrices_digest` slides along the hash instead."""
        for seed in range(400):
            digest = matrices_digest({"h": encode(_random(4, 8, 0.5, seed=seed))})
            assert len(digest) == 16
            assert not digest.isdigit()
            assert isinstance(load_yaml(dump_yaml({"m": digest}))["m"], str)

    def test_a_numeric_window_is_skipped_not_truncated(self, monkeypatch):
        import hashlib

        forced = "1234567890123456" + "abcdef0123456789" + "0" * 32

        class _Fake:
            def hexdigest(self):
                return forced

        monkeypatch.setattr(hashlib, "sha256", lambda _data: _Fake())
        digest = matrices_digest({"h": [[1, 0]]})
        assert len(digest) == 16
        assert not digest.isdigit()
        assert digest in forced


class TestStoredCodeCache:
    """The dedup scan reads every stored code, so it is cached across calls —
    but `add_circuit` writes code files as it goes, so a stale cache would make
    a bulk import blind to the codes it just created."""

    def _write(self, path, text):
        path.write_text(text, encoding="utf-8")

    def test_reuses_a_parse_when_nothing_changed(self, tmp_path):
        from scripts.add_circuit import compute

        codes = tmp_path / "codes"
        codes.mkdir()
        self._write(codes / "a.yaml", "name: A\nn: 7\nk: 1\n")
        first = compute._load_stored_codes(codes)
        second = compute._load_stored_codes(codes)
        assert first == second
        # the same object, not merely an equal one: nothing was re-parsed
        assert first[0][1] is second[0][1]

    def test_sees_a_code_written_after_the_first_scan(self, tmp_path):
        from scripts.add_circuit import compute

        codes = tmp_path / "codes"
        codes.mkdir()
        self._write(codes / "a.yaml", "name: A\nn: 7\nk: 1\n")
        assert [slug for slug, _ in compute._load_stored_codes(codes)] == ["a"]
        self._write(codes / "b.yaml", "name: B\nn: 9\nk: 1\n")
        assert [slug for slug, _ in compute._load_stored_codes(codes)] == ["a", "b"]

    def test_sees_a_code_that_was_rewritten(self, tmp_path):
        from scripts.add_circuit import compute

        codes = tmp_path / "codes"
        codes.mkdir()
        path = codes / "a.yaml"
        self._write(path, "name: A\nn: 7\nk: 1\n")
        assert compute._load_stored_codes(codes)[0][1]["n"] == 7
        # A rewrite that keeps the byte count still has to be noticed, which is
        # why the stamp carries mtime and not just size.
        self._write(path, "name: A\nn: 9\nk: 1\n")
        assert compute._load_stored_codes(codes)[0][1]["n"] == 9


class TestOriginalLogicals:
    """The submitted-order logicals are the canonical ones permuted back, not a
    second independent computation — so they must still be valid logicals."""

    def test_permuting_back_gives_valid_logicals(self):
        import yaml as _yaml

        from scripts.add_circuit.code_identify import canonical_form, split_h_to_css
        from scripts.add_circuit.compute import (
            _compute_logicals_css,
            _logicals_in_original_order,
        )
        from scripts.add_circuit.matrix_format import decode as _decode

        doc = _yaml.safe_load(open("data_yaml/codes/steane-code.yaml"))
        hx, hz = split_h_to_css(_decode(doc["h"]), doc["n"])
        c_hx, c_hz, perm = canonical_form(hx, hz)
        lx, lz = _compute_logicals_css(c_hx, c_hz, 3)
        o_lx, o_lz = _logicals_in_original_order(lx, lz, perm, hx, hz)

        assert o_lx is not None
        assert not (o_lx @ np.asarray(hz).T % 2).any()
        assert not (o_lz @ np.asarray(hx).T % 2).any()
        assert np.array_equal(o_lx @ o_lz.T % 2, np.eye(o_lx.shape[0], dtype=int))

    def test_refuses_a_permutation_of_the_wrong_length(self):
        from scripts.add_circuit.compute import _logicals_in_original_order

        lx = np.array([[1, 1, 1]])
        assert _logicals_in_original_order(lx, lx, [0, 1], lx, lx) == (None, None)
