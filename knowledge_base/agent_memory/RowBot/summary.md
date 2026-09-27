# Technical Analysis: siddsachar/row-bot

**Repository:** https://github.com/siddsachar/row-bot
**Version analyzed:** 4.9.1 (fallback in Start Row-Bot.command:13-41; RELEASE_NOTES.md:1-40 head only)
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Row-Bot addresses the problem of running model-assisted work that spans files, repos, workflows, memory, and messaging channels without routing all data through a hosted service. The wiki defines it as "a local-first desktop AI assistant for doing real work with models, memory, and tools" whose name is the operating model: Reason through messy context, Orchestrate tools and model providers, Work inside user-chosen files, repos, workflows, and channels (README.md:22-25).

The primary user is an individual owner-operator on a desktop machine (Windows/macOS first-class, Linux browser/server) who wants provider choice, durable local memory, bounded agent delegation, and channel/voice access under one install. The repo addresses this by combining chat, durable memory/knowledge graph, 30+ core tool modules, Agent Profiles with Goal Mode and parent-led child-agent orchestration, Developer/Designer Studios, workflows with schedules/webhooks, Smart Skills, Plugin System v2, MCP, context metering with rolling compaction, multi-provider routing (local Ollama, provider keys, ChatGPT/Codex and Claude subscriptions, xAI Grok OAuth, custom OpenAI-compatible endpoints), and messaging channels, with app data local by default and no account system, no hosted inference server, and no first-party telemetry pipeline (README.md:27-35, README.md:37-42, README.md:61-72, README.md:74-81).

## 2. High-Level Architecture

```
User surfaces (desktop composer │ Buddy overlay │ browser │ channels/voice)
  ▼
Agent runtime (LangGraph ReAct agent │ Agent Profiles │ Goal Mode │ parent-led orchestration)
  ▼
Capability layer (30+ core tools ─ MCP ─ plugins ─ Custom Tools ─ skills ─ channel capabilities)
  ▼
Provider / model routing (Ollama │ provider keys │ subscriptions/OAuth │ custom OpenAI-compatible endpoints)
  ▼
Durable local state (~/.row-bot/ │ OS credential store │ Docker encryption-key volume │ knowledge graph / vectors)
```

Data-flow narrative:

1. Input enters through the desktop composer, Buddy overlay, browser access, or a channel adapter (Telegram, WhatsApp, Discord, Slack, SMS, plugin-owned channels), with realtime voice via provider-backed sessions plus local faster-whisper or FunASR/SenseVoice STT and Kokoro TTS (README.md:98-111).
2. The thread runs through the LangGraph ReAct agent under a focused Agent Profile with a visible goal; for larger tasks the parent orchestrates scoped child agents (research, review, implementation, follow-up) with required vs. detached work, dependency ordering, multi-wave live joins, steering/approvals, retries, and generation-scoped cancellation, joining required results itself (README.md:37-42, README.md:98-111).
3. Capability loading resolves tools per request: Recommended Auto keeps permitted core tools direct and searches enabled MCP, plugin, Custom Tool, and channel capabilities on demand; skills are selected per parent/child task under the same profile, approval, workspace, and budget boundaries (README.md:50-54).
4. Model calls route by provider identity with explicit capability labels, reasoning controls, context limits, and media surfaces; local models go through Ollama, hosted through provider keys, subscriptions through ChatGPT/Codex and Claude Subscription sign-in and xAI Grok OAuth, self-hosted through custom OpenAI-compatible endpoint profiles (README.md:61-72, README.md:98-111).
5. Long conversations are metered (complete next model input) and compacted (older turns into durable untrusted reference context preserving newest turn and atomic tool-call/result groups, validated before save, exact capacity error on failure); checkpoints preserve approvals, steering, retries, stops, and recovery, bounded by work budgets and delegation limits (README.md:41-43, README.md:54-59).
6. Persistent state lives locally by default: app state under `~/.row-bot/` (Start Row-Bot.command:13-41, Start Row-Bot.command:122-200), provider keys/OAuth/subscription tokens in the OS credential store (Docker uses a separate persistent encryption-key volume with encrypted records), plus durable memory artifacts (knowledge graph, sharded vectors, document batches, checkpoints, run history) on local disk (README.md:74-81, README.md:98-111).

## 3. The Agent Thread with Checkpointed Orchestration

