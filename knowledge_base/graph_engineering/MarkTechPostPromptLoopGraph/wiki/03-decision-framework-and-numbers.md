> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Decision Framework and Numbers

**In one sentence:** Choose the simplest layer that can verify "done" mechanically and stay within one context window, because higher layers buy real gains (+90% on an internal eval) only at roughly 15x token cost — and the person's task understanding, not the architecture, is often what differs.

## Key points

- Use an ordered four-question checklist to pick a layer, where the first "no" tells you where to stop climbing: (1) human reviewed every output? (2) can "done" be checked by something other than a human? (3) does the task stay in one agent's context window and a single domain? (4) do genuinely independent parts need to run in parallel?
- If a human reviews every output before it gets acted on, the prompt layer alone is enough — there is no need for a loop.
- If "done" cannot be checked by tests, a schema, a rubric, or a second model, building a loop is premature: it would only stop on a token budget, not on correctness.
- The layers compose rather than replace one another: a loop is essentially a prompt repeated with extra scaffolding around it, and a graph is built out of loops the same way loops are built out of prompts.
- A roughly +90% improvement on an internal research evaluation is cited for a multi-agent/graph-style setup, but at around 15x the token cost of a single chat turn, with token spend alone explaining about 80% of the variance in outcome quality.

## The ordered checklist for picking a layer

The article proposes an ordered checklist, where the first "no" answer tells you where to stop climbing:

1. **Is a human reviewing every output before it gets acted on?** If yes, the prompt layer alone is enough — there is no need for a loop.
2. **Can "done" be checked by something other than a human — tests, a schema, a rubric, or a second model?** If not, there is no real mechanical stop condition, so building a loop is premature (it would only stop on a token budget, not on correctness).
3. **Does the task stay within a single agent's context window and a single domain?** If yes, build a loop rather than a graph — one continuous reasoning trace is the cheapest way to keep assumptions consistent.
4. **Do genuinely independent parts of the task need to execute in parallel?** Only if yes is this actually a graph problem, requiring explicit nodes, edges, shared state, and failure-handling routes. If no, the better move is to extend the loop's tools rather than add more agents.

## Composition: loops are prompts, graphs are built from loops

The layers compose rather than replace one another:

- A **loop** is essentially a prompt repeated with extra scaffolding around it.
- A **graph** is built out of loops the same way loops are built out of prompts.

So higher layers are not a different kind of system — they are lower layers plus structure, which is why they are harder to design well than a single prompt, not easier.

## Closing caution: operator skill, not architecture

The article's closing caution concerns the person building the system, not the architecture itself: two engineers can build an identical loop and get very different outcomes depending on how deeply each one actually understands the underlying task — and the system itself cannot detect or correct for that gap. This is why the higher layers (loop, graph) are harder to design well than a single prompt.

## Headline cost/performance numbers

- A roughly **+90% improvement** on an internal research evaluation is cited for a multi-agent/graph-style setup, but at around **15x the token cost** of a single chat turn.
- **Token spend alone** is said to explain about **80% of the variance** in outcome quality.
- The overall takeaway: most tasks do not need to climb all the way to the graph layer. The example where it does pay off is writing- or knowledge-heavy work involving many dispersed decisions, which would otherwise produce conflicting assumptions if handled by a single long reasoning trace.

## Sources the article cites

- Anthropic's engineering blog — posts on context engineering, the "building effective agents" piece describing five workflow patterns (December 2024), and a writeup on building their multi-agent research system
- Simon Willison's post on designing agentic loops
- Several independent practitioner write-ups specifically on "loop engineering" and "graph engineering"
- LangChain's guidance on when to build multi-agent systems, plus the LangGraph API documentation
- Two 2026 arXiv papers — one on agentic workflows in building engineering ("Buildrix") and one on coding-agent loop design

**Covers:** Decision checklist for choosing a layer; headline numbers; cited sources (source chunk 03)
