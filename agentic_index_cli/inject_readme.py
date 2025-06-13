from scripts.inject_readme import main


def cli(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description="Inject README table")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    main(force=args.force)

if __name__ == "__main__":
    cli()
