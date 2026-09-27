> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
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
---
## Configuration template (.env.example)
Template header (verbatim, `.env.example:1-6`):
```env
# Copy this file to `~/.agentmemory/.env` (or to your project root if you
# prefer scoped config) and uncomment the lines you want to override.
# Every line is OFF by default — `agentmemory` runs out of the box with no
# LLM key, no embedding key, and no API auth.
# Run `npx -y @agentmemory/agentmemory@latest init` to copy this file into
# place automatically.
```
Key config groups with exact parameter names:

| Group | Parameters |
|---|---|
| LLM provider (pick ONE) | `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `OPENAI_API_KEY_FOR_LLM`, `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`, `ANTHROPIC_BASE_URL`, `GEMINI_API_KEY` / `GOOGLE_API_KEY`, `GEMINI_MODEL`, `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`, `MINIMAX_API_KEY`, `MINIMAX_MODEL`, `MAX_TOKENS`, `AGENTMEMORY_LLM_TIMEOUT_MS`, `AGENTMEMORY_ALLOW_AGENT_SDK`, `FALLBACK_PROVIDERS` (`.env.example:30-56`) |
| Embeddings | `EMBEDDING_PROVIDER` (`local \| openai \| voyage \| cohere \| gemini \| openrouter`), `VOYAGE_API_KEY`, `COHERE_API_KEY`, `OPENAI_EMBEDDING_MODEL`, `OPENAI_EMBEDDING_DIMENSIONS`, `OPENROUTER_EMBEDDING_MODEL` (`.env.example:74-86`) |
| Auth | `AGENTMEMORY_SECRET` — bearer-token auth for REST + viewer + plugins; without it REST is open on loopback (`.env.example:99-106`) |
| Search tuning | `BM25_WEIGHT`, `VECTOR_WEIGHT`, `AGENTMEMORY_GRAPH_WEIGHT`, `TOKEN_BUDGET`, `MAX_OBS_PER_SESSION`, `SUMMARIZE_CHUNK_SIZE`, `SUMMARIZE_CHUNK_CONCURRENCY` (`.env.example:112-118`) |
| Behaviour flags | `AGENTMEMORY_AUTO_COMPRESS`, `AGENTMEMORY_INJECT_CONTEXT`, `CONSOLIDATION_ENABLED`, `CONSOLIDATION_DECAY_DAYS`, `GRAPH_EXTRACTION_ENABLED`, `GRAPH_EXTRACTION_BATCH_SIZE`, `AGENTMEMORY_LLM_NOTHINK`, `AGENTMEMORY_REFLECT`, `AGENTMEMORY_DROP_STALE_INDEX`, `AGENTMEMORY_IMAGE_EMBEDDINGS`, `AGENTMEMORY_INDEX_SAVE_INTERVAL_MS`, `AGENTMEMORY_VECTOR_BUCKET_SIZE`, `AGENTMEMORY_VECTOR_BACKFILL_MAX`, `AGENTMEMORY_VECTOR_BACKFILL` (`.env.example:124-143`) |
| CLI / runtime | `AGENTMEMORY_TOOLS` (`all` 54 tools default \| `core` 8 tools), `AGENTMEMORY_SLOTS`, `AGENTMEMORY_DEBUG`, `AGENTMEMORY_FORCE_PROXY`, `AGENTMEMORY_PROBE_TIMEOUT_MS`, `AGENTMEMORY_URL`, `AGENTMEMORY_VIEWER_URL`, `AGENTMEMORY_DATA_DIR`, `AGENTMEMORY_USE_DOCKER`, `AGENTMEMORY_EXPORT_ROOT`, `STANDALONE_MCP`, `STANDALONE_PERSIST_PATH`, `SNAPSHOT_ENABLED`, `SNAPSHOT_DIR`, `SNAPSHOT_INTERVAL`, `TEAM_MODE`, `TEAM_ID`, `USER_ID` (`.env.example:149-176`) |
| Ports | `III_REST_PORT` (3111), `III_STREAM_PORT` / `III_STREAMS_PORT` (3112), `III_VIEWER_PORT` (3113) (`.env.example:182-185`) |

Notable semantics (verbatim excerpts):
- `"Without a provider key, agentmemory runs in noop mode: observations are indexed via zero-LLM synthetic compression and BM25 recall still works"` (`.env.example:31-33`).
- `"A provider key alone does not enable LLM-written observation compression; that path also requires AGENTMEMORY_AUTO_COMPRESS=true."` (`.env.example:34-35`).
- `"Local embeddings are an explicit opt-in, not the keyless default."` (`.env.example:82`).
- Truncated in chunk: `.env.example` shown to ~line 185 of 210; tail beyond `III_VIEWER_PORT` was cut, so remaining port/env lines are not covered here.

## Engine configs (iii-config.yaml, iii-config.docker.yaml)
Native `iii-config.yaml` binds loopback with fixed ports (verbatim, `iii-config.yaml:1-8`):
```yaml
workers:
  - name: iii-http
    config:
      port: 3111
      host: 127.0.0.1
      default_timeout: 180000
