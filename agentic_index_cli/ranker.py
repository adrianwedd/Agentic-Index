"""Command line interface for ranking repositories."""

import argparse

from .config import load_config
from .internal.rank import main


def cli(argv=None) -> None:
    """Run the ranking command."""
    parser = argparse.ArgumentParser(description="Rank repositories")
    parser.add_argument("path", nargs="?", default="data/repos.json")
    parser.add_argument("--config", dest="config")
    args = parser.parse_args(argv)

    cfg = load_config(args.config) if args.config else None
    if cfg is None:
        main(args.path)
    else:
        main(args.path, config=cfg)

if __name__ == "__main__":
    import sys
    cli(sys.argv[1:])
