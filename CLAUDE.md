# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agentic-Index is a data-driven repository index that continuously scores and curates open-source frameworks for building autonomous AI agents. The project consists of two main packages:

- `agentic_index_cli` - Command line utilities for scraping, scoring, and ranking repositories
- `agentic_index_api` - REST API exposing ranking and metadata

## Common Development Commands

### Build and Test
```bash
# Run the full test suite
pytest -q

# Run tests with network restrictions (mimics CI)
CI_OFFLINE=1 pytest --disable-socket

# Run with coverage reporting
pytest --cov=agentic_index_cli --cov-report=term-missing

# Type checking with mypy
mypy agentic_index_cli/cli.py agentic_index_cli/enricher.py agentic_index_cli/inject_readme.py agentic_index_cli/network.py
```

### Development Setup
```bash
# Quick environment setup (installs dependencies, pre-commit hooks)
source scripts/setup-env.sh

# Install pre-commit hooks manually
pre-commit install

# Run pre-commit on specific files
pre-commit run --files <path>
```

### Data Pipeline Operations
```bash
# Complete data refresh pipeline
make top100

# Individual pipeline steps
python scripts/scrape_repos.py --min-stars 50 --output data/repos.json
python scripts/score_metrics.py data/repos.json
python -m agentic_index_cli.ranker data/repos.json
python scripts/inject_readme.py --force

# Force README injection (bypasses change detection)
python scripts/inject_readme.py --force

# Preview changes without writing
python scripts/inject_readme.py --dry-run
```

### CLI Usage
```bash
# Install the CLI package
pip install -e .

# Basic scraping and ranking
agentic-index scrape --min-stars 100
agentic-index enrich data/repos.json
agentic-index faststart --top 100 data/repos.json

# Use custom config
agentic-index scrape --config my_config.yml
```

### Testing and Quality
```bash
# Run accessibility checks (requires Chrome)
npx pa11y web/index.html

# Validate fixtures and schema
python scripts/validate_fixtures.py
python scripts/validate_tasks.py
```

## Architecture and Code Organization

### Core Modules
- `agentic_index_cli/cli.py` - Main CLI interface and command definitions
- `agentic_index_cli/scraper.py` - GitHub repository discovery and data collection
- `agentic_index_cli/scoring.py` - Repository scoring algorithms
- `agentic_index_cli/ranker.py` - Ranking and sorting logic
- `agentic_index_cli/inject_readme.py` - README.md table injection system
- `agentic_index_cli/enricher.py` - Repository metadata enrichment

### Data Flow
1. **Scraping**: Discover repositories via GitHub API searches and topic filters
2. **Scoring**: Apply transparent scoring formula based on stars, maintenance, docs, etc.
3. **Ranking**: Sort repositories by computed scores
4. **Injection**: Update README.md with ranked table using marker comments

### Configuration
- `agentic_index_cli/config.yaml` - Default ranking parameters and output settings
- `pyproject.toml` - Package metadata, dependencies, and tool configuration
- `pytest.ini` - Test configuration with CI_OFFLINE environment
- `mypy.ini` - Type checker configuration for specific modules

### Key Data Files
- `data/repos.json` - Main repository database with metrics and scores
- `data/top100.md` - Generated markdown table for top repositories
- `data/by_category/index.json` - Category-based repository groupings

## Development Practices

### Testing
- Tests run offline by default (`CI_OFFLINE=1`)
- Use `pytest-socket` to prevent network calls during testing
- Coverage threshold set at 70% (configurable in pyproject.toml)
- Property-based testing with Hypothesis for fuzzing

### Code Quality
- Black for code formatting
- isort for import sorting  
- MyPy for type checking on selected modules
- Pre-commit hooks enforce formatting and run tests

### README Injection System
The project uses an automated system to inject ranked repository tables into README.md:
- Markers: `<!-- TOP50:START -->` and `<!-- TOP50:END -->`
- Injection must be idempotent (running twice produces same result)
- Use `--force` to bypass change detection
- Use `--dry-run` to preview changes

### Environment Variables
- `GITHUB_TOKEN_REPO_STATS` - Increases GitHub API rate limits
- `CI_OFFLINE` - Disables network calls for testing
- `API_KEY` - For third-party service integrations

## Scoring Algorithm
The repository scoring system considers:
- ⭐ Stars and momentum (7-day deltas)
- 🔧 Maintenance health (issue/PR management)
- 📅 Release recency
- 📚 Documentation quality (README analysis)
- 🧠 Ecosystem fit (keyword matching)
- ⚖️ License permissiveness

See `docs/methodology.md` for the complete scoring formula and weights.