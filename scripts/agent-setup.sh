#!/usr/bin/env bash
set -euo pipefail

# Silence pip's warning about running as root
export PIP_ROOT_USER_ACTION=ignore

# Install project dependencies
pip install -r requirements.txt
pip install -e .
# Install tooling used in CI
pip install black isort flake8 mypy bandit
# Install pre-commit hooks for linting
pip install pre-commit
pre-commit install --install-hooks
