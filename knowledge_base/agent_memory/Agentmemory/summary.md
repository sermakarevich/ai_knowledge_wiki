# Technical Analysis: rohitg00/agentmemory

**Repository:** https://github.com/rohitg00/agentmemory
**Version analyzed:** unknown
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Coding agents lose context between sessions, forcing repeated explanation of decisions, conventions, and prior work (README.md:13). agentmemory addresses this with a persistent, local-first memory server shared across agents via hooks, MCP, or REST (README.md:155). The primary user is a developer running one or more coding agents (Claude Code, Cursor, Codex CLI, Gemini CLI, Copilot CLI, OpenCode, and others) who wants observations recorded once and recalled automatically (README.md:16, README.md:160-210). Implementation is delegated to the iii engine (pinned v0.22.1), extending the LLM Wiki pattern with confidence scoring, lifecycle, knowledge graphs, and hybrid search (README.md:16, README.md:44, README.md:147). Claimed characteristics from the overview page: 95.2% retrieval R@5, 92% fewer tokens, 54 MCP tools, 12 auto hooks, 0 external DBs, 1,674+ tests passing (README.md:54-59); the contributor page cites a v0.9.29 snapshot of 54 MCP tools, 132 REST endpoints, 6 resources, 3 prompts, 12 hooks, 17 skills, 260+ functions, 1,596+ tests (AGENTS.md:118-126). The version discrepancy reflects two snapshot points in the wiki, not independent verification. Coverage note: the available wiki pages document top-level configuration, install, runtime, and governance only; `src/`, `plugin/`, and `integrations/` internals are not covered.

## 2. High-Level Architecture

```text
coding agents (Claude Code, Cursor, Codex, Gemini CLI, Copilot CLI, OpenCode, ...)
  │ hooks (12 auto) │ MCP (54 tools) │ REST (132 endpoints)
  ▼
agentmemory server ──► iii-engine v0.22.1 (WebSocket :49134)
  │                     │ iii-http (:3111) ─ iii-state ─ iii-queue ─ iii-pubsub ─ iii-cron ─ iii-stream (:3112) ─ iii-observability
  ▼                     ▼
viewer (:3113)        file-backed state (state_store.db + stream_store)
```

Data-flow narrative:

1. Capture: agent lifecycle events invoke hooks (context-injecting vs telemetry-only per `AGENTS.md:94-98`) or explicit `memory_save` / `POST /agentmemory/remember` calls (INSTALL_FOR_AGENTS.md:128-151).
2. Compress/index: observations are indexed via zero-LLM synthetic compression in noop (keyless) mode; LLM-written compression requires a provider key plus `AGENTMEMORY_AUTO_COMPRESS=true` (`.env.example:31-35`).
3. Store: iii-engine persists KV state to `state_store.db` and streams to `stream_store` via the `iii-state` and `iii-stream` workers (`iii-config.yaml:1-10`, `iii-config.docker.yaml:1-10`).
4. Recall: keyless `memory_recall` (`mem::search` path) uses BM25; `memory_smart_search` can fuse structural graph matches when graph data exists; on-device semantic recall requires `EMBEDDING_PROVIDER=local` (README.md:100, `.env.example:80-84`).
5. Inject: hooks and MCP recall paths return context into the agent session; viewer on port 3113 exposes state for inspection (README.md:102, INSTALL_FOR_AGENTS.md:68-74).
6. Share: one memory server is shared across all wired agents; additional agents attach via `agentmemory connect <agent>` (README.md:117, README.md:155).

Persistent state lives in the iii-engine file backend, not an external database (README.md:54-59, AGENTS.md:6-8): platform defaults are `~/Library/Application Support/agentmemory` (macOS), `$XDG_DATA_HOME/agentmemory` or `~/.local/share/agentmemory` (Linux), `%APPDATA%\agentmemory` (Windows), overridable with `--data-dir` or `AGENTMEMORY_DATA_DIR` (README.md:102). Worker-level paths are `./data/state_store.db` and `./data/stream_store` natively, `/data/state_store.db` and `/data/stream_store` under Docker (`iii-config.yaml:6-9`, `iii-config.docker.yaml:7-9`). A legacy `./data/state_store.db` or `./data/iii-config.yaml` takes precedence for instance 0 for backward compatibility (README.md:102).

