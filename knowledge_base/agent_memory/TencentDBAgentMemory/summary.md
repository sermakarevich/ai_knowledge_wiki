# Technical Analysis: TencentCloud/TencentDB-Agent-Memory

**Repository:** https://github.com/TencentCloud/TencentDB-Agent-Memory
**Version analyzed:** v2.0.1-beta.1 (per ROADMAP.md:6, ROADMAP_CN.md:5; current stable v2.0.0 per README_CN.md:305)
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Problem space: agent sessions repeat work — project context is re-explained, documents re-read, workflows rediscovered each session (README.md:91). Chat logs are not reusable across sessions, agents, or team members, and plain retrieval answers "what can be found" but not who may use it, which version is valid, or which agent should receive it (README.md:222).

What the repo does: provides a shared Memory Hub + Proxy stack that converts existing information (conversations, documents, code) into reusable, versioned, permissioned memory assets, summarised as "Existing information → Reusable memory assets → Fewer turns → Less rework" (README.md:95-97). Three services boot together — `memory-core` + `memory-hub` + `proxy` — with the control panel at `http://localhost:8125` (README.md:36-46). One proxy gives zero-code integration: pointing an agent's base URL at the proxy suffices, with no plugin, hook, or MCP server required (README.md:62-64).

Primary user: teams running multiple coding agents (Claude Code, Codex, CodeBuddy, DeepSeek Harness, WorkBuddy, Hermes, OpenClaw per README.md:66-79) who need shared, persistent team memory rather than per-session chat history. Secondary user: team/system admins who curate, review, and permission assets in Memory Hub (README.md:152-155).

## 2. High-Level Architecture

```text
Agents (Claude Code / Codex / CodeBuddy / Hermes / OpenClaw / ...)
  │ base_url → Proxy:8096 (Anthropic/OpenAI dual-protocol)
  ▼
MemoryProxy ─► MemoryCore:8420 (Gateway binary, v1/v2/v3 APIs, L0→L3 pipeline)
  │                  │
  │                  ├──► MemoryKnowledge:8424 (Wiki + CodeGraph, Swagger at /docs)
  │                  │
  │                  ▼
  └────────── MemoryHub / Panel UI:8125 (teams, agents, assets, ACLs, cold-start import)
                     │
                     ▼
              State: SQLite default (container volume) │ MongoDB experimental │
                   Service mode: TCVDB + COS, Redis (locks/queues)
```

Data-flow narrative (5 steps):

1. **Intercept.** Agent LLM traffic goes through the Proxy (`ANTHROPIC_BASE_URL=http://127.0.0.1:8096/...`, INSTALL.md:43); session `mem:` commands (`mem:sync`, `mem:create-skill [prompt]`, `mem:help`, ROADMAP.md:89) trigger refresh or async Skill extraction within the session.
2. **Extract.** Memory Hub automatically extracts Chat Memory and Skills from conversations/tasks, and ingests docs/code into Wiki and CodeGraph (README.md:105-107). Past sessions, codebases, and documents are importable from the panel for cold start (README.md:170-172).
3. **Distill and index.** Conversations distill L0 Conversation → L1 Atom → L2 Scenario → L3 Persona (README.md:115); Wiki builds structured pages with a link graph while CodeGraph indexes symbols, files, calls, and impact paths (README.md:137-144).
4. **Govern.** Assets carry owner, version, status, visibility (`private` / `team` / `restricted`, README.md:154; plus `agent` directed assembly per README_CN.md:232), User/Role/Agent ACLs, and agent bindings, managed in the panel under System Admin vs. team Admin/Member roles (README.md:152-155, INSTALL.md:146).
5. **Inject.** Assets bind via Fixed Binding + ACL and are exposed on demand through `/v3/tools/list` + `/v3/tools/call` (README_CN.md:262, README_CN.md:267); recall uses L2/L3 layers for context with BM25 + vector + RRF back to L1/L0 under count/char/timeout budgets (README_CN.md:258).

