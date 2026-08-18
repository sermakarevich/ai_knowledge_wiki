---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Graph Engineering with Claude Code

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. In the article's mapping, what does each of Claude Code's subagents, the orchestrator's routing, and a subagent's returned result correspond to in graph terms?

> [!tip]- Answer
> Subagents map to nodes (each a separate agent instance with its own context window, system prompt, and scoped tools), the main agent's runtime routing decisions map to edges, and a subagent's returned result flowing back to the orchestrator maps to shared state. See [[wiki/01-claude-code-as-a-graph-engine|Claude Code as a Graph Engine]].

### Q2. What two numbers does the article cite from Anthropic's multi-agent research system, and what do they each represent?

> [!tip]- Answer
> 90.2% is the improvement Anthropic's multi-agent (orchestrator-workers) system reported over a single-agent Claude Opus 4 baseline on an internal research eval. ~15x is the token cost of that multi-agent run relative to a normal chat turn — the disclosed price of the quality gain. See [[wiki/01-claude-code-as-a-graph-engine|Claude Code as a Graph Engine]].

### Q3. Why does the article recommend hand-rolling a graph interactively in Claude Code before reaching for the Claude Agent SDK?

> [!tip]- Answer
> A graph you hand-rolled and watched run is a graph you actually understand; reaching for the SDK first means you may end up debugging orchestration logic you never really designed. Hand-rolling first lets the shape stabilize before it gets lifted into code. See [[wiki/01-claude-code-as-a-graph-engine|Claude Code as a Graph Engine]].

### Q4. What failure mode did early versions of Anthropic's orchestrator exhibit, and what does it illustrate about edges in a graph?

> [!tip]- Answer
> Early orchestrator versions over-spawned subagents even for simple questions that did not need a team. It illustrates that edges (routing decisions) carry a real cost — dynamic, model-chosen routing can misjudge how much parallel work a task actually needs, adding token and coordination overhead without added quality. See [[wiki/01-claude-code-as-a-graph-engine|Claude Code as a Graph Engine]].

### Q5. What makes a job a good candidate for a "first graph," according to the wiring recipe?

> [!tip]- Answer
> A job that genuinely splits into an independent produce step and check step — e.g. draft-then-review, research-then-write, or build-then-test — where each step can be given its own narrowly-scoped subagent. See [[wiki/02-wiring-your-first-graph|Wiring Your First Graph]].

### Q6. Why should a loop-back edge (e.g. a reviewer rejecting a draft and sending it back to the writer) be treated as "a real edge" rather than an afterthought?

> [!tip]- Answer
> It is a node with a conditional return — the orchestrator's routing decision to re-invoke the writer is exactly the same kind of runtime edge as the initial researcher→writer→reviewer handoff, just conditioned on the reviewer's verdict. Treating it as a first-class edge (rather than an ad hoc retry) is what keeps the graph's behavior something the builder actually understands. See [[wiki/02-wiring-your-first-graph|Wiring Your First Graph]].

### Q7. A team wants to automate "scrape competitor pricing pages, summarize changes, and flag anything above a 10% price move" using three separate roles. Using the article's guidance, which edge in this pipeline should be a hook rather than left to the orchestrator's judgment, and why?

> [!tip]- Answer
> The "flag anything above 10% move" check should be a hook (or at least the trigger for it), because it is a rule that must fire every time a price move crosses the threshold — not something that should depend on whether the model happens to notice or prioritize it. Hooks give guaranteed transitions for edges that cannot be left to "the agent usually catches it." See [[wiki/02-wiring-your-first-graph|Wiring Your First Graph]].

### Q8. The article borrows its central evidence (90.2% / 15x) from a different Anthropic post about its research system rather than reporting original data about Claude Code graphs specifically. What is the weakest link in this article's own evidence base, and how much should that limit how you weigh its recommendations?

> [!tip]- Answer
> The weakest link is that the headline numbers describe a different system (Anthropic's internal multi-agent research tool) under different conditions, not a controlled comparison of graphs built with `.claude/agents/` subagents specifically — so the 90.2%/15x figures support "graphs can beat single agents when work is separable" only as an existing-proof analogy, not as data about Claude Code subagent graphs themselves. The wiring recipe and primitive descriptions are still useful practical guidance, but the quantitative case for reaching for a graph should be treated as borrowed, not measured for this specific tool. See [[critical_thinking|Critical Analysis]].
