"""Automatically resolve merge conflicts in open PRs."""

import json
import os
import subprocess
import sys
from pathlib import Path

DRY_RUN = os.getenv("DRY_RUN") == "1"


def run(cmd, **kwargs):
    """Execute ``cmd`` showing command text."""
    print("+", " ".join(cmd))
    if DRY_RUN:
        return subprocess.CompletedProcess(cmd, 0, "", "")
    return subprocess.run(cmd, check=True, text=True, **kwargs)


def run_capture(cmd):
    """Run ``cmd`` and capture stdout."""
    print("+", " ".join(cmd))
    if DRY_RUN:
        return ""
    return subprocess.check_output(cmd, text=True)


def get_conflict_prs():
    """Return PRs with merge conflicts on the default branch."""
    out = run_capture(
        [
            "gh",
            "pr",
            "list",
            "--state",
            "open",
            "--json",
            "number,headRefName,isCrossRepository,mergeable",
        ]
    )
    prs = json.loads(out)
    # Filter to same-repo PRs that need conflict resolution
    return [
        p for p in prs if p["mergeable"] == "CONFLICTING" and not p["isCrossRepository"]
    ]


def checkout_pr(number):
    """Fetch and check out the branch for PR ``number``."""
    run(["gh", "pr", "checkout", str(number)])


def conflict_files():
    """Return files with merge conflicts."""
    out = run_capture(["git", "diff", "--name-only", "--diff-filter=U"])
    return [f.strip() for f in out.splitlines() if f.strip()]


def resolve_file(path):
    """Resolve merge conflict for ``path`` using heuristics."""
    if path == "README.md":
        run(["git", "checkout", "--ours", path])
        run([sys.executable, "scripts/inject_readme.py", "README.md"])
    elif path.startswith("data/") and (path.endswith(".md") or path.endswith(".json")):
        # Prefer incoming changes for generated repo data
        run(["git", "checkout", "--theirs", path])
        run([sys.executable, "-m", "agentic_index_cli.ranker", "data/repos.json"])
        run([sys.executable, "scripts/inject_readme.py", "README.md"])
    else:
        run(["git", "checkout", "--theirs", path])
    run(["git", "add", path])


def continue_rebase():
    """Continue rebasing, resolving conflicts as they appear."""
    while True:
        try:
            run(["git", "rebase", "--continue"])
            break
        except subprocess.CalledProcessError:
            files = conflict_files()
            if not files:
                raise
            for f in files:
                resolve_file(f)


def rebase_main():
    """Attempt to rebase the PR branch onto main."""
    try:
        run(["git", "rebase", "origin/main"])
        return True
    except subprocess.CalledProcessError:
        files = conflict_files()
        if not files:
            run(["git", "rebase", "--abort"])
            return False
        for f in files:
            resolve_file(f)
        continue_rebase()
        return True


def quality_gate():
    """Run pre-commit hooks and tests after merging."""
    try:
        run(["pre-commit", "run", "--all-files"])
        run(["pytest", "-q"])
        run([sys.executable, "scripts/validate_top100.py"])
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    """Process all conflicting PRs in the repository."""
    prs = get_conflict_prs()
    fixed = []
    failed = []
    for pr in prs:
        num = pr["number"]
        head = pr["headRefName"]
        print(f"Processing PR #{num} ({head})")
        checkout_pr(num)
        if not rebase_main():
            failed.append(num)
            continue
        if not quality_gate():
            run(["git", "rebase", "--abort"], check=False)
            if not DRY_RUN:
                run(
                    [
                        "gh",
                        "pr",
                        "comment",
                        str(num),
                        "-b",
                        "⚠️ Auto-resolver failed tests after conflict merge. Needs manual review.",
                    ]
                )
            failed.append(num)
            continue
        if not DRY_RUN:
            run(["git", "push", "--force-with-lease"])
            run(
                [
                    "gh",
                    "pr",
                    "comment",
                    str(num),
                    "-b",
                    "✅ Auto-resolved merge conflicts and ensured CI green. Please review & merge.",
                ]
            )
        fixed.append(num)
    print("Fixed PRs:", fixed)
    print("Needs manual review:", failed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
