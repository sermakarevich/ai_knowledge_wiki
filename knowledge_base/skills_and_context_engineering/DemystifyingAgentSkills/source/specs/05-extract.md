# Task: Write one LLM-wiki page from a paper chunk (chunk 05 of 5, largest chunk)

You are extracting ONE wiki page for a knowledge-base entry on the paper
"Demystifying Agent Skills: Why They Work-Until They Don't" (arXiv 2608.14036).

**Context is tight on this model — read ONLY the chunk file listed below, nothing else.**
Do NOT read this task's own fleet artifacts/log/event files
(`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`),
and do NOT read sibling wiki pages "for style/convention reference" — the format contract
below is the only convention needed. On a retry, do not diagnose the prior failure by reading
logs; just re-read the chunk and write directly.

## Input

Read this file in full (it is the paper's Appendix A "Implementation Details" and Appendix B
"Prompts" — the largest chunk, ~35k characters — extracted from the PDF as markdown-ish text
with some OCR-style ligature artifacts — read past minor glyph noise):

`/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/source/chunks/05.txt`

No figures belong to this chunk. It DOES contain several data tables (numbered roughly
Table 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 depending on how the PDF extraction numbered them)
and example/prompt text blocks — preserve these as markdown tables and fenced/quoted blocks,
not prose paraphrase.

## Output

Write the page to this exact absolute path:

`/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/wiki/05-implementation-details-and-prompts.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Implementation Details and Prompts

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <complete claim 1 — a real fact/mechanism/number, not a topic label>
- <complete claim 2>
- ... (5-8 bullets total, each standing alone as substance)

---

## Implementation Details (Appendix A)

<full detail: agents, models, benchmarks, task-split information, mode-level statistics,
and any other implementation specifics the appendix gives. Reproduce data tables as markdown
tables with their original numbers, not paraphrased.>

## Prompts (Appendix B)

<full detail: reproduce the actual prompt templates/examples the appendix gives, in fenced
code blocks or blockquotes, verbatim where feasible>

**Covers:** Appendix A (Implementation Details), Appendix B (Prompts) of arXiv 2608.14036
```

Write in full prose paragraphs for the detail sections in addition to the tables/prompts (not
just more bullets). No line limit — be thorough; this chunk is large and dense, so do not
compress it — reproduce every table and every distinct prompt template found in the chunk.

## Definition of done

- Output file written at the exact path above, non-trivial (well over 40 lines — likely much
  longer given the chunk's size), covering the chunk's ENTIRE content including its LAST major
  topic (Appendix B prompts), not just the opening of Appendix A.
- No git commands — do not run git anything. `.ai` auto-syncs on its own.
- Touch ONLY the one output file. Do not run any fleet commands other than closing your own bead.
- When done: `bd close <own-id> --reason "chunk 05 extracted"`
