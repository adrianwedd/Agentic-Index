"""CLI utilities for AgentIndex.

This module simply re-exports the command-line interface implemented in
`agentindex_cli/indexer.py` so that it can be used as a package and documented via
mkdocstrings.
"""

from agentindex_cli.indexer import *  # noqa: F401,F403
