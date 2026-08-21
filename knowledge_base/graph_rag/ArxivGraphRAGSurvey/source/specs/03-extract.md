# Extract task: Graph-Based Indexing

## Problem

This is one chunk of a long academic survey paper ("Graph Retrieval-Augmented Generation: A Survey", Peng et al. 2024, arXiv:2408.08921) being converted into an LLM-wiki. Your job is to turn this one chunk of source text into one polished wiki page. You are one of several workers each handling a different chunk in parallel -- you only need to cover YOUR chunk.

**Context is tight on this model -- read ONLY the chunk file listed below (plus the figure descriptions inlined in this spec), nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" -- the format contract below is the only convention you need. If this is a retry, do not try to diagnose the prior failure by reading logs -- just re-read the chunk and write directly.

## Fix

**Input:** Read the chunk text at `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/source/chunks/03.txt` (extracted markdown text from pages of the paper's PDF, covering: Sec 5 Graph-Based Indexing).

**Output:** Write the wiki page to `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/03-graph-based-indexing.md`.

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

Topic for this page: **Graph-Based Indexing**
Section(s) covered: Sec 5 Graph-Based Indexing

## Figures for this section

Image file: `images/fig3-indexing-10.png` (already extracted; embed it at the point in the text that discusses it)

Vision-model description of this image:

**Figure 3 — "The overview of graph-based indexing" (schematic flow diagram)**

**What it shows:** A left‑to‑right pipeline diagram (not a quantitative plot) illustrating the components of graph‑based indexing. There are **no axes, no curves, and no numerical trends**; it is a structural/conceptual schematic.

**Structure (left → right):**
1. **Data Source** (input box): three input types — *Wikipedia*, *Text Corpus*, and *Tables*.
2. **§ 5.1 Graph Data** (middle box): the knowledge‑graph layer, split into *Self‑constructed Knowledge Graphs* and *Open Knowledge Graphs*, with the open category further divided into *General* and *Domain Knowledge Graphs*.
3. **Graph Database** (right, with a database icon): the stored, indexable graph store.
4. **§ 5.2 Indexing** (top‑right box): the indexing strategies that operate over the graph, listed as *Graph Indexing, Text Indexing, Vector Indexing,* and *Hybrid Indexing*, feeding into the graph database.

**Takeaway:** Graph‑based indexing is organized as a staged pipeline — raw heterogeneous sources (Wikipedia, text, tables) are transformed into knowledge graphs, persisted in a graph database, and made retrievable through four complementary indexing schemes (graph, text, vector, and their hybrid). The diagram's purpose is to map the paper's §5.1/§5.2 structure rather than to report measured results.


**If `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/03-graph-based-indexing.md` already exists (this is a retry), overwrite it completely.**

## Tests

- `test -f /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/03-graph-based-indexing.md` succeeds
- `wc -l /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/03-graph-based-indexing.md` reports more than 40 lines
- `grep -c "In one sentence" /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/03-graph-based-indexing.md` reports 1
- `grep -c "## Key points" /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/03-graph-based-indexing.md` reports 1

## DoD

1. `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/03-graph-based-indexing.md` is written per the format contract above, covering the ENTIRE chunk (including its last subsections, not just the opening).
2. No git commands at all -- `.kb` auto-syncs on its own schedule.
3. `bd close <own-id> --reason "chunk 03 extracted"` -- never exit rc=0 without closing.

## Scope & constraints

- Touch ONLY `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/03-graph-based-indexing.md`. Do not edit any other file.
- Do not run any fleet commands other than `bd close`.
- cwd: /Users/sergii/.kb
