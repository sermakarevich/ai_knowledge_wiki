> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Top-Level Files

**In one sentence:** The repo-top-level files define how to install, deploy, contribute to, and steer TencentDB Agent Memory (memory-core + memory-hub + proxy stack with L0→L3 memory).

## Key points

- The three-in-one install (`memory-core` + `memory-hub` + `proxy`) is booted interactively via `./start-all.sh` from `deploy/global-images`, which probes LLM connectivity and prints a ready-to-run `claude` block (INSTALL.md:21, INSTALL.md:29).
- Default ports are fixed: Memory Core `8420`, Panel UI `8125`, Knowledge `8424`, Proxy `8096` (INSTALL.md:57, INSTALL_CN.md:53).
- MongoDB is an opt-in experimental storage backend enabled by `./start-all-mongo.sh` writing `MEMORY_CORE_STORE_MODE=mongodb`; sqlite stays the default and switching backends does not migrate data (INSTALL.md:68, INSTALL.md:80, INSTALL.md:100).
- Post-deploy use requires a `team / agent / task` triple with an admin-vs-business-user permission split, where only admin sees "New Team"/"New User" entries and business users are created inside a Team's member flow or via `user/create` + `team-member/add` (INSTALL.md:134, INSTALL.md:146, INSTALL.md:193).
- Two Hermes plugin generations exist: v1 `memory_tencentdb` (self-managed Gateway subprocess, standalone) vs v2 `memory_tencentdb_v2` (external Gateway over v2 REST, service/K8s/multi-tenant) (README.deployment.md:307, README.deployment.md:352, README.deployment.md:398).
- Contributions target branch `feat/server_team` by default, use Conventional Commits types (`feat`/`fix`/`perf`/`refactor`/`docs`/`test`/`chore`/`style`/`revert`) with module scopes, and require a DCO `Signed-off-by:` line (CONTRIBUTING_CN.md:61, CONTRIBUTING_CN.md:92, CONTRIBUTING_CN.md:128).
- The roadmap's next release is v2.0.1 (current v2.0.1-beta.1) with Agent templates, `mem:` Task commands, editable L1–L3 memories, L0/L1 search, and Cursor support; shipped `mem:` commands are `mem:sync`, `mem:create-skill [prompt]`, `mem:help` (ROADMAP.md:6, ROADMAP.md:16, ROADMAP.md:89).
- `.gitignore` keeps runtime secrets, volumes, and build outputs out of VCS, including `.env`, `workspace/`, `dist/`, SDK `dist/`, `vectors.db`, `data/*.db`, and `deploy/global-images/.admin-key` (`.gitignore:2`, `.gitignore:8`, `.gitignore:25`, `.gitignore:118`, `.gitignore:67`).

---

## `.gitignore`

Excludes dependencies, runtime state, secrets, and build outputs from VCS:

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

- Dependencies and caches: `node_modules/` (`.gitignore:2`), `__pycache__/`, `*.pyc`, `.vite/` (`.gitignore:14`, `.gitignore:57`).
- Runtime workspace and secrets: `workspace/` (`.gitignore:5`), `.env` plus `.env.*` except `!.env.example` (`.gitignore:8`, `.gitignore:60`), offload-server `remote-config.json` (`.gitignore:64`), start-all.sh outputs `.admin-key`, `.proxy-config/`, `.memory-core-config/` (`.gitignore:67`).
- Build outputs: root `dist/` (`.gitignore:25`), `sdk/typescript/dist/`, `sdk/python/dist/` (`.gitignore:52`), `*.tsbuildinfo`, `*.js.map` (`.gitignore:47`), tarballs `*.tgz`/`*.tar.gz` (`.gitignore:42`).
- Runtime data (never commit): `vectors.db` (`.gitignore:78`), `data/skills.db`, `data/tdai-memory.db`, `**/data/vectors.db`, `**/data/knowledge.db*` (`.gitignore:118`).

## `CONTRIBUTING_CN.md`

Chinese contribution guide covering all open modules (`MemoryCore` / `MemoryPanel` / `MemoryKnowledge` / `MemoryProxy` + SDK) (CONTRIBUTING_CN.md:3).

Repo layout excerpt:

```text
tdai-memory-openclaw-plugin/
├── MemoryCore/          # 记忆内核（Gateway、四层记忆管线、Skill 抽取）
├── MemoryHub/           # 管控面（Panel UI + Knowledge Service，合并镜像）
├── MemoryPanel/         # 团队记忆面板
├── MemoryKnowledge/     # 知识服务（Wiki + CodeGraph）
├── MemoryProxy/         # 面向 coding agent 的 LLM 请求代理
├── sdk/memory-core/     # 官方 TypeScript / Python SDK
├── deploy/              # 镜像构建 & 本地部署脚本
```