Persistent state lives: by default SQLite on container volumes (`data/skills.db`, `data/tdai-memory.db`, `vectors.db`, `knowledge.db*` — all git-ignored per `.gitignore:78`, `.gitignore:118`); Gateway standalone data dir `~/.memory-tencentdb/memory-tdai/` (README.deployment.md:40). Optional experimental MongoDB mode covers L0/L1/profile/skill docs plus mongot BM25 (INSTALL.md:68). Service (cloud) mode uses TCVDB + COS for document/vector state and Redis for distributed locks and task queues (README.deployment.md:10, README.deployment.md:157). Env/YAML/config state in `deploy/global-images/.env`, `.admin-key`, `.proxy-config/`, `.memory-core-config/` is git-ignored (`.gitignore:67`).

## 3. Memory Assets (The Core Abstraction)

Representation: the central concept is a **memory asset, not a chat log** — a versioned, owned, permissioned, agent-bindable unit of reusable experience (README.md:93-97). Four named kinds:

- **Chat Memory** — per-agent persistent memory of preferences, facts, decisions, interaction history; distilled L0 Conversation → L1 Atom → L2 Scenario → L3 Persona/Core (README.md:113-115, README_CN.md:102, README_CN.md:252).
- **Skill** — executable experience with versions, resource files, trigger boundaries, execution steps, and validation rules; private by default, shared team-wide after review, importable into a designated agent's context (README.md:125-127). Examples: troubleshooting, code review, release checklists (README.md:131).
- **Wiki** — structured pages with link graph generated from product docs, design specs, runbooks (README.md:137).
- **CodeGraph** — indexed symbols, files, call relationships, impact paths; supports caller/callee inspection and pre-edit impact analysis (README.md:141-144, README.md:146).

Governance attributes per asset: owner (auto-holds management permission, README.md:155), version, status, visibility, usage counts, agent bindings (README.md:152-153). Visibility levels:

| Level | Meaning (README.md:154; `agent` from README_CN.md:232) |
|---|---|
| `private` | Owner only |
| `team` | All team members |
| `restricted` | User / Role / Agent ACLs |
| `agent` | Directed same-team assembly |

Key queries (verbatim API/tool surface from wiki):

```text
v1 plugin tools: memory_tencentdb_memory_search / memory_tencentdb_conversation_search (README.deployment.md:341)
v2 plugin tools: tdai_memory_search (query, limit=5), tdai_conversation_search, tdai_read_scene (scene_id) (README.deployment.md:384)
v2 API: /v2/conversation/{add,query,search,delete}, /v2/atomic/{add,query,search,delete}, /v2/scenario/{ls,read,write,rm}, /v2/persona/{read,write} (README.deployment.md:426)
```

Recall path: L2/L3 injected as context; BM25 + vector + RRF retrieval back to L1/L0 under budgets (README_CN.md:258); knowledge exposed via `/v3/tools/list` + `/v3/tools/call` (README_CN.md:267).

## 4. LLM / External Service Integration

Providers: bring-your-own LLM, OpenAI-compatible. Standalone defaults: `TDAI_LLM_BASE_URL` default `https://api.openai.com/v1`, `TDAI_LLM_MODEL` default `gpt-4o` (README.deployment.md:56). Docker/config keys map env↔YAML (`TDAI_LLM_API_KEY`↔`llm.apiKey`, README.docker.md:163). The deploy flow probes LLM connectivity before booting containers and re-prompts on failure (INSTALL.md:29; `verify.sh --skip-llm` skips the probe, INSTALL.md:39).

Two LLM parameter groups are required at install time (both filled in `deploy/global-images/.env`):

| Env var | Group | Purpose |
|---|---|---|
| `MEMORY_LLM_BASE_URL` / `MEMORY_LLM_API_KEY` / `MEMORY_LLM_MODEL` | memory | Extraction/distillation/recall inside memory-core/knowledge (INSTALL.md:29) |
| `PROXY_UPSTREAM_URL` / `PROXY_UPSTREAM_API_KEY` / `PROXY_UPSTREAM_MODEL` | proxy | Upstream model the proxy forwards agent traffic to (INSTALL.md:29) |

Standalone Gateway equivalents: `TDAI_LLM_API_KEY`, `TDAI_LLM_BASE_URL`, `TDAI_LLM_MODEL` (README.deployment.md:56); v1 plugin needs `TDAI_LLM_API_KEY` (README.deployment.md:332); v2 plugin needs `TDAI_MEMORY_ENDPOINT=http://127.0.0.1:8420`, `TDAI_MEMORY_API_KEY`, `TDAI_MEMORY_SERVICE_ID` (README.deployment.md:376).

