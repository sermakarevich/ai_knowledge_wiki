# 3 Years of Graph Engineering with LangGraph

**Article:** [3 Years of Graph Engineering with LangGraph](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph) — LangChain blog, 2026-07-22

## Human Readable TL;DR

Think of building an AI agent like designing a factory floor instead of hiring one incredibly talented (but occasionally forgetful) generalist. A graph is the factory layout: fixed stations do fixed jobs, and at certain points a supervisor (the model) decides which station a piece of work goes to next. LangChain's founders say that after three years of building this kind of factory (LangGraph), they've learned it's rarely a straight assembly line — pieces loop back for rework, get sent to multiple stations at once, or wait for a human to sign off — and that some jobs are too improvisational for a factory layout at all and need a skilled generalist instead. Their final point: none of this is new. Good engineers have always separated "the part a machine should always do the same way" from "the part that needs judgment" — graphs are just today's word for that old idea.

## Technical TL;DR

A graph is a state-machine representation of an agent workflow: nodes (deterministic code, a single LLM call, a tool call, or a full nested agent) do work, and edges (deterministic or conditional) decide transitions, with state flowing through the structure. The article argues graphs are the right tool when a workflow has predictable structure (classify → search → synthesize) but the wrong tool when a task is inherently open-ended (generic deep research), where an agent harness like Deep Agents should own the loop instead. Three lessons from three years of production use: (1) agent graphs are usually not DAGs — cycles are needed for retries, clarifying questions, revision, and human-in-the-loop pauses; (2) a loop is simply a directed, cyclic graph, so loop engineering is a special case of graph engineering, not an alternative to it; (3) dynamic transitions matter — LangGraph's `Send` mechanism lets a node fan work out to a runtime-determined number of downstream nodes (the map-reduce case), so graphs need not have every edge fixed in advance. The article closes by arguing the only genuinely new thing is what can live inside a node — a full agent run, not just an LLM call — and that "graph engineering" itself is just the current name for an established discipline shared with loop engineering and harness engineering: putting model reasoning in the right place with the right context.

## Problem & Motivation

Teams building production LLM agents face a recurring failure mode: give the model total discretion over every step and you get behavior that's expensive, slow, and unpredictable; hardcode everything and you lose the model's ability to handle the genuinely ambiguous parts of the task. The article's motivation is to give practitioners a mental model — and a concrete abstraction (the graph) — for deciding, workflow by workflow and even node by node, where to put fixed logic and where to put model judgment, based on three years of building and operating LangGraph in production.

## Main Original Ideas

- **Graphs as encoded world knowledge.** Representing a workflow as a graph is treated as equivalent to what a prompt does with domain knowledge: it encodes how the system *should* work, functioning as a "cognitive architecture" rather than just plumbing.
- **A graph/no-graph boundary.** Not every agent should be a graph — tasks that are inherently open-ended (planning, delegation, and context management that can't be pinned down ahead of time) belong in an agent harness instead, illustrated by LangChain's own deep-research product and GPT Researcher both migrating away from graph-shaped pipelines toward Deep Agents.
- **Loops are a special case of graphs, not a rival to them.** Citing David Khourshid's line that "a loop is merely a directed, cyclic graph," the article positions loop engineering as nested inside graph engineering rather than as a competing paradigm — and notes the LangChain agent framework itself is built on top of LangGraph.
- **Dynamic transitions via `Send`.** Because a node's output can determine how much downstream work exists (the map-reduce case), a graph's edges cannot always be fully predefined; `Send` lets a node route to a runtime-determined set of downstream nodes.
- **The deterministic-to-agentic scale.** A single graph can mix three tiers of node: fixed steps (plain code/API calls), model steps (a single LLM call, no tools), and agent steps (a full agent run with its own loop) — illustrated with a docs agent that mixes Slack/Linear API calls, a classifier, and reference/conceptual docs agents.

## Key Findings

This is a practitioner opinion piece, not an empirical study, so there are no benchmark numbers — the "findings" are three lessons distilled from three years of operating LangGraph in production, plus a framing claim:

- **Lesson 1 — agent graphs are usually not DAGs.** Cycles are structural, not incidental: retrying failed tool calls, asking for missing information, revising after validation, and pausing for human input all require loops.
- **Lesson 2 — loops are simple graphs.** Loop engineering doesn't replace graph engineering; it's what a graph looks like when it's just a cycle.
- **Lesson 3 — dynamic transitions are essential.** Real agent systems need to combine known structure (a research task fans out then integrates) with runtime variability (how many sources, which workers) — a graph that can't add edges at runtime can't model this.
- **The bigger-idea claim.** Graph engineering, loop engineering, and harness engineering are framed as the same underlying discipline wearing different names, not three separate trends.

## Suggestions & Future Directions

The article's implicit recommendation is a decision procedure: model a workflow as a graph if it has real predictable structure; reach for an agent harness instead when the task is fundamentally open-ended; and when a graph is the right call, deliberately choose — per node — where on the deterministic-to-agentic scale that node should sit, upgrading nodes to full agent runs only where the underlying agent capability (e.g., coding agents) is now reliable enough to trust. The explicit call to action is simply: "If you want to try out graph engineering, try out LangGraph."

## Authors & Institutions

Sydney Runkle, Harrison Chase — LangChain
