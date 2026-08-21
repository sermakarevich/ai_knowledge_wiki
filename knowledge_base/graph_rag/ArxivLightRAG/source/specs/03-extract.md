# Task: Write wiki page 03 — Evaluation Setup and Main Results (RQ1)

## Context

You are extracting one section of the paper "LightRAG: Simple and Fast Retrieval-Augmented Generation" (arXiv:2410.05779) into one wiki page. This is chunk 3 of 5. Context is tight on this model — **read ONLY the input file listed below, nothing else.** Do NOT read this task's own fleet artifacts/logs (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input

Read this file only:
`/Users/sergii/.kb/papers/ArxivLightRAG/source/chunks/03.txt`

This chunk covers: the evaluation section intro (Section 4), experimental settings (4.1 — datasets, baselines, evaluation protocol), and the comparison of LightRAG with existing RAG methods answering RQ1 (4.2 — including any results tables/win-rate comparisons in the text).

There are no figures for this chunk.

## Output

Write the file:
`/Users/sergii/.kb/papers/ArxivLightRAG/wiki/03-evaluation-setup-and-main-results.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Evaluation Setup and Main Results (RQ1)

**In one sentence:** <the chapter's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <complete claim>
- (5-8 bullets total, each carrying real content — numbers, mechanisms, conclusions, not "discusses X">

---

## <subsection headings mirroring the chunk's own structure, e.g. Research Questions, Experimental Settings (datasets, baselines, metrics), Comparison with Existing RAG Methods (RQ1)>

<hierarchical detail. Include exact numbers, dataset names, baseline names, and any comparison results verbatim from the text where present, as markdown tables where the source has tabular results. Be thorough — no line limit.>

**Covers:** Section 4 intro, 4.1 experimental settings, 4.2 comparison with existing RAG methods (RQ1)
```

Rules:
- Every wiki page opens with the backlink line, then `# <Topic>`, then `**In one sentence:**`, then `## Key points` (5-8 bullets that stand alone as this chapter at medium depth), then `---`, then full hierarchical detail, then the `**Covers:**` footer.
- Use Obsidian `[[wikilink]]` syntax for internal links (only the backlink line needs one here).
- Reproduce any quantitative comparison as a markdown table with exact numbers from the text.
- No meta-commentary about your own process — only the paper's content.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

## Done

1. Write the output file.
2. `bd close <own-id> --reason "chunk 03 extracted"`
