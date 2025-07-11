from agentic_index_cli import scoring as ai


def test_categorize_branches():
    assert ai.categorize("dev toolkit", []) == "DevTools"
    assert ai.categorize("Video processing", []) == "Domain-Specific"
    assert ai.categorize("Experimental research", []) == "Experimental"
    assert ai.categorize("Just another repo", []) == "General-purpose"
