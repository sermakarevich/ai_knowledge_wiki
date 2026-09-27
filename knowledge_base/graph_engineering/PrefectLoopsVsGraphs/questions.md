> [[index|Wiki]] | [[summary|Summary]]

# Questions

Retrieval practice: try to answer before expanding each callout.

### 1. (Recall — wiki 01) What is the key structural difference between a traditional DAG and Prefect's "directed agentic graph"?

> [!question]- Answer
> A traditional DAG (Directed Acyclic Graph) forbids loops/cycles — edges only ever move forward and never revisit a node. Prefect's directed agentic graph deliberately *permits* cycles; instead of the acyclic constraint, it imposes agentic-specific governance (per-node tools, parameters, access level, model).

### 2. (Recall — wiki 01) What does the article mean by "loop engineering wearing a graph costume"?

> [!question]- Answer
> A degenerate, single-node "graph" that has been handed every tool and instruction at once. Technically it satisfies the definition of a graph, but it gets none of a graph's actual benefits (per-step tool/model selection, purely programmatic nodes) because all the work still happens in one undifferentiated box.

### 3. (Elaboration — wiki 01) Why does the article argue that reproducibility matters more for businesses than for individuals using a chatbot?

> [!question]- Answer
> An individual chatting with Claude or ChatGPT doesn't need to verify that repeated runs take the same decision path — there's no downstream audit or consistency requirement. A business running a multi-step workflow (e.g., a ten-step refund-eligibility process) needs to be able to verify a consistent, auditable decision path across runs, both to trust the system and to satisfy external scrutiny (regulators, customers). Bare loop engineering doesn't provide that; an explicit graph does, because progress becomes programmatically observable at each node.

### 4. (Recall — wiki 02) Why is the "refund agent" example a diagnostic nightmare in a single-node design?

> [!question]- Answer
> Because the same untrustworthy process both performs the action (issuing the refund) and reports on whether it went correctly. If the agent misuses the refund tool, its false self-report ("everything went fine") arrives at the exact same moment as the actual failure — there's no independent signal to catch the problem.

### 5. (Elaboration — wiki 02) How does graph-based capability segregation fix the refund-agent problem?

> [!question]- Answer
> By splitting the workflow into (at least) two nodes along the decision path: a diligence node that has no access to the refund-issuing tool at all, and a separate, subsequent node that receives the tool only after the diligence decision — locked to one customer and usable exactly once. The dangerous capability simply doesn't exist during the judgment phase, so misuse during that phase is structurally impossible.

### 6. (Transfer — wiki 02) How do LangGraph and Pydantic AI differ from Prefect's directed agentic graphs in terms of what they graph?

> [!question]- Answer
> LangGraph and Pydantic AI model the internals of a *single* agent as a graph — e.g., which tool to call next inside one agent's reasoning. Prefect's directed agentic graphs operate one level up: they orchestrate *across* multiple complete agent invocations, where each node is itself a full agentic step (potentially built internally using LangGraph or Pydantic AI). One is micro-orchestration inside an agent; the other is macro-orchestration across agents.

### 7. (Transfer) If you were designing a workflow that both looks up sensitive customer PII and separately needs to email a marketing campaign, how would you apply the article's capability-segregation principle to node design?

> [!question]- Answer
> Put the PII lookup in a node scoped only to read access on customer records, with no ability to send external communications. Put campaign sending in a separate, later node that only receives the specific approved recipient list/content — not raw PII access — and make that node single-use per campaign run. The edge between them should represent an explicit decision point (e.g., an approval or a data-transformation step) rather than letting one node hold both capabilities simultaneously.

### 8. (Evaluation — draws on `critical_thinking.md`) Given that Prefect estimates its own work as "~95% established practice, ~5% new," and the article was published in the same window as the Dagster acquisition, how much weight should you give this piece's framing as evidence that you specifically need a graph-orchestration *product* (rather than just the design principle) to build secure agent workflows?

> [!question]- Answer
> Relatively little as product evidence, more as a design-principle argument. The security case (capability segregation, human-approval-as-node) is sound and implementable with plain code, LangGraph, Pydantic AI, or a hand-rolled state machine — it doesn't require Prefect's specific tooling. The article provides no benchmarks, named customers, or code samples to substantiate a claim that Prefect's implementation is uniquely necessary; its self-reported "95% established, 5% new" framing and its timing alongside the Dagster acquisition both suggest the piece functions primarily as strategic positioning, with the underlying design principle being the genuinely useful takeaway.
