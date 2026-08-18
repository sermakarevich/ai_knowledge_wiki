> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Modeling Agents as Graphs

**In one sentence:** A graph is a concrete state-machine representation of an agent's workflow — nodes do work, edges decide what happens next — and encoding real-world agents as graphs lets you fix the predictable structure in code while reserving the model's discretion for where it actually adds value.

## Key points

- A graph gives you a concrete way to define the workflow an agent follows: nodes do work, edges define what happens next, and state flows through the structure, making it essentially a state machine.
- In LangGraph, nodes can be deterministic code, a single LLM call, a tool call, or even a full agent with its own internal loop — the graph composition is uniform across all of them.
- Edges come in two kinds: deterministic edges that always fire the same way, and conditional edges whose choice depends on a node's result, the current state, or an external signal.
- Real-world agent workflows have predictable structure — a support agent classifies before answering or escalating, a coding agent inspects the repository before proposing a change, a compliance workflow requires approval before external action — and graphs let you encode that structure directly.
- Representing an agent as a graph means encoding your world knowledge of how the system should work, the same way prompts encode domain knowledge to separate your agent from generic ChatGPT; these graphs are effectively "cognitive architectures".
- In the knowledge-base agent example (GitHub + Notion + Slack search subagents), the three fixed stages — classify, search, synthesize — are handled by code, while the model reasons only where it adds value, making the agent cheaper, faster, and more predictable.

---

## Modeling agents as graphs

A graph gives you a concrete way to define the workflow an agent follows. In LangGraph, nodes do work. A node can be deterministic code, a single LLM call, a tool call, or a full agent with its own internal loop.

Edges define what happens next. Some edges are deterministic. Others are conditional, based on the result of a node, the current state, or some external signal.

You can think of this as a state machine. The graph defines the workflow, the state that moves through it, and the transitions between steps.

## When to represent agents as graphs

Real-world agent workflows often have predictable structure: a support agent classifies an issue before answering or escalating, a coding agent inspects the repository before proposing a change, and a compliance workflow requires approval before taking an external action.

Graphs let you encode that structure directly: the valid paths, where the model gets to choose, and where the system should enforce deterministic behavior instead of hoping the model makes the right call every time.

By representing the system as a graph, you are encoding your world knowledge of how this system should work. Just as prompts contain domain knowledge that separates your agent from generic ChatGPT, so can these "cognitive architectures".

Take a knowledge base agent that uses three subagents for search: a GitHub agent for code, issues, and pull requests, a Notion agent for internal docs and wikis, and a Slack agent for relevant threads. The workflow has three fixed stages: classify, search, synthesize.

The result is code and model reasoning working together: the model reasons where it adds value, code handles the rest, and the agent gets cheaper, faster, and more predictable.

**Covers:** Modeling agents as graphs; When to represent agents as graphs
