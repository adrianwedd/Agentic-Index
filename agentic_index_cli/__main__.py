"""Entrypoint for the ``agentic-index`` command line tool."""

import logging
import time
import uuid
from pathlib import Path
from typing import List, Optional

import requests
import structlog
import typer

from . import cli as agentic_index
from . import enricher, faststart, prune
from .logging_config import configure_logging, configure_sentry

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
    configure_logging(level)
    configure_sentry()


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
    log = structlog.get_logger(__name__).bind(run_id=str(uuid.uuid4()))
    start = time.perf_counter()
    log.info("cli-start", args=args)
    try:
        app(prog_name="agentic-index", args=args, standalone_mode=False)
    except SystemExit as exc:
        if exc.code == 2:
            raise SystemExit(1)
        raise
    except requests.RequestException as exc:
        typer.secho(f"Network error: {exc}", fg="red", err=True)
        log.error("network-error", error=str(exc))
        raise SystemExit(2)
    except Exception as exc:  # pragma: no cover - unknown error path
        typer.secho(f"Unknown error: {exc}", fg="red", err=True)
        log.error("unknown-error", error=str(exc))
        raise SystemExit(3)
    finally:
        log.info("cli-finish", duration=time.perf_counter() - start)

    return


def main(args: Optional[List[str]] = None) -> None:
    run(args)


if __name__ == "__main__":  # pragma: no cover
    main()
