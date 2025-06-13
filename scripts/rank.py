import json
import math
import sys
from pathlib import Path

def compute_score(repo):
    stars = repo.get("stars", 0)
    recency = repo.get("recency_factor", 0)
    issue = repo.get("issue_health", 0)
    doc = repo.get("doc_completeness", 0)
    license_free = repo.get("license_freedom", 0)
    ecosys = repo.get("ecosystem_integration", 0)
    score = (
        0.35 * math.log2(stars + 1)
        + 0.20 * recency
        + 0.15 * issue
        + 0.15 * doc
        + 0.10 * license_free
        + 0.05 * ecosys
    )
    return round(score, 2)

def infer_category(repo):
    text = " ".join(repo.get("topics", [])) + " " + repo.get("description", "") + " " + repo.get("name", "")
    text = text.lower()
    if "rag" in text:
        return "RAG-centric"
    if "multi-agent" in text or "multi agent" in text or "crew" in text:
        return "Multi-Agent Coordination"
    if "devtool" in text or "runtime" in text or "tool" in text:
        return "DevTools"
    if "experiment" in text or "research" in text:
        return "Experimental"
    return "General-purpose"

def main(json_path: str):
    data_file = Path(json_path)
    repos = json.loads(data_file.read_text())
    for repo in repos:
        repo["score"] = compute_score(repo)
        repo["category"] = infer_category(repo)
    repos.sort(key=lambda r: r["score"], reverse=True)
    data_file.write_text(json.dumps(repos, indent=2))

    table_lines = [
        "| Rank | Repo | Score | Category |",
        "|------|------|-------|----------|",
    ]
    for i, repo in enumerate(repos[:50], start=1):
        table_lines.append(
            f"| {i} | {repo.get('name')} | {repo['score']} | {repo['category']} |"
        )
    Path("data").mkdir(exist_ok=True)
    Path("data/top50.md").write_text("\n".join(table_lines) + "\n")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/repos.json"
    main(path)
