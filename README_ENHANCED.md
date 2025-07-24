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

---

## 🏆 Top AI Agent Repositories

<div align="center">

[![Repository Count](https://img.shields.io/badge/tracked%20repos-283+-blue?style=for-the-badge&logo=github)](https://adrianwedd.github.io/Agentic-Index)
[![Last Update](https://img.shields.io/badge/last%20update-daily-brightgreen?style=for-the-badge&logo=calendar)](https://github.com/adrianwedd/Agentic-Index/actions)
[![Average Score](https://img.shields.io/badge/avg%20score-3.76-orange?style=for-the-badge&logo=star)](https://adrianwedd.github.io/Agentic-Index)

**[🌟 View Interactive Rankings →](https://adrianwedd.github.io/Agentic-Index)**

</div>

### 🥇 **Current Top Performers**

| Rank | Repository | Stars | Score | Category | Language | Trend |
|------|------------|-------|-------|----------|----------|-------|
| 1 | [**dify**](https://github.com/langgenius/dify) | 103,268 ⭐ | 5.28 | General-purpose | TypeScript | 📈 |
| 2 | [**langflow**](https://github.com/logspace-ai/langflow) | 73,776 ⭐ | 5.17 | DevTools | Python | 📈 |
| 3 | [**browser-use**](https://github.com/gregpr07/browser-use) | 63,197 ⭐ | 5.10 | General-purpose | Python | 🚀 |
| 4 | [**OpenHands**](https://github.com/All-Hands-AI/OpenHands) | 58,086 ⭐ | 5.07 | General-purpose | Python | 📈 |
| 5 | [**lobe-chat**](https://github.com/lobehub/lobe-chat) | 62,457 ⭐ | 5.06 | RAG-centric | TypeScript | 📈 |

### 📈 **Trending Insights**

<div align="center">

```
🎯 Current Focus Areas:
████████████████████████████████████████ General-purpose (65%)
██████████ RAG-centric (11%)
██████████ Multi-Agent (11%) 
██████ DevTools (8%)
████ Experimental (6%)

💻 Language Distribution:
████████████████████████████████████████ Python (67%)
████████████ TypeScript (19%)
██ JavaScript (4%)
█ Others (10%)
```

</div>

---

## 🏷️ Explore by Category

<div align="center">

[![General Purpose](https://img.shields.io/badge/General%20Purpose-183%20repos-blue?style=for-the-badge&logo=robot)](https://adrianwedd.github.io/Agentic-Index?category=General-purpose)
[![RAG Centric](https://img.shields.io/badge/RAG%20Centric-30%20repos-green?style=for-the-badge&logo=database)](https://adrianwedd.github.io/Agentic-Index?category=RAG-centric)
[![Multi Agent](https://img.shields.io/badge/Multi%20Agent-30%20repos-purple?style=for-the-badge&logo=users)](https://adrianwedd.github.io/Agentic-Index?category=Multi-Agent)
[![DevTools](https://img.shields.io/badge/DevTools-23%20repos-orange?style=for-the-badge&logo=tools)](https://adrianwedd.github.io/Agentic-Index?category=DevTools)
[![Experimental](https://img.shields.io/badge/Experimental-17%20repos-red?style=for-the-badge&logo=flask)](https://adrianwedd.github.io/Agentic-Index?category=Experimental)

</div>

### 🎨 **Category Definitions**

<details>
<summary><b>🤖 General-purpose (183 repos)</b></summary>

Comprehensive frameworks for building diverse AI agent applications:
- **Scope**: Multi-modal agents, workflow orchestration, general automation
- **Examples**: CrewAI, AutoGPT, LangChain agents, Semantic Kernel
- **Best for**: Production applications, enterprise solutions, versatile agent systems

</details>

<details>
<summary><b>🗄️ RAG-centric (30 repos)</b></summary>

Specialized frameworks for Retrieval-Augmented Generation:
- **Scope**: Document processing, vector databases, knowledge systems
- **Examples**: LlamaIndex, Haystack, RAGFlow, Chroma
- **Best for**: Knowledge bases, document Q&A, research assistants

</details>

<details>
<summary><b>👥 Multi-Agent Coordination (30 repos)</b></summary>

Systems enabling multiple AI agents to collaborate:
- **Scope**: Agent communication, task delegation, swarm intelligence
- **Examples**: MetaGPT, AutoGen, CrewAI swarms, Agent coordination frameworks
- **Best for**: Complex workflows, team-based problem solving, distributed AI

</details>

<details>
<summary><b>🛠️ DevTools (23 repos)</b></summary>

Development tools and utilities for AI agent builders:
- **Scope**: Testing frameworks, debugging tools, prompt engineering, monitoring
- **Examples**: LangSmith, Agent evaluation tools, prompt optimizers
- **Best for**: Development workflows, testing, debugging, optimization

</details>

<details>
<summary><b>🧪 Experimental (17 repos)</b></summary>

Cutting-edge research and experimental implementations:
- **Scope**: Novel architectures, research prototypes, proof-of-concepts
- **Examples**: Academic research implementations, novel agent architectures
- **Best for**: Research, experimentation, exploring new paradigms

</details>

---

## 📊 Data & Analytics

### 🎨 **Beautiful Trend Visualizations**

<div align="center">

[![Trends Report](https://img.shields.io/badge/📊%20Trends%20Report-View%20Latest-blue?style=for-the-badge)](docs/trends/beautiful_trends_report.txt)
[![CSV Export](https://img.shields.io/badge/📈%20CSV%20Data-Download-green?style=for-the-badge)](docs/trends/repository_trends.csv)
[![Interactive Charts](https://img.shields.io/badge/📉%20Live%20Charts-Explore-orange?style=for-the-badge)](https://adrianwedd.github.io/Agentic-Index)

</div>

**Recent Analytics Insights:**
- 📈 **Average Growth**: 8,855 stars per repository
- 🏆 **Score Range**: 2.39 → 5.28 (healthy distribution)  
- 🌍 **Global Reach**: 531 days of tracking across 5 major snapshots
- 🔥 **Hot Category**: General-purpose frameworks dominating with 65% market share

### 🔌 **API & Integration**

<details>
<summary><b>🌐 REST API Usage</b></summary>

```bash
# Get all repositories
curl https://adrianwedd.github.io/Agentic-Index/data/repos.json

# Filter by category (programmatically)
curl -s https://adrianwedd.github.io/Agentic-Index/data/repos.json | \
  jq '.[] | select(.category == "RAG-centric")'

# Get top 10 by score
curl -s https://adrianwedd.github.io/Agentic-Index/data/repos.json | \
  jq '. | sort_by(.AgenticIndexScore) | reverse | .[0:10]'
```

</details>

<details>
<summary><b>🐍 Python Integration</b></summary>

```python
import requests
import pandas as pd

# Load data
response = requests.get('https://adrianwedd.github.io/Agentic-Index/data/repos.json')
repos = response.json()

# Convert to DataFrame for analysis
df = pd.DataFrame(repos)

# Top repositories by category
top_by_category = df.groupby('category').apply(
    lambda x: x.nlargest(5, 'AgenticIndexScore')
)
```

</details>

---

## 🛠️ Advanced Usage

### 📚 **Documentation & Guides**

<div align="center">

[![Full Documentation](https://img.shields.io/badge/📖%20Full%20Docs-MkDocs%20Site-blue?style=for-the-badge&logo=read-the-docs)](https://adrianwedd.github.io/Agentic-Index/docs)
[![API Reference](https://img.shields.io/badge/🔧%20API%20Reference-Technical%20Docs-green?style=for-the-badge&logo=swagger)](https://adrianwedd.github.io/Agentic-Index/docs/api)
[![Methodology](https://img.shields.io/badge/🔬%20Methodology-Scoring%20Formula-orange?style=for-the-badge&logo=calculator)](docs/methodology.md)

</div>

### 🔧 **CLI Commands Reference**

<details>
<summary><b>Core Pipeline Commands</b></summary>

```bash
# Complete pipeline
agentic-index faststart --top 100 data/repos.json

# Individual steps
agentic-index scrape --min-stars 50 --output data/repos.json
agentic-index enrich data/repos.json  
agentic-index rank data/repos.json
agentic-index inject --force  # Update README with latest rankings

# Custom configuration
agentic-index scrape --config my_config.yml --min-stars 100
```

</details>

<details>
<summary><b>Data Analysis Commands</b></summary>

```bash
# Generate trend reports
python scripts/plot_text_trends.py

# Validate data integrity  
python scripts/validate_fixtures.py
python scripts/validate_tasks.py

# Export formats
agentic-index export --format csv --output rankings.csv
agentic-index export --format json --output rankings.json
```

</details>

### 🧪 **Development & Testing**

<details>
<summary><b>Setup Development Environment</b></summary>

```bash
# Clone and setup
git clone https://github.com/adrianwedd/Agentic-Index.git
cd Agentic-Index

# Quick environment setup
source scripts/setup-env.sh

# Manual setup
pip install -e .
pre-commit install

# Run tests
pytest -q
CI_OFFLINE=1 pytest --disable-socket  # Offline tests
pytest --cov=agentic_index_cli --cov-report=term-missing  # With coverage
```

</details>

<details>
<summary><b>Quality Assurance</b></summary>

```bash
# Type checking
mypy agentic_index_cli/cli.py agentic_index_cli/enricher.py

# Code formatting
black agentic_index_cli/
isort agentic_index_cli/

# Security scanning
bandit -r agentic_index_cli/

# Accessibility testing (requires Chrome)
npx pa11y web/index.html
```

</details>

---

## 🗺️ Project Roadmap

<div align="center">

[![View Full Roadmap](https://img.shields.io/badge/🗺️%20Full%20Roadmap-View%20Detailed%20Plan-blue?style=for-the-badge&logo=map)](ROADMAP.md)

</div>

### 🎯 **Upcoming Milestones**

<table>
<tr>
<th>Phase</th>
<th>Timeline</th>
<th>Key Features</th>
<th>Impact</th>
</tr>
<tr>
<td><b>🚀 Phase 1</b><br>Foundation</td>
<td>2-3 weeks</td>
<td>• Fix Δ Stars pipeline<br>• Enhanced algorithms<br>• 40+ search queries</td>
<td>2-3x more repos<br>Better accuracy</td>
</tr>
<tr>
<td><b>⚡ Phase 2</b><br>Intelligence</td>
<td>3-4 weeks</td>
<td>• Real-time trending<br>• ML-enhanced scoring<br>• Community metrics</td>
<td>Predictive insights<br>Trend detection</td>
</tr>
<tr>
<td><b>🌟 Phase 3</b><br>Ecosystem</td>
<td>4-6 weeks</td>
<td>• Deep tech analysis<br>• Security scoring<br>• Market intelligence</td>
<td>Production-ready<br>Enterprise insights</td>
</tr>
<tr>
<td><b>✨ Phase 4</b><br>Experience</td>
<td>6-8 weeks</td>
<td>• Interactive dashboard<br>• Personalization<br>• Advanced UX</td>
<td>User-centric<br>Customized experience</td>
</tr>
</table>

---

## 🤝 Community & Contributing

### 💡 **Get Involved**

<div align="center">

[![Contribute](https://img.shields.io/badge/🤝%20Contribute-Welcome-brightgreen?style=for-the-badge&logo=heart)](CONTRIBUTING.md)
[![Discussions](https://img.shields.io/badge/💬%20Discussions-Join%20Community-blue?style=for-the-badge&logo=github)](https://github.com/adrianwedd/Agentic-Index/discussions)
[![Issues](https://img.shields.io/badge/🐛%20Issues-Report%20Bugs-red?style=for-the-badge&logo=github)](https://github.com/adrianwedd/Agentic-Index/issues)
[![Feature Requests](https://img.shields.io/badge/💡%20Ideas-Request%20Features-yellow?style=for-the-badge&logo=lightbulb)](https://github.com/adrianwedd/Agentic-Index/issues/new?template=feature_request.md)

</div>

### 🌟 **Ways to Contribute**

- **🔍 Repository Suggestions**: Know an amazing AI agent framework we missed?
- **📊 Algorithm Improvements**: Ideas for better scoring or categorization?  
- **🐛 Bug Reports**: Found issues with rankings or data accuracy?
- **📖 Documentation**: Help improve guides, examples, and explanations
- **💻 Code Contributions**: Enhancements to CLI tools, API, or web interface

### 👥 **Community Stats**

<div align="center">

[![Contributors](https://img.shields.io/github/contributors/adrianwedd/Agentic-Index?style=for-the-badge&logo=users)](https://github.com/adrianwedd/Agentic-Index/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/adrianwedd/Agentic-Index?style=for-the-badge&logo=git-alt)](https://github.com/adrianwedd/Agentic-Index/network/members)
[![Issues](https://img.shields.io/github/issues/adrianwedd/Agentic-Index?style=for-the-badge&logo=github)](https://github.com/adrianwedd/Agentic-Index/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/adrianwedd/Agentic-Index?style=for-the-badge&logo=github)](https://github.com/adrianwedd/Agentic-Index/pulls)

</div>

---

## 📜 License & Attribution

<div align="center">

[![Dual License](https://img.shields.io/badge/License-Dual%20MIT%2FCC--BY--SA-blue?style=for-the-badge&logo=balance-scale)](LICENSE)
[![FOSSA Status](https://img.shields.io/badge/FOSSA-Compliant-brightgreen?style=for-the-badge&logo=balance-scale)](https://app.fossa.com/projects/git%2Bgithub.com%2Fadrianwedd%2FAgentic-Index)

**Dual Licensed for Maximum Freedom**

• **Code**: MIT License (use, modify, distribute freely)  
• **Documentation**: Creative Commons Attribution-ShareAlike 4.0

</div>

---

<div align="center">

### 🚀 **Ready to Build the Future of AI Agents?**

**[🌟 Explore the Index](https://adrianwedd.github.io/Agentic-Index)** • **[📖 Read the Docs](https://adrianwedd.github.io/Agentic-Index/docs)** • **[🗺️ View Roadmap](ROADMAP.md)**

---

[![Made with ❤️](https://img.shields.io/badge/made%20with-❤️-red?style=for-the-badge)](https://github.com/adrianwedd/Agentic-Index)
[![Powered by AI](https://img.shields.io/badge/powered%20by-AI-blue?style=for-the-badge&logo=robot)](https://github.com/adrianwedd/Agentic-Index)
[![Built for Developers](https://img.shields.io/badge/built%20for-developers-green?style=for-the-badge&logo=code)](https://github.com/adrianwedd/Agentic-Index)

**Agentic-Index** • Building the definitive intelligence layer for autonomous AI agents

*Last updated: January 2025 • Next refresh: Daily via GitHub Actions*

</div>