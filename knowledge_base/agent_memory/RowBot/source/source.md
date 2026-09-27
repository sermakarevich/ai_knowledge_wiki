PDF: https://github.com/siddsachar/row-bot (no PDF artifact; source is a git repo, see Source below)
# siddsachar/row-bot
Source: https://github.com/siddsachar/row-bot
Kind: repo
Fetched: 2026-09-26T13:44:18.560982+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# siddsachar/row-bot

Commit: e3bd281e4d515c217017edf1240f486d74bc0bb8

## README

<p align="center">
  <img src="docs/row_bot_glyph_256.png" alt="Row-Bot" width="180">
</p>

<h1 align="center">Row-Bot</h1>

<p align="center"><sub>(formerly Thoth)</sub></p>

<p align="center">
   <a href="https://github.com/siddsachar/row-bot/releases"><img src="https://img.shields.io/github/v/release/siddsachar/row-bot?style=flat&label=release&color=4F78A4" alt="Release"></a>
   <a href="https://github.com/siddsachar/row-bot/actions/workflows/ci.yml"><img src="https://github.com/siddsachar/row-bot/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
   <a href="LICENSE"><img src="https://img.shields.io/github/license/siddsachar/row-bot?style=flat" alt="License"></a>
   <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-4F78A4?style=flat" alt="Platform">
</p>

Row-Bot is a local-first desktop AI assistant for doing real work with models,
memory, and tools. Its name is the operating model: **Reason** through messy
context, **Orchestrate** tools and model providers, and **Work** inside the
files, repos, workflows, and channels you choose.

It combines chat, durable memory, tool use, Agent Profiles, Goal Mode,
automatic parent-led agent orchestration, profile-first workflows, Developer
Studio, Designer Studio, Smart Skills, Skills Hub, Custom Tools, Plugin System
v2, progressive external-tool and skill discovery, context metering and rolling
compaction, provider-aware reasoning controls, messaging channels,
authenticated multi-device owner access with durable trusted addresses,
a native Buddy desktop overlay, managed visible-browser automation, opt-in
native Computer Use, centralized conversation cleanup, realtime voice, and
provider-aware model routing. Durable app data stays local by default.

For larger tasks, Row-Bot can keep a visible goal, run the thread through a
focused Agent Profile, and orchestrate scoped child agents for research, review,
implementation, or follow-up work. The original parent remains responsible for
joining required results and answering, while durable checkpoints preserve
approvals, steering, retries, stops, and recovery. Checkpoint-safe work budgets
and application-wide delegation limits keep long or repetitive runs bounded and
visible. Parallel writers can be assigned to distinct existing local folders as
separate Developer workspaces; folder-scoped locks let those children work
concurrently while preserving one writer at a time inside any shared folder.
If an app restart interrupts delegation or owned shell work, Row-Bot closes
unanswered tool calls without replaying them and resumes the saved parent when
its required child results are ready.

Recommended Auto capability loading keeps permitted core tools directly
available and searches enabled MCP, plugin, Custom Tool, and channel
capabilities only when a request needs them. Enabled manual and plugin skills
can be selected for the current parent or child task under the same profile,
approval, workspace, and execution-budget boundaries. For long conversations,
the responsive desktop composer meters the complete next model input and
Row-Bot can compact complete older turns into durable untrusted reference
context while preserving the newest turn and atomic tool-call/result groups.
It validates the rebuilt prompt before saving and fails with an exact capacity
message when the fixed prompt and tool schemas cannot fit the selected window.

