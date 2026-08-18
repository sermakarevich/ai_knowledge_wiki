# 3 Years of Graph Engineering with LangGraph

**Authors:** Sydney Runkle, Harrison Chase
**Publication date:** July 22, 2026
**URL:** https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph
**Retrieved:** 2026-08-18

---

## Modeling agents as graphs

A graph gives you a concrete way to define the workflow an agent follows.

In LangGraph, nodes do work. A node can be deterministic code, a single LLM call, a tool call, or a full agent with its own internal loop.

Edges define what happens next. Some edges are deterministic. Others are conditional, based on the result of a node, the current state, or some external signal.

You can think of this as a state machine. The graph defines the workflow, the state that moves through it, and the transitions between steps.

## When to represent agents as graphs

Real-world agent workflows often have predictable structure: a support agent classifies an issue before answering or escalating, a coding agent inspects the repository before proposing a change, and a compliance workflow requires approval before taking an external action.

Graphs let you encode that structure directly: the valid paths, where the model gets to choose, and where the system should enforce deterministic behavior instead of hoping the model makes the right call every time.

By representing the system as a graph, you are encoding your world knowledge of how this system should work. Just as prompts contain domain knowledge that separates your agent from generic ChatGPT, so can these "cognitive architectures".

Take a knowledge base agent that uses three subagents for search: a GitHub agent for code, issues, and pull requests, a Notion agent for internal docs and wikis, and a Slack agent for relevant threads. The workflow has three fixed stages: classify, search, synthesize.

The result is code and model reasoning working together: the model reasons where it adds value, code handles the rest, and the agent gets cheaper, faster, and more predictable.

## When not to use graphs

Some tasks are more agentic by nature, and forcing them into deterministic paths is the wrong move. In these cases, you don't want to represent the system as a graph but rather just use an agent harness (like Deep Agents).

Generic deep research is a good example: a research agent needs to plan, delegate, search, read, and synthesize in ways that are hard to pin down ahead of time. We built early deep research on predefined LangGraph workflows, then moved to a more agentic core loop. GPT Researcher, a popular deep research implementation, made the same move, swapping its graph-shaped multi-agent pipeline for Deep Agents so planning, delegation, and context management emerge in the harness rather than being hardcoded in the graph.

## What building LangGraph taught us

We've been building agents powered by graphs for the last three years. Here's what we've learned.

**First, agent graphs are usually not DAGs.**

Production agents need cycles: retrying failed tool calls, asking users for missing information, revising answers after validation, calling tools repeatedly until they have enough context, and pausing for human input before resuming. Looping is a core part of agentic systems, so they are likely not DAGs.

**Second, loops are simple graphs.**

Loop engineering isn't an alternative to graphs, so much as a simple version of them. As David Khourshid put it, a loop is just a directed, cyclic graph. In fact, the LangChain framework, which is based on a simple agentic loop, is built on top of LangGraph.

**Third, dynamic transitions matter.**

You do not always want to define every edge up front. Sometimes a node decides at runtime how much work to create. Map-reduce is the classic case: split an input into pieces, send each to a worker, then combine the results. The number of workers depends on the input, and you do not know that number in advance.

LangGraph handles this with Send, which lets a node route work to one or more downstream nodes dynamically, without statically defining every transition.

This is important because useful agent systems mix known structure with runtime variability. You might know research should fan out and then synthesize, but not how many sources there will be. You might know a supervisor should delegate to workers, but not know which specific workers to use until the task starts. Graphs still need flexibility at runtime.

## What's actually new

Representing agentic systems as graphs isn't new, we've been doing it for three years! Has anything changed in this new wave of "graph engineering"?

A generous interpretation would say that what's changed is what you can put inside a node. Early on, nodes were deterministic code or a single LLM call. Now that agents themselves are reliable enough to trust with real work, a node can be a full agent run — you're orchestrating agents, not just LLM calls.

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
