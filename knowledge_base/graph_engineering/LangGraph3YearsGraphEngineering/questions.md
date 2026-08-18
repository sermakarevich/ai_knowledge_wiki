---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: 3 Years of Graph Engineering with LangGraph

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. In LangGraph's terms, what are the two components of a graph, and what is each responsible for?

> [!tip]- Answer
> Nodes do the actual work — they can be deterministic code, a single LLM call, a tool call, or a full agent with its own internal loop. Edges decide what happens next, either deterministically (always the same) or conditionally, based on a node's result, the current state, or an external signal. See [[wiki/01-modeling-agents-as-graphs|Modeling Agents as Graphs]].

### Q2. Why does the article say a workflow with predictable structure (e.g., "classify before answering or escalating") is a good candidate for a graph?

> [!tip]- Answer
> Because encoding that structure directly — the valid paths, where the model gets to choose, and where the system should enforce deterministic behavior — captures real world knowledge about how the system should work, the same way a prompt encodes domain knowledge. It stops you from hoping the model makes the right call every time and instead builds the right call into the structure itself. See [[wiki/01-modeling-agents-as-graphs|Modeling Agents as Graphs]].

### Q3. What kind of task does the article say should NOT be modeled as a graph, and what should be used instead?

> [!tip]- Answer
> Tasks that are inherently open-ended and agentic by nature — the article's example is generic deep research, where planning, delegation, search, reading, and synthesis can't be pinned down ahead of time. For these, an agent harness (the article names Deep Agents) should own the loop instead of a predefined graph, letting those capabilities emerge at runtime. See [[wiki/02-when-not-to-use-graphs|When Not to Use Graphs]].

### Q4. Both LangChain's own deep-research product and GPT Researcher made the same architectural move. What was it, and why does the article treat it as evidence for its graph/no-graph boundary?

> [!tip]- Answer
> Both moved away from a predefined, graph-shaped (multi-agent) pipeline toward a more agentic core loop / Deep Agents. The article treats this as real-world confirmation that when a task is fundamentally open-ended, forcing it into a fixed graph is the wrong move — independent teams converging on the same fix supports the claim rather than it being just one team's opinion. See [[wiki/02-when-not-to-use-graphs|When Not to Use Graphs]].

### Q5. The article claims "agent graphs are usually not DAGs." Why — what specifically requires cycles in production agents?

> [!tip]- Answer
> Cycles are needed for retrying failed tool calls, asking users for missing information, revising answers after validation, repeatedly calling tools until there's enough context, and pausing for human input before resuming. Because looping is one of the core parts of agentic systems, production agent graphs generally end up cyclic rather than acyclic. See [[wiki/03-lessons-from-three-years|Lessons from Three Years]].

### Q6. How does the article relate "loop engineering" to "graph engineering," and what does LangGraph's `Send` mechanism add on top of a basic loop?

> [!tip]- Answer
> The article treats loop engineering as a special case of graph engineering rather than a rival to it — citing David Khourshid's line that a loop is merely a directed, cyclic graph. `Send` goes further than a simple loop: it lets a node dynamically route work to a runtime-determined number of downstream nodes (the map-reduce case), so not every edge needs to be predefined in advance — the graph itself can grow branches at runtime. See [[wiki/03-lessons-from-three-years|Lessons from Three Years]].

### Q7. According to the article, what has genuinely changed in the recent wave of "graph engineering," as opposed to what LangGraph has always done?

> [!tip]- Answer
> What's changed is what can live inside a node: early on, nodes were deterministic code or a single LLM call, but now that agents (e.g., coding agents) are reliable enough to trust with real work, a node can be a full agent run — so you're orchestrating agents, not just LLM calls, inside the same graph structure LangGraph has used for three years. See [[wiki/04-whats-new-and-the-bigger-idea|What's Actually New, and the Bigger Idea]].

### Q8. The article's closing claim is that graph engineering "is not a new idea." Given that the piece is written by LangChain's own founders about their own product, how strong is the evidence for that claim, and what would make it more convincing?

> [!tip]- Answer
> The claim is asserted rather than demonstrated: the article names loop engineering and harness engineering as the "same idea" but does not trace a rigorous lineage (e.g., classical workflow engines, BPMN, or older state-machine-based agent frameworks) or address why "graph engineering" needed a new name if it isn't new. It would be more convincing with a concrete comparison to a pre-LLM system that already separated fixed structure from delegated judgment. See [[critical_thinking|Critical Analysis]].
