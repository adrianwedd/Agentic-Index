# 🌐 Agentic-Index – The Data-Driven AI-Agent Repository Index

Agentic-Index continuously scores and curates every open-source framework for building autonomous AI agents. Fast search, transparent metrics, zero BS.

We rank everything using a transparent scoring formula based on:

  * 🌟 Stars & momentum
* 🔧 Maintenance & issue health
* 📚 Docs & examples
* 🧠 Ecosystem fit
* 📅 Recency
* ⚖️ Licensing

### Metrics Explained

| Emoji | Field | Formula | Updated | Source |
|-------|-------|---------|---------|--------|
| ⭐ | `stars_7d` | GitHub star Δ (7 days) | Nightly | `scraper/github.py` |
| 🔧 | `maintenance` | Issue/PR hygiene score | Weekly | `score/maintenance.py` |
| 📅 | `release_age` | Days since latest release | Nightly | `scraper/github.py` |
| 📚 | `docs_quality` | Heuristic score (README + examples) | Monthly | `score/docs.py` |
| 🧠 | `ecosystem_fit` | Keyword-based tag affinity | Monthly | `score/ecosystem.py` |
| ⚖️ | `license_score` | OSI compatibility / restrictiveness | Static | `score/license.py` |

Small fluctuations up to ±0.02 are normal between refreshes. See the [📊 Metrics Legend](#metrics-legend) for metric details. The full JSON schema is documented in [SCHEMA.md](SCHEMA.md).

> **🎯 TL;DR:** This isn’t just a list—it’s your launchpad for building with AI agents.

[🚀 Jump to Fast-Start Picks →](FAST_START.md)

-----

<p align="center">
![build](badges/build.svg)
![coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)
![docs](badges/docs.svg)
![Site](https://img.shields.io/website?down_message=offline&up_message=online&url=https%3A%2F%2Fadrianwedd.github.io%2FAgentic-Index)
![license](badges/license.svg)
![PyPI](badges/pypi.svg)
![Release Notes](https://img.shields.io/github/release/adrianwedd/Agentic-Index?include_prereleases)
</p>

This catalogue is maintained by the Agentic-Index project and is updated regularly (aiming for monthly refreshes) to reflect the rapidly evolving landscape of Agentic-AI.

-----

## TOC

* [✨ Why Agentic Index is Different](#-why-agentic-index-is-different)
* [⚡ Installation & Quick-start](#-installation--quick-start)
* [🏆 The Agentic-Index Top 100: AI Agent Repositories](#-the-agentic-index-top-100-ai-agent-repositories)
  * [💎 Honourable Mentions / Niche & Novel Gems](HONOURABLE.md)
    * [🔬 Our Methodology & Scoring Explained](#our-methodology--scoring-explained)
    * [🏷️ Category Definitions](#-category-definitions)
  * [🔄 Changelog](#-changelog)
  * [🏗 Architecture](#-architecture)
  * [🔧 Usage](#-usage)
  * [🔄 How refresh works](#-how-refresh-works)
  * [🧪 Testing](#-testing)
  * [🤝 How to Contribute](#-how-to-contribute)
  * [🛡 Code of Conduct](#-code-of-conduct)
  * [📜 License](#-license)

-----
<a id="-why-agentic-index-is-different"></a>

## ✨ Why Agentic Index is Different

In the fast-moving world of Agentic-AI, finding high-quality, actively maintained, and truly impactful frameworks can be a pain. Many lists are subjective or just track stars. Agentic-Index cuts through the noise with an analytical approach:

  * **Systematic Scoring:** Every repo gets crunched through our [transparent scoring formula](#our-methodology--scoring-explained). We look at real signals: community traction (stars [1, 2]), development activity (commit recency [1, 2]), maintenance health (issue management [3, 4]), documentation quality, license permissiveness [1, 2], and ecosystem integration.[1, 5] No black boxes.
  * **Focus on Builder Tools:** We spotlight frameworks, toolkits, and platforms that *actually help you build and orchestrate AI agents*. Check our [scope definition](./docs/methodology.md) for the nitty-gritty.
  * **Relentlessly Fresh:** Data gets a refresh monthly (or sooner if big shifts happen). Stale lists suck. Our [Changelog](./CHANGELOG.md) keeps score.
  * **Automated Vigilance:** A GitHub Action keeps an eye on things weekly, flagging big score or rank changes for review. This keeps the "freshness" promise real.
  * **Open & Transparent:** Our entire [methodology](./docs/methodology.md) – data sources, scoring weights, the lot – is out in the open. Trust through transparency.

Agentic-Index is built to be a reliable, data-driven launchpad for your next Agentic-AI project.
<a id="-installation--quick-start"></a>

## ⚡ Installation & Quick-start

```bash
pip install agentic-index-cli

agentic-index scrape --min-stars 100
agentic-index enrich data/repos.json
agentic-index rank data/repos.json
cat README.md | less         # see table injected
```

-----


<a id="-the-agentic-index-top-100-ai-agent-repositories"></a>
## 🏆 The Agentic-Index Top 100: AI Agent Repositories

The definitive list of Agentic-AI repositories, ranked by the Agentic Index Score. This score is a holistic measure of project quality, activity, and community love.
*(Data updated as of: {timestamp} UTC)*

<!-- TOP50:START -->
| Rank | <abbr title="Overall">📊</abbr> Overall | Repo | <abbr title="Stars gained in last 7 days">⭐ Δ7d</abbr> | <abbr title="Maintenance score">🔧 Maint</abbr> | <abbr title="Last release date">📅 Release</abbr> | <abbr title="Documentation score">📚 Docs</abbr> | <abbr title="Ecosystem fit">🧠 Fit</abbr> | <abbr title="License">⚖️ License</abbr> |
|-----:|------:|------|-------:|-------:|-----------|-------:|-------:|---------|
| 1 | 6.08 | dify | 123 | 0.90 | 2025-06-01 | 0.80 | 0.70 | NOASSERTION |
| 2 | 5.96 | langflow | 0 | - | - | - | - | MIT |
| 3 | 5.88 | browser-use | 0 | - | - | - | - | MIT |
| 4 | 5.84 | OpenHands | 0 | - | - | - | - | MIT |
| 5 | 5.83 | lobe-chat | 0 | - | - | - | - | NOASSERTION |
| 6 | 5.82 | MetaGPT | 0 | - | - | - | - | MIT |
| 7 | 5.81 | ragflow | 0 | - | - | - | - | Apache-2.0 |
| 8 | 5.79 | LLaMA-Factory | 0 | - | - | - | - | Apache-2.0 |
| 9 | 5.78 | system-prompts-and-models... | 0 | - | - | - | - | GPL-3.0 |
| 10 | 5.72 | cline | 0 | - | - | - | - | Apache-2.0 |
| 11 | 5.71 | anything-llm | 0 | - | - | - | - | MIT |
| 12 | 5.68 | llama_index | 0 | - | - | - | - | MIT |
| 13 | 5.67 | autogen | 0 | - | - | - | - | CC-BY-4.0 |
| 14 | 5.63 | awesome-llm-apps | 0 | - | - | - | - | Apache-2.0 |
| 15 | 5.60 | Flowise | 0 | - | - | - | - | NOASSERTION |
| 16 | 5.57 | mem0 | 0 | - | - | - | - | Apache-2.0 |
| 17 | 5.56 | ChatTTS | 0 | - | - | - | - | AGPL-3.0 |
| 18 | 5.56 | Langchain-Chatchat | 0 | - | - | - | - | Apache-2.0 |
| 19 | 5.55 | crewAI | 0 | - | - | - | - | MIT |
| 20 | 5.51 | AgentGPT | 0 | - | - | - | - | GPL-3.0 |
| 21 | 5.47 | agno | 0 | - | - | - | - | MPL-2.0 |
| 22 | 5.46 | khoj | 0 | - | - | - | - | AGPL-3.0 |
| 23 | 5.45 | ChatDev | 0 | - | - | - | - | Apache-2.0 |
| 24 | 5.45 | LibreChat | 0 | - | - | - | - | MIT |
| 25 | 5.43 | ai-agents-for-beginners | 0 | - | - | - | - | MIT |
| 26 | 5.43 | cherry-studio | 0 | - | - | - | - | NOASSERTION |
| 27 | 5.43 | Jobs_Applier_AI_Agent_AIHawk | 0 | - | - | - | - | AGPL-3.0 |
| 28 | 5.42 | qlib | 0 | - | - | - | - | MIT |
| 29 | 5.37 | composio | 0 | - | - | - | - | NOASSERTION |
| 30 | 5.36 | FastGPT | 0 | - | - | - | - | NOASSERTION |
| 31 | 5.35 | gpt-researcher | 0 | - | - | - | - | Apache-2.0 |
| 32 | 5.33 | CopilotKit | 0 | - | - | - | - | MIT |
| 33 | 5.33 | haystack | 0 | - | - | - | - | Apache-2.0 |
| 34 | 5.26 | swarm | 0 | - | - | - | - | MIT |
| 35 | 5.24 | agentic | 0 | - | - | - | - | MIT |
| 36 | 5.23 | vanna | 0 | - | - | - | - | MIT |
| 37 | 5.21 | DB-GPT | 0 | - | - | - | - | MIT |
| 38 | 5.21 | deep-research | 0 | - | - | - | - | MIT |
| 39 | 5.21 | letta | 0 | - | - | - | - | Apache-2.0 |
| 40 | 5.20 | agenticSeek | 0 | - | - | - | - | GPL-3.0 |
| 41 | 5.20 | SWE-agent | 0 | - | - | - | - | MIT |
| 42 | 5.19 | eliza | 0 | - | - | - | - | MIT |
| 43 | 5.19 | RagaAI-Catalyst | 0 | - | - | - | - | Apache-2.0 |
| 44 | 5.18 | DocsGPT | 0 | - | - | - | - | MIT |
| 45 | 5.17 | awesome-ai-agents | 0 | - | - | - | - | NOASSERTION |
| 46 | 5.14 | devika | 0 | - | - | - | - | MIT |
| 47 | 5.14 | goose | 0 | - | - | - | - | Apache-2.0 |
| 48 | 5.13 | suna | 0 | - | - | - | - | Apache-2.0 |
| 49 | 5.13 | SuperAGI | 0 | - | - | - | - | MIT |
| 50 | 5.12 | ai-pdf-chatbot-langchain | 0 | - | - | - | - | MIT |
| 51 | 5.12 | dagger | 0 | - | - | - | - | Apache-2.0 |
| 52 | 5.11 | activepieces | 0 | - | - | - | - | NOASSERTION |
| 53 | 5.11 | botpress | 0 | - | - | - | - | MIT |
| 54 | 5.11 | plandex | 0 | - | - | - | - | MIT |
| 55 | 5.11 | web-ui | 0 | - | - | - | - | MIT |
| 56 | 5.10 | ai | 0 | - | - | - | - | NOASSERTION |
| 57 | 5.10 | deer-flow | 0 | - | - | - | - | MIT |
| 58 | 5.08 | camel | 0 | - | - | - | - | Apache-2.0 |
| 59 | 5.08 | ChuanhuChatGPT | 0 | - | - | - | - | GPL-3.0 |
| 60 | 5.08 | mastra | 0 | - | - | - | - | NOASSERTION |
| 61 | 5.04 | GenAI_Agents | 0 | - | - | - | - | NOASSERTION |
| 62 | 5.02 | Llama-Chinese | 0 | - | - | - | - | - |
| 63 | 5.02 | openai-agents-python | 0 | - | - | - | - | MIT |
| 64 | 5.01 | graphiti | 0 | - | - | - | - | Apache-2.0 |
| 65 | 4.99 | LangBot | 0 | - | - | - | - | AGPL-3.0 |
| 66 | 4.96 | pydantic-ai | 0 | - | - | - | - | MIT |
| 67 | 4.95 | adk-python | 0 | - | - | - | - | Apache-2.0 |
| 68 | 4.94 | ai-engineering-hub | 0 | - | - | - | - | MIT |
| 69 | 4.93 | opik | 0 | - | - | - | - | Apache-2.0 |
| 70 | 4.93 | Qwen-Agent | 0 | - | - | - | - | Apache-2.0 |
| 71 | 4.89 | agent-zero | 0 | - | - | - | - | NOASSERTION |
| 72 | 4.89 | bisheng | 0 | - | - | - | - | Apache-2.0 |
| 73 | 4.88 | AstrBot | 0 | - | - | - | - | AGPL-3.0 |
| 74 | 4.88 | E2B | 0 | - | - | - | - | Apache-2.0 |
| 75 | 4.87 | cua | 0 | - | - | - | - | MIT |
| 76 | 4.85 | Figma-Context-MCP | 0 | - | - | - | - | MIT |
| 77 | 4.82 | Bert-VITS2 | 0 | - | - | - | - | AGPL-3.0 |
| 78 | 4.81 | Upsonic | 0 | - | - | - | - | MIT |
| 79 | 4.80 | agentscope | 0 | - | - | - | - | Apache-2.0 |
| 80 | 4.80 | pr-agent | 0 | - | - | - | - | AGPL-3.0 |
| 81 | 4.80 | UFO | 0 | - | - | - | - | MIT |
| 82 | 4.79 | awesome-LLM-resources | 0 | - | - | - | - | Apache-2.0 |
| 83 | 4.79 | WrenAI | 0 | - | - | - | - | AGPL-3.0 |
| 84 | 4.78 | OpenRLHF | 0 | - | - | - | - | Apache-2.0 |
| 85 | 4.78 | promptfoo | 0 | - | - | - | - | MIT |
| 86 | 4.77 | aichat | 0 | - | - | - | - | Apache-2.0 |
| 87 | 4.77 | R2R | 0 | - | - | - | - | MIT |
| 88 | 4.75 | nanobrowser | 0 | - | - | - | - | Apache-2.0 |
| 89 | 4.73 | intentkit | 0 | - | - | - | - | MIT |
| 90 | 4.72 | agents | 0 | - | - | - | - | Apache-2.0 |
| 91 | 4.71 | deep-searcher | 0 | - | - | - | - | Apache-2.0 |
| 92 | 4.70 | XAgent | 0 | - | - | - | - | Apache-2.0 |
| 93 | 4.69 | agent-squad | 0 | - | - | - | - | Apache-2.0 |
| 94 | 4.68 | LLocalSearch | 0 | - | - | - | - | Apache-2.0 |
| 95 | 4.68 | RD-Agent | 0 | - | - | - | - | MIT |
| 96 | 4.67 | lamda | 0 | - | - | - | - | - |
| 97 | 4.67 | TaskWeaver | 0 | - | - | - | - | MIT |
| 98 | 4.66 | mcp-agent | 0 | - | - | - | - | Apache-2.0 |
| 99 | 4.66 | superagent | 0 | - | - | - | - | MIT |
| 100 | 4.66 | ten-framework | 0 | - | - | - | - | NOASSERTION |
<!-- TOP50:END -->
*➡️ Dig into how these scores are cooked up in our [Methodology section](#our-methodology--scoring-explained) and the [full recipe in /docs/methodology.md](./docs/methodology.md).*

<a id="metrics-legend"></a>

<details>
<summary>📊 Metrics Legend</summary>

Our score blends stars, recency, issue health, docs completeness, license freedom and ecosystem integration. **[See full formula →](./docs/methodology.md#scoring-formula)**
- ⭐ Δ7d = stars gained in the last 7 days
- 🔧 Maint = 1 / (days_since_last_commit * open_issue_ratio)
- 📅 Release = 1 / days_since_last_release
- 📚 Docs = 1 if README > 300 words & has code else 0
- 🧠 Fit = fraction of ecosystem keywords matched
- ⚖️ License = 1 for permissive, 0.5 for viral, 0 if none
- Missing data for a metric shows as `-` instead of `0.00`

</details>

For a full description of every metric field, see [SCHEMA.md](./docs/SCHEMA.md).

-----

### Our Methodology & Scoring Explained

<a id="our-methodology--scoring-explained"></a>
\<details\>
\<summary\>🔬 Our Methodology & Scoring Explained (Click to Expand)\</summary\>

Agentic-Index believes in full transparency. Here’s the lowdown on how we find, vet, and score repositories.

Our score balances stars, recency, maintenance health, documentation quality, license freedom, and ecosystem fit. **[See full formula →](./docs/methodology.md#scoring-formula)**

**Quick Look at Components:**

  * **Seed Discovery:** GitHub searches (e.g., `"agent framework"`, `"LLM agent"`), topic filters (e.g., `topic:agent` [17]), and crawling curated lists [24, 25, 7] to cast a wide net.
  * **Metadata Harvest:** Pulling key data: stars, forks, open/closed issues, commit dates, language, license, README snippets. (Examples: [13, 1, 12, 26, 23, 2, 10, 8, 3, 14, 15, 16, 19, 22, 27, 28] and many others as detailed in `docs/methodology.md`)
  * **Quality & Activity Scoring:** The formula balances community buzz, dev activity, maintenance, docs, license, and how well it plays with others.
  * **De-duplication & Categorisation:** Forks usually get skipped unless they’re their own thing now. Repos get bucketed by their main gig.

For the full, unabridged version, see **[./docs/methodology.md](./docs/methodology.md)**.

\</details\>

-----

<a id="-category-definitions"></a>
## 🏷️ Category Definitions

Quick guide to our categories (and the icons you'll see in the table):

  * 🌐 **General-purpose:** Flexible frameworks for all sorts of agentic tasks (e.g., Langchain [8]).
  * 🤖 **Multi-Agent Coordination:** For orchestrating teams of collaborating agents (e.g., CrewAI [1]).
  * 📚 **RAG-centric:** Focused on agents that are wizards at Retrieval-Augmented Generation (e.g., AutoAgent's Agentic-RAG [29]).
  * 🎯 **Domain-Specific:** Tools built for specific industries or tasks (e.g., `video-db/Director` [22]).
  * 🛠️ **DevTools:** Libraries and platforms to help you build, test, deploy, or secure agents (e.g., `msoedov/agentic_security` [23]).
  * 🧪 **Experimental:** Bleeding-edge, research-heavy, or early-stage projects (e.g., BabyAGI [3]).

-----

<a id="-changelog"></a>
## 🔄 Changelog

This isn't a static list. It's alive\! See [CHANGELOG.md](./CHANGELOG.md) for all the adds, drops, and major rank shuffles.

-----

<a id="-architecture"></a>
## 🏗 Architecture


![System Architecture](docs/architecture.svg)

-----

<a id="-usage"></a>
## 🔧 Usage

Run the indexer to fetch fresh repo data:

```bash
python -m agentic_index_cli.agentic_index --min-stars 50 --iterations 1 --output data
```

The CLI reads tuning parameters from `agentic_index_cli/config.yaml`. Use
`--config my.yml` with any command to override these defaults.

Generated tables live in the `data/` directory.

<a id="-how-refresh-works"></a>
## 🔄 How refresh works

A scheduled GitHub Action keeps the index up to date. It runs the scraper and
ranker, opens a pull request with any changes, and can auto-merge when all
checks pass. You can also trigger this process manually by running
[`scripts/trigger_refresh.sh`](scripts/trigger_refresh.sh).

<a id="-testing"></a>
## 🧪 Testing

This project uses `pytest` for unit tests and [pa11y](https://github.com/pa11y/pa11y) for accessibility checks. Ensure Chrome is installed before running pa11y:

```bash
# via puppeteer
npx puppeteer browsers install chrome
# or with apt
sudo apt-get install -y chromium
```

Run tests with:

```bash
pytest -q
```

CI runs tests with network access disabled. Set `CI_OFFLINE=1` or run
`pytest --disable-socket` locally to replicate the offline environment.
An autouse fixture still permits UNIX-domain `socketpair()` calls so FastAPI's
`TestClient` can start its event loop.

To check accessibility after building the site:

```bash
npx pa11y web/index.html
```

You can also run `./scripts/install_pa11y_deps.sh` to install pa11y and Chrome.

## 💻 Developer

To trigger a data refresh via GitHub Actions, run:

```bash
bash scripts/trigger_refresh.sh 75
```

Replace `75` with your desired minimum star count. The script requires the GitHub CLI and an authenticated token.
Set a personal access token via the `GITHUB_TOKEN_REPO_STATS` environment variable to avoid hitting rate limits when scraping.

-----

<a id="-how-to-contribute"></a>
## 🤝 How to Contribute

Agentic-Index aims to be *the* spot for Agentic-AI frameworks. Your brainpower and suggestions are gold.

Check out [CONTRIBUTING.md](./CONTRIBUTING.md) for how to:

  * Nominate new repositories.
  * Flag outdated info or errors.
  * Suggest tweaks to scoring or categories.
  * Understand what makes a repo eligible.
  * Install [Git LFS](https://git-lfs.github.com/) and run `git lfs install`.
    PNG and GIF assets are tracked via LFS.
  * Set up your dev environment with [DEVELOPMENT.md](./docs/DEVELOPMENT.md).
  * Install dependencies with `scripts/agent-setup.sh`.

For tips on keeping your branch in sync with `main` and resolving conflicts, see
[CONFLICT_RESOLUTION.md](./docs/CONFLICT_RESOLUTION.md).

Let's build the best damn agent list together\!


-----
<a id="-code-of-conduct"></a>
## 🛡 Code of Conduct

Please see our [Code of Conduct](./CODE_OF_CONDUCT.md) for contributor expectations.


<a id="-license"></a>
## 📜 License

The content of Agentic-Index (this `README.md`, files in `/docs/`, etc.) is licensed under([https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/)).

Any scripts or code for analysis and generation (e.g., in `/scripts`, if we add 'em) are licensed under([https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)).

© 2025 Agentic-Index Maintainers


![Last Sync](badges/last_sync.svg) ![Top Repo](badges/top_repo.svg) ![Repo Count](badges/repo_count.svg)
