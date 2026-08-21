# Extract task: Introduction, Motivation & Related Surveys

## Problem

This is one chunk of a long academic survey paper ("Graph Retrieval-Augmented Generation: A Survey", Peng et al. 2024, arXiv:2408.08921) being converted into an LLM-wiki. Your job is to turn this one chunk of source text into one polished wiki page. You are one of several workers each handling a different chunk in parallel -- you only need to cover YOUR chunk.

**Context is tight on this model -- read ONLY the chunk file listed below (plus the figure descriptions inlined in this spec), nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" -- the format contract below is the only convention you need. If this is a retry, do not try to diagnose the prior failure by reading logs -- just re-read the chunk and write directly.

## Fix

**Input:** Read the chunk text at `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/source/chunks/01.txt` (extracted markdown text from pages of the paper's PDF, covering: Abstract; Sec 1 Introduction; Sec 2 Comparison with Related Techniques and Surveys).

**Output:** Write the wiki page to `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/01-introduction-and-related-work.md`.

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

Topic for this page: **Introduction, Motivation & Related Surveys**
Section(s) covered: Abstract; Sec 1 Introduction; Sec 2 Comparison with Related Techniques and Surveys

## Figures for this section

Image file: `images/fig1-comparison-03.png` (already extracted; embed it at the point in the text that discusses it)

Vision-model description of this image:

**Figure 1 — Technical summary**

**What it shows.** A schematic side‑by‑side flow diagram comparing three answer‑generation pipelines for the same user query ("How did the artistic movements of the 19th century impact the development of modern art in the 20th century?"). Each panel is a vertical flow: *Query → (optional) Retriever → LLMs → Response*. A red "✗" or black "✓" under each response signals whether the output is deemed adequate.

**Axes / quantitative trends.** There are no plotted axes, scales, or numerical trends; this is a qualitative architecture diagram rather than a chart. The only "trend" is a left‑to‑right progression in retrieval structure and answer specificity:

- **Left — Direct LLM:** Query goes straight to the LLMs. The response is a generic, shallow summary. Marked ✗.
- **Middle — RAG:** A Retriever returns *retrieved text* (a short numbered fact list, ~4 items) that is fed to the LLMs. The response is more concrete but still blends relational claims into prose. Marked ✗.
- **Right — GraphRAG:** A Retriever returns *retrieved triplets* — explicit subject–predicate–object edges (e.g., (Claude Monet)–introduced→(new techniques); (Impressionist techniques)–influenced→(later art movements); (Pablo Picasso)–pioneered→(Cubism)) — which drive the LLMs to a precise, relation‑faithful answer. Marked ✓.

**Takeaway.** Direct LLM answers are shallow; RAG improves grounding but, because natural‑language text encodes entity relationships loosely and at variable length, it under‑emphasizes the relational ("influence") structure that is the core of the question. GraphRAG, by retrieving explicit entity–relation triples from a graph, preserves that relational structure and yields a more accurate, specific response — the only configuration endorsed with a checkmark.


**If `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/01-introduction-and-related-work.md` already exists (this is a retry), overwrite it completely.**

## Tests

- `test -f /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/01-introduction-and-related-work.md` succeeds
- `wc -l /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/01-introduction-and-related-work.md` reports more than 40 lines
- `grep -c "In one sentence" /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/01-introduction-and-related-work.md` reports 1
- `grep -c "## Key points" /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/01-introduction-and-related-work.md` reports 1

## DoD

1. `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/01-introduction-and-related-work.md` is written per the format contract above, covering the ENTIRE chunk (including its last subsections, not just the opening).
2. No git commands at all -- `.kb` auto-syncs on its own schedule.
3. `bd close <own-id> --reason "chunk 01 extracted"` -- never exit rc=0 without closing.

## Scope & constraints

- Touch ONLY `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/01-introduction-and-related-work.md`. Do not edit any other file.
- Do not run any fleet commands other than `bd close`.
- cwd: /Users/sergii/.kb
