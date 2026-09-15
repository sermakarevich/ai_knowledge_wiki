# Extract wiki page 04: Analysis

## Problem

We are building an LLM-wiki entry for the paper "The Bitter Lesson of Tool Calling"
(arXiv:2608.06370) under `/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/`. This
task writes ONE wiki page from ONE chunk of the paper's text, plus one figure
description.

## Input

Read ONLY these two files:
1. `/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/source/chunks/04.txt`
   (the paper's Section 5, "Analysis", covering 5.1 Model Generation Predicts
   Programmatic tool calling Viability, 5.2 Programmatic tool calling Handles
   [enumeration/fan-out], 5.3 Programmatic tool calling Reduces Latency on
   Chaining Tasks)
2. `/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/wiki/images/04-description.md`
   (a text description of Figure 2, "Accuracy (%) on the BFCL v4 subset for JSON
   tool calling and programmatic tool calling (PTC) by model generation" — a
   two-panel line chart, OpenAI models vs. Anthropic models)

**Context is tight on this model — read ONLY the two files listed above, nothing
else.** Do NOT read this task's own fleet artifacts/log/event files
(`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`,
`KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference"
— the format contract below is the only convention needed. On a retry, do not
diagnose the prior failure by reading logs; just re-read the two input files and
write directly.

## Output

Write the file:
`/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/wiki/04-analysis.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Analysis

**In one sentence:** <the chunk's whole argument in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content — exact numbers,
  percentages, thresholds. Not "discusses X".>

---

## Model Generation Predicts Programmatic Tool Calling Viability

<full detail from subsection 5.1>

![Accuracy on BFCL v4 by model generation, JSON vs. programmatic tool calling](images/fig2-accuracy-by-model-generation.png)

<1-3 sentences summarizing the figure, based on the figure description file, placed
right after the embedded image>

## Enumeration vs. Aggregation Behavior

<full detail from subsection 5.2, covering the enumeration/fan-out findings and any
fan-out threshold numbers (e.g. specific N values and accuracy percentages)>

## Programmatic Tool Calling Reduces Latency on Chaining Tasks

<full detail from subsection 5.3, with exact latency ratios/numbers>

**Covers:** Section 5 (Analysis): 5.1, 5.2, 5.3; Figure 2
```

Preserve exact numbers, percentages, and thresholds verbatim from the chunk. Do not
invent numbers not present in the text. The image path
`images/fig2-accuracy-by-model-generation.png` already exists — reference it
exactly as shown, do not change the filename.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other
than the close command below. No git commands — `.ai` auto-syncs on its own.

## Definition of Done

1. Output file written at the path above, following the format contract, with the
   figure embedded.
2. `bd close <own-id> --reason "chunk 04 extracted"`
