"""
Tests for tag_suggest.py.
"""

import pytest

from scripts.add_circuit.models import CodeParams
from scripts.add_circuit.tag_suggest import (
    CircuitProperties,
    suggest_circuit_tags,
    suggest_classification_tags,
    suggest_code_tags,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def params_422():
    return CodeParams(n=4, k=2, is_css=True, d=2)


@pytest.fixture
def params_713():
    return CodeParams(n=7, k=1, is_css=True, d=3)


@pytest.fixture
def params_513():
    return CodeParams(n=5, k=1, is_css=False, d=3)


@pytest.fixture
def props_encoding():
    return CircuitProperties(
        qubit_count=4, depth=3, gate_count=4, detected_functionality="encoding"
    )


# ---------------------------------------------------------------------------
# suggest_code_tags
# ---------------------------------------------------------------------------


class TestSuggestCodeTags:
    def test_css_tag_present_for_css_code(self, params_422):
        tags = suggest_code_tags(params_422)
        names = [t.name for t in tags]
        assert "CSS" in names

    def test_no_css_tag_for_general_code(self, params_513):
        tags = suggest_code_tags(params_513)
        names = [t.name for t in tags]
        assert "CSS" not in names

    def test_no_nkd_tag(self, params_422):
        tags = suggest_code_tags(params_422)
        nkd_tags = [t for t in tags if t.name.startswith("[[")]
        assert len(nkd_tags) == 0


# ---------------------------------------------------------------------------
# suggest_classification_tags
# ---------------------------------------------------------------------------


class TestSuggestClassificationTags:
    def test_single_round_flagged_without_repeat(self):
        circuit = "H 4\nCNOT 4 0\nM 4\n"
        tags = suggest_classification_tags("syndrome-extraction", circuit)
        names = [t.name for t in tags]
        assert "single-round" in names

    def test_no_single_round_with_repeat(self):
        circuit = "REPEAT 10 {\nH 4\nCNOT 4 0\nM 4\n}\n"
        tags = suggest_classification_tags("syndrome-extraction", circuit)
        names = [t.name for t in tags]
        assert "single-round" not in names

    def test_fault_tolerant_flagged_with_flag_in_comment(self):
        # "flag" in a comment triggers the heuristic (common annotation pattern)
        circuit = "# flag qubit\nH 5\nCNOT 5 0\nM 5\n"
        tags = suggest_classification_tags("syndrome-extraction", circuit)
        names = [t.name for t in tags]
        assert "fault-tolerant" in names

    def test_fault_tolerant_not_triggered_by_substring(self):
        # "flagged" should not trigger (whole word match)
        circuit = "# flagged for review\nH 5\nCNOT 5 0\nM 5\n"
        tags = suggest_classification_tags("syndrome-extraction", circuit)
        names = [t.name for t in tags]
        assert "fault-tolerant" not in names

    def test_functionality_added_as_tag(self):
        circuit = "CNOT 0 1\n"
        tags = suggest_classification_tags("encoding", circuit)
        names = [t.name for t in tags]
        assert "encoding" in names

    def test_syndrome_extraction_added_as_tag(self):
        circuit = "REPEAT 10 {\nH 4\nCNOT 4 0\nM 4\n}\n"
        tags = suggest_classification_tags("syndrome-extraction", circuit)
        names = [t.name for t in tags]
        assert "syndrome-extraction" in names


# ---------------------------------------------------------------------------
# suggest_circuit_tags
# ---------------------------------------------------------------------------


class TestSuggestCircuitTags:
    def test_depth_tag_confirmed(self, params_422, props_encoding):
        tags = suggest_circuit_tags(props_encoding, params_422)
        depth_tags = [t for t in tags if t.name.startswith("depth:")]
        assert len(depth_tags) == 1
        assert depth_tags[0].status == "confirmed"

    def test_no_distance_tag(self, params_422, props_encoding):
        tags = suggest_circuit_tags(props_encoding, params_422)
        dist_tags = [t for t in tags if t.name.startswith("distance:")]
        assert len(dist_tags) == 0
