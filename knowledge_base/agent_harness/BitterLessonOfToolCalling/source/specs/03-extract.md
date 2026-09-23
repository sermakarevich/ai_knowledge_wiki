# Extract wiki page 03: Experiments

## Problem

We are building an LLM-wiki entry for the paper "The Bitter Lesson of Tool Calling"
(arXiv:2608.06370) under `/Users/sergii/.ai/knowledge/research/BitterLessonOfToolCalling/`. This
task writes ONE wiki page from ONE chunk of the paper's text.

## Input

Read ONLY this file:
`/Users/sergii/.ai/knowledge/research/BitterLessonOfToolCalling/source/chunks/03.txt`

The chunk covers the paper's **Section 4, "Experiments"**: 4.1 BFCL v4 Main
Evaluation, 4.2 Chaining Ablation, 4.3 Parallelism Ablation, 4.4 Context Rot
Ablation. There are no figures in this chunk (the chunk text mentions "Table 6
(Appendix)" — that table is handled by a different wiki page; do not try to
reproduce it here, just note its existence if referenced).

**Context is tight on this model — read ONLY the chunk file listed above, nothing
else.** Do NOT read this task's own fleet artifacts/log/event files
(`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`,
`KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference"
— the format contract below is the only convention needed. On a retry, do not
diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Output

Write the file:
`/Users/sergii/.ai/knowledge/research/BitterLessonOfToolCalling/wiki/03-experiments.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments

**In one sentence:** <the chunk's whole argument in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content — exact numbers,
  percentages, model counts, result directions. Not "discusses X".>

---

## BFCL v4 Main Evaluation

<full detail: setup, models, headline results with exact numbers/percentages,
include a markdown results table if the chunk gives per-model or per-category
numbers that fit a table>

## Chaining Ablation

<full detail with exact numbers>

## Parallelism Ablation

<full detail with exact numbers>

## Context Rot Ablation

<full detail with exact numbers>

**Covers:** Section 4 (Experiments): 4.1 BFCL v4 Main Evaluation, 4.2 Chaining
Ablation, 4.3 Parallelism Ablation, 4.4 Context Rot Ablation
```

Preserve exact numbers, percentages, and model names verbatim from the chunk. Do
not invent numbers not present in the text. Use a markdown table wherever the
chunk presents comparable numbers across multiple models or conditions.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other
than the close command below. No git commands — `.ai` auto-syncs on its own.

## Definition of Done

1. Output file written at the path above, following the format contract.
2. `bd close <own-id> --reason "chunk 03 extracted"`
