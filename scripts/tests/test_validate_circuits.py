"""Tests for validate_circuits.py."""

import yaml

from scripts.validate_circuits import validate_all


def test_skips_non_css_with_explanatory_message(tmp_path):
    # Set up a minimal non-CSS code + tagged encoding circuit.
    (tmp_path / "tools").mkdir()
    (tmp_path / "codes").mkdir()
    (tmp_path / "circuits").mkdir()

    code_yaml = {
        "name": "Test Code",
        "n": 5,
        "k": 1,
        "h": [[1, 0, 0, 0, 1, 1, 1, 0, 1, 1]],
        "logical": [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]],
        "canonical_hash": "sym:5:1:abc",
    }
    (tmp_path / "codes" / "test-code.yaml").write_text(yaml.dump(code_yaml))

    circ_yaml = {
        "qec_id": 9999,
        "name": "Stub",
        "source": "test",
        "tags": ["encoding"],
    }
    (tmp_path / "circuits" / "test-code--stub.yaml").write_text(yaml.dump(circ_yaml))
    (tmp_path / "circuits" / "test-code--stub.stim").write_text("I 0 1 2 3 4")

    results = validate_all(data_dir=str(tmp_path))
    statuses = [c.status for r in results for c in r.checks]
    assert "skipped" in statuses


def test_all_skipped_checks_count_as_skipped_not_failed():
    """A circuit whose only check is 'skipped' (e.g. a non-CSS code) must report
    is_skipped=True and passed=False, so the summary counts it as skipped."""
    from scripts.validate_circuits import CheckResult, CircuitResult

    r = CircuitResult(stem="x--y", circuit_type="state-preparation")
    r.checks.append(CheckResult("load_code", "skipped", "non-CSS validation not yet supported"))
    assert r.is_skipped is True
    assert r.passed is False

    ok = CircuitResult(stem="x--z", circuit_type="encoding")
    ok.checks.append(CheckResult("validate_encoding", "passed"))
    assert ok.is_skipped is False
    assert ok.passed is True
