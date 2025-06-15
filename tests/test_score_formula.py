import math
import agentic_index_cli.agentic_index as ai


def test_compute_score_formula():
    repo = {
        "stargazers_count": 100,
        "open_issues_count": 2,
        "closed_issues": 8,
        "pushed_at": "2025-06-01T00:00:00Z",
        "license": {"spdx_id": "MIT"},
        "topics": ["tool"],
    }
    readme = "word " * 300 + "```code```"
    score = ai.compute_score(repo, readme)

    recency = ai.compute_recency_factor(repo["pushed_at"])
    issue_health = ai.compute_issue_health(2, 8)
    doc_comp = ai.readme_doc_completeness(readme)
    license_free = ai.license_freedom("MIT")
    eco = ai.ecosystem_integration(["tool"], readme)
    expected = (
        0.30 * math.log2(100 + 1)
        + 0.25 * recency
        + 0.20 * issue_health
        + 0.15 * doc_comp
        + 0.07 * license_free
        + 0.03 * eco
    )
    expected = round(expected * 100 / 8, 2)
    assert math.isclose(score, expected)
