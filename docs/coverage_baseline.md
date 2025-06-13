................                                                         [100%]
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.11.12-final-0 _______________

Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
agentic_index_cli/__init__.py            0      0   100%
agentic_index_cli/__main__.py           32      8    75%   15-16, 25-26, 36-37, 42, 46
agentic_index_cli/agentic_index.py     211    211     0%   1-318
agentic_index_cli/faststart.py          34      1    97%   15
agentic_index_cli/helpers.py             2      0   100%
agentic_index_cli/inject_readme.py       3      3     0%   1-4
agentic_index_cli/plot_trends.py         4      4     0%   3-7
agentic_index_cli/prune.py              50     11    78%   23, 25, 54-61, 65
agentic_index_cli/ranker.py              3      3     0%   1-4
agentic_index_cli/scraper.py             3      3     0%   1-4
------------------------------------------------------------------
TOTAL                                  342    244    29%
16 passed in 5.25s

The coverage gate is intentionally lenient. We target baseline plus twenty
percentage points, ratcheting upward only when tests improve significantly.
Edit `THRESHOLD` in `scripts/coverage_gate.py` to bump the requirement.
