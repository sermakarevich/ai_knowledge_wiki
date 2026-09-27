> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Hindsight is an agent memory system that makes agents learn over time rather than just recall conversation history (README.md:32).
## Key points
- Hindsight is an agent memory system focused on learning, explicitly positioned against recall-only history, RAG, and knowledge-graph techniques (README.md:32, README.md:36).
- It claims state-of-the-art accuracy on the LongMemEval long-term memory benchmark, with live per-model accuracy, latency, and cost published externally (README.md:54, README.md:58).
- Benchmark data was independently reproduced by Virginia Tech's Sanghani Center and The Washington Post, while other vendors' scores are self-reported (README.md:60).
- The system is deployed as a server (Docker, external PostgreSQL, pip bare metal, Helm/Kubernetes, or hosted Cloud) exposing API on port 8888 and UI on port 9999 (README.md:76, README.md:89, README.md:94, README.md:105, README.md:114, README.md:125).
- Clients connect via Python (`hindsight-client`), Node.js (`@vectorize-io/hindsight-client`), Go, CLI, REST API, or no-server embedded modes, using the three operations retain / recall / reflect against a `bank_id` (README.md:135, README.md:145, README.md:168, README.md:182).
- The LLM Wrapper (`wrap_openai`, `wrap_anthropic` via `hindsight-litellm`) auto-stores and retrieves memories on every LLM call with per-call `hindsight_*` overrides and 100+ model coverage through LiteLLM (README.md:229, README.md:257).
- It ships 60+ no-code-change integrations spanning coding agents and agent frameworks, plus a docs skill installed via `npx skills add` (README.md:66, README.md:265).
---
## What is Hindsight?
Hindsight™ is an agent memory system built to create smarter agents that learn over time (README.md:32):
> "Most agent memory systems focus on recalling conversation history. Hindsight is focused on making agents that learn, not just remember." (README.md:32)
> "It eliminates the shortcomings of alternative techniques such as RAG and knowledge graph and delivers state-of-the-art performance on long term memory tasks." (README.md:36)
Contents map in chunk (README.md:40): Memory Performance & Accuracy, Quick Start (server, clients, platforms, embedded), Adding Hindsight to Your Agent (LLM Wrapper, integrations, coding agents, MCP), Core Concepts (memory types, retain / recall / reflect, observations, mental models & knowledge pages, banks), Use Cases, Running in Production, Resources.
## Performance and accuracy
Claims SOTA on LongMemEval as of January 2026 (README.md:54):
> "Hindsight is the most accurate agent memory system ever tested according to benchmark performance." (README.md:54)
Live results at `benchmarks.hindsight.vectorize.io`, including per-model accuracy, latency and cost (README.md:58). Reproduction note (README.md:60):
> "The benchmark performance data for Hindsight has been independently reproduced by research collaborators at the Virginia Tech [Sanghani Center for Artificial Intelligence and Data Analytics](https://sanghani.cs.vt.edu/) and The Washington Post." (README.md:60)
Usage claim: in production at Fortune 500 enterprises and AI startups (README.md:62).
## Server deployment
Verbatim Docker start (README.md:80):
```bash
export OPENAI_API_KEY=sk-xxx

docker run -it --pull always --name hindsight --restart unless-stopped -p 8888:8888 -p 9999:9999 \
  -e HINDSIGHT_API_LLM_API_KEY=$OPENAI_API_KEY \
  -v hindsight-data:/home/hindsight/.pg0 \
  ghcr.io/vectorize-io/hindsight:latest
```
Endpoints (README.md:89): API `http://localhost:8888`, UI `http://localhost:9999`. LLM provider selection via `HINDSIGHT_API_LLM_PROVIDER` covering 25+ providers: hosted (`openai`, `anthropic`, `gemini`, `groq`, `bedrock`, `vertexai`, `minimax`, `deepseek`, `atlas`, `meta`, …), local (`ollama`, `lmstudio`, `llamacpp`), any OpenAI-compatible endpoint, gateways (`litellm`, `litellmrouter`); subscription-backed `openai-codex`, `claude-code`, `cursor`, `github-copilot` need no API key (README.md:92).
| Deployment | Command / source |
|---|---|
| Docker external PostgreSQL | `export HINDSIGHT_DB_PASSWORD=choose-a-password; cd docker/docker-compose; docker compose up` (README.md:96) |
| Bare metal (pip) | `pip install hindsight-api`, `export HINDSIGHT_API_LLM_API_KEY=sk-xxx`, `hindsight-api` (README.md:105) |
| Kubernetes (Helm) | `helm install hindsight oci://ghcr.io/vectorize-io/charts/hindsight --set api.llm.provider=openai --set api.llm.apiKey=sk-xxx --set postgresql.enabled=true` (README.md:114) |
| Managed Cloud | Point any client at `https://api.hindsight.vectorize.io` with API key; usage-based billing, dashboard, backups, collaboration, 99.9% SLA (README.md:125) |
Oracle AI Database supported with full feature parity for enterprise (README.md:103).
## Client connection
Install (README.md:135):
```bash
pip install hindsight-client -U                                  # Python
npm install @vectorize-io/hindsight-client                        # Node.js / TypeScript
go get github.com/vectorize-io/hindsight/hindsight-clients/go     # Go
curl -fsSL https://hindsight.vectorize.io/get-cli | bash          # CLI
```
Python verbatim (README.md:142):
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
Three operations are `retain` (store), `recall` (search), `reflect` (disposition-aware response) (README.md:152). Node.js verbatim (README.md:165):
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
Full reference links: Python, Node.js, Go, CLI, REST API (README.md:182).
## Supported platforms
Exact table (README.md:188):
| Platform | Docker | Bare Metal (pip) | Embedded DB (pg0) |
|----------|--------|------------------|--------------------|
| **Linux** (x86_64, ARM64) | ✅ | ✅ | ✅ |
| **macOS** (Apple Silicon / arm64) | ✅ | ✅ | ✅ |
| **macOS** (Intel / x86_64) | ✅ | ⚠️ | ✅ |
| **Windows** (x86_64) | ✅ | ✅ | ✅ |
Intel Mac caveat: use `hindsight-all-slim` (README.md:195, README.md:205).
## Python embedded (no server)
Install (README.md:199): `pip install hindsight-all -U`. Verbatim (README.md:207):
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
Exact parameter names: `llm_provider`, `llm_model`, `llm_api_key`, `base_url`/`server.url`, `bank_id`, `content`, `query` (README.md:207). Node.js equivalent and daemon CLI also exist (README.md:221).
## LLM wrapper and integrations
Easiest path is the LLM Wrapper: swap LLM client for wrapped one, memories stored/retrieved automatically (README.md:229). Install (README.md:231): `pip install hindsight-litellm`. Verbatim (README.md:235):
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
Exact names: `wrap_openai`, `wrap_anthropic`, `bank_id`, `hindsight_api_url`, per-call `hindsight_*` kwargs (bank, recall budget, fact types, reflect instead of recall); LiteLLM underneath covers 100+ models (README.md:257). Explicit control requires SDKs/REST API directly (README.md:259). Integrations claim: 60+ integrations, most need no code changes (README.md:265); coding-agent rows seen: Claude Code, Codex, Cursor, GitHub Copilot, opencode, Cline, Aider, Zed, Continue, Roo Code, OpenHands (README.md:269). Docs skill (README.md:66):
```bash
npx skills add https://github.com/vectorize-io/hindsight --skill hindsight-docs
```
Truncation note: the chunk cuts off mid-table at `Pyd` (agent-frameworks row, README.md:270), so remaining integrations, Core Concepts, Use Cases, Production, and Resources sections were not in the source and are not covered here.
**Covers:** README (project definition, benchmarks, server/client/embedded/wrapper entry points, platforms table); chunk `01-overview.md:270` truncated, no other files in scope.
