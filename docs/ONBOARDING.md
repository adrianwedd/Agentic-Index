# Developer Onboarding Guide

Welcome! This document collects everything you need to set up a working development environment for Agentic Index.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Fork & Clone](#fork--clone)
- [Install Dependencies](#install-dependencies)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Running Tests](#running-tests)
- [Troubleshooting](#troubleshooting)

## Prerequisites
- Linux or macOS. Windows users can use WSL.
- Python 3.11+
- [Git LFS](https://git-lfs.github.com/) for large assets.

## Fork & Clone
1. Fork the repository on GitHub.
2. Clone your fork:
   ```bash
   git clone https://github.com/<you>/Agentic-Index.git
   cd Agentic-Index
   ```

## Install Dependencies
Use the helper script to install all runtime and development dependencies and set up editable installs:
```bash
bash scripts/agent-setup.sh
```
This installs `pre-commit` and performs a `pip install -e .` under the hood.

## Pre-commit Hooks
Activate hooks so formatting and lint checks run before each commit:
```bash
pre-commit install
```
Run them manually on changed files with:
```bash
pre-commit run --files <path>
```

## Running Tests
Run the full test suite with:
```bash
PYTHONPATH="$PWD" pytest -q
```
To mimic CI's network restrictions use:
```bash
CI_OFFLINE=1 pytest --disable-socket
```

## Troubleshooting
- **Network errors when installing packages** – use the mirror described in [docs/CI_SETUP.md](CI_SETUP.md).
- **GitHub API rate limits** – export `GITHUB_TOKEN_REPO_STATS` with a personal token or lower `--min-stars` when scraping.
- **Windows path issues** – run tools inside WSL or use forward slashes.

