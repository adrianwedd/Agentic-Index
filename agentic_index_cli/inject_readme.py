"""Helpers for injecting the top-50 table into ``README.md``."""

from .internal.inject_readme import DEFAULT_TOP_N, main


def cli(argv=None):
    """Entry point for the README injector."""
    import argparse

    parser = argparse.ArgumentParser(description="Inject README table")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Write README even if no changes are detected",
    )
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N)
    args = parser.parse_args(argv)
    main(force=args.force, top_n=args.top_n)


if __name__ == "__main__":
    cli()
