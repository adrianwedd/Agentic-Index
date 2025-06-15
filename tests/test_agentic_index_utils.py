import agentic_index_cli.agentic_index as ai


def test_compute_score_simple():
    repo = {
        "stargazers_count": 100,
        "open_issues_count": 2,
        "closed_issues": 8,
        "pushed_at": "2025-06-01T00:00:00Z",
        "license": {"spdx_id": "MIT"},
        "topics": ["tool"],
    }
    readme = "Example readme with code\n```python\npass\n```"
    score = ai.compute_score(repo, readme)
    assert score > 0


def test_categorize():
    assert ai.categorize("This is a multi-agent framework", ["agent"]) == "Multi-Agent"
    assert ai.categorize("Retrieval Augmented", []) == "RAG-centric"


def test_readme_doc():
    good = "word " * 300 + "```code```"
    assert ai.readme_doc_completeness(good) == 1.0
    assert ai.readme_doc_completeness("short") == 0.0
