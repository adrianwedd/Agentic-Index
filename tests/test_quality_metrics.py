import sys
from pathlib import Path
import math
import pytest

# ensure project root on path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from lib.quality_metrics import maintenance_score, docs_score, ecosystem_tag


def test_maintenance_score_basic():
    score = maintenance_score(30, 0.2)
    recency = 1 - 30 / 365
    issues = 1 - 0.2
    expected = round((recency + issues) / 2, 2)
    assert math.isclose(score, expected)


def test_maintenance_score_clamps():
    assert maintenance_score(400, 1.5) == 0.0
    assert maintenance_score(-1, -0.5) == 1.0


def test_docs_score():
    assert docs_score(True, 1200) == 1.0
    assert docs_score(False, 100) == round(100/1000, 2)


@pytest.mark.parametrize(
    "topics, lang, deps, expected",
    [
        (["LangChain"], "Python", [], "langchain"),
        ([], "Python", [], "python"),
        ([], "Rust", ["langchain"], "langchain"),
        ([], "Go", [], "other"),
    ],
)
def test_ecosystem_tag(topics, lang, deps, expected):
    assert ecosystem_tag(topics, lang, deps) == expected
