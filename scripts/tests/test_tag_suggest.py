"""
Tests for tag_suggest.py.
"""

import numpy as np
import pytest

from scripts.add_circuit.models import CodeParams
from scripts.add_circuit.tag_suggest import (
    suggest_circuit_tags,
    suggest_code_tags,
    suggest_classification_tags,
    CircuitProperties,
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
def Hx_422():
    return np.array([[1, 1, 1, 1]])


@pytest.fixture
def Hz_422():
    return np.array([[1, 1, 1, 1]])


@pytest.fixture
def props_encoding():
    return CircuitProperties(qubit_count=4, depth=3, gate_count=4, detected_functionality="encoding")


# ---------------------------------------------------------------------------
# suggest_code_tags
# ---------------------------------------------------------------------------

class TestSuggestCodeTags:
    def test_css_tag_present_for_css_code(self, params_422, Hx_422, Hz_422):
        tags = suggest_code_tags(params_422, Hx_422, Hz_422)
        names = [t.name for t in tags]
        assert "CSS" in names

    def test_no_css_tag_for_general_code(self, params_513):
        Hx = np.zeros((4, 5), dtype=int)
        Hz = np.zeros((4, 5), dtype=int)
        tags = suggest_code_tags(params_513, Hx, Hz)
        names = [t.name for t in tags]
        assert "CSS" not in names

    def test_nkd_label_confirmed_when_d_known(self, params_422, Hx_422, Hz_422):
        tags = suggest_code_tags(params_422, Hx_422, Hz_422)
        confirmed = [t for t in tags if t.status == "confirmed"]
        nkd_tags = [t for t in confirmed if t.name.startswith("[[")]
        assert len(nkd_tags) == 1
        assert nkd_tags[0].name == "[[4,2,2]]"

    def test_nkd_label_suggested_when_d_unknown(self, Hx_422, Hz_422):
        params = CodeParams(n=4, k=2, is_css=True, d=None)
        tags = suggest_code_tags(params, Hx_422, Hz_422)
        suggested = [t for t in tags if t.status == "suggested" and t.name.startswith("[[")]
        assert any("?" in t.name for t in suggested)

    def test_repetition_code_detected(self):
        # Repetition code: k=1, each row has weight 2
        Hx = np.array([[1, 1, 0], [0, 1, 1]])
        Hz = np.zeros((2, 3), dtype=int)
        params = CodeParams(n=3, k=1, is_css=True)
        tags = suggest_code_tags(params, Hx, Hz)
        names = [t.name for t in tags]
        assert "repetition-code" in names

    def test_surface_code_candidate_detected(self, params_713):
        # [[7,1,3]] doesn't match surface code heuristic (7 ≠ d²)
        Hx = np.zeros((3, 7), dtype=int)
        Hz = np.zeros((3, 7), dtype=int)
        tags = suggest_code_tags(params_713, Hx, Hz)
        names = [t.name for t in tags]
        assert "surface-code" not in names

    def test_9_qubit_surface_code_detected(self):
        # [[9,1,3]]: n=9=3², k=1 → surface code candidate
        params = CodeParams(n=9, k=1, is_css=True)
        Hx = np.zeros((4, 9), dtype=int)
        Hz = np.zeros((4, 9), dtype=int)
        tags = suggest_code_tags(params, Hx, Hz)
        names = [t.name for t in tags]
        assert "surface-code" in names


# ---------------------------------------------------------------------------
# suggest_classification_tags
# ---------------------------------------------------------------------------

class TestSuggestClassificationTags:
    def test_single_shot_flagged_without_repeat(self):
        circuit = "H 4\nCNOT 4 0\nM 4\n"
        tags = suggest_classification_tags("syndrome-extraction", circuit)
        names = [t.name for t in tags]
        assert "single-shot" in names

    def test_no_single_shot_with_repeat(self):
        circuit = "REPEAT 10 {\nH 4\nCNOT 4 0\nM 4\n}\n"
        tags = suggest_classification_tags("syndrome-extraction", circuit)
        names = [t.name for t in tags]
        assert "single-shot" not in names

    def test_fault_tolerant_flagged_with_flag_qubits(self):
        circuit = "# flag qubit\nH 5\nCNOT 5 0\nM 5\n"
        tags = suggest_classification_tags("syndrome-extraction", circuit)
        names = [t.name for t in tags]
        assert "fault-tolerant" in names

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

    def test_distance_tag_when_d_known(self, params_422, props_encoding):
        tags = suggest_circuit_tags(props_encoding, params_422)
        dist_tags = [t for t in tags if t.name.startswith("distance:")]
        assert len(dist_tags) == 1
        assert dist_tags[0].name == "distance:2"

    def test_no_distance_tag_when_d_unknown(self, props_encoding):
        params = CodeParams(n=4, k=2, is_css=True, d=None)
        tags = suggest_circuit_tags(props_encoding, params)
        dist_tags = [t for t in tags if t.name.startswith("distance:")]
        assert len(dist_tags) == 0
