#!/usr/bin/env python3
from agentic_index_cli.internal.inject_readme import main

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Synchronise README top50 table")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="Fail if README is outdated")
    group.add_argument("--write", action="store_true", help="Update README in place (default)")
    group.add_argument("--dry-run", action="store_true", help="Alias for --check")
    parser.add_argument("--force", action="store_true", help="Write even if unchanged")
    args = parser.parse_args()

    check = args.check or args.dry_run
    write = args.write or not check
    main(force=args.force, check=check, write=write)
