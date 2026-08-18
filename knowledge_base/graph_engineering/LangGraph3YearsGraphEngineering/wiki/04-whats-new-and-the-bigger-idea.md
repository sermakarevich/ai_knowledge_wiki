> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# What's Actually New, and the Bigger Idea

**In one sentence:** What's genuinely changed is what can live inside a node — a node can now be a full agent run rather than fixed code or a single LLM call — but graph engineering itself is just the latest name for a long-established approach to building reliable agents, the same idea behind loop engineering and harness engineering.

## Key points

- What has changed in the new wave of graph engineering is what you can put inside a node: early on, nodes were deterministic code or a single LLM call, but now that agents are reliable enough to trust with real work, a node can be a full agent run — you're orchestrating agents, not just LLM calls.
- Coding agents illustrate this shift: they are among the most effective and impactful agents in production today, and embedding one as a node inside a larger graph is a newly practical pattern.
- The deterministic-to-agentic scale has three tiers, each shown in the docs-agent example: fixed steps (the slack and linear operations powered by set code and API calls), model steps (the classifier and the synthesize step using a single LLM call with no tools), and agent steps (the reference docs agent and the conceptual docs agent completing more open-ended work in their relevant codebases).
- Graph engineering is not a new idea — it is the latest name for a well-established approach to building reliable agents.
- It is the same idea behind loop engineering and harness engineering: putting model reasoning in the right places, with the right context, at each step.

---

## What's actually new

Representing agentic systems as graphs isn't new — LangGraph has been doing it for three years. So has anything changed in this new wave of "graph engineering"? A generous interpretation would say that what's changed is what you can put inside a node. Early on, nodes were deterministic code or a single LLM call. Now that agents themselves are reliable enough to trust with real work, a node can be a full agent run — you're orchestrating agents, not just LLM calls.

Coding agents are a good example of this. They're some of the most effective and impactful agents in production today, and embedding one as a node inside a larger graph is a newly practical pattern.

Each node in this graph sits at a different point on the deterministic-to-agentic scale:

* Fixed steps: the slack and linear operations are powered by set code and API calls.
* Model steps: the classifier and the synthesize step use a single LLM call with no tools.
* Agent steps: the reference docs agent and the conceptual docs agent complete more open ended work in their relevant codebases.

The mix of determinism and agency here is what makes this docs agent predictable, powerful, and efficient.

## The bigger idea

Graph engineering isn't a new idea. It's the latest name for a well established approach to building reliable agents.

It's the same idea behind loop engineering and harness engineering: putting model reasoning in the right places, with the right context, at each step.

If you want to try out graph engineering, try out LangGraph.

**Covers:** What's actually new; The bigger idea
