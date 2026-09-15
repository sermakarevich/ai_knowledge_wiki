# Extract wiki page 06: Appendix Details

## Problem

We are building an LLM-wiki entry for the paper "The Bitter Lesson of Tool Calling"
(arXiv:2608.06370) under `/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/`. This
task writes ONE wiki page from ONE chunk of the paper's text.

## Input

Read ONLY this file:
`/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/source/chunks/06.txt`

The chunk covers the paper's appendices: **Appendix A ("Per-Category Accuracy on
BFCL v4"**, containing Table 6, a per-category accuracy table**)**, **Appendix B
("Programmatic tool calling" worked example** — a concrete Python script example
executed as a tool call, with subprocess output**)**, and **Appendix C ("System
Prompts"** — condensed descriptions of the JSON tool calling system prompt, the
programmatic tool calling system prompt, and the stub module design**)**. There are
no images in this chunk.

**Context is tight on this model — read ONLY the chunk file listed above, nothing
else.** Do NOT read this task's own fleet artifacts/log/event files
(`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`,
`KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference"
— the format contract below is the only convention needed. On a retry, do not
diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Output

Write the file:
`/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/wiki/06-appendix-details.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix Details

**In one sentence:** <what these appendices add beyond the main text, in one
sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content — e.g. specific
  per-category accuracy numbers from Table 6, the key mechanic of the worked
  example, the key design choice of the stub modules or system prompts. Not
  "discusses X".>

---

## Per-Category Accuracy on BFCL v4 (Appendix A)

<Reproduce Table 6 as a markdown table exactly as given in the chunk (category names
and per-model/per-paradigm accuracy numbers). Add 1-2 sentences on what the
category-level breakdown reveals beyond the paper's aggregate numbers.>

## Programmatic Tool Calling Worked Example (Appendix B)

<Describe the worked example: what it demonstrates, and include the example Python
script and its output as a fenced code block, exactly as given in the chunk.>

## System Prompts (Appendix C)

<Full detail: the JSON tool calling system prompt design, the programmatic tool
calling system prompt design, and the stub module design, as described in the
chunk.>

**Covers:** Appendix A (Table 6), Appendix B, Appendix C
```

Preserve exact numbers, table values, and code verbatim from the chunk. Do not
invent numbers or code not present in the text.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other
than the close command below. No git commands — `.ai` auto-syncs on its own.

## Definition of Done

1. Output file written at the path above, following the format contract.
2. `bd close <own-id> --reason "chunk 06 extracted"`
