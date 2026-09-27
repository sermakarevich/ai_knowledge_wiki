# Task: Write one LLM-wiki page from a paper chunk (chunk 01 of 5)

You are extracting ONE wiki page for a knowledge-base entry on the paper
"Demystifying Agent Skills: Why They Work-Until They Don't" (arXiv 2608.14036).

**Context is tight on this model — read ONLY the chunk file listed below, nothing else.**
Do NOT read this task's own fleet artifacts/log/event files
(`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`),
and do NOT read sibling wiki pages "for style/convention reference" — the format contract
below is the only convention needed. On a retry, do not diagnose the prior failure by reading
logs; just re-read the chunk and write directly.

## Input

Read this file in full (it is the paper's Abstract, Section 1 Introduction, and Section 2
Related Works, extracted from the PDF as markdown-ish text with some OCR-style ligature
artifacts — read past minor glyph noise):

`/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/source/chunks/01.txt`

No figures belong to this chunk.

## Output

Write the page to this exact absolute path:

`/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/wiki/01-introduction-and-related-work.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Related Work

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <complete claim 1 — a real fact/mechanism/number, not a topic label>
- <complete claim 2>
- ... (5-8 bullets total, each standing alone as substance)

---

## <subsection mirroring the chunk's own structure>

<full detail: the paper's motivation, the gap in prior evaluation methodology it identifies,
the specific research question(s) it poses, and how it positions itself against the related
work it cites (memory-reuse-in-LLM-agents literature, agent benchmarks). Name specific prior
methods/papers it contrasts itself with if the chunk names them. Include exact numbers/claims
verbatim where given.>

## <another subsection>

...

**Covers:** Abstract, Section 1 (Introduction), Section 2 (Related Works) of arXiv 2608.14036
```

Write in full prose paragraphs for the detail sections (not just more bullets), organized under
`##` subsections that mirror the chunk's own structure (e.g. one subsection for the motivation/
gap, one for the research questions, one for related work positioning). No line limit — be
thorough; do not compress the whole chunk into the Key points block alone.

## Definition of done

- Output file written at the exact path above, non-trivial (well over 40 lines), covering the
  chunk's ENTIRE content (not just its opening paragraphs).
- No git commands — do not run git anything. `.ai` auto-syncs on its own.
- Touch ONLY the one output file. Do not run any fleet commands other than closing your own bead.
- When done: `bd close <own-id> --reason "chunk 01 extracted"`
