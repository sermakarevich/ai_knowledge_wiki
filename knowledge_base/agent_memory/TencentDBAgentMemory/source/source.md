# TencentCloud/TencentDB-Agent-Memory
Source: https://github.com/TencentCloud/TencentDB-Agent-Memory
Kind: repo
Fetched: 2026-09-26T13:41:32.216064+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# TencentCloud/TencentDB-Agent-Memory

Commit: bd88cc83870bf9e7dbd2ec36aa13608d2295c7f4

## README

### Agents remember. Humans innovate.

<a href="https://trendshift.io/repositories/29310?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-29310" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/29310" alt="TencentCloud%2FTencentDB-Agent-Memory | Trendshift" width="250" height="55"/></a>

[![npm](https://img.shields.io/npm/v/@tencentdb-agent-memory/memory-tencentdb?color=blue)](https://www.npmjs.com/package/@tencentdb-agent-memory/memory-tencentdb)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E=22.16-brightgreen)](https://nodejs.org/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-%3E=2026.3.13-orange)](https://github.com/openclaw/openclaw)
[![Hermes](https://img.shields.io/badge/Hermes-Gateway-7B61FF)](https://hermes-agent.nousresearch.com/docs/)
[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white)](https://discord.gg/dJQM6mKMF)

[Installation](#installation) · [Supported Agents](#all-agents-share-the-same-memory-server) · [What is it?](#what-is-tencentdb-agent-memory) · [Team Play](#one-play-style-build-a-growing-agent-team-for-a-one-person-company) · [Technical Implementation](#technical-implementation) · [Benchmark](#benchmark) · [Roadmap](#roadmap)

[**English**](./README.md) · [简体中文](./README_CN.md)

</div>

---

> **Latest:** Team Memory Beta is evolving quickly — install it and start exploring in minutes.

<td>
   <video src="https://github.com/user-attachments/assets/efb1a808-1f86-4cfe-802c-f7453f7ca938" width="100%" controls autoplay loop muted playsinline></video>
</td>



# Installation

Start all three services in one go (`memory-core` + `memory-hub` + `proxy`):

```bash
git clone https://github.com/TencentCloud/TencentDB-Agent-Memory.git
cd TencentDB-Agent-Memory/deploy/global-images
cp .env.example .env
$EDITOR .env       # Fill in two sets of LLM parameters (memory group + proxy group)
./start-all.sh     # Launch everything with one command; when finished, it prints a one-liner you can paste directly into Claude
```

Open the panel: [http://localhost:8125](http://localhost:8125).

Complete installation documentation (standalone Memory Hub deployment, Proxy + Claude Code / CodeBuddy usage, stop and cleanup, port reference, etc.) is available in [**INSTALL.md**](./INSTALL.md) (中文: [INSTALL_CN.md](./INSTALL_CN.md)).
The MongoDB storage backend is **experimental** (off by default); see
[INSTALL.md · MongoDB storage backend](./INSTALL.md#optional-mongodb-storage-backend-experimental-off-by-default).



### Migrating data from an older version

If you're already on an older release (v1.x / v0.x) and want to bring your existing data over to v2.0.0+, we provide a migration tool:

See [**Data Migration Tool (v2 → v3)**](./MemoryCore/scripts/migrate-v2-to-v3/README.md) for full usage and flags. New installations can skip this.



## All Agents Share the Same Memory Server

One Proxy, unchanged protocol, zero-code integration — point the Agent's base URL to the Proxy and it's done. No plugin, hook, or MCP server is required.

<table>
<tr>
<td align="center" width="140"><a href="./INSTALL.md#using-proxy-with-deepseek-harness-dsh"><img src="./assets/images/agents/dsh.png" width="48" height="48" /><br /><sub><b>DeepSeek Harness</b></sub></a></td>
<td align="center" width="140"><a href="./INSTALL.md#using-proxy-with-claude-code"><img src="./assets/images/agents/claude-code.png" width="48" height="48" /><br /><sub><b>Claude Code</b></sub></a></td>
<td align="center" width="140"><a href="./INSTALL.md#using-proxy-with-codex"><img src="./assets/images/agents/codex.png" width="48" height="48" /><br /><sub><b>Codex</b></sub></a></td>
<td align="center" width="140"><a href="./INSTALL.md#using-proxy-with-codebuddy"><img src="./assets/images/agents/codebuddy.png" width="48" height="48" /><br /><sub><b>CodeBuddy</b></sub></a></td>
</tr>
<tr>
<td align="center" width="140"><a href="./INSTALL.md#using-proxy-with-workbuddy"><img src="./assets/images/agents/workbuddy.png" width="48" height="48" /><br /><sub><b>WorkBuddy</b></sub></a></td>
<td align="center" width="140"><a href="./INSTALL.md#using-proxy-with-hermes"><img src="./assets/images/agents/hermes.png" width="48" height="48" /><br /><sub><b>Hermes</b></sub></a></td>
<td align="center" width="140"><a href="./INSTALL.md#using-proxy-with-openclaw"><img src="./assets/images/agents/openclaw.png" width="48" height="48" /><br /><sub><b>OpenClaw</b></sub></a></td>
<td align="center" width="140"><a href="./INSTALL.md#using-proxy-with-other-platforms-generic"><sub><b>More frameworks coming soon...</b></sub></a></td>
</tr>
</table>

See [**INSTALL.md**](./INSTALL.md) for the exact configuration steps of each client.

Don't see your favorite Agent? You can try adapting it yourself with the [Generic integration guide](./INSTALL.md#using-proxy-with-other-platforms-generic) — and we'd love a PR adding native support for it. See [**CONTRIBUTING.md**](./CONTRIBUTING.md) to get started.



# What is TencentDB Agent Memory?

We started from a practical question: **How do you reduce repetitive work when using Agents?**

If project context has already been explained, it shouldn't need to be repeated in a new session. If documents have already been read, every Agent shouldn't have to start again from page one. A workflow that already works shouldn't have to be rediscovered next time.

Memory here means more than just "remembering conversations." **Any information that helps the next Agent avoid reinventing the wheel should be saved, organized, and reused.**

```text
Existing information → Reusable memory assets → Fewer turns → Less rework → More stable results and higher efficiency
```



### Let experience accumulate, flow, and pass on to the next Agent

**Memory Hub** for Agent teams closes the loop across the entire experience lifecycle: work produces assets, assets circulate through the team, and new members can load the team's save file on day one.

1. **Automatic asset extraction**: Extract Chat Memory and Skills from conversations and tasks; convert documents and code into Wiki and CodeGraph; then manage, review, and route them consistently.
2. **Portable & multi-Agent compatible**: Memory assets are decoupled from Agent frameworks — they can move across frameworks and be shared and maintained by multiple Agents and team members.
3. **Cold-start friendly**: Import existing documents, codebases, and Agent conversation sessions. New Agent teams can start from existing experience instead of learning from scratch.



### 🧠 A brain that remembers people and context

- **Chat Memory** retains preferences, facts, decisions, and interaction history.
- Each Agent automatically gets its own memory when created — no need to re-introduce yourself next time.
- L0 Conversation → L1 Atom → L2 Scenario → L3 Persona — raw conversations are distilled layer by layer.

<img width="" src="assets/images/chat_memory.png" alt="image.png" />

> "Don't refactor the old auth module — mobile is still using it." — Context this costly shouldn't depend on humans repeating it every time.



### ⚡ A Skill library that accumulates expertise

- After completing complex work, Agents can extract and manage reusable Skills from conversations and tool calls, and import them into the context of a designated Agent when needed.
- A Skill isn't just a prompt snippet; it has versions, resource files, trigger boundaries, execution steps, and validation rules.
- Personal Skills are private by default; after review, they can be shared with the team and assigned to other Agents.

<img width="" src="assets/images/skill.png" alt="image.png" />

> Troubleshooting, code review, release checklists — learn it once, and the whole team can use it.



### 📖 A knowledge map that reads both docs and code

- **Wiki** turns product docs, design specs, and ops runbooks into structured pages with a link graph. (Inspired by Karpathy's LLM knowledge base.)

<img src="./assets/images/wiki.png" alt="image.png" />

- **CodeGraph** indexes code symbols, files, call relationships, and impact paths.
<img width="" src="assets/images/codegraph.png" alt="image.png" />

- Agents can search, read, inspect callers/callees, and perform impact analysis before modifying code.

> Wiki keeps Agents from reading every file list before getting to work. CodeGraph doesn't just tell them "the code is here" — it tells them "changing this might affect those."



### 🛡️ A team memory panel controlled by humans

- Create teams and Agents in Memory Hub; review, share, and equip memory assets.
- Manage ownership, versions, status, visibility, usage counts, and Agent bindings in one place.
- `private` belongs strictly to the Owner; `team` is visible to all team members; `restricted` grants precise access via User / Role / Agent ACLs.
- Two role layers: **global System Admin** manages users and teams (creating teams, adding members) and can also use Wiki, CodeGraph, Skill, and other asset management features; **Team-level roles** include Admin (team manager) and Member (regular member), responsible for asset collaboration and access control within a team. Asset ownership is tracked via Owner — the Owner automatically has management permissions for their assets.

<img width="" src="assets/images/asset.png" alt="image.png" />




## Cold Start: Load the Save File, Then Get to Work

Most Agents' first task is re-learning your project. TencentDB Agent Memory turns the learning cost you've already paid into a save file:

<img alt="Cold Start: import codebase, docs, and history into Memory Hub" src="assets/images/flowchart3.png" />

Specifically, these existing assets can be imported directly and processed automatically in the panel:

- **Codebases**: Import existing repositories — **CodeGraph** automatically indexes symbols, files, call relationships, and impact paths.
- **Documents & files**: Import relevant docs and files — **Wiki** automatically generates structured pages with a link graph.
- **Conversation sessions**: Import past Agent conversation sessions — **Skills and Chat Memory** are automatically extracted as reusable assets.

> Stop retraining every Agent. Give it the save file.



## One Play Style: Build a Growing Agent Team for a One-Person Company

Open Memory Hub and create a team:

```text
Tiny but Serious Inc.
├── 👤 You · Set goals / Make decisions
├── 🔭 Scout · Research / Find opportunities
├── 🛠 Builder · Write code / Build products
├── 🧪 Reviewer · Test / Find issues
└── 🧠 Agent Memory · Preserve the team's experience
```

You're not opening four disconnected chat windows — you're assembling a squad with different roles that can inherit the team's accumulated experience.



### Recruit first, then equip

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

Different roles, different loadouts. Less noise — give each Agent the memory assets it actually needs to get work done.

**The company can be tiny. Experience can compound forever.**



## Memory Assets, Not a Chat Log Warehouse

RAG answers "what can be found?" Team Memory also answers "who can use it, which version is valid, and which Agent should receive it."

| | Chat History | Standard RAG | TencentDB Agent Memory |
| :--- | :---: | :---: | :---: |
| Cross-session user understanding | △ | △ | ✅ Chat Memory |
| Distilled executable experience | — | — | ✅ Skill |
| Document structure & relationships | — | △ Chunk retrieval | ✅ Wiki + Link Graph |
| Code call graphs & impact scope | — | △ Text match | ✅ CodeGraph |
| Ownership / Versi

... (truncated, 9539 more characters)

## Top-level layout

- .github/ (dir, 5 files, ~340 lines)
- .gitignore (~141 lines)
- adapters/ (dir, 4 files, ~269 lines)
- agents/ (dir, 21 files, ~7571 lines)
- assets/ (dir, 34 files, ~0 lines)
- CHANGELOG.md (~372 lines)
- CONTRIBUTING.md (~155 lines)
- CONTRIBUTING_CN.md (~151 lines)
- deploy/ (dir, 18 files, ~3204 lines)
- INSTALL.md (~830 lines)
- INSTALL_CN.md (~687 lines)
- LICENSE (~27 lines)
- MemoryCore/ (dir, 400 files, ~118655 lines)
- MemoryKnowledge/ (dir, 78 files, ~14831 lines)
- MemoryPanel/ (dir, 284 files, ~64702 lines)
- MemoryProxy/ (dir, 202 files, ~62431 lines)
- README.deployment.md (~607 lines)
- README.docker.md (~265 lines)
- README.md (~378 lines)
- README_CN.md (~382 lines)
- ROADMAP.md (~119 lines)
- ROADMAP_CN.md (~108 lines)
- sdk/ (dir, 44 files, ~10824 lines)

