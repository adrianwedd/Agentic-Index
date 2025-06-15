"""Generate a dummy ``repos.json`` file for testing."""

import json

# Placeholder script generating example repos.json
sample = [
    {"name": "repo1", "AgentOpsScore": 10},
    {"name": "repo2", "AgentOpsScore": 9},
    {"name": "repo3", "AgentOpsScore": 8},
    {"name": "repo4", "AgentOpsScore": 7},
    {"name": "repo5", "AgentOpsScore": 6},
]

with open("repos.json", "w") as f:
    json.dump(sample, f)
