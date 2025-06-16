import click


def config_option(func):
    """Shared ``--config`` option."""
    return click.option(
        "--config",
        "-c",
        type=click.Path(dir_okay=False, readable=True),
        help="Path to YAML configuration file",
    )(func)


def output_option(func):
    """Shared ``--output`` option."""
    return click.option(
        "--output",
        "-o",
        type=click.Path(dir_okay=False, writable=True),
        default="data/repos.json",
        show_default=True,
        help="Output file path",
    )(func)
