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
