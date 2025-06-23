#!/usr/bin/env python3
"""Synchronize README table with ranking results."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from agentic_index_cli.internal.inject_readme import (
    DEFAULT_SORT_FIELD,
    DEFAULT_TOP_N,
    main,
    write_all_categories,
    write_category_readme,
)

if __name__ == "__main__":
    import argparse

    class _Parser(argparse.ArgumentParser):
        def error(self, message):
            self.print_help()
            self.exit(1)

    parser = _Parser(description="Synchronise README top100 table")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--check", action="store_true", help="Fail if README is outdated"
    )
    group.add_argument(
        "--write", action="store_true", help="Update README in place (default)"
    )
    group.add_argument("--dry-run", action="store_true", help="Alias for --check")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Write README even if no changes are detected",
    )
    parser.add_argument(
        "--sort-by",
        default=DEFAULT_SORT_FIELD,
        choices=[
            "score",
            "stars",
            "stars_delta",
            "score_delta",
            "recency",
            "issue_health",
        ],
        help="Sort table by metric",
    )
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N)
    parser.add_argument("--limit", type=int, help="Maximum rows to render")
    parser.add_argument("--repos-path", type=Path, help="Path to repos.json")
    parser.add_argument("--ranked-path", type=Path, help="Path to ranked.json")
    cat_group = parser.add_mutually_exclusive_group()
    cat_group.add_argument("--category", help="Generate README for one category")
    cat_group.add_argument(
        "--all-categories",
        action="store_true",
        help="Generate README_<cat>.md for all categories",
    )
    args = parser.parse_args()

    check = args.check or args.dry_run
    write = args.write or not check
    kwargs = {
        "force": args.force,
        "check": check,
        "write": write,
        "sort_by": args.sort_by,
        "top_n": args.top_n,
        "limit": args.limit,
        "repos_path": args.repos_path,
        "ranked_path": args.ranked_path,
    }
    if args.category or args.all_categories:
        if args.all_categories:
            write_all_categories(**kwargs)
        else:
            write_category_readme(args.category, **kwargs)
    else:
        main(**kwargs)
