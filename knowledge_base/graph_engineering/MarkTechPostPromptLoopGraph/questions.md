---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Prompt Engineering vs Loop Engineering vs Graph Engineering

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. In the article's framing, what are the three layers and what unit of work does each one shape?

> [!tip]- Answer
> Prompt shapes one model call, loop shapes one agent's repeated cycle built around that call, and graph shapes how several such loops/agents are wired together. See [[wiki/01-prompt-and-loop-layers|Prompt and Loop Layers]].

### Q2. Why is the "stop condition" described as the hard part of a loop, rather than the repeat-and-check cycle itself?

> [!tip]- Answer
> The repeat-and-check mechanism (try, verify, retry) is easy to build. What's hard is a reliable, mechanical test that can tell "genuinely finished" apart from "stuck" — without it, an unattended run doesn't fail loudly, it just keeps consuming tokens until an arbitrary budget cap ends it, regardless of whether the work is actually correct. See [[wiki/01-prompt-and-loop-layers|Prompt and Loop Layers]].

### Q3. A team's multi-agent system has a bug where one simple query spawns 50 subagents. According to the article's citation of Anthropic material, what kind of fix actually resolved this — and what does that imply about diagnosing multi-agent failures generally?

> [!tip]- Answer
> The fix was better prompting, not an architectural redesign of the agent topology. It implies that when a multi-agent system misbehaves, the root cause is often sloppy prompting at a lower layer rather than a structural flaw in the graph — so diagnosis should check the lower layers before redesigning the higher ones. See [[wiki/01-prompt-and-loop-layers|Prompt and Loop Layers]].

### Q4. What is the difference between an "org graph" and a "work graph," and what question does each one answer?

> [!tip]- Answer
> The org graph is slow-changing, updated only on redeploy, and captures which agents exist and who owns what — it answers "who is responsible." The work graph is fast-changing and scoped to one task, capturing active branches, where work splits for parallelism, and where branches merge or get pruned — it answers "what is happening right now." See [[wiki/02-graph-layer|The Graph Layer]].

### Q5. The article is skeptical that "graph engineering" is a genuinely new idea. What evidence does it cite for that skepticism, and what does it say is actually new?

> [!tip]- Answer
> It cites LangGraph modeling agent systems as explicit graphs (nodes on a state graph, declared conditional edges, a start/end point) well before the term became popular, plus earlier-documented workflow shapes (chaining, routing, parallel branches, orchestrator-worker delegation, evaluator-optimizer loops) that were never called "graphs." What it credits as actually new is a shared vocabulary for what counts as a node, an edge, and what data travels along an edge as shared state. See [[wiki/02-graph-layer|The Graph Layer]].

### Q6. Describe the edge-carries-state failure mode the article names. Why does it call this a "design gap," not a "runtime bug"?

> [!tip]- Answer
> Information can silently fail to reach a node simply because no edge was defined to carry it there. It's a design gap rather than a runtime bug because nothing crashes — the system keeps running, the data just never arrives at the node that needed it. See [[wiki/02-graph-layer|The Graph Layer]].

### Q7. Walk through the four-question checklist in order. If a task has a mechanical way to check "done" but stays entirely within one agent's context window, which layer does the checklist land on, and why not go further?

> [!tip]- Answer
> The checklist: (1) is a human reviewing every output? (2) can "done" be checked without a human? (3) does the task stay within one context/domain? (4) do independent parts need genuine parallelism? Given a mechanical done-check and a single context, the answer lands on the loop layer — question 4 doesn't apply because the task isn't split into independent parallel parts, so a graph would add unnecessary structure; the better move is to extend the loop's tools instead. See [[wiki/03-decision-framework-and-numbers|Decision Framework and Numbers]].

### Q8. The article cites roughly a +90% improvement from a multi-agent/graph setup at about 15x the token cost, with token spend explaining ~80% of outcome variance. Given the critical analysis in this folder, why should these numbers be treated cautiously before being reused elsewhere?

> [!tip]- Answer
> The numbers are borrowed from another source (likely an Anthropic internal evaluation) rather than produced by this article, which does not specify what the eval measured, its task distribution, or whether the article's use of it as a general property of "graph-style setups" is warranted — the figures probably describe one specific evaluation, not graphs in general. See [[critical_thinking|Critical Analysis]].