```
Docker `iii-config.docker.yaml` binds `0.0.0.0` with env-substituted ports and file paths (verbatim, `iii-config.docker.yaml:1-10`):
```yaml
workers:
  - name: iii-http
    config:
      port: ${III_REST_PORT:3111}
      host: 0.0.0.0
      default_timeout: 180000
```
Worker differences:

| Worker | Native (`iii-config.yaml`) | Docker (`iii-config.docker.yaml`) |
|---|---|---|
| `iii-http` | port 3111, host 127.0.0.1 | port `${III_REST_PORT:3111}`, host 0.0.0.0 |
| `iii-state` | kv file `./data/state_store.db` | kv file `/data/state_store.db` |
| `iii-stream` | port 3112, host 127.0.0.1, file `./data/stream_store` | port `${III_STREAM_PORT:3112}`, host 0.0.0.0, file `/data/stream_store` |
| `iii-observability` | `sampling_ratio: 0.1`, `logs_console_output: false` with #519 feedback-loop rationale comment | same `0.1` / console-off, shorter comment |
| `iii-exec` (dev reload) | present: watches `src/**/*.ts`, runs `node dist/index.mjs` (`iii-config.yaml:55-61`) | absent |

Both declare `iii-queue` (builtin), `iii-pubsub` (local), `iii-cron` (kv), and CORS origins for `localhost`/`127.0.0.1` on REST and viewer ports (`iii-config.yaml:6-9`, `iii-config.docker.yaml:7-9`).

## Agent and install docs (AGENTS.md, INSTALL_FOR_AGENTS.md)
`AGENTS.md` architecture pins (verbatim, `AGENTS.md:6-8`):
- `"Engine: iii-sdk 0.22.1 with @iii-dev/helpers 0.22.1 (WebSocket to iii-engine 0.22.1 on port 49134 ...)"`
- `"State: File-based SQLite via iii-engine's StateModule (./data/state_store.db)"`
- `"Build: TypeScript → ESM via tsdown, output to dist/"`

Mandatory consistency checklists (`AGENTS.md:11-33`): adding/removing MCP tools touches 8 places (`tools-registry.ts`, `server.ts`, `triggers/api.ts`, `index.ts`, `test/mcp-standalone.test.ts`, `README.md`, `plugin.json` files); REST endpoints touch `triggers/api.ts` + `index.ts` + `README.md`; version bumps touch 7 places (`package.json`, `version.ts`, `types.ts`, `export-import.ts`, test, plugin manifests); new KV scopes touch `state/schema.ts` + `types.ts`; new audit ops touch `AuditEntry.operation` in `types.ts`.

Code patterns given verbatim: `sdk.registerFunction("mem::your-function", ...)` with kv + `recordAudit()` (`AGENTS.md:48-56`); REST registration via `sdk.registerFunction("api::your-endpoint", ...)` + `sdk.registerTrigger({ type: "http", ... api_path: "/agentmemory/your-path" })` (`AGENTS.md:62-75`); MCP handler `case "memory_your_tool":` validating args, splitting CSV args, and returning `{ content: [{ type: "text", text: JSON.stringify(result) }] }` (`AGENTS.md:78-88`). Hook convention: context-injecting hooks (`pre-tool-use`, `pre-compact`, `session-start`) await fetch with `AbortSignal.timeout(N)`; telemetry-only hooks fire-and-forget with `.catch(() => {})` plus `setTimeout(() => process.exit(0), 500).unref()` (1500ms for multi-request `stop`/`session-end`) (`AGENTS.md:94-98`). Coding standards: ESM-only, `fingerprintId()` for dedup vs `generateId()` for unique IDs, `Promise.all` for independent kv ops, whitelist REST fields, single-capture ISO timestamps (`AGENTS.md:100-109`). Stats line (v0.9.29): 54 MCP tools, 132 REST endpoints, 6 resources, 3 prompts, 12 hooks, 17 skills, 260+ functions, 1,596+ tests (`AGENTS.md:118-126`).

`INSTALL_FOR_AGENTS.md` port table (verbatim structure, `INSTALL_FOR_AGENTS.md:68-74`):

| Port | Owner | Validation |
|---|---|---|
| 3111 | agentmemory REST/MCP | `/agentmemory/livez` and `/agentmemory/health` return 200 |
| 3112 | iii streams | listed in the ready panel; must be free at startup |
| 3113 | agentmemory viewer | opening the URL returns the viewer |
| 49134 | iii engine WebSocket | listed in the ready panel and worker registration succeeds |

Other runbook facts: prerequisites Node ≥20 plus `curl`/`sh`/`tar` on macOS/Linux; Windows needs manually extracted pinned `iii.exe` v0.22.1 or Docker/WSL2 (`INSTALL_FOR_AGENTS.md:13-17`); canonical start `npx -y @agentmemory/agentmemory@latest` with `--data-dir` and `--instance 1` (ports 3211/3212/3213/49234) variants (`INSTALL_FOR_AGENTS.md:20-62`); `demo` seeds three sessions with BM25-only default recall (`INSTALL_FOR_AGENTS.md:88-92`); `connect <agent>` supports 18 agents (`claude-code`, `copilot-cli`, `codex`, `cursor`, `gemini-cli`, `opencode`, `cline`, `continue`, `droid`, `hermes`, `openclaw`, `openhuman`, `pi`, `qwen`, `warp`, `zed`, `antigravity`, `kiro`) (`INSTALL_FOR_AGENTS.md:104-113`); `memory_save` → `memory_smart_search` or `POST /agentmemory/remember` (201) → `POST /agentmemory/smart-search` (200) persistence check with `Authorization: Bearer $AGENTMEMORY_SECRET` when set (`INSTALL_FOR_AGENTS.md:128-151`); opt-in costs section for `AGENTMEMORY_INJECT_CONTEXT`, `AGENTMEMORY_AUTO_COMPRESS` + provider key, and `EMBEDDING_PROVIDER=local` (`INSTALL_FOR_AGENTS.md:174-180`). Truncated in chunk: `INSTALL_FOR_AGENTS.md` shown to ~line 184 of 222 with the tool-surface tail cut, so the `--tools all` vs `core` detail past that point is not covered here.

## Governance, roadmap, security (GOVERNANCE.md, MAINTAINERS.md, ROADMAP.md, SECURITY.md)
- `GOVERNANCE.md` follows Linux Foundation Minimum Viable Governance scoped to a single maintainer, with a mission of zero-external-database, MCP-compatible, local-first memory (`GOVERNANCE.md:3-12`); maintainers must answer PRs within ~3 working days, uphold the code of conduct, avoid self-merging non-trivial PRs once count > 1, and disclose conflicts (`GOVERNANCE.md:27-33`); maintainer promotion needs 6 months of cross-subsystem contributions, a public `MAINTAINERS.md` PR, 7-day objection window, and no standing objection (`GOVERNANCE.md:37-43`); default decision mode is lazy consensus (silence is assent after 72h), non-PR/governance/breaking decisions go through a `governance`-labeled issue with `+1`/`-1`/`0` majority vote (7-day public window when only one maintainer) (`GOVERNANCE.md:47-57`); breaking REST/MCP changes need a `breaking`-labeled tracking issue one minor ahead, a deprecation path for one minor, and a `Breaking` CHANGELOG section (`GOVERNANCE.md:61-65`).
- `MAINTAINERS.md` table lists one Active maintainer — Rohit Ghumare (`@rohitg00`), Independent, project lead all subsystems, since 2026-01 — and `_None yet._` under Emeritus (`MAINTAINERS.md:5-13`); recruitment aims to add a maintainer from a different organization per `ROADMAP.md`, via a `governance`-tagged issue (`MAINTAINERS.md:15-19`).
- `ROADMAP.md` covers Q2 2026–Q1 2027 with Shipped/Active/Planned/Candidate states (`ROADMAP.md:3-12`); quarterly themes Depth (multimodal, connectors), Breadth (hook parity, OpenSSF), Trust (SSO, audit export, RBAC, deployment, SLO, security audit), v1.0 (surface freeze, LTS `v1.x`, foundation) (`ROADMAP.md:18-23`); Q2 shipped includes console docs, health RSS gating, standalone MCP proxy, `mem::forget` audit, fs-watcher, website, CI npm publishes (`ROADMAP.md:27-35`); active items are multimodal memory (#64/PR #111) and governance baseline; planned includes GitHub connector sharing the `POST /agentmemory/observe` wire format, session replay UI, CI benchmark guarding the 95.2% R@5 number (`ROADMAP.md:37-44`); out of scope states no cloud SaaS, no billing/commercial licensing beyond Apache-2.0, no agent frameworks (`ROADMAP.md:84-90`).
- `SECURITY.md` reporting: no public issues; preferred channel is GHSA private form, fallback encrypted email to `ghumare64@gmail.com` with PGP/SSH keys, minimum report contents version + surface + curl/MCP repro + impact (`SECURITY.md:3-17`); handling is acknowledge ≤72h (target 24h), CVSS 3.1 triage, private-branch fix with advisory draft, 30-day (up to 90-day) coordinated disclosure, npm patch + advisory + `### Security` CHANGELOG (`SECURITY.md:21-25`); supported versions table: latest minor `0.9.x` yes, previous `0.8.x` critical/high only for 90 days, older no (`SECURITY.md:27-32`); in scope covers server, `@agentmemory/mcp`, `@agentmemory/fs-watcher`, `integrations/` (`hermes/`, `openclaw/`, `filesystem-watcher/`), `plugin/`; out of scope is third-party clients, `iii-sdk` upstream, `website/` except user-security issues (`SECURITY.md:36-50`); supply chain: pre-built `dist/` in tarball, 6 production deps (`@anthropic-ai/sdk`, `@anthropic-ai/claude-agent-sdk`, `@clack/prompts`, `dotenv`, `iii-sdk`, `zod`) plus guarded `optionalDependencies`, no committed lockfile with `npm-shrinkwrap` guidance for hardened pipelines, Dependabot + full matrix CI per PR (`SECURITY.md:54-76`).

