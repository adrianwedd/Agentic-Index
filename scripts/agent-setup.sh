#!/usr/bin/env bash
set -euo pipefail

# Install project dependencies
pip install -r requirements.txt
pip install -e .
# Install pre-commit hooks for linting
pip install pre-commit
pre-commit install --install-hooks
