"""Command line interface for ranking repositories."""

from .internal.rank import main


def cli(argv=None) -> None:
    """Run the ranking command."""
    path = argv[0] if argv else "data/repos.json"
    main(path)

if __name__ == "__main__":
    import sys
    cli(sys.argv[1:])
