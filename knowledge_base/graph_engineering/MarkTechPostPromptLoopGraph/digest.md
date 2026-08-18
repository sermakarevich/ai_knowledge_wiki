> [[index|Wiki]] | [[summary|Summary]]

# Prompt Engineering vs Loop Engineering vs Graph Engineering — Digest

The whole source at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-prompt-and-loop-layers|Prompt and Loop Layers]]

**In one sentence:** Prompt, loop, and graph engineering are not competing techniques but three nested levels of control, and the loop layer — which automates the agent's observe-act-verify cycle — fails not because of its machinery but because of the stop condition that separates "genuinely finished" from "stuck."

- "Prompt engineering," "loop engineering," and "graph engineering" are three nested levels of control that stack: a prompt shapes one model call, a loop shapes one agent's repeated cycle built around that call, and a graph wires several such loops/agents together.
- Adding a layer does not retire the lower one: building a loop around a prompt leaves the prompt operating inside each cycle — it only changes who (or what) writes it on each pass.
- A supervised prompt-response cycle works while a human reads and judges every output; it breaks down once volume rises, tasks span multiple steps, no grader is available, or one step's output must feed the next without review — the prompt did not get worse, the deployment conditions outgrew manual review.
- Even inside multi-agent systems, sloppy prompting (not the agent topology) is often the root cause of coordination failures; the article cites Anthropic material on a bug where one simple query needlessly spawned 50 subagents, fixed by better prompting rather than architectural redesign.
- A production loop is built from: scheduled or event-triggered unsupervised automations, isolated worktrees so parallel agents don't collide on the same files, reusable written-down skills/conventions, connector-based access to external tools and data (issue trackers, databases, staging APIs), a separate checker pass so the producing model is not the sole grader (models grade their own work too generously), and externally persisted state (a markdown file or board) because the model retains no memory across runs.
- The loop layer's central thesis is that the repeat-and-check mechanism is easy to build, while the stop condition — a reliable, mechanical test distinguishing "genuinely finished" from "stuck" — is hard and where loops actually fail; without it, an unattended run fails silently by consuming tokens until an arbitrary budget cap ends it, rather than stopping because the work is correct or complete.

## 2. [[wiki/02-graph-layer|The Graph Layer]]

**In one sentence:** Graph engineering generalizes the loop to multiple agents, and its real content is twofold: production systems simultaneously maintain a slow-changing "org graph" (who is responsible) and a fast-changing "work graph" (what is happening right now), while the concept itself is largely a renaming of pre-existing graph frameworks whose lasting contribution is a shared vocabulary for nodes, edges, and edge state.

- Graph engineering generalizes the loop idea to multiple agents operating as a system.
- Real production systems maintain two distinct graphs at the same time: an "org graph" that is slow-changing — which agents exist, their roles and ownership, updated only on redeploy — answering "who is responsible"; and a "work graph" that is fast-changing and scoped to one task — which branches are active, where work splits for parallelism, where branches merge or get pruned once evidence resolves them — answering "what is happening right now."
- The article is skeptical that "graph engineering" is conceptually new, since frameworks like LangGraph long before the term modeled agent systems as explicit graphs: nodes registered on a state graph, declared edges (including conditional ones), and a start/end point defined before compilation and execution.
- General multi-agent workflow shapes — chaining steps, routing, parallel branches, orchestrator-to-worker delegation, and evaluator-feeding-back-to-optimizer loops — were documented years earlier without being called "graphs."
- What the article credits to the new label is a shared vocabulary for decisions those frameworks always forced on designers: what counts as a node, what counts as an edge, and what information may travel along an edge as shared state.
- The article explicitly names a recurring failure mode: information can silently fail to reach a node because no edge was defined to carry it there — a design gap, not a runtime bug, since nothing crashes and the data simply never arrives.

## 3. [[wiki/03-decision-framework-and-numbers|Decision Framework and Numbers]]

**In one sentence:** Choose the simplest layer that can verify "done" mechanically and stay within one context window, because higher layers buy real gains (+90% eval gain) only at roughly 15x token cost — and the person's task understanding, not the architecture, is often what differs.

- Use an ordered four-question checklist to pick a layer, where the first "no" tells you where to stop climbing: (1) human reviewed every output? (2) can "done" be checked by something other than a human? (3) does the task stay in one agent's context window and a single domain? (4) do genuinely independent parts need to run in parallel?
- If a human reviews every output before it gets acted on, the prompt layer alone is enough — there is no need for a loop.
- If "done" cannot be checked by tests, a schema, a rubric, or a second model, building a loop is premature: it would only stop on a token budget, not on correctness.
- The layers compose rather than replace one another: a loop is essentially a prompt repeated with extra scaffolding around it, and a graph is built out of loops the same way loops are built out of prompts.
- A roughly +90% improvement on an internal research evaluation is cited for a multi-agent/graph-style setup, but at around 15x the token cost of a single chat turn, with token spend alone explaining about 80% of the variance in outcome quality.

## The argument in five moves

1. Prompt, loop, and graph engineering are nested levels of control, not rival techniques — each wraps the one below without retiring it.
2. Layers get added when manual review stops scaling, not because the underlying prompt or model got worse.
3. The loop layer's hard problem is the stop condition — a mechanical "done vs. stuck" test — not the repeat-and-check machinery itself.
4. The graph layer generalizes loops to multiple agents via two coexisting graphs (org and work), and is mostly a naming event over pre-existing frameworks like LangGraph.
5. An ordered four-question checklist (review? mechanical done-check? single context? real parallelism?) tells you the minimum sufficient layer.
6. Layers compose — a graph is built from loops the way loops are built from prompts — so higher layers are harder to design well, not easier.
7. The payoff is real but expensive: +90% eval gain at ~15x token cost, with token spend explaining ~80% of the variance, so most tasks should not climb to the graph layer at all.
