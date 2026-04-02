"""
Tests for tag_suggest.py.
"""

from scripts.add_circuit.models import CodeParams
from scripts.add_circuit.tag_suggest import suggest_code_tags

# ---------------------------------------------------------------------------
# suggest_code_tags
# ---------------------------------------------------------------------------


class TestSuggestCodeTags:
    def test_css_tag_present_for_css_code(self):
        params = CodeParams(n=4, k=2, is_css=True, d=2)
        tags = suggest_code_tags(params)
        names = [t.name for t in tags]
        assert "CSS" in names

    def test_no_css_tag_for_general_code(self):
        params = CodeParams(n=5, k=1, is_css=False, d=3)
        tags = suggest_code_tags(params)
        names = [t.name for t in tags]
        assert "CSS" not in names

    def test_no_nkd_tag(self):
        params = CodeParams(n=4, k=2, is_css=True, d=2)
        tags = suggest_code_tags(params)
        nkd_tags = [t for t in tags if t.name.startswith("[[")]
        assert len(nkd_tags) == 0
