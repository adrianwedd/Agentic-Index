"""CLI for injecting the ranked table into the README."""

from .internal.inject_readme import main


def cli(argv=None) -> None:
    """Run the injector."""
    import argparse

    parser = argparse.ArgumentParser(description="Synchronise README table")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    main(force=args.force)


if __name__ == "__main__":
    cli()