- Prereqs: Node.js ≥ 22.16.0, npm/pnpm, Python ≥ 3.9 for SDK/migration scripts, Docker for images (CONTRIBUTING_CN.md:38).
- Local loop: `git clone …/TencentDB-Agent-Memory.git`, `cd …/deploy/global-images`, `cp .env.example .env`, `./start-all.sh`, then per-module `cd <module> && npm install && npm run dev` (CONTRIBUTING_CN.md:49).
- Submit flow defaults to feature branch off `feat/server_team` (`git switch -c fix/xxx-issue origin/feat/server_team`), run `npm test`, open PR to the same base (CONTRIBUTING_CN.md:61).
- Commit type table (`type` / 说明): `feat` 新功能, `fix` Bug 修复, `perf` 性能优化, `refactor` 重构, `docs` 文档更新, `test` 测试相关, `chore` 构建/依赖/工具变更, `style` 格式化, `revert` 回滚 (CONTRIBUTING_CN.md:92); recommended `scope`: `memory-core` / `panel` / `knowledge` / `proxy` / `sdk-ts` / `sdk-py` / `deploy` / `docs` (CONTRIBUTING_CN.md:104).
- DCO: `git commit -s -m "feat(memory-core): ..."`; missing `Signed-off-by:` is not merged (CONTRIBUTING_CN.md:128).
- Security: do not open public Issues; mail `agentmemory@tencent.com` (CONTRIBUTING_CN.md:141); contributions licensed under MIT `LICENSE` (CONTRIBUTING_CN.md:146).

## `INSTALL.md` / `INSTALL_CN.md`

English (`INSTALL.md`) and Simplified-Chinese (`INSTALL_CN.md`) guides for the same three modes (INSTALL.md:5, INSTALL_CN.md:5):

1. Full three-in-one stack (recommended); 2. Memory Hub only; 3. Proxy with Claude Code (INSTALL.md:7).

Full-stack boot:

```bash
git clone https://github.com/TencentCloud/TencentDB-Agent-Memory.git
cd TencentDB-Agent-Memory/deploy/global-images
./start-all.sh
```

- `start-all.sh` copies `.env.example`→`.env`, walks the `memory` group (`MEMORY_LLM_BASE_URL` / `MEMORY_LLM_API_KEY` / `MEMORY_LLM_MODEL`) and `proxy` group (`PROXY_UPSTREAM_URL` / `PROXY_UPSTREAM_API_KEY` / `PROXY_UPSTREAM_MODEL`), probes LLM connectivity with re-entry on failure, persists to `.env`, then boots three containers (INSTALL.md:29).
- Dry-run check: `./verify.sh` (`--skip-llm` skips probe) (INSTALL.md:39).
- First boot creates admin via `init-admin` (random 32-char `user_key` in `./.admin-key`), verifies with `POST /v3/meta/auth/verify`, prints `export ANTHROPIC_BASE_URL=http://127.0.0.1:8096/claude-code/default` + `export ANTHROPIC_AUTH_TOKEN='sk-mem-…'` + `claude --model <PROXY_UPSTREAM_MODEL>` (INSTALL.md:43).

Default ports:

| Service | Port | Purpose |
|---|---|---|
| Memory Core | `8420` | memory read/write, auth, skill/RAG data plane |
| Panel UI | `8125` | team memory control panel |
| Knowledge | `8424` | wiki / code-graph service |
| Proxy | `8096` | LLM request proxy (Anthropic / OpenAI dual-protocol) |

(INSTALL.md:57; same table in INSTALL_CN.md:53.)

- MongoDB backend (experimental, off by default): sqlite is default on container volume; Mongo covers L0/L1/profile/skill docs plus mongot BM25 with metadata co-located; enable via `./start-all-mongo.sh` (writes `MEMORY_CORE_STORE_MODE=mongodb`); unset `MONGODB_ENDPOINT` starts local `mongodb-atlas-local`; disable by commenting out `MEMORY_CORE_STORE_MODE` or setting `sqlite` (INSTALL.md:68, INSTALL.md:80, INSTALL.md:95).
- Panel at `http://localhost:8125` (admin key from `.admin-key`); Knowledge Swagger at `http://localhost:8424/docs` (INSTALL.md:134, INSTALL.md:159); permission model: admin creates Teams/users, business users manage assets inside joined Teams; since 2.0.0 stable admin can also own assets (INSTALL.md:146).
- Business-user creation is two API steps (both admin/team-admin only): `user/create` (account only) then `team-member/add` with `team_id`, `user_id`, `role` (INSTALL.md:193).

## `README.deployment.md`

Deployment/integration guide for standalone vs service modes plus Hermes plugins (README.deployment.md:2).

