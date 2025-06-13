"""CLI utilities for AgentOps.

This module simply re-exports the command-line interface implemented in
`scripts/agentops.py` so that it can be used as a package and documented via
mkdocstrings.
"""

from scripts.agentops import *  # noqa: F401,F403
