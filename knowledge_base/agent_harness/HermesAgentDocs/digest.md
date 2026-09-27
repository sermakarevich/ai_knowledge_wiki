> [[index|Wiki]] | [[summary|Summary]]

# Hermes Agent Documentation — Digest

The whole source at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-installation-and-quickstart|Installation and Quickstart]]

**In one sentence:** Install Hermes Agent with the Desktop installer or one curl/PowerShell command, configure a provider with `hermes setup --portal` or `hermes model`, then verify with `hermes` and `hermes --continue` before adding gateway, tools, skills, MCP, or ACP layers.

- Install on Linux, macOS, WSL2 (Windows Subsystem for Linux 2), or Termux (Android terminal app) with `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash` and reload the shell with `source ~/.bashrc` or `source ~/.zshrc`.
- Install on native Windows 10/11 in PowerShell (command-line shell for Windows) with `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`, or use the Hermes Desktop installer on macOS or Windows for CLI (Command Line Interface) plus desktop app together.
- Prerequisites are Git on all non-Windows platforms plus `curl` and `xz-utils` on Linux (for example `sudo apt install curl xz-utils` on Debian/Ubuntu), with `build-essential` or `g++` additionally required for the desktop app.
- Per-user installs put code at `~/.hermes/hermes-agent/`, the launcher at `~/.local/bin/hermes`, and data at `~/.hermes/`, while root-mode installs use `/usr/local/lib/hermes-agent/`, `/usr/local/bin/hermes`, and `/root/.hermes/` or `$HERMES_HOME`.
- Fastest provider setup is `hermes setup --portal` for Nous Portal OAuth (login in browser, no API key) login covering 300+ models plus Tool Gateway, otherwise run `hermes model` and switch providers any time with the same command.
- Hermes Agent requires a model with at least 64,000 tokens of context (64K context minimum), so local models must be started with at least `--ctx-size 65536` or `-c 65536`.
- Secrets and tokens live in `~/.hermes/.env` while non-secret settings live in `~/.hermes/config.yaml`, best edited with `hermes config set <KEY> <value>`, and failures are diagnosed in order with `hermes doctor`, `hermes model`, `hermes setup`, `hermes sessions list`, `hermes --continue`, `hermes gateway status`.

## 2. [[wiki/02-configuration-providers-cli|Configuration, Providers, and CLI]]

**In one sentence:** Hermes Agent stores non-secret settings in `~/.hermes/config.yaml` and secrets in `~/.hermes/.env`, connects to 40+ models through Nous Portal, API keys, OAuth, or custom endpoints, and is operated through `hermes` CLI/TUI commands with SQLite-backed sessions.

- `~/.hermes/config.yaml` holds all non-secret settings while `~/.hermes/.env` holds API keys, tokens, and passwords, with `hermes config set` routing values automatically and CLI args overriding both.
- `hermes model` is the full provider setup wizard, `/model` inside chat only switches between already-configured providers, and `hermes tools`, `hermes config`, and `hermes doctor` manage tools, settings, and diagnostics.
- Nous Portal via `hermes setup --portal` is the recommended path, giving one OAuth login for 300+ models plus Tool Gateway search, image, TTS, and browser tools.
- Provider breadth includes OpenRouter, Anthropic, OpenAI, Gemini, Vertex AI, Bedrock, Copilot, xAI, Fireworks, NovitaAI, DeepSeek, Hugging Face, Ollama Cloud, LM Studio, vLLM, and any OpenAI-compatible custom endpoint.
- Local and self-hosted models require at least 64K context, which for Ollama must be set server-side via `OLLAMA_CONTEXT_LENGTH`, systemd config, or Modelfile since it cannot be set through the chat API.
- Classic CLI (`hermes`, `hermes chat -q`, `hermes --continue`) is line-oriented with slash commands and `!` shell mode, while `hermes --tui` provides modal overlays, mouse selection, and non-blocking input.
- Sessions persist in `~/.hermes/state.db` with resume by ID, title, or `latest`, automatic context compression, background `/bg` tasks, and disposable git worktrees via `hermes -w`.

