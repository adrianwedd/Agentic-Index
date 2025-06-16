"""CLI entry point for scraping repositories."""

from __future__ import annotations

import click

from .helpers.click_options import output_option
from .internal.scrape import main as scrape_main

# expose for tests
main = scrape_main


@click.command(help="Scrape repositories")
@output_option
def _cli(output: str) -> None:
    main()  # pragma: no cover - actual parsing happens in submodule


def cli(argv: list[str] | None = None) -> None:
    _cli.main(args=argv, standalone_mode=False)


if __name__ == "__main__":
    cli()
