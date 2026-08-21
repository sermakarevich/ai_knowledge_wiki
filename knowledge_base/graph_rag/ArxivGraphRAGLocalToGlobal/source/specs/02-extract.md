# Task: Extract wiki page 02 — GraphRAG Methodology

## Context is tight on this model

Read ONLY the input file listed below. Nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do NOT diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input

- Source text chunk: `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/source/chunks/02.txt`
  (covers: Section 3 Methods — 3.1 GraphRAG Workflow with sub-steps 3.1.1 through 3.1.6 describing the indexing pipeline from source documents to global answers, 3.2 Global Sensemaking Question Generation with its algorithm and example personas/tasks/questions table, 3.3 Criteria for Evaluating Global Sensemaking)

No images in this chunk.

## Output

Write to: `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/02-graphrag-methodology.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# GraphRAG Methodology

**In one sentence:** <the whole mechanism in one sentence — how GraphRAG builds a graph index and answers queries via map-reduce over community summaries>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (the 6 pipeline steps, key design choices like Leiden community detection, the map-reduce query answer process, the K*N*M question generation formula, the 4 evaluation criteria) — not "discusses X">

---

## The GraphRAG Indexing Pipeline (Section 3.1)

<full detail prose covering each of the 6 sub-steps (3.1.1-3.1.6) in order, as its own subsection or clearly delineated paragraph each:>

### Source Documents → Text Chunks (3.1.1)
### Text Chunks → Entities & Relationships (3.1.2)
<include the NeoChip worked example verbatim if present in the chunk text>
### Entities & Relationships → Knowledge Graph (3.1.3)
### Knowledge Graph → Graph Communities (3.1.4)
### Graph Communities → Community Summaries (3.1.5)
### Community Summaries → Community Answers → Global Answer (3.1.6)

## Global Sensemaking Question Generation (Section 3.2)

<describe the K*N*M persona/task/question generation algorithm; include example questions from the source's Table 1 if present in the chunk>

## Criteria for Evaluating Global Sensemaking (Section 3.3)

<the 4 criteria: Comprehensiveness, Diversity, Empowerment, Directness — with their exact definitions from the source>

---

**Covers:** Section 3 (Methods: 3.1 GraphRAG Workflow, 3.2 Global Sensemaking Question Generation, 3.3 Criteria for Evaluating Global Sensemaking).
```

## Rules

- Cover the WHOLE chunk — verify the end of the chunk (3.3 evaluation criteria) got real coverage, not just the pipeline steps at the top.
- No meta-commentary about your own process. No "as an AI" disclaimers. Just the page content.
- Use exact numbers, definitions, and terminology from the source text — do not paraphrase away specifics (e.g. keep "K = M = N = 5", "125 test questions per dataset").
- Preserve worked examples (like the NeoChip entity extraction example) verbatim where they appear.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other than closing your own bead.

## DoD

1. `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/02-graphrag-methodology.md` written per the format contract above, covering the entire chunk.
2. `bd close <own-id> --reason "chunk 02 extracted"`
