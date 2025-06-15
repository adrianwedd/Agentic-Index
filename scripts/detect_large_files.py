#!/usr/bin/env python
"""Invoke ``check_added_large_files`` via ``pre-commit``."""

from pre_commit_hooks.check_added_large_files import main

if __name__ == "__main__":
    raise SystemExit(main())
