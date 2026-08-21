# Task: Write wiki page 01 — Problem, Motivation & Preliminaries

You are extracting ONE section of a paper into ONE wiki page. Context is tight on this model — **read ONLY the files listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

## Input

Read this file in full:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/source/chunks/01.txt`

This chunk covers the Abstract, Section 1 (Introduction), and Section 2 (Preliminaries) of the paper "GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs" (Feng et al., ICLR 2026).

Also read this figure description (a vision-model transcription of Figure 1, which appears in this chunk's section):
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/images/fig1-router-comparison-description.md`

The actual image file already exists at `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/images/fig1-router-comparison.png` — you do not need to view it, just embed it at the right point using the markdown syntax below.

## Output

Write the wiki page to:
- `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/01-problem-and-preliminaries.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Problem, Motivation & Preliminaries

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content — numbers, mechanisms, definitions — not "discusses X">

---

## <subsection mirroring the source's structure, e.g. "Why LLM Routing Needs an Agentic View">

<hierarchical detail, tables/numbers/definitions preserved exactly as in the source>

## <next subsection, e.g. "Limitations of Single-Round and Multi-Round Routers">

...

## <subsection covering Section 2 Preliminaries, e.g. "Formalizing Routing as an MDP">

<formal definitions, notation, the MDP formulation as given in the source>

![Comparison between agentic, single-round, and multi-round routers](images/fig1-router-comparison.png)

<a sentence or two describing what the figure shows, informed by the figure description file>

**Covers:** Abstract, Section 1 (Introduction), Section 2 (Preliminaries)
```

Requirements:
- Cover the WHOLE chunk, including its final subsection — do not stop after the opening paragraphs.
- Preserve exact numbers, definitions, and notation from the source text.
- Embed the figure using the exact path shown above, near the text that discusses it (the router comparison figure belongs with the "why agentic routing" discussion in Section 1).
- No meta-commentary about your own extraction process in the output file.

## Scope & completion

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

When done: `bd close <own-id> --reason "chunk 01 extracted"`