| 形态 | 后端存储 | 状态后端 | 多租户 | 适用场景 |
|---|---|---|---|---|
| **Standalone（开源单机版）** | SQLite + 本地文件 | 进程内 Map / Timer | 单空间 | 本地开发、单 Agent sidecar、Docker 一体化、离线部署 |
| **Service（云服务化版）** | TCVDB + COS | Redis（分布式锁 + 任务队列） | 多空间 per-`service_id` | K8s 多副本、多租户 SaaS、多 Agent 共享记忆 |

(README.deployment.md:10.) Both share one Gateway binary and v1/v2 HTTP APIs; switch via `TDAI_DEPLOY_MODE` (README.deployment.md:20).

- Quickstart: `cd MemoryCore && npm install`, `export TDAI_LLM_API_KEY/BASE_URL/MODEL`, `npx tsx src/gateway/server.ts`; Gateway listens `http://127.0.0.1:8420`, data in `~/.memory-tencentdb/memory-tdai/` (README.deployment.md:28, README.deployment.md:40).
- Standalone env: `TDAI_LLM_API_KEY`, `TDAI_LLM_BASE_URL` (default `https://api.openai.com/v1`), `TDAI_LLM_MODEL` (default `gpt-4o`), `TDAI_GATEWAY_PORT=8420`, `TDAI_GATEWAY_HOST="127.0.0.1"`, `TDAI_DATA_DIR` (README.deployment.md:56); config search order `$TDAI_GATEWAY_CONFIG` → `./tdai-gateway.yaml` → `<dataDir>/tdai-gateway.yaml` (README.deployment.md:71).
- Service env: `TDAI_DEPLOY_MODE="service"`, Redis (`STATE_BACKEND`, `REDIS_HOST/PORT/PASSWORD/KEY_PREFIX`), VDB (`VDB_ENDPOINT/USER/API_KEY/DATABASE`) or COS (`COS_SECRET_ID/SECRET_KEY/URL/PATH_PREFIX`), or Shark (`SHARK_BASE_URL`) (README.deployment.md:157).
- v1 plugin `memory_tencentdb`: env `TDAI_LLM_API_KEY`, `MEMORY_TENCENTDB_GATEWAY_PORT=8420`, tools `memory_tencentdb_memory_search` / `memory_tencentdb_conversation_search` (README.deployment.md:332, README.deployment.md:341).
- v2 plugin `memory_tencentdb_v2`: env `TDAI_MEMORY_ENDPOINT=http://127.0.0.1:8420`, `TDAI_MEMORY_API_KEY`, `TDAI_MEMORY_SERVICE_ID`; tools `tdai_memory_search` (`query`, `limit`=5), `tdai_conversation_search`, `tdai_read_scene` (`scene_id`) (README.deployment.md:376, README.deployment.md:384).
- Selection: local/Docker → v1 + standalone (plugin-managed); shared/K8s/SaaS → v2 + service (README.deployment.md:398).
- v1 API: `GET /health`, `POST /recall`, `POST /capture`, `POST /search/memories`, `POST /search/conversations`, `POST /session/end`, `POST /seed` (README.deployment.md:414); v2 API: `/v2/conversation/{add,query,search,delete}`, `/v2/atomic/{add,query,search,delete}`, `/v2/scenario/{ls,read,write,rm}`, `/v2/persona/{read,write}` (README.deployment.md:426).

## `README.docker.md`

Docker reference for `tencentdb-agent-memory` (README.docker.md:1).

| 项目 | 值 |
|---|---|
| 镜像名 | `tencentdb-agent-memory` |
| 基础镜像 | `node:22-slim` |
| 大小 | ~920MB |
| 端口 | 8420 |
| 运行用户 | tdai (uid 10001) |
| PID 1 | tini |

(README.docker.md:7.)

- Build: `docker build -t tencentdb-agent-memory:latest .` (run in `MemoryCore/`) (README.docker.md:23); templates `tdai-gateway.standalone.yaml` (local) vs `tdai-gateway.service.yaml` (K8s/multi-tenant) (README.docker.md:32); verify `curl http://localhost:8420/health` → `{status:"ok", version:"0.1.0", services:{timerScanner, pipelineWorker, stateBackend}}` (README.docker.md:90).
- Config precedence: env vars > `tdai-gateway.yaml` > code defaults; container config path from `TDAI_GATEWAY_CONFIG` (default `/data/config/tdai-gateway.yaml`) (README.docker.md:116).
- Env↔YAML map includes `TDAI_DEPLOY_MODE`↔`deployMode` (`standalone`), `TDAI_LLM_API_KEY`↔`llm.apiKey`, `REDIS_HOST/PORT/PASSWORD/KEY_PREFIX`, `SHARK_BASE_URL`, `STATE_BACKEND` (`redis`/`local`), `SCANNER_INTERVAL_MS=500`, `WORKER_POLL_MS=200` (README.docker.md:163).
- API: `GET /health`, `POST /recall`, `POST /capture`, `POST /search/memories`, `POST /search/conversations`, `POST /session/end`, `POST /v2/*` (v2 needs Bearer Token) (README.docker.md:214).
- Layout: `MemoryCore/Dockerfile`, `docker-compose.local.yaml`, `tdai-gateway.standalone.yaml`, `tdai-gateway.service.yaml`, `scripts/mock-shark-server.ts`, `src/gateway/server.ts` (README.docker.md:254).