## 3. [[wiki/03-memory-skills-learning-loop|Memory, Skills, and the Learning Loop]]

**In one sentence:** Hermes Agent remembers with two tiny curated files (MEMORY.md for facts, USER.md for user profile) plus searchable session history, learns procedures as on-demand skills it writes itself, and improves after every turn through a background review loop with optional human approval.

- Built-in memory is two files in `~/.hermes/memories/` — MEMORY.md (agent notes: environment facts, conventions, lessons, 2,200 chars) and USER.md (user profile: preferences, style, 1,375 chars) — injected as a frozen snapshot into the system prompt at session start.
- The agent manages memory itself with the `memory` tool (`add`, `replace`, `remove` via unique-substring matching, no `read` action since memory is already in context), and writes that would overflow the limit fail loudly so the agent consolidates entries instead of silently dropping them.
- Session search (`session_search` tool, SQLite FTS5 over `~/.hermes/state.db`) gives unlimited recall of past conversations at ~20ms per query with zero token cost until searched, complementing the small always-loaded memory.
- After each turn a background self-improvement review replays the conversation and may save memories or patch skills, announced by a `💾 Memory updated` line; it can run on a cheaper model, be deferred on local-GPU machines, disabled, or gated behind approval.
- `memory.write_approval: true` stages every memory write for review (`/memory pending`, `/memory approve`, `/memory reject`), and the `/journey` timeline (`hermes journey`) visualizes everything learned with list/edit/delete pruning.
- Skills are on-demand knowledge documents in `~/.hermes/skills/` following progressive disclosure (index ~3k tokens, full content only when needed), usable as slash commands, stackable up to 5 per message, and groupable into YAML bundles.
- The agent creates and patches its own skills via `skill_manage` (procedural memory: lessons not logs), installable from 8 hub sources (official, skills.sh, well-known endpoints, GitHub taps, ClawHub, LobeHub, browse.sh, direct URL) with security scanning, and background-maintained by the Curator; 8 external memory providers (Mem0, Honcho, OpenViking, Hindsight, Holographic, RetainDB, ByteRover, Supermemory) add deeper recall alongside built-in memory.

## 4. [[wiki/04-messaging-gateway-bot-mode|Messaging Gateway and Bot Mode]]

**In one sentence:** Hermes runs one gateway process that connects 20+ messaging platforms at once, while Bot Mode provides a roster of named specialist Bots with their own model, memory, skills, routines, and group-chat collaboration.

- Hermes messaging gateway connects 20+ platforms from one background process, including Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, Email, SMS, DingTalk, Feishu, WeCom, Weixin, QQ Bot, Yuanbao, BlueBubbles, Home Assistant, Teams, Google Chat, LINE, ntfy, SimpleX, IRC, and webhooks.
- Setup starts with `hermes gateway setup` for interactive configuration, then `hermes gateway`, `hermes gateway install`, `hermes gateway start`, `hermes gateway stop`, and `hermes gateway status` for running and service management.
- Bot Mode turns Hermes profiles into a roster of named Bots, where each Bot has its own chat, role, model pin, memory, skills, toolsets, SOUL.md persona, and avatar.
- Bots run recurring routines as namespaced cron jobs in the form `[bot:<name>] <routine>`, visible in both the Routines pane and `hermes cron list`.
- Group chats hold 2--6 Bots that coordinate in serial rounds, pull each other in with @mentions, escalate with @user, and show a needs-you badge when human judgment is required.
- Bot-to-bot messaging uses @mentions resolved against the live roster plus direct `message_agent` calls with automatic sender attribution, and cross-machine delivery works through Desktop relay or `hermes peer` links.
- For always-on service setup, Linux uses systemd user service plus `sudo loginctl enable-linger $USER` or a boot-time system service, while macOS uses a launchd agent, and `platforms.<name>.enabled: false` in config always wins over leftover credentials.

## 5. [[wiki/05-tools-integrations-mcp|Tools, Integrations, and MCP]]

**In one sentence:** Hermes Agent ships 60+ built-in tools grouped into enable/disable toolsets with 7 terminal backends, connects external capabilities through MCP servers and the Nous Portal subscription with its managed Tool Gateway, and covers voice, browser, vision, image generation, TTS, and web search providers.

