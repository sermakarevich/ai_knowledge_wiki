# SemaClaw: A Step Towards General-Purpose Personal AI Agents through Harness Engineering

**Paper:** [SemaClaw: A Step Towards General-Purpose Personal AI Agents through Harness Engineering (Zhu et al., 2026)](https://arxiv.org/abs/2604.11548)

## Human Readable TL;DR

Imagine hiring a personal assistant who forgets everything after every meeting, can't be trusted to act without supervision, and falls apart on complex multi-step errands. SemaClaw is a blueprint for building AI assistants that remember things across conversations, ask permission before doing anything risky, and can break big jobs into smaller pieces and hand them off to specialist helpers. It's like giving that forgetful assistant a notebook, a rulebook, and a team to delegate to -- so they actually become useful over time.

## TL;DR

SemaClaw is an open-source multi-agent application framework addressing three core harness engineering challenges: dynamic-yet-structured orchestration (via DAG-based two-phase planning), runtime behavioral safety (via PermissionBridge authorization checkpoints), and structured long-term memory (via a three-tier context architecture plus a wiki-based personal knowledge base). The key empirical insight is that harness improvements alone can drive significant capability gains -- a controlled demonstration showed a 13.7 percentage-point completion rate increase with the model held constant -- suggesting harness design is as important as model selection.

---

## Problem & Motivation

As personal AI agents (e.g., OpenClaw) reach large-scale deployment, three systemic engineering gaps emerge that existing open-source frameworks fail to address:

1. **Dynamic yet structured orchestration** -- Real tasks require hierarchical decomposition with dependency management and failure recovery. Current systems are either too rigid (declarative workflows) or too opaque (unconstrained agentic reasoning with no execution traceability).
2. **Runtime behavioral safety** -- Agents performing consequential actions (file writes, API calls) need authorization enforced at the runtime level, not just at the application or tool level.
3. **Structured long-term memory** -- Sustained use requires cross-session knowledge retention that goes beyond log retrieval -- task-derived insights must sediment into a durable, user-owned format.

---

## Main Original Ideas

1. **Two-Layer Architecture (sema-code-core + semaclaw)** -- Separates a reusable event-driven agent runtime (ReAct loop, context lifecycle, multi-tenant isolation) from the application harness (channel integration, memory, plugin ecosystem). Each layer evolves independently.

2. **DAG Teams: Two-Phase Hybrid Orchestration** -- An LLM orchestrator declares a full Directed Acyclic Graph (DAG) of subtasks in one shot via `create_parent`, specifying agents, prompts, and `dependsOn` edges. A deterministic `DispatchBridge` scheduler then executes the validated DAG, combining dynamic LLM planning with observable, fault-isolated graph execution.

3. **PermissionBridge** -- A globally scoped, single-instance coordination layer that pauses agent execution on high-risk tool invocations or clarification requests, routes interactive prompts to the user, and resumes upon response. It enforces a two-tier permission policy: internal tools (memory retrieval) are pre-authorized; external tools (filesystem, APIs) require per-invocation consent.

4. **Three-Tier Context Architecture** -- Working memory with automatic compaction at 75% capacity; external persistent memory (`MEMORY.md` + rolling daily logs with hybrid BM25 + vector retrieval via sqlite-vec); and persona partitioning (SOUL.md for stable identity, workspace layer for task environment), all scoped per agent.

5. **Wiki-Based Knowledge Sedimentation** -- A user-owned corpus of plain Markdown files organized as a directory tree. The agent curates it via `Save`/`Organize` CLI operations; users edit it directly through a Web UI. A separate retrieval interface with tag filtering supports on-demand queries. This creates a bidirectional human-agent learning loop.

6. **Four-Layer Plugin Ecosystem** -- MCP tools (action space extension), subagents (delegated subtasks with isolated context), skills (lazy-injected modular capability packages), and hooks (lifecycle insertion points for logging/monitoring without modifying agent reasoning).

7. **Four-Mode Scheduled Task System** -- Matches execution cost to task complexity: pure notification, pure script, pure agent, or hybrid script-plus-agent. Token consumption is proportional to actual reasoning work required.

---

## Key Findings

| Mechanism | Effect |
|---|---|
| Harness changes alone (model fixed) | +13.7 pp task completion rate (LangChain Terminal Bench 2.0 reference) |
| Retrieval substituting parametric knowledge | Reduces need for frontier model memorization |
| Skill injection narrowing task scope | Distributes reasoning load, improves focus |
| Execution mode routing | Eliminates model invocation for deterministic work |

- Harness engineering can partially substitute for raw model capability on structured, context-supported, or decomposable tasks.
- Capable mid-tier models with well-designed harnesses may match frontier model performance at significantly lower cost.
- Plain-file Markdown wiki ensures user data ownership, direct inspectability, and version-controllability -- a deliberate design choice over opaque vector stores.
- Compaction with rule/task re-injection after summarization prevents context rot without losing task state continuity.

---

## Suggestions & Future Directions

1. **Virtual vs. persistent agent personas** -- Tension remains between ephemeral context and durable identity; the right boundary is an open question.
2. **Harness-model complementarity boundary** -- Exact characterization of which task classes benefit most from harness investment vs. model capability is unresolved.
3. **Memory ownership and IP** -- As agents accumulate user-specific knowledge, questions of intellectual property and privacy in knowledge corpora need frameworks.
4. **Stateful harness plugins** -- Current plugin layers are largely stateless; designing persistent, stateful plugin primitives is a next step.
5. **Cross-operator agent interaction** -- Community-level agent forms (A2A interaction across operators, shared knowledge commons) require new infrastructure standards.
6. **Intelligent task routing with heterogeneous model pools** -- Harness-managed routing between models of different capability tiers based on task complexity is proposed as a near-term priority.

---

## Authors & Institutions

Ningyan Zhu, Huacan Wang (corresponding), Jie Zhou, Feiyu Chen, Shuo Zhang, Ge Chen, Chen Liu, Jiarou Wu, Wangyi Chen, Xiaofeng Mou, Yi Xu (corresponding) -- all at Midea AIRC.
