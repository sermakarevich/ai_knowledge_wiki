> [[index|Wiki]] | [[summary|Summary]]

# Graph Engineering for Multi-Agent Systems — Digest

The whole source at medium depth: the headline claim and key points, in order. ~5 min. Descend into [[wiki/01-graph-engineering-enterprise-guide|the wiki page]] for full detail.

## 1. [[wiki/01-graph-engineering-enterprise-guide|Graph Engineering Enterprise Guide]]

**In one sentence:** Graph engineering is the emerging discipline of designing and operating multi-agent systems as explicit, programmable graphs of heterogeneous nodes — agents, functions, routers, joins, tools, and human checkpoints — where the topology itself becomes a versionable, governable, cost-attributable, and observable artifact distinct from knowledge-graph engineering.

- Graph engineering structures who a multi-agent system *is* (its topology of agents, tools, and governed transitions), whereas knowledge-graph engineering structures what a system *knows* (graph-structured data) — the two use "graph" for unrelated purposes.
- Graph engineering sits atop a layered hierarchy of prompt → context → loop → graph, and these layers compose rather than supersede one another, because a graph whose nodes have unengineered loops is "an org chart of unreliable employees."
- Enterprise governance requires resolved identity for every independently governed caller, gateway-mediated model/MCP policy, tool-level restrictions that scope each node to its mandate, four guardrail hooks (`llm_input`, `llm_output`, and pre/post tool-invoke pairs), and acknowledgment that cross-agent prompt-injection risk is *not* eliminated by per-node guardrails alone.
- Cost control works by propagating `graph_id` / `run_id` / `node_id` (plus a node-specific virtual-account token) into every call so budget and rate-limit rules can be scoped at tenant/team level through virtual accounts or metadata, mapping each call back to the exact graph, run, and node.
- Observability splits authority between two correlated record streams: the orchestrator is the source of truth for runtime topology (the actual work graph), while the gateway is the source of truth for model, tool, policy, latency, and cost evidence.
- Once node-level attribution exists, the graph becomes tunable — expensive nodes get cheaper models, repeated subtasks get semantic caching, flaky targets get fallback chains — and durable enterprise operation requires explicit ownership across orchestration, identity, policy, budgets, approvals, and evidence.

## The argument in five moves

1. Draw a firm boundary: graph engineering structures the multi-agent system's topology; knowledge-graph engineering structures data — do not conflate them.
2. Place graph engineering atop a composing hierarchy (prompt → context → loop → graph): a well-shaped graph cannot compensate for unreliable node-level loops.
3. Make the graph governable in production: resolved identity, gateway-mediated policy, tool-level restriction, guardrail hooks — while conceding guardrails alone don't stop cross-agent prompt injection.
4. Make the graph accountable: correlate every call to `graph_id`/`run_id`/`node_id` so cost and rate limits attach to the right tenant/team, and let the orchestrator and gateway jointly supply topology plus metering evidence.
5. Close with a seven-item operational checklist and a candid boundary statement — TrueFoundry's own Agent Harness is one level deep today — grounding the pitch in what the product can and cannot yet do.
