# Graph Engineering with Claude Code: Anthropic's Agent Graph

**Source:** AI Builder Club
**URL:** https://www.aibuilderclub.com/blog/graph-engineering-with-claude-code
**Author:** Shirley
**Published:** July 24, 2026 (Updated August 3, 2026)
**Retrieved:** 2026-08-18

---

Graph engineering means wiring specialized agents into a graph of nodes, edges, and shared state. The surprise for most builders is that you do not need a Python orchestration framework to do it - Claude Code already ships the primitives. Subagents are the nodes. The main agent that delegates to them is the orchestrator node, and its routing between them is the edges. The Claude Agent SDK is how you lift the whole thing into code when the interactive version stops being enough. If you have been reading the graph engineering posts and wondering what to actually build with, this is the shortest path: you probably have the tool open already.

When "graph engineering" trended in mid-July 2026, the framing made it sound like a new discipline you had to go adopt. But Anthropic had already shipped the pattern under a plainer name. Their guide on building effective agents lays out five composable patterns - prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer. Read those as graphs and they snap into focus: prompt chaining is a line of nodes, routing is a conditional edge, orchestrator-workers is a hub node fanning out to worker nodes and fanning their results back in. Graph engineering is the label. This is the mechanism.

## What "graph engineering with Claude" actually means

Strip the term down and a graph is three things: nodes (an agent or a step that does one job), edges (the routing that decides which node runs next, including branches, fan-out, fan-in, and loops back), and shared state (the data that flows along the edges). A single agent loop is the smallest possible graph - one node with an edge back to itself. Graph engineering is what you do when one node is no longer enough and you need several specialized ones wired together.

Doing that "with Claude" does not mean learning a new API first. It means mapping those three parts onto tools Claude Code already exposes:

- **Nodes → subagents.** Each subagent is a separate agent instance with its own context window, its own system prompt, and scoped tool access. That isolation is exactly what makes a good node: a researcher subagent that only reads and searches, a writer that only drafts, a reviewer that only critiques, none of them stepping on each other's context.
- **Edges → the orchestrator's routing.** Your main Claude session is itself a node, and its decisions about which subagent to spawn, when, and with what brief are the edges. Because the orchestrator routes at runtime rather than following a hardcoded diagram, you get dynamic edges without drawing one by hand.
- **Shared state → the returned results.** A subagent's final output flows back to the orchestrator, which passes the relevant piece to the next node. That handoff is the state moving along the edge.

## The primitives Claude Code already gives you

You wire a graph in Claude Code with three things, in rough order of how far you are willing to go:

1. **Subagents in `.claude/agents/`.** Drop a markdown file with YAML frontmatter per node - a name, a description, the tools it may use, and its system prompt. The main agent reads these and delegates to them. This is the fastest way to stand up a multi-node graph, and it is version-controlled by default because it is just files in your repo.
2. **Hooks as deterministic edges.** When you need an edge that fires every time rather than one the model chooses, Claude Code hooks (run on events like a tool call finishing or a session stopping) give you a guaranteed transition. That is the difference between "the agent usually runs the tests" and "the tests always run before the writer node hands off."
3. **The Claude Agent SDK.** When the graph needs to run unattended, be tested like code, or fan out to subagents programmatically, you define the same nodes through the SDK's `agents` parameter in Python or TypeScript. Same node-edge-state shape, now embeddable in a larger system.

Hand-roll the graph interactively first, then lift the stable shape into the SDK. The order matters. A graph you hand-rolled and watched run is a graph you understand. Reaching for the SDK before you have seen the shape work is how you end up debugging orchestration you never really designed.

## Anthropic already ships graph engineering (they call it orchestrator-workers)

The clearest proof that this is not a rebrand you have to wait on is Anthropic's own multi-agent research system. It is an orchestrator-worker graph: a lead agent plans the work, spins up specialized subagents that run in parallel, and a separate pass adds citations. The subagents are nodes, the lead agent is the orchestrator node whose delegation forms the edges, and the plan plus each subagent's findings are the shared state.

Anthropic reported that this multi-agent setup beat a single-agent Claude Opus 4 baseline by 90.2% on an internal research eval. The same post is honest about the cost, which is the part most graph-engineering hype skips. That multi-agent graph burned roughly 15x the tokens of a normal chat turn, and early versions of the orchestrator would over-spawn - firing off far more subagents than a simple question needed. That is the real tradeoff of graph engineering: you are buying quality and parallelism with tokens and coordination overhead. A graph earns its keep when the job genuinely has separable parts. When it does not, you have built a more expensive way to run one loop.

## How to wire your first agent graph in Claude Code

Pick a job that actually splits. A good first candidate is anything with a produce step and an independent check step - draft-then-review, research-then-write, build-then-test. Then:

1. **Write one subagent per node.** Give each a narrow system prompt and only the tools it needs. The reviewer should not have write access; the writer should not be searching the web. Narrow nodes are what make the graph better than one big prompt.
2. **Let the orchestrator route.** Ask the main agent to run the researcher, hand its findings to the writer, then hand the draft to the reviewer, and loop the writer if the reviewer rejects. That loop-back is a real edge - a node with a conditional return.
3. **Fan out when the work is parallel.** If three sources need reading, spawn three researcher subagents at once and let the orchestrator merge their results. That is fan-out and fan-in, the move that gave Anthropic's research system its speed.
4. **Add a hook for the edge you cannot trust to the model.** If tests must run before a handoff, make it a hook, not a polite instruction.