Optional/external services: Redis (`STATE_BACKEND`, `REDIS_HOST/PORT/PASSWORD/KEY_PREFIX`) for service-mode locks/queues; VDB (`VDB_ENDPOINT/USER/API_KEY/DATABASE`) or COS (`COS_SECRET_ID/SECRET_KEY/URL/PATH_PREFIX`) or Shark (`SHARK_BASE_URL`) for service-mode storage (README.deployment.md:157, README.docker.md:163); local `mongodb-atlas-local` auto-starts if `MONGODB_ENDPOINT` unset in mongo mode (INSTALL.md:80); `SCANNER_INTERVAL_MS=500`, `WORKER_POLL_MS=200` tune background workers (README.docker.md:163).

## 5. Experience Lifecycle Pipeline (The Main Pipeline)

The primary workflow is the Memory Hub experience lifecycle: work → assets → circulation → cold start (README.md:103-107). Steps with entry points (function-level source lines are not in the available wiki subset, which covers only top-level docs; entry scripts and APIs below are cited to their doc lines):

1. **Boot stack** — `deploy/global-images/start-all.sh` copies `.env.example`→`.env`, walks both LLM groups, probes connectivity, persists `.env`, boots three containers, creates admin via `init-admin` (random 32-char `user_key` in `./.admin-key`), verifies with `POST /v3/meta/auth/verify` (INSTALL.md:29, INSTALL.md:43).
2. **Onboard team/agent** — admin creates Teams/users; business users are created inside a Team's member flow or via `user/create` then `team-member/add` with `team_id`, `user_id`, `role` (INSTALL.md:146, INSTALL.md:193); since 2.0.0 admin can also own assets (INSTALL.md:146).
3. **Point agent at proxy** — export `ANTHROPIC_BASE_URL=http://127.0.0.1:8096/claude-code/default` + `ANTHROPIC_AUTH_TOKEN='sk-mem-…'` and run `claude --model <PROXY_UPSTREAM_MODEL>` (INSTALL.md:43); per-client steps in `INSTALL.md`, generic guide for unlisted agents (README.md:81-83).
4. **Cold-start import** — panel imports codebases → CodeGraph index; documents/files → Wiki pages + link graph; past sessions → Skills + Chat Memory (README.md:170-172).
5. **In-session use** — `mem:sync` refreshes injected assets; `mem:create-skill [prompt]` archives the conversation as an asynchronously extracted Skill; `mem:help` shows help; format `mem:<command>`, no space after colon, case-insensitive (ROADMAP.md:89, ROADMAP.md:93).
6. **Review and share** — panel review/share/equip flow; personal Skills private by default, shared after review and assignable to other agents (README.md:127, README.md:152-153); L1–L3 editing and L0/L1 search are roadmap items, not yet shipped (ROADMAP.md:46, ROADMAP.md:60).

Gateway-level capture/recall APIs backing the pipeline: `POST /recall`, `POST /capture`, `POST /search/memories`, `POST /search/conversations`, `POST /session/end`, `POST /seed`, `GET /health` (README.deployment.md:414, README.docker.md:214); health returns `{status:"ok", version:"0.1.0", services:{timerScanner, pipelineWorker, stateBackend}}` (README.docker.md:90).

## 6. Key Files

Wiki subset covers only top-level docs; module source line counts are not available. Table ordered by structural importance within that scope:

