# Task: extract wiki page 1 — Background & RAG pipeline

## Context is tight on this model
Read ONLY the one input file listed below (plus the one image description file, if listed). Nothing else.
Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input
- Full paper text (markdown-ish, extracted from PDF): `/Users/sergii/.kb/papers/ArxivSevenFailurePointsRAG/source/chunks/01.txt`
- Figure description (vision-model output for Figure 1): `/Users/sergii/.kb/papers/ArxivSevenFailurePointsRAG/wiki/images/01-description.md`
- Figure image file (already extracted, do not regenerate — just embed by path): `images/01-figure1-rag-pipeline.png`

## Your scope within the paper
Cover ONLY these sections of the input text:
- Section 1 — INTRODUCTION
- Section 2 — RELATED WORK
- Section 3 — RETRIEVAL AUGMENTED GENERATION (3.1 Index Process, 3.2 Query Process), including Figure 1 (the indexing/query pipeline diagram)

Ignore all other sections of the input file (case studies, failure points, lessons, conclusion) — those become other wiki pages, not this one.

## Output
Write exactly one file: `/Users/sergii/.kb/papers/ArxivSevenFailurePointsRAG/wiki/01-background-and-rag-pipeline.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not append or merge.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Background & RAG Pipeline

**In one sentence:** <the whole point of this section, one sentence>

## Key points

- <complete claim, not a topic label — 5-8 bullets total>
- <...>

---

## <subsection headings mirroring the source, e.g. "Why RAG over fine-tuning", "The index process", "The query process">

<full detail prose, hierarchical, following the source's own structure. Use tables/exact wording where the source has them.>

![Figure 1: Indexing and Query processes for a RAG system](images/01-figure1-rag-pipeline.png)

<Describe what Figure 1 shows in your own words too, informed by the figure description file above — don't just caption it.>

**Covers:** Sections 1-3 (Introduction, Related Work, Retrieval Augmented Generation)
```

Each key-point bullet must be a complete, content-bearing claim (numbers, mechanisms, conclusions) — not "discusses X". The figure MUST be embedded with the markdown image syntax shown above; this is non-negotiable since the page names it.

## Definition of done
1. Output file written at the exact path above, non-trivial (>40 lines), covering all three sections including their subsections.
2. `bd close <own-bead-id> --reason "chunk 01 (background) extracted"`

## Scope constraints
- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than the `bd close` above.
- No git commands.
