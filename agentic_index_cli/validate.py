"""Validation helpers for repository JSON files."""

import json
import sys
from pathlib import Path
from typing import List

from pydantic import BaseModel, ValidationError, ConfigDict


class License(BaseModel):
    """Model for the ``license`` block."""

    spdx_id: str | None = None


class Owner(BaseModel):
    """Simplified repository owner model."""

    login: str | None = None


class Repo(BaseModel):
    """Repository schema used by :mod:`agentic_index_cli`."""

    name: str | None = None
    full_name: str | None = None
    html_url: str | None = None
    description: str | None = None
    stargazers_count: int | None = None
    forks_count: int | None = None
    open_issues_count: int | None = None
    closed_issues: int | None = None
    archived: bool | None = None
    license: License | str | None = None
    language: str | None = None
    pushed_at: str | None = None
    owner: Owner | None = None
    AgenticIndexScore: float | None = None
    category: str | None = None
    stars: int | None = None
    recency_factor: float | None = None
    issue_health: float | None = None
    doc_completeness: float | None = None
    license_freedom: float | None = None
    ecosystem_integration: float | None = None
    stars_delta: int | str | None = None
    forks_delta: int | str | None = None
    issues_closed_delta: int | str | None = None
    score_delta: float | str | None = None
    stars_log2: float | None = None
    last_commit: str | None = None
    one_liner: str | None = None
    stars_30d: int | None = None
    maintenance: float | None = None
    docs_score: float | None = None
    ecosystem: float | None = None
    last_release: str | None = None

    model_config = ConfigDict(extra="forbid")


class RepoFile(BaseModel):
    """Container for a list of :class:`Repo` objects."""

    schema_version: int = 2
    repos: List[Repo]

    model_config = ConfigDict(extra="forbid")


def _migrate_item(item: dict) -> dict:
    item = dict(item)
    if "AgentOpsScore" in item:
        item["AgenticIndexScore"] = item.pop("AgentOpsScore")
    if "score" in item and "AgenticIndexScore" not in item:
        item["AgenticIndexScore"] = item.pop("score")
    if isinstance(item.get("license"), dict):
        item["license"] = item["license"].get("spdx_id")
    return item


def load_repos(path: Path) -> List[dict]:
    """Validate and load repository JSON data."""
    raw = json.loads(path.read_text())
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, dict):
        version = raw.get("schema_version", 1)
        if version not in (1, 2):
            raise ValidationError(f"Unsupported schema_version {version}")
        items = raw.get("repos")
        if not isinstance(items, list):
            raise ValidationError('"repos" must be a list')
    else:
        raise ValidationError("Invalid JSON structure")
    seen: set[str] = set()
    repos: List[dict] = []
    duplicates: List[str] = []
    for item in items:
        item = _migrate_item(item)
        repo = Repo(**item)
        name = repo.full_name or repo.name or ""
        if name in seen:
            duplicates.append(name)
            continue
        seen.add(name)
        repos.append(repo.model_dump(exclude_none=True))
    if duplicates:
        dup = ", ".join(duplicates)
        raise ValidationError(f"duplicate entries: {dup}")
    return repos


def save_repos(path: Path, repos: List[dict]) -> None:
    """Write validated ``repos`` to ``path``."""
    payload = RepoFile(repos=[Repo(**_migrate_item(r)) for r in repos]).model_dump(exclude_none=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def validate_file(path: str) -> List[dict]:
    """Load and validate a repository JSON file."""
    return load_repos(Path(path))


def main(argv=None) -> int:
    """CLI entry for validating repo files."""
    argv = argv or sys.argv[1:]
    json_path = Path(argv[0] if argv else "data/repos.json")
    try:
        validate_file(str(json_path))
    except ValidationError as e:
        print(f"ValidationError: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
