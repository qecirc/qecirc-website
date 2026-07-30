"""Tests for the non-CSS ingestion path (compute_code_data_h)."""

from pathlib import Path

import numpy as np
import pytest

from scripts.add_circuit.compute import compute_code_data, compute_code_data_h

FIXTURES = Path(__file__).parent / "fixtures"


def _load_108_8_10() -> tuple[np.ndarray, np.ndarray]:
    """Parse the [[108,8,10]] Hx/Hz blocks from the test fixture."""
    text = (FIXTURES / "108_8_10.txt").read_text()
    blocks = [b for b in text.split("\n\n") if b.strip()]
    Hx = np.array([[int(x) for x in line.split()] for line in blocks[0].strip().split("\n")])
    Hz = np.array([[int(x) for x in line.split()] for line in blocks[1].strip().split("\n")])
    return Hx, Hz


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

    def test_original_h_is_submission_verbatim(self):
        """Issue #138: the H= path must store the submitted H as the original,
        not the RREF basis split_h_to_css produces to detect CSS structure."""
        H = _steane_block_diagonal_H()
        # Scramble away from RREF without changing the row space: add row 1
        # into row 0, append a redundant row, and reverse the row order.
        scrambled = H.copy()
        scrambled[0] = (scrambled[0] + scrambled[1]) % 2
        scrambled = np.vstack([scrambled, (scrambled[2] + scrambled[3]) % 2])[::-1]

        result = compute_code_data_h(scrambled, n=7, d=3)
        assert result["code"]["is_css"] is True
        om = result["original_matrices"]
        assert np.array_equal(om["h"], scrambled.tolist())
        # The original logicals are in the submitted column order and must
        # commute with the submitted stabilizers: logical · Λ · Hᵀ = 0.
        orig_logical = np.array(om["logical"])
        H_swap = np.hstack([scrambled[:, 7:], scrambled[:, :7]])
        assert np.all((orig_logical @ H_swap.T) % 2 == 0)

    def test_original_h_verbatim_with_mixed_rows(self):
        """A submitted row may mix X and Z (sum of an X- and a Z-check) while
        the row *space* is still CSS. The original must keep that row as-is."""
        H = _steane_block_diagonal_H()
        mixed = H.copy()
        mixed[0] = (mixed[0] + mixed[3]) % 2  # X-check + Z-check
        assert mixed[0, :7].any() and mixed[0, 7:].any()  # genuinely mixed

        result = compute_code_data_h(mixed, n=7, d=3)
        # Still detected as CSS (row space unchanged) ...
        assert result["code"]["is_css"] is True
        # ... but the stored original is the submission, mixed row included.
        assert np.array_equal(result["original_matrices"]["h"], mixed.tolist())


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


