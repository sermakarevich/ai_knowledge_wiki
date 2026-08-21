# Extract task: chunk 02 — Question Answering results

## Context (tight — read ONLY what is listed below, nothing else)

You are writing ONE wiki page for a knowledge-base entry on the paper "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights" (Han et al., 2025, arXiv:2502.11371).

Context is tight on this model — read ONLY the files listed below. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

**Input (read exactly these files, nothing else):**
- `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/source/chunks/02.txt` (the section text)
- `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/wiki/images/fig1-qa-performance-description.md` (description of Figure 1)
- `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/wiki/images/fig2-confusion-matrices-description.md` (description of Figure 2)
- `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/wiki/images/fig3-qa-performance-comparison-description.md` (description of Figure 3)

This chunk covers: Section 4 (Question Answering) in full — datasets/metrics, QA main results, QA with reranking and iterative retrieval, comparative QA analysis, improving QA performance (Selection/Integration hybrid strategies), computation and storage analysis, graph construction model ablation.

**Output (write exactly this file):**
`/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/wiki/02-question-answering-results.md`

If this file already exists (a retry), overwrite it completely.

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Question Answering Results

**In one sentence:** <the section's whole argument, in one sentence>

## Key points

- <complete claim with real content — numbers, mechanisms, conclusions — not "discusses X">
- <5-8 bullets total>

---

<## subsections mirroring the chunk's internal structure: datasets/metrics, main results, reranking/IRCoT, comparative analysis, hybrid strategies, cost analysis, graph-construction-model ablation>
<tables, exact numbers (F1 scores, timings, storage sizes) verbatim from the chunk>

![Overall QA performance (F1) under different inference strategies](images/fig1-qa-performance.png)

<embed fig1 near the discussion of reranking/IRCoT results; embed fig2 near the confusion-matrix discussion; embed fig3 near the Selection/Integration hybrid-strategy discussion, each using the corresponding description file's content as your source for describing the figure in prose>

**Covers:** Section 4 (Question Answering)
```

Rules:
- Backlink line first, exactly as shown.
- `**In one sentence:**` and `## Key points` near the top, before the `---` divider.
- Embed all three figures (`![...](images/fig1-qa-performance.png)`, `![...](images/fig2-confusion-matrices.png)`, `![...](images/fig3-qa-performance-comparison.png)`) at the point in the text where the chunk discusses that figure. Use the corresponding `*-description.md` content to write an accurate caption and surrounding prose — you cannot see the images directly, only their text descriptions.
- Cover the WHOLE chunk, including the final subsections (computation/storage analysis, graph construction model) — this is the longest chunk; do not stop after the opening results table.
- No line limit — be thorough, but no filler or repetition.
- No meta-commentary about the task itself; write only the page content.

## Done

1. Write the output file above.
2. `bd close <own-id> --reason "chunk 02 extracted"`

## Scope

Touch ONLY the one output file listed above. Do not run any fleet command other than `bd close`. Do not run git commands.