| File | Lines | What It Does |
|---|---|---|
| `README.md` | ~230+ (truncated at Ownership row) | Flagship doc: thesis, install, proxy onboarding, four asset kinds, Hub panel, cold start, RAG comparison |
| `README_CN.md` | 300+ (truncated at community) | Chinese flagship; adds recall budgets, Fixed Binding + ACL, `/v3/tools/*`, v2.0.0 version note |
| `INSTALL.md` / `INSTALL_CN.md` | Partial (INSTALL breaks mid `team/create`) | Three deploy modes, `start-all.sh` flow, ports, mongo backend, team/agent/task model, per-client proxy setup |
| `deploy/global-images/start-all.sh` | n/a (invoked, not quoted) | Interactive three-container boot, LLM probing, admin init, prints paste-ready `claude` block (INSTALL.md:21-43) |
| `deploy/global-images/start-all-mongo.sh` | n/a | Mongo-mode boot; writes `MEMORY_CORE_STORE_MODE=mongodb` (INSTALL.md:80) |
| `deploy/global-images/verify.sh` | n/a | Dry-run check with `--skip-llm` flag (INSTALL.md:39) |
| `MemoryCore/src/gateway/server.ts` | n/a | Gateway entry (`npx tsx src/gateway/server.ts`, listens 8420; README.deployment.md:28) |
| `MemoryCore/` (module) | n/a | Memory kernel: Gateway, four-layer pipeline, Skill extraction (CONTRIBUTING_CN.md:3 layout) |
| `MemoryHub/` + `MemoryPanel/` | n/a | Control plane: Panel UI + Knowledge Service merged image; team memory panel (CONTRIBUTING_CN.md layout) |
| `MemoryKnowledge/` (+ `openapi.yaml`) | n/a | Wiki + CodeGraph service on 8424 (CONTRIBUTING_CN.md:3, README_CN.md:292) |
| `MemoryProxy/` | n/a | Coding-agent LLM request proxy on 8096, dual-protocol (CONTRIBUTING_CN.md:3) |
| `README.deployment.md` | 400+ (partial env table) | Standalone vs Service modes, `TDAI_DEPLOY_MODE` switch, Hermes v1/v2 plugins, v1/v2 APIs |
| `README.docker.md` | ~250 | Image reference (`node:22-slim`, ~920MB, user tdai, tini), compose files, config precedence, API list |
| `ROADMAP.md` / `ROADMAP_CN.md` | ~90 | v2.0.1 plan (templates, Task commands, L1–L3 editing, L0/L1 search, Cursor) + shipped `mem:` commands |
| `CONTRIBUTING_CN.md` | ~146 | Repo layout, prereqs, branch `feat/server_team`, Conventional Commits, DCO sign-off |
| `.gitignore` | ~118+ | Excludes `.env`, `workspace/`, `dist/`, SDK dists, `vectors.db`, `data/*.db`, `.admin-key` |
| `sdk/memory-core/` (TS + Python) | n/a | Official SDKs (CONTRIBUTING_CN.md:3) |
| `MemoryCore/scripts/migrate-v2-to-v3/README.md` | n/a | v1.x/v0.x → v3 migration; skipped on new installs (README.md:56-58) |
| `MemoryPanel/panel-api-doc.md` | n/a | Panel API reference (cited README_CN.md:292) |
| `MemoryKnowledge/openapi.yaml` + v3 API docs | n/a | Knowledge/Core/Proxy v3 API contracts (cited README_CN.md:292) |

## 7. Dependencies

Package-manifest constraints (`package.json` / `requirements.txt`) are not covered by the available wiki subset; only runtime prerequisites and backing services appear. Required first:

| Package | Version constraint | Purpose |
|---|---|---|
| Node.js | `≥ 22.16.0` (CONTRIBUTING_CN.md:38) | All TS modules; Gateway, Panel, Knowledge, Proxy; Docker base `node:22-slim` (README.docker.md:7) |
| npm / pnpm | (no version string in subset) | Per-module `npm install && npm run dev` loop (CONTRIBUTING_CN.md:49) |
| Python | `≥ 3.9` (CONTRIBUTING_CN.md:38) | SDK / migration scripts |
| Docker | (no version string in subset) | Image builds and `deploy/global-images` local deploy (CONTRIBUTING_CN.md:38) |
| tini | (container PID 1, README.docker.md:7) | Container init for `tencentdb-agent-memory` image |
| SQLite (embedded) | default, no version string | Default store on container volume (INSTALL.md:68) |
| MongoDB / mongodb-atlas-local | opt-in via `MEMORY_CORE_STORE_MODE=mongodb` (INSTALL.md:80); local auto-start if `MONGODB_ENDPOINT` unset | Experimental alternate store for L0/L1/profile/skill docs + mongot BM25 |
| Redis | service mode only (`STATE_BACKEND`, `REDIS_HOST/PORT/PASSWORD/KEY_PREFIX`; README.deployment.md:157) | Distributed locks + task queues in multi-tenant service mode |
| TCVDB (`VDB_ENDPOINT/USER/API_KEY/DATABASE`) | service mode only | Vector/document store in service mode |
| COS (`COS_SECRET_ID/SECRET_KEY/URL/PATH_PREFIX`) | service mode only | Object store in service mode |
| Shark (`SHARK_BASE_URL`) | service mode alternative | Alternate service backend / mock via `scripts/mock-shark-server.ts` (README.docker.md:254) |

