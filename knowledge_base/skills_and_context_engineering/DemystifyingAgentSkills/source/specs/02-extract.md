# Task: Write one LLM-wiki page from a paper chunk (chunk 02 of 5)

You are extracting ONE wiki page for a knowledge-base entry on the paper
"Demystifying Agent Skills: Why They Work-Until They Don't" (arXiv 2608.14036).

**Context is tight on this model — read ONLY the files listed below, nothing else.**
Do NOT read this task's own fleet artifacts/log/event files
(`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`),
and do NOT read sibling wiki pages "for style/convention reference" — the format contract
below is the only convention needed. On a retry, do not diagnose the prior failure by reading
logs; just re-read the inputs and write directly.

## Input

Read these files in full:

1. `/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/source/chunks/02.txt` — the paper's
   Section 3 "Study Design" (research questions, experimental setup, experimental design),
   extracted from the PDF as markdown-ish text with some OCR-style ligature artifacts — read
   past minor glyph noise.
2. `/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/wiki/images/01-fig1-overview-page2-description.md`
   — a vision-model description of Figure 1 (the two-panel experimental pipeline schematic),
   which belongs to this section. Use it to write about the figure without seeing the image.

## Output

Write the page to this exact absolute path:

`/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/wiki/02-study-design.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Study Design

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <complete claim 1 — a real fact/mechanism/number, not a topic label>
- <complete claim 2>
- ... (5-8 bullets total, each standing alone as substance)

---

## <subsection mirroring the chunk's own structure, e.g. Research Questions>

<full detail>

## <subsection, e.g. Experimental Setup>

<full detail: benchmarks, agent harnesses, LLMs used, exact configuration numbers>

## <subsection, e.g. Experimental Design / Contrastive Design>

<full detail on how the controlled quantitative experiments and the paired trajectory
analysis are combined>

## Figure: Experimental Pipelines

![Experimental pipelines — skill-vs-procedural-memory pipeline and three-experiment skill-retrieval evaluation](images/01-fig1-overview-page2.png)

<1-2 paragraphs describing what the figure shows, drawn from the description file, placed
next to the text that discusses the methodology it illustrates>

**Covers:** Section 3 (Study Design) of arXiv 2608.14036, including Figure 1
```

Write in full prose paragraphs for the detail sections (not just more bullets). Include exact
numbers, benchmark names, model names, and configuration details verbatim where given. No line
limit — be thorough; do not compress the whole chunk into the Key points block alone.

## Definition of done

- Output file written at the exact path above, non-trivial (well over 40 lines), covering the
  chunk's ENTIRE content (not just its opening paragraphs), and embedding the figure exactly as
  shown above.
- No git commands — do not run git anything. `.ai` auto-syncs on its own.
- Touch ONLY the one output file. Do not run any fleet commands other than closing your own bead.
- When done: `bd close <own-id> --reason "chunk 02 extracted"`
