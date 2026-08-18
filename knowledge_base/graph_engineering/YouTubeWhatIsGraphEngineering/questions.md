---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: What Is Graph Engineering?

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. Why does the presenter insist a single agent cannot "self-prompt itself," and what pattern actually makes a self-prompting solution work?

> [!tip]- Answer
> A single agent trying to re-prompt its own loop directly is the incorrect technique and cannot work. The working pattern needs two agents: agent one produces a response, and agent two evaluates that response and re-prompts agent one — the loop closes through a second agent's evaluation, not through self-reference. See [[wiki/01-graph-engineering-defined|Graph Engineering Defined]].

### Q2. What is a "node" in graph engineering, and what three things can it be?

> [!tip]- Answer
> A node is one coordinated unit in a graph-engineering system, orchestrated together with other nodes to reach a goal. A node can be an agent, a self-prompting (loop-engineering) solution, or a direct LLM call. See [[wiki/01-graph-engineering-defined|Graph Engineering Defined]].

### Q3. GraphRAG and graph engineering both use the words "node" and "edge." What two structural properties actually distinguish them?

> [!tip]- Answer
> Node behavior and edge behavior. In GraphRAG, nodes are static things/entities that take no action, and edges only express a relationship with no data flowing between nodes. In graph engineering, nodes actively take action (agents, loop parts, or direct LLM calls), and edges carry data that flows from node to node. See [[wiki/02-graph-engineering-vs-graphrag|Graph Engineering vs GraphRAG]].

### Q4. Why does the presenter say decomposing a simple task like "summarize this PDF" into a multi-node graph is "overdoing it"?

> [!tip]- Answer
> A simple, single-task problem doesn't need to be broken into multiple coordinated parts — routing it through a multi-node graph adds structural overhead (and cost) without any matching benefit, since graph engineering exists for genuinely multi-part problems, not one-shot tasks. See [[wiki/03-when-to-use-graph-engineering|When to Use Graph Engineering]].

### Q5. According to the video's self-reported cost multipliers, roughly how much more expensive (in tokens/cost) is a single agent and a graph of agents compared to a plain LLM call — and what caveat should you attach to those numbers?

> [!tip]- Answer
> Roughly 4x for a single agent and roughly 15x for a graph of agents, versus a plain LLM call baseline. The caveat: these are the presenter's own approximate, unsourced figures with no stated methodology or benchmark behind them, so they should be treated as a rough intuition rather than a measured result. See [[wiki/03-when-to-use-graph-engineering|When to Use Graph Engineering]] and [[critical_thinking|Critical Analysis]].

### Q6. A team wants to build a system that answers a single, well-scoped factual question by making one call to an LLM. A teammate suggests wrapping it in a full multi-agent graph "to be safe." Using this video's decision framework, how would you respond?

> [!tip]- Answer
> Push back: per the video's decision framework, you should pick the cheapest technique that fits the task's actual complexity, not default to the most sophisticated one. A single well-scoped factual question is exactly the kind of simple task the presenter warns against over-engineering — a plain LLM call is likely sufficient, and wrapping it in a graph would add roughly 15x the cost for no corresponding benefit. See [[wiki/03-when-to-use-graph-engineering|When to Use Graph Engineering]].