## 8. CLI / Usage Surface

Entry points:

```bash
git clone https://github.com/TencentCloud/TencentDB-Agent-Memory.git
cd TencentDB-Agent-Memory/deploy/global-images
cp .env.example .env
$EDITOR .env   # fill memory group + proxy group
./start-all.sh # boot memory-core + memory-hub + proxy; prints paste-ready claude block
```

- `./verify.sh` (`--skip-llm` skips LLM probe) — dry-run check (INSTALL.md:39).
- `./start-all-mongo.sh` — mongo-backend boot (INSTALL.md:80).
- Direct Gateway (dev): `cd MemoryCore && npm install`, `export TDAI_LLM_API_KEY/BASE_URL/MODEL`, `npx tsx src/gateway/server.ts` → `http://127.0.0.1:8420` (README.deployment.md:28).
- Docker: `docker build -t tencentdb-agent-memory:latest .` in `MemoryCore/`; `curl http://localhost:8420/health` (README.docker.md:23, README.docker.md:90).
- Panel: `http://localhost:8125` (admin key from `.admin-key`); Knowledge Swagger: `http://localhost:8424/docs` (INSTALL.md:134, INSTALL.md:159).

Commands:

| Command | Scope | Effect |
|---|---|---|
| `mem:sync` | in-session (v2.0.0 shipped) | Refresh every asset injected into this session (ROADMAP.md:89) |
| `mem:create-skill [prompt]` | in-session | Archive conversation as Skill, extracted asynchronously (ROADMAP.md:89) |
| `mem:help` | in-session | Show command help (ROADMAP.md:89) |

Format: `mem:<command>`, no space after colon, case-insensitive (ROADMAP.md:93). Roadmap: Task-scoped `mem:` commands, Agent templates, Cursor support (ROADMAP.md:16-72).

HTTP surface (v1 Gateway, no auth noted): `GET /health`, `POST /recall`, `POST /capture`, `POST /search/memories`, `POST /search/conversations`, `POST /session/end`, `POST /seed` (README.deployment.md:414); plus `POST /v2/*` requiring Bearer Token (README.docker.md:214); v2 resource APIs `/v2/conversation|atomic|scenario|persona/...` (README.deployment.md:426); admin verify `POST /v3/meta/auth/verify`; knowledge on demand `/v3/tools/list` + `/v3/tools/call` (README_CN.md:267).

Env-var and config tables:

| Var | Default / note |
|---|---|
| `MEMORY_LLM_BASE_URL` / `MEMORY_LLM_API_KEY` / `MEMORY_LLM_MODEL` | memory group, walked interactively by `start-all.sh` (INSTALL.md:29) |
| `PROXY_UPSTREAM_URL` / `PROXY_UPSTREAM_API_KEY` / `PROXY_UPSTREAM_MODEL` | proxy group (INSTALL.md:29) |
| `TDAI_LLM_API_KEY` / `TDAI_LLM_BASE_URL` (`https://api.openai.com/v1`) / `TDAI_LLM_MODEL` (`gpt-4o`) | standalone Gateway (README.deployment.md:56) |
| `TDAI_GATEWAY_PORT=8420`, `TDAI_GATEWAY_HOST="127.0.0.1"`, `TDAI_DATA_DIR`, `$TDAI_GATEWAY_CONFIG` → `./tdai-gateway.yaml` → `<dataDir>/tdai-gateway.yaml` | Gateway listen/config search (README.deployment.md:56-71) |
| `TDAI_DEPLOY_MODE` (`standalone` default) | Switches standalone vs service; env > YAML > code defaults (README.deployment.md:20, README.docker.md:116) |
| `MEMORY_CORE_STORE_MODE=mongodb` \| `sqlite`, `MONGODB_ENDPOINT` | Mongo opt-in switch (INSTALL.md:68-95) |
| `MEMORY_TENCENTDB_GATEWAY_PORT=8420` | v1 Hermes plugin (README.deployment.md:332) |
| `TDAI_MEMORY_ENDPOINT`, `TDAI_MEMORY_API_KEY`, `TDAI_MEMORY_SERVICE_ID` | v2 Hermes plugin (README.deployment.md:376) |

