import pytest
from agentic_index_cli.internal.inject_readme import _fmt_delta


@pytest.mark.parametrize(
    "val,expected",
    [
        (0, ""),
        (5, "+5"),
        (-3, "-3"),
        (1.25, "+1.2"),
        ("foo", "foo"),
    ],
)
def test_fmt_delta(val, expected):
    assert _fmt_delta(val) == expected
