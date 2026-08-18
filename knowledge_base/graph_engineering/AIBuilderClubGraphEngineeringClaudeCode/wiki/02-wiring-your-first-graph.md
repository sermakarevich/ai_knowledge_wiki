> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Wiring Your First Graph

**In one sentence:** The first agent graph in Claude Code is a few narrowly-scoped subagents (one per node) with an orchestrator that routes and loops between them, fan-out for parallel work and hooks for non-negotiable edges — but only after each node is already a loop that reliably ships on its own.

## Key points

- A good first graph is a job that genuinely splits into a produce step and an independent check step — draft-then-review, research-then-write, build-then-test — wired as one subagent per node, each with a narrow system prompt and only the tools it needs (the reviewer gets no write access, the writer no web search), because narrow nodes are what make the graph better than one big prompt.
- The orchestrator (main agent) routes between nodes — researcher → writer → reviewer — and the loop-back that sends a rejected draft back to the writer is a real edge, a node with a conditional return; when the work is genuinely parallel (e.g. three sources to read), spawn three researcher subagents at once and merge their results, the fan-out/fan-in move behind the speed of Anthropic's research system.
- Any edge that must fire every time (e.g. tests must run before a handoff) should be a hook, not a polite instruction the model merely usually follows, and the first graph should stay to a few nameable nodes whose every edge you understand, shipping that before deciding whether to outgrow the interactive setup and move to the SDK or a dedicated framework.
- Do not reach for a graph when every node must already be a loop that reliably ships on its own: a graph of weak nodes is "slop produced in parallel," and if one agent with a clear verifier already does the job, wiring three together just costs more tokens for nothing — read "Agent Graph vs Loop" before splitting a job that did not need splitting.
- Nail the single loop first, since which loop to nail first is a business call, not an architecture call: the functions worth converting early are the ones whose output you can check cheaply and honestly, which is why SEO and support functions are typically converted before anything touching revenue.

## How to wire your first agent graph in Claude Code

**Pick a job that actually splits.** A good first candidate is anything with a produce step and an independent check step — draft-then-review, research-then-write, build-then-test.

**Write one subagent per node.** Give each a narrow system prompt and only the tools it needs. The reviewer should not have write access; the writer should not be searching the web. Narrow nodes are what make the graph better than one big prompt.

**Let the orchestrator route.** Ask the main agent to run the researcher, hand its findings to the writer, then hand the draft to the reviewer, and loop the writer if the reviewer rejects. That loop-back is a real edge — a node with a conditional return.

**Fan out when the work is parallel.** If three sources need reading, spawn three researcher subagents at once and let the orchestrator merge their results. That is fan-out and fan-in, the move that gave Anthropic's research system its speed.

**Add a hook for the edge you cannot trust to the model.** If tests must run before a handoff, make it a hook, not a polite instruction.

Keep it to a few nodes you can name and whose every edge you understand. Ship that, watch it run, and only then decide whether you have outgrown the interactive setup and need the SDK or a dedicated framework.

## When not to reach for a graph

- Every node in your graph has to be a loop that reliably ships on its own. A graph of weak nodes is just slop produced in parallel.
- If one agent with a clear verifier already does the job, wiring three of them together will cost more tokens and buy you nothing.
- The honest test lives in *Agent Graph vs Loop: When to Use Which* — read it before you split a job that did not need splitting.
- **Nail the single loop first.** The nodes you wire together later are only worth wiring if each one already works.
- Which loop to nail first is a separate call, and it is about your business rather than your architecture. The functions worth converting early are the ones where you can check the output cheaply and honestly, which is why SEO and support usually go before anything touching revenue. That ordering is in *How to Become an AI-Native Company*.

## Related Content

- **Graph Engineering: The 2026 Guide** — The pillar: what nodes, edges, and shared state actually mean, the frameworks, and when a graph beats a loop.
- **Agent Graph vs Loop: When to Use Which** — The decision that comes before you spawn a single subagent; don't wire a graph you don't need.
- **Is Graph Engineering Just LangGraph?** — How Claude Code's subagents compare to LangGraph, AutoGen GraphFlow, and Google ADK.
- **Loop Engineering Guide** — The layer below graph engineering: designing the loop each node has to be, and writing the verifier that decides "done."

