# Extract task: Preliminaries & the GraphRAG Framework

## Problem

This is one chunk of a long academic survey paper ("Graph Retrieval-Augmented Generation: A Survey", Peng et al. 2024, arXiv:2408.08921) being converted into an LLM-wiki. Your job is to turn this one chunk of source text into one polished wiki page. You are one of several workers each handling a different chunk in parallel -- you only need to cover YOUR chunk.

**Context is tight on this model -- read ONLY the chunk file listed below (plus the figure descriptions inlined in this spec), nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" -- the format contract below is the only convention you need. If this is a retry, do not try to diagnose the prior failure by reading logs -- just re-read the chunk and write directly.

## Fix

**Input:** Read the chunk text at `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/source/chunks/02.txt` (extracted markdown text from pages of the paper's PDF, covering: Sec 3 Preliminaries; Sec 4 Overview of GraphRAG).

**Output:** Write the wiki page to `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/02-preliminaries-and-framework.md`.

## Wiki page format contract (follow exactly)

- Start with a backlink line: `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`
- Then `# <Topic>` (use the topic given above).
- Then `**In one sentence:** <the whole argument/job of this section, in one sentence>`
- Then `## Key points` — 5-8 bullets, each a COMPLETE claim (not a topic label). Include real numbers, mechanisms, named methods/systems, conclusions -- not "discusses X". Someone reading only these bullets should have the section's substance.
- Then a `---` separator, then the full detail as `##` subsections mirroring the source's own internal structure (hierarchical, not flat prose). Use tables for comparisons where the source has them. Name specific methods/papers/systems cited in the text (e.g. "G-Retriever [55]") since this is a survey -- the named techniques ARE the content.
- If this chunk lists a named Figure (e.g. "Figure 3"), embed it inline next to the passage that discusses it using `![<caption>](images/<filename>)` -- use the exact image filename(s) given below, and write 1-3 sentences paraphrasing the figure description provided below (do not just paste the raw description).
- End with a footer line: `**Covers:** <the source section numbers/titles given above>`.
- Do not include any content outside the source chunk text below. Do not invent numbers or citations not present in the chunk.
- No line limit -- be thorough and cover the ENTIRE chunk, including its final subsections (do not stop after the opening topic).

Topic for this page: **Preliminaries & the GraphRAG Framework**
Section(s) covered: Sec 3 Preliminaries; Sec 4 Overview of GraphRAG

## Figures for this section

Image file: `images/fig2-overview-04.png` (already extracted; embed it at the point in the text that discusses it)

Vision-model description of this image:

**Figure 2 — Technical Summary**

- **What it shows:** A conceptual, left‑to‑right architecture diagram of the GraphRAG question‑answering pipeline (not a data plot). It decomposes the framework into three stages — **G‑Indexing**, **G‑Retrieval**, and **G‑Generation**. The left block (G‑Retrieval) applies *query enhancements* (expansion, decomposition) and *knowledge enhancements* (merging, pruning) around a central retriever, drawing on two indexed sources: open‑source knowledge graphs and self‑constructed graph data. The middle column lists the *retrieval result types* (nodes, triplets, paths, subgraphs, hybrid) and the *graph formats* they can be rendered in (adjacency/edge table, natural language, and code‑like forms such as syntax trees, node sequences, graph embeddings). The right block (G‑Generation) shows three enhancement slots — pre‑, mid‑, and post‑generation — each paired with a generator, ending in a natural‑language output response. A worked example query/answer brackets the top and right edges.

- **Axes / trends:** None numerically. There are no axes, scales, or plotted series; the only "direction" is the unidirectional data flow from input query → retrieval/indexing → format conversion → generation → response. The three parallel generator rows are a categorical (not ordinal/quantitative) breakdown of where in the generation loop enhancements can be injected.

- **Takeaway:** GraphRAG is a modular, three‑stage pipeline in which graph‑structured knowledge is retrieved from either public KGs or self‑built graph data and then *translated into generator‑friendly patterns* before generation — the key distinction from vanilla RAG, which feeds retrieved text directly to the LLM. This format‑conversion step, plus the explicit pre/mid/post‑generation enhancement hooks, is what the figure argues lets graph knowledge improve task performance.


**If `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/02-preliminaries-and-framework.md` already exists (this is a retry), overwrite it completely.**

## Tests

- `test -f /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/02-preliminaries-and-framework.md` succeeds
- `wc -l /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/02-preliminaries-and-framework.md` reports more than 40 lines
- `grep -c "In one sentence" /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/02-preliminaries-and-framework.md` reports 1
- `grep -c "## Key points" /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/02-preliminaries-and-framework.md` reports 1

## DoD

1. `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/02-preliminaries-and-framework.md` is written per the format contract above, covering the ENTIRE chunk (including its last subsections, not just the opening).
2. No git commands at all -- `.kb` auto-syncs on its own schedule.
3. `bd close <own-id> --reason "chunk 02 extracted"` -- never exit rc=0 without closing.

## Scope & constraints

- Touch ONLY `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/02-preliminaries-and-framework.md`. Do not edit any other file.
- Do not run any fleet commands other than `bd close`.
- cwd: /Users/sergii/.kb