- Hermes organizes 60+ built-in tools into toolsets such as `web`, `terminal`, `file`, `browser`, `vision`, `image_gen`, `tts`, `memory`, `cronjob`, `code_execution`, and `delegation`, selectable per run with `hermes chat --toolsets "web,terminal"` and configured with `hermes tools`.
- The terminal tool supports 7 backends -- `local`, `docker`, `ssh`, `singularity`, `modal`, `daytona`, and `vercel_sandbox` -- with container defaults of 1 CPU, 5120 MB memory, 51200 MB disk, and persistent filesystems when `container_persistent: true`.
- Nous Portal at portal.nousresearch.com provides one OAuth login and one bill for 300+ models including Claude Sonnet 4.6, GPT-5.5 Pro, Gemini 3 Pro Preview, and DeepSeek V4 Pro, set up with `hermes setup --portal`.
- The Nous Tool Gateway routes 5 categories through managed infrastructure -- Firecrawl web search and extract, FAL image generation with 9 models, OpenAI TTS, Browser Use cloud browsers, and Modal cloud terminals -- enabled per tool with the value `nous` in config.
- MCP servers are declared under `mcp_servers` in `~/.hermes/config.yaml` as stdio servers with `command` plus `args` plus `env` or as HTTP servers with `url` plus `headers` plus `auth: oauth`, registered with the prefix `mcp_<server>_<tool>` and a runtime toolset named `mcp-<server>`.
- MCP exposure is controlled with `enabled: false`, `tools.include` whitelists, `tools.exclude` blacklists with fnmatch globs, and `tools.prompts: false` plus `tools.resources: false`, where `include` wins when both lists match.
- Voice mode works in CLI plus Telegram plus Discord, started with `/voice on` and toggled with Ctrl+B, using OpenAI TTS through the gateway or a direct TTS provider key.
- Web search defaults to Firecrawl through the gateway or a direct Firecrawl key, with self-hosted SearXNG supported as an alternative backend selected in `hermes tools` via `web.backend`.

## 6. [[wiki/06-automation-security-architecture|Automation, Security, and Architecture]]

**In one sentence:** Hermes combines built-in cron scheduling, subagent delegation with programmatic code execution, checkpoint rollback, layered security, and a modular agent-gateway architecture that also supports batch research and RL (Reinforcement Learning) training.

- Built-in cron runs one-shot or recurring agent tasks via a single `cronjob` tool with natural-language or cron-expression schedules and full pause, resume, edit, trigger, and remove lifecycle.
- Cron jobs run in fresh isolated agent sessions on a 60-second gateway tick, support skill attachment, project workdir, model pinning, preflight validation, and delivery to origin chat, local files, or any connected platform.
- `delegate_task` spawns child subagents with fresh context and inherited toolsets for single or parallel work, while `execute_code` handles mechanical multi-step pipelines with lower token cost.
- Checkpoints and rollback use shadow git repos plus snapshots so destructive or exploratory work can be reviewed and reverted.
- Security is defense-in-depth across eight layers including command approval, user authorization, file-write guards, container isolation, credential filtering, and injection scanning.
- A hardline blocklist of catastrophic commands can never be overridden, even in YOLO (You Only Look Once, auto-approve-all) mode or headless cron approval modes.
- One platform-agnostic `AIAgent` core serves CLI, gateway, ACP (Agent Client Protocol, IDE integration), batch, and API entry points with shared prompt building, provider resolution, and tool dispatch.
- Batch processing, trajectory export, and Atropos integration make agent runs reusable as research data and RL training material.

## The argument in five moves

1. Install with one command and connect a model (Portal OAuth is fastest).
2. Remember cheaply: tiny always-loaded memory plus free searchable history.
3. Learn procedurally: the agent writes skills, a background review compounds them, humans gate what lands.
4. Reach everywhere: one gateway process, 20+ chat platforms, specialist bots that collaborate.
5. Act safely unattended: scoped toolsets, isolated cron sessions, checkpoints with rollback, layered security.
