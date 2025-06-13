"""Utility to verify that ``data/top50.md`` uses the correct table schema."""

EXPECTED_HEADER = [
    "Rank", "Repo (Click to Visit)", "★ Stars",
    "Last Commit", "Score", "Category", "One-Liner"
]

with open("data/top50.md", encoding="utf-8") as f:
    rows = [line.strip() for line in f if line.startswith("|")]

first_row = rows[0].strip("| ").split(" | ")
assert first_row == EXPECTED_HEADER, (
    "TOP50 table header is wrong; expected 7-column full schema."
)
print("top50.md validated")

