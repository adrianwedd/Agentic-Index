import sys
from pathlib import Path

# ensure project root is on the path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from .helpers import _parse_table, assert_readme_equivalent


def test_parse_table_strips_abbr():
    table = (
        '| Rank | <abbr title="Overall">📊</abbr> Overall | Repo |\n'
        "|-----:|------:|------|\n"
        "| 1 | 1.0 | foo |\n"
    )
    headers, rows = _parse_table(table)
    assert headers == ["Rank", "📊 Overall", "Repo"]
    assert rows == [["1", "1.0", "foo"]]


def test_assert_equivalent_ignores_abbr():
    expected = (
        '| Rank | <abbr title="Overall">📊</abbr> Overall | Repo |\n'
        "|-----:|------:|------|\n"
        "| 1 | 1.0 | foo |\n"
    )
    actual = (
        "| Rank | <abbr title='Overall'>📊</abbr> Overall | Repo |\n"
        "|-----:|------:|------|\n"
        "| 1 | 1.0 | foo |\n"
    )
    assert_readme_equivalent(expected, actual)


def test_parse_table_strips_generic_html():
    table = (
        "| <b>Rank</b> | <span>Score</span> | Repo |\n"
        "|-----:|------:|------|\n"
        "| 1 | 1.0 | foo |\n"
    )
    headers, rows = _parse_table(table)
    assert headers == ["Rank", "Score", "Repo"]
    assert rows == [["1", "1.0", "foo"]]
