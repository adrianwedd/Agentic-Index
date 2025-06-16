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
| ⭐ | `stars_7d` | GitHub star Δ (7 days) | Nightly | `scripts/scrape_repos.py` |
| 🔧 | `maintenance` | Issue/PR hygiene score | Weekly | `score/maintenance.py` |
| 📅 | `release_age` | Days since latest release | Nightly | `scripts/scrape_repos.py` |
| 📚 | `docs_quality` | Heuristic score (README + examples) | Monthly | `score/docs.py` |
| 🧠 | `ecosystem_fit` | Keyword-based tag affinity | Monthly | `score/ecosystem.py` |
| ⚖️ | `license_score` | OSI compatibility / restrictiveness | Static | `score/license.py` |

Small fluctuations up to ±0.02 are normal between refreshes. See the [📊 Metrics Legend](#metrics-legend) for metric details. The full JSON schema is documented in [SCHEMA.md](SCHEMA.md). Detailed metric fields live in [docs/METRICS_SCHEMA.md](docs/METRICS_SCHEMA.md).

> **🎯 TL;DR:** This isn’t just a list—it’s your launchpad for building with AI agents.

[🚀 Jump to Fast-Start Picks →](FAST_START.md)

-----

<p align="center">
![build](badges/build.svg)
![coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)
![security](https://img.shields.io/badge/security-0%20issues-brightgreen)
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
*(Data updated as of: {timestamp})*

<!-- TOP50:START -->
| Rank | Repo | Score | Stars | Δ Stars | Δ Score | Recency | Issue Health | Doc Complete | License Freedom | Ecosystem | log₂(Stars) | Category |
|-----:|------|------:|------:|--------:|--------:|-------:|-------------:|-------------:|---------------:|---------:|------------:|----------|
| 1 | dify | 5.28 | 103268 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 16.66 | DevTools |
| 2 | langflow | 5.17 | 73776 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 16.17 | DevTools |
| 3 | browser-use | 5.10 | 63197 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.95 | General-purpose |
| 4 | OpenHands | 5.07 | 58086 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.83 | General-purpose |
| 5 | lobe-chat | 5.06 | 62457 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 15.93 | RAG-centric |
| 6 | MetaGPT | 5.06 | 56406 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.78 | Multi-Agent |
| 7 | ragflow | 5.04 | 55104 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.75 | RAG-centric |
| 8 | system-prompts-and-models... | 5.03 | 57495 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 15.81 | DevTools |
| 9 | LLaMA-Factory | 5.02 | 52281 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.67 | General-purpose |
| 10 | anything-llm | 4.96 | 45309 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.47 | RAG-centric |
| 11 | cline | 4.96 | 45704 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.48 | General-purpose |
| 12 | autogen | 4.93 | 45993 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 15.49 | General-purpose |
| 13 | llama_index | 4.93 | 42355 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.37 | General-purpose |
| 14 | awesome-llm-apps | 4.92 | 41125 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.33 | RAG-centric |
| 15 | Flowise | 4.87 | 40065 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 15.29 | General-purpose |
| 16 | ChatTTS | 4.84 | 36799 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 15.17 | General-purpose |
| 17 | mem0 | 4.84 | 34513 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.07 | General-purpose |
| 18 | crewAI | 4.82 | 32933 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.01 | Multi-Agent |
| 19 | Langchain-Chatchat | 4.81 | 35287 |  |  | 0.84 | 0.00 | 0.00 | 1.00 | 0.00 | 15.11 | RAG-centric |
| 20 | AgentGPT | 4.79 | 34323 |  |  | 0.95 | 0.00 | 0.00 | 0.50 | 0.00 | 15.07 | General-purpose |
| 21 | agno | 4.76 | 28280 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.79 | Multi-Agent |
| 22 | khoj | 4.75 | 30327 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.89 | Experimental |
| 23 | ChatDev | 4.74 | 27024 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.72 | Multi-Agent |
| 24 | ai-agents-for-beginners | 4.73 | 26615 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.70 | General-purpose |
| 25 | LibreChat | 4.73 | 26789 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.71 | General-purpose |
| 26 | cherry-studio | 4.72 | 28444 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.80 | General-purpose |
| 27 | Jobs_Applier_AI_Agent_AIHawk | 4.72 | 28310 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.79 | General-purpose |
| 28 | qlib | 4.71 | 25192 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.62 | Experimental |
| 29 | composio | 4.68 | 25499 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.64 | General-purpose |
| 30 | FastGPT | 4.66 | 24718 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.59 | RAG-centric |
| 31 | gpt-researcher | 4.65 | 21875 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.42 | Experimental |
| 32 | CopilotKit | 4.63 | 21205 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.37 | General-purpose |
| 33 | haystack | 4.63 | 21154 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.37 | RAG-centric |
| 34 | swarm | 4.56 | 19920 |  |  | 0.80 | 0.00 | 0.00 | 1.00 | 0.00 | 14.28 | Multi-Agent |
| 35 | agentic | 4.55 | 17639 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.11 | General-purpose |
| 36 | vanna | 4.54 | 18127 |  |  | 0.89 | 0.00 | 0.00 | 1.00 | 0.00 | 14.15 | RAG-centric |
| 37 | agenticSeek | 4.53 | 18268 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.16 | General-purpose |
| 38 | DB-GPT | 4.53 | 16764 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.03 | DevTools |
| 39 | deep-research | 4.53 | 16638 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.02 | Experimental |
| 40 | letta | 4.53 | 16861 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.04 | General-purpose |
| 41 | SWE-agent | 4.52 | 16305 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.99 | Domain-Specific |
| 42 | eliza | 4.51 | 16078 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.97 | General-purpose |
| 43 | RagaAI-Catalyst | 4.51 | 16193 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.98 | Multi-Agent |
| 44 | DocsGPT | 4.50 | 15708 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.94 | RAG-centric |
| 45 | awesome-ai-agents | 4.48 | 18587 |  |  | 0.76 | 0.00 | 0.00 | 0.50 | 0.00 | 14.18 | General-purpose |
| 46 | goose | 4.47 | 14627 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.84 | DevTools |
| 47 | activepieces | 4.46 | 15291 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 13.90 | General-purpose |
| 48 | suna | 4.46 | 14425 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.82 | General-purpose |
| 49 | ai | 4.45 | 14955 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 13.87 | DevTools |
| 50 | botpress | 4.45 | 13805 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.75 | General-purpose |

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

For a full description of every metric field, see [SCHEMA.md](./docs/SCHEMA.md) and [docs/METRICS_SCHEMA.md](docs/METRICS_SCHEMA.md).

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

A scheduled GitHub Action keeps the index up to date. It runs the extended
scraper and metric scoring before ranking repositories, then opens a pull
request with any changes and can auto-merge when all
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
  * Install dependencies with `scripts/agent-setup.sh` (includes formatting tools).

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
