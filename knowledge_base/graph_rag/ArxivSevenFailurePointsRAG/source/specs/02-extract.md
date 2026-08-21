# Task: extract wiki page 2 — Case studies

## Context is tight on this model
Read ONLY the one input file listed below. Nothing else.
Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input
- Full paper text: `/Users/sergii/.kb/papers/ArxivSevenFailurePointsRAG/source/chunks/01.txt`

## Your scope within the paper
Cover ONLY Section 4 — CASE STUDIES, including:
- The intro to the case studies and Table 1 (summary of the RAG case studies)
- 4.1 Cognitive Reviewer
- 4.2 AI Tutor
- 4.3 Biomedical Question and Answer

Ignore all other sections of the input file (background/RAG pipeline, failure points, lessons, conclusion) — those become other wiki pages, not this one.

## Output
Write exactly one file: `/Users/sergii/.kb/papers/ArxivSevenFailurePointsRAG/wiki/02-case-studies.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not append or merge.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Case Studies

**In one sentence:** <the whole point of this section, one sentence>

## Key points

- <complete claim, not a topic label — 5-8 bullets total, one or more per case study>
- <...>

---

## Overview of the three case studies

<Reproduce Table 1's content as a markdown table: domain, dataset, users, running system status, etc. — whatever columns the source table has.>

## Cognitive Reviewer

<full detail — what it is, domain, purpose, deployment status, what failures were observed here>

## AI Tutor

<full detail>

## Biomedical Question and Answer

<full detail>

**Covers:** Section 4 (Case Studies), Table 1
```

Each key-point bullet must be a complete, content-bearing claim — not "discusses X". Reproduce Table 1 faithfully as markdown.

## Definition of done
1. Output file written at the exact path above, non-trivial (>40 lines), covering all three case studies and Table 1.
2. `bd close <own-bead-id> --reason "chunk 02 (case studies) extracted"`

## Scope constraints
- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than the `bd close` above.
- No git commands.
