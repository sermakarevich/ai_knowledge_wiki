> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Graph Engineering Enterprise Guide

**In one sentence:** Graph engineering is the emerging discipline of designing and operating multi-agent systems as explicit, programmable graphs of heterogeneous nodes — agents, functions, routers, joins, tools, and human checkpoints — where the topology itself becomes a versionable, governable, cost-attributable, and observable artifact distinct from knowledge-graph engineering.

## Key points

- Graph engineering structures who a multi-agent system *is* (its topology of agents, tools, and governed transitions), whereas knowledge-graph engineering structures what a system *knows* (graph-structured data) — the two use "graph" for unrelated purposes.
- Graph engineering sits atop a layered hierarchy of prompt → context → loop → graph, and these layers compose rather than supersede one another, because a graph whose nodes have unengineered loops is "an org chart of unreliable employees."
- Enterprise governance requires resolved identity for every independently governed caller, gateway-mediated model/MCP policy, tool-level restrictions that scope each node to its mandate, four guardrail hooks (`llm_input`, `llm_output`, and pre/post tool-invoke pairs), and acknowledgment that cross-agent prompt-injection risk is *not* eliminated by per-node guardrails alone.
- Cost control works by propagating `graph_id` / `run_id` / `node_id` (plus a node-specific virtual-account token) into every call so budget and rate-limit rules can be scoped at tenant/team level through virtual accounts or metadata, mapping each call back to the exact graph, run, and node.
- Observability splits authority between two correlated record streams: the orchestrator is the source of truth for runtime topology (the actual work graph), while the gateway is the source of truth for model, tool, policy, latency, and cost evidence.
- Once node-level attribution exists, the graph becomes tunable — expensive nodes get cheaper models, repeated subtasks get semantic caching, flaky targets get fallback chains — and durable enterprise operation requires explicit ownership across orchestration, identity, policy, budgets, approvals, and evidence.

---

## Definition and its boundary

Graph engineering designs and operates multi-agent systems as explicit graphs of heterogeneous nodes — agents, deterministic functions, routers, joins, tools, and human checkpoints — with communication as edges. The topology itself becomes a programmable, versionable artifact.

The article draws a firm distinction from a discipline it shares a keyword with:

> this is *not* knowledge-graph engineering — the established discipline of building graph-structured data … Knowledge graphs structure what a system *knows*; graph engineering … structures who the system *is*.

The practical consequence of the explicitness: the orchestrator can record the *actual runtime work graph* as a first-class artifact, and identity, policy, cost, and audit can be attached at the nodes and edges instead of being inferred after the fact from chat logs.

## A brief history: three roots and a naming event

The concept draws from three historical roots:

1. **Dataflow computation** — early dataflow architectures, compiler dependency graphs, MapReduce DAGs, and frameworks like Airflow.
2. **Multi-agent systems research** — actor models, contract-net protocols, and distributed-AI communication vocabularies.
3. **Organizational practice** — org charts, RACI matrices, and business-process notation.

The article frames graph engineering as a **"naming event"**: the moment an assembling practice became discussable as a unified concept, which in turn enables shared tooling and operational discourse.

## Where graph engineering fits: prompt, context, and loop engineering

Graph engineering sits atop a layered hierarchy. Each layer governs a different scope of the agent system, and the layers stack:

