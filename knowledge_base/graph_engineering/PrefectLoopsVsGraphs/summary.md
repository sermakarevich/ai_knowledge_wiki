> [[index|Wiki]] | [[digest|Digest]]

# Loops vs. Graphs — Summary

**Article:** [Loops vs. Graphs](https://www.prefect.io/blog/loops-vs-graphs) — Prefect blog, 2026-07-22

## Human Readable TL;DR

Prefect (a workflow-automation company) argues that building AI agents has gone through three stages: first you write one good instruction (prompt engineering), then you wrap that instruction in a repeat-until-done loop (loop engineering), and now the state of the art is wiring several such steps together into an explicit map with boxes and arrows — a graph — where each box can have its own tools and rules, and arrows can even loop back on themselves. Their main pitch: graphs let you keep dangerous tools (like "issue a refund") away from the parts of the process that shouldn't have them, which is otherwise a real production risk. They also connect this to their business: they recently bought Dagster (a data-pipeline company that already thinks in graphs) and want their own "directed agentic graph" to become the standard way people build trustworthy business AI agents.

## TL;DR

Prefect's Jeremiah Lowin and Radhika Gulati frame agent engineering as a three-stage progression — prompt engineering, loop engineering, graph engineering — written partly in response to a viral tweet asking "loops or graphs?" A graph is nodes (units of work) connected by edges (decision-driven paths); Prefect's "directed agentic graph" deliberately permits cycles (unlike a traditional DAG) and lets each node carry its own tools, model, and access level. The strongest argument for graphs, in their telling, is security: segregating a dangerous capability (e.g., issuing a refund) into a separate, single-use node reached only after a diligence node approves it, rather than handing one agent every tool at once. Human approval and plain programmatic steps are modeled as ordinary nodes too. Prefect positions its graphs as a macro-orchestration layer sitting above single-agent frameworks like LangGraph and Pydantic AI, and backs the strategic bet with its Dagster acquisition — explicitly estimating the work as ~95% established orchestration practice and ~5% new AI-specific ideas.

## Problem & Motivation

Bare "loop engineering" (an agent repeating a step until some condition is met) gives businesses no way to verify a consistent decision path across runs, and it collapses tool access and self-reporting into the same untrustworthy channel — the article's example is a refund agent that can both issue a refund and falsely report that nothing went wrong at the exact same moment it did. Individuals using a chatbot don't need reproducibility or auditability; businesses running a multi-step workflow do, and current bare-loop agent APIs don't provide it.

## Main Original Ideas

- **Prompt → loop → graph as a maturity ladder**, each stage adding more structural control over agent behavior, with reproducibility as the missing ingredient that makes cross-run evaluation possible at all.
- **The "Ralph loop" as a cautionary tale** — a genuinely useful mechanism (loop engineering, borrowed from ML training loops) degraded in public discourse into an oversimplified viral version that became the thing everyone associates with the whole idea.
- **Directed agentic graph, defined**: nodes are units of business logic executed by an agent (or a human, or plain code, or an external-event wait); edges are decision-driven, one-directional paths; cycles are deliberately allowed (the key departure from a traditional DAG); each node can have distinct tools, parameters, access level, instructions, and even a different underlying model.
- **Capability segregation by decision path** as the strongest single case for graphs — a diligence node with no access to the dangerous tool, followed by a separate node that receives a locked-down, single-use version of that tool only after the decision point.
- **Control vs. autonomy as the central design tension** — full agent autonomy inside a node, control returning to the orchestrator exactly at an edge transition; nodes are only worth adding where monitoring, human intervention, retry logic, or programmatic injection actually matter.
- **Macro vs. micro orchestration**: LangGraph and Pydantic AI model the internals of a single agent as a graph; Prefect's directed agentic graphs operate one level up, treating each node as a complete agentic invocation (which could itself be built on those frameworks).

## Key Findings

- A degenerate single-node graph handed every tool is "loop engineering wearing a graph costume" — splitting work across nodes is what actually delivers per-step tool/model selection and purely programmatic steps.
- Human approval fits cleanly as just another node type, resolving an awkward pattern where approval is normally bolted onto a tool call or a skill-document request.
- The piece frames itself as responding responsibly to a viral tweet by connecting the current graph-engineering discourse to decades of prior orchestration experience, rather than letting a "worst version" of the idea become the canonical one (as happened with the Ralph loop).
- Prefect estimates its own directed-agentic-graph work as ~95% established software/orchestration practice, ~5% genuinely new AI-specific ideas.
- The Dagster acquisition (asset graphs + data lineage) combined with Prefect's durable agent-loop runtime is framed as a strategic "Avengers-assemble moment" underpinning the company's product direction.

## Suggestions & Future Directions

The article does not propose new techniques or benchmarks; its call to action is directional — expect Prefect's product to make directed agentic graphs the primary way agent behavior is represented (visualized conditional paths, failure locations, step-by-step observability), with early-access partners first and broader production release "in the coming months." It invites reader comments on confusion about graphs, agents, or MCP.

## Authors & Institutions

Jeremiah Lowin (CEO, Prefect) and Radhika Gulati (Sr. Product Marketing Manager, Prefect); published on the Prefect company blog, 2026-07-22.
