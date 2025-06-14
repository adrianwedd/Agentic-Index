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
<a href="https://github.com/adrianwedd/Agentic-Index/actions/workflows/ci.yml"><img src="badges/build.svg" alt="build"></a>
<a href="badges/coverage.svg"><img src="badges/coverage.svg" alt="coverage"></a>
<a href="https://adrianwedd.github.io/Agentic-Index/"><img src="badges/docs.svg" alt="docs"></a>
<a href="https://adrianwedd.github.io/Agentic-Index/"><img src="https://img.shields.io/website?down_message=offline&up_message=online&url=https%3A%2F%2Fadrianwedd.github.io%2FAgentic-Index" alt="Site"></a>
<a href="./LICENSE.md"><img src="badges/license.svg" alt="license"></a>
<a href="https://pypi.org/project/agentic-index-cli/"><img src="badges/pypi.svg" alt="PyPI"></a>
<a href="https://github.com/adrianwedd/Agentic-Index/releases"><img src="https://img.shields.io/github/release/adrianwedd/Agentic-Index?include_prereleases" alt="Release Notes"></a>
</p>

This catalogue is maintained by the Agentic-Index project and is updated regularly (aiming for monthly refreshes) to reflect the rapidly evolving landscape of Agentic-AI.

-----

## TOC

