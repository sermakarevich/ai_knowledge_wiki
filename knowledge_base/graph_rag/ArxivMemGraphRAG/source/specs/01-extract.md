# Extract wiki page 01 — Motivation, Problem Statement, Preliminary Study

## Problem
We are building an LLM-wiki knowledge-base entry for the paper "MemGraphRAG: Memory-based
Multi-Agent System for Graph Retrieval-Augmented Generation" (arXiv 2606.00610). Your job is
to write ONE wiki page covering one chunk of the paper's text.

## Input (read ONLY these files — nothing else)
- Chunk text: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/source/chunks/01.txt`
  (covers: Abstract, Section 1 Introduction, Section 2 Problem Statement (2.1 Key Definitions,
  2.2 Problem Formulation), Section 3 Preliminary Study (3.1 Performance Degradation,
  3.2 Error Analysis, 3.3 Discussion))
- Figure description 1: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/wiki/images/page02_fig2-description.md`
  (for Figure 2: evaluation of representative RAG/GraphRAG methods — retrieval recall vs
  generation accuracy trade-off)
- Figure description 2: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/wiki/images/page04_fig3_fig4-description.md`
  (for Figure 3: illustration of three conflict types in extracted knowledge — mutually
  exclusive, temporal, granularity conflicts)

Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`,
`events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling
wiki pages "for style/convention reference" — the format contract below is the only
convention needed. Context is tight on this model — read ONLY the files listed above.

## Fix — write the output file

Output path: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/wiki/01-motivation-and-problem.md`

If this file already exists (a retry), overwrite it completely with a fresh write covering
the whole chunk.

Write the page following this EXACT structure (a page is itself a ladder — shallow at the
top, deep below):

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Motivation, Problem Statement, and Preliminary Study

**In one sentence:** <the chapter's whole argument, in one sentence — what breaks in naive
GraphRAG indexing and why>

## Key points

- <5-8 bullets, each a COMPLETE claim with real content (numbers, mechanisms, conclusions) —
  not "discusses X". These must stand alone as the chapter at medium depth.>

---

## <subsections mirroring the source's own structure, e.g.:>
## Introduction
## Problem Statement
### Key Definitions
### Problem Formulation
## Preliminary Study
### Performance Degradation
### Error Analysis (Thematic Irrelevance, Logical Inconsistency, Structural Fragmentation)
### Discussion

<Full detail: hierarchical summary of the chunk's content, not flat prose. Use tables and
exact numbers/percentages where the source gives them. Embed the two figures inline, right
next to the passage that discusses them:>

![Figure 2: Evaluation of representative RAG/GraphRAG methods](images/page02_fig2.png)

<one or two sentences paraphrasing the figure description file content, placed near the
"Performance Degradation" discussion>

![Figure 3: Three conflict types in extracted knowledge](images/page04_fig3_fig4.png)

<one or two sentences paraphrasing the figure description file content, placed near the
"Error Analysis" / conflict-types discussion>

**Covers:** Abstract, Section 1, Section 2 (2.1, 2.2), Section 3 (3.1-3.3) of arXiv 2606.00610
```

Notes:
- The image markdown paths above (`images/page02_fig2.png`, `images/page04_fig3_fig4.png`)
  are correct as written — do not change them (they are relative to the `wiki/` folder the
  output file lives in).
- Cover the WHOLE chunk, including its last topic (Section 3.3 Discussion) — do not stop
  after the opening.
- No meta-commentary about being an AI or about this task. Write only the wiki page content.

## Tests
- File exists at the output path and is non-trivial (> 40 lines).
- Both `![...]( images/...)` figure embeds are present verbatim as written above.

## DoD
1. Output file written.
2. `bd close <own-id> --reason "chunk 01 extracted"` — never exit rc=0 without closing.

## Scope & constraints
- Touch ONLY the one output file listed above.
- No git commands at all — `.kb` auto-syncs.
- Do not run any fleet commands other than `bd close`.
- On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and
  write directly.
