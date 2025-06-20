# FunkyAF Demo

Run `python scripts/funky_demo.py` for an interactive tour of the repository.

Highlights:

1. Progress bars visualize formatting checks and test execution.
2. Docstrings from key pipeline functions scroll by to explain what each step does.
3. Fixture validation runs with clear success/failure output.
4. A miniature pipeline processes fixture repos and renders a metrics table showing repository count and average star count.
5. The README sync check may fail when demo data is stale, but the script continues so you can still explore the pipeline.
6. Finally, it invokes `scripts/e2e_test.sh` for a quick smoke test and prints the location of generated artifacts.
