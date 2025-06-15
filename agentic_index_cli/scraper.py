"""CLI entry point for scraping repositories."""

from .internal.scrape import main


def cli(argv=None) -> None:
    """Run the scraper."""
    main()


if __name__ == "__main__":
    cli()
