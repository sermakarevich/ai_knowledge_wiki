# Source

- **Title:** Prompt Engineering vs Loop Engineering vs Graph Engineering: What Changes at Each Layer
- **Author:** Asif Razzaq
- **Publication:** MarkTechPost
- **Date:** 2026-07-29
- **URL:** https://www.marktechpost.com/2026/07/29/prompt-engineering-vs-loop-engineering-vs-graph-engineering/
- **Retrieved:** 2026-08-18

Note: these are original summary notes distilling the article's claims and definitions for
personal knowledge-base use — not a reproduction of the article's text or structure.

## Gist

The piece argues that "prompt engineering," "loop engineering," and "graph engineering" get
used as if they compete, when they're really three nested levels of control that stack: a
prompt shapes one model call, a loop shapes one agent's repeated cycle of that call, and a
graph shapes how several such loops/agents are wired together. Lower layers keep operating
inside higher ones — building a loop around a prompt doesn't retire the prompt, it just moves
who writes it.

## Why layers get added

A single supervised prompt-response cycle works as long as a human reads and judges every
output. It stops being enough once volume rises, tasks span multiple steps, no one is around
to grade results, or one step's output must feed straight into the next without review. The
article's point: the prompt didn't get worse — the deployment conditions moved past what
manual review can keep up with. Anthropic's own writeups are cited noting that even in
multi-agent systems, sloppy prompting (not architecture) was often the actual root cause of
coordination failures (e.g., a bug that had one query needlessly spawn 50 subagents).

## The loop layer

A loop automates the observe-act-verify-repeat cycle so a coding/task agent can run without a
human approving every step. The article inventories commonly cited building blocks for a
production loop: scheduled/triggered automations, isolated worktrees per parallel agent,
reusable written-down skills instead of re-explaining conventions each session, tool/data
access via connectors, a separate "checker" pass so the same model doesn't grade its own work,
and externally persisted state/notes since the model itself has no memory across runs. Its
core thesis: the loop mechanism is easy; the hard and failure-prone part is the **stop
condition** — a reliable, mechanical test for "actually done" versus "stuck." Without one, a
run just burns tokens until a budget cap kicks in rather than stopping on correctness.

## The graph layer

Graph engineering generalizes the loop to multiple agents. The article's key structural claim
is that real systems maintain two distinct graphs simultaneously: a slow-changing **org
graph** (which agents exist, what role/ownership each holds, changed only on redeploy) and a
fast-changing, per-task **work graph** (which branches are currently active, where they split
for parallelism, where they merge or get pruned once evidence resolves them). One answers "who
is responsible," the other answers "what is happening right now."

The article is skeptical of the term's novelty — frameworks like LangGraph already modeled
agent systems as an explicit graph (nodes registered onto a `StateGraph`, edges declared with
`add_edge`/`add_conditional_edges`, a defined `START`/`END`), and Anthropic had already
described comparable workflow shapes (chaining, routing, parallel fan-out/fan-in,
orchestrator-worker delegation, evaluator-optimizer loops) years earlier without calling them
"graphs." What's new, in the article's framing, is just a shared vocabulary for choices those
frameworks always forced on designers: what counts as a node, what counts as an edge, and what
data rides along the edges as shared state. It flags one recurring failure mode explicitly:
information silently fails to reach a node because no edge was defined to carry it there.

## Choosing a layer — the article's decision test

Presented as an ordered checklist where the first "no" tells you where to stop climbing:
1. Is a human reviewing every output before it's acted on? → prompt layer is enough.
2. Is "done" checkable by something other than a person (tests, schema, rubric, another
   model)? → if not, there's no real stop condition to build a loop around.
3. Does the task stay within one agent's context and one domain? → build a loop, not a graph.
4. Do independent parts of the task genuinely need to run in parallel? → only then declare a
   graph (nodes/edges/state/failure routes); otherwise, extend the loop's tools instead.

Layers compose rather than replace each other: a loop is described as "a prompt repeated with
scaffolding," and a graph as built from loops the same way loops are built from prompts. The
article's closing caution is about people, not architecture: two engineers can build the same
loop and get very different results depending on how deeply each actually understands the
underlying task — the system can't detect or correct for that gap, which is why the higher
layers are argued to be harder to get right, not easier.

## Headline numbers and claims cited

- A roughly +90% gain on an internal research evaluation was reported for a
  multi-agent/graph-style setup, but at about 15x the token cost of a single chat turn, with
  token spend alone said to account for ~80% of the outcome variance.
- The article's takeaway is that most tasks don't need to climb to the graph layer at all;
  the case it gives where it pays off is writing/knowledge-work with many dispersed decisions
  that would otherwise produce conflicting assumptions across a single long reasoning trace.

## Sources the article draws on

Anthropic engineering blog posts on context engineering, "building effective agents" (the
Dec-2024 five-workflow-patterns piece), and the multi-agent research system writeup; Simon
Willison's "designing agentic loops"; independent write-ups on "loop engineering" and "graph
engineering" from several practitioner blogs; LangChain's guidance on when to build
multi-agent systems plus the LangGraph API docs; and two 2026 arXiv papers, one on agentic
building-engineering workflows ("Buildrix") and one on coding-agent loop design.

## Author

Asif Razzaq, CEO of Marktechpost Media Inc.
