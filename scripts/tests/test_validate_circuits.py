"""Tests for validate_circuits.py."""

from pathlib import Path

import numpy as np
import yaml

from scripts.validate_circuits import validate_all

# The five-qubit perfect code: non-CSS (every stabilizer mixes X and Z, e.g.
# YZIZY), so it has no Hx/Hz split and used to be skipped entirely.
FIVE_QUBIT_CODE = {
    "name": "Five-Qubit Perfect Code",
    "n": 5,
    "k": 1,
    "d": 3,
    "h": [
        [1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    ],
    "logical": [[1, 0, 1, 1, 0, 0, 0, 1, 1, 0], [0, 0, 1, 1, 0, 1, 0, 0, 0, 0]],
    "canonical_hash": "sym:5:1:abc",
}

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_FIVE_QUBIT_ENCODER = (
    _REPO_ROOT / "data_yaml/circuits/five-qubit-code--circuit-synth-encoding-depth-optimized.stim"
).read_text()


def _build(tmp_path, stim_body, code=None, tags=("encoding",)):
    """Lay out a minimal data_yaml tree with one code and one circuit."""
    for sub in ("tools", "codes", "circuits"):
        (tmp_path / sub).mkdir()
    (tmp_path / "codes" / "test-code.yaml").write_text(yaml.dump(code or FIVE_QUBIT_CODE))
    circ_yaml = {"qec_id": 9999, "name": "Stub", "source": "test", "tags": list(tags)}
    (tmp_path / "circuits" / "test-code--stub.yaml").write_text(yaml.dump(circ_yaml))
    (tmp_path / "circuits" / "test-code--stub.stim").write_text(stim_body)
    return validate_all(data_dir=str(tmp_path))


def _checks(results):
    return {c.name: c for r in results for c in r.checks}


def test_non_css_encoder_is_validated_and_passes(tmp_path):
    """A correct non-CSS encoder must be checked, not skipped."""
    results = _build(tmp_path, _FIVE_QUBIT_ENCODER)
    checks = _checks(results)
    assert checks["validate_encoding"].status == "passed"
    assert checks["logical_input_count"].status == "passed"
    assert results[0].passed is True
    assert results[0].is_skipped is False


def test_non_css_bad_encoder_fails(tmp_path):
    """The gap this closes: an identity circuit does not encode the five-qubit
    code, and must now be reported as failed rather than skipped."""
    results = _build(tmp_path, "I 0 1 2 3 4")
    checks = _checks(results)
    assert checks["validate_encoding"].status == "failed"
    assert results[0].is_skipped is False
    assert results[0].passed is False


def test_logical_input_count_catches_wrong_k(tmp_path):
    """The #134 failure mode: a circuit whose implied logical-input count
    disagrees with the code's k. Here the encoder is genuinely the five-qubit
    code's, but the code claims k=2, so exactly one input goes unaccounted for."""
    code = {**FIVE_QUBIT_CODE, "k": 2}
    results = _build(tmp_path, _FIVE_QUBIT_ENCODER, code=code)
    check = _checks(results)["logical_input_count"]
    assert check.status == "failed"
    assert "implies 1 logical inputs" in check.detail
    assert "k=2" in check.detail


def test_non_css_state_prep_is_validated(tmp_path):
    """State-prep on a non-CSS code takes the same symplectic path."""
    results = _build(tmp_path, "I 0 1 2 3 4", tags=("state-preparation",))
    checks = _checks(results)
    # |00000> is not a five-qubit codeword, so this must be a real verdict.
    assert checks["validate_state_prep"].status == "failed"
    assert "logical_input_count" not in checks  # encoder-only invariant


# A [[3,2,1]] toy: qubit 2 is held at |0> by the lone stabilizer Z2, and qubits
# 0-1 carry the two logical inputs. An encoder need never touch qubit 2, so stim
# sizes it at 2 qubits — narrower than n = 3.
NARROW_CODE = {
    "name": "Narrow",
    "n": 3,
    "k": 2,
    "d": 1,
    "h": [[0, 0, 0, 0, 0, 1]],
    "logical": [
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
    ],
    "canonical_hash": "x",
}

# The 3-qubit repetition code: k=1, stabilizers Z0Z1 and Z1Z2.
REPETITION_CODE = {
    "name": "Rep",
    "n": 3,
    "k": 1,
    "d": 1,
    "h": [[0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 1]],
    "logical": [[0, 0, 0, 0, 0, 1], [1, 1, 1, 0, 0, 0]],
    "canonical_hash": "x",
}


def test_encoder_narrower_than_code_still_checks_inputs(tmp_path):
    """stim sizes a circuit by its highest touched qubit, so a valid encoder can
    be narrower than n. That must not make logical_input_count silently skip —
    silent skipping is the exact failure this check exists to prevent."""
    results = _build(tmp_path, "CX 0 1", code=NARROW_CODE)  # num_qubits = 2 < n = 3
    check = _checks(results)["logical_input_count"]
    assert check.status != "skipped", check.detail
    assert check.status == "passed"


def test_logical_input_count_catches_what_codespace_check_cannot(tmp_path):
    """An all-Z stabilizer group stabilizes |0...0> no matter what the circuit
    does, so the codespace check passes any CNOT circuit on the repetition code.
    Only the input-count invariant notices the encoder is incomplete."""
    # A correct encoder is CX 0 1 + CX 0 2; this one leaves qubit 2 unentangled.
    results = _build(tmp_path, "CX 0 1", code=REPETITION_CODE)
    checks = _checks(results)
    assert checks["validate_encoding"].status == "passed"  # blind to this
    assert checks["logical_input_count"].status == "failed"
    assert "implies 2 logical inputs" in checks["logical_input_count"].detail
    assert results[0].passed is False


# [[4,2,2]] code: Hx = Hz = [1 1 1 1], k = 2 — CSS, so the basis is meaningful.
CODE_422 = {
    "name": "422",
    "n": 4,
    "k": 2,
    "d": 2,
    "h": [[1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1]],
    "logical": [
        [1, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 0],
    ],
    "canonical_hash": "x",
}

ZERO_PREP_422 = "H 0\nCX 0 1 0 2 0 3\n"
PLUS_PREP_422 = ZERO_PREP_422 + "H 0 1 2 3\n"


def test_logical_basis_passes_on_correct_tag(tmp_path):
    results = _build(
        tmp_path, ZERO_PREP_422, code=CODE_422, tags=("state-preparation", "logical-state:zero")
    )
    assert _checks(results)["logical_basis"].status == "passed"


def test_logical_basis_catches_wrong_basis_tag(tmp_path):
    """The error class this check exists for: the body prepares |+>_L but the
    circuit is filed as |0>_L. The codespace check cannot see it — every codeword
    satisfies every stabilizer regardless of logical state."""
    results = _build(
        tmp_path, PLUS_PREP_422, code=CODE_422, tags=("state-preparation", "logical-state:zero")
    )
    checks = _checks(results)
    assert checks["validate_state_prep"].status == "passed"  # blind to this
    assert checks["logical_basis"].status == "failed"
    assert "'x'-basis state" in checks["logical_basis"].detail
    assert results[0].passed is False


def test_logical_basis_skipped_for_non_css(tmp_path):
    """Non-CSS: X-bar/Z-bar labeling is a convention, so there is no
    convention-independent basis to check. Skipped explicitly, with a reason."""
    results = _build(
        tmp_path, _FIVE_QUBIT_ENCODER, tags=("state-preparation", "logical-state:zero")
    )
    check = _checks(results)["logical_basis"]
    assert check.status == "skipped"
    assert "convention" in check.detail


def test_logical_basis_skipped_without_tag(tmp_path):
    results = _build(tmp_path, ZERO_PREP_422, code=CODE_422, tags=("state-preparation",))
    check = _checks(results)["logical_basis"]
    assert check.status == "skipped"
    assert "no logical-state" in check.detail


# One syndrome-extraction round for the repetition code: ancilla 3 reads Z0Z1,
# ancilla 4 reads Z1Z2.
REPETITION_SE = "R 3 4\nCX 0 3 1 3 1 4 2 4\nM 3 4\n"


def test_syndrome_extraction_is_validated_not_skipped(tmp_path):
    """The gap this closes: before the third branch existed, a circuit tagged
    syndrome-extraction matched neither `encoding` nor `state-preparation` and
    was reported as skipped — i.e. published unchecked."""
    results = _build(tmp_path, REPETITION_SE, code=REPETITION_CODE, tags=("syndrome-extraction",))
    assert results[0].circuit_type == "syndrome-extraction"
    assert results[0].is_skipped is False
    assert _checks(results)["validate_syndrome_extraction"].status == "passed"


def test_syndrome_extraction_failure_is_reported(tmp_path):
    """Dropping the last CNOT leaves ancilla 4 reading a bare Z1, which is not in
    the stabilizer group."""
    results = _build(
        tmp_path,
        "R 3 4\nCX 0 3 1 3 1 4\nM 3 4\n",
        code=REPETITION_CODE,
        tags=("syndrome-extraction",),
    )
    check = _checks(results)["validate_syndrome_extraction"]
    assert check.status == "failed"
    assert "outside the stabilizer group" in check.detail
    assert results[0].passed is False


def test_syndrome_extraction_reads_a_sparsely_stored_logical(tmp_path):
    """A big code's `logical` is stored as nonzero column indices, not 0/1 rows.
    Handing that mapping straight to numpy is a TypeError, and the check reported
    an error rather than a result — which is how the [[241,121,3]] hypergraph
    product code's rounds failed the moment its `logical` crossed the threshold.
    """
    from scripts.add_circuit.matrix_format import encode

    code = dict(REPETITION_CODE)
    code["logical"] = encode(REPETITION_CODE["logical"], threshold=1)
    assert isinstance(code["logical"], dict), "fixture must be stored sparsely"

    results = _build(tmp_path, REPETITION_SE, code=code, tags=("syndrome-extraction",))
    assert _checks(results)["validate_syndrome_extraction"].status == "passed"


def test_syndrome_extraction_measuring_the_logical_is_rejected(tmp_path):
    """Reading X0X1X2 is a logical measurement, not a syndrome extraction: it
    collapses the logical state and reads none of the checks.

    (The `L -> L` branch itself is exercised in test_syndrome_extraction.py —
    reaching it from here would need a round that measures the full stabilizer
    group and *still* disturbs a logical, which the group check catches first.)
    """
    results = _build(
        tmp_path,
        "R 3\nH 3\nCX 3 0 3 1 3 2\nH 3\nM 3\n",
        code=REPETITION_CODE,
        tags=("syndrome-extraction",),
    )
    assert _checks(results)["validate_syndrome_extraction"].status == "failed"


def test_all_skipped_checks_count_as_skipped_not_failed():
    """A circuit whose only check is 'skipped' must report is_skipped=True and
    passed=False, so the summary counts it as skipped rather than a failure."""
    from scripts.validate_circuits import CheckResult, CircuitResult

    r = CircuitResult(stem="x--y", circuit_type="state-preparation")
    r.checks.append(CheckResult("load_code", "skipped", "not derivable"))
    assert r.is_skipped is True
    assert r.passed is False

    ok = CircuitResult(stem="x--z", circuit_type="encoding")
    ok.checks.append(CheckResult("validate_encoding", "passed"))
    assert ok.is_skipped is False
    assert ok.passed is True


# Bacon-Shor [[9,1,3]] as the library stores it: `h` is the stabilizer group,
# and the four gauge qubits are recorded separately because k cannot be read off
# `h` alone.
BACON_SHOR_CODE = {
    "name": "Bacon-Shor",
    "n": 9,
    "k": 1,
    "d": 3,
    "gauge_qubits": 4,
    "h": [
        [1, 1, 1, 1, 1, 1, 0, 0, 0] + [0] * 9,
        [0, 0, 0, 1, 1, 1, 1, 1, 1] + [0] * 9,
        [0] * 9 + [1, 1, 0, 1, 1, 0, 1, 1, 0],
        [0] * 9 + [0, 1, 1, 0, 1, 1, 0, 1, 1],
    ],
    "logical": [[1, 0, 0, 1, 0, 0, 1, 0, 0] + [0] * 9, [0] * 9 + [1, 1, 1, 0, 0, 0, 0, 0, 0]],
    "canonical_hash": "x",
}


def test_a_subsystem_encoder_may_expose_more_inputs_than_k(tmp_path):
    """A subsystem code's encoder takes the gauge qubits as inputs too, so
    Bacon-Shor [[9,1,3]] has five and not one. Comparing against k alone failed
    every such encoder — which is why the codes could not be stored at all."""
    from scripts.add_circuit.code_identify import gf2_rank

    h = np.array(BACON_SHOR_CODE["h"])
    assert 9 - gf2_rank(h) == BACON_SHOR_CODE["k"] + BACON_SHOR_CODE["gauge_qubits"] == 5

    results = _build(tmp_path, "I 0 1 2 3 4 5 6 7 8", code=BACON_SHOR_CODE)
    check = _checks(results)["logical_input_count"]
    assert check.status != "error", check.detail
    if check.status == "failed":
        assert "gauge qubits" in check.detail, check.detail


def test_a_wrong_k_is_still_caught_on_a_subsystem_code(tmp_path):
    """The gauge count must not become a licence for any input count: it is
    added to the stored k, not derived from h, so a k that disagrees still
    fails rather than being explained away."""
    code = {**BACON_SHOR_CODE, "k": 3}  # claims 3 + 4 = 7 inputs
    results = _build(tmp_path, _FIVE_QUBIT_ENCODER, code=code)
    check = _checks(results)["logical_input_count"]
    assert check.status == "failed"
    assert "k=3 plus 4 gauge qubits" in check.detail