## `README_CN.md`

Chinese flagship README: tagline "让 Agent 沉淀经验，让人专注创造" (README_CN.md:5); install is the same three-piece `deploy/global-images` + `cp .env.example .env` + `./start-all.sh` flow, panel at `http://localhost:8125`, details deferred to `INSTALL_CN.md` (README_CN.md:36, README_CN.md:45).

- Proxy: one proxy, unchanged protocol, zero-code onboarding by pointing the Agent's base URL at it (README_CN.md:57).
- Memory growth L0 Conversation → L1 Atom → L2 Scenario → L3 Core/Persona (README_CN.md:102, README_CN.md:252); recall layers L2/L3 for context, BM25 + vector + RRF back to L1/L0 under count/char/timeout budgets (README_CN.md:258).
- Memory assets (Chat Memory, Skill, Wiki, CodeGraph) bound via Fixed Binding + ACL; knowledge exposed via `/v3/tools/list` + `/v3/tools/call` on demand (README_CN.md:262, README_CN.md:267).
- Visibility: `private` (owner only), `team` (team-readable), `restricted` (User/Role/Agent ACL), `agent` (directed same-team assembly) (README_CN.md:232).
- Related docs: `ROADMAP_CN.md`, `INSTALL_CN.md`, `MemoryCore/scripts/migrate-v2-to-v3/README_CN.md`, `MemoryKnowledge/openapi.yaml`, v3 API docs for MemoryCore/MemoryKnowledge/MemoryProxy, `MemoryPanel/panel-api-doc.md`, `CONTRIBUTING_CN.md` (README_CN.md:292).
- Current version v2.0.0 (v2.0.1 priorities: zero-config cold start, faster Wiki, custom prompts, Skill export, Codex IDE Plan-mode) (README_CN.md:305).

## `ROADMAP.md` / `ROADMAP_CN.md`

Forward-looking plan; shipped history lives in `CHANGELOG.md` (ROADMAP.md:3). Current release v2.0.1-beta.1 (ROADMAP.md:6, ROADMAP_CN.md:5); scope/timing may change, feedback via Discussions (ROADMAP.md:10).

Next release v2.0.1 items (module-tagged):

- Agent templates (Memory Hub): admins define default-Agent asset loadout per team (ROADMAP.md:16).
- `mem:` commands extended around Tasks (Memory Proxy): in-conversation Task create/update, effective within session; today only `sync`/`create-skill`/`help` (ROADMAP.md:33).
- Editable L1–L3 memories in panel (Memory Hub): correct instead of delete-and-rebuild (ROADMAP.md:46).
- L0/L1 memory search (Memory Hub): complements time-range filtering (ROADMAP.md:60).
- Cursor support (Memory Proxy) reusing the same injection/write-back path (ROADMAP.md:72).

Shipped `mem:` session commands (v2.0.0):

| Command | What it does |
|---|---|
| `mem:sync` | Refresh every asset injected into this session |
| `mem:create-skill [prompt]` | Archive this conversation as a Skill, extracted asynchronously |
| `mem:help` | Show command help |

(ROADMAP.md:89; Chinese mirror ROADMAP_CN.md:81.) Format `mem:<command>`, no space after colon, case-insensitive (ROADMAP.md:93).

> Truncation note: the chunk embeds full `.gitignore`, `CONTRIBUTING_CN.md`, `README.docker.md`, `ROADMAP.md`, and `ROADMAP_CN.md`, but cuts four files — `INSTALL.md` (breaks off mid `team/create` API), `INSTALL_CN.md` (breaks off mid `sessionInit.defaultTaskId`), `README.deployment.md` (breaks off mid full-env-var table), and `README_CN.md` (breaks off at the community section) — so claims above for those four cover only the visible portion and do not guess the cut remainder.

**Covers:** `.gitignore`, `CONTRIBUTING_CN.md`, `INSTALL.md`, `INSTALL_CN.md`, `README.deployment.md`, `README.docker.md`, `README_CN.md`, `ROADMAP.md`, `ROADMAP_CN.md`
