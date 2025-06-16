"""Helpers for posting Codex agent logs."""

from __future__ import annotations

from typing import List, Optional

from .. import issue_logger


def format_agent_log(cr_text: str, steps: List[str] | None = None) -> str:
    lines = ["<!-- agent-log -->"]
    if cr_text:
        lines.append(cr_text.strip())
    if steps:
        lines.append("")
        lines.append("### Steps")
        for i, step in enumerate(steps, 1):
            lines.append(f"{i}. {step}")
    return "\n".join(lines)


def post_agent_log(
    issue_url: str,
    cr_text: str,
    steps: List[str] | None = None,
    *,
    token: str | None = None,
) -> str:
    """Post a formatted agent log comment."""
    body = format_agent_log(cr_text, steps)
    return issue_logger.post_comment(issue_url, body, token=token)