The central concept is the agent thread: a goal-scoped conversation that carries profile, model override, approvals, budgets, checkpoints, and child-agent joins. Representation in the wiki is behavioral rather than a single class definition: thread + Agent Profile + visible goal + parent/child delegation + durable checkpoints + work budgets + context metering/compaction (README.md:37-42, README.md:50-59, README.md:98-111).

Named kinds/types attested in the wiki:

- Agent Profiles and Profile Library, with per-thread/per-workflow/per-profile/per-Developer model overrides (README.md:98-111).
- Goal Mode with durable child-agent and Goal Mode notices (README.md:98-111).
- Parent-led child agents: required and detached work, dependency ordering, multi-wave live joins, ordered steering and approvals, transient retry, configurable nesting/concurrency/active-time limits, profile/tool allowlists (README.md:37-42, README.md:98-111).
- Developer workspaces: distinct existing local folders as parallel-writer scopes with folder-scoped locks (one writer per shared folder), per-thread and child-agent worktrees, optional Docker Sandbox with shadow workspace and explicit import (README.md:43-45, README.md:98-111).
- Memory entities: personal knowledge graph with 10 entity types and 67 typed relations, bounded semantic/lexical/graph recall, document batches, audit/review states, recall traces, Dream Cycle refinement (README.md:98-111).

Key queries are not SQL but operational rules, stated verbatim:

```
"closes unanswered tool calls without replaying them and resumes the saved parent when its required child results are ready" (README.md:46-48)
```

```
"the responsive desktop composer meters the complete next model input" and "Row-Bot can compact complete older turns into durable untrusted reference context while preserving the newest turn and atomic tool-call/result groups" (README.md:54-57)
```

## 4. LLM / External Service Integration

Providers (README.md:61-72): local models via Ollama; provider keys for OpenAI, Anthropic, Google AI, xAI, MiniMax, OpenRouter, Atlas Cloud, Requesty, Ollama Cloud, OpenCode Zen, OpenCode Go; subscription/OAuth sign-in for ChatGPT/Codex, Claude Subscription, xAI Grok; custom OpenAI-compatible endpoints (oMLX, LM Studio, vLLM, llama.cpp, LocalAI, LiteLLM, SGLang). Native OpenCode gateway discovery with per-model transport routing; provider-scoped credential-backed live catalog discovery with last-known-good preservation; xAI live image-generation quality/resolution metadata (README.md:98-111).

Required vs. optional calls: no call is required by default. Ground rules prohibit surprise network/provider/channel calls and require preserving approval gates (AGENTS.md:13-19, AGENTS.md:21-44). Provider calls go only to the chosen provider/endpoint (README.md:74-77). Default tests must not depend on live providers, MCP, channels, network, or Ollama models; live-provider tests are an opt-in `live_provider` marker lane (AGENTS.md:21-44, pytest.ini:6-17). Optional external calls include web search, DuckDuckGo, Wikipedia, arXiv, YouTube transcripts, URL reading, Gmail, Google Calendar, X, image/video generation/editing, Wolfram Alpha, weather, and Cua Driver for the opt-in Computer Use beta (README.md:98-111, README.md:79-81).

Env vars: the two wiki pages name no provider env-var names. Credential storage is stated as OS credential store when available, Docker encrypted records otherwise (README.md:75-79). Config/state paths attested: `~/.row-bot/` for `row_bot_home` and `installed_version` (Start Row-Bot.command:122-200), port 11434 for the Ollama presence check (Start Row-Bot.command:43-63).

## 5. The Parent-Led Task Run Pipeline

Primary workflow: a goal-scoped thread executed by a parent agent that delegates to scoped children and joins required results (README.md:37-42).

1. Scope the thread: select Agent Profile (optionally from Profile Library), set visible goal, apply per-thread/per-workflow/per-profile/per-Developer model overrides and profile/tool allowlists (README.md:98-111).
2. Load capabilities: Recommended Auto keeps permitted core tools direct; enabled MCP, plugin, Custom Tool, and channel capabilities are searched only when the request needs them; manual/plugin skills are selected for the current parent or child task under the same boundaries (README.md:50-54).
3. Delegate: parent creates scoped child agents for research, review, implementation, or follow-up with required vs. detached designation, dependency ordering, and nesting/concurrency/active-time limits; parallel writers map to distinct existing local folders with folder-scoped locks (README.md:37-45).
4. Execute with controls: ordered steering and approvals, transient retry, repeated-action protection, generation-scoped cancellation, checkpoint-safe work budgets; Developer children work in assigned folders/worktrees or the optional Docker Sandbox (fails closed inside the official server container); channel runs support interactive approvals and notification-only runs (README.md:41-45, README.md:98-111).
5. Join and complete: parent joins required results and answers with exactly-once completion and multi-wave live joins; durable checkpoints preserve approvals, steering, retries, stops, and recovery; orphan-only checkpoint repair and explicit parent restart recovery apply on failure (README.md:39-42, README.md:98-111).
6. Bound the context: meter the complete next input including fixed envelope preflight; compact older turns into durable untrusted reference context preserving newest turn and atomic tool-call/result groups; validate rebuilt prompt before saving; fail with exact capacity message when fixed prompt plus tool schemas exceed the window; app restart closes unanswered tool calls without replay and resumes the saved parent when required child results are ready (README.md:46-48, README.md:54-59, README.md:98-111).

