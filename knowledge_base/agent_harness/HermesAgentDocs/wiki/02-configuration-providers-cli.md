> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Configuration, Providers, and CLI
**In one sentence:** Hermes Agent stores non-secret settings in `~/.hermes/config.yaml` and secrets in `~/.hermes/.env`, connects to 40+ models through Nous Portal, API keys, OAuth, or custom endpoints, and is operated through `hermes` CLI/TUI commands with SQLite-backed sessions.
## Key points
- `~/.hermes/config.yaml` holds all non-secret settings while `~/.hermes/.env` holds API keys, tokens, and passwords, with `hermes config set` routing values automatically and CLI args overriding both.
- `hermes model` is the full provider setup wizard, `/model` inside chat only switches between already-configured providers, and `hermes tools`, `hermes config`, and `hermes doctor` manage tools, settings, and diagnostics.
- Nous Portal via `hermes setup --portal` is the recommended path, giving one OAuth login for 300+ models plus Tool Gateway search, image, TTS, and browser tools.
- Provider breadth includes OpenRouter, Anthropic, OpenAI, Gemini, Vertex AI, Bedrock, Copilot, xAI, Fireworks, NovitaAI, DeepSeek, Hugging Face, Ollama Cloud, LM Studio, vLLM, and any OpenAI-compatible custom endpoint.
- Local and self-hosted models require at least 64K context, which for Ollama must be set server-side via `OLLAMA_CONTEXT_LENGTH`, systemd config, or Modelfile since it cannot be set through the chat API.
- Classic CLI (`hermes`, `hermes chat -q`, `hermes --continue`) is line-oriented with slash commands and `!` shell mode, while `hermes --tui` provides modal overlays, mouse selection, and non-blocking input.
- Sessions persist in `~/.hermes/state.db` with resume by ID, title, or `latest`, automatic context compression, background `/bg` tasks, and disposable git worktrees via `hermes -w`.
---
## Config file layout and key settings
All state lives under `~/.hermes/` with `config.yaml` for settings, `.env` for secrets, `auth.json` for OAuth credentials, `SOUL.md` for agent identity, plus `memories/`, `skills/`, `cron/`, `sessions/`, and `logs/`.
Resolution order is CLI args first, then `config.yaml`, then `.env`, then built-in defaults, with `config.yaml` winning for non-secrets and `.env` required for secrets.
Useful management commands are `hermes config`, `hermes config edit`, `hermes config get KEY`, `hermes config set KEY VAL`, `hermes config unset KEY`, `hermes config check`, and `hermes config migrate`.
`config.yaml` supports `${VAR_NAME}` and `${env:VAR_NAME}` substitution against process env or profile `.env`, and terminal backends include `local`, `docker`, `ssh`, `modal`, `daytona`, `vercel_sandbox`, and `singularity`.
Key sections cover `model`, `auxiliary`, `terminal`, `compression`, `database`, `updates`, `display`, `skills`, and `quick_commands`, with managed org scope able to pin values via [[01-overview-installation-desktop|Overview]].
## CLI commands reference
Base invocation `hermes` starts interactive chat, `hermes chat -q "..."` runs one non-interactive query, `hermes chat --query-file` reads prompts verbatim from file or stdin, and flags select `--model`, `--provider`, `--toolsets`, and `-s` for preloaded skills.
`hermes --tui` launches the modern TUI described in [[03-tui-desktop-gateway-bot|TUI Desktop]], while classic CLI offers status bar, `/status`, `/context`, `/usage`, personalities, multiline input, `Ctrl+C` redirect, `busy_input_mode`, and `!` shell mode for zero-token shell commands.
`hermes --continue` or `-c` resumes the latest CLI session, `hermes --resume <id|title|latest>` resumes a specific session, and `--in ./dir` scopes to a workspace directory.
`hermes model` adds providers, runs OAuth, enters keys, and configures endpoints; `hermes tools` enables or disables toolsets; `hermes setup --portal` does OAuth plus provider plus gateway in one step.
`hermes doctor` checks backends, keys, and retired models such as xAI Grok retirements with `hermes migrate xai --apply`; `hermes update` updates installs with `updates.pre_update_backup`, `backup_keep`, and stash or discard handling for dirty trees.
Gateway operations use `hermes gateway`, `hermes serve`, `hermes sessions list`, `hermes sessions rename`, `hermes plugins`, and `hermes worktree list/prune`, with full command tables in [[05-reference-glossary|Reference]].
Slash commands include `/help`, `/model`, `/tools`, `/skills browse`, `/bg`, `/btw`, `/sessions`, `/title`, `/voice`, `/reasoning`, and skill or `quick_commands` shortcuts defined in `config.yaml`.
## Provider catalog and setup modes
Quick mode is `hermes setup --portal` for fresh installs, creating provider plus Tool Gateway routing plus subscription billing without YAML edits, inspected later with `hermes portal info`.
Full mode is `hermes model` for existing installs, walking through OAuth providers like Nous Portal, Anthropic, Copilot, Codex, Vertex, Bedrock, Ollama Cloud, Qwen OAuth, MiniMax OAuth, and xAI OAuth, or API-key providers via `.env` entries such as `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `DEEPSEEK_API_KEY`, `FIREWORKS_API_KEY`, `NOVITA_API_KEY`, `HF_TOKEN`, `NVIDIA_API_KEY`, and `XAI_API_KEY`.
Blank Slate mode is manual editing of `model.provider`, `model.default`, `model.base_url`, and `bedrock` or `vertex` blocks in `config.yaml`, plus auxiliary overrides for vision, compression, and summarization models.
Subscription semantics vary: Anthropic OAuth needs Max plus extra credits, Copilot needs OAuth or `COPILOT_GITHUB_TOKEN` rather than classic `ghp_` tokens, and xAI OAuth reuses one bearer for inference plus TTS, image, video, and search tools.
Advanced routing uses fallback chains, credential pools, provider routing, and per-provider `request_timeout_seconds` and `stale_timeout_seconds` with per-model overrides.
## Custom endpoints and local models
Any OpenAI-compatible `/v1/chat/completions` server works as `provider: custom` with `base_url`, `default` model name, and optional `api_key`, configured via `hermes model` Custom endpoint choice or direct `config.yaml` edits.
Local patterns include Ollama at `http://localhost:11434/v1`, vLLM with `--enable-auto-tool-choice` and `--tool-call-parser`, LM Studio, llama.cpp, and remote GPU servers over SSH or cloud sandboxes.
Named custom providers allow `/model custom:local:qwen-2.5` switching, `/model custom` auto-detects single-model endpoints via `/models`, and switching away from custom clears stale `base_url`.
Ollama defaults to 4K to 32K context on low VRAM hosts and must be raised to 64K minimum via server env, systemd override, or Modelfile `PARAMETER num_ctx 64000`, verified with `ollama ps`.
vLLM context comes from `max_position_embeddings` or `--max-model-len`, tool calling needs explicit parser flags, and small 32K local models may need reduced toolsets such as `-t file,web` to leave room for system prompt plus tools.
## Sessions management
CLI sessions store metadata, messages, lineage, and full-text search in `~/.hermes/state.db`, with exit summaries printing resume ID, duration, and message counts.
Resume restores full history including tool calls, shows a Previous Conversation recap panel, and supports naming via `/title` or `hermes sessions rename`.
Compression triggers at `compression.threshold` by default 0.50, preserves first 3 and last 20 turns, and can pin a cheap auxiliary model under `auxiliary.compression.model`.
Background sessions via `/bg <prompt>` spawn isolated daemon sessions inheriting model and provider but not history, reporting completion panels plus optional bell and active-task counts in the status bar.
Worktree sessions via `hermes -w` create disposable trees under `<repo>/.worktrees/`, pruned conservatively by `hermes worktree prune` without deleting tracked changes, unique unpushed commits, in-use trees, or unarchived untracked scratch.
**Covers:** user-guide/configuration, user-guide/cli, integrations/providers (docs site, retrieved 2026-09-08)
