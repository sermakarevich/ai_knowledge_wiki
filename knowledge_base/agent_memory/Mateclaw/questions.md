---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: mateaix/mateclaw

### Q1. What is MateClaw in one sentence, and what makes it a "whole-widget" deployment?
> [!tip]- Answer
> MateClaw is a self-hosted, pluggable agent runtime ("second brain") that runs digital employees over native or DSH engines in one deployment. It bundles reasoning, knowledge/memory, tools, and channels together, with automatic retry on the next healthy provider when the primary model fails. See [[wiki/01-overview|Overview]].

### Q2. How does MateClaw's provider failover and health tracking work?
> [!tip]- Answer
> When a call fails (expired key, 401, network blip, drained quota), MateClaw tries the next healthy provider in the configured order from Settings → Models. A provider health tracker parks failing vendors in a cooldown window and only surfaces an error once the whole chain is exhausted. See [[wiki/01-overview|Overview]].

### Q3. What is the `AgentRuntimeProvider` contract, and what are the native vs. DSH engines?
> [!tip]- Answer
> The contract separates employee identity (role, goal, backstory, governance) from the execution engine. The native runtime is an in-process StateGraph engine with ReAct, Plan-and-Execute, Goals, and Team Runs, while the DSH runtime manages a `dsh-jsonrpc-agent` child process over authenticated JSON-RPC with normalized runtime events. See [[wiki/01-overview|Overview]].

### Q4. How do persistent Goals and Team Runs make long-horizon work recoverable and observable?
> [!tip]- Answer
> Persistent Goals persist checklist, continuation state, attempts, cooldowns, leases, and user input, so after a backend restart the supervisor reconciles the interrupted attempt instead of repeating it. One Team Run with a stable `runId` links objective, task DAG, worker executions, synthesis, and deliverables, with chat as the outcome surface, Agents Live for observation, and Teams for history and governance. See [[wiki/01-overview|Overview]].

### Q5. What is the LLM Wiki, and how is employee capability extended and bounded?
> [!tip]- Answer
> The LLM Wiki digests raw materials (PDF, markdown, scraped pages) into structured pages with `[[links]]` and traceable citations, with a hot cache auto-injected into system prompts. Capability grows via SKILL.md packages, MCP servers with per-employee binding, and ACP bridges to Claude Code/Codex, all bounded by Tool Guard RBAC, approvals, and path protection. See [[wiki/01-overview|Overview]].

### Q6. How do the top-level files pin MateClaw's Docker build, environment, and checkout policy?
> [!tip]- Answer
> `.dockerignore` keeps the build context lean by excluding git/IDE artifacts, build outputs, the desktop app, data/logs, secrets, and most markdown with narrow re-inclusions. `.env.example` is the fail-closed copy-and-rename template over PostgreSQL 16 where unset required values abort `docker compose up`, while `.gitattributes` pins shell/SQL files to LF and Windows scripts to CRLF and `.gitignore` scopes ignores to this pnpm monorepo. See [[wiki/02-top-level-files|top-level-files]].

### Q7. Would you recommend MateClaw for a team that needs governed, long-running agent work on its own infrastructure?
> [!tip]- Answer
> Yes, if the team values self-hosting, approval-gated multi-user work with a full audit trail, and recovery across provider outages and restarts via failover, Goals, and Team Runs. The trade-off is operational cost: you own the deployment, PostgreSQL 16 stack, and provider keys, so a team wanting zero-ops SaaS should look elsewhere. See [[wiki/01-overview|Overview]].
