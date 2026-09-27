> [[index|Wiki]] | [[summary|Summary]]
# siddsachar/row-bot — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Row-Bot is a local-first desktop AI assistant that reasons through messy context, orchestrates tools and model providers, and works inside user-chosen files, repos, workflows, and channels.
## Key points
- Row-Bot is a local-first desktop AI assistant for doing real work with models, memory, and tools, with the name defining the operating model: Reason, Orchestrate, Work (README.md:22-25).
- It combines chat, durable memory, tool use, Agent Profiles, Goal Mode, parent-led orchestration, Developer/Designer Studios, Smart Skills, Plugin System v2, context metering with rolling compaction, provider-aware reasoning controls, messaging channels, multi-device owner access, Buddy overlay, browser automation, opt-in Computer Use, and provider-aware routing, with durable app data local by default (README.md:27-35).
- For larger tasks it runs the thread through a focused Agent Profile with a visible goal and orchestrates scoped child agents, while the parent joins required results; checkpoints preserve approvals, steering, retries, stops, and recovery, and budgets plus delegation limits bound long runs (README.md:37-42).
- Parallel writers can target distinct existing local folders as separate Developer workspaces with folder-scoped locks allowing concurrency while keeping one writer per shared folder, and app restarts close unanswered tool calls without replaying them (README.md:43-48).
- Recommended Auto capability loading keeps permitted core tools direct and searches enabled MCP, plugin, Custom Tool, and channel capabilities on demand, while long conversations are metered and compacted into durable untrusted reference context preserving the newest turn and atomic tool-call/result groups, with validation and exact capacity errors (README.md:50-59).
- Model paths include local models via Ollama, provider keys (OpenAI, Anthropic, Google AI, xAI, MiniMax, OpenRouter, Atlas Cloud, Requesty, Ollama Cloud, OpenCode Zen/Go), ChatGPT/Codex, Claude Subscription, and xAI Grok subscriptions/OAuth, plus custom OpenAI-compatible endpoints (oMLX, LM Studio, vLLM, llama.cpp, LocalAI, LiteLLM, SGLang), with explicit provider identity, capability labels, reasoning choices, context limits, and media surfaces (README.md:61-72).
- Row-Bot has no account system, no Row-Bot-hosted inference server, and no first-party telemetry pipeline; provider calls go to the chosen provider, keys/tokens live in the OS credential store (Docker uses a separate encryption-key volume with encrypted records), and the optional Computer Use beta requires accepting separately disclosed Cua Driver upstream telemetry (README.md:74-81).
- Distribution is via GitHub Releases, with one-click installers for Windows/macOS and a one-line user installer for Linux (README.md:83).

## 2. [[wiki/02-top-level-files|top-level-files]]
**In one sentence:** The repository root defines agent rules, thin launch wrappers, build/test/security metadata, and the macOS one-click installer that together frame Row-Bot as a local-first desktop assistant.
## Key points
- `AGENTS.md` is the canonical instruction file for AI coding agents, declaring Row-Bot a local-first desktop assistant and ranking protection of local data/secrets above all else (AGENTS.md:1-7).
- Root launchers `app.py` and `launcher.py` contain no application logic; both only prepend `src/` to `sys.path` and delegate to `row_bot.app` / `row_bot.launcher.main` (app.py:12-18, launcher.py:12-19).
- `pyproject.toml` is canonical for dependencies, `uv.lock` is the locked resolution, and `requirements.txt` is a generated installer export that must not be hand-edited (AGENTS.md:92-93, requirements.txt:1-4).
- `scripts/run_test_matrix.py` is the executable source of truth for testing, with `fast`, `changed`, `pr`, and `release` tiers plus focused lanes (contracts, subsystem, deterministic, installer-contracts, app-smoke) (AGENTS.md:119-139).
- `pytest.ini` fixes `testpaths = tests` and `pythonpath = src` and declares the `live_provider`, `contract`, `subsystem`, `snapshot`, `installer`, `mcp_transport`, `integration`, `smoke`, `slow`, and `e2e` markers (pytest.ini:1-17).
- `Start Row-Bot.command` implements a fast-path launch versus first-install setup: it reuses an existing `.venv`, starts Ollama when present, performs a version-aware upgrade, and otherwise installs Python/Ollama/venv/packages/Chromium before writing `~/.row-bot/` state (Start Row-Bot.command:43-63).
- `osv-scanner.toml` holds only narrow, time-bound OSV exceptions (`setuptools` 81.0.0, `torch` 2.11.0 / 2.11.0+cpu, npm `image-size` 2.0.2), all expiring 2026-09-30 (osv-scanner.toml:1-37).
- `SECURITY.md` routes vulnerability reports to email instead of public issues, lists shell/browser/prompt-injection/file-access/updater/channel/key scope, and supports only the latest stable release (SECURITY.md:3-37).

## The system in five moves
1. Row-Bot starts from a local-first identity — Reason, Orchestrate, Work — with durable app data, credentials, and memory kept on the user's machine rather than a hosted backend.
2. The user works through chat inside chosen files, repos, workflows, and channels, with Agent Profiles, Goal Mode, and studios framing larger tasks.
3. The parent thread orchestrates scoped child agents with checkpoints, budgets, and folder-scoped writer locks, joining required results while bounding long runs.
4. Capability loading stays lean via Recommended Auto search over MCP/plugin/custom/channel tools, while metered rolling compaction preserves long conversations within the selected model's window.
5. Any local, hosted, subscription, or self-hosted model can sit side by side behind explicit provider identity and reasoning controls, with provider calls going only to the chosen endpoint.
6. The repository root enforces this operating model in code: canonical agent rules, thin launch wrappers, locked dependencies, tiered test matrix, email-routed security policy, and one-click installers.
