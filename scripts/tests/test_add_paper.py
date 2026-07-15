"""Tests for the paper fetcher's pure parts.

Nothing here touches the network: the fetch itself is a thin wrapper over arXiv
and Crossref, but what breaks in practice is the parsing around it -- which
reference shapes are recognised, and how names survive becoming a filename.
"""

import pytest

from scripts.add_paper import ascii_fold, extract_ref, slugify, surname


class TestExtractRef:
    @pytest.mark.parametrize(
        "text,expected",
        [
            # The shapes that actually appear in circuit `source` fields.
            ("https://arxiv.org/abs/2402.17761", ("arxiv", "2402.17761")),
            ("http://arxiv.org/abs/2402.17761", ("arxiv", "2402.17761")),
            ("https://arxiv.org/abs/2402.17761/", ("arxiv", "2402.17761")),
            ("https://doi.org/10.1098/rspa.1996.0136", ("doi", "10.1098/rspa.1996.0136")),
            # Bare identifiers, as a maintainer would type them.
            ("2402.17761", ("arxiv", "2402.17761")),
            ("10.1098/rspa.1996.0136", ("doi", "10.1098/rspa.1996.0136")),
            ("doi:10.1098/rspa.1996.0136", ("doi", "10.1098/rspa.1996.0136")),
            # Old-style arXiv ids predate the numeric scheme; the 1996 Steane
            # paper is one, so this is not hypothetical.
            ("quant-ph/9601029", ("arxiv", "quant-ph/9601029")),
            ("https://arxiv.org/abs/quant-ph/9601029", ("arxiv", "quant-ph/9601029")),
            # A version suffix names the same work: v1 and v2 must not become two
            # papers, and the stored id is the bare one.
            ("2402.17761v2", ("arxiv", "2402.17761")),
            ("https://arxiv.org/abs/2402.17761v3", ("arxiv", "2402.17761")),
            # A /pdf/ link is the same paper as its /abs/ page.
            ("https://arxiv.org/pdf/2402.17761", ("arxiv", "2402.17761")),
            ("https://arxiv.org/pdf/2402.17761v2", ("arxiv", "2402.17761")),
            ("https://arxiv.org/pdf/2402.17761.pdf", ("arxiv", "2402.17761")),
        ],
    )
    def test_recognised(self, text, expected):
        assert extract_ref(text) == expected

    @pytest.mark.parametrize(
        "text",
        [
            # A tool name, not a work: 109 circuits carry this and must not be
            # mistaken for something fetchable.
            "circuit-synth",
            "",
            "   ",
            "Smith et al., some journal, 1998",  # free-form citation
            "https://github.com/some/repo",  # a repo is not a paper
            "https://example.com/paper.html",
        ],
    )
    def test_unrecognised(self, text):
        assert extract_ref(text) is None


class TestAsciiFold:
    @pytest.mark.parametrize(
        "text,expected",
        [
            # Dropping the accent instead of folding it would give "Brugire" and
            # "Mller" -- both real authors in this catalogue.
            ("Brugière", "Brugiere"),
            ("Müller", "Muller"),
            ("Zdeněk Kolář", "Zdenek Kolar"),
            # NFKD does not decompose ß, so it is mapped by hand; without that
            # "Heußen" folds to "Heuen".
            ("Heußen", "Heussen"),
            ("Sascha Heußen", "Sascha Heussen"),
            ("Andrew Steane", "Andrew Steane"),
            ("", ""),
        ],
    )
    def test_fold(self, text, expected):
        assert ascii_fold(text) == expected

    def test_ascii_is_unchanged(self):
        text = "Automated Synthesis of Fault-Tolerant State Preparation Circuits"
        assert ascii_fold(text) == text


class TestSurname:
    @pytest.mark.parametrize(
        "full,expected",
        [
            ("Remmy Zen", "Zen"),
            ("Andrew Steane", "Steane"),
            ("Markus Müller", "Müller"),
            ("Timothée Goubault de Brugière", "Brugière"),
            ("Cher", "Cher"),
        ],
    )
    def test_surname(self, full, expected):
        assert surname(full) == expected


class TestSlugify:
    def test_matches_the_hand_written_convention(self):
        slug = slugify(
            {
                "authors": ["Tom Peham", "Ludwig Schmid"],
                "title": "Automated Synthesis of Fault-Tolerant State Preparation Circuits",
                "year": 2024,
            }
        )
        # <surname>-<year>-<title words, stopwords dropped>
        assert slug == "peham-2024-automated-synthesis-fault-tolerant"

    def test_folds_accents_rather_than_dropping_them(self):
        slug = slugify(
            {
                "authors": ["Timothée Goubault de Brugière"],
                "title": "A graph-state based synthesis framework",
                "year": 2022,
            }
        )
        assert slug.startswith("brugiere-2022-")

    def test_survives_a_missing_year(self):
        slug = slugify({"authors": ["Andrew Steane"], "title": "Multiple Particle Interference"})
        assert slug == "steane-multiple-particle-interference"

    def test_is_filename_safe(self):
        slug = slugify(
            {
                "authors": ["Chen Kang"],
                "title": "QUITS: A modular Qldpc code circUIT Simulator",
                "year": 2025,
            }
        )
        # No colon, no space, no capital -- this becomes a path.
        assert slug == "kang-2025-quits-modular-qldpc-code"
