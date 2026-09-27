PDF: https://github.com/vectorize-io/hindsight
# vectorize-io/hindsight
Source: https://github.com/vectorize-io/hindsight
Kind: repo
Fetched: 2026-09-26T13:46:15.537675+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# vectorize-io/hindsight

Commit: a921929a0e0ea82fb49da1daa0ca3e152e41fcc1

## README

<div align="center">

![Hindsight Banner](./hindsight-docs/static/img/hindsight-github-banner.png)

[Documentation](https://hindsight.vectorize.io) • [Integrations](https://hindsight.vectorize.io/integrations) • [Cookbook](https://hindsight.vectorize.io/cookbook) • [Benchmarks](https://benchmarks.hindsight.vectorize.io/) • [Paper](https://arxiv.org/abs/2512.12818) • [Hindsight Cloud](https://ui.hindsight.vectorize.io/signup)

[![Release](https://github.com/vectorize-io/hindsight/actions/workflows/release.yml/badge.svg)](https://github.com/vectorize-io/hindsight/actions/workflows/release.yml)
[![Version](https://img.shields.io/pypi/v/hindsight-api?logo=python&logoColor=white&label=version&color=blue)](https://pypi.org/project/hindsight-api/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/hindsight-client?logo=pypi&logoColor=white&label=PyPI&color=blue)](https://pypi.org/project/hindsight-client/)
[![NPM Downloads](https://img.shields.io/npm/dm/%40vectorize-io%2Fhindsight-client?logo=npm&logoColor=white&label=NPM&color=blue)](https://www.npmjs.com/package/@vectorize-io/hindsight-client)
[![Slack Community](https://img.shields.io/badge/Slack-Join%20Community-4A154B?logo=slack)](https://vectorize.io/slack)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<br/>
<p align="center">
 <a href="https://www.star-history.com/vectorize-io/hindsight"><img src="https://api.star-history.com/badge?repo=vectorize-io/hindsight&type=rank" alt="Star History Rank" /> <img src="https://api.star-history.com/badge?repo=vectorize-io/hindsight&type=trending" alt="GitHub Trending Repository of the Day" /></a>
</p>

</div>

---



## What is Hindsight?

Hindsight™ is an agent memory system built to create smarter agents that learn over time. Most agent memory systems focus on recalling conversation history. Hindsight is focused on making agents that learn, not just remember.

<video src="https://github.com/user-attachments/assets/923b798d-3581-4897-bb62-9cfa5a931682" controls></video>

It eliminates the shortcomings of alternative techniques such as RAG and knowledge graph and delivers state-of-the-art performance on long term memory tasks.

**Contents**

- [Memory Performance & Accuracy](#memory-performance--accuracy)
- [Quick Start](#quick-start) — [server](#1-start-a-server) · [clients](#2-connect-a-client) · [platforms](#supported-platforms) · [embedded](#python-embedded-no-server-required)
- [Adding Hindsight to Your Agent](#adding-hindsight-to-your-agent) — [LLM Wrapper](#llm-wrapper-2-lines-of-code) · [integrations](#integrations) · [coding agents](#coding-agents) · [MCP](#mcp-server)
- [Core Concepts](#core-concepts) — [memory types](#memory-types) · [retain / recall / reflect](#the-three-operations) · [observations](#observations) · [mental models & knowledge pages](#mental-models--knowledge-pages) · [banks](#memory-banks)
- [Use Cases](#use-cases)
- [Running in Production](#running-in-production)
- [Resources](#resources)

---



## Memory Performance & Accuracy

Hindsight is the most accurate agent memory system ever tested according to benchmark performance. It has achieved state-of-the-art performance on the LongMemEval benchmark, widely used to assess memory system performance across a variety of conversational AI scenarios. The current reported performance of Hindsight and other agent memory solutions as of January 2026 is shown here:

![Overview](./hindsight-docs/static/img/hindsight-benchmarks.png)

> Live, continuously updated results — including per-model accuracy, latency and cost — are published at [benchmarks.hindsight.vectorize.io](https://benchmarks.hindsight.vectorize.io/).

The benchmark performance data for Hindsight has been independently reproduced by research collaborators at the Virginia Tech [Sanghani Center for Artificial Intelligence and Data Analytics](https://sanghani.cs.vt.edu/) and The Washington Post. Other scores are self-reported by software vendors.

Hindsight is being used in production at Fortune 500 enterprises and by a growing number of AI startups.

---

> 🤖 **Using a coding agent?** Install the Hindsight documentation skill for instant access to docs while you code:
> ```bash
> npx skills add https://github.com/vectorize-io/hindsight --skill hindsight-docs
> ```
> Works with Claude Code, Cursor, and other AI coding assistants.

---



### 1. Start a server

#### Docker (recommended)

```bash
export OPENAI_API_KEY=sk-xxx

docker run -it --pull always --name hindsight --restart unless-stopped -p 8888:8888 -p 9999:9999 \
  -e HINDSIGHT_API_LLM_API_KEY=$OPENAI_API_KEY \
  -v hindsight-data:/home/hindsight/.pg0 \
  ghcr.io/vectorize-io/hindsight:latest
```

>API: http://localhost:8888
>UI: http://localhost:9999

Hindsight works with **25+ LLM providers** via `HINDSIGHT_API_LLM_PROVIDER` — hosted (`openai`, `anthropic`, `gemini`, `groq`, `bedrock`, `vertexai`, `minimax`, `deepseek`, `atlas`, `meta`, …), fully local (`ollama`, `lmstudio`, `llamacpp`), any OpenAI-compatible endpoint, and gateways (`litellm`, `litellmrouter`) that reach the rest. Existing subscriptions work too: `openai-codex` (ChatGPT Plus/Pro), `claude-code` (Claude Pro/Max), `cursor` (Cursor) and `github-copilot` (GitHub Copilot) need no API key. See [supported models](https://hindsight.vectorize.io/developer/models).

#### Docker (external PostgreSQL)

```bash
export OPENAI_API_KEY=sk-xxx
export HINDSIGHT_DB_PASSWORD=choose-a-password
cd docker/docker-compose
docker compose up
```

> Oracle AI Database is also supported for enterprise deployments with full feature parity. See the [storage documentation](https://hindsight.vectorize.io/developer/storage) for details.

#### Bare metal (pip)

```bash
pip install hindsight-api
export HINDSIGHT_API_LLM_API_KEY=sk-xxx

hindsight-api
```

#### Kubernetes (Helm)

```bash
helm install hindsight oci://ghcr.io/vectorize-io/charts/hindsight \
  --set api.llm.provider=openai \
  --set api.llm.apiKey=sk-xxx \
  --set postgresql.enabled=true
```

#### Managed (no server)

[Hindsight Cloud](https://vectorize.io/pricing) is the hosted option: managed infrastructure that scales automatically, plus a dashboard, backups, team collaboration and a 99.9% uptime SLA. Billing is usage-based with free credits to start — no fixed monthly or per-seat fee. Point any client at `https://api.hindsight.vectorize.io` with your API key and skip the deployment entirely.

[Compare self-hosted, Cloud and Enterprise →](https://vectorize.io/pricing) · [Sign up →](https://ui.hindsight.vectorize.io/signup)

All options, including Windows and air-gapped setups, are covered in the [installation guide](https://hindsight.vectorize.io/developer/installation).



### 2. Connect a client

```bash
pip install hindsight-client -U                                  # Python
npm install @vectorize-io/hindsight-client                        # Node.js / TypeScript
go get github.com/vectorize-io/hindsight/hindsight-clients/go     # Go
curl -fsSL https://hindsight.vectorize.io/get-cli | bash          # CLI
```

#### Python

```python
from hindsight_client import Hindsight

client = Hindsight(base_url="http://localhost:8888")



# Retain: Store information
client.retain(bank_id="my-bank", content="Alice works at Google as a software engineer")



# Recall: Search memories
client.recall(bank_id="my-bank", query="What does Alice do?")



# Reflect: Generate disposition-aware response
client.reflect(bank_id="my-bank", query="Tell me about Alice")
```

#### Node.js / TypeScript

```javascript
const { HindsightClient } = require('@vectorize-io/hindsight-client');

const main = async () => {
  const client = new HindsightClient({ baseUrl: 'http://localhost:8888' });

  await client.retain('my-bank', 'Alice loves hiking in Yosemite');

  const results = await client.recall('my-bank', 'What does Alice like?');
  console.log(results);
}

main();
```

Full reference: [Python](https://hindsight.vectorize.io/sdks/python) · [Node.js](https://hindsight.vectorize.io/sdks/nodejs) · [Go](https://hindsight.vectorize.io/sdks/go) · [CLI](https://hindsight.vectorize.io/sdks/cli) · [REST API](https://hindsight.vectorize.io/api-reference)



### Supported Platforms

| Platform | Docker | Bare Metal (pip) | Embedded DB (pg0) |
|----------|--------|------------------|--------------------|
| **Linux** (x86_64, ARM64) | ✅ | ✅ | ✅ |
| **macOS** (Apple Silicon / arm64) | ✅ | ✅ | ✅ |
| **macOS** (Intel / x86_64) | ✅ | ⚠️ | ✅ |
| **Windows** (x86_64) | ✅ | ✅ | ✅ |

⚠️ Intel Macs: use `hindsight-all-slim` — see the [installation guide](https://hindsight.vectorize.io/developer/installation#supported-platforms) for details.



### Python Embedded (no server required)

```bash
pip install hindsight-all -U
```

On Intel (x86_64) Macs, install `hindsight-all-slim` instead — see [Supported Platforms](#supported-platforms).

```python
import os
from hindsight import HindsightServer, HindsightClient

with HindsightServer(
    llm_provider="openai",
    llm_model="gpt-5-mini",
    llm_api_key=os.environ["OPENAI_API_KEY"]
) as server:
    client = HindsightClient(base_url=server.url)
    client.retain(bank_id="my-bank", content="Alice works at Google")
    results = client.recall(bank_id="my-bank", query="Where does Alice work?")
```

A [Node.js equivalent](https://hindsight.vectorize.io/sdks/hindsight-all-npm) and a [daemon CLI](https://hindsight.vectorize.io/sdks/embed) are also available.

---



### LLM Wrapper (2 lines of code)

The easiest way to add memory to an existing agent is the LLM Wrapper. Swap your LLM client for a wrapped one — memories are then stored and retrieved automatically on every call, with no other changes to your code.

```bash
pip install hindsight-litellm
```

```python
from openai import OpenAI
from hindsight_litellm import wrap_openai



# Defaults to Hindsight Cloud; pass hindsight_api_url for a self-hosted server.
client = wrap_openai(
    OpenAI(),
    bank_id="user-123",
    hindsight_api_url="http://localhost:8888",
)



# and retains the conversation after it.
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": "What do you know about me?"}],
)
```

`wrap_anthropic()` does the same for the Anthropic SDK, and every setting — bank, recall budget, fact types, reflect instead of recall — can be overridden per call with `hindsight_*` kwargs. LiteLLM sits underneath, so the same integration covers **100+ models**. See the [LiteLLM integration](https://hindsight.vectorize.io/sdks/integrations/litellm).

If you need explicit control over *when* memories are stored and recalled, use the [SDKs or REST API](#2-connect-a-client) directly instead.



### Integrations

**60+ integrations** — most need no code changes.

| | |
|---|---|
| **Coding agents** | [Claude Code](https://hindsight.vectorize.io/sdks/integrations/claude-code) · [Codex](https://hindsight.vectorize.io/sdks/integrations/codex) · [Cursor](https://hindsight.vectorize.io/sdks/integrations/cursor) · [GitHub Copilot](https://hindsight.vectorize.io/sdks/integrations/github-copilot) · [opencode](https://hindsight.vectorize.io/sdks/integrations/opencode) · [Cline](https://hindsight.vectorize.io/sdks/integrations/cline) · [Aider](https://hindsight.vectorize.io/sdks/integrations/aider) · [Zed](https://hindsight.vectorize.io/sdks/integrations/zed) · [Continue](https://hindsight.vectorize.io/sdks/integrations/continue) · [Roo Code](https://hindsight.vectorize.io/sdks/integrations/roo-code) · [OpenHands](https://hindsight.vectorize.io/sdks/integrations/openhands) |
| **Agent frameworks** | [LangGraph / LangChain](https://hindsight.vectorize.io/sdks/integrations/langgraph) · [LlamaIndex](https://hindsight.vectorize.io/sdks/integrations/llamaindex) · [CrewAI](https://hindsight.vectorize.io/sdks/integrations/crewai) · [Pyd

... (truncated, 12819 more characters)

## pyproject.toml

```
[tool.uv.workspace]
members = ["hindsight-all", "hindsight-api", "hindsight-api-slim", "hindsight-all-slim", "hindsight-dev", "hindsight-mcp-server", "hindsight-clients/python", "hindsight-embed"]

[tool.uv]
# Allow uv to search all configured indexes for packages, not just the first one
# This prevents dependency resolution failures when using pytorch index + PyPI
index-strategy = "unsafe-best-match"
dev-dependencies = []

```

## package.json

```
{
  "name": "hindsight",
  "private": true,
  "workspaces": [
    "hindsight-clients/typescript",
    "hindsight-control-plane",
    "hindsight-docs",
    "hindsight-interfig",
    "hindsight-all-npm",
    "hindsight-tools/hindsight-agent-sdk"
  ],
  "scripts": {
    "prepare": "./scripts/setup-hooks.sh"
  },
  "overrides": {
    "qs": ">=6.16.0 <7.0.0",
    "fast-xml-parser": ">=5.5.6",
    "serialize-javascript": "^7.0.5",
    "minimatch": "^3.1.4",
    "undici": ">=7.29.0 <8.0.0",
    "flatted": ">=3.4.2",
    "picomatch": ">=2.3.2 <3.0.0 || >=4.0.4",
    "yaml": ">=1.10.3",
    "svgo": ">=4.1.0",
    "dompurify": ">=3.4.13",
    "@redocly/openapi-core": {
      "minimatch": "^5.1.8"
    },
    "@typescript-eslint/typescript-estree": {
      "minimatch": "^9.0.7"
    },
    "ajv-formats": {
      "ajv": "^8.18.0"
    },
    "handlebars": ">=4.7.9",
    "path-to-regexp": ">=0.1.13",
    "brace-expansion": ">=1.1.18 <2.0.0 || >=2.1.4 <3.0.0",
    "lodash-es": ">=4.18.1",
    "mermaid": ">=11.16.1",
    "websocket-driver": ">=0.7.5",
    "http-proxy-middleware": ">=2.0.10 <3",
    "next": ">=16.3.3 <17",
    "fast-uri": ">=3.1.6 <4",
    "sharp": ">=0.35.4",
    "shell-quote": ">=1.9.0",
    "@istanbuljs/load-nyc-config": {
      "js-yaml": "^3.15.2"
    },
    "gray-matter": {
      "js-yaml": "^3.15.2"
    },
    "sockjs": {
      "uuid": "^11.1.1"
    },
    "postcss": ">=8.5.23",
    "js-yaml": ">=3.15.2 <4.0.0 || >=4.3.2 <5.0.0",
    "nanoid": ">=3.3.18 <4.0.0",
    "webpack-dev-server": ">=5.2.6 <6.0.0",
    "esbuild": ">=0.28.1 <0.29.0",
    "body-parser": ">=1.20.6 <2.0.0",
    "browserslist": ">=4.28.7 <5.0.0",
    "postcss-selector-parser": ">=7.1.3 <8.0.0",
    "postcss-calc": {
      "postcss-selector-parser": "^6.1.3"
    },
    "postcss-discard-unused": {
      "postcss-selector-parser": "^6.1.3"
    },
    "postcss-merge-rules": {
      "postcss-selector-parser": "^6.1.3"
    },
    "postcss-minify-selectors": {
      "postcss-selector-parser": "^6.1.3"
    },
    "postcss-unique-selectors": {
      "postcss-selector-parser": "^6.1.3"
    },
    "stylehacks": {
      "postcss-selector-parser": "^6.1.3"
    },
    "@tailwindcss/typography": {
      "postcss-selector-parser": "6.0.10"
    },
    "colord": ">=2.9.4 <3.0.0",
    "joi": ">=17.13.6 <18.0.0"
  }
}

```

## Top-level layout

- .claude/ (dir, 4 files, ~978 lines)
- .claude-plugin/ (dir, 1 files, ~21 lines)
- .dockerignore (~33 lines)
- .env.example (~725 lines)
- .githooks/ (dir, 1 files, ~27 lines)
- .github/ (dir, 12 files, ~7730 lines)
- .gitignore (~78 lines)
- .prettierrc.json (~7 lines)
- .python-version (~1 lines)
- AGENTS.md (~3 lines)
- CLAUDE.md (~518 lines)
- CODE_OF_CONDUCT.md (~127 lines)
- CONTRIBUTING.md (~157 lines)
- cookbook/ (dir, 1 files, ~11 lines)
- deno.lock (~170 lines)
- docker/ (dir, 36 files, ~3592 lines)
- helm/ (dir, 25 files, ~1947 lines)
- hindsight-all/ (dir, 15 files, ~2789 lines)
- hindsight-all-npm/ (dir, 13 files, ~709 lines)
- hindsight-all-slim/ (dir, 2 files, ~82 lines)
- hindsight-api/ (dir, 2 files, ~163 lines)
- hindsight-api-slim/ (dir, 950 files, ~370631 lines)
- hindsight-cli/ (dir, 42 files, ~17812 lines)
- hindsight-clients/ (dir, 553 files, ~179361 lines)
- hindsight-control-plane/ (dir, 263 files, ~70846 lines)
- hindsight-dev/ (dir, 74 files, ~19033 lines)
- hindsight-docs/ (dir, 1217 files, ~184071 lines)
- hindsight-embed/ (dir, 63 files, ~14910 lines)
- hindsight-extensions/ (dir, 16 files, ~2713 lines)
- hindsight-favicon.png (~0 lines)
- hindsight-integration-tests/ (dir, 7 files, ~1774 lines)
- hindsight-integrations/ (dir, 1188 files, ~260803 lines)
- hindsight-interfig/ (dir, 35 files, ~5428 lines)
- hindsight-system-evals/ (dir, 40 files, ~8148 lines)
- hindsight-system-tests/ (dir, 78 files, ~10810 lines)
- hindsight-tools/ (dir, 5 files, ~2018 lines)
- LICENSE (~21 lines)
- monitoring/ (dir, 3 files, ~2436 lines)
- package-lock.json (~35137 lines)
- package.json (~87 lines)
- pyproject.toml (~8 lines)
- README.md (~442 lines)
- ruff.toml (~33 lines)
- scripts/ (dir, 48 files, ~5286 lines)
- SECURITY.md (~39 lines)
- skills/ (dir, 162 files, ~56181 lines)
- uv.lock (~5709 lines)

