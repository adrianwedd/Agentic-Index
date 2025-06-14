from datetime import datetime, timedelta

from hypothesis import given, strategies as st, settings

from agentic_index_cli.rank import compute_score


# Helper to build minimal repo dict for compute_score

def _repo(stars: int, open_issues: int, closed_issues: int, days_old: int):
    pushed_at = (
        datetime.utcnow() - timedelta(days=days_old)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "stargazers_count": stars,
        "open_issues_count": open_issues,
        "closed_issues": closed_issues,
        "pushed_at": pushed_at,
        "license": {"spdx_id": "MIT"},
        "topics": [],
    }

@settings(max_examples=20)

@given(
    stars1=st.integers(min_value=0, max_value=1_000_000),
    stars2=st.integers(min_value=0, max_value=1_000_000),
    open_issues=st.integers(min_value=0, max_value=1000),
    closed_issues=st.integers(min_value=0, max_value=1000),
    days=st.integers(min_value=0, max_value=365),
)
def test_score_monotonic_and_range(stars1, stars2, open_issues, closed_issues, days):
    if stars1 > stars2:
        stars1, stars2 = stars2, stars1  # ensure stars2 >= stars1

    repo_low = _repo(stars1, open_issues, closed_issues, days)
    repo_high = _repo(stars2, open_issues, closed_issues, days)
    readme = "word " * 300 + "```code```"

    score_low = compute_score(repo_low, readme)
    score_high = compute_score(repo_high, readme)

    assert 0 <= score_low <= 100
    assert 0 <= score_high <= 100
    assert score_high >= score_low
