---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Graph Engineering for Multi-Agent Systems

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. How does the article distinguish graph engineering from knowledge-graph engineering?

> [!tip]- Answer
> Knowledge-graph engineering structures what a system *knows* (graph-structured data, e.g. entity-relationship stores). Graph engineering structures who a system *is* — the topology of agents, tools, routers, and governed transitions that make up a multi-agent system. The two disciplines share the word "graph" for unrelated purposes and should not be conflated. See [[wiki/01-graph-engineering-enterprise-guide|Graph Engineering Enterprise Guide]].

### Q2. Why do the prompt, context, loop, and graph engineering layers compose rather than replace each other?

> [!tip]- Answer
> Each layer governs a different scope — prompt controls one call, context controls what a model sees, loop controls one agent's cycle, graph controls topology across nodes — and a higher layer cannot fix failures in a lower one. A graph whose individual nodes have unengineered loops is described as "an org chart of unreliable employees": good topology cannot compensate for unreliable node-level behavior, and edges without identity or policy cannot be centrally governed regardless of how the graph is shaped. See [[wiki/01-graph-engineering-enterprise-guide|Graph Engineering Enterprise Guide]].

### Q3. Name the four guardrail hooks and explain why the article says they don't fully solve cross-agent prompt injection.

> [!tip]- Answer
> The four hooks are `llm_input`, `llm_output`, and a pre/post pair around tool invocation. They don't eliminate cross-agent prompt-injection risk because content produced by one node can become input to another node — the risk lives in the topology and identity boundaries between nodes, not just inside any single node's own guardrail checks. See [[wiki/01-graph-engineering-enterprise-guide|Graph Engineering Enterprise Guide]].

### Q4. Walk through the correlation pattern the article gives for cost control. What three identifiers does it propagate, and what does each enable?

> [!tip]- Answer
> It propagates `graph_id` (which graph produced the call), `run_id` (which specific execution), and `node_id` (which node within that run), alongside a node-specific virtual-account token in the Authorization header. Together they let budget and rate-limit rules be scoped at tenant/team level and let every call be mapped back to the exact graph, run, and node that produced it — necessary because fan-out, retries, and dynamic spawning make cost a property of the graph, not of any single request. See [[wiki/01-graph-engineering-enterprise-guide|Graph Engineering Enterprise Guide]].

### Q5. The article splits observability authority between two record streams. What is each one authoritative for, and why isn't either one sufficient alone?

> [!tip]- Answer
> The orchestrator is the source of truth for runtime topology — which nodes ran, in what order, with what inputs/outputs (the actual work graph). The gateway is the source of truth for model, tool, policy, latency, and cost evidence. Gateway records lack graph structure (they see individual calls, not the topology); orchestrator traces lack authoritative metering (they don't independently verify cost/policy). Both must be correlated to reconstruct a complete picture. See [[wiki/01-graph-engineering-enterprise-guide|Graph Engineering Enterprise Guide]].

### Q6. A team is designing a code-review graph where a "security-reviewer" node can request a production config change. Using the checklist, what two items would specifically apply to that node, and why?

> [!tip]- Answer
> Item 6 ("are sensitive tool actions protected by explicit approval checkpoints?") applies directly — a production config change is exactly the kind of consequential action that should sit behind a structural human-approval checkpoint, converting "the agent decided to do X" into "the agent proposed X and a human approved it." Item 2 ("do gateway-mediated calls carry stable graph/run/node identifiers?") also applies, since the security-reviewer's specific calls need to be individually attributable for audit purposes given its sensitive mandate. See [[wiki/01-graph-engineering-enterprise-guide|Graph Engineering Enterprise Guide]].

### Q7. According to the FAQ, what do LangGraph, AutoGen, and CrewAI provide versus what TrueFoundry provides?

> [!tip]- Answer
> Graph frameworks (LangGraph, AutoGen, CrewAI) provide the topology — the mechanics of defining nodes, edges, and state. TrueFoundry provides managed execution and governance for gateway-mediated operations — identity, policy, budgets, guardrails, approvals, and correlated records — layered on top of, not replacing, those frameworks' topology definitions. See [[wiki/01-graph-engineering-enterprise-guide|Graph Engineering Enterprise Guide]].

### Q8. Given this is a vendor blog post, which specific claims should be weighed more skeptically than the article's definitional framing, and why?

> [!tip]- Answer
> The measured metrics (~10ms latency, ~3-4ms core gateway latency, 350+ RPS on 1 vCPU) and the implicit case for needing a gateway product at all deserve more skepticism than the definitional/governance framing, because they are marketing claims about TrueFoundry's own product with no independent benchmark methodology disclosed, whereas the definitional distinction (graph vs. knowledge-graph engineering) and the governance checklist are vendor-neutral and independently verifiable against first principles. See [[critical_thinking|Critical Analysis]].
