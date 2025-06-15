import logging

"""Entrypoint for the ``agentic-index`` command line tool."""

import argparse
from pathlib import Path
from typing import List, Optional

import requests
import typer

from . import agentic_index, enricher, faststart, prune

def main(argv=None):
    """Dispatch subcommands for the CLI."""
    parser = argparse.ArgumentParser(prog="agentic-index", description="Agentic Index CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

app = typer.Typer(add_completion=True, help="Agentic Index CLI")


@app.callback()
def _main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show info logs"),
    debug: bool = typer.Option(False, "--debug", help="Show debug logs"),
):
    level = logging.WARNING
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


@app.command()
def scrape(
    min_stars: int = typer.Option(0, "--min-stars"),
    iterations: int = typer.Option(1, "--iterations"),
    output: Path = typer.Option(Path("data"), "--output"),
):
    """Scrape repositories."""
    agentic_index.run_index(min_stars, iterations, output)


@app.command()
def enrich(path: str = typer.Argument("data/repos.json")):
    """Compute enrichment factors."""
    enricher.main([path])


@app.command()
def faststart_cmd(
    top: int = typer.Option(..., "--top"),
    data_path: str = typer.Argument(...),
):
    """Generate FAST_START table."""
    faststart.run(top, Path(data_path))


@app.command()
def prune_cmd(
    inactive: int = typer.Option(..., "--inactive"),
    repos_path: Path = typer.Option(Path("repos.json"), "--repos-path"),
    changelog_path: Path = typer.Option(Path("CHANGELOG.md"), "--changelog-path"),
):
    """Remove inactive repos."""
    prune.prune(inactive, repos_path=repos_path, changelog_path=changelog_path)


def run(args: Optional[List[str]] = None) -> None:
    try:
        app(prog_name="agentic-index", args=args, standalone_mode=False)
    except SystemExit as exc:
        if exc.code == 2:
            raise SystemExit(1)
        raise
    except requests.RequestException as exc:
        typer.secho(f"Network error: {exc}", fg="red", err=True)
        raise SystemExit(2)
    except Exception as exc:  # pragma: no cover - unknown error path
        typer.secho(f"Unknown error: {exc}", fg="red", err=True)
        raise SystemExit(3)

    issue_p = subparsers.add_parser("issue-logger", help="Post GitHub issues or comments")
    mode = issue_p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--new-issue", action="store_true")
    mode.add_argument("--comment", action="store_true")
    issue_p.add_argument("--repo", required=True)
    issue_p.add_argument("--title")
    issue_p.add_argument("--body")
    issue_p.add_argument("--issue-number", type=int)
    issue_p.add_argument("--dry-run", action="store_true")
    issue_p.add_argument("--verbose", action="store_true")

    def run_issue(args):
        from . import issue_logger
        issue_logger.main([
            *( ["--new-issue"] if args.new_issue else ["--comment"] ),
            "--repo", args.repo,
            *( ["--title", args.title] if args.title else [] ),
            *( ["--body", args.body] if args.body else [] ),
            *( ["--issue-number", str(args.issue_number)] if args.issue_number is not None else [] ),
            *( ["--dry-run"] if args.dry_run else [] ),
            *( ["--verbose"] if args.verbose else [] ),
        ])

    issue_p.set_defaults(func=run_issue)

    args = parser.parse_args(argv)
    args.func(args)


def main(args: Optional[List[str]] = None) -> None:
    run(args)


if __name__ == "__main__":  # pragma: no cover
    main()
