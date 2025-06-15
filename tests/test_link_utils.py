import pytest
from agentic_index_cli.internal.link_integrity import slug


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Hello World", "hello-world"),
        ("Üñîçødé", "d"),
        ("Spaces  and---Symbols!", "spaces-and---symbols"),
    ],
)
def test_slug(text, expected):
    assert slug(text) == expected
