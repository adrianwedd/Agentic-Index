from agentops_cli.agentops import run_index

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Agentic Index CLI")
    parser.add_argument("--min-stars", type=int, default=0)
    parser.add_argument("--iterations", type=int, default=1)
    parser.add_argument("--output", type=str, default="data")
    args = parser.parse_args()
    run_index(args.min_stars, args.iterations, args.output)
