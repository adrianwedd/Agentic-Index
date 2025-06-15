#!/usr/bin/env python3
"""Wrapper for internal regression guard."""
import sys

from agentic_index_cli.internal.regression_check import main

if __name__ == "__main__":
    sys.exit(main())
