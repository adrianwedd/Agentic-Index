"""Wrapper to generate markdown artifacts for the repository."""

from scripts.inject_readme import main as inject


def main(argv=None):
    """Run the README injection helper."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate markdown outputs")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    inject(force=args.force)


if __name__ == "__main__":
    main()
