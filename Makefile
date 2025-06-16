refresh:
	./scripts/trigger_refresh.sh


top100:
	python scripts/scrape_repos.py --min-stars 50 --output data/repos.json
	python scripts/score_metrics.py data/repos.json
	python -m agentic_index_cli.ranker data/repos.json
	python scripts/inject_readme.py --force