Default ports: Memory Core 8420, Panel UI 8125, Knowledge 8424, Proxy 8096 (INSTALL.md:57).

## 9. Extensibility Points

- **New agent clients** — no code change: reuse the proxy's unchanged-protocol path (point base URL at `:8096`); generic guide covers unlisted agents, PRs via `CONTRIBUTING.md` (README.md:64, README.md:81-83). Client-specific work (e.g. Cursor support reusing the same injection/write-back path, ROADMAP.md:72) belongs in `MemoryProxy/`.
- **New memory/asset logic** — `MemoryCore/` (Gateway, four-layer L0→L3 pipeline, Skill extraction; CONTRIBUTING_CN.md layout). Recall tuning (BM25 + vector + RRF, budgets per README_CN.md:258) and state backends (`local` Map/Timer vs Redis; SQLite vs Mongo vs TCVDB+COS per README.deployment.md:10) live here and in gateway YAML (`tdai-gateway.standalone.yaml` vs `tdai-gateway.service.yaml`, README.docker.md:32).
- **Wiki/CodeGraph sources** — `MemoryKnowledge/` (Wiki + CodeGraph service; `openapi.yaml` contract per README_CN.md:292).
- **Team workflows and agent loadouts** — `MemoryHub/` + `MemoryPanel/` (teams/agents/tasks, review/share/equip, Agent templates roadmap item ROADMAP.md:16; `panel-api-doc.md` per README_CN.md:292).
- **SDK consumers** — `sdk/memory-core/` TypeScript/Python SDKs (CONTRIBUTING_CN.md:3); Hermes integrations fork by generation: local/sidecar extends v1 `memory_tencentdb` (self-managed Gateway subprocess), shared/K8s/SaaS extends v2 `memory_tencentdb_v2` over v2 REST (README.deployment.md:398).
- **Deploy variants** — `deploy/` (image builds, `global-images` scripts, compose/YAML templates; README.docker.md:254); standalone↔service switch is config-only via `TDAI_DEPLOY_MODE` (README.deployment.md:20).
- **Contributions** — branch off `feat/server_team`, Conventional Commits (`feat/fix/perf/refactor/docs/test/chore/style/revert` + module scopes `memory-core/panel/knowledge/proxy/sdk-ts/sdk-py/deploy/docs`), DCO `Signed-off-by:` required (CONTRIBUTING_CN.md:61-128); security reports by mail, not public issues (CONTRIBUTING_CN.md:141).

## 10. Limitations and Gotchas

- **Wiki subset is truncated; four files cut mid-content.** `INSTALL.md` breaks off mid `team/create`, `INSTALL_CN.md` mid `sessionInit.defaultTaskId`, `README.deployment.md` mid env-var table, `README_CN.md` at community, and the README RAG table cuts at `Ownership / Versi...` (02-top-level-files.md:174, 01-overview.md:100-107). Do not infer rows beyond the cut.
- **MongoDB backend is experimental and non-migrating.** SQLite is the default on container volume; enabling mongo via `start-all-mongo.sh` (`MEMORY_CORE_STORE_MODE=mongodb`) does not migrate existing data, and switching back is a config change only (INSTALL.md:68-100).
- **Two LLM credential sets are mandatory.** `start-all.sh` walks both the `memory` group and the `proxy` group and probes connectivity, re-prompting on failure (INSTALL.md:29); a single key will not complete setup, and `verify.sh` without `--skip-llm` will attempt the probe (INSTALL.md:39).
- **Permission model split is easy to misread.** Only admin sees "New Team"/"New User"; business users are created inside a Team's member flow or via the two-step `user/create` + `team-member/add` (both admin/team-admin only) — creating a user alone does not add them to a team (INSTALL.md:134-193). System Admin vs. team Admin/Member plus per-asset Owner permission all interact (README.md:155).
- **Hermes plugin generations are not interchangeable.** v1 `memory_tencentdb` self-manages a Gateway subprocess (standalone) while v2 `memory_tencentdb_v2` talks to an external Gateway over v2 REST with `service_id` multi-tenancy; local/Docker uses v1, shared/K8s/SaaS uses v2 (README.deployment.md:307-398). Mixing tools (`memory_tencentdb_*` vs `tdai_*`) across modes fails.
- **In-session Skill capture is async and L1–L3 are not yet editable.** `mem:create-skill` extracts asynchronously (ROADMAP.md:89), so the Skill is not immediately available; correcting distilled L1–L3 memories currently means delete-and-rebuild until the editable-memories roadmap item ships (ROADMAP.md:46). L0/L1 search is likewise roadmap-only (ROADMAP.md:60).

