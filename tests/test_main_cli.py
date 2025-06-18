from pathlib import Path

import agentic_index_cli.__main__ as main
import agentic_index_cli.cli as ai


def test_main_scrape(monkeypatch, tmp_path):
    called = {}

    def fake_run_index(min_stars, iterations, output):
        called["args"] = (min_stars, iterations, output)

    monkeypatch.setattr(ai, "run_index", fake_run_index)
    main.main(
        ["scrape", "--min-stars", "1", "--iterations", "2", "--output", str(tmp_path)]
    )
    assert called["args"] == (1, 2, Path(tmp_path))