**Start here:** Graph engineering with Claude Code is the layer above loop engineering, so the honest move is to master the loop before you wire the graph. Each subagent node is only as good as the loop running inside it — discover, plan, execute, verify — and a graph of shaky loops just multiplies the shakiness. The Loop Engineering course takes you from "you are the for loop" to an agent that wakes on its own, pulls the top task off your backlog, ships a PR behind quality gates, and reports back — the exact building block each node in your Claude Code graph has to be. Get that solid and the subagents you wire together are each worth wiring.

## Frequently Asked Questions

**Can you do graph engineering with Claude?**
Yes, and you do not need a separate framework to start. Graph engineering means wiring specialized agents into a graph of nodes (each an agent or step), edges (the routing between them, including branches, fan-out, fan-in, and loops), and shared state that flows along those edges. Claude Code already gives you the pieces: subagents are the nodes, the main agent that delegates to them is the orchestrator node whose routing draws the edges, and the Claude Agent SDK lets you define the whole graph in code when you outgrow the interactive setup.

**What are Claude Code subagents?**
Subagents are separate agent instances your main Claude session can spawn to handle a focused subtask. Each runs in its own context window with its own system prompt and scoped tool access, so a subagent's work does not pollute the main thread. You define them as markdown files with YAML frontmatter in `.claude/agents/`, or programmatically through the Claude Agent SDK's agents parameter. In graph terms, each subagent is a node.

**Is Claude Code a graph framework like LangGraph?**
Not exactly. LangGraph makes you declare state, nodes, and edges explicitly and gives you a runtime with checkpointing. Claude Code lets the orchestrating agent decide at runtime which subagents to call and in what order, which is closer to Anthropic's "agent" end of the spectrum than a fixed workflow graph. You get the node-edge-state shape without hand-drawing the graph, and you reach for a framework only when you need durable checkpointing, resumability, or cross-vendor handoffs the SDK does not cover.

**Do you need the Claude Agent SDK to build an agent graph?**
No. For an interactive graph, defining a handful of subagents in `.claude/agents/` and letting the main agent route to them is enough. The Claude Agent SDK earns its place when you want the graph to run unattended, to be version-controlled and tested like code, to fan out to subagents programmatically, or to be embedded in a larger application. Hand-roll the graph in Claude Code first, then lift it into the SDK once the shape is stable.

**How is graph engineering with Claude different from just prompting harder?**
A single prompt, however good, is one node doing everything in one context window. Graph engineering splits the job across specialized nodes so each has a clean context and a narrow brief — a researcher, a writer, a reviewer — and passes state between them. Anthropic's own multi-agent research system reported a large quality jump from exactly this move, at a real token cost, which is the tradeoff you are choosing to make.

## Sources & Verification

This guide explains an emerging term against tools that already exist. "Graph engineering" surfaced on X in mid-July 2026; the Claude Code and Claude Agent SDK capabilities described here are drawn from Anthropic's official docs and engineering posts, all verified July 2026 and linked below. Treat product specifics as of that date.

- **Building Effective Agents (Anthropic)** — Anthropic's five composable patterns — prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer — and the workflows-versus-agents distinction. Orchestrator-workers is a graph in all but name.
- **How we built our multi-agent research system (Anthropic)** — A lead agent plans, spins up subagents that run in parallel, and a separate pass adds citations. Reported 90.2% improvement over a single-agent Claude Opus 4 baseline on an internal research eval, at roughly 15x the tokens of a chat turn.
- **Subagents — Claude Code documentation** — Subagents run in their own context window with a custom system prompt and scoped tool access, defined as markdown files in `.claude/agents/` or programmatically via the Claude Agent SDK's agents parameter.
- **Graph Engineering Guide (AI Builder Club)** — The pillar: what nodes, edges, and shared state mean, the frameworks, and when a graph actually beats a loop.
- **Loop Engineering Guide (AI Builder Club)** — The layer directly below graph engineering; a single agent loop is one node with an edge back to itself, and each node in a graph has to be a loop that reliably ships.

**Covers:** Step-by-step first-graph recipe (splittable job, one subagent per node, orchestrator routing, fan-out/fan-in, hooks); when not to reach for a graph; Related Content; full FAQ; Sources & Verification (source chunk 02)
