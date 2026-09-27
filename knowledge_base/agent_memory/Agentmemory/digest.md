> [[index|Wiki]] | [[summary|Summary]]
# rohitg00/agentmemory — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** agentmemory is persistent memory for AI coding agents, built on the iii engine and shared across agents via MCP, hooks, and REST with no external databases.
## Key points
- Provides persistent memory for coding agents so they "remember everything" with "no more re-explaining" (README.md:13).
- Supports Claude Code, GitHub Copilot CLI, Cursor, Gemini CLI, Codex CLI, Hermes, OpenClaw, pi, OpenCode, and any MCP client (README.md:16).
- Is built on the iii engine, specifically pinned iii-engine v0.22.1 (README.md:16, README.md:147).
- Advertises 95.2% retrieval R@5, 92% fewer tokens, 54 MCP tools, 12 auto hooks, 0 external DBs, and 1,674+ tests passing (README.md:54-59).
- Installs canonically via `npx -y @agentmemory/agentmemory@latest`, which runs interactive setup that seeds config and starts the memory server plus its pinned iii engine (README.md:95, README.md:98).
- Runs keyless by default with BM25 recall (`memory_recall` / `mem::search` path); free on-device semantic recall requires `EMBEDDING_PROVIDER=local` (README.md:100).
- Shares one memory server across all agents via hooks, MCP, or REST API, with more agents wired any time via `agentmemory connect <agent>` (README.md:155, README.md:117).

## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** Top-level files define agentmemory's runtime configuration, build/test pipeline, contributor governance, and install runbooks — everything outside `src/`, `plugin/`, and `integrations/`.
## Key points
- `.env.example` is the commented configuration template copied to `~/.agentmemory/.env` by `init`, with every line OFF by default so the daemon runs keyless with no LLM key, embedding key, or API auth (`.env.example:1-18`).
- LLM detection wins in priority order `OPENAI_API_KEY → MINIMAX_API_KEY → ANTHROPIC_API_KEY → GEMINI_API_KEY → OPENROUTER_API_KEY → noop`, and without a key the daemon runs in noop mode with zero-LLM synthetic compression plus BM25 recall (`.env.example:24-37`).
- Embedding detection order is `EMBEDDING_PROVIDER` override → `GEMINI_API_KEY` → `OPENAI_API_KEY` → `VOYAGE_API_KEY` → `COHERE_API_KEY` → `OPENROUTER_API_KEY` → BM25-only, with `EMBEDDING_PROVIDER=local` opting into on-device `Xenova/all-MiniLM-L6-v2` (`.env.example:80-84`).
- `iii-config.yaml` (loopback `127.0.0.1`, `./data/state_store.db`) and `iii-config.docker.yaml` (`0.0.0.0`, `/data/state_store.db`, env-substituted ports) declare the same iii-engine workers: `iii-http`, `iii-state`, `iii-queue`, `iii-pubsub`, `iii-cron`, `iii-stream`, `iii-observability` (`iii-config.yaml:1-10`, `iii-config.docker.yaml:1-10`).
- `AGENTS.md` pins the stack to iii-sdk 0.22.1 over WebSocket on port 49134, TypeScript→ESM via tsdown to `dist/`, vitest with 1,596+ tests, and mandatory multi-file update checklists for MCP tools, REST endpoints, versions, KV scopes, and audit ops (`AGENTS.md:4-10`, `AGENTS.md:11-33`).
- `INSTALL_FOR_AGENTS.md` is a step-by-step agent runbook: Node ≥20, `npx -y @agentmemory/agentmemory@latest` start, four-port validation (3111 REST/MCP, 3112 streams, 3113 viewer, 49134 engine), `demo`, `connect <agent>`, skills install, and save/recall/restart persistence check (`INSTALL_FOR_AGENTS.md:1-8`, `INSTALL_FOR_AGENTS.md:68-74`).
- Governance is split across `GOVERNANCE.md` (Linux Foundation MVG, lazy-consensus PRs, `governance`/`breaking` issue flows), `MAINTAINERS.md` (single active maintainer Rohit Ghumare since 2026-01), `ROADMAP.md` (Q2 2026–Q1 2027 Depth/Breadth/Trust/v1.0), and `SECURITY.md` (GHSA-first reporting, supported-version table, no-lockfile supply-chain stance) (`GOVERNANCE.md:5-6`, `MAINTAINERS.md:7-9`, `ROADMAP.md:18-23`, `SECURITY.md:27-32`).
- Build/test wiring is `tsconfig.json` (ES2022/ESNext/bundler, `rootDir src`, `outDir dist`, strict with `noUnusedLocals`/`noUnusedParameters`, excludes `test` and `src/hooks`), `tsdown.config.ts` (ESM/node20 entries for `src/index.ts`, `src/cli.ts`, `src/mcp/standalone.ts` plus 14 hook entries dual-emitted to `dist/hooks` and `plugin/scripts`), and `vitest.config.ts` (sandboxed `HOME`/`USERPROFILE` under a throwaway tmpdir so tests never read the developer's real `~/.agentmemory/.env`) (`tsconfig.json:1-21`, `tsdown.config.ts:1-16`, `vitest.config.ts:1-12`).

## The system in five moves
1. agentmemory positions itself as persistent, shared memory for coding agents so they stop needing re-explanation.
2. One npx install seeds config and starts the memory server plus its pinned iii engine, verified over four local ports.
3. By default it runs keyless with BM25 recall, with opt-in local or provider-backed embeddings and LLM compression.
4. All agents share the same server through hooks, MCP, or REST, extended any time via `connect <agent>`.
5. Top-level files pin the runtime contract — env defaults, engine configs, build/test wiring — plus governance, roadmap, and security.
6. Mandatory multi-file checklists and sandboxed tests keep the MCP/REST surface, versions, and state schema consistent.
