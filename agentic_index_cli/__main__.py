import argparse
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(prog="agentic-index", description="Agentic Index CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scrape_p = subparsers.add_parser("scrape", help="Scrape repositories")
    scrape_p.add_argument("--min-stars", type=int, default=0)
    scrape_p.add_argument("--iterations", type=int, default=1)
    scrape_p.add_argument("--output", type=Path, default=Path("data"))

    def run_scrape(args):
        from . import agentic_index
        agentic_index.run_index(args.min_stars, args.iterations, args.output)

    scrape_p.set_defaults(func=run_scrape)

    enrich_p = subparsers.add_parser("enrich", help="Compute enrichment factors")
    enrich_p.add_argument("path", nargs="?", default="data/repos.json")

    def run_enrich(args):
        from . import enricher
        enricher.main([args.path])

    enrich_p.set_defaults(func=run_enrich)

    faststart_p = subparsers.add_parser("faststart", help="Generate FAST_START table")
    faststart_p.add_argument("--top", type=int, required=True)
    faststart_p.add_argument("data_path")

    def run_faststart(args):
        from . import faststart
        faststart.run(args.top, Path(args.data_path))

    faststart_p.set_defaults(func=run_faststart)

    prune_p = subparsers.add_parser("prune", help="Remove inactive repos from repos.json")
    prune_p.add_argument("--inactive", type=int, required=True)
    prune_p.add_argument("--repos-path", type=Path, default=Path("repos.json"))
    prune_p.add_argument("--changelog-path", type=Path, default=Path("CHANGELOG.md"))

    def run_prune(args):
        from . import prune
        prune.prune(args.inactive, repos_path=args.repos_path, changelog_path=args.changelog_path)

    prune_p.set_defaults(func=run_prune)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