## Build, ignore, design, test (tsconfig.json, tsdown.config.ts, .gitignore, DESIGN.md, vitest.config.ts)
- `tsconfig.json`: `target ES2022`, `module ESNext`, `moduleResolution bundler`, `declaration` + `declarationMap` + `sourceMap`, `outDir dist`, `rootDir src`, `strict`, `esModuleInterop`, `skipLibCheck`, `forceConsistentCasingInFileNames`, `resolveJsonModule`, `isolatedModules`, `noUnusedLocals`, `noUnusedParameters`; `include ["src/**/*"]`, `exclude ["node_modules", "dist", "test", "src/hooks"]` (`tsconfig.json:1-21`).
- `tsdown.config.ts` hook entries (verbatim, `tsdown.config.ts:3-16`): 14 entries `session-start`, `prompt-submit`, `pre-tool-use`, `post-tool-use`, `post-tool-failure`, `pre-compact`, `subagent-start`, `subagent-stop`, `notification`, `task-completed`, `stop`, `session-end`, `post-commit`, `antigravity-bridge`; shared `format ["esm"]`, `target "node20"`, `neverBundle ["@huggingface/transformers", "@anthropic-ai/claude-agent-sdk", "@anthropic-ai/sdk"]` because transformers is lazy-loaded from `src/providers/embedding/{clip,local}.ts` and `src/state/reranker.ts` and bundling would inline unresolvable `onnxruntime_binding.node` paths (`tsdown.config.ts:20-32`); build matrix emits `src/index.ts` (dts, clean, sourcemap, `#!/usr/bin/env node` banner) to `dist`, `src/cli.ts` and `src/mcp/standalone.ts` to `dist`, and each hook entry twice — to `dist/hooks` and `plugin/scripts` — one entry per config block to avoid hashed-chunk hoisting (`tsdown.config.ts:46-86`).
- `.gitignore` (32 lines): ignores `node_modules/`, `dist/`, `*.tsbuildinfo`, `.env`/`.env.*` except `!.env.example`, `*.log`, `.DS_Store`, `.claude/`, `plugin/scripts/*.map` + `*.d.mts`, `data/` except `!eval/data/`, `data-*/`, `agentmemory-debug/`, `.gstack/`, lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`), `integrations/hermes/__pycache__/`, `eval/reports/`, `eval/data/longmemeval/` (278MB LongMemEval fetch-on-demand) (`.gitignore:1-32`).
- `DESIGN.md` (289 lines): Lamborghini-inspired viewer theme — true black `#000000` canvas, white type, sole accent Lamborghini Gold `#FFC000` for primary CTAs; LamboType Neo-Grotesk with 12° angled terminals, all-caps display scale 120px→10px; zero border-radius buttons (gold CTA hover `#917300`, transparent ghost, white/black/gray variants); charcoal `#202020` cards, transparent floating nav with centered bull logo, full-viewport video heroes (`DESIGN.md:1-30`). Truncated in chunk: shown to ~line 153 of 289 (through "Distinctive C"), so the remainder of the design spec is not covered here.
- `vitest.config.ts` sandboxes `HOME`/`USERPROFILE` to `mkdtempSync(join(tmpdir(), "agentmemory-test-home-"))` because `config.ts` reads `~/.agentmemory/.env` under `process.env` and asserted defaults would otherwise inherit the developer's local install state (`vitest.config.ts:6-12`).

**Covers:** `.env.example`, `.gitignore`, `AGENTS.md`, `DESIGN.md`, `GOVERNANCE.md`, `iii-config.docker.yaml`, `iii-config.yaml`, `INSTALL_FOR_AGENTS.md`, `MAINTAINERS.md`, `ROADMAP.md`, `SECURITY.md`, `tsconfig.json`, `tsdown.config.ts`, `vitest.config.ts`