Keep it to a few nodes you can name and whose every edge you understand. Ship that, watch it run, and only then decide whether you have outgrown the interactive setup and need the SDK or a dedicated framework.

## When not to reach for a graph

Every node in your graph has to be a loop that reliably ships on its own. A graph of weak nodes is just slop produced in parallel. If one agent with a clear verifier already does the job, wiring three of them together will cost more tokens and buy you nothing. The honest test lives in "agent graph vs loop: when to use which" - read it before you split a job that did not need splitting.

Nail the single loop first. The nodes you wire together later are only worth wiring if each one already works. Which loop to nail first is a separate call, and it is about your business rather than your architecture. The functions worth converting early are the ones where you can check the output cheaply and honestly, which is why SEO and support usually go before anything touching revenue. That ordering is in "how to become an AI-native company."

## Related Content

- **Graph Engineering: The 2026 Guide** - The pillar: what nodes, edges, and shared state actually mean, the frameworks, and when a graph beats a loop.
- **Agent Graph vs Loop: When to Use Which** - The decision that comes before you spawn a single subagent. Don't wire a graph you don't need.
- **Is Graph Engineering Just LangGraph?** - How Claude Code's subagents compare to LangGraph, AutoGen GraphFlow, and Google ADK.
- **Loop Engineering Guide** - The layer below graph engineering: designing the loop each node has to be, and writing the verifier that decides "done."

## Frequently Asked Questions

**Can you do graph engineering with Claude?**
Yes, and you do not need a separate framework to start. Graph engineering means wiring specialized agents into a graph of nodes (each an agent or step), edges (the routing between them, including branches, fan-out, fan-in, and loops), and shared state that flows along those edges. Claude Code already gives you the pieces: subagents are the nodes, the main agent that delegates to them is the orchestrator node whose routing draws the edges, and the Claude Agent SDK lets you define the whole graph in code when you outgrow the interactive setup.

**What are Claude Code subagents?**
Subagents are separate agent instances your main Claude session can spawn to handle a focused subtask. Each runs in its own context window with its own system prompt and scoped tool access, so a subagent's work does not pollute the main thread. You define them as markdown files with YAML frontmatter in `.claude/agents/`, or programmatically through the Claude Agent SDK's `agents` parameter. In graph terms, each subagent is a node.

**Is Claude Code a graph framework like LangGraph?**
Not exactly. LangGraph makes you declare state, nodes, and edges explicitly and gives you a runtime with checkpointing. Claude Code lets the orchestrating agent decide at runtime which subagents to call and in what order, which is closer to Anthropic's "agent" end of the spectrum than a fixed workflow graph. You get the node-edge-state shape without hand-drawing the graph, and you reach for a framework only when you need durable checkpointing, resumability, or cross-vendor handoffs the SDK does not cover.

**Do you need the Claude Agent SDK to build an agent graph?**
No. For an interactive graph, defining a handful of subagents in `.claude/agents/` and letting the main agent route to them is enough. The Claude Agent SDK earns its place when you want the graph to run unattended, to be version-controlled and tested like code, to fan out to subagents programmatically, or to be embedded in a larger application. Hand-roll the graph in Claude Code first, then lift it into the SDK once the shape is stable.

**How is graph engineering with Claude different from just prompting harder?**
A single prompt, however good, is one node doing everything in one context window. Graph engineering splits the job across specialized nodes so each has a clean context and a narrow brief - a researcher, a writer, a reviewer - and passes state between them. Anthropic's own multi-agent research system reported a large quality jump from exactly this move, at a real token cost, which is the tradeoff you are choosing to make.

## Sources & Verification

This guide explains an emerging term against tools that already exist. 'Graph engineering' surfaced on X in mid-July 2026; the Claude Code and Claude Agent SDK capabilities described here are drawn from Anthropic's official docs and engineering posts (Building Effective Agents, the multi-agent research system, and the subagents documentation), all verified July 2026.

- **Building Effective Agents (Anthropic)** - Anthropic's five composable patterns - prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer - and the workflows-versus-agents distinction. Orchestrator-workers is a graph in all but name.
- **How we built our multi-agent research system (Anthropic)** - A lead agent plans, spins up subagents that run in parallel, and a separate pass adds citations. Reported 90.2% improvement over a single-agent Claude Opus 4 baseline on an internal research eval, at roughly 15x the tokens of a chat turn.
- **Subagents - Claude Code documentation** - Subagents run in their own context window with a custom system prompt and scoped tool access, defined as markdown files in `.claude/agents/` or programmatically via the Claude Agent SDK's `agents` parameter.
- **Graph Engineering Guide (AI Builder Club)** - The pillar: what nodes, edges, and shared state mean, the frameworks, and when a graph actually beats a loop.
- **Loop Engineering Guide (AI Builder Club)** - The layer directly below graph engineering; a single agent loop is one node with an edge back to itself, and each node in a graph has to be a loop that reliably ships.