No function-level file.py:line citations are available: the wiki's two pages describe this pipeline from README.md behavior and never expose the implementing module/function names.

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | head + 98-111 cited | Identity, operating model, feature surface, provider paths, install |
| `AGENTS.md` | 1-232 cited | Canonical agent instructions, priorities, ground rules, test lanes, release flow |
| `CLAUDE.md` | 1-7 | Pointer declaring `@AGENTS.md` canonical |
| `app.py` | 8-18 | Thin launcher: prepend `src/`, `runpy` into `row_bot.app` |
| `launcher.py` | 9-19 | Thin launcher: prepend `src/`, call `row_bot.launcher.main` |
| `src/row_bot/version.py` | version read cited | Version source read by macOS installer with fallback |
| `pyproject.toml` | canonical per AGENTS.md:92-93 | Canonical dependency declarations |
| `uv.lock` | locked per AGENTS.md:92-93 | Locked dependency resolution |
| `requirements.txt` | 1-305 | Generated installer export (305 pinned lines, CPU torch index) |
| `pytest.ini` | 1-17 | `testpaths`, `pythonpath`, addopts/cache, 10 test markers |
| `scripts/run_test_matrix.py` | per AGENTS.md:119-139 | Executable test matrix: fast/changed/pr/release + focused lanes |
| `scripts/cut_release.py` | per AGENTS.md:220-232 | Release-cut entry used in branch release flow |
| `scripts/export_locked_requirements.py` | per requirements.txt:1-4 | Regenerates requirements.txt via `uv export` |
| `Start Row-Bot.command` | 1-200+ (truncated) | macOS double-click installer/launcher, Ollama/venv/Chromium setup |
| `installer/build_linux_app.sh` | via 7-line wrapper | Real Linux app builder (root `build_linux_app.sh` forwards) |
| `osv-scanner.toml` | 1-37 | Time-bound OSV exceptions expiring 2026-09-30 |
| `SECURITY.md` | 3-37 | Vulnerability reporting policy and in-scope areas |
| `RELEASE_NOTES.md` | 1-190+ (truncated) | v4.9.1/v4.9.0 heads; ~475k chars absent after cut |
| `NOTICE` | 1-5 | Copyright and Apache-2.0 attribution |
| `.gitignore` / `.dockerignore` / `.gitattributes` | 92 / 40 / 36 | Ignore, container-exclude, line-ending/generated-file metadata |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `nicegui` | `==3.12.1` | Desktop/web UI (per requirements.txt:5-305) |
| `playwright` | `==1.62.0` | Managed visible-browser automation; Chromium installed at setup |
| `torch` | `==2.11.0` / `2.11.0+cpu` | Local embedding/model support via CPU extra index |
| `setuptools` | `==81.0.0` | Build backend pin (Torch 2.11 requires setuptools<82) |
| `uv` / `pip` toolchain | `uv export --locked --all-extras --no-dev --no-hashes` | Locked export of requirements.txt (requirements.txt:1-4) |
| `ollama` (external service) | presence-checked, not version-pinned in wiki | Local model serving (`ollama serve`, port 11434 check) |
| `chromium` (via playwright) | `python -m playwright install chromium` | Browser automation runtime |
| provider/channel/MCP/voice/document packages | pinned in 305-line requirements.txt:5-305 (exact strings not enumerated in wiki) | Hosted models, channels, MCP, STT/TTS, file ingestion |
| `image-size` (npm) | `2.0.2` | Docs-build-only transitive dep (osv-scanner.toml:30-37) |

