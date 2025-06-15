from typer.testing import CliRunner

from agentic_index_cli.__main__ import app


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "scrape" in result.stdout
    assert "faststart" in result.stdout