Choose the model path that fits the task: local models through
[Ollama](https://ollama.com/); provider keys for OpenAI, Anthropic, Google AI,
xAI, MiniMax, OpenRouter,
[Atlas Cloud](https://www.atlascloud.ai/?utm_source=github&utm_medium=link&utm_campaign=row_bot),
[Requesty](https://requesty.ai/),
Ollama Cloud, OpenCode Zen, and OpenCode Go; subscription or OAuth sign-in for
ChatGPT / Codex, Claude Subscription, and xAI Grok; or custom
OpenAI-compatible endpoints such as oMLX, LM Studio, vLLM, llama.cpp, LocalAI,
LiteLLM, and SGLang. Row-Bot keeps provider identity, capability labels,
reasoning choices, context limits, media surfaces, and chat-only fallbacks
explicit so local, hosted, subscription, and self-hosted models can sit side by
side.

Row-Bot itself has no account system, no Row-Bot-hosted inference server, and
no first-party telemetry pipeline. Provider calls go to the provider or
endpoint you choose, and provider keys, OAuth tokens, and subscription tokens
are stored in the OS credential store when available. Official Docker
deployments use a separate persistent encryption-key volume and encrypted
credential records instead. The optional Computer Use beta depends on Cua
Driver, whose separately disclosed upstream telemetry must be accepted before
Row-Bot installs or invokes it.

Download the latest installer from [GitHub Releases](https://github.com/siddsachar/row-bot/releases). Windows and macOS use one-click installers. Linux has a one-line user installer.

<table align="center">
  <tr>
    <td align="center"><a href="https://youtu.be/GA2Tnlt4jNk"><img src="https://img.youtube.com/vi/GA2Tnlt4jNk/maxresdefault.jpg" width="360" alt="Turn Research Into a Client-Ready Report with Row-Bot"></a><br><sub><a href="https://youtu.be/GA2Tnlt4jNk">Turn Research Into a Client-Ready Report with Row-Bot</a></sub></td>
    <td align="center"><a href="https://youtu.be/wOUSGTyfEpk"><img src="https://img.youtube.com/vi/wOUSGTyfEpk/maxresdefault.jpg" width="360" alt="Turn Your Inbox Into an Action Plan with Row-Bot"></a><br><sub><a href="https://youtu.be/wOUSGTyfEpk">Turn Your Inbox Into an Action Plan with Row-Bot</a></sub></td>
  </tr>
  <tr>
    <td align="center"><a href="https://youtu.be/Vuk2xz-vPcA"><img src="https://img.youtube.com/vi/Vuk2xz-vPcA/maxresdefault.jpg" width="360" alt="Create a Background AI Workflow with Row-Bot"></a><br><sub><a href="https://youtu.be/Vuk2xz-vPcA">Create a Background AI Workflow with Row-Bot</a></sub></td>
    <td align="center"><a href="https://youtu.be/hRLuOEqbsds"><img src="https://img.youtube.com/vi/hRLuOEqbsds/maxresdefault.jpg" width="360" alt="Create Launch Campaign Designs with Row-Bot Designer Studio"></a><br><sub><a href="https://youtu.be/hRLuOEqbsds">Create Launch Campaign Designs with Row-Bot Designer Studio</a></sub></td>
  </tr>
</table>



## What You Get

| Area | Details |
|------|---------|
| Agent orchestration | LangGraph ReAct agent, Goal Mode, Agent Profiles, Profile Library, automatic parent-led child-agent orchestration, required and detached work, dependency ordering, multi-wave live joins, ordered steering and approvals, transient retry, folder-scoped parallel writers, orphan-only checkpoint repair, explicit parent restart recovery, compact Agent groups and cards, exactly-once completion, checkpoint-safe work budgets, repeated-action protection, configurable nesting/concurrency/active-time limits, profile/tool allowlists, promoted Agent-run workflows, generation-scoped cancellation, complete-input context metering, fixed-envelope preflight, recoverable capacity-aware rolling compaction, and per-thread, per-workflow, per-profile, and per-Developer model overrides. |
| Models and providers | Provider-qualified model selection, exact per-thread/per-model reasoning effort, toggle, and budget controls, readiness routing, chat-only fallback for non-tool models, chat/agent/vision/image/video capability labels, native Ollama tool-capability detection with maintained-family fallback, model-scoped custom endpoint profiles and probes, detected/manual/custom context caps, provider-scoped credential-backed live catalog discovery with last-known-good preservation, xAI Grok OAuth and live image-generation quality/resolution metadata, ChatGPT / Codex and Claude Subscription providers, native OpenCode gateway discovery and per-model transport routing, provider-scoped tool-schema compatibility, phased OpenAI-compatible timeouts with safe pre-stream retry, prompt-cache diagnostics, and background model cache. |
| Memory and knowledge | Personal knowledge graph, 10 entity types, 67 typed relations, bounded semantic/lexical/graph recall, a disclosed checked-by-default local embedding setup download, cache-only normal recall, explicit repair, fast lexical/graph fallback, durable bounded document batches, streamed upload hashing and deduplication, atomic sharded vectors, resumable extraction, queue controls and health repair, audit and review states, recall traces, graph visualization, Obsidian-compatible wiki export with source provenance, Dream Cycle refinement, duplicate merging, stale-confidence decay, relationship inference, self-knowledge, insights, and conversation search. |
| Tools | 30+ core tool modules for web search, DuckDuckGo, Wikipedia, arXiv, YouTube transcripts, URL reading, documents, wiki vault, Gmail, Google Calendar, filesystem, shell, managed visible-browser automation, opt-in native Computer Use, workflows, Goal Mode, child-agent delegation, tracker, channels, X, image generation/editing, video generation, MCP, Developer Studio, Designer Studio, Custom Tool Builder, status, calculator, Wolfram Alpha, weather, vision, memory, system info, and charts. Browser and Computer Use keep separate targets and runtimes but share bounded observation, receipt, error, activity, approval, and cancellation contracts. Recommended Auto loading keeps core profile tools direct and searches enabled external MCP, plugin, Custom Tool, and channel schemas on demand; eager compatibility mode remains available. File tools read PDF, CSV, Excel, JSON, JSONL, TSV, and image files, with schema, stats, previews, and PDF export where supported. |
| Developer Studio | Local Git workspace linking and cloning, code threads, explicit existing-folder assignment for child Agents, folder-scoped writer locks, per-thread and child-agent worktrees, repo inspector, file tree, diffs, todos, tests, branch, commit, push and PR prep, approval modes, and optional Docker Sandbox with a shadow workspace and explicit import back into the real repo. Docker Sandbox intentionally fails closed inside the official Row-Bot server container instead of nesting or falling back silently. |
| Designer Studio | Decks, documents, landing pages, app mockups, and storyboards with a sandboxed interactive runtime, templates, brand controls, critique and repair, AI image and video generation, chart insertion, Mermaid and Plotly rendering, shareable HTML, and export to PDF, HTML, PNG, and PPTX. |
| Workflows | Scheduled runs, webhook triggers, task-completion triggers, step pipelines, conditions, approvals, subtasks, notification-only runs, concurrency groups, delivery defaults, profile-first workflow agents, promoted Agent-run workflows, per-workflow model/tool/skill/profile overrides, safety modes, run status, run history, upcoming runs, and a Workflow Console. |
| Controlled self-evolution | Structured self-reflection, bounded change proposals, reviewable execution boundaries, persistence, Dream Cycle and memory integration, and Command Center/status visibility for improvement work that stays explicit and auditable. |
| Channels and voice | Telegram, WhatsApp, Discord, Slack, SMS, and plugin-owned channels with platform-aware live streaming, typing and edit fallbacks, interactive approvals, durable child-agent and Goal Mode notices, media intake, voice transcription, document extraction, health checks, auto-generated send/photo/document tools, and optional tunnel support. SMS remains final-text-only. Realtime voice adds provider-backed voice sessions, action handling, speech/cue policy, and local faster-whisper or FunASR/SenseVoice STT plus Kokoro TTS options. |
| Platform and app | Native desktop app plus authenticated single-owner desktop and compact browser access; one-time invitations, durable revocable sessions, exact trusted-address add/remove controls, assigned-interface route discovery, route and device management, Tailscale Serve, browser-local voice, and strict HTTP/WebSocket origin gates; authenticated headless `serve` mode; off

... (truncated, 58237 more characters)

## pyproject.toml

```
[build-system]
requires = [
  "setuptools>=80,<81",
  "wheel>=0.45,<0.46",
]
build-backend = "setuptools.build_meta"

[project]
name = "row-bot"
dynamic = ["version"]
description = "Local-first personal AI assistant."
readme = "README.md"
requires-python = ">=3.12,<3.14"
license = { file = "LICENSE" }
authors = [
  { name = "Row-Bot" },
]
dependencies = [
  "nicegui>=2.21,<4.0",
  "fastapi>=0.115,<1.0",
  "starlette>=1.3.1,<1.4",
  "ollama>=0.5,<1.0",
  "langchain>=1.0,<2.0",
  "langchain-core>=1.0,<2.0",
  "langchain-classic>=1.0,<2.0",
  "langchain-community>=0.4,<0.5",
  "langchain-google-community[gmail]>=2.0,<4.0",
  "langchain-ollama>=1.0,<2.0",
  "langchain-anthropic>=1.0,<2.0",
  "langchain-google-genai>=4.2.4,<5.0",
  "langchain-openai>=1.3.3,<2.0",
  "langchain-openrouter>=0.2,<0.3",
  "langchain-xai>=0.2,<2.0",
  "langchain-text-splitters>=1.0,<2.0",
  "langgraph>=1.0,<2.0",
  "langgraph-checkpoint-sqlite>=2.0,<4.0",
  "tiktoken>=0.9,<1.0",
  "openai>=2.0,<3.0",
  "anthropic>=0.69,<2.0",
  "google-genai>=1.30,<2.0",
  "tavily-python>=0.7,<1.0",
  "wikipedia>=1.4,<2.0",
  "arxiv>=3.0,<4.0",
  "duckduckgo-search>=8.1,<9.0",
  "ddgs>=9.0,<10.0",
  "networkx>=3.4,<4.0",
  "simpleeval>=1.0,<2.0",
  "apscheduler>=3.11,<4.0",
  "plyer>=2.1,<3.0",
  "numpy>=1.26,<2.3",
  "requests>=2.32,<3.0",
  "httpx>=0.28,<1.0",
  "pydantic>=2.10,<3.0",
  "pyyaml>=6.0,<7.0",
  "beautifulsoup4>=4.13,<5.0",
  "keyring>=24.0,<26.0",
  "wolframalpha>=5.1,<6.0",
  "psutil>=6.0,<8.0",
  "pystray>=0.19,<1.0",
  "pyobjc-core>=12.2,<13.0; sys_platform == 'darwin'",
  "pyobjc-framework-Cocoa>=12.2,<13.0; sys_platform == 'darwin'",
  "Pillow>=11.0,<13.0",
  "qrcode>=8.0,<9.0",
  "pyjwt[crypto]>=2.8,<3.0",
  "pywebview>=5.4,<6.0",
]

[project.optional-dependencies]
voice = [
  "sounddevice>=0.5,<1.0",
  "faster-whisper>=1.1,<2.0",
  "funasr>=1.3.22,<2.0; sys_platform != 'darwin' or platform_machine != 'x86_64'",
  "modelscope>=1.38,<2.0; sys_platform != 'darwin' or platform_machine != 'x86_64'",
  "torch==2.11.0; sys_platform != 'darwin' or platform_machine != 'x86_64'",
  "torchaudio==2.11.0; sys_platform != 'darwin' or platform_machine != 'x86_64'",
  "kokoro-onnx>=0.4,<1.0",
]
designer = [
  "fpdf2>=2.8,<3.0",
  "python-pptx>=1.0,<2.0",
  "python-docx>=1.1,<2.0",
  "pandas>=2.2,<3.0",
  "plotly>=6.0,<7.0",
  "kaleido>=1.0,<2.0",
  "playwright>=1.62,<2.0",
]
browser = [
  "playwright>=1.62,<2.0",
]
channels = [
  "python-telegram-bot>=22.0,<23.0",
  "slack-bolt>=1.28,<2.0",
  "twilio>=9.0,<10.0",
  "discord.py>=2.7,<3.0",
  "pyngrok>=7.0,<8.0",
]
mcp = [
  "mcp>=1.20,<2.0",
  "langchain-mcp-adapters>=0.1,<1.0",
]
developer = [
  "pywinpty>=2.0,<3.0; sys_platform == 'win32'",
]
local-embeddings = [
  "faiss-cpu>=1.12,<2.0",
  "sentence-transformers>=5.1,<6.0",
  "huggingface-hub>=1.5,<2.0",
  "transformers>=5.3,<6.0",
  "tokenizers>=0.22,<1.0",
  "einops>=0.8,<1.0",
  "torch>=2.7,<3.0",
  "langchain-huggingface>=1.0,<2.0",
]
media = [
  "opencv-python>=4.10,<5.0",
  "mss>=9.0,<11.0",
  "youtube-search>=2.1,<3.0",
  "youtube-transcript-api>=1.2,<2.0",
  "pypdf>=6.16.1,<7.0",
  "pandas>=2.2,<3.0",
  "openpyxl>=3.1,<4.0",
  "xlrd>=2.0,<3.0",
  "plotly>=6.0,<7.0",
  "kaleido>=1.0,<2.0",
]
all = [
  "sounddevice>=0.5,<1.0",
  "faster-whisper>=1.1,<2.0",
  "funasr>=1.3.22,<2.0; sys_platform != 'darwin' or platform_machine != 'x86_64'",
  "modelscope>=1.38,<2.0; sys_platform != 'darwin' or platform_machine != 'x86_64'",
  "torchaudio==2.11.0; sys_platform != 'darwin' or platform_machine != 'x86_64'",
  "kokoro-onnx>=0.4,<1.0",
  "fpdf2>=2.8,<3.0",
  "python-pptx>=1.0,<2.0",
  "python-docx>=1.1,<2.0",
  "pandas>=2.2,<3.0",
  "plotly>=6.0,<7.0",
  "kaleido>=1.0,<2.0",
  "playwright>=1.62,<2.0",
  "python-telegram-bot>=22.0,<23.0",
  "slack-bolt>=1.28,<2.0",
  "twilio>=9.0,<10.0",
  "discord.py>=2.7,<3.0",
  "pyngrok>=7.0,<8.0",
  "mcp>=1.20,<2.0",
  "langchain-mcp-adapters>=0.1,<1.0",
  "pywinpty>=2.0,<3.0; sys_platform == 'win32'",
  "faiss-cpu>=1.12,<2.0",
  "sentence-transformers>=5.1,<6.0",
  "huggingface-hub>=1.5,<2.0",
  "transformers>=5.3,<6.0",
  "tokenizers>=0.22,<1.0",
  "einops>=0.8,<1.0",
  "torch==2.11.0; sys_platform != 'darwin' or platform_machine != 'x86_64'",
  "torch>=2.7,<3.0",
  "langchain-huggingface>=1.0,<2.0",
  "opencv-python>=4.10,<5.0",
  "mss>=9.0,<11.0",
  "youtube-search>=2.1,<3.0",
  "youtube-transcript-api>=1.2,<2.0",
  "pypdf>=6.16.1,<7.0",
  "openpyxl>=3.1,<4.0",
  "xlrd>=2.0,<3.0",
]

[project.scripts]
row-bot = "row_bot.launcher:main"

[dependency-groups]
test = [
  "pytest>=9.0.3,<10.0",
  "pytest-cov>=6.0,<8.0",
]
lint = [
  "ruff>=0.12,<1.0",
]
dev = [
  "build>=1.3,<2.0",
  "pytest>=9.0.3,<10.0",
  "ruff>=0.12,<1.0",
]

[tool.setuptools]
package-dir = { "" = "src", "scripts" = "scripts" }

[tool.setuptools.cmdclass]
build_py = "scripts.client_build.ClientBuildPy"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
"row_bot.computer_use" = ["*.json"]
"row_bot.designer.runtime" = ["runtime_bridge.js", "runtime_bridge.css"]
"row_bot.voice" = ["realtime_runtime.js", "realtime_runtime.d.ts"]
"row_bot" = [
  "static/client-v2/index.html",
  "static/client-v2/app.webmanifest",
  "static/client-v2/service-worker.js",
  "static/client-v2/icon-192.png",
  "static/client-v2/icon-512.png",
  "static/client-v2/asset-manifest.json",
  "static/client-v2/.vite/manifest.json",
  "static/client-v2/assets/*",
]

[tool.setuptools.dynamic]
version = { attr = "row_bot.version.__version__" }

[tool.uv]
required-version = ">=0.7"

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch-cpu" }
torchaudio = { index = "pytorch-cpu" }

```

## Top-level layout

- .dockerignore (~39 lines)
- .gitattributes (~35 lines)
- .github/ (dir, 25 files, ~2321 lines)
- .gitignore (~91 lines)
- AGENTS.md (~250 lines)
- app.py (~17 lines)
- build_linux_app.sh (~7 lines)
- bundled_skills/ (dir, 17 files, ~1188 lines)
- CLAUDE.md (~6 lines)
- CODE_OF_CONDUCT.md (~30 lines)
- contracts/ (dir, 368 files, ~113925 lines)
- CONTRIBUTING.md (~251 lines)
- deploy/ (dir, 8 files, ~814 lines)
- docs/ (dir, 442 files, ~17404 lines)
- docs-content/ (dir, 13 files, ~2234 lines)
- docs-site/ (dir, 160 files, ~24072 lines)
- examples/ (dir, 7 files, ~182 lines)
- frontend/ (dir, 421 files, ~151784 lines)
- installer/ (dir, 15 files, ~2854 lines)
- launcher.py (~18 lines)
- LICENSE (~190 lines)
- NOTICE (~4 lines)
- osv-scanner.toml (~36 lines)
- pyproject.toml (~220 lines)
- pytest.ini (~16 lines)
- README.md (~957 lines)
- RELEASE_NOTES.md (~5700 lines)
- requirements.txt (~304 lines)
- row-bot.ico (~0 lines)
- scripts/ (dir, 52 files, ~16611 lines)
- SECURITY.md (~36 lines)
- sounds/ (dir, 2 files, ~0 lines)
- src/ (dir, 591 files, ~319944 lines)
- Start Row-Bot.command (~416 lines)
- static/ (dir, 148 files, ~4614 lines)
- tests/ (dir, 680 files, ~186230 lines)
- tool_guides/ (dir, 23 files, ~919 lines)
- uv.lock (~5437 lines)

