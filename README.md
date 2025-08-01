# 🌐 Agentic-Index – The Data-Driven AI-Agent Repository Index

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/adrianwedd/Agentic-Index?style=for-the-badge&logo=github&color=gold)](https://github.com/adrianwedd/Agentic-Index/stargazers)
[![Build Status](https://img.shields.io/github/actions/workflow/status/adrianwedd/Agentic-Index/ci.yml?style=for-the-badge&logo=github-actions)](https://github.com/adrianwedd/Agentic-Index/actions)
[![Coverage](https://img.shields.io/codecov/c/github/adrianwedd/Agentic-Index?style=for-the-badge&logo=codecov&color=brightgreen)](https://codecov.io/gh/adrianwedd/Agentic-Index)
[![Site Status](https://img.shields.io/website?down_message=offline&up_message=online&url=https%3A%2F%2Fadrianwedd.github.io%2FAgentic-Index&style=for-the-badge&logo=github-pages)](https://adrianwedd.github.io/Agentic-Index)

[![PyPI Version](https://img.shields.io/pypi/v/agentic-index-cli?style=for-the-badge&logo=pypi&color=blue)](https://pypi.org/project/agentic-index-cli/)
[![Python Versions](https://img.shields.io/pypi/pyversions/agentic-index-cli?style=for-the-badge&logo=python)](https://pypi.org/project/agentic-index-cli/)
[![License](https://img.shields.io/github/license/adrianwedd/Agentic-Index?style=for-the-badge&logo=open-source-initiative&color=success)](https://github.com/adrianwedd/Agentic-Index/blob/main/LICENSE)
[![Security](https://img.shields.io/badge/security-0%20issues-brightgreen?style=for-the-badge&logo=security)](https://github.com/adrianwedd/Agentic-Index/security/advisories)

**🚀 Continuously scoring & curating the world's best open-source AI agent frameworks**

*Fast search • Transparent metrics • Zero BS*

[🌟 **Explore Live Index**](https://adrianwedd.github.io/Agentic-Index) • [📖 **Documentation**](https://adrianwedd.github.io/Agentic-Index/docs) • [🗺️ **Roadmap**](ROADMAP.md) • [⚡ **Quick Start**](#-quick-start)

</div>

---

## 🎯 What Makes Agentic-Index Special

<table>
<tr>
<td width="50%">

### 🔬 **Data-Driven Intelligence**
- **283+ repositories** tracked and scored
- **Transparent algorithm** with 6 key factors
- **Daily updates** via automated GitHub Actions
- **Historical trend analysis** with beautiful visualizations
- **Category-based insights** across 5 major domains

</td>
<td width="50%">

### 🚀 **Developer-First Experience**
- **Interactive web interface** with advanced filtering
- **CLI tools** for programmatic access
- **REST API** for integration
- **CSV exports** for custom analysis
- **Comprehensive documentation** and guides

</td>
</tr>
</table>

### 📊 **Our Transparent Scoring Formula**

We rank repositories using a sophisticated, open-source algorithm that considers:

<div align="center">

| Factor | Weight | Description | Update Frequency |
|--------|--------|-------------|------------------|
| ⭐ **Stars & Momentum** | 30% | GitHub stars + 7-day growth velocity | Daily |
| 🔧 **Maintenance Health** | 25% | Issue/PR resolution rates & activity patterns | Daily |
| 📅 **Development Recency** | 20% | Recent commits and release activity | Daily |
| 📚 **Documentation Quality** | 15% | README completeness, examples, API docs | Weekly |
| ⚖️ **License Freedom** | 7% | OSI compatibility & usage restrictions | Static |
| 🧠 **Ecosystem Integration** | 3% | Framework compatibility & keyword relevance | Monthly |

</div>

> **🎯 TL;DR:** This isn't just a list—it's your intelligent launchpad for building with AI agents.

---

## ⚡ Quick Start

<details>
<summary><b>🔧 1. Installation Options</b></summary>

### Python Package (Recommended)
```bash
pip install agentic-index-cli
```

### From Source
```bash
git clone https://github.com/adrianwedd/Agentic-Index.git
cd Agentic-Index
pip install -e .
```

### Docker
```bash
docker pull ghcr.io/adrianwedd/agentic-index:latest
```

</details>

<details>
<summary><b>⚙️ 2. Configuration</b></summary>

```bash
# Copy default configuration
cp agentic_index_cli/config.yaml my_config.yml

# Set up environment variables
cp .env.example .env
```

Edit `.env` to add your GitHub token for higher rate limits:
```bash
GITHUB_TOKEN_REPO_STATS=your_github_token_here
```

</details>

<details>
<summary><b>🚀 3. Run the Pipeline</b></summary>

```bash
# Full pipeline (scrape + score + rank + export)
agentic-index faststart --top 100

# Individual steps
agentic-index scrape --min-stars 100
agentic-index enrich data/repos.json
agentic-index rank data/repos.json
```

Results appear in `data/repos.json` and get injected into `README.md`.

</details>

<details>
<summary><b>📊 4. Generate Beautiful Trends</b></summary>

```bash
# Create trend visualizations
python scripts/plot_text_trends.py

# Output: docs/trends/beautiful_trends_report.txt
# Output: docs/trends/repository_trends.csv
```

</details>

<a id="-getting-started"></a>
## 🚀 Getting Started

1. **Install the CLI**
   ```bash
   pip install agentic-index-cli
   ```
2. **Configure tokens and settings**
   ```bash
   cp agentic_index_cli/config.yaml my_config.yml
   cp .env.example .env
   ```
   Edit `my_config.yml` and `.env` to tweak ranking parameters and add any tokens.
3. **Run the full pipeline**
   ```bash
   agentic-index scrape --min-stars 100
   agentic-index enrich data/repos.json
   agentic-index faststart --top 100 data/repos.json
   ```
   Results appear in `data/` and are injected into `README.md`.
4. **Browse the docs** – The full API reference lives in [`docs/`](docs/index.md).

-----

## TOC

* [✨ Why Agentic Index is Different](#-why-agentic-index-is-different)
* [⚡ Installation & Quick-start](#-installation--quick-start)
* [🚀 Getting Started](#-getting-started)
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
  * [📝 Forcing README injection](#-forcing-readme-injection)
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
agentic-index faststart --top 3 data/repos.json
cat FAST_START.md | less     # see table injected
```

-----


<a id="-the-agentic-index-top-100-ai-agent-repositories"></a>
## 🏆 The Agentic-Index Top 100: AI Agent Repositories

The definitive list of Agentic-AI repositories, ranked by the Agentic Index Score. This score is a holistic measure of project quality, activity, and community love.
*(Data updated as of: 2025-06-16T05:56:02 UTC)*

<!-- TOP100:START -->
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
| 51 | [dagger](https://github.com/dagger/dagger) | An open-source runtime for composable workflows. Great for AI agents and CI/CD. | 4.45 | 13931 |  |
| 52 | [plandex](https://github.com/plandex-ai/plandex) | Open source AI coding agent. Designed for large projects and real world tasks. | 4.45 | 13790 |  |
| 53 | [ai-pdf-chatbot-langchain](https://github.com/mayooear/ai-pdf-chatbot-langchain) | AI PDF chatbot agent built with LangChain & LangGraph  | 4.44 | 15574 |  |
| 54 | [deer-flow](https://github.com/bytedance/deer-flow) | DeerFlow is a community-driven Deep Research framework, combining language models with tools like web search, crawling, and Python execution, while... | 4.44 | 13528 |  |
| 55 | [SuperAGI](https://github.com/TransformerOptimus/SuperAGI) | <⚡️> SuperAGI - A dev-first open source autonomous AI agent framework. Enabling developers to build, manage & run useful autonomous agents quickly ... | 4.44 | 16414 |  |
| 56 | [web-ui](https://github.com/browser-use/web-ui) | 🖥️ Run AI Agent in your browser. | 4.44 | 13672 |  |
| 57 | [camel](https://github.com/camel-ai/camel) | 🐫 CAMEL: The first and the best multi-agent framework. Finding the Scaling Law of Agents. https://www.camel-ai.org | 4.42 | 12909 |  |
| 58 | [mastra](https://github.com/mastra-ai/mastra) | The TypeScript AI agent framework. ⚡ Assistants, RAG, observability. Supports any LLM: GPT-4, Claude, Gemini, Llama. | 4.42 | 14211 |  |
| 59 | [ChuanhuChatGPT](https://github.com/GaiZhenbiao/ChuanhuChatGPT) | GUI for ChatGPT API and many LLMs. Supports agents, file-based QA, GPT finetuning and query with web search. All with a neat UI. | 4.41 | 15414 |  |
| 60 | [devika](https://github.com/stitionai/devika) | Devika is an Agentic AI Software Engineer that can understand high-level human instructions, break them down into steps, research relevant informat... | 4.41 | 19329 |  |
| 61 | [GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) | This repository provides tutorials and implementations for various Generative AI Agent techniques, from basic to advanced. It serves as a comprehen... | 4.39 | 13225 |  |
| 62 | [Llama-Chinese](https://github.com/LlamaFamily/Llama-Chinese) | Llama中文社区，实时汇总最新Llama学习资料，构建最好的中文Llama大模型开源生态，完全开源可商用 | 4.37 | 14611 |  |
| 63 | [graphiti](https://github.com/getzep/graphiti) | Build Real-Time Knowledge Graphs for AI Agents | 4.36 | 11288 |  |
| 64 | [openai-agents-python](https://github.com/openai/openai-agents-python) | A lightweight, powerful framework for multi-agent workflows | 4.36 | 11447 |  |
| 65 | [LangBot](https://github.com/RockChinQ/LangBot) | 🤩 Easy-to-use global IM bot platform designed for the LLM era / 简单易用的大模型即时通信机器人平台 ⚡️ Bots for QQ / Discord / WeChat（企业微信、个人微信）/ Telegram / 飞书 / 钉钉 ... | 4.35 | 11933 |  |
| 66 | [pydantic-ai](https://github.com/pydantic/pydantic-ai) | Agent Framework / shim to use Pydantic with LLMs | 4.32 | 10239 |  |
| 67 | [adk-python](https://github.com/google/adk-python) | An open-source, code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents with flexibility and control. | 4.31 | 10116 |  |
| 68 | [ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub) | In-depth tutorials on LLMs, RAGs and real-world AI agent applications. | 4.30 | 9779 |  |
| 69 | [opik](https://github.com/comet-ml/opik) | Debug, evaluate, and monitor your LLM applications, RAG systems, and agentic workflows with comprehensive tracing, automated evaluations, and produ... | 4.29 | 9739 |  |
| 70 | [Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) | Agent framework and applications built upon Qwen>=3.0, featuring Function Calling, MCP, Code Interpreter, RAG, Chrome extension, etc. | 4.29 | 9528 |  |
| 71 | [agent-zero](https://github.com/frdel/agent-zero) | Agent Zero AI framework | 4.27 | 9872 |  |
| 72 | [AstrBot](https://github.com/AstrBotDevs/AstrBot) | ✨ 易上手的多平台 LLM 聊天机器人及开发框架 ✨ 平台支持 QQ、QQ频道、Telegram、微信、企微、飞书、钉钉 / 知识库、MCP 服务器、OpenAI、DeepSeek、Gemini、硅基流动、月之暗面、Ollama、OneAPI、Dify 等。 WebUI。 | 4.26 | 9720 |  |
| 73 | [bisheng](https://github.com/dataelement/bisheng) | BISHENG is an open LLM devops platform for next generation Enterprise AI applications. Powerful and comprehensive features include: GenAI workflow,... | 4.25 | 8843 |  |
| 74 | [awesome-LLM-resources](https://github.com/WangRongsheng/awesome-LLM-resources) | 🧑‍🚀 全世界最好的LLM资料总结（视频生成、Agent、辅助编程、数据处理、模型训练、模型推理、o1 模型、MCP、小语言模型、视觉语言模型） / Summary of the world's best LLM resources.  | 4.24 | 5444 |  |
| 75 | [cua](https://github.com/trycua/cua) | c/ua is the Docker Container for Computer-Use AI Agents. | 4.24 | 8591 |  |
| 76 | [E2B](https://github.com/e2b-dev/E2B) | Secure open source cloud runtime for AI apps & AI agents | 4.24 | 8628 |  |
| 77 | [Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) | MCP server to provide Figma layout information to AI coding agents like Cursor | 4.22 | 8150 |  |
| 78 | [Bert-VITS2](https://github.com/fishaudio/Bert-VITS2) | vits2 backbone with multilingual-bert | 4.20 | 8468 |  |
| 79 | [agentscope](https://github.com/modelscope/agentscope) | Start building LLM-empowered multi-agent applications in an easier way. | 4.18 | 7489 |  |
| 80 | [pr-agent](https://github.com/qodo-ai/pr-agent) | 🚀 PR-Agent (Qodo Merge open-source): An AI-Powered 🤖 Tool for Automated Pull Request Analysis, Feedback, Suggestions and More! 💻🔍 | 4.18 | 8127 |  |
| 81 | [UFO](https://github.com/microsoft/UFO) | The Desktop AgentOS. | 4.18 | 7384 |  |
| 82 | [Upsonic](https://github.com/Upsonic/Upsonic) | The most reliable AI agent framework that supports MCP. | 4.18 | 7523 |  |
| 83 | [WrenAI](https://github.com/Canner/WrenAI) | ⚡️Wren AI is your GenBI Agent, that you can query any database with natural language → get accurate SQL(Text-to-SQL), charts(Text-to-Charts) & AI-g... | 4.18 | 8045 |  |
| 84 | [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) | An Easy-to-use, Scalable and High-performance RLHF Framework based on Ray (PPO & GRPO & REINFORCE++ & vLLM & Ray & Dynamic Sampling & Async Agent RL) | 4.16 | 7076 |  |
| 85 | [promptfoo](https://github.com/promptfoo/promptfoo) | Test your prompts, agents, and RAGs. Red teaming, pentesting, and vulnerability scanning for LLMs. Compare performance of GPT, Claude, Gemini, Llam... | 4.16 | 7194 |  |
| 86 | [aichat](https://github.com/sigoden/aichat) | All-in-one LLM CLI tool featuring Shell Assistant, Chat-REPL, RAG, AI Tools & Agents, with access to OpenAI, Claude, Gemini, Ollama, Groq, and more. | 4.15 | 7022 |  |
| 87 | [R2R](https://github.com/SciPhi-AI/R2R) | SoTA production-ready AI retrieval system. Agentic Retrieval-Augmented Generation (RAG) with a RESTful API. | 4.15 | 6971 |  |
| 88 | [nanobrowser](https://github.com/nanobrowser/nanobrowser) | Open-Source Chrome extension for AI-powered web automation. Run multi-agent workflows using your own LLM API key. Alternative to OpenAI Operator. | 4.14 | 6803 |  |
| 89 | [agents](https://github.com/livekit/agents) | A powerful framework for building realtime voice AI agents 🤖🎙️📹  | 4.11 | 6321 |  |
| 90 | [intentkit](https://github.com/crestalnetwork/intentkit) | An open and fair framework for everyone to build AI agents equipped with powerful skills. Launch your agent, improve the world, your wallet, or both! | 4.11 | 6420 |  |
| 91 | [deep-searcher](https://github.com/zilliztech/deep-searcher) | Open Source Deep Research Alternative to Reason and Search on Private Data. Written in Python. | 4.10 | 6253 |  |
| 92 | [agent-squad](https://github.com/awslabs/agent-squad) | Flexible and powerful framework for managing multiple AI agents and handling complex conversations | 4.09 | 6031 |  |
| 93 | [lamda](https://github.com/firerpa/lamda) |  The most powerful Android RPA agent framework, next generation of mobile automation robots. | 4.08 | 7029 |  |
| 94 | [RD-Agent](https://github.com/microsoft/RD-Agent) | Research and development (R&D) is crucial for the enhancement of industrial productivity, especially in the AI era, where the core aspects of R&D a... | 4.08 | 5872 |  |
| 95 | [LLocalSearch](https://github.com/nilsherzig/LLocalSearch) | LLocalSearch is a completely locally running search aggregator using LLM Agents. The user can ask a question and the system will use a chain of LLM... | 4.07 | 5928 |  |
| 96 | [TaskWeaver](https://github.com/microsoft/TaskWeaver) | A code-first agent framework for seamlessly planning and executing data analytics tasks.  | 4.07 | 5764 |  |
| 97 | [mcp-agent](https://github.com/lastmile-ai/mcp-agent) | Build effective agents using Model Context Protocol and simple workflow patterns | 4.06 | 5720 |  |
| 98 | [ten-framework](https://github.com/TEN-framework/ten-framework) | Open-source framework for all AI agents. | 4.06 | 6157 |  |
| 99 | [cognee](https://github.com/topoteretes/cognee) | Memory for AI Agents in 5 lines of code | 4.05 | 5536 |  |
| 100 | [julep](https://github.com/julep-ai/julep) | Deploy serverless AI workflows at scale. Firebase for AI agents | 4.05 | 5548 |  |
<!-- TOP100:END -->
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
  * **Metadata Harvest:** Pulling key data: stars, forks, open/closed issues, commit dates, language, license, README snippets. (Examples: [13, 1, 12, 26, 23, 2, 10, 8, 3, 14, 15, 16, 19, 22, 27, 28]. More in [Data Sources & Scraping](./docs/methodology.md#data-sources--scraping))
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

Use the CLI to fetch fresh repo data:

```bash
agentic-index scrape --min-stars 50 --iterations 1 --output data
agentic-index enrich data/repos.json
agentic-index faststart --top 5 data/repos.json
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

### Running Tests

Run tests with:

```bash
pytest -q
```

`pytest` will fail if optional development packages are missing.
Run `source scripts/setup-env.sh` or install `dev-requirements.lock`
to ensure all dependencies are available.

CI runs tests with network access disabled. Set `CI_OFFLINE=1` or run
`pytest --disable-socket` locally to replicate the offline environment.
An autouse fixture still permits UNIX-domain `socketpair()` calls so FastAPI's
`TestClient` can start its event loop.

### Troubleshooting

If collection fails with messages like `ImportError: No module named 'responses'`,
make sure all test dependencies are installed:

```bash
pip install -r requirements.lock
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

### Optional Environment Variables

- `GITHUB_TOKEN_REPO_STATS` – increases GitHub API rate limits when scraping.
- `API_KEY` – used by some metrics scripts for third-party services.
- `CI_OFFLINE` – set to `1` to disable network calls during tests, matching CI.

## 💻 Developer

To trigger a data refresh via GitHub Actions, run:

```bash
bash scripts/trigger_refresh.sh 75
```

Replace `75` with your desired minimum star count. The script requires the GitHub CLI and an authenticated token.
Set a personal access token via the `GITHUB_TOKEN_REPO_STATS` environment variable to avoid hitting rate limits when scraping.

If a pipeline step fails and leaves corrupted data, see [ROLLBACK.md](docs/ROLLBACK.md) for how to revert the GitHub state and clear local caches before re-running.

### 📝 Forcing README injection

The injector normally skips writing `README.md` when no changes are detected. Use `--force` to rewrite the table regardless:

```bash
python scripts/inject_readme.py --force
```

This can be handy after metric tweaks that don't change rankings but should refresh the snapshot.

### 🔍 Preview changes with `--dry-run`

Use `--dry-run` to print a unified diff without modifying `README.md`:

```bash
python scripts/inject_readme.py --dry-run
```

This lets you verify upcoming updates locally or in CI.

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

The content of Agentic-Index (this `README.md`, files in `/docs/`, etc.) is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

Any scripts or code for analysis and generation (e.g., in `/scripts`, if we add 'em) are licensed under the [MIT License](https://opensource.org/licenses/MIT).

© 2025 Agentic-Index Maintainers


![Last Sync](badges/last_sync.svg) ![Top Repo](badges/top_repo.svg) ![Repo Count](badges/repo_count.svg)
