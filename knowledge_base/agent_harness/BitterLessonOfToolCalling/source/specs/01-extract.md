# Extract wiki page 01: Introduction and Related Work

## Problem

We are building an LLM-wiki entry for the paper "The Bitter Lesson of Tool Calling"
(arXiv:2608.06370) under `/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/`. This
task writes ONE wiki page from ONE chunk of the paper's text.

## Input

Read ONLY this file:
`/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/source/chunks/01.txt`

**Context is tight on this model — read ONLY the chunk file listed above, nothing
else.** Do NOT read this task's own fleet artifacts/log/event files
(`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`,
`KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference"
— the format contract below is the only convention needed. On a retry, do not
diagnose the prior failure by reading logs; just re-read the chunk and write directly.

The chunk covers the paper's **Abstract, Section 1 (Introduction), and Section 2
(Related Work)**. There are no figures in this chunk.

## Output

Write the file:
`/Users/sergii/.ai/knowledge/papers/BitterLessonOfToolCalling/wiki/01-introduction-and-related-work.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Related Work

**In one sentence:** <the chunk's whole argument in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (numbers,
  mechanisms, conclusions) — not "discusses X". A reader who reads ONLY these
  bullets must come away with the chunk's substance.>

---

## <subsection headings mirroring the chunk's own structure, e.g. "Motivation",
   "Programmatic tool calling vs. JSON tool calling", "Prior benchmarks and their gaps">

<Full detail: hierarchical prose under `##`/`###` headings following the chunk's own
section order (Abstract framing, then Section 1 Introduction, then Section 2 Related
Work). Preserve exact numbers, percentages, and cited prior-work claims verbatim
(e.g. specific % figures, benchmark names, author-year citations like "(Yang et al.,
2026)"). Do not invent numbers not present in the text.>

**Covers:** Abstract, Section 1 (Introduction), Section 2 (Related Work)
```

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other
than the close command below. No git commands — `.ai` auto-syncs on its own.

## Definition of Done

1. Output file written at the path above, following the format contract.
2. `bd close <own-id> --reason "chunk 01 extracted"`
