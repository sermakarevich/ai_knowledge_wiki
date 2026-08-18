> [[index|Wiki]] | [[summary|Summary]]

# Graph Engineering with Claude Code: Anthropic's Agent Graph — Digest

The whole article at medium depth: both sections' headline claim and key points, in order. ~5 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-claude-code-as-a-graph-engine|Claude Code as a Graph Engine]]

**In one sentence:** Graph engineering with Claude requires no new framework, because Claude Code already ships the primitives — subagents are the nodes, the orchestrator's runtime routing is the edges, and returned results are the shared state.

- "Graph engineering" as it trended in mid-July 2026 is not a new discipline to adopt — Anthropic had already shipped the same pattern under a plainer name before that framing caught on.
- A graph is three things: nodes (an agent or step that does one job), edges (the routing that decides which node runs next, including branches, fan-out, fan-in, and loops back), and shared state (the data that flows along the edges); a single agent loop is the smallest possible graph — one node with an edge back to itself — and graph engineering is what begins when one node is no longer enough.
- Claude Code's subagents, hooks, and the Claude Agent SDK map directly onto those three parts: nodes become subagents (a separate context window, its own system prompt, and scoped tool access), edges become the main agent's runtime routing decisions (dynamic rather than hand-drawn), and shared state becomes a subagent's returned result flowing back to the orchestrator and being passed to the next node.
- The three primitives come in rough order of commitment: subagents as markdown files with YAML frontmatter in `.claude/agents/` (fastest, version-controlled by default), hooks as deterministic/guaranteed edges (the difference between "the agent usually runs the tests" and "the tests always run before the writer node hands off"), and the Claude Agent SDK's `agents` parameter for graphs that must run unattended, be tested like code, or fan out to subagents programmatically.
- Anthropic's own multi-agent research system is the proof this already ships — a lead agent (orchestrator node) spins up parallel specialized subagents (worker nodes) plus a separate citation pass, beating a single-agent Claude Opus 4 baseline by 90.2% on an internal research eval at roughly 15x the token cost of a normal chat turn, with early orchestrator versions over-spawning subagents for simple questions — the real tradeoff is buying quality and parallelism with tokens and coordination overhead, which only pays off when the job genuinely has separable parts.

## 2. [[wiki/02-wiring-your-first-graph|Wiring Your First Graph]]

**In one sentence:** The first agent graph in Claude Code is a few narrowly-scoped subagents (one per node) with an orchestrator that routes and loops between them, fan-out for parallel work and hooks for non-negotiable edges — but only after each node is already a loop that reliably ships on its own.

- A good first graph is a job that genuinely splits into a produce step and an independent check step — draft-then-review, research-then-write, build-then-test — wired as one subagent per node, each with a narrow system prompt and only the tools it needs (the reviewer gets no write access, the writer no web search), because narrow nodes are what make the graph better than one big prompt.
- The orchestrator (main agent) routes between nodes — researcher → writer → reviewer — and the loop-back that sends a rejected draft back to the writer is a real edge, a node with a conditional return; when the work is genuinely parallel (e.g. three sources to read), spawn three researcher subagents at once and merge their results, the fan-out/fan-in move behind the speed of Anthropic's research system.
- Any edge that must fire every time (e.g. tests must run before a handoff) should be a hook, not a polite instruction the model merely usually follows, and the first graph should stay to a few nameable nodes whose every edge you understand, shipping that before deciding whether to outgrow the interactive setup and move to the SDK or a dedicated framework.
- Do not reach for a graph when every node must already be a loop that reliably ships on its own: a graph of weak nodes is "slop produced in parallel," and if one agent with a clear verifier already does the job, wiring three together just costs more tokens for nothing — read "Agent Graph vs Loop" before splitting a job that did not need splitting.
- Nail the single loop first, since which loop to nail first is a business call, not an architecture call: the functions worth converting early are the ones whose output you can check cheaply and honestly, which is why SEO and support functions are typically converted before anything touching revenue.

## The argument in five moves

1. "Graph engineering" trended as if it were a new discipline, but Anthropic's own agent patterns were already graphs under a plainer name.
2. Strip the term to its essentials — nodes, edges, shared state — and it maps directly onto Claude Code's subagents, orchestrator routing, and returned results.
3. Three primitives let you build a graph with increasing commitment: subagent files, hooks for guaranteed edges, and the Claude Agent SDK for code-level graphs — hand-roll before you lift into the SDK.
4. Anthropic's own multi-agent research system proves the pattern works, at a real and disclosed cost: +90.2% quality, ~15x tokens, and an early over-spawning failure mode.
5. Wiring a first graph is a small recipe — a splittable job, narrow subagents, orchestrator loop-backs, fan-out/fan-in, hooks — but only worth doing once each node's underlying loop already ships reliably alone.
