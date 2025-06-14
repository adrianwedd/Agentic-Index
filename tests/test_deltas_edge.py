import pytest
from agentic_index_cli.internal.deltas import _fmt_delta


@pytest.mark.parametrize(
    "stars_old,stars_new,expect",
    [
        (None, 100, "+new"),
        (50, 100, "+50"),
        (80, 80, ""),
    ],
)
def test_format_stars_delta(stars_old, stars_new, expect):
    assert _fmt_delta(stars_old, stars_new) == expect
