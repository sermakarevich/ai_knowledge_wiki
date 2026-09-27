[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** agentmemory is persistent memory for AI coding agents, built on the iii engine and shared across agents via MCP, hooks, and REST with no external databases.
## Key points
- Provides persistent memory for coding agents so they "remember everything" with "no more re-explaining" (README.md:13).
- Supports Claude Code, GitHub Copilot CLI, Cursor, Gemini CLI, Codex CLI, Hermes, OpenClaw, pi, OpenCode, and any MCP client (README.md:16).
- Is built on the iii engine, specifically pinned iii-engine v0.22.1 (README.md:16, README.md:147).
- Advertises 95.2% retrieval R@5, 92% fewer tokens, 54 MCP tools, 12 auto hooks, 0 external DBs, and 1,674+ tests passing (README.md:54-59).
- Installs canonically via `npx -y @agentmemory/agentmemory@latest`, which runs interactive setup that seeds config and starts the memory server plus its pinned iii engine (README.md:95, README.md:98).
- Runs keyless by default with BM25 recall (`memory_recall` / `mem::search` path); free on-device semantic recall requires `EMBEDDING_PROVIDER=local` (README.md:100).
- Shares one memory server across all agents via hooks, MCP, or REST API, with more agents wired any time via `agentmemory connect <agent>` (README.md:155, README.md:117).
---
## Purpose and positioning
Persistent memory for coding agents, tagline "Your coding agent remembers everything. No more re-explaining." (README.md:13). Built on the [iii engine](https://github.com/iii-hq/iii) (README.md:16). Extends "Karpathy's LLM Wiki pattern with confidence scoring, lifecycle, knowledge graphs, and hybrid search" — "agentmemory is the implementation" (README.md:44).

Claimed stats (README.md:54-59):

| Claim | Value |
|---|---|
| Retrieval R@5 | 95.2% |
| Token reduction | 92% fewer tokens |
| MCP tools | 54 |
| Auto hooks | 12 |
| External DBs | 0 |
| Tests | 1,674+ passing |

## Install and setup
Requirements (README.md:88-90):

- Node.js 20 or newer with npm and npx (`node -v`, `npm -v`, `npx -v`).
- macOS/Linux automatic iii-engine install also needs `curl`, POSIX `sh`, `tar` (minimal `node:20-slim` images may lack them).
- Native Windows requires pinned iii-engine v0.22.1 `iii.exe` installed manually; WSL2 or Docker Desktop are the other supported paths.

Canonical fresh-install command (README.md:95):

```bash
npx -y @agentmemory/agentmemory@latest
```

First run is interactive: pick agents to wire (Claude Code, Cursor, Codex, Gemini CLI, OpenCode, ...), pick an LLM provider or stay keyless; it seeds config, starts the memory server and pinned iii engine, and offers a global install so bare `agentmemory` works everywhere (README.md:98). `-y` accepts the npx package prompt and `@latest` avoids a stale cached release (README.md:98). LLM-written observation compression starts only when `AGENTMEMORY_AUTO_COMPRESS=true` is also set (README.md:98).

Verify plus skills (README.md:106-109):

```bash
npx -y @agentmemory/agentmemory@latest demo  # seed sample sessions + exercise recall
npx skills add rohitg00/agentmemory -y   # 17 native skills so your agent knows when to reach for memory
```

Keyword searches hit in default keyless mode through BM25; the demo's `database performance optimization` query is intentionally semantic and can return zero until an embedding provider is configured (README.md:111). Agent-driven install instruction (README.md:115):

> Retrieve and follow the instructions at: https://raw.githubusercontent.com/rohitg00/agentmemory/main/INSTALL_FOR_AGENTS.md

Extra install notes in chunk: Windows fast path is WSL2 with manual v0.22.1 ZIP extraction for native (README.md:122); global install via `npm install -g @agentmemory/agentmemory@latest` but npx remains canonical (README.md:130-133); stale npx cache fixed with `npx -y @agentmemory/agentmemory@latest` or `rm -rf ~/.npm/_npx` (README.md:140); won't attach to a non-v0.22.1 iii engine — stop the other engine, binary lives in `~/.agentmemory/bin` (README.md:147).

## Runtime, ports and state
Keyless mode disables vector embeddings: `memory_recall` (the `mem::search` path) uses BM25, while `memory_smart_search` can also fuse structural graph matches when graph data already exists (README.md:100). Free on-device semantic recall: set `EMBEDDING_PROVIDER=local` in `~/.agentmemory/.env` and restart; first embedding request downloads `Xenova/all-MiniLM-L6-v2`, inference runs locally after that (README.md:100).

Local runtime ports (README.md:102):

| Port | Use |
|---|---|
| `3111` | REST/MCP HTTP |
| `3112` | iii streams |
| `3113` | viewer |
| `49134` | iii worker WebSocket |

Persistent iii state locations (README.md:102):

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/agentmemory` |
| Linux | `$XDG_DATA_HOME/agentmemory` or `~/.local/share/agentmemory` |
| Windows | `%APPDATA%\agentmemory` |

Override with `--data-dir <path>` or `AGENTMEMORY_DATA_DIR`, reused on every restart (README.md:102). For backward compatibility an existing `./data/state_store.db` or `./data/iii-config.yaml` takes precedence over the platform default for instance 0; explicit flag or env override still wins (README.md:102).

## Agent compatibility
Works with "any agent that supports hooks, MCP, or REST API" and "all agents share the same memory server" (README.md:155). Wire more agents any time (README.md:117):

```bash
agentmemory connect <agent>
```

Adapters visible before truncation include Claude Code ("native plugin + 12 hooks + MCP"), Codex CLI ("native plugin + 6 hooks + MCP"), GitHub Copilot CLI ("MCP + plugin hooks/skills"), OpenClaw, Hermes, pi (each "native plugin + MCP"), OpenHuman ("native Memory trait backend"), Cursor ("native plugin + MCP"), Gemini CLI ("MCP server"), OpenCode ("22 hooks + MCP + plugin") (README.md:160-210). The chunk truncates mid-row on the Cline entry at `<strong>Cline</s` (README.md:213); remaining agents table rows and any content after line 214 were cut, so they are not covered here.

**Covers:** `README.md` (repo overview, install, runtime ports/state, agent-compatibility table as far as preserved in chunk)
