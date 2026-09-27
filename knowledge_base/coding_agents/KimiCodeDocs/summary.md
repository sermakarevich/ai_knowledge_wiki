# Kimi Code Documentation

**Source:** [Kimi Code Docs](https://www.kimi.com/code/docs/en/)

## Human Readable TL;DR

Kimi Code is Moonshot AI's answer to Claude Code -- a terminal app (plus a VS Code extension) that lets an AI agent read your files, edit them, and run commands on your behalf. It ships as a free perk of a Kimi membership, talks to Moonshot's own "Kimi" models by default, but can be pointed at Claude, GPT, or Gemini instead. Think of it as a coding assistant that lives in your terminal, remembers project context across sessions, and can be taught new tricks via small "skill" files or by plugging in external tools (MCP servers).

## TL;DR

Kimi Code CLI is a terminal-based AI coding agent (Rust/Node-distributed, installed via curl script or npm) analogous to Claude Code / Codex CLI. It authenticates via OAuth or API key, configures models/providers through a TOML file (`~/.kimi-code/config.toml`) supporting six provider backends (kimi, anthropic, openai, openai_responses, google-genai, vertexai), and extends via MCP servers (`mcp.json`), Agent Skills (Markdown + YAML frontmatter), and plugins. It also ships a VS Code extension. The managed Kimi service offers up to 100 tokens/s output and 300-1,200 requests per 5-hour rolling window, refreshed every 7 days.

---

## Problem & Motivation

Developers using LLM-based coding agents want a terminal-native tool that can read/edit code and run commands autonomously, without being locked to one model vendor. Kimi Code positions itself as Moonshot AI's entry in this space (competing with Claude Code, Codex CLI, Gemini CLI), differentiated by being bundled free into Kimi's consumer/subscription membership and by explicit "broad compatibility" with other agents' ecosystems (it can proxy to Anthropic/OpenAI/Google models, and its API is also consumable from *other* coding agents via OpenAI- and Anthropic-compatible endpoints).

---

## Main Original Ideas (Product & Design Choices)

1. **Membership-bundled quota model.** Kimi Code access rides on the same quota pool as Kimi chat membership -- a rolling 7-day refresh window (300-1,200 requests / 5 hours, up to 30 concurrent) rather than pay-per-token billing for the managed tier.

2. **Provider-agnostic core with six backend types.** `kimi`, `anthropic`, `openai`, `openai_responses`, `google-genai`, `vertexai` are all first-class in `config.toml`, each with auto-detected capabilities (thinking, vision, tool-use) matched by model name -- so switching from Kimi's own models to Claude/GPT/Gemini is a config edit, not a fork.

3. **TOML-based long-term config with layered scopes.** User config (`~/.kimi-code/config.toml`, `tui.toml`) vs. project-local (`.kimi-code/local.toml`) separates shareable team settings from machine-specific paths, echoing the `.env`/`.env.local` pattern.

4. **Agent Skills as Markdown+YAML micro-extensions.** Reusable capability packets (`SKILL.md` with `name`/`description`/`whenToUse`/`arguments`) that the model can invoke automatically (via `description` matching) or a user can invoke explicitly (`/skill:name`), scanned from four priority tiers (project, user, extra dirs, built-in).

5. **MCP-native tool extension.** The CLI is an MCP *client* -- external tools appear as `mcp__<server>__<tool>` alongside built-ins (Read, Bash, Grep), configured via `mcp.json` at user or project scope, over stdio, HTTP, or (legacy) SSE transport.

6. **Rule-based permission engine.** `[[permission.rules]]` arrays with `decision` (`allow`/`deny`/`ask`), `pattern` (tool name + arg glob, e.g. `Bash(rm -rf*)`), and `scope` (`turn-override` -> `session-runtime` -> `project` -> `user`) give fine-grained, auditable control over what the agent can execute unattended -- complemented by a blunt `--yolo` flag for trusted batch runs.

7. **Ephemeral env-var model override.** Setting `KIMI_MODEL_NAME` + `KIMI_MODEL_API_KEY` (etc.) creates an in-memory temporary provider for one run, without touching config files -- useful for CI or one-off experiments.

---

## Key Findings (Documented Capabilities)

- **Performance claims (per docs; not independently verified):** up to 100 tokens/s output; 300-1,200 requests per 5-hour window; up to 30 concurrent requests.
- **Two install paths:** official curl/PowerShell script (no Node.js prerequisite) or `npm install -g @moonshot-ai/kimi-code` (requires Node.js >= 22.19.0).
- **Session/task persistence:** background tasks and scheduled/cron-style reminders survive `kimi resume`, but expire after 7 days; sessions exportable as ZIP or Markdown transcripts.
- **Plan mode:** `kimi --plan` or `Shift-Tab` toggles a propose-before-execute mode, recommended for multi-file refactors and unfamiliar codebases.
- **Compatibility surface:** exposes both an OpenAI-compatible endpoint (`https://api.kimi.com/coding/v1`) and an Anthropic-compatible endpoint (`https://api.kimi.com/coding/`) under model id `kimi-for-coding`, so third-party agents can consume Kimi's coding model directly.
- **Config keys of note:** `default_permission_mode` (`manual`/`auto`/`yolo`), `default_plan_mode`, `merge_all_available_skills`, `extra_skill_dirs`, `telemetry` (on by default), `[loop_control]` (`max_steps_per_turn`, `max_retries_per_step`, `reserved_context_size`), `[background].max_running_tasks`, `[experimental].micro_compaction`.
- **Diagnostics:** `KIMI_LOG_LEVEL` (`off`/`error`/`warn`/`info`/`debug`), log rotation via `KIMI_LOG_GLOBAL_MAX_BYTES`/`_FILES` and session-scoped equivalents.

---

## Suggestions & Future Directions (Open Questions / Gaps in Docs)

1. Docs don't quantify pricing for usage beyond the membership quota (e.g., overage cost, standalone API pricing tier).
2. No mention of offline/local-model support (e.g., Ollama) -- all six provider types are cloud APIs.
3. Security guidance for MCP is present but generic ("connect only to trusted servers"); no sandboxing details for stdio-launched MCP child processes.
4. `KIMI_CODE_AGENT_SWARM_MAX_CONCURRENCY` env var hints at a multi-agent/swarm feature not otherwise documented on the pages crawled here -- worth a follow-up deep dive if relevant.
5. VS Code extension docs (`kimi-code-for-vscode/*`) and `third-party-tools/other-coding-agents.html` were linked but not fetched in this pass -- candidates for a `--deep` follow-up.

---

## Product & Source

Moonshot AI ("Kimi"). Docs crawled: overview page (`/code/docs/en/`), CLI getting-started, configuration (config-files, providers, env-vars), customization (MCP, Agent Skills), and use-cases guide.
