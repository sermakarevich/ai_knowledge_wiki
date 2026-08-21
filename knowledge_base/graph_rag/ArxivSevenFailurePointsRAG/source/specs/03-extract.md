# Task: extract wiki page 3 — Seven failure points of RAG systems

## Context is tight on this model
Read ONLY the one input file listed below. Nothing else.
Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input
- Full paper text: `/Users/sergii/.kb/papers/ArxivSevenFailurePointsRAG/source/chunks/01.txt`

## Your scope within the paper
Cover ONLY Section 5 — FAILURE POINTS OF RAG SYSTEMS. This is the paper's core contribution: exactly seven named failure points, each with its explanation and (where given) which case study surfaced it. Do not skip any of the seven.

Ignore all other sections of the input file (background/RAG pipeline, case studies, lessons, conclusion) — those become other wiki pages, not this one.

## Output
Write exactly one file: `/Users/sergii/.kb/papers/ArxivSevenFailurePointsRAG/wiki/03-seven-failure-points.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not append or merge.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Seven Failure Points of RAG Systems

**In one sentence:** <the whole point of this section, one sentence>

## Key points

- <one bullet per failure point (7 bullets), each a complete claim naming the failure point and its cause/consequence>

---

## 1. <Failure point name>

<full detail: what causes it, why it happens, example/evidence from the source>

## 2. <Failure point name>

...

(continue through all 7, using the exact failure-point names from the source as sub-headings)

**Covers:** Section 5 (Failure Points of RAG Systems)
```

Each key-point bullet must be a complete, content-bearing claim — not "discusses X". This page is the paper's central content — be thorough, do not compress any of the 7 into a single sentence in the detail section.

## Definition of done
1. Output file written at the exact path above, non-trivial (>40 lines), covering all 7 failure points with their own sub-headings.
2. `bd close <own-bead-id> --reason "chunk 03 (failure points) extracted"`

## Scope constraints
- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than the `bd close` above.
- No git commands.
