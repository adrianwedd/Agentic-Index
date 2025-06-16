#!/usr/bin/env python3
"""Synchronize README table with ranking results."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from agentic_index_cli.internal.inject_readme import (
    DEFAULT_SORT_FIELD,
    DEFAULT_TOP_N,
    main,
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
    parser.add_argument("--force", action="store_true", help="Write even if unchanged")
    parser.add_argument(
        "--sort-by",
        default=DEFAULT_SORT_FIELD,
        choices=["overall", "stars_7d", "maintenance", "last_release"],
        help="Sort table by metric",
    )
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N)
    args = parser.parse_args()

    check = args.check or args.dry_run
    write = args.write or not check
    main(
        force=args.force,
        check=check,
        write=write,
        sort_by=args.sort_by,
        top_n=args.top_n,
    )
