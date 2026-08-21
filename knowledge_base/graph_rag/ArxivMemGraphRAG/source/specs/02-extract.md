# Extract wiki page 02 — MemGraphRAG Framework and Experiments

## Problem
We are building an LLM-wiki knowledge-base entry for the paper "MemGraphRAG: Memory-based
Multi-Agent System for Graph Retrieval-Augmented Generation" (arXiv 2606.00610). Your job is
to write ONE wiki page covering one chunk of the paper's text.

## Input (read ONLY these files — nothing else)
- Chunk text: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/source/chunks/02.txt`
  (covers: Section 4 Our Framework (4.1 MemGraphRAG Architecture, 4.2 Memory-based Indexing
  Graph, 4.3 Memory-guided Online Retrieval), Section 5 Experiments (5.1 Experimental
  Setting, 5.2 Generation Accuracy (Q1), 5.3 Retrieval Analysis (Q2), 5.4 Indexing Graph
  Adaptability Analysis (Q3), 5.5 Ablation Study (Q4)))
- Figure description 1: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/wiki/images/page04_fig3_fig4-description.md`
  (for Figure 4: overview of the MemGraphRAG framework, two phases — Memory-Based Indexing
  Graph Construction and Memory-guided Online Retrieval)
- Figure description 2: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/wiki/images/page08_fig5-description.md`
  (for Figure 5: ablation study of MemGraphRAG on three datasets)

Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`,
`events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling
wiki pages "for style/convention reference" — the format contract below is the only
convention needed. Context is tight on this model — read ONLY the files listed above.

## Fix — write the output file

Output path: `/Users/sergii/.kb/papers/ArxivMemGraphRAG/wiki/02-memgraphrag-framework.md`

If this file already exists (a retry), overwrite it completely with a fresh write covering
the whole chunk.

Write the page following this EXACT structure (a page is itself a ladder — shallow at the
top, deep below):

```
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The MemGraphRAG Framework and Experimental Results

**In one sentence:** <the chapter's whole argument, in one sentence — how MemGraphRAG's
Global Memory + Hierarchical Indexing Graph solve the problems from the motivation chapter,
and what the experiments show>

## Key points

- <5-8 bullets, each a COMPLETE claim with real content (numbers, mechanisms, conclusions,
  benchmark results) — not "discusses X". These must stand alone as the chapter at medium
  depth.>

---

## Framework Architecture
### Global Memory (M) and the Hierarchical Indexing Graph (G)
## Memory-based Indexing Graph Construction
### Schema Filtering
### Consistency Maintenance via Global Adjudication
## Memory-guided Online Retrieval
### Entity Node Initialization via Facts
### Type Node Initialization via Schemas
### Passage Node Initialization via Information Density
## Experimental Setting
## Generation Accuracy (Q1)
## Retrieval Analysis (Q2)
## Indexing Graph Adaptability Analysis (Q3)
## Ablation Study (Q4)

<Full detail: hierarchical summary of the chunk's content, not flat prose. Use tables and
exact numbers/percentages/metric values where the source gives them (e.g. recall, accuracy
figures per dataset/method). Embed the two figures inline, right next to the passage that
discusses them:>

![Figure 4: Overview of the MemGraphRAG framework](images/page04_fig3_fig4.png)

<one or two sentences paraphrasing the figure description file content, placed near the
"Framework Architecture" discussion>

![Figure 5: Ablation study of MemGraphRAG on three datasets](images/page08_fig5.png)

<one or two sentences paraphrasing the figure description file content, placed near the
"Ablation Study (Q4)" discussion>

**Covers:** Section 4 (4.1-4.3), Section 5 (5.1-5.5) of arXiv 2606.00610
```

Notes:
- The image markdown paths above are correct as written — do not change them.
- Cover the WHOLE chunk, including its last topic (5.5 Ablation Study) — do not stop after
  the opening sections.
- No meta-commentary about being an AI or about this task. Write only the wiki page content.

## Tests
- File exists at the output path and is non-trivial (> 40 lines).
- Both `![...]( images/...)` figure embeds are present verbatim as written above.

## DoD
1. Output file written.
2. `bd close <own-id> --reason "chunk 02 extracted"` — never exit rc=0 without closing.

## Scope & constraints
- Touch ONLY the one output file listed above.
- No git commands at all — `.kb` auto-syncs.
- Do not run any fleet commands other than `bd close`.
- On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and
  write directly.
