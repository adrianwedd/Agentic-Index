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

![build](badges/build.svg) ![coverage](https://img.shields.io/badge/coverage-80%25-brightgreen) ![security](https://img.shields.io/badge/security-0%20issues-brightgreen) ![docs](badges/docs.svg) ![Site](https://img.shields.io/website?down_message=offline&up_message=online&url=https%3A%2F%2Fadrianwedd.github.io%2FAgentic-Index) ![license](badges/license.svg) ![PyPI](badges/pypi.svg) ![Release Notes](https://img.shields.io/github/release/adrianwedd/Agentic-Index?include_prereleases)

This catalogue is maintained by the Agentic-Index project and is updated regularly (aiming for monthly refreshes) to reflect the rapidly evolving landscape of Agentic-AI.

-----

## TOC

* [✨ Why Agentic Index is Different](#-why-agentic-index-is-different)
* [⚡ Installation & Quick-start](#-installation--quick-start)
* [🏆 The Agentic-Index Top 100: AI Agent Repositories](#-the-agentic-index-top-100-ai-agent-repositories)
  * [💎 Honourable Mentions / Niche & Novel Gems](HONOURABLE.md)
    * [🔬 Our Methodology & Scoring Explained](#our-methodology--scoring-explained)
    * [🏷️ Category Definitions](#-category-definitions)
  * [📚 Explore by Category](#-explore-by-category)
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

New contributors should start with the [ONBOARDING guide](docs/ONBOARDING.md) for environment setup and troubleshooting.

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
*(Data updated as of: 2025-06-16T05:56:02 UTC)*

<!-- TOP50:START -->
| Rank | Repo | Description | Score | Stars | Δ Stars |
|-----:|------|-------------|------:|------:|--------:|
| 1 | [dify](https://github.com/langgenius/dify) | Production-ready platform for agentic workflow development. | 5.28 | 103268 |  |
| 2 | [langflow](https://github.com/langflow-ai/langflow) | Langflow is a powerful tool for building and deploying AI-powered agents and workflows. | 5.17 | 73776 |  |
| 3 | [browser-use](https://github.com/browser-use/browser-use) | 🌐 Make websites accessible for AI agents. Automate tasks online with ease. | 5.10 | 63197 |  |
| 4 | [OpenHands](https://github.com/All-Hands-AI/OpenHands) | 🙌 OpenHands: Code Less, Make More | 5.07 | 58086 |  |
| 5 | [lobe-chat](https://github.com/lobehub/lobe-chat) | 🤯 Lobe Chat - an open-source, modern-design AI chat framework. Supports Multi AI Providers( OpenAI / Claude 4 / Gemini / Ollama / DeepSeek / Qwen),... | 5.06 | 62457 |  |
| 6 | [MetaGPT](https://github.com/FoundationAgents/MetaGPT) | 🌟 The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming | 5.06 | 56406 |  |
| 7 | [ragflow](https://github.com/infiniflow/ragflow) | RAGFlow is an open-source RAG (Retrieval-Augmented Generation) engine based on deep document understanding. | 5.04 | 55104 |  |
| 8 | [system-prompts-and-models...](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) | FULL v0, Cursor, Manus, Same.dev, Lovable, Devin, Replit Agent, Windsurf Agent, VSCode Agent, Dia Browser & Trae AI (And other Open Sourced) System... | 5.03 | 57495 |  |
| 9 | [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | Unified Efficient Fine-Tuning of 100+ LLMs & VLMs (ACL 2024) | 5.02 | 52281 |  |
| 10 | [anything-llm](https://github.com/Mintplex-Labs/anything-llm) | The all-in-one Desktop & Docker AI application with built-in RAG, AI agents, No-code agent builder, MCP compatibility,  and more. | 4.96 | 45309 |  |
| 11 | [cline](https://github.com/cline/cline) | Autonomous coding agent right in your IDE, capable of creating/editing files, executing commands, using the browser, and more with your permission ... | 4.96 | 45704 |  |
| 12 | [autogen](https://github.com/microsoft/autogen) | A programming framework for agentic AI 🤖 PyPi: autogen-agentchat Discord: https://aka.ms/autogen-discord Office Hour: https://aka.ms/autogen-office... | 4.93 | 45993 |  |
| 13 | [llama_index](https://github.com/run-llama/llama_index) | LlamaIndex is the leading framework for building LLM-powered agents over your data. | 4.93 | 42355 |  |
| 14 | [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | Collection of awesome LLM apps with AI Agents and RAG using OpenAI, Anthropic, Gemini and opensource models. | 4.92 | 41125 |  |
| 15 | [Flowise](https://github.com/FlowiseAI/Flowise) | Build AI Agents, Visually | 4.87 | 40065 |  |
| 16 | [ChatTTS](https://github.com/2noise/ChatTTS) | A generative speech model for daily dialogue. | 4.84 | 36799 |  |
| 17 | [mem0](https://github.com/mem0ai/mem0) | Memory for AI Agents; Announcing OpenMemory MCP - local and secure memory management. | 4.84 | 34513 |  |
| 18 | [crewAI](https://github.com/crewAIInc/crewAI) | Framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together se... | 4.82 | 32933 |  |
| 19 | [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | Langchain-Chatchat（原Langchain-ChatGLM）基于 Langchain 与 ChatGLM, Qwen 与 Llama 等语言模型的 RAG 与 Agent 应用 / Langchain-Chatchat (formerly langchain-ChatGLM),... | 4.81 | 35287 |  |
| 20 | [AgentGPT](https://github.com/reworkd/AgentGPT) | 🤖 Assemble, configure, and deploy autonomous AI Agents in your browser. | 4.79 | 34323 |  |
| 21 | [agno](https://github.com/agno-agi/agno) | Full-stack framework for building Multi-Agent Systems with memory, knowledge and reasoning. | 4.76 | 28280 |  |
| 22 | [khoj](https://github.com/khoj-ai/khoj) | Your AI second brain. Self-hostable. Get answers from the web or your docs. Build custom agents, schedule automations, do deep research. Turn any o... | 4.75 | 30327 |  |
| 23 | [ChatDev](https://github.com/OpenBMB/ChatDev) | Create Customized Software using Natural Language Idea (through LLM-powered Multi-Agent Collaboration) | 4.74 | 27024 |  |
| 24 | [ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) | 11 Lessons to Get Started Building AI Agents | 4.73 | 26615 |  |
| 25 | [LibreChat](https://github.com/danny-avila/LibreChat) | Enhanced ChatGPT Clone: Features Agents, DeepSeek, Anthropic, AWS, OpenAI, Assistants API, Azure, Groq, o1, GPT-4o, Mistral, OpenRouter, Vertex AI,... | 4.73 | 26789 |  |
| 26 | [cherry-studio](https://github.com/CherryHQ/cherry-studio) | 🍒 Cherry Studio is a desktop client that supports for multiple LLM providers. | 4.72 | 28444 |  |
| 27 | [Jobs_Applier_AI_Agent_AIHawk](https://github.com/feder-cr/Jobs_Applier_AI_Agent_AIHawk) | AIHawk aims to easy job hunt process by automating the job application process. Utilizing artificial intelligence, it enables users to apply for mu... | 4.72 | 28310 |  |
| 28 | [qlib](https://github.com/microsoft/qlib) | Qlib is an AI-oriented Quant investment platform that aims to use AI tech to empower Quant Research, from exploring ideas to implementing productio... | 4.71 | 25192 |  |
| 29 | [composio](https://github.com/ComposioHQ/composio) | Composio equips your AI agents & LLMs with 100+ high-quality integrations via function calling | 4.68 | 25499 |  |
| 30 | [FastGPT](https://github.com/labring/FastGPT) | FastGPT is a knowledge-based platform built on the LLMs, offers a comprehensive suite of out-of-the-box capabilities such as data processing, RAG r... | 4.66 | 24718 |  |
| 31 | [gpt-researcher](https://github.com/assafelovic/gpt-researcher) | LLM based autonomous agent that conducts deep local and web research on any topic and generates a long report with citations. | 4.65 | 21875 |  |
| 32 | [CopilotKit](https://github.com/CopilotKit/CopilotKit) | React UI + elegant infrastructure for AI Copilots, AI chatbots, and in-app AI agents. The Agentic last-mile 🪁 | 4.63 | 21205 |  |
| 33 | [haystack](https://github.com/deepset-ai/haystack) | AI orchestration framework to build customizable, production-ready LLM applications. Connect components (models, vector DBs, file converters) to pi... | 4.63 | 21154 |  |
| 34 | [swarm](https://github.com/openai/swarm) | Educational framework exploring ergonomic, lightweight multi-agent orchestration. Managed by OpenAI Solution team. | 4.56 | 19920 |  |
| 35 | [agentic](https://github.com/transitive-bullshit/agentic) | AI agent stdlib that works with any LLM and TypeScript AI SDK. | 4.55 | 17639 |  |
| 36 | [vanna](https://github.com/vanna-ai/vanna) | 🤖 Chat with your SQL database 📊. Accurate Text-to-SQL Generation via LLMs using RAG 🔄. | 4.54 | 18127 |  |
| 37 | [agenticSeek](https://github.com/Fosowl/agenticSeek) | Fully Local Manus AI. No APIs, No $200 monthly bills. Enjoy an autonomous agent that thinks, browses the web, and code for the sole cost of electri... | 4.53 | 18268 |  |
| 38 | [DB-GPT](https://github.com/eosphoros-ai/DB-GPT) | AI Native Data App Development framework with AWEL(Agentic Workflow Expression Language) and Agents | 4.53 | 16764 |  |
| 39 | [deep-research](https://github.com/dzhng/deep-research) | An AI-powered research assistant that performs iterative, deep research on any topic by combining search engines, web scraping, and large language ... | 4.53 | 16638 |  |
| 40 | [letta](https://github.com/letta-ai/letta) | Letta (formerly MemGPT) is the stateful agents framework with memory, reasoning, and context management. | 4.53 | 16861 |  |
| 41 | [SWE-agent](https://github.com/SWE-agent/SWE-agent) | SWE-agent takes a GitHub issue and tries to automatically fix it, using your LM of choice. It can also be employed for offensive cybersecurity or c... | 4.52 | 16305 |  |
| 42 | [eliza](https://github.com/elizaOS/eliza) | Autonomous agents for everyone | 4.51 | 16078 |  |
| 43 | [RagaAI-Catalyst](https://github.com/raga-ai-hub/RagaAI-Catalyst) | Python SDK for Agent AI Observability, Monitoring and Evaluation Framework. Includes features like agent, llm and tools tracing, debugging multi-ag... | 4.51 | 16193 |  |
| 44 | [DocsGPT](https://github.com/arc53/DocsGPT) | DocsGPT is an open-source genAI tool that helps users get reliable answers from knowledge source, while avoiding hallucinations. It enables private... | 4.50 | 15708 |  |
| 45 | [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) | A list of AI autonomous agents | 4.48 | 18587 |  |
| 46 | [goose](https://github.com/block/goose) | an open source, extensible AI agent that goes beyond code suggestions - install, execute, edit, and test with any LLM | 4.47 | 14627 |  |
| 47 | [activepieces](https://github.com/activepieces/activepieces) | AI Agents & MCPs & AI Workflow Automation • (280+ MCP servers for AI agents) • AI Automation / AI Agent with MCPs • AI Workflows & AI Agents • MCPs... | 4.46 | 15291 |  |
| 48 | [suna](https://github.com/kortix-ai/suna) | Suna - Open Source Generalist AI Agent | 4.46 | 14425 |  |
| 49 | [ai](https://github.com/vercel/ai) | The AI Toolkit for TypeScript. From the creators of Next.js, the AI SDK is a free open-source library for building AI-powered applications and agents  | 4.45 | 14955 |  |
| 50 | [botpress](https://github.com/botpress/botpress) | The open-source hub to build & deploy GPT/LLM Agents ⚡️ | 4.45 | 13805 |  |
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
<details>
<summary>🔬 Our Methodology & Scoring Explained (Click to Expand)</summary>

Agentic-Index believes in full transparency. Here’s the lowdown on how we find, vet, and score repositories.

Our score balances stars, recency, maintenance health, documentation quality, license freedom, and ecosystem fit. **[See full formula →](./docs/methodology.md#scoring-formula)**

**Quick Look at Components:**

  * **Seed Discovery:** GitHub searches (e.g., `"agent framework"`, `"LLM agent"`), topic filters (e.g., `topic:agent` [17]), and crawling curated lists [24, 25, 7] to cast a wide net.
  * **Metadata Harvest:** Pulling key data: stars, forks, open/closed issues, commit dates, language, license, README snippets. (Examples: [13, 1, 12, 26, 23, 2, 10, 8, 3, 14, 15, 16, 19, 22, 27, 28] and many others as detailed in `docs/methodology.md`)
  * **Quality & Activity Scoring:** The formula balances community buzz, dev activity, maintenance, docs, license, and how well it plays with others.
  * **De-duplication & Categorisation:** Forks usually get skipped unless they’re their own thing now. Repos get bucketed by their main gig.

For the full, unabridged version, see **[./docs/methodology.md](./docs/methodology.md)**.

</details>

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

<a id="-explore-by-category"></a>
## 📚 Explore by Category
<!-- CATEGORY:START -->

<!-- CATEGORY:END -->
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

See [ONBOARDING.md](docs/ONBOARDING.md#running-tests) for instructions on running the test suite and replicating CI's offline environment.

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
  * Run `source scripts/setup-env.sh` to configure your environment.


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
