# What Is Graph Engineering?

**Video:** [What Is Graph Engineering?](https://www.youtube.com/watch?v=S1vqM0aTRFc) — KGP Talkie, ~9 min
**Wiki:** [[index]] | **Digest:** [[digest]]

## Human Readable TL;DR

This short video explains "graph engineering," a term you might hear in AI job interviews or online. The presenter's main point: it's not actually a new technique. It's just a new name for something tools like LangGraph, Google ADK, and Microsoft AutoGen have already been doing for years — wiring together multiple small "agent teams" (each one an agent that produces an answer and a second agent that checks and improves it) into a bigger coordinated system. The video also clears up a common mix-up: graph engineering is not the same thing as GraphRAG, even though both use words like "node" and "edge." And it ends with a practical warning: using an agent instead of a plain AI call costs roughly 4x more, and using a whole graph of agents costs roughly 15x more — so don't reach for a graph unless the task actually needs one.

## TL;DR

The video positions graph engineering as the top of a five-layer "agentic-AI technique stack": prompt engineering, context engineering, and harness engineering apply on the input side inside a single AI agent; loop engineering applies outside the agent, pairing a producing agent with an evaluating agent so the pair can "self-prompt" without either agent prompting itself; and graph engineering is what you get when multiple such loop-engineering solutions are arranged and coordinated together as nodes in a graph, where a node can be an agent, a loop-engineering solution, or a direct LLM call. The presenter stresses this is not new — LangGraph, Google ADK, and Microsoft AutoGen have used this exact pattern for years, only the name is new. The video then distinguishes graph engineering from GraphRAG: GraphRAG's nodes are static, passive entities connected by relationship-only edges with no data flow, while graph engineering's nodes actively take action and its edges carry data flowing from node to node — so the two cannot be equated despite sharing vocabulary. It closes with a cost-based decision rule: decomposing a simple task (like summarizing one PDF) into a multi-node graph is overkill; a single agent costs roughly 4x the tokens of a plain LLM call, and a graph of agents costs roughly 15x, so the practical advice is to match the technique (LLM call, agent, harness engineering, loop engineering, or graph engineering) to the task's actual complexity rather than defaulting to the most sophisticated option.

## Problem & Motivation

"Graph engineering" is a term circulating in AI job interviews and online discourse, and viewers may encounter it without knowing whether it names something genuinely new or is just relabeling. The video's motivation is to demystify the term so viewers can answer confidently at a job or in an interview, and to prevent the common confusion between graph engineering and GraphRAG.

## Main Original Ideas

1. **The five-layer agentic-technique stack.** Prompt, context, and harness engineering apply inside an agent on the input side; loop engineering applies outside the agent; graph engineering is multiple loop-engineering solutions coordinated together.
2. **Loop engineering is agent-evaluates-agent, not self-reference.** A single agent cannot self-prompt itself — the working pattern is a producer agent plus an evaluator agent that re-prompts the producer, together forming a "self-prompting solution."
3. **Graph engineering = coordinated self-prompting solutions as nodes.** Arranging multiple self-prompting solutions together, where each node can be an agent, a loop-engineering solution, or a direct LLM call, produces a graph; nodes are orchestrated to reach a goal.
4. **Graph engineering ≠ GraphRAG.** GraphRAG's nodes are static/passive and its edges carry no data; graph engineering's nodes take action and its edges carry data flowing between nodes — the shared "node"/"edge" vocabulary is coincidental, not conceptual overlap.
5. **A cost-based decision rule.** Decomposing simple tasks into a graph is "overdoing it"; pick the cheapest technique (LLM call, agent, harness engineering, loop engineering, graph engineering) that fits the task's actual complexity.

## Key Findings

- Graph engineering is explicitly framed as **not a new technique** — LangGraph, Google ADK, and Microsoft AutoGen have implemented this pattern for years under different names.
- **Cost multipliers (self-reported, no methodology given):** a single agent costs roughly **4x** the tokens/cost of a plain LLM call baseline; a graph of agents costs roughly **15x**.
- The GraphRAG distinction rests on two properties: node passivity vs. action, and edge data-flow vs. relationship-only.

## Suggestions & Future Directions

The presenter's only forward-looking guidance is the decision framework itself: before reaching for graph engineering, check whether the task's complexity actually warrants the added cost, and be ready to explain the "not a new technique" framing and the graph-vs-GraphRAG distinction in an interview setting.

## Authors & Institutions

Lakshmikanth, KGP Talkie
