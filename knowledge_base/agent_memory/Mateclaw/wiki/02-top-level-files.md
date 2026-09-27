> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** Top-level files define how the MateClaw repo is configured, built, deployed, and presented — Docker build context, environment template, line-ending/checkout policy, ignored paths, and the Chinese-language product README.
## Key points
- `.dockerignore` keeps build context lean by excluding git/IDE artifacts, Node/Maven outputs, the desktop app, data/logs, secrets, and most markdown with narrow re-inclusions (`.dockerignore:1-28`).
- `.env.example` is the single copy-and-rename deployment template (`cp .env.example .env`) where every required-but-unset value fails `docker compose up` instead of shipping defaults (`.env.example:1-6`).
- `.env.example` pins the Docker stack to PostgreSQL 16 (`DB_HOST`, `DB_PORT=5432`, `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`, `DB_ADMIN_USERNAME`, `DB_ADMIN_PASSWORD`) and warns old MySQL volumes need `mysqldump`/migration (`.env.example:8-29`).
- `.env.example` documents all optional runtime tuning under exact names: search keys, `JWT_SECRET`, CORS/public-URL/OpenAPI flags, browser CDP/path/channel, Playwright SSRF/timeout/snapshot limits, OpenAI OAuth mode, wiki allowlist/watcher, skill workspace/upload caps, pip mirror, and Maven flags (`.env.example:31-165`).
- `.gitattributes` pins `*.sh`/`*.bash`/`*.sql` to LF so bind-mounted Linux init scripts and Flyway checksums survive Windows checkouts, while `*.bat`/`*.cmd`/`*.ps1` keep CRLF (`.gitattributes:1-20`).
- `.gitignore` excludes Gradle/Maven/Node/VitePress/Astro build outputs, IDE files, logs, local runtime data (`mateclaw-server/data/`, `.sessions/`, `/data/`), secrets (`.env` but not `.env.example`), SSL certs, and stray npm/yarn lockfiles in this pnpm monorepo (`.gitignore:1-136`).
- `README_zh.md` is the product entry point (v2.3.0, 2026-09-20): pluggable Agent Runtime, provider failover, LLM Wiki, five entrances, quick-start, repo layout, stack table, and roadmap — chunk content is truncated so post-2.1.0 roadmap detail is not covered here (`README_zh.md:33-270`).
---
## .dockerignore
Excludes development, build, and secret artifacts from the Docker build context (`.dockerignore:1-28`):
```dockerignore
# Git and IDE
.git
.idea
*.iml

# Node artifacts
**/node_modules
**/dist
**/.nuxt
**/.output

# Maven build output (will be rebuilt in Docker)
**/target

# Desktop / webchat (not needed for server or sites build)
mateclaw-desktop

# Data and logs
data
*.log

# Misc
.env
*.md
!docs/**/*.md
!matevip-sites/**/*.md
!mateclaw-plugin-api/**
!mateclaw-server/**
```
Notable behavior: `*.md` is ignored by default but `docs/`, `matevip-sites/`, `mateclaw-plugin-api/`, and `mateclaw-server/` markdown paths are re-included (`.dockerignore:24-28`); `mateclaw-desktop` is explicitly not needed for the server/sites build (`.dockerignore:15-16`).
## .env.example
Template with 166 lines; copy to `.env` before `docker compose up` (`.env.example:1-2`):
```bash
cp .env.example .env
```
Required-value enforcement: items marked 必填 abort `docker compose up` via `${VAR:?}` rather than falling back to example values (`.env.example:6`).
### Database (Docker, required)
PostgreSQL 16 is the Docker default; pre-switch MySQL deployments must migrate (`mysqldump`/pgloader) or stay pinned (`.env.example:8-12`):
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mateclaw
DB_USERNAME=mateclaw
DB_PASSWORD=change-me-strong-user-password
DB_ADMIN_USERNAME=mateclaw_admin
DB_ADMIN_PASSWORD=change-me-strong-admin-password
```
`DB_USERNAME` is a least-privilege role created by `docker/postgres/init/10-app-role.sh` on first init, not a superuser (`.env.example:18-20`); both passwords must be changed to distinct strong values (`.env.example:22-29`).
### Config/flags reference
| Variable | Purpose / default noted in template |
|---|---|
| `SERPER_API_KEY` / `TAVILY_API_KEY` | Cloud search APIs for WebSearch tool, either/or/empty; empty falls back to SearXNG sidecar (`.env.example:33-35`) |
| `JWT_SECRET` | JWT signing key; empty uses built-in default with a startup WARN, must be set in production via `openssl rand -base64 48` (`.env.example:39-41`) |
| `MATECLAW_CORS_ALLOWED_ORIGINS` | Comma-separated CORS allowlist; empty allows all origins with WARN (`.env.example:43-45`) |
| `MATECLAW_PUBLIC_BASE_URL` | Absolute base for agent-generated file download links; falls back to request host then relative path (`.env.example:47-50`) |
| `MATECLAW_OPENAPI_EXPOSE_UI` | Exposes `/swagger-ui.html`, `/v3/api-docs`; default false under production DB profiles, admin-only (`.env.example:52-55`) |
| `SEARXNG_SECRET` | Internal SearXNG session key; dev default when empty, use 32+ random chars in production (`.env.example:57-58`) |
| `MATECLAW_BROWSER_CDP_URL` | Browser sidecar CDP endpoint, e.g. `http://chrome-sidecar:9222`; image already bundles Chromium so default is zero-config (`.env.example:61-74`) |
| `MATECLAW_BROWSER_CHROME_PATH` | Non-Playwright browser binary, e.g. `/usr/bin/google-chrome-stable` (`.env.example:75`) |
| `MATECLAW_BROWSER_CHANNEL` | Forced Playwright channel (`chrome` / `msedge` / `chrome-beta` …) (`.env.example:76`) |
| `PLAYWRIGHT_ALLOW_PRIVATE_NETWORK` | Browser SSRF guard for loopback/private IPs; default `false`, must stay false on public deploys (`.env.example:78-81`) |
| `PLAYWRIGHT_IGNORE_HTTPS_ERRORS` | Ignore HTTPS cert errors for self-signed/IP scenarios; must stay `false` publicly (`.env.example:82-84`) |
| `PLAYWRIGHT_DEFAULT_TIMEOUT_SECONDS=30` | Per-operation timeout, raisable on slow links (`.env.example:86`) |
| `PLAYWRIGHT_NAVIGATION_TIMEOUT_SECONDS=30` | Navigation timeout, raisable on slow networks (`.env.example:88`) |
| `PLAYWRIGHT_SNAPSHOT_MAX_LENGTH=20000` | Snapshot text truncation; overflow returns `truncated:true` hint to narrow by selector (`.env.example:90`) |
| `MATECLAW_OAUTH_OPENAI_DEPLOYMENT_MODE` | Force `local` / `device_code` / `manual_paste`; empty auto-selects LOCAL on localhost, DEVICE_CODE on IP/domain (`.env.example:92-108`) |
| `MATECLAW_OAUTH_OPENAI_CALLBACK_BIND_HOST` | Set `0.0.0.0` with `1455:1455` mapping for in-Docker localhost PKCE callback (`.env.example:109`) |
| `MATE_WIKI_ALLOWED_SOURCE_ROOTS` | Wiki directory-scan allowlist, comma-separated, e.g. `/data/wiki,/opt/docs`; empty forbids all scans, fail-closed (`.env.example:111-122`) |
| `MATE_WIKI_WATCHER_ENABLED=false` | Master switch for wiki source auto-sync; AND-semantics with per-library switch, manual scan unaffected (`.env.example:124-128`) |
| `MATE_WIKI_WATCHER_INTERVAL_MS=300000` | Global auto-sync interval, 5 minutes, no per-library override (`.env.example:130`) |
| `MATECLAW_SKILL_WORKSPACE_ROOT` | Installed skills + `LESSONS.md` + run artifacts; container default `/app/data/skills` persisted by `server_data` volume (`.env.example:132-139`) |
| `MATECLAW_SKILL_UPLOAD_MAX_ENTRY_SIZE_MB` | Per-file skill ZIP cap; default 1MB, peak install memory scales with the whole-package cap (`.env.example:141-145`) |
| `MATECLAW_SKILL_UPLOAD_MAX_TOTAL_SIZE_MB` | Whole-package cap; default 50MB; note Spring `spring.servlet.multipart` caps (100MB/200MB) (`.env.example:141-145`) |
| `PIP_INDEX_URL` / `PIP_TRUSTED_HOST` | Pip mirror for skill Python deps; Tsinghua and LAN-private-source examples given, HTTP sources auto-derive trusted host (`.env.example:148-155`) |
| `MATECLAW_PIP_INDEX_URL` / `MATECLAW_PIP_TRUSTED_HOST` | Desktop (non-Docker) equivalents injected via Spring config (`.env.example:157-160`) |
| `MAVEN_FLAGS=-Paliyun-first` | Commented out by default; uncomment in mainland China to prefer Aliyun repo, else US Central → Google CDN → Aliyun order (`.env.example:162-165`) |
## .gitattributes
Full 20-line policy (`.gitattributes:1-20`):
```gitattributes
*.sh   text eol=lf
*.bash text eol=lf
*.sql  text eol=lf

# Windows-native scripts keep CRLF.
*.bat  text eol=crlf
*.cmd  text eol=crlf
*.ps1  text eol=crlf
```
Rationale recorded in-file: shell scripts bind-mount into Linux containers (`docker/postgres/init/` → `/docker-entrypoint-initdb.d`), so a Windows CRLF checkout breaks the `#!/bin/sh` shebang; SQL is pinned to LF so Flyway migration checksums are identical across platforms (`.gitattributes:3-11`).
## .gitignore
136-line ignore set (`.gitignore:1-136`). Verbatim excerpts by group:
```
.gradle
/build/
!gradle/wrapper/gradle-wrapper.jar
```
```
mateclaw-ui/dist/
```
```
target/
*.war
*.ear
```
```
mateclaw-server/src/main/resources/static/
**/${project.build.directory}/
```
```
mateclaw-server/data/
.sessions/
/data/
```
```
.env
.env.local
.env.*.local
!.env.example
!**/.env.example
```
```
package-lock.json
yarn.lock
```
Groups present: Gradle/STS/IDEA/NetBeans outputs (`.gitignore:2-29`); Vite primary output note — only `stats.html` from `ANALYZE=1 pnpm build` lands in `mateclaw-ui/dist/` (`.gitignore:31-34`); Maven artifacts (`.gitignore:36-42`); logs/temp/system files (`.gitignore:44-64`); Node, `pom.xml.versionsBackup`, `.flattened-pom.xml`, `.cursor`, `.gstack/` (`.gitignore:66-74`); static build output and unresolved `${project.build.directory}` guard (`.gitignore:76-80`); local runtime data (`.gitignore:82-85`); VitePress/Astro caches, SSL certs under `deploy/nginx/ssl/` (`.gitignore:87-97`); secrets with `.env.example` templates kept tracked (`.gitignore:99-105`); Claude Code/Codex local settings, `.codebase-memory/`, sync-tool state, `outputs/` sandbox dir (`.gitignore:107-123`); pnpm-only lockfile rule ignoring npm/yarn lockfiles (`.gitignore:125-128`); Python `__pycache__/` + `*.pyc` from skill scripts (`.gitignore:130-132`).
## README_zh.md
Chinese-language product README, 338 lines in source; the chunk is truncated (3809 further characters cut), so claims below cover only the visible portion (`README_zh.md:1-270`).
- Product frame: 太一（MateClaw）, "你的超级大脑", pluggable Agent Runtime · Native + DSH · Spring Boot kernel; badges link repo, docs at `https://claw.mate.vip/docs`, demo, site, Java 21+, Spring Boot 3.5, Vue 3 (`README_zh.md:1-23`).
- Current release banner: v2.3.0 (2026-09-20) — JSON acceptance with required fields bound to requirements and immutable artifact versions, plus controlled member intervention, skill docs/folder upload, DSH history/output-budget, vLLM reasoning, and SSE framing fixes (`README_zh.md:33`).
- Positioning: multi-user workspace, approval-gated sensitive ops, audit log, Actuator health, per-channel error isolation, single-JAR self-hosted deployment; Native StateGraph (ReAct, Plan-and-Execute, Goal, Team Run) or managed external loop via authenticated JSON-RPC to DeepSeek Harness, sharing session/workspace/Tool Guard/event-projection/lifecycle (`README_zh.md:37-42`).
- Three differentiators: cross-vendor failover chain (DashScope, OpenAI, Anthropic, Gemini, DeepSeek, Kimi, Ollama, LM Studio, MLX) with Provider Health Tracker cooldowns (`README_zh.md:51-57`); LLM Wiki digesting PDF/markdown/pages into linked pages with traceable citations and chunk drawer (`README_zh.md:59-65`); five entrances — Web console, Electron desktop, embeddable `<script>` webchat, IM channels (DingTalk/Feishu/WeCom/WeChat/Telegram/Discord/QQ/Slack), plugin SDK (`README_zh.md:67-77`).
- Quick start (verbatim, `README_zh.md:163-180`):
```bash
# 后端
cd mateclaw-server
mvn spring-boot:run           # http://localhost:18088

# 前端
cd mateclaw-ui
npm install && npm run dev    # http://localhost:5173
```
Default login `admin` / `admin123`; Docker via `cp .env.example .env` + `docker compose up -d` (`http://localhost:18080`); desktop via GitHub Releases with embedded JRE 21 (`README_zh.md:173-184`).
- Repo layout (verbatim, `README_zh.md:203-217`):
```
mateclaw/
├── mateclaw-server/        Spring Boot 3.5 后端（Agent Runtime contract · Native StateGraph + DSH）
├── mateclaw-ui/            Vue 3 + TypeScript 管理 SPA（构建产物打进后端 JAR）
├── mateclaw-desktop/       Electron 桌面端（本地内嵌 / 远程集中双模式）
├── mateclaw-webchat/       网页嵌入式聊天组件（UMD / ES bundle）
├── mateclaw-plugin-api/    第三方能力插件的 Java SDK
├── mateclaw-plugin-sample/ 参考插件实现
├── mateclaw-plugin-mem0/   可选 Mem0 记忆 Provider 插件
├── mateclaw-plugin-search-sample/ 搜索 Provider SPI 示例
├── docker-compose.yml
└── .env.example
```
- Stack table rows present: Spring Boot 3.5 · Spring AI Alibaba 1.1 · MyBatis Plus · Flyway; `AgentRuntimeProvider` contract; workflows/triggers/wiki-processor; SKILL.md/MCP/ACP; H2/PostgreSQL 16/MySQL 8.0+/Kingbase; Spring Security + JWT; Vue 3/Vite/Element Plus/TailwindCSS 4; Electron; Vite-library webchat (`README_zh.md:221-233`).
- Truncation note: roadmap detail beyond the visible v2.3.0/v2.2.0/v2.1.0 entries was cut in the chunk and is not summarized here.
**Covers:** `.dockerignore`, `.env.example`, `.gitattributes`, `.gitignore`, `README_zh.md` (truncated in chunk: 338 lines with 3809 further characters cut)
