# Task: Extract wiki page 02 — Graphs for Planning

You are writing ONE wiki page for a knowledge-base entry summarizing an academic survey paper: "Graph-Augmented Large Language Model Agents: Current Progress and Future Prospects" (arXiv 2507.21407).

**Context is tight on this model — read ONLY the chunk file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

Read this file (plain text, extracted from the PDF):
`/Users/sergii/.kb/papers/ArxivGraphAugmentedLLMAgents/source/chunks/02.txt`

It covers Section 2.1 "Graphs for Agent Planning": plan-as-a-graph, sub-task pools as graphs / task graphs, reasoning as a graph (e.g. Tree-of-Thought-style), and environment as a graph — with named methods (e.g. AFlow, AgentKit, HuggingGPT and others as they appear in the text).

One figure is available for this page (already extracted as a page-render PNG, do not open it — just reference by filename):
- `fig3-planning-graphs.png` — Figure 3: Graphs for planning in LLM agent systems (covers plan graphs, task-pool graphs, reasoning graphs, environment graphs).

## Output

Write the page to (absolute path):
`/Users/sergii/.kb/papers/ArxivGraphAugmentedLLMAgents/wiki/02-graphs-for-planning.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Graphs for Planning

**In one sentence:** <the chunk's whole argument — how graphs structure the planning module of LLM agents>

## Key points

- <5-8 bullets, each a complete standalone claim with real content. Cover: what a plan graph is and why it's used for task decomposition; the sub-task pool / task graph approach and how it differs from free-form plan graphs; reasoning-as-a-graph approaches; environment-as-a-graph; named methods/systems the paper cites and what each one specifically does differently.>

---

## <hierarchical ## subsections mirroring the chunk's own structure, e.g. "Plan as a graph", "Sub-task pool as a graph", "Reasoning as a graph", "Environment as a graph">

<Full detail: exact claims, named systems (AFlow, AgentKit, etc. — use whatever names actually appear in the chunk text, do not invent names), what problem each one solves and how it uses a graph, and any distinctions the paper draws between approaches (e.g. static vs. dynamic graphs, task-independent vs. task-adaptive).>

![Figure 3: Graphs for planning in LLM agent systems](images/fig3-planning-graphs.png)

**Covers:** Section 2.1 (Graphs for Agent Planning)
```

Embed the image at the point in the text where planning graph types are discussed. Use the relative image path `images/fig3-planning-graphs.png` exactly (the page lives in `wiki/`, images live in `wiki/images/`).

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than closing your own bead.

## Done

Once the file is written: `bd close <own-id> --reason "chunk 02 extracted"`.
