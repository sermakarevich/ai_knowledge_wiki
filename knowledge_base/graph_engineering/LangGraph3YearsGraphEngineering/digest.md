> [[index|Wiki]] | [[summary|Summary]]

# 3 Years of Graph Engineering with LangGraph — Digest

The whole source at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-modeling-agents-as-graphs|Modeling Agents as Graphs]]

**In one sentence:** A graph is a concrete state-machine representation of an agent's workflow — nodes do work, edges decide what happens next — and encoding real-world agents as graphs lets you fix the predictable structure in code while reserving the model's discretion for where it actually adds value.

- A graph gives you a concrete way to define the workflow an agent follows: nodes do work, edges define what happens next, and state flows through the structure, making it essentially a state machine.
- In LangGraph, nodes can be deterministic code, a single LLM call, a tool call, or even a full agent with its own internal loop — the graph composition is uniform across all of them.
- Edges come in two kinds: deterministic edges that always fire the same way, and conditional edges whose choice depends on a node's result, the current state, or an external signal.
- Real-world agent workflows have predictable structure — a support agent classifies before answering or escalating, a coding agent inspects the repository before proposing a change, a compliance workflow requires approval before external action — and graphs let you encode that structure directly.
- Representing an agent as a graph means encoding your world knowledge of how the system should work, the same way prompts encode domain knowledge to separate your agent from generic ChatGPT; these graphs are effectively "cognitive architectures".
- In the knowledge-base agent example (GitHub + Notion + Slack search subagents), the three fixed stages — classify, search, synthesize — are handled by code, while the model reasons only where it adds value, making the agent cheaper, faster, and more predictable.

## 2. [[wiki/02-when-not-to-use-graphs|When Not to Use Graphs]]

**In one sentence:** Some tasks are inherently agentic, and forcing them into a deterministic graph is the wrong move — for those, an agent harness (like Deep Agents) is the right substrate.

- Some tasks are more agentic by nature; forcing them into deterministic (graph) paths is the wrong move.
- For such tasks you should not represent the system as a graph at all, but use an agent harness like Deep Agents instead.
- Generic deep research is a good example: a research agent must plan, delegate, search, read, and synthesize in ways that are hard to pin down ahead of time.
- LangChain built early deep research on predefined LangGraph workflows, then moved to a more agentic core loop.
- GPT Researcher, a popular deep research implementation, made the same move: it swapped its graph-shaped multi-agent pipeline for Deep Agents so that planning, delegation, and context management emerge in the harness rather than being hardcoded in the graph.

## 3. [[wiki/03-lessons-from-three-years|Lessons from Three Years]]

**In one sentence:** Three years of building production agents taught three lessons — agent graphs are usually not DAGs, loops are simply a basic form of graphs, and dynamic transition is essential.

- Agent graphs are usually not DAGs: production agents inherently require cycles.
- Cycles are needed for retrying failed tool calls, asking users for missing information, revising answers after validation, repeatedly calling tools until there is enough context, and pausing for human input before resuming — looping is one of the core parts of agentic systems.
- Loops are simple graphs: loop engineering is not an alternative to graphs, but a simple version of them. As David Khorshid put it, a loop is merely a directed, cyclic graph — in fact, the LangChain framework, built on top of a simple agentic loop, is constructed on top of LangGraph.
- Dynamic transitions matter: we should not always predefine all edges in advance, because at runtime a node may decide how much work to generate.
- The Send mechanism is precisely for this purpose: it allows a node to dynamically route work to one or more downstream nodes without statically defining every transition — the classic case being map-reduce, where the number of workers depends on the input and cannot be known in advance.
- This is important because useful agent systems combine known structure with runtime variability — for example, knowing that a research task first fans out and then integrates, but not knowing how many sources exist in advance; or knowing that a supervisor delegates to workers, but not knowing which worker until the task begins. Graphs still need runtime flexibility.

## 4. [[wiki/04-whats-new-and-the-bigger-idea|What's Actually New, and the Bigger Idea]]

**In one sentence:** What's genuinely changed is what can live inside a node — a node can now be a full agent run rather than fixed code or a single LLM call — but graph engineering itself is just the latest name for a long-established approach to building reliable agents, the same idea behind loop engineering and harness engineering.

- What has changed in the new wave of graph engineering is what you can put inside a node: early on, nodes were deterministic code or a single LLM call, but now that agents are reliable enough to trust with real work, a node can be a full agent run — you're orchestrating agents, not just LLM calls.
- Coding agents illustrate this shift: they are among the most effective and impactful agents in production today, and embedding one as a node inside a larger graph is a newly practical pattern.
- The deterministic-to-agentic scale has three tiers, each shown in the docs-agent example: fixed steps (the slack and linear operations powered by set code and API calls), model steps (the classifier and the synthesize step using a single LLM call with no tools), and agent steps (the reference docs agent and the conceptual docs agent completing more open-ended work in their relevant codebases).
- Graph engineering is not a new idea — it is the latest name for a well-established approach to building reliable agents.
- It is the same idea behind loop engineering and harness engineering: putting model reasoning in the right places, with the right context, at each step.

## The argument in five moves

1. Represent agent workflows as graphs — nodes do work, edges decide what's next, state flows through.
2. Use a graph specifically when the workflow has predictable structure worth encoding as world knowledge.
3. Don't use a graph when the task is inherently open-ended — hand it to an agent harness instead.
4. Three years of production taught that real agent graphs cycle, that loops are just a special case of graphs, and that edges sometimes must be created at runtime (`Send`).
5. What's new is what a node can now be — a full agent, not just code or one LLM call — letting a single graph mix fixed, model, and agent steps.
6. Graph engineering therefore isn't a new trend; it's the current name for putting model reasoning in the right place, the same discipline behind loop and harness engineering.
7. The practical takeaway: pick the abstraction (graph vs. harness) by whether the task's structure is knowable in advance, then try LangGraph.
