#!/usr/bin/env python3
from agentic_index_cli.internal.inject_readme import main

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Inject top50 table into README")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    main(force=args.force)