Constraint strings above are exact as quoted in the wiki (`==` pins, `uv export` flags, install commands). The wiki states `pyproject.toml` is canonical and `uv.lock` is the lockfile, with `requirements.txt` generated and not hand-edited (AGENTS.md:92-93, requirements.txt:1-4).

## 8. CLI / Usage Surface

Entry points:

| Entry | Command | Behavior |
|---|---|---|
| `app.py` | `python app.py` | Prepends `src/`, `runpy.run_module("row_bot.app")` (app.py:8-16) |
| `launcher.py` | `python launcher.py` | Prepends `src/`, `from row_bot.launcher import main; main()` (launcher.py:9-19) |
| `Start Row-Bot.command` | double-click on macOS | Fast-path reuse of `.venv` + Ollama start + version-aware upgrade, else full install (Start Row-Bot.command:43-63, 122-200) |
| `build_linux_app.sh` | `./build_linux_app.sh "$@"` | Forwards to `installer/build_linux_app.sh` (build_linux_app.sh:1-7) |
| Test matrix | `uv run python scripts/run_test_matrix.py fast` | Focused change tier; variants `changed --base origin/main`, `pr`, `release`, plus `contracts`, `subsystem`, `contract-subsystem`, `coverage`, `deterministic`, `installer-contracts`, `app-smoke`, `legacy-inventory` (AGENTS.md:119-139) |
| Release cut | `python scripts/cut_release.py X.Y.Z` | Branch release flow, then `pr` matrix, merge, manual `release.yml`, artifact/checksum review, `installer-verify.yml`, OS signing/notarization, clean-machine smoke (AGENTS.md:220-232) |
| Requirements export | `python scripts/export_locked_requirements.py` | Regenerates requirements.txt (requirements.txt:1-4) |
| Headless serve | authenticated headless `serve` mode | Single-owner desktop + compact browser access (README.md:98-111, truncated row) |

Env-var and config table (only attested values; wiki names no secret env-var keys):

| Key / Path | Scope | Meaning |
|---|---|---|
| `PATH` prepend `/opt/homebrew/bin`, `/usr/local/bin` | `Start Row-Bot.command:13-41` | Finder-launch PATH fix on macOS |
| `PROJECT_DIR`, `.venv`, `~/.row-bot/` | `Start Row-Bot.command:13-41` | Resolved install/state locations |
| `~/.row-bot/row_bot_home`, `~/.row-bot/installed_version` | `Start Row-Bot.command:122-200` | Recorded home and installed version |
| `ROW_BOT_VERSION` vs `INSTALLED_VERSION` | `Start Row-Bot.command:43-63` | Version-aware upgrade gate |
| `11434` (Ollama port) | `Start Row-Bot.command:43-63` | Listening check before `ollama serve` |
| `python3.12/3.11/3.10/3/python`, 3.10+ floor | `Start Row-Bot.command:122-200` | `find_python` interpreter selection |
| `pytest.ini` settings/markers | `pytest.ini:1-17` | `testpaths=tests`, `pythonpath=src`, 10 markers |
| OS credential store / Docker encryption-key volume | `README.md:75-79` | Key/token storage locations |

## 9. Extensibility Points

- MCP servers/capabilities: searched on demand under Auto loading; `mcp_transport` marker covers transport and tool-safety contracts; treat MCP changes as security-sensitive with cross-subsystem tests and `source_test_map.py` updates (README.md:50-52, pytest.ini:6-17, AGENTS.md:78-88).
- Plugin System v2 and plugin-owned channels: searched on demand; plugin skills selectable per parent/child task under profile/approval/budget boundaries (README.md:50-54, README.md:98-111).
- Custom Tool Builder / Custom Tools: same on-demand capability path as MCP/plugins (README.md:50-52, README.md:98-111).
- Smart Skills (manual + plugin): select per current parent or child task; same boundary inheritance (README.md:52-54).
- Agent Profiles / Profile Library and promoted Agent-run workflows: add profiles, allowlists, per-workflow model/tool/skill/profile overrides, safety modes, concurrency groups (README.md:98-111).
- Workflows: schedules, webhooks, task-completion triggers, step pipelines, conditions, approvals, subtasks, notification-only runs, Workflow Console (README.md:98-111).
- Developer/Designer Studios: Developer git workspaces, worktrees, repo inspector, Docker Sandbox; Designer templates, brand controls, Mermaid/Plotly, export targets (README.md:98-111).
- Channels and voice: Telegram/WhatsApp/Discord/Slack/SMS adapters, tunnel support, STT/TTS backends (faster-whisper, FunASR/SenseVoice, Kokoro) (README.md:98-111).
- Custom model endpoints: model-scoped custom endpoint profiles and probes for OpenAI-compatible servers (README.md:98-111).