- **Prompt engineering** — controls a single model response (one call's framing and constraints).
- **Context engineering** — controls what a model *sees* (retrieval, memory, context windows).
- **Loop engineering** — controls one agent's observe–reason–act cycle (per-agent behavior and termination).
- **Graph engineering** — controls *topology across heterogeneous nodes* (identity, governance, and cost across many nodes).

The article emphasizes that these layers **compose rather than supersede**:

> these layers *compose* rather than supersede. A graph whose nodes have unengineered loops is an org chart of unreliable employees.

A well-shaped graph with unreliable nodes inherits each node's failures, and a graph whose edges have no identity or policy cannot be governed centrally.

## Enterprise: governance, cost control, and observability

### Governance requirements

1. **Resolved identity** — every independently governed caller needs a resolved identity so policy, budget, and audit can attach to it.
2. **Gateway-mediated policy** — model requests and MCP tool invocations should flow through a gateway where policy is enforced uniformly, rather than being embedded per-node in framework code.
3. **Tool-level restrictions** — scope each node to its mandate: a node's authority is expressed as what it may *call*, not as a prompt-level suggestion.
4. **Four guardrail hooks** — `llm_input`, `llm_output`, and the pre/post pair around tool invocation.
5. **Cross-agent prompt-injection risk** — this remains *uneliminated* by guardrails alone: content produced by one node can become input to another, so containment depends on graph topology and identity, not just per-node hooks.

### Cost control

Work graphs increase model and tool calls through **fan-out, retries, and dynamic spawning**, so cost is a graph property, not a per-request property:

- **Budget rules** operate at **tenant/team scope**, with separate limits per virtual account or metadata dimension.
- **Rate-limit rules** partition by supported metadata dimensions.
- **Correlation** — propagating `graph_id` or `node_id` (with a run identifier and a node-specific virtual-account token) enables every call to be mapped back to the graph, run, and node that produced it.

Illustrative correlation pattern (verbatim from the article):

```
Authorization: Bearer <node-specific-virtual-account-token>
X-TFY-METADATA: {
  "graph_id": "release-review",
  "run_id": "run-8f31",
  "node_id": "security-reviewer"
}
```

### Observability

Two record streams must be correlated:

- **Gateway metrics and records** — model/tool calls seen at the edge: tokens, latency, tool identity, policy decisions.
- **Orchestrator execution traces** — the runtime work graph: which nodes ran, in what order, with what inputs and outputs.

The article is explicit about the split of authority: **the orchestrator remains the source of truth for topology**, while **the gateway contributes model, tool, policy, latency, and cost evidence**. Gateway records lack graph structure; orchestrator traces lack authoritative metering.

### Structural / human approval checkpoints

TrueFoundry Agent Harness provides managed execution with **structural (human) approval checkpoints placed immediately before configured sensitive tool calls, at exactly the edges where consequence concentrates** — converting "the agent decided to do X" into "the agent proposed X and a human approved X at this edge," with the approval as a first-class record.

### Optimization via node-level attribution

Node-associated attribution is what makes the graph *tunable*:

- **Expensive nodes** receive **cheaper models**.
- **Repeated subtasks** get **semantic caching**.
- **Flaky targets** receive **fallback chains**.

## Enterprise graph engineering checklist (verbatim)

Seven critical questions for production multi-agent graphs:

1. Does every independently governed caller have a resolved identity?
2. Do gateway-mediated model and MCP calls carry stable graph, run, and node identifiers?
3. Does the orchestrator record the actual runtime work graph?
4. Can orchestration traces correlate with gateway cost, policy, latency, and tool records?
5. Are graph- or node-associated budget rules mapped through virtual accounts or metadata?
6. Are sensitive tool actions protected by explicit approval checkpoints?
7. Are model changes isolated behind virtual-model routing where permitted?

> Each unanswered item is a plausible incident location.

## The future of graph engineering: what to watch

The article's predictions for how the field will develop:

- **Vocabulary will churn** — "org graph" and "work graph" may not survive as terms.
- **Frameworks will race to claim the term.**
- **Engineering will concentrate** on **runtime work-graph mutation under stable org-graph policy** (the dynamic graph under a comparatively static governance layer).
- **Standards (A2A and successors) will evolve at the edge layer.**
- **Enterprise requirements become visible** as systems move into shared production.

## The TrueFoundry perspective

The closing argument, in the article's words:

> paradigms are born on X and in frameworks, but they grow up in production. Regardless of which terminology survives, durable operation will require explicit ownership across orchestration, identity, policy, budgets, approvals, and evidence.

TrueFoundry positions itself around three capabilities: **governed model and MCP operations through gateways**, **a managed Agent Harness runtime for agentic nodes**, and **governance correlated with orchestrator records**.

## FAQ

**Is graph engineering the same as knowledge-graph engineering?**
No. Knowledge graphs structure *data*; graph engineering structures the multi-agent system itself.

**What does graph engineering require in an enterprise environment?**
The orchestrator records topology and runtime state; callers propagate identifiers; and the platform (TrueFoundry) applies identity, access policy, budgets, rate limits, guardrails, approvals, records, and metrics.

**What tools support graph engineering today?**
Graph frameworks (LangGraph, AutoGen, CrewAI) provide topology; the A2A protocol supports inter-agent communication; TrueFoundry provides managed execution and governance for gateway-mediated operations.

## Technical details & metrics

- **Latency:** ~10 ms under load; **~3–4 ms core gateway latency**.
- **Throughput:** **350+ RPS on 1 vCPU**.
- **Enterprise support:** production-ready with full support.

## Product boundary statement (important caveat)

> Agent Harness is a managed runtime for a root agent and automatically generated, one-level subagents; it is not currently a general-purpose authoring layer for arbitrary org graphs. Current subagents share the root agent's MCP tools and sandbox, cannot create nested subagents, and cannot yet be defined as named specialists with independent tools or models.

In short, Agent Harness's current graph support is **one level deep and shared-context**: no nested subagents, and no independently configured specialist subagents.

**Covers:** Entire article — definition, history, layered hierarchy, enterprise governance/cost/observability, checklist, future outlook, FAQ, metrics, product boundaries (source chunk 01, full article)
