# Methodology

AgentOps ranking and research utilities.

This module encapsulates the high-level research loop used for the AgentOps catalogue. The
process begins by seeding GitHub searches with a mix of hand curated queries and topic
filters. Each query fetches a batch of repositories through the GitHub API. Results are
stored and we capture repo metadata such as stars, forks, issue counts, commit history,
primary language, and license information. The crawler also pulls README excerpts so that
projects can be categorised and assessed for documentation quality.

After harvesting raw data we compute a composite score for each repository. The goal of the
score is to surface well maintained, permissively licensed projects that demonstrate strong
community traction. We normalise recency so that active projects are favoured, but we do not
penalise established libraries. Issue health looks at the ratio of open to closed issues to
spot abandoned repos. Documentation completeness checks for a reasonably detailed README
and inline code examples. License freedom considers whether a project uses a permissive or
viral license. Finally, ecosystem integration detects references to popular agent frameworks
or tooling within the README text and repository topics.

The research loop repeats until the top results stabilise across multiple iterations. This
helps smooth out one-off spikes in GitHub search results. Between iterations we also prune
repositories that fall below a minimum star threshold or that clearly lie outside the
framework or tooling categories. The output is a ranked CSV and Markdown table describing
the top repositories along with a simple changelog noting additions or removals since the
previous run.

This docstring acts as the canonical description of the research workflow so that
`docs/METHODOLOGY.md` can be auto-generated and kept in sync with the code. Running the
`gen_methodology.py` script extracts this text and combines it with the scoring formula from
the README to produce the full documentation.

The collected metrics are versioned with each run so that score trends can be analysed over time. We encourage community contributions via pull requests, which can add new search seeds or propose changes to the weighting scheme. Because everything is scripted, the entire pipeline can be executed locally for transparency. The methodology outlined here reflects our current best attempt at a fair ranking system, and feedback is always welcome. Our approach aims to remain lightweight and reproducible so other researchers can fork the pipeline, rerun it on new datasets, and compare results with minimal fuss.

## Scoring Formula

`Score = 0.35*log2(stars+1) + 0.20*recency_factor + 0.15*issue_health + 0.15*doc_completeness + 0.10*license_freedom + 0.05*ecosystem_integration`\<sup\>†\</sup\>
