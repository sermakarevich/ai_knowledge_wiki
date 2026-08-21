# Extract task: chunk 01 — Introduction, Related Works, Evaluation Framework

## Context (tight — read ONLY what is listed below, nothing else)

You are writing ONE wiki page for a knowledge-base entry on the paper "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights" (Han et al., 2025, arXiv:2502.11371).

Context is tight on this model — read ONLY the chunk file listed below. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

**Input (read exactly this file, nothing else):**
`/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/source/chunks/01.txt`

This chunk covers: Section 1 (Introduction), Section 2 (Related Works — RAG, Graph RAG), Section 3 (Evaluation Framework — RAG pipeline, GraphRAG implementations, tasks, unified experimental settings). No figures belong to this chunk.

**Output (write exactly this file):**
`/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/wiki/01-introduction-and-evaluation-framework.md`

If this file already exists (a retry), overwrite it completely.

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Evaluation Framework

**In one sentence:** <the section's whole argument, in one sentence>

## Key points

- <complete claim with real content — numbers, mechanisms, conclusions — not "discusses X">
- <5-8 bullets total, each standing alone as substance>

---

<## subsections mirroring the chunk's internal structure — hierarchical, not flat prose>
<tables, exact numbers, named methods/datasets verbatim where the chunk gives them>

**Covers:** Sections 1-3 (Introduction, Related Works, Evaluation Framework)
```

Rules:
- Backlink line first, exactly as shown.
- `**In one sentence:**` and `## Key points` must appear near the top, before the `---` divider — someone reading only that far should have the section's substance.
- Cover the WHOLE chunk, including its final subsection (3.4 Unified Experimental Settings) — do not stop after the opening paragraphs.
- No line limit — be thorough, but no filler or repetition.
- No meta-commentary about the task itself; write only the page content.

## Done

1. Write the output file above.
2. `bd close <own-id> --reason "chunk 01 extracted"`

## Scope

Touch ONLY the one output file listed above. Do not run any fleet command other than `bd close`. Do not run git commands.
