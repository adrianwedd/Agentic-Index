import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from agentic_index_cli.internal import issue_logger as il


def test_format_agent_log():
    body = il.format_agent_log("CR", ["a", "b"])
    assert "<!-- agent-log -->" in body
    assert "CR" in body
    assert "1. a" in body
    assert "2. b" in body