## 3. Memory Observations with Confidence, Lifecycle, and Hybrid Recall

The central concept is the persistent memory observation: a recorded fact/session artifact that is compressed (synthetic noop by default, LLM-written when opted in), indexed for BM25/vector/graph retrieval, and recalled across agents and sessions (`.env.example:31-35`, `README.md:100`). The repo positions this as an implementation of the LLM Wiki pattern "with confidence scoring, lifecycle, knowledge graphs, and hybrid search" (README.md:44).

Named kinds/types visible from the wiki pages (function- and scope-level, not a full type system):

- `mem::search` — recall path behind `memory_recall`, BM25 in keyless mode (README.md:100).
- `mem::forget` — audited deletion path; the roadmap notes `mem::forget` audit as shipped (ROADMAP.md:27-35).
- `mem::your-function` — documented pattern for new memory functions via `sdk.registerFunction("mem::your-function", ...)` with KV plus `recordAudit()` (AGENTS.md:48-56).
- `api::your-endpoint` — REST registration pattern via `sdk.registerFunction("api::your-endpoint", ...)` plus `sdk.registerTrigger({ type: "http", ... api_path: "/agentmemory/your-path" })` (AGENTS.md:62-75).
- KV scopes — new scopes touch `state/schema.ts` + `types.ts`; new audit ops extend `AuditEntry.operation` in `types.ts` (AGENTS.md:11-33).
- `fingerprintId()` for dedup vs `generateId()` for unique IDs (AGENTS.md:100-109).

Key queries (verbatim names from the wiki):

```text
memory_save → memory_smart_search  (MCP)
POST /agentmemory/remember (201) → POST /agentmemory/smart-search (200)  (REST)
memory_recall (mem::search path, BM25 keyless) / memory_smart_search (graph fusion when graph data exists)
```

per `INSTALL_FOR_AGENTS.md:128-151` and `README.md:100`. No query-language grammar or ranking formula is documented in the available pages beyond the tuning knobs `BM25_WEIGHT`, `VECTOR_WEIGHT`, `AGENTMEMORY_GRAPH_WEIGHT`, `TOKEN_BUDGET`, `MAX_OBS_PER_SESSION` (`.env.example:112-118`).

## 4. LLM / External Service Integration

The repo calls LLMs optionally; keyless operation is the default and calls no external service. Detection orders are documented in `.env.example:24-37` and `.env.example:80-84`.

- LLM provider detection priority: `OPENAI_API_KEY → MINIMAX_API_KEY → ANTHROPIC_API_KEY → GEMINI_API_KEY → OPENROUTER_API_KEY → noop` (`.env.example:24-37`). Without a key the daemon runs in noop mode with zero-LLM synthetic compression and BM25 recall (`.env.example:31-33`).
- A provider key alone does not enable LLM-written observation compression; `AGENTMEMORY_AUTO_COMPRESS=true` is additionally required (`.env.example:34-35`, `README.md:98`).
- Embedding detection order: `EMBEDDING_PROVIDER` override → `GEMINI_API_KEY` → `OPENAI_API_KEY` → `VOYAGE_API_KEY` → `COHERE_API_KEY` → `OPENROUTER_API_KEY` → BM25-only, with `EMBEDDING_PROVIDER=local` opting into on-device `Xenova/all-MiniLM-L6-v2` (first request downloads the model; inference runs locally after) (`.env.example:80-84`, `README.md:100`).
- `EMBEDDING_PROVIDER` values: `local | openai | voyage | cohere | gemini | openrouter` (`.env.example:74-86`).

Relevant env vars:

