import os
import pytest

from bench import benchmark as bench_module

pytestmark = pytest.mark.skipif(os.getenv("PERF") != "true", reason="perf tests disabled")


@pytest.mark.benchmark
def test_scrape_rank_benchmark(benchmark):
    benchmark(bench_module.run)
