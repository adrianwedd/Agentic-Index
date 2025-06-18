# CLI Usage

Agentic Index ships a unified `agentic-index` command. Run `agentic-index --help` for an overview of available options.

## Commands

### scrape
Fetch repository metadata from GitHub and write `repos.json` to the output directory.

```bash
agentic-index scrape --min-stars 100 --iterations 2 --output data
```

### enrich
Compute enrichment factors for a scraped `repos.json` file.

```bash
agentic-index enrich data/repos.json
```

### faststart
Create the `FAST_START.md` table for the highest scoring repositories.

```bash
agentic-index faststart --top 10 data/repos.json
```

### prune
Remove repositories that have been inactive for a given number of days.

```bash
agentic-index prune --inactive 365 --repos-path data/repos.json --changelog-path CHANGELOG.md
```

Metric field definitions are documented in [METRICS_SCHEMA.md](METRICS_SCHEMA.md).
