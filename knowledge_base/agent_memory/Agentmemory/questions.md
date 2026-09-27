---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: rohitg00/agentmemory

### Q1. What is agentmemory in one sentence, and which agents and interfaces does it share memory across?
> [!tip]- Answer
> Agentmemory is persistent memory for AI coding agents, built on the pinned iii engine v0.22.1 and shared across agents with no external databases.
> It supports Claude Code, Copilot CLI, Cursor, Gemini CLI, Codex CLI, Hermes, OpenClaw, pi, OpenCode, and any MCP client via hooks, MCP, or REST, with more agents wired any time via `agentmemory connect <agent>`. See [[wiki/01-overview|Overview]].

### Q2. What is the canonical install command, and what happens on first run?
> [!tip]- Answer
> The canonical command is `npx -y @agentmemory/agentmemory@latest`, where `-y` accepts the npx prompt and `@latest` avoids a stale cached release.
> First run is interactive: pick agents to wire and an LLM provider or stay keyless, then it seeds config, starts the memory server plus its pinned iii engine, and offers a global install; verify with `demo` and `npx skills add rohitg00/agentmemory -y`. See [[wiki/01-overview|Overview]].

### Q3. How does keyless recall work, and what are the four local ports plus state locations?
> [!tip]- Answer
> Keyless mode disables vector embeddings: `memory_recall` (the `mem::search` path) uses BM25, while `memory_smart_search` can fuse structural graph matches when graph data exists, and free on-device semantic recall requires `EMBEDDING_PROVIDER=local` with its first-request `Xenova/all-MiniLM-L6-v2` download.
> Ports are 3111 REST/MCP HTTP, 3112 iii streams, 3113 viewer, and 49134 iii worker WebSocket, with state under macOS `~/Library/Application Support/agentmemory`, Linux `$XDG_DATA_HOME` or `~/.local/share/agentmemory`, or Windows `%APPDATA%`, overridable via `--data-dir` or `AGENTMEMORY_DATA_DIR`. See [[wiki/01-overview|Overview]].

### Q4. What does `.env.example` configure by default, and what are the LLM and embedding detection orders?
> [!tip]- Answer
> It is the commented template copied to `~/.agentmemory/.env` by `init`, with every line OFF by default so the daemon runs keyless with no LLM key, embedding key, or API auth.
> LLM priority is `OPENAI_API_KEY → MINIMAX_API_KEY → ANTHROPIC_API_KEY → GEMINI_API_KEY → OPENROUTER_API_KEY → noop`, and embedding priority is `EMBEDDING_PROVIDER` override → `GEMINI_API_KEY` → `OPENAI_API_KEY` → `VOYAGE_API_KEY` → `COHERE_API_KEY` → `OPENROUTER_API_KEY` → BM25-only, with `local` opting into on-device MiniLM. See [[wiki/02-top-level-files|Top-level-files]].

### Q5. How do the native and Docker iii-engine configs differ while declaring the same workers?
> [!tip]- Answer
> Both declare the same workers — `iii-http`, `iii-state`, `iii-queue`, `iii-pubsub`, `iii-cron`, `iii-stream`, and `iii-observability` — but native `iii-config.yaml` binds loopback `127.0.0.1` with fixed ports and `./data/state_store.db`, while `iii-config.docker.yaml` binds `0.0.0.0` with env-substituted ports and `/data/state_store.db`.
> Native also includes a dev-reload `iii-exec` worker watching `src/**/*.ts`, which Docker omits. See [[wiki/02-top-level-files|Top-level-files]].

### Q6. What do `AGENTS.md`, `INSTALL_FOR_AGENTS.md`, and the governance files pin down for contributors?
> [!tip]- Answer
> `AGENTS.md` pins iii-sdk 0.22.1 over WebSocket on port 49134, TypeScript→ESM via tsdown to `dist/`, vitest with 1,596+ tests, and mandatory multi-file checklists for MCP tools, REST endpoints, versions, KV scopes, and audit ops.
> `INSTALL_FOR_AGENTS.md` is the agent runbook from Node ≥20 through four-port validation, `demo`, `connect <agent>`, and a save/recall/restart check, while governance splits across `GOVERNANCE.md` (MVG lazy consensus), `MAINTAINERS.md` (single maintainer Rohit Ghumare since 2026-01), `ROADMAP.md` (Q2 2026–Q1 2027), and `SECURITY.md` (GHSA-first reporting). See [[wiki/02-top-level-files|Top-level-files]].

### Q7. Should a small team adopt agentmemory as its shared coding-agent memory today?
> [!tip]- Answer
> Recommend it only if the team accepts single-maintainer governance, a strict pinned iii-engine v0.22.1, and keyless BM25-only recall unless they opt into local or provider embeddings and doubly-gated LLM compression.
> Its strengths are zero-external-DB local-first sharing across many agents with documented runbooks and sandboxed tests, but teams needing managed recall quality, SSO/RBAC, or multi-maintainer assurance should wait for the Trust and v1.0 roadmap items. See [[wiki/02-top-level-files|Top-level-files]].