class TestUncertainDedup:
    """Tests for the new uncertain-dedup path (Phase 2 of _check_yaml_dedup)."""

    @pytest.fixture(autouse=True)
    def _shrink_budget(self, monkeypatch):
        """Use a short budget so tests don't sit at the 10-second default."""
        from scripts.add_circuit import compute as _compute

        monkeypatch.setattr(_compute, "DEDUP_BUDGET_SECONDS", 0.5)

    @staticmethod
    def _seed_108_8_10(tmp_path):
        """Write the [[108,8,10]] code to data_yaml/codes/."""
        from scripts.add_circuit.yaml_helpers import build_code_yaml, dump_yaml

        Hx, Hz = _load_108_8_10()
        (tmp_path / "codes").mkdir(parents=True, exist_ok=True)
        (tmp_path / "circuits" / "originals").mkdir(parents=True, exist_ok=True)
        result = compute_code_data(Hx, Hz, d=10, code_name="[[108,8,10]]", data_dir=str(tmp_path))
        (tmp_path / "codes" / "108-8-10.yaml").write_text(
            dump_yaml(build_code_yaml(result["code"]))
        )
        return Hx, Hz

    def test_phase2_recovers_after_forced_hash_miss(self, tmp_path):
        """Forces a Phase-1 hash miss against a seeded Steane (by writing a
        deliberately wrong canonical_hash into the YAML) and verifies that the
        Phase-2 permutation-equivalence scan still recovers the match with a
        valid σ. Steane is small enough that backtracking finishes well within
        the budget — this proves the Phase-2 code path is exercised."""
        from scripts.add_circuit import find_existing_code_full
        from scripts.add_circuit.code_identify import build_symplectic_h, gf2_row_basis
        from scripts.add_circuit.yaml_helpers import build_code_yaml, dump_yaml

        Hx = np.array(
            [
                [1, 0, 1, 0, 1, 0, 1],
                [0, 1, 1, 0, 0, 1, 1],
                [0, 0, 0, 1, 1, 1, 1],
            ]
        )
        Hz = Hx.copy()
        (tmp_path / "codes").mkdir(parents=True, exist_ok=True)
        seed = compute_code_data(Hx, Hz, d=3, code_name="Steane", data_dir=str(tmp_path))
        # Corrupt the stored canonical_hash so Phase 1 misses; the actual h
        # matrix is unchanged, so Phase 2 should still match.
        seed["code"]["canonical_hash"] = "0" * 64
        (tmp_path / "codes" / "steane.yaml").write_text(dump_yaml(build_code_yaml(seed["code"])))

        p = [3, 1, 5, 0, 6, 2, 4]
        Hx_p, Hz_p = Hx[:, p], Hz[:, p]
        match = find_existing_code_full(Hx_p, Hz_p, data_dir=str(tmp_path))
        assert match is not None
        assert match.status == "match"
        assert match.slug == "steane"
        # Verify the returned σ actually relabels the submission to match the
        # stored code's row space.
        sigma = match.qubit_permutation
        assert sigma is not None
        cols = list(sigma) + [s + 7 for s in sigma]
        H_user = build_symplectic_h(Hx_p, Hz_p)
        H_stored = build_symplectic_h(Hx, Hz)
        assert np.array_equal(gf2_row_basis(H_user[:, cols]), gf2_row_basis(H_stored))

    def test_108_8_10_permuted_raises_uncertain(self, tmp_path):
        """[[108,8,10]] under a non-trivial qubit perm: cheap invariants match
        but backtracking times out → add_circuit must raise UncertainDedupError."""
        from scripts.add_circuit import UncertainDedupError, add_circuit

        Hx, Hz = self._seed_108_8_10(tmp_path)

        p = list(range(108))
        p[0], p[1] = p[1], p[0]
        with pytest.raises(UncertainDedupError) as exc:
            add_circuit(
                circuit="I 0",
                circuit_name="permuted",
                d=10,
                Hx=Hx[:, p],
                Hz=Hz[:, p],
                code_name="[[108,8,10]] permuted",
                data_dir=str(tmp_path),
                source="test",
            )
        assert "108-8-10" in exc.value.candidates
        assert exc.value.n == 108
        assert exc.value.k == 8

    def test_108_8_10_assume_new_overrides(self, tmp_path):
        """`assume_new=True` must suppress the uncertain error and add as new."""
        from scripts.add_circuit import add_circuit

        Hx, Hz = self._seed_108_8_10(tmp_path)
        p = list(range(108))
        p[0], p[1] = p[1], p[0]

        result = add_circuit(
            circuit="I 0",
            circuit_name="permuted-as-new",
            d=10,
            Hx=Hx[:, p],
            Hz=Hz[:, p],
            code_name="[[108,8,10]]-perm",
            data_dir=str(tmp_path),
            source="test",
            assume_new=True,
        )
        assert result.code_status == "new"
        assert result.code_slug == "108-8-10-perm"

    def test_find_existing_code_full_surfaces_uncertain(self, tmp_path):
        """find_existing_code_full must report status='uncertain' and list the
        candidate slug rather than swallowing it as 'no match'."""
        from scripts.add_circuit import find_existing_code_full

        Hx, Hz = self._seed_108_8_10(tmp_path)
        p = list(range(108))
        p[0], p[1] = p[1], p[0]

        match = find_existing_code_full(Hx[:, p], Hz[:, p], data_dir=str(tmp_path))
        assert match is not None
        assert match.status == "uncertain"
        assert match.slug is None  # do not leak a confirmed-looking slug
        assert match.uncertain_candidates == ["108-8-10"]
        assert match.qubit_permutation is None


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
        assert any(p.endswith(".original.stim") for p in paths)
        # Shared matrices file, named by content digest.
        assert any("/matrices/" in p for p in result.files_written)


class TestExistingNonCssCodeSlug:
    """A non-CSS submission that matches a stored code must file under the
    stored slug.

    It used not to: `code_slug` — or a slug derived from `code_name` — won over
    the code the submission actually matched, so the circuit was written as
    `five-qubit-perfect-code--<circuit>.yaml` while the code lives at
    `five-qubit-code`. No code YAML was written under that name (there was no
    new code), leaving circuit files that reference an entry which does not
    exist; `annotate_circuits.py` reported `code '...' not found` and
    `db:create` rejected them. The CSS path never had this — these tests pin the
    two paths to the same behaviour.
    """

    @staticmethod
    def _five_qubit_h():
        Hx, Hz = _five_qubit_matrices()
        return np.hstack([Hx, Hz])

    def _add(self, tmp_path, **kwargs):
        from scripts.add_circuit import add_circuit

        return add_circuit(
            circuit="I 0 1 2 3 4",
            circuit_name="Slug Probe",
            d=3,
            H=self._five_qubit_h(),
            n=5,
            source="test://example",
            data_dir="data_yaml",
            dry_run=True,
            **kwargs,
        )

    def test_code_name_does_not_override_the_matched_slug(self, tmp_path):
        result = self._add(tmp_path, code_name="Five-Qubit Perfect Code")
        assert result.code_status == "existing"
        assert result.code_slug == "five-qubit-code"

    def test_code_slug_does_not_override_the_matched_slug(self, tmp_path):
        """`code_slug` is documented as naming a *new* code, and on a match
        there is no new code to name."""
        result = self._add(tmp_path, code_name="Anything", code_slug="5-1-3")
        assert result.code_status == "existing"
        assert result.code_slug == "five-qubit-code"

    def test_the_circuit_files_are_named_after_the_code_that_exists(self, tmp_path):
        from pathlib import Path

        result = self._add(tmp_path, code_name="Five-Qubit Perfect Code")
        stems = {Path(p).name.split("--")[0] for p in result.files_written if "--" in p}
        assert stems == {"five-qubit-code"}
        # and nothing is written for a code that does not exist
        assert not any(
            Path(p).name.startswith("five-qubit-perfect-code") for p in result.files_written
        )