## 11. How It Compares to Alternatives

Available wiki pages compare only against Chat History and Standard RAG (README.md:224-230): cross-session understanding, distilled executable experience (Skill), document structure/link graph (Wiki), and code call-graph/impact scope (CodeGraph) are claimed as differentiators over `—`/`△ Chunk retrieval`/`△ Text match`. Named third-party alternatives below are outside the wiki subset and positioned on that claimed axis:

- **Mem0 / Mem0g (open-source agent memory layer)** — per-agent long-term memory with extraction and scoped recall; closest to Chat Memory L0→L3, but without the team Hub panel, Skill review flow, or Wiki+CodeGraph bundle described here.
- **Zep / Graphiti (temporal knowledge-graph memory service)** — graph-backed session/user memory with its own server; overlaps conversation distillation and recall, but is a developer API rather than a proxy + human-governed team asset system with `private/team/restricted/agent` ACLs.
- **LangChain / LangGraph memory (incl. LangMem) and LlamaIndex memory** — framework-embedded stores (often app-local); this repo inverts the coupling by sitting behind an unchanged-protocol proxy so heterogeneous agents share one server without per-framework plugins.
- **OpenAI / Anthropic managed memory and IDE built-ins (e.g. Cursor memory)** — vendor-locked, single-assistant memory; this repo's positioning is cross-vendor portability ("assets decoupled from frameworks", README.md:105-107) plus cold-start import of repos, docs, and past sessions (README.md:170-172).

Positioning sentence: where framework libraries and vendor memories keep per-assistant recall, this project bundles proxy-level capture, four asset kinds, and human ACL governance so a whole team of heterogeneous agents cold-starts from the same versioned experience.

## Appendix: Selected Code Snippets

1. Reusable-asset pipeline thesis (`README.md:95-97`, via 01-overview.md:33-36):

```text
Existing information → Reusable memory assets → Fewer turns → Less rework → More stable results and higher efficiency
```

2. Full-stack boot and panel (`README.md:36-46`, via 01-overview.md:14-23; INSTALL.md:29):

```bash
git clone https://github.com/TencentCloud/TencentDB-Agent-Memory.git
cd TencentDB-Agent-Memory/deploy/global-images
cp .env.example .env
$EDITOR .env       # Fill in two sets of LLM parameters (memory group + proxy group)
./start-all.sh     # Launch everything with one command; when finished, it prints a one-liner you can paste directly into Claude
# Panel: http://localhost:8125
```

3. Proxy onboarding exports (`INSTALL.md:43`, via 02-top-level-files.md:84):

```bash
export ANTHROPIC_BASE_URL=http://127.0.0.1:8096/claude-code/default
export ANTHROPIC_AUTH_TOKEN='sk-mem-…'
claude --model <PROXY_UPSTREAM_MODEL>
```

4. Health check and `.gitignore` runtime-state guard (`README.docker.md:90`; `.gitignore:2-118` via 02-top-level-files.md:24-42):

```bash
curl http://localhost:8420/health
# → {status:"ok", version:"0.1.0", services:{timerScanner, pipelineWorker, stateBackend}}
```

```gitignore
node_modules/
workspace/
.env
dist/
sdk/typescript/dist/
sdk/python/dist/
vectors.db
data/skills.db
data/tdai-memory.db
coverage/
deploy/global-images/.admin-key
__tests__/offload_server/remote-config.json
```
