# Task: Extract wiki page 03 — Graphs for Memory and Tools

You are writing ONE wiki page for a knowledge-base entry summarizing an academic survey paper: "Graph-Augmented Large Language Model Agents: Current Progress and Future Prospects" (arXiv 2507.21407).

**Context is tight on this model — read ONLY the chunk file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

Read this file (plain text, extracted from the PDF):
`/Users/sergii/.kb/papers/ArxivGraphAugmentedLLMAgents/source/chunks/03.txt`

It covers two sections: 2.2 "Graphs for Agent Memory Management" (graph-organized interaction memory, knowledge-graph-backed memory, retrieval over structured memory) and 2.3 "Graphs for Tool Management" (tool graphs for tool selection/combination, e.g. parameter-level tool graphs, fine-tuning with tool-interaction data).

Two figures are available for this page (already extracted as page-render PNGs, do not open them — just reference by filename):
- `fig4-memory-graphs.png` — Figure 4: Graphs for memory management in LLM agent systems.
- `fig5-tool-graphs.png` — Figure 5: Graphs for tool management in LLM agent systems.

## Output

Write the page to (absolute path):
`/Users/sergii/.kb/papers/ArxivGraphAugmentedLLMAgents/wiki/03-graphs-for-memory-and-tools.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Graphs for Memory and Tools

**In one sentence:** <the chunk's whole argument — how graphs organize agent memory and tool management>

## Key points

- <5-8 bullets, each a complete standalone claim with real content. Cover both sub-topics: memory (why flat/sequential memory is limited, what a graph-organized memory buys — reduced hallucination, richer context retrieval, etc.) and tools (why tool graphs help tool selection/combination, and how they're used to build fine-tuning data). Cite named methods/systems as they appear in the chunk.>

---

## Graphs for Agent Memory Management

<Full detail on section 2.2: exact claims, named systems, mechanisms (e.g. graph-organized interaction memory, knowledge-graph retrieval), and results/benefits described.>

![Figure 4: Graphs for memory management](images/fig4-memory-graphs.png)

## Graphs for Tool Management

<Full detail on section 2.3: exact claims, named systems (e.g. ToolFlow or others as they appear), the parameter-level tool graph idea, and how sampled tool subsets are used for fine-tuning.>

![Figure 5: Graphs for tool management](images/fig5-tool-graphs.png)

**Covers:** Section 2.2 (Graphs for Agent Memory Management), Section 2.3 (Graphs for Tool Management)
```

Embed each image under its matching subsection. Use the relative image paths `images/fig4-memory-graphs.png` and `images/fig5-tool-graphs.png` exactly (the page lives in `wiki/`, images live in `wiki/images/`).

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than closing your own bead.

## Done

Once the file is written: `bd close <own-id> --reason "chunk 03 extracted"`.
