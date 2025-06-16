# 🌐 Agentic-Index – The Data-Driven AI-Agent Repository Index

Agentic-Index continuously scores and curates every open-source framework for building autonomous AI agents. Fast search, transparent metrics, zero BS.

We rank everything using a transparent scoring formula based on:

  * 🌟 Stars & momentum
  * 🔧 Maintenance & issue health
  * 📚 Docs & examples
  * 🧠 Ecosystem fit
  * 📅 Recency
  * ⚖️ Licensing

> **🎯 TL;DR:** This isn’t just a list—it’s your launchpad for building with AI agents.

Want a shortcut? Jump to the [Fast-Start table](FAST_START.md).

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
* [🚀 Fast-Start Picks (Curated for Newcomers)](#-fast-start-picks-curated-for-newcomers)
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

<a id="-fast-start-picks-curated-for-newcomers"></a>
## 🚀 Fast-Start Picks (Curated for Newcomers)

New to Agentic-AI or just want the good stuff fast? These repos are top-tier for usability, community, docs, or just plain cool ideas:

  * **CrewAI ([crewAIInc/crewAI](https://github.com/crewAIInc/crewAI))**: Slick orchestration for role-playing, autonomous AI agents. Built for collaborative intelligence. [1]
  * **AutoGen ([microsoft/autogen](https://github.com/microsoft/autogen))**: Microsoft's powerhouse for multi-agent conversational apps. Flexible and robust. [6, 7, 2]
  * **Langchain ([langchain-ai/langchain](https://github.com/langchain-ai/langchain))**: The OG. A massive library for LLM apps with deep agent capabilities and tons of integrations. [8, 9]
  * **AutoGPT ((https://github.com/Significant-Gravitas/AutoGPT))**: One of the first to show off truly autonomous GPT-4, making agentic concepts go viral. [10, 11]
  * **BabyAGI ([yoheinakajima/babyagi](https://github.com/yoheinakajima/babyagi))**: Simple, elegant task management loop that inspired a generation of agent frameworks. [3]
  * **VoltAgent ([VoltAgent/voltagent](https://github.com/VoltAgent/voltagent))**: Clean TypeScript framework for modular AI agent dev, with built-in observability. [12]

-----

<a id="-the-agentic-index-top-100-ai-agent-repositories"></a>
## 🏆 The Agentic-Index Top 100: AI Agent Repositories

The definitive list of Agentic-AI repositories, ranked by the Agentic Index Score. This score is a holistic measure of project quality, activity, and community love.
*(Data updated as of: 2025-06-16T17:39:49 UTC)*

<!-- TOP50:START -->
| Rank | Repo | Score | Stars | Δ Stars | Δ Score | Recency | Issue Health | Doc Complete | License Freedom | Ecosystem | log₂(Stars) | Category |
|-----:|------|------:|------:|--------:|--------:|-------:|-------------:|-------------:|---------------:|---------:|------------:|----------|
| 1 | dify | 6.07 | 103135 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 16.65 | General-purpose |
| 2 | langflow | 5.96 | 73030 |  | +0 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 16.16 | DevTools |
| 3 | browser-use | 5.88 | 63085 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.95 | General-purpose |
| 4 | OpenHands | 5.84 | 57980 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.82 | General-purpose |
| 5 | lobe-chat | 5.83 | 62452 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 15.93 | RAG-centric |
| 6 | MetaGPT | 5.82 | 56381 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.78 | Multi-Agent Coordination |
| 7 | ragflow | 5.81 | 55032 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.75 | RAG-centric |
| 8 | LLaMA-Factory | 5.79 | 52214 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.67 | General-purpose |
| 9 | system-prompts-and-models... | 5.78 | 57188 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 15.80 | DevTools |
| 10 | cline | 5.72 | 45640 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.48 | General-purpose |
| 11 | anything-llm | 5.71 | 45276 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.47 | RAG-centric |
| 12 | llama_index | 5.68 | 42328 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.37 | General-purpose |
| 13 | autogen | 5.67 | 45934 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 15.49 | General-purpose |
| 14 | awesome-llm-apps | 5.63 | 38434 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.23 | RAG-centric |
| 15 | Flowise | 5.60 | 39990 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 15.29 | General-purpose |
| 16 | mem0 | 5.57 | 34409 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.07 | General-purpose |
| 17 | ChatTTS | 5.56 | 36777 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 15.17 | General-purpose |
| 18 | Langchain-Chatchat | 5.56 | 35279 |  |  | 0.85 | 0.00 | 0.00 | 1.00 | 0.00 | 15.11 | RAG-centric |
| 19 | crewAI | 5.55 | 32869 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 15.00 | Multi-Agent Coordination |
| 20 | AgentGPT | 5.51 | 34319 |  |  | 0.95 | 0.00 | 0.00 | 0.50 | 0.00 | 15.07 | General-purpose |
| 21 | agno | 5.47 | 28227 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.78 | Multi-Agent Coordination |
| 22 | khoj | 5.46 | 30318 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.89 | Experimental |
| 23 | ChatDev | 5.45 | 27021 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.72 | Multi-Agent Coordination |
| 24 | LibreChat | 5.45 | 26727 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.71 | General-purpose |
| 25 | ai-agents-for-beginners | 5.43 | 26018 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.67 | General-purpose |
| 26 | cherry-studio | 5.43 | 28392 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.79 | General-purpose |
| 27 | Jobs_Applier_AI_Agent_AIHawk | 5.43 | 28304 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.79 | General-purpose |
| 28 | qlib | 5.42 | 25080 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.61 | Experimental |
| 29 | composio | 5.37 | 25493 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.64 | General-purpose |
| 30 | FastGPT | 5.36 | 24714 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.59 | RAG-centric |
| 31 | gpt-researcher | 5.35 | 21855 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.42 | Experimental |
| 32 | CopilotKit | 5.33 | 21149 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.37 | General-purpose |
| 33 | haystack | 5.33 | 21141 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.37 | RAG-centric |
| 34 | swarm | 5.26 | 19917 |  |  | 0.81 | 0.00 | 0.00 | 1.00 | 0.00 | 14.28 | Multi-Agent Coordination |
| 35 | agentic | 5.24 | 17632 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.11 | General-purpose |
| 36 | vanna | 5.23 | 18102 |  |  | 0.90 | 0.00 | 0.00 | 1.00 | 0.00 | 14.14 | RAG-centric |
| 37 | DB-GPT | 5.21 | 16757 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.03 | General-purpose |
| 38 | deep-research | 5.21 | 16627 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.02 | Experimental |
| 39 | letta | 5.21 | 16841 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 14.04 | General-purpose |
| 40 | agenticSeek | 5.20 | 18115 |  |  | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | 14.14 | General-purpose |
| 41 | SWE-agent | 5.20 | 16282 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.99 | General-purpose |
| 42 | eliza | 5.19 | 16065 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.97 | General-purpose |
| 43 | RagaAI-Catalyst | 5.19 | 16188 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.98 | RAG-centric |
| 44 | DocsGPT | 5.18 | 15708 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.94 | DevTools |
| 45 | awesome-ai-agents | 5.17 | 18563 |  |  | 0.77 | 0.00 | 0.00 | 0.50 | 0.00 | 14.18 | General-purpose |
| 46 | devika | 5.14 | 19330 |  |  | 0.29 | 0.00 | 0.00 | 1.00 | 0.00 | 14.24 | Experimental |
| 47 | goose | 5.14 | 14558 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.83 | General-purpose |
| 48 | suna | 5.13 | 14367 |  |  | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 13.81 | General-purpose |
| 49 | SuperAGI | 5.13 | 16412 |  |  | 0.67 | 0.00 | 0.00 | 1.00 | 0.00 | 14.00 | RAG-centric |
| 50 | ai-pdf-chatbot-langchain | 5.12 | 15572 |  |  | 0.75 | 0.00 | 0.00 | 1.00 | 0.00 | 13.93 | General-purpose |
<!-- TOP50:END -->
*➡️ Dig into how these scores are cooked up in our [Methodology section](#our-methodology--scoring-explained) and the [full recipe in /docs/methodology.md](./docs/methodology.md).*

<details>
<summary>📊 Metrics Legend</summary>

- Our score blends stars, recency, issue health, docs completeness, license freedom and ecosystem integration. **[See full formula →](./docs/methodology.md#scoring-formula)**
- ⭐ Δ7d = stars gained in the last 7 days
- 🔧 Maint = 1 / (days_since_last_commit * open_issue_ratio)
- 📅 Release = 1 / days_since_last_release
- 📚 Docs = 1 if README > 300 words & has code else 0
- 🧠 Fit = fraction of ecosystem keywords matched
- ⚖️ License = 1 for permissive, 0.5 for viral, 0 if none

</details>

-----

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

```mermaid
flowchart LR
    A[User] --> B[Scrape]
    B --> C[JSON]
    C --> D[Rank]
    D --> E[Markdown]
    E --> F[View]
```

-----

<a id="-usage"></a>
## 🔧 Usage

Run the indexer to fetch fresh repo data:

```bash
python -m agentic_index_cli.agentic_index --min-stars 50 --iterations 1 --output data
```

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

### Troubleshooting

If collection fails with messages like `ImportError: No module named 'responses'`,
make sure all test dependencies are installed:

```bash
pip install -r requirements.txt
```

You may also see `Missing required environment variables:` errors when
`CI_OFFLINE` or API tokens are unset. Export the variables before running tests:

```bash
export CI_OFFLINE=1
```

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

For tips on keeping your branch in sync with `main` and resolving conflicts, see
[CONFLICT_RESOLUTION.md](./docs/CONFLICT_RESOLUTION.md).

Let's build the best damn agent list together\!
![Code of Conduct](badges/coc.svg)


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