* [✨ Why Agentic Index is Different](#-why-agentic-index-is-different)
* [🚀 Fast-Start Picks (Curated for Newcomers)](#-fast-start-picks-curated-for-newcomers)
* [⚡ Installation & Quick-start](#-installation--quick-start)
* [🏆 The Agentic-Index Top 50: AI Agent Repositories](#-the-agentic-index-top-50-ai-agent-repositories)
  * [💎 Honourable Mentions / Niche & Novel Gems](#-honourable-mentions--niche--novel-gems)
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

<a id="-the-agentic-index-top-50-ai-agent-repositories"></a>
## 🏆 The Agentic-Index Top 50: AI Agent Repositories

The definitive list of Agentic-AI repositories, ranked by the Agentic Index Score. This score is a holistic measure of project quality, activity, and community love.
*(Data updated as of: {timestamp} UTC)*

<!-- TOP50:START -->
| Rank | Repo | Score | ▲ StarsΔ | ▲ ScoreΔ | Category |
|-----:|------|------:|-------:|--------:|----------|
| 1 | dify | 6.08 |  |  | General-purpose |
| 2 | langflow | 5.95 |  |  | DevTools |
| 3 | browser-use | 5.88 |  |  | General-purpose |
| 4 | OpenHands | 5.84 |  |  | General-purpose |
| 5 | lobe-chat | 5.83 |  |  | RAG-centric |
| 6 | MetaGPT | 5.82 |  |  | Multi-Agent Coordination |
| 7 | ragflow | 5.81 |  |  | RAG-centric |
| 8 | LLaMA-Factory | 5.79 |  |  | General-purpose |
| 9 | system-prompts-and-models-of-ai-tools | 5.78 |  |  | DevTools |
| 10 | cline | 5.72 |  |  | General-purpose |
| 11 | anything-llm | 5.71 |  |  | RAG-centric |
| 12 | llama_index | 5.68 |  |  | General-purpose |
| 13 | autogen | 5.67 |  |  | General-purpose |
| 14 | awesome-llm-apps | 5.63 |  |  | RAG-centric |
| 15 | Flowise | 5.60 |  |  | General-purpose |
| 16 | mem0 | 5.57 |  |  | General-purpose |
| 17 | ChatTTS | 5.56 |  |  | General-purpose |
| 18 | Langchain-Chatchat | 5.56 |  |  | RAG-centric |
| 19 | crewAI | 5.55 |  |  | Multi-Agent Coordination |
| 20 | AgentGPT | 5.51 |  |  | General-purpose |
| 21 | agno | 5.47 |  |  | Multi-Agent Coordination |
| 22 | khoj | 5.46 |  |  | Experimental |
| 23 | ChatDev | 5.45 |  |  | Multi-Agent Coordination |
| 24 | LibreChat | 5.45 |  |  | General-purpose |
| 25 | ai-agents-for-beginners | 5.43 |  |  | General-purpose |
| 26 | cherry-studio | 5.43 |  |  | General-purpose |
| 27 | Jobs_Applier_AI_Agent_AIHawk | 5.43 |  |  | General-purpose |
| 28 | qlib | 5.42 |  |  | Experimental |
| 29 | composio | 5.37 |  |  | General-purpose |
| 30 | FastGPT | 5.36 |  |  | RAG-centric |
| 31 | gpt-researcher | 5.35 |  |  | Experimental |
| 32 | CopilotKit | 5.33 |  |  | General-purpose |
| 33 | haystack | 5.33 |  |  | RAG-centric |
| 34 | swarm | 5.26 |  |  | Multi-Agent Coordination |
| 35 | agentic | 5.24 |  |  | General-purpose |
| 36 | vanna | 5.23 |  |  | RAG-centric |
| 37 | DB-GPT | 5.21 |  |  | General-purpose |
| 38 | deep-research | 5.21 |  |  | Experimental |
| 39 | letta | 5.21 |  |  | General-purpose |
| 40 | agenticSeek | 5.20 |  |  | General-purpose |
| 41 | SWE-agent | 5.20 |  |  | General-purpose |
| 42 | eliza | 5.19 |  |  | General-purpose |
| 43 | RagaAI-Catalyst | 5.19 |  |  | RAG-centric |
| 44 | DocsGPT | 5.18 |  |  | DevTools |
| 45 | awesome-ai-agents | 5.17 |  |  | General-purpose |
| 46 | devika | 5.14 |  |  | Experimental |
| 47 | goose | 5.14 |  |  | General-purpose |
| 48 | suna | 5.13 |  |  | General-purpose |
| 49 | SuperAGI | 5.13 |  |  | RAG-centric |
| 50 | ai-pdf-chatbot-langchain | 5.12 |  |  | General-purpose |
<!-- TOP50:END -->
*➡️ Dig into how these scores are cooked up in our [Methodology section](#our-methodology--scoring-explained) and the [full recipe in /docs/methodology.md](./docs/methodology.md).*

-----

<a id="-honourable-mentions--niche--novel-gems"></a>
## 💎 Honourable Mentions / Niche & Novel Gems

Beyond the top-ranked, these projects are cooking up unique ideas, serving specific niches, or pushing experimental boundaries in Agentic-AI:

  * **[daydreamsai/daydreams](https://github.com/daydreamsai/daydreams)**: 🎯 TypeScript framework for generative agents that live on-chain. AI meets web3. [17, 18]
  * **[fetchai/agents-aea](https://github.com/fetchai/agents-aea) & [valory-xyz/open-aea](https://github.com/valory-xyz/open-aea)**: 🎯 Dedicated frameworks for Autonomous Economic Agents (AEAs) in decentralized systems. [17, 19, 20]
  * **([https://github.com/ReversecLabs/damn-vulnerable-llm-agent](https://github.com/ReversecLabs/damn-vulnerable-llm-agent))**: 🛠️ Learn to break (and fix) ReAct agents. Essential for security-conscious devs. [21]
  * **(https://github.com/video-db/Director)**: 🎯 AI agent framework for serious video magic: search, edit, compile, generate. [17, 22]
  * **[msoedov/agentic\_security](https://github.com/msoedov/agentic_security)**: 🛠️ Open-source vulnerability scanner for Agent Workflows and LLMs. Stay safe out there. [23]

-----
### Our Methodology & Scoring Explained

<a id="our-methodology--scoring-explained"></a>
\<details\>
\<summary\>🔬 Our Methodology & Scoring Explained (Click to Expand)\</summary\>

Agentic-Index believes in full transparency. Here’s the lowdown on how we find, vet, and score repositories.

The core Agentic-Index Scoring Formula:
`Score = 0.35*log2(stars+1) + 0.20*recency_factor + 0.15*issue_health + 0.15*doc_completeness + 0.10*license_freedom + 0.05*ecosystem_integration`\<sup\>†\</sup\>

\<sup\>†\</sup\> *Weights are reviewed and potentially tuned quarterly. Full math and reasoning in [`/docs/methodology.md`](./docs/methodology.md).*

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
<a href="./CODE_OF_CONDUCT.md"><img src="badges/coc.svg" alt="Code of Conduct"></a>


-----
<a id="-code-of-conduct"></a>
## 🛡 Code of Conduct

Please see our [Code of Conduct](./CODE_OF_CONDUCT.md) for contributor expectations.


<a id="-license"></a>
## 📜 License

The content of Agentic-Index (this `README.md`, files in `/docs/`, etc.) is licensed under([https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/)).

Any scripts or code for analysis and generation (e.g., in `/scripts`, if we add 'em) are licensed under([https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)).

© 2025 Agentic-Index Maintainers


![Last Sync](badges/last_sync.svg) ![Top Repo](badges/top_repo.svg)