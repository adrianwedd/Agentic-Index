import argparse
from pathlib import Path


HEADER = (
    "| Rank | Repo (Click to Visit) | ★ Stars | Last Commit | Score | Category | One-Liner |\n"
    "|------|-----------------------|---------|-------------|-------|----------|-----------|\n"
)


def format_stars(stars: int) -> str:
    if stars >= 1000:
        return f"{stars/1000:.1f}k"
    return str(stars)


def generate_table(repos):
    lines = [HEADER]
    for idx, repo in enumerate(repos, 1):
        repo_link = f"[{repo['full_name']}](https://github.com/{repo['full_name']})"
        line = (
            f"| {idx} | {repo_link} | {format_stars(repo['stars'])} | "
            f"{repo['last_commit']} | {repo.get('AgenticIndexScore', repo.get('AgentOpsScore', 0))} | "
            f"{repo.get('category', '')} | {repo.get('one_liner', '')} |"
        )
        lines.append(line)
    return "\n".join(lines) + "\n"


from .validate import load_repos


def run(top: int, data_path: Path, output_path: Path | None = None) -> None:
    repos = load_repos(data_path)

    filtered = [
        r for r in repos
        if r.get("stars", 0) >= 5000 and r.get("doc_completeness") == 1
    ]

    ranked = sorted(filtered, key=lambda r: r.get("AgenticIndexScore", r.get("AgentOpsScore", 0)), reverse=True)
    ranked = ranked[:top]

    table = generate_table(ranked)

    if output_path is None:
        output_path = Path("FAST_START.md")
    with output_path.open("w") as f:
        f.write(table)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate Fast Start table")
    parser.add_argument("--top", type=int, required=True, help="number of repos")
    parser.add_argument("data_path", help="path to repos.json")
    args = parser.parse_args(argv)


    run(args.top, Path(args.data_path))

if __name__ == "__main__":
    main()
