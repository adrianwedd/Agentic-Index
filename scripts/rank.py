#!/usr/bin/env python3
from agentic_index_cli.internal.rank import main, generate_badges

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "data/repos.json"
    main(path)