| Variable | Required? | Purpose |
|---|---|---|
| `OPENAI_API_KEY`, `MINIMAX_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`/`GOOGLE_API_KEY`, `OPENROUTER_API_KEY` | No (one optionally) | LLM provider selection in fixed priority order (`.env.example:30-56`) |
| `OPENAI_MODEL`, `ANTHROPIC_MODEL`, `GEMINI_MODEL`, `OPENROUTER_MODEL`, `MINIMAX_MODEL`, `MAX_TOKENS`, `AGENTMEMORY_LLM_TIMEOUT_MS`, `FALLBACK_PROVIDERS` | No | Model choice, token cap, timeout, fallbacks (`.env.example:30-56`) |
| `EMBEDDING_PROVIDER`, `VOYAGE_API_KEY`, `COHERE_API_KEY`, `OPENAI_EMBEDDING_MODEL`, `OPENAI_EMBEDDING_DIMENSIONS`, `OPENROUTER_EMBEDDING_MODEL` | No | Embedding backend; `local` = on-device MiniLM (`.env.example:74-86`) |
| `AGENTMEMORY_AUTO_COMPRESS`, `AGENTMEMORY_INJECT_CONTEXT`, `AGENTMEMORY_LLM_NOTHINK`, `AGENTMEMORY_REFLECT`, `AGENTMEMORY_ALLOW_AGENT_SDK` | No | Behaviour flags; compression and injection are opt-in costs (`.env.example:124-143`, `INSTALL_FOR_AGENTS.md:174-180`) |
| `AGENTMEMORY_SECRET` | No | Bearer-token auth for REST + viewer + plugins; loopback REST is open without it (`.env.example:99-106`) |

## 5. The Shared-Memory Save-to-Recall Pipeline

Primary workflow: one server captures observations from any wired agent and serves recall to all of them (README.md:155). Function-level signatures are not documented in the available wiki pages; steps below cite the narrowest file:line the wiki provides for each stage.

