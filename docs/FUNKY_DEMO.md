# FunkyAF Demo

Run `python scripts/funky_demo.py` to experience an end-to-end walkthrough of the tests and pipeline.

The script:

1. Checks formatting with `black` and `isort`.
2. Runs the full test suite.
3. Validates README fixtures and top100 consistency.
4. Spins up a temporary pipeline using sample data and generates a demo README.
5. Calls `scripts/e2e_test.sh` for a quick smoke test of the enrichment and ranking pipeline.

The output directory is printed at the end so you can inspect the generated artifacts.
