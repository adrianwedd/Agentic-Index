#!/usr/bin/env python
"""Invoke ``check_added_large_files`` via ``pre-commit``."""

if __name__ == "__main__":
    from pre_commit_hooks.check_added_large_files import main

    raise SystemExit(main())
