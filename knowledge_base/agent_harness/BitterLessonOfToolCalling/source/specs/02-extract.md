# Extract wiki page 02: Method

## Problem

We are building an LLM-wiki entry for the paper "The Bitter Lesson of Tool Calling"
(arXiv:2608.06370) under `/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/`. This
task writes ONE wiki page from ONE chunk of the paper's text, plus one figure
description.

## Input

Read ONLY these two files:
1. `/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/source/chunks/02.txt`
   (the paper's Section 3, "Method", covering Task Definition, Paradigms, Benchmark
   and Evaluation, Ablation Design, and Models)
2. `/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/wiki/images/01-description.md`
   (a text description of Figure 1, "Overview of the two primary paradigms
   evaluated" — a process diagram contrasting JSON tool calling vs. programmatic/
   inline Python tool calling)

**Context is tight on this model — read ONLY the two files listed above, nothing
else.** Do NOT read this task's own fleet artifacts/log/event files
(`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`,
`KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference"
— the format contract below is the only convention needed. On a retry, do not
diagnose the prior failure by reading logs; just re-read the two input files and
write directly.

## Output

Write the file:
`/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/wiki/02-method.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Method

**In one sentence:** <the chunk's whole argument in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (numbers,
  mechanisms, conclusions) — not "discusses X".>

---

## Task Definition

<full detail from that subsection>

## Paradigms: JSON tool calling vs. programmatic tool calling

<full detail from that subsection, describing both paradigms precisely>

![Overview of the two primary paradigms evaluated](images/fig1-paradigm-overview.png)

<1-3 sentences summarizing the figure, based on the figure description file, placed
right after the embedded image>

## Benchmark and Evaluation

<full detail from that subsection>

## Ablation Design

<full detail from that subsection>

## Models

<full detail from that subsection — list the models/model families evaluated>

**Covers:** Section 3 (Method): 3.1 Task Definition, 3.2 Paradigms, 3.3 Benchmark
and Evaluation, 3.4 Ablation Design, 3.5 Models; Figure 1
```

Preserve exact numbers, model names, and configuration details verbatim from the
chunk. Do not invent numbers not present in the text. The image path
`images/fig1-paradigm-overview.png` already exists — reference it exactly as shown,
do not change the filename.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other
than the close command below. No git commands — `.ai` auto-syncs on its own.

## Definition of Done

1. Output file written at the path above, following the format contract, with the
   figure embedded.
2. `bd close <own-id> --reason "chunk 02 extracted"`
