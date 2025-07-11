"""Command line interface for ranking repositories."""

from __future__ import annotations

import click

from .config import load_config
from .helpers.click_options import config_option
from .internal.rank_main import main as rank_main

# re-export for backward compatibility
main = rank_main


@click.command(help="Rank repositories")
@click.argument("path", default="data/repos.json")
@config_option
def _cli(path: str, config: str | None) -> None:
    """Wrapper for the ranking CLI."""
    try:
        cfg = load_config(config)
    except ValueError as exc:
        click.echo(f"Config error: {exc}", err=True)
        raise SystemExit(1)

    main(path, config=cfg)


def cli(argv: list[str] | None = None) -> None:
    """Run the ranking command."""
    _cli.main(args=argv, standalone_mode=False)


if __name__ == "__main__":
    import sys

    cli(sys.argv[1:])
