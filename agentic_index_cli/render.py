"""Output helpers for ranking results."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List

from jinja2 import Template

from agentic_index_cli.constants import SCORE_KEY


def save_csv(repos: List[Dict], path: Path) -> None:
    """Write ``repos`` to ``path`` as CSV."""
    keys = ["name", "stars", "last_commit", SCORE_KEY, "category", "description"]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in repos:
            writer.writerow({k: r[k] for k in keys})


def save_markdown(repos: List[Dict], path: Path) -> None:
    """Write a Markdown table of ``repos`` to ``path``."""
    tmpl = Template(
        """
| # | Repo | ★ | Last Commit | Score | Category | One-liner |
|---|------|----|------------|-------|----------|-----------|
{% for i, r in rows %}| {{ i }} | {{ r.name }} | {{ r.stars }} | {{ r.date }} | {{ r.score }} | {{ r.category }} | {{ r.description }} |
{% endfor %}"""
    )
    rows = [
        (
            i,
            {
                "name": r["name"],
                "stars": r["stars"],
                "date": r["last_commit"].split("T")[0],
                "score": r[SCORE_KEY],
                "category": r["category"],
                "description": r["description"],
            },
        )
        for i, r in enumerate(repos, 1)
    ]
    path.write_text(tmpl.render(rows=rows))


def load_previous(path: Path) -> List[str]:
    """Load previously ranked repository names from ``path``."""
    if not path.exists():
        return []
    with path.open() as f:
        reader = csv.DictReader(f)
        return [row["name"] for row in reader]


def changelog(old: List[str], new: List[str]) -> List[Dict]:
    """Return changelog entries comparing old and new repo lists."""
    old_set = set(old)
    new_set = set(new)
    changes = []
    for name in new_set - old_set:
        changes.append({"repo": name, "action": "Added"})
    for name in old_set - new_set:
        changes.append({"repo": name, "action": "Removed"})
    return changes


def save_changelog(changes: List[Dict], path: Path) -> None:
    """Write changelog entries to ``path``."""
    if not changes:
        return
    with path.open("w") as f:
        f.write("| Repo | Action |\n|------|--------|\n")
        for c in changes:
            f.write(f"| {c['repo']} | {c['action']} |\n")
