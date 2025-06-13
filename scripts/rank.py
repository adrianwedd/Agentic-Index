import argparse
import json
from datetime import datetime
from pathlib import Path

CHANGELOG = Path("CHANGELOG.md")
TOP50 = Path("data/top50.md")


def parse_top(path: Path) -> list[str]:
    if not path.exists():
        return []
    names = []
    for line in path.read_text().splitlines():
        parts = [p.strip() for p in line.strip().split("|")]
        if len(parts) > 2 and parts[1].isdigit():
            names.append(parts[2])
    return names


def build_table(repos: list[dict]) -> str:
    lines = [
        "| # | Repo | ★ | Last Commit | Score | Category | One-liner |",
        "|---|------|----|------------|-------|----------|-----------|",
    ]
    for idx, repo in enumerate(repos, 1):
        line = (
            f"| {idx} | {repo['full_name']} | {repo.get('stars', 0)} | "
            f"{repo.get('last_commit', '')} | {repo.get('AgentOpsScore', 0)} | "
            f"{repo.get('category', '')} | {repo.get('one_liner', '')} |"
        )
        lines.append(line)
    return "\n".join(lines) + "\n"


def append_changelog(entries: list[str], changelog: Path = CHANGELOG) -> None:
    if not entries:
        return
    if changelog.exists():
        lines = changelog.read_text().rstrip().splitlines()
    else:
        lines = []
    lines.extend(entries)
    changelog.write_text("\n".join(lines) + "\n")


def rank(
    data_path: Path,
    top_path: Path = TOP50,
    changelog_path: Path = CHANGELOG,
) -> list[dict]:
    old = parse_top(top_path)
    with data_path.open() as f:
        repos = json.load(f)
    repos = sorted(repos, key=lambda r: r.get("AgentOpsScore", 0), reverse=True)[:50]
    top_path.parent.mkdir(parents=True, exist_ok=True)
    top_path.write_text(build_table(repos))

    new_names = [r["full_name"] for r in repos]
    date = datetime.utcnow().strftime("%Y-%m-%d")
    entries = []
    for name in new_names:
        if name not in old:
            entries.append(f"{date}  Added {name} – entered top list")
    for name in old:
        if name not in new_names:
            entries.append(f"{date}  Removed {name} – dropped from top list")
    append_changelog(entries, changelog_path)
    return repos


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank repositories")
    parser.add_argument("data_path", help="path to repos.json")
    args = parser.parse_args()
    rank(Path(args.data_path))


if __name__ == "__main__":
    main()
