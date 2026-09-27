[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
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
---
## Installation (memory-core + memory-hub + proxy)
Start all three services in one go (README.md:36-44):
```bash
git clone https://github.com/TencentCloud/TencentDB-Agent-Memory.git
cd TencentDB-Agent-Memory/deploy/global-images
cp .env.example .env
$EDITOR .env       # Fill in two sets of LLM parameters (memory group + proxy group)
./start-all.sh     # Launch everything with one command; when finished, it prints a one-liner you can paste directly into Claude
```
Panel: `http://localhost:8125` (README.md:46).
Full deployment details (standalone Memory Hub, Proxy + Claude Code / CodeBuddy usage, stop/cleanup, ports) live in `INSTALL.md` / `INSTALL_CN.md` (README.md:48). MongoDB storage backend is experimental and off by default (README.md:49-50). Older v1.x/v0.x data is migrated with `MemoryCore/scripts/migrate-v2-to-v3/README.md`; new installs skip this (README.md:56-58).
## All agents share the same memory server
One Proxy, unchanged protocol, zero-code integration — "point the Agent's base URL to the Proxy and it's done" (README.md:64). Supported clients listed (README.md:66-79):
| Row | Agents |
|---|---|
| 1 | DeepSeek Harness, Claude Code, Codex, CodeBuddy |
| 2 | WorkBuddy, Hermes, OpenClaw, More frameworks coming soon... |
Exact per-client steps are in `INSTALL.md`; a generic guide covers unlisted agents, with PRs invited via `CONTRIBUTING.md` (README.md:81-83).
## What it is: from repetitive work to reusable assets
Motivating question: "How do you reduce repetitive work when using Agents?" (README.md:89). Project context, read documents, and working workflows should not be re-explained, re-read, or rediscovered each session (README.md:91). Verbatim pipeline (README.md:95-97):
```text
Existing information → Reusable memory assets → Fewer turns → Less rework → More stable results and higher efficiency
```
Memory means "any information that helps the next Agent avoid reinventing the wheel should be saved, organized, and reused" (README.md:93).
## Experience lifecycle (Memory Hub)
Work produces assets, assets circulate, new members load the team's save file on day one (README.md:103). Three properties (README.md:105-107):
1. **Automatic asset extraction**: Chat Memory and Skills from conversations/tasks; docs and code into Wiki and CodeGraph; managed, reviewed, routed consistently.
2. **Portable & multi-Agent compatible**: assets decoupled from frameworks; shared/maintained by multiple agents and members.
3. **Cold-start friendly**: import docs, codebases, and past sessions; start from existing experience.
## Chat Memory: a brain that remembers people and context
- Retains preferences, facts, decisions, interaction history; each agent automatically gets its own memory (README.md:113-114).
- Distillation layers: `L0 Conversation → L1 Atom → L2 Scenario → L3 Persona` (README.md:115).
- Motivating quote: "Don't refactor the old auth module — mobile is still using it." (README.md:119).
## Skill library: accumulated expertise
- Extracted after complex work from conversations and tool calls; imported into a designated agent's context when needed (README.md:125).
- A Skill has versions, resource files, trigger boundaries, execution steps, and validation rules — not just a prompt snippet (README.md:126).
- Personal Skills private by default; shared team-wide after review and assignable to other agents (README.md:127). Examples: troubleshooting, code review, release checklists (README.md:131).
## Knowledge map: Wiki + CodeGraph
- **Wiki** turns product docs, design specs, ops runbooks into structured pages with a link graph (README.md:137).
- **CodeGraph** indexes code symbols, files, call relationships, impact paths (README.md:141).
- Agents can search, read, inspect callers/callees, and run impact analysis before modifying code (README.md:144). Wiki avoids re-listing files; CodeGraph answers "changing this might affect those" (README.md:146).
## Team memory panel (human-controlled)
- Create teams and agents; review, share, equip assets; manage ownership, versions, status, visibility, usage counts, agent bindings in one place (README.md:152-153).
- Visibility levels (README.md:154):
| Level | Meaning |
|---|---|
| `private` | Belongs strictly to the Owner |
| `team` | Visible to all team members |
| `restricted` | Precise access via User / Role / Agent ACLs |
- Roles: global **System Admin** (users/teams plus asset features) vs. team-level **Admin** and **Member**; Owner auto-holds management permission on owned assets (README.md:155).
## Cold start: load the save file
Thesis: "Stop retraining every Agent. Give it the save file." (README.md:174). Panel-importable inputs with automatic processing (README.md:170-172):
| Import | Result |
|---|---|
| Codebases (existing repos) | CodeGraph indexes symbols, files, calls, impact paths |
| Documents & files | Wiki generates structured pages with link graph |
| Conversation sessions (past agent sessions) | Skills and Chat Memory extracted as reusable assets |
## Team play style: one-person company squad
Verbatim org (README.md:182-189):
```text
Tiny but Serious Inc.
├── 👤 You · Set goals / Make decisions
├── 🔭 Scout · Research / Find opportunities
├── 🛠 Builder · Write code / Build products
├── 🧪 Reviewer · Test / Find issues
└── 🧠 Agent Memory · Preserve the team's experience
```
Recruit first, then equip — verbatim loadouts (README.md:197-212):
```text
🔭 Scout
   ├── User interview Chat Memory
   ├── Market research Wiki
   └── Competitive analysis Skill

🛠 Builder
   ├── Product Wiki
   ├── Project CodeGraph
   └── Feature Delivery Skill

🧪 Reviewer
   ├── Historical incident Chat Memory
   ├── Project CodeGraph
   └── Release Checklist Skill
```
"Different roles, different loadouts... The company can be tiny. Experience can compound forever." (README.md:214-216).
## Memory assets vs. chat logs and RAG
Claim: RAG answers "what can be found?"; Team Memory also answers "who can use it, which version is valid, and which Agent should receive it" (README.md:222). Partial comparison table (README.md:224-230); the source chunk is truncated mid-row at `| Ownership / Versi`, so rows below that point are not covered here:
| | Chat History | Standard RAG | TencentDB Agent Memory |
|---|---|---|---|
| Cross-session user understanding | △ | △ | ✅ Chat Memory |
| Distilled executable experience | — | — | ✅ Skill |
| Document structure & relationships | — | △ Chunk retrieval | ✅ Wiki + Link Graph |
| Code call graphs & impact scope | — | △ Text match | ✅ CodeGraph |
> Truncation note: the chunk cuts off at README.md:230 (`Ownership / Versi...`); no claims are made here about ownership/versioning rows or anything after that line.
**Covers:** README.md (project purpose, installation, agent support, Chat Memory / Skill / Wiki / CodeGraph / Memory Hub panel, cold start, team play, RAG comparison through truncated row); pointers to INSTALL.md, INSTALL_CN.md, MemoryCore/scripts/migrate-v2-to-v3/README.md, CONTRIBUTING.md
