# Performance Tuning

Large `repos.json` files can slow down table generation and diff checks.

## Recommended Limits

- Keep `repos.json` under **10 MB** for best CLI responsiveness.
- Use the `--top` option of `faststart` to limit rows when testing locally.

## Tips

- Enable caching by passing `use_cache=True` to `load_repos` when repeatedly
  loading the same file. Cached reads are skipped if the file has not changed.
- Install `ijson` to parse very large JSON files in streaming mode:
  ```bash
  pip install ijson
  ```
  Then call `load_repos(..., use_stream=True)`.
- Run `scripts/benchmark_ops.py` to measure sort and diff times. The script
  prints a warning when operations exceed built-in baselines.
