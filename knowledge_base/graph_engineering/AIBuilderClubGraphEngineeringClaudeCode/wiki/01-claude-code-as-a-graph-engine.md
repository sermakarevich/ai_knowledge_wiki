> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Claude Code as a Graph Engine

**In one sentence:** Graph engineering with Claude requires no new framework, because Claude Code already ships the primitives — subagents are the nodes, the orchestrator's runtime routing is the edges, and returned results are the shared state.

## Key points

- "Graph engineering" as it trended in mid-July 2026 is not a new discipline to adopt — Anthropic had already shipped the same pattern under a plainer name before that framing caught on.
- A graph is three things: nodes (an agent or step that does one job), edges (the routing that decides which node runs next, including branches, fan-out, fan-in, and loops back), and shared state (the data that flows along the edges); a single agent loop is the smallest possible graph — one node with an edge back to itself — and graph engineering is what begins when one node is no longer enough.
- Claude Code's subagents, hooks, and the Claude Agent SDK map directly onto those three parts: nodes become subagents (a separate context window, its own system prompt, and scoped tool access), edges become the main agent's runtime routing decisions (dynamic rather than hand-drawn), and shared state becomes a subagent's returned result flowing back to the orchestrator and being passed to the next node.
- The three primitives come in rough order of commitment: subagents as markdown files with YAML frontmatter in `.claude/agents/` (fastest, version-controlled by default), hooks as deterministic/guaranteed edges (the difference between "the agent usually runs the tests" and "the tests always run before the writer node hands off"), and the Claude Agent SDK's `agents` parameter for graphs that must run unattended, be tested like code, or fan out to subagents programmatically.
- Anthropic's own multi-agent research system is the proof this already ships — a lead agent (orchestrator node) spins up parallel specialized subagents (worker nodes) plus a separate citation pass, beating a single-agent Claude Opus 4 baseline by 90.2% on an internal research eval at roughly 15x the token cost of a normal chat turn, with early orchestrator versions over-spawning subagents for simple questions — the real tradeoff is buying quality and parallelism with tokens and coordination overhead, which only pays off when the job genuinely has separable parts.

---

## Why no new framework: the primitives already ship

Graph engineering means wiring specialized agents into a structure of nodes, edges, and shared state — but the surprise for most builders is that a Python orchestration framework is not required, because Claude Code already ships the primitives:

- **Subagents** are the nodes.
- The **main agent** that delegates to them is the orchestrator node, and its routing between them is the edges.
- The **Claude Agent SDK** is how you lift the whole thing into code when the interactive version stops being enough.

If you have been reading the graph engineering posts and wondering what to actually build with, that is the shortest path: you probably have the tool open already.

### "Graph engineering" is a label for a mechanism that already exists

When "graph engineering" trended in mid-July 2026, the framing made it sound like a new discipline you had to go adopt. But Anthropic had already shipped the pattern under a plainer name. Their guide on building effective agents lays out five composable patterns — **prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer**. Read those as graphs and they snap into focus:

- **prompt chaining** is a line of nodes (each step's output feeds the next);
- **routing** is a conditional edge (deciding which downstream step runs);
- **orchestrator-workers** is a hub node fanning out to worker nodes and fanning their results back in — a graph in all but name.

Graph engineering is the label; this is the mechanism.

## What "graph engineering with Claude" actually means

Strip the term down and a graph is three things:

- **Nodes** — an agent or a step that does one job.
- **Edges** — the routing that decides which node runs next (including branches, fan-out, fan-in, and loops back).
- **Shared state** — the data that flows along the edges.

A **single agent loop** is the smallest possible graph — **one node with an edge back to itself**. Graph engineering is what you do when one node is no longer enough and you need several specialized ones wired together. Doing that "with Claude" does not mean learning a new API first. It means mapping those three parts onto tools Claude Code already exposes:

### The three-part mapping

- **Nodes → subagents.** Each subagent is a separate agent instance with its **own context window**, **its own system prompt**, and **scoped tool access**. That isolation is exactly what makes a good node: a researcher subagent that only reads and searches, a writer that only drafts, a reviewer that only critiques — none of them stepping on each other's context.
- **Edges → the orchestrator's routing.** Your main Claude session is itself a node, and its decisions about which subagent to spawn, when, and with what brief are the edges. Because the orchestrator routes at runtime rather than following a hardcoded diagram, you get **dynamic edges without drawing one by hand**.
- **Shared state → the returned results.** A subagent's final output flows back to the orchestrator, which passes the relevant piece to the next node. That handoff is the state moving along the edge.

## The primitives Claude Code already gives you

You wire a graph in Claude Code with three things, in rough order of how far you are willing to go:

### 1. Subagents in `.claude/agents/`

Drop a markdown file with YAML frontmatter per node — a name, a description, the tools it may use, and its system prompt. The main agent reads these and delegates to them. This is the **fastest** way to stand up a multi-node graph, and it is **version-controlled by default** because it is just files in your repo.

### 2. Hooks as deterministic edges

When you need an edge that fires **every time** rather than one the model chooses, Claude Code hooks (run on events like a tool call finishing or a session stopping) give you a guaranteed transition. That is the difference between "the agent usually runs the tests" and "the tests always run before the writer node hands off."

### 3. The Claude Agent SDK

When the graph needs to run **unattended**, be **tested like code**, or fan out to subagents programmatically, you define the same nodes through the SDK's `agents` parameter in Python or TypeScript. Same node-edge-state shape, now embeddable in a larger system.

### Hand-roll the graph interactively first, then lift the stable shape into the SDK

The order matters. A graph you hand-rolled and watched run is a graph you understand. Reaching for the SDK before you have seen the shape work is how you end up debugging orchestration you never really designed.

## Anthropic already ships graph engineering (they call it orchestrator-workers)

The clearest proof that this is not a rebrand you have to wait on is **Anthropic's own multi-agent research system**. It is an orchestrator-worker graph: a lead agent plans the work, spins up specialized subagents that run in parallel, and a separate pass adds citations. The subagents are nodes, the lead agent is the **orchestrator node** whose delegation forms the **edges**, and the plan plus each subagent's findings are the **shared state**.

- **90.2%** — Anthropic reported this multi-agent setup beat a **single-agent Claude Opus 4** baseline on an internal research eval.
- **15x** — the same post is honest about the cost: that multi-agent graph burned roughly **15x the tokens of a normal chat turn**, the part most graph-engineering hype skips.
- **Over-spawning** — early versions of the orchestrator would fire off far more subagents than a simple question needed — a concrete failure mode of the orchestrator.

That is the **real tradeoff of graph engineering**: you are buying quality and parallelism with tokens and coordination overhead. A graph earns its keep when the job genuinely has separable parts. When it does not, you have built a more expensive way to run one loop.

**Covers:** What "graph engineering with Claude" means; nodes/edges/state mapped onto subagents/orchestrator routing/returned results; the three primitives (subagents, hooks, Claude Agent SDK) and hand-roll-then-lift ordering; Anthropic's orchestrator-workers system as existing proof (90.2% improvement, 15x tokens, over-spawn failure mode) (source chunk 01)
