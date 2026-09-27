> [[index|Wiki]] | [[summary|Summary]]
# TencentCloud/TencentDB-Agent-Memory — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** TencentDB Agent Memory is a shared Memory Hub + Proxy system that turns past conversations, documents, and code into reusable team memory assets (Chat Memory, Skills, Wiki, CodeGraph) so any agent can cold-start from experience instead of relearning.
## Key points
- The project ships three services launched together with one command (`memory-core` + `memory-hub` + `proxy`), with the web panel at `http://localhost:8125` (README.md:36-46).
- One Proxy gives zero-code integration for many agents: pointing an agent's base URL at the Proxy is enough, with no plugin, hook, or MCP server required (README.md:62-64).
- The core model is "memory assets, not chat logs": existing information becomes reusable assets that reduce turns and rework (README.md:93-97).
- Memory Hub closes the experience lifecycle loop: automatic asset extraction, portable multi-agent assets, and cold-start import of docs, code, and sessions (README.md:103-107).
- Chat Memory distills L0 Conversation → L1 Atom → L2 Scenario → L3 Persona, giving each agent its own persistent memory of preferences, facts, and decisions (README.md:113-115).
- Skills are versioned, reviewable executable experience (trigger boundaries, execution steps, validation rules), private by default and shareable to the team after review (README.md:125-127).
- Wiki plus CodeGraph cover docs and code jointly: Wiki builds structured pages with a link graph while CodeGraph indexes symbols, calls, and impact paths for pre-edit impact analysis (README.md:137-144).
- Human control is explicit: teams/agents are managed in Memory Hub with `private` / `team` / `restricted` (User/Role/Agent ACLs) visibility, global System Admin vs. team Admin/Member roles, and Owner-tracked assets (README.md:152-155).

## 2. [[wiki/02-top-level-files|Top-Level Files]]
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

## The system in five moves
1. Repetitive agent work motivates turning existing conversations, documents, and code into reusable memory assets instead of relearning each session.
2. Three services (memory-core + memory-hub + proxy) boot together via `./start-all.sh` on fixed ports, with one Proxy giving zero-code agent integration.
3. The Memory Hub distills experience into four asset types: L0→L3 Chat Memory, versioned reviewable Skills, Wiki pages with link graph, and CodeGraph with call/impact paths.
4. Human control governs the assets through teams, agents, Owner tracking, `private`/`team`/`restricted` visibility, and admin-vs-member roles.
5. New agents cold-start from the team's save file by importing codebases, documents, and past sessions rather than retraining.
6. Repo-top-level files steer what comes next: deploy modes, contribution rules, and the v2.0.1 roadmap (Agent templates, `mem:` commands, editable memories, Cursor support).
