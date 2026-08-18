# Task: Extract wiki page 01 — Introduction and Agent Framework

You are writing ONE wiki page for a knowledge-base entry summarizing an academic survey paper: "Graph-Augmented Large Language Model Agents: Current Progress and Future Prospects" (arXiv 2507.21407).

**Context is tight on this model — read ONLY the chunk file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

Read this file (plain text, extracted from the PDF):
`/Users/sergii/.kb/papers/ArxivGraphAugmentedLLMAgents/source/chunks/01.txt`

It covers: the Abstract, Section 1 (Introduction) — motivation for graph-augmented LLM agents (GLA) — and the opening of Section 2 (the LLM agent system framework: planning, memory, and tool-use modules).

Two figures are available for this page (already extracted as page-render PNGs, do not open them — just reference by filename):
- `fig1-agent-framework.png` — Figure 1: LLM agent framework and multi-agent system overview.
- `fig2-graph-types.png` — Figure 2: the different graph types used across LLM agent systems (tool graphs, task/workflow graphs, knowledge graphs, agent coordination graphs).

## Output

Write the page to (absolute path):
`/Users/sergii/.kb/papers/ArxivGraphAugmentedLLMAgents/wiki/01-introduction-and-agent-framework.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Agent Framework

**In one sentence:** <the chunk's whole argument in one sentence — why graphs are needed to augment LLM agents and what the three core agent modules are>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (not "discusses X"). Cover: what limits plain LLM agents; why graphs help (reliability, efficiency, interpretability — use the paper's own numbered benefits if present); the three core LLM agent system modules (planning, memory, tool-use) and where graphs fit into each; the four graph types used (tool graphs, task/workflow graphs, knowledge graphs, agent coordination graphs).>

---

## <hierarchical ## subsections mirroring the chunk's own structure — e.g. "Why LLMs need graphs", "The LLM agent system framework", "Types of graphs used in agent systems">

<Full detail: exact claims, the paper's own numbered points (❶❷❸ etc rendered as 1/2/3), named systems/methods mentioned, and terminology as used in the source. Do not invent facts not in the chunk.>

![Figure 1: LLM agent framework and multi-agent system](images/fig1-agent-framework.png)

![Figure 2: Different graph types in LLM agent systems](images/fig2-graph-types.png)

**Covers:** Abstract, Section 1 (Introduction), Section 2 opening (agent framework: planning/memory/tool modules)
```

Embed both images at the point in the text where they are naturally discussed (Figure 1 near the framework discussion, Figure 2 near the graph-types discussion). Use relative image paths `images/<file>.png` exactly as shown (the page lives in `wiki/`, images live in `wiki/images/`).

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than closing your own bead.

## Done

Once the file is written: `bd close <own-id> --reason "chunk 01 extracted"`.