1. Install and start via `npx -y @agentmemory/agentmemory@latest` (README.md:95); interactive setup seeds config, starts the memory server and pinned iii engine, and offers a global install (README.md:98). Alternative: `npm install -g @agentmemory/agentmemory@latest`, though npx remains canonical (README.md:130-133).
2. Validate four endpoints: `:3111 /agentmemory/livez` and `/agentmemory/health` return 200, `:3112` streams worker free at startup, `:3113` viewer reachable, `:49134` engine WebSocket registered (INSTALL_FOR_AGENTS.md:68-74).
3. Wire agents with `agentmemory connect <agent>` covering 18 agents (`claude-code`, `copilot-cli`, `codex`, `cursor`, `gemini-cli`, `opencode`, `cline`, `continue`, `droid`, `hermes`, `openclaw`, `openhuman`, `pi`, `qwen`, `warp`, `zed`, `antigravity`, `kiro`) (INSTALL_FOR_AGENTS.md:104-113, README.md:117). Native adapters combine plugins, hooks, and MCP per agent (e.g., Claude Code "native plugin + 12 hooks + MCP", OpenCode "22 hooks + MCP + plugin") (README.md:160-210).
4. Seed and exercise with `demo`, which seeds sample sessions and exercises recall BM25-only by default (README.md:106-109, INSTALL_FOR_AGENTS.md:88-92). Install 17 native skills via `npx skills add rohitg00/agentmemory -y` so agents invoke memory at the right time (README.md:106-109).
5. Save via `memory_save` (MCP) or `POST /agentmemory/remember` expecting 201, with `Authorization: Bearer $AGENTMEMORY_SECRET` when set (INSTALL_FOR_AGENTS.md:128-151).
6. Recall via `memory_smart_search` (MCP) or `POST /agentmemory/smart-search` expecting 200; restart persistence check confirms survival across restarts (INSTALL_FOR_AGENTS.md:128-151). Keyless recall is BM25; semantic queries (e.g., the demo's `database performance optimization`) can return zero until an embedding provider is configured (README.md:111).
7. Opt into costs explicitly: `AGENTMEMORY_INJECT_CONTEXT`, `AGENTMEMORY_AUTO_COMPRESS` + provider key, `EMBEDDING_PROVIDER=local` (INSTALL_FOR_AGENTS.md:174-180). MCP handler convention for new tools is `case "memory_your_tool":` with arg validation, CSV splitting, and `{ content: [{ type: "text", text: JSON.stringify(result) }] }` return (AGENTS.md:78-88).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | ~214+ (truncated at 213) | Overview, install, runtime ports/state, agent-compatibility table (01-overview) |
| `.env.example` | ~210 (shown to ~185) | Commented config template copied to `~/.agentmemory/.env`; all lines OFF by default (`.env.example:1-18`) |
| `iii-config.yaml` | ~61 | Native engine config: loopback binds, file state paths, 7 workers, dev-reload `iii-exec` (`iii-config.yaml:1-10`, `iii-config.yaml:55-61`) |
| `iii-config.docker.yaml` | ~10+ | Docker engine config: `0.0.0.0` binds, env-substituted ports, `/data` paths (`iii-config.docker.yaml:1-10`) |
| `AGENTS.md` | ~126 | Contributor pins (iii-sdk 0.22.1, file SQLite, tsdown ESM) and multi-file update checklists (AGENTS.md:4-33) |
| `INSTALL_FOR_AGENTS.md` | ~222 (shown to ~184) | Agent runbook: prereqs, start, port validation, demo, connect, persistence check (INSTALL_FOR_AGENTS.md:1-113) |
| `tsdown.config.ts` | ~86 | ESM/node20 build; entries for `src/index.ts`, `src/cli.ts`, `src/mcp/standalone.ts` + 14 hook entries dual-emitted to `dist/hooks` and `plugin/scripts` (`tsdown.config.ts:1-86`) |
| `tsconfig.json` | 21 | Strict TS config: ES2022/ESNext/bundler, `rootDir src`, `outDir dist`, excludes `test` and `src/hooks` (`tsconfig.json:1-21`) |
| `vitest.config.ts` | 12 | Test sandboxing of `HOME`/`USERPROFILE` to a throwaway tmpdir (`vitest.config.ts:1-12`) |
| `GOVERNANCE.md` | ~65 | Linux Foundation MVG, lazy consensus, `governance`/`breaking` flows (GOVERNANCE.md:5-65) |
| `MAINTAINERS.md` | ~19 | Single active maintainer Rohit Ghumare since 2026-01 (MAINTAINERS.md:7-19) |
| `ROADMAP.md` | ~90 | Q2 2026–Q1 2027 Depth/Breadth/Trust/v1.0 themes and shipped/active/planned items (ROADMAP.md:18-44) |
| `SECURITY.md` | ~76 | GHSA-first reporting, supported-version table, scope, supply-chain stance (SECURITY.md:3-76) |
| `.gitignore` | 32 | Ignores `node_modules/`, `dist/`, `.env*`, `data/`, lockfiles, eval artifacts (`.gitignore:1-32`) |
| `DESIGN.md` | 289 (shown to ~153) | Viewer theme spec: black/gold palette, type scale, button/card/nav rules (DESIGN.md:1-30) |

`src/`, `plugin/`, and `integrations/` files are referenced only indirectly (e.g., `src/index.ts`, `src/cli.ts`, `src/mcp/standalone.ts`, `src/hooks`, `tools-registry.ts`, `server.ts`, `triggers/api.ts`, `state/schema.ts`, `types.ts`) and are not covered by the available wiki pages.

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `iii-sdk` | `0.22.1` (AGENTS.md:6-8) | Engine SDK; WebSocket to iii-engine on port 49134 |
| `@iii-dev/helpers` | `0.22.1` (AGENTS.md:6-8) | Engine helper library paired with iii-sdk |
| `iii-engine` (binary) | `v0.22.1` pinned (README.md:147) | Runtime engine; server refuses non-matching engines, binary in `~/.agentmemory/bin` |
| `@anthropic-ai/sdk` | unknown (listed without constraint in SECURITY.md:54-76) | Production dependency (LLM provider path) |
| `@anthropic-ai/claude-agent-sdk` | unknown (listed without constraint in SECURITY.md:54-76) | Production dependency; also in tsdown `neverBundle` (tsdown.config.ts:20-32) |
| `@clack/prompts` | unknown (listed without constraint in SECURITY.md:54-76) | Production dependency (interactive CLI prompts) |
| `dotenv` | unknown (listed without constraint in SECURITY.md:54-76) | Production dependency (env loading; `~/.agentmemory/.env`) |
| `zod` | unknown (listed without constraint in SECURITY.md:54-76) | Production dependency (validation; MCP `case "memory_your_tool"` arg validation per AGENTS.md:78-88) |
| `@huggingface/transformers` | unknown, explicitly never bundled (tsdown.config.ts:20-32) | Lazy-loaded local embeddings (`src/providers/embedding/{clip,local}.ts`) and reranker (`src/state/reranker.ts`) |
| Node.js | `>=20` (README.md:88-90, INSTALL_FOR_AGENTS.md:13-17) | Runtime prerequisite with npm/npx |
| `curl`, POSIX `sh`, `tar` | present on macOS/Linux (README.md:88-90) | Automatic iii-engine install; minimal `node:20-slim` images may lack them |

No committed lockfile; hardened pipelines are directed to `npm-shrinkwrap`, with Dependabot and full-matrix CI per PR (SECURITY.md:54-76). Exact semver strings for the six production npm packages are not present in the available wiki pages.

## 8. CLI / Usage Surface

Entry points (build): `src/index.ts` (daemon, dts/clean/sourcemap) and `src/cli.ts`, `src/mcp/standalone.ts` to `dist/`, plus 14 hook entries (`session-start`, `prompt-submit`, `pre-tool-use`, `post-tool-use`, `post-tool-failure`, `pre-compact`, `subagent-start`, `subagent-stop`, `notification`, `task-completed`, `stop`, `session-end`, `post-commit`, `antigravity-bridge`) dual-emitted to `dist/hooks` and `plugin/scripts` (`tsdown.config.ts:1-86`).

Commands:

| Command | Effect |
|---|---|
| `npx -y @agentmemory/agentmemory@latest` | Canonical fresh install/start; interactive agent wiring, config seeding, server + engine start (README.md:95, README.md:98) |
| `npx -y @agentmemory/agentmemory@latest demo` | Seed sample sessions and exercise recall (README.md:106-109) |
| `npx -y @agentmemory/agentmemory@latest init` | Copy `.env.example` into place as `~/.agentmemory/.env` (`.env.example:1-6`) |
| `agentmemory connect <agent>` | Wire one of 18 named agents at any time (README.md:117, INSTALL_FOR_AGENTS.md:104-113) |
| `npm install -g @agentmemory/agentmemory@latest` | Global install; npx remains canonical (README.md:130-133) |
| `npx skills add rohitg00/agentmemory -y` | Install 17 native skills for memory-aware agents (README.md:106-109) |

Env-var and config tables:

| Variable | Default | Purpose |
|---|---|---|
| `AGENTMEMORY_TOOLS` | `all` (54 tools) \| `core` (8 tools) (`.env.example:149-176`) | MCP tool surface size |
| `AGENTMEMORY_DATA_DIR` / `--data-dir` | platform default (README.md:102) | Override persistent state location |
| `AGENTMEMORY_URL`, `AGENTMEMORY_VIEWER_URL` | unset (`.env.example:149-176`) | Client/server endpoint overrides |
| `III_REST_PORT` / `III_STREAM_PORT`(+`S` alias) / `III_VIEWER_PORT` | 3111 / 3112 / 3113 (`.env.example:182-185`) | Port overrides (Docker config env-substitutes them) |
| `AGENTMEMORY_SECRET` | unset = open loopback REST (`.env.example:99-106`) | Bearer auth for REST + viewer + plugins |
| `BM25_WEIGHT`, `VECTOR_WEIGHT`, `AGENTMEMORY_GRAPH_WEIGHT`, `TOKEN_BUDGET`, `MAX_OBS_PER_SESSION`, `SUMMARIZE_CHUNK_SIZE`, `SUMMARIZE_CHUNK_CONCURRENCY` | unset/keyless defaults (`.env.example:112-118`) | Search fusion and summarization tuning |
| `TEAM_MODE`, `TEAM_ID`, `USER_ID`, `SNAPSHOT_ENABLED`, `SNAPSHOT_DIR`, `SNAPSHOT_INTERVAL`, `AGENTMEMORY_EXPORT_ROOT` | unset (`.env.example:149-176`) | Team scoping, snapshots, export root |

Config files: `~/.agentmemory/.env` (or project-root scoped copy) from `.env.example` (`.env.example:1-6`); `iii-config.yaml` (native) vs `iii-config.docker.yaml` (container) for workers, hosts, ports, and state paths (`iii-config.yaml:1-10`, `iii-config.docker.yaml:1-10`).

## 9. Extensibility Points

- New MCP tool: follow the 8-place checklist — `tools-registry.ts`, `server.ts`, `triggers/api.ts`, `index.ts`, `test/mcp-standalone.test.ts`, `README.md`, `plugin.json` files — using the `case "memory_your_tool":` handler convention (AGENTS.md:11-33, AGENTS.md:78-88).
- New REST endpoint: touch `triggers/api.ts` + `index.ts` + `README.md`; register via `sdk.registerFunction("api::your-endpoint", ...)` plus `sdk.registerTrigger({ type: "http", ... })` (AGENTS.md:11-33, AGENTS.md:62-75).
- New memory function: use `sdk.registerFunction("mem::your-function", ...)` with KV access and `recordAudit()` (AGENTS.md:48-56).
- New KV scope: extend `state/schema.ts` + `types.ts` (AGENTS.md:11-33).
- New audit operation: extend `AuditEntry.operation` in `types.ts` (AGENTS.md:11-33).
- Version bump: synchronize 7 places (`package.json`, `version.ts`, `types.ts`, `export-import.ts`, test, plugin manifests) (AGENTS.md:11-33).
- New hook: add an entry to `tsdown.config.ts` alongside the existing 14 and emit to both `dist/hooks` and `plugin/scripts`; observe the context-hook (await fetch with `AbortSignal.timeout(N)`) vs telemetry-hook (fire-and-forget with `.catch(() => {})` + `setTimeout(exit, 500/1500).unref()`) convention (AGENTS.md:94-98, `tsdown.config.ts:3-86`).
- New agent adapter: extend the `connect <agent>` matrix (18 agents listed in INSTALL_FOR_AGENTS.md:104-113) with the corresponding plugin + hooks + MCP wiring pattern per README.md:160-210.
- Viewer/theme: follow `DESIGN.md` (black `#000000` canvas, gold `#FFC000` CTAs, zero-radius buttons) (DESIGN.md:1-30).

## 10. Limitations and Gotchas

- **Native Windows requires manual engine install.** Automatic install assumes `curl`/`sh`/`tar` on macOS/Linux; native Windows needs pinned `iii.exe` v0.22.1 extracted manually, otherwise use WSL2 or Docker (README.md:88-90, README.md:122, INSTALL_FOR_AGENTS.md:13-17).
- **Engine version is strict.** The server will not attach to a non-v0.22.1 iii engine; a conflicting engine must be stopped and the binary kept in `~/.agentmemory/bin` (README.md:147).
- **Keyless semantic search silently underperforms.** Default recall is BM25-only; the demo's `database performance optimization` query is intentionally semantic and can return zero until an embedding provider (`EMBEDDING_PROVIDER=local` or a key) is configured (README.md:111, `.env.example:82`).
- **LLM compression is doubly gated.** Setting a provider key is insufficient; `AGENTMEMORY_AUTO_COMPRESS=true` must also be set or observations stay on synthetic noop compression (`.env.example:34-35`, `README.md:98`).
- **Stale npx cache serves old releases.** Fix with an explicit `npx -y @agentmemory/agentmemory@latest` invocation or `rm -rf ~/.npm/_npx`; global `npm install -g` is supported but not canonical (README.md:98, README.md:130-140).
- **Four ports plus engine socket must be free.** 3111 (REST/MCP), 3112 (streams), 3113 (viewer), 49134 (engine WebSocket); `--instance 1` shifts to 3211/3212/3213/49234 (README.md:102, INSTALL_FOR_AGENTS.md:20-74).
- **Wiki coverage is top-level only.** The two available pages stop at configuration, install, and governance; `src/`, `plugin/`, and `integrations/` behavior, plus the agent-table rows past the truncated Cline entry (README.md:213) and the `.env.example` tail past line ~185, are not documented and should not be assumed.

## 11. How It Compares to Alternatives

- **iii-hq/iii (the underlying engine):** agentmemory is pinned to iii-engine v0.22.1 over WebSocket :49134 with iii-sdk 0.22.1 (AGENTS.md:6-8, README.md:147). Using iii directly exposes generic workers (http/state/queue/pubsub/cron/stream/observability); agentmemory adds the memory-specific layer (54 MCP tools, 132 REST endpoints, 12 hooks, 17 skills, observation compression, hybrid recall).
- **mem0:** a hosted-plus-open-source memory layer with vector-store backends. agentmemory's differentiator per the wiki is zero external databases with file-backed SQLite state and keyless BM25 that works with no keys (README.md:54-59, `.env.example:31-33`).
- **Letta (formerly MemGPT):** agent-centric stateful memory with managed persistence. agentmemory instead shares one local server across heterogeneous coding agents through hooks/MCP/REST rather than embedding memory in a single framework (README.md:155).
- **Zep / OpenMemory-style stores:** typically require a vector database or service dependency. agentmemory's positioning is local-first, single-maintainer, MCP/hook-native memory with optional on-device embeddings (`Xenova/all-MiniLM-L6-v2`) instead of mandatory external infrastructure (`.env.example:80-84`, `SECURITY.md:54-76`).

Positioning sentence: agentmemory occupies the local-first, zero-external-DB niche for polyglot coding-agent setups — one shared file-backed memory server over MCP/hooks/REST — trading managed-service recall quality and multi-maintainer governance (single maintainer since 2026-01 per MAINTAINERS.md:7-9) for zero-config keyless operation with opt-in LLM and embedding upgrades.

## Appendix: Selected Code Snippets

1. Config template header (`.env.example:1-6`):

```env
# Copy this file to `~/.agentmemory/.env` (or to your project root if you
# prefer scoped config) and uncomment the lines you want to override.
# Every line is OFF by default — `agentmemory` runs out of the box with no
# LLM key, no embedding key, and no API auth.
# Run `npx -y @agentmemory/agentmemory@latest init` to copy this file into
# place automatically.
```

2. Native engine HTTP worker (`iii-config.yaml:1-8`):

```yaml
workers:
  - name: iii-http
    config:
      port: 3111
      host: 127.0.0.1
      default_timeout: 180000
```

3. Docker engine HTTP worker (`iii-config.docker.yaml:1-10`):

```yaml
workers:
  - name: iii-http
    config:
      port: ${III_REST_PORT:3111}
      host: 0.0.0.0
      default_timeout: 180000
```

4. Contributor architecture pins (`AGENTS.md:6-8`):

```text
"Engine: iii-sdk 0.22.1 with @iii-dev/helpers 0.22.1 (WebSocket to iii-engine 0.22.1 on port 49134 ...)"
"State: File-based SQLite via iii-engine's StateModule (./data/state_store.db)"
"Build: TypeScript → ESM via tsdown, output to dist/"
```
