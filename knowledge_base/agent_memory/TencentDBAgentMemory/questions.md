---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: TencentCloud/TencentDB-Agent-Memory

### Q1. What problem does TencentDB Agent Memory solve, and what is its reusable-asset pipeline?

> [!tip]- Answer
> > It solves repetitive agent work where project context, documents, and workflows are re-explained or rediscovered each session. The pipeline is: existing information → reusable memory assets → fewer turns → less rework → more stable results and higher efficiency. Memory is defined as anything that helps the next agent avoid reinventing the wheel.
> > See [[wiki/01-overview|Overview]].

### Q2. What are the three services in the stack, and how does the Proxy give zero-code integration?

> [!tip]- Answer
> > The stack ships memory-core, memory-hub, and proxy, launched together with one command (`./start-all.sh`), with the web panel at `http://localhost:8125`. One Proxy covers many agents with unchanged protocol: pointing an agent's base URL at the Proxy is enough, with no plugin, hook, or MCP server required. Supported clients include Claude Code, Codex, DeepSeek Harness, CodeBuddy, WorkBuddy, Hermes, and OpenClaw.
> > See [[wiki/01-overview|Overview]].

### Q3. How does Chat Memory distill experience across layers, and what makes a Skill more than a prompt snippet?

> [!tip]- Answer
> > Chat Memory distills L0 Conversation → L1 Atom → L2 Scenario → L3 Persona, retaining each agent's preferences, facts, decisions, and interaction history across sessions. A Skill is versioned, reviewable executable experience with resource files, trigger boundaries, execution steps, and validation rules, private by default and shared team-wide only after review. Examples include troubleshooting, code review, and release checklists.
> > See [[wiki/01-overview|Overview]].

### Q4. How do Wiki and CodeGraph jointly cover docs and code, and how is human control enforced?

> [!tip]- Answer
> > Wiki turns product docs, specs, and runbooks into structured pages with a link graph so agents avoid re-listing files, while CodeGraph indexes symbols, files, and call relationships for caller/callee inspection and pre-edit impact analysis. Human control runs through the team memory panel with `private` (owner only), `team` (all members), and `restricted` (User/Role/Agent ACLs) visibility. Global System Admins manage users and teams while team Admins/Members operate inside teams, and owners hold management permission on owned assets.
> > See [[wiki/01-overview|Overview]].

### Q5. How do you boot the full stack, what are the default ports, and what is the MongoDB storage option?

> [!tip]- Answer
> > Clone the repo, go to `deploy/global-images`, copy `.env.example` to `.env`, fill in the memory and proxy LLM groups, and run `./start-all.sh`, which probes LLM connectivity and prints a ready-to-run `claude` block. Default ports are Memory Core `8420`, Panel UI `8125`, Knowledge `8424`, and Proxy `8096`. MongoDB is an opt-in experimental backend enabled via `./start-all-mongo.sh` (writing `MEMORY_CORE_STORE_MODE=mongodb`); sqlite stays the default and switching backends does not migrate data.
> > See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. What are the Standalone vs. Service deployment modes, the v1 vs. v2 Hermes plugins, and the contribution and roadmap rules?

> [!tip]- Answer
> > Standalone is the single-machine SQLite plus in-process state mode for local dev and single-agent sidecars, while Service uses TCVDB/COS plus Redis for K8s multi-replica multi-tenant SaaS, switched via `TDAI_DEPLOY_MODE`. The v1 `memory_tencentdb` plugin self-manages a Gateway subprocess for standalone use, whereas v2 `memory_tencentdb_v2` talks to an external Gateway over v2 REST for shared/service use. Contributions target branch `feat/server_team` with Conventional Commits and a DCO `Signed-off-by:` line, and the next release v2.0.1 adds Agent templates, `mem:` Task commands, editable L1–L3 memories, L0/L1 search, and Cursor support.
> > See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. (Evaluation) A small team with one shared repo and no K8s asks whether to adopt TencentDB Agent Memory in Standalone or Service mode — what do you recommend and why?

> [!tip]- Answer
> > Recommend starting with Standalone (sqlite, `./start-all.sh`, Proxy-only onboarding) because it needs no Redis, VDB/COS, or K8s yet still delivers the full asset loop of Chat Memory, Skills, Wiki, and CodeGraph for cold-starting agents. Move to Service mode only when multiple replicas, tenants, or shared SaaS memory demand it, since that adds Redis distributed state and external storage to operate. Revisit the call when the team outgrows a single space or needs per-service-id isolation.
> > See [[wiki/02-top-level-files|Top-Level Files]].
