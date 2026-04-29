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