## 10. Limitations and Gotchas

- **Truncated evidence:** Platform-and-app feature row cuts mid-word at "off" (README.md:111), `Start Row-Bot.command` loses ~4093 trailing chars after the `Info.plist` stanza, and `RELEASE_NOTES.md` loses ~475k chars after the Buddy lifecycle section; no claims are made beyond the cuts (01-overview.md:46-49, 02-top-level-files.md:87-89).
- **Time-bound vulnerability exceptions:** `setuptools` 81.0.0, `torch` 2.11.0/2.11.0+cpu, npm `image-size` 2.0.2 exceptions all expire 2026-09-30; past expiry the OSV gate fails closed unless re-triaged (osv-scanner.toml:1-37).
- **Restart drops pending tool calls:** app restarts close unanswered tool calls without replaying them and only resume the saved parent when required child results are ready; in-flight approvals/actions do not survive restart (README.md:46-48).
- **Capacity failures are hard errors:** when the fixed prompt plus tool schemas cannot fit the selected window, compaction validates and then fails with an exact capacity message rather than silently degrading (README.md:58-59).
- **Narrow support window:** only the latest stable release is supported, with critical backports only when practical; vulnerability reports must go to email, never public issues (SECURITY.md:3-37).
- **Sandbox and installer sharp edges:** Sandbox fails closed inside the official server container; macOS setup continues cloud-only with a warning if Ollama install is declined; generated `requirements.txt` must never be hand-edited (README.md:98-111, Start Row-Bot.command:122-200, AGENTS.md:21-44).

## 11. How It Compares to Alternatives

- **AnythingLLM:** desktop/server RAG assistant with multi-provider chat and document recall. Row-Bot covers the same local-chat-plus-memory shape but adds parent-led child-agent orchestration, Developer/Designer Studios, workflows, and channel/voice operation in one desktop install (README.md:37-42, README.md:98-111).
- **Open WebUI:** self-hosted model front-end with pipelines and knowledge features. Row-Bot is instead a local-first desktop app with OS-credential-store secrets, folder-scoped parallel writers, checkpointed delegation, and metering/compaction semantics rather than a server UI over models (README.md:43-48, README.md:54-59, README.md:74-81).
- **LangChain / LangGraph agent stacks:** toolkit for building ReAct agents and graphs. Row-Bot ships a finished LangGraph ReAct agent product on top of that pattern (orchestration, budgets, exactly-once completion, capacity-aware compaction) rather than a library for assembling one (README.md:98-111).
- **CrewAI / AutoGen-style multi-agent frameworks:** code-first role/delegation frameworks. Row-Bot provides the equivalent delegation (required/detached work, dependency ordering, live joins, steering/approvals) as end-user runtime behavior with checkpoints and budgets, not as developer API (README.md:37-42, README.md:98-111).

Positioning: Row-Bot occupies the local-first desktop owner-operator niche — provider-neutral routing plus durable memory, bounded multi-agent execution, and channel-connected workflows under local data custody — where the alternatives are either self-hosted server UIs, RAG front-ends, or frameworks requiring custom assembly.

## Appendix: Selected Code Snippets

1. Root wrapper import-path shim (app.py:8-11, launcher.py:9-12):

```
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
```

2. Root wrapper dispatch lines (app.py:16, launcher.py:15-19):

```
runpy.run_module("row_bot.app", run_name="__main__")   # app.py:16
from row_bot.launcher import main                        # launcher.py:15
main()                                                   # launcher.py:19 (under __main__)
```

3. Linux builder forwarder (build_linux_app.sh:1-7):

```
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/installer/build_linux_app.sh" "$@"
```

4. Test core settings and generated-requirements header (pytest.ini:1-5, requirements.txt:1-4):

```
testpaths = tests
pythonpath = src
addopts = --ignore=tests/test_output_log.txt --basetemp=.tmp/pytest_tmp_current
cache_dir = .tmp/pytest_cache_current
```

```
# This file is generated from pyproject.toml and uv.lock.
# Do not edit by hand.
# Regenerate with: python scripts/export_locked_requirements.py
# Export command: uv export --locked --all-extras --no-dev --no-hashes --no-emit-project --output-file requirements.txt
```
