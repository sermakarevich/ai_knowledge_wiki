# Extract task: Graph-Enhanced Generation

## Problem

This is one chunk of a long academic survey paper ("Graph Retrieval-Augmented Generation: A Survey", Peng et al. 2024, arXiv:2408.08921) being converted into an LLM-wiki. Your job is to turn this one chunk of source text into one polished wiki page. You are one of several workers each handling a different chunk in parallel -- you only need to cover YOUR chunk.

**Context is tight on this model -- read ONLY the chunk file listed below (plus the figure descriptions inlined in this spec), nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" -- the format contract below is the only convention you need. If this is a retry, do not try to diagnose the prior failure by reading logs -- just re-read the chunk and write directly.

## Fix

**Input:** Read the chunk text at `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/source/chunks/05.txt` (extracted markdown text from pages of the paper's PDF, covering: Sec 7 Graph-Enhanced Generation (generators, graph-to-text formats)).

**Output:** Write the wiki page to `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/05-graph-enhanced-generation.md`.

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

Topic for this page: **Graph-Enhanced Generation**
Section(s) covered: Sec 7 Graph-Enhanced Generation (generators, graph-to-text formats)

## Figures for this section

Image file: `images/fig5-generation-17.png` (already extracted; embed it at the point in the text that discusses it)

Vision-model description of this image:

**Figure 5 — "The overview of graph-enhanced generation."**

**What it shows.** A conceptual (schematic) pipeline, not a quantitative plot. It maps the *generation* stage of a Graph‑Retrieval‑Augmented Generation (GraphRAG) system, organized under section §7.3 "Generation Enhancement." The diagram is a left‑to‑right flow with three "enhancement" hooks mounted above it.

**Axes / trends.** There are no numeric axes, scales, or time series to read — the only "trend" is the directional data flow. Reading left to right:

1. **Input:** *Retrieval Results* (a small node‑edge graph icon) — the retrieved graph data that feeds generation.
2. **§7.2 Graph Formats:** the retrieved data is rendered into a generator‑compatible form via *Graph Languages* or *Graph Embeddings*.
3. **§7.1 Generators:** the formatted graph is consumed by a model class — *GNNs*, *LMs*, or *Hybrid Models*.
4. **Output:** *Response* (light‑bulb icon) — the final generated answer.

Overlaid on this main path are three purple "enhancement" stages that intervene at different points: *Pre‑Generation Enhancement* (before/at the format step), *Mid‑Generation Enhancement* (during generation), and *Post‑Generation Enhancement* (refining the response), each shown with a downward arrow into the pipeline.

**Takeaway.** Graph‑enhanced generation is a modular pipeline in which retrieved graph data is first *formatted* (graph languages/embeddings), then *decoded* by a suitable generator (GNN, LLM, or hybrid), with optional *generation‑enhancement* techniques applied before, during, or after decoding to lift response quality. The selection of generator and enhancement depends on the downstream task (discriminative vs. generative), per the accompanying §7.1 text.

*(No exact numeric values are present in the figure; the §‑numbers above are the only labels and are reproduced as shown.)*


**If `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/05-graph-enhanced-generation.md` already exists (this is a retry), overwrite it completely.**

## Tests

- `test -f /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/05-graph-enhanced-generation.md` succeeds
- `wc -l /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/05-graph-enhanced-generation.md` reports more than 40 lines
- `grep -c "In one sentence" /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/05-graph-enhanced-generation.md` reports 1
- `grep -c "## Key points" /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/05-graph-enhanced-generation.md` reports 1

## DoD

1. `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/05-graph-enhanced-generation.md` is written per the format contract above, covering the ENTIRE chunk (including its last subsections, not just the opening).
2. No git commands at all -- `.kb` auto-syncs on its own schedule.
3. `bd close <own-id> --reason "chunk 05 extracted"` -- never exit rc=0 without closing.

## Scope & constraints

- Touch ONLY `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/05-graph-enhanced-generation.md`. Do not edit any other file.
- Do not run any fleet commands other than `bd close`.
- cwd: /Users/sergii/.kb
