# Task: Write one LLM-wiki page from a paper chunk (chunk 03 of 5)

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

1. `/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/source/chunks/03.txt` — the paper's
   Section 4 "Skill-Use Mechanisms: A Contrastive [Trajectory Analysis]" — extracted from the
   PDF as markdown-ish text with some OCR-style ligature artifacts — read past minor glyph noise.
2. `/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/wiki/images/02-fig2-taxonomy-page3-description.md`
   — a vision-model description of Figure 2 (the taxonomy figure), which belongs to this
   section. Use it to write about the figure without seeing the image.

## Output

Write the page to this exact absolute path:

`/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/wiki/03-skill-use-mechanisms.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Skill-Use Mechanisms: A Contrastive Trajectory Analysis

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <complete claim 1 — a real fact/mechanism/number, not a topic label>
- <complete claim 2>
- ... (5-8 bullets total, each standing alone as substance)

---

## <subsection(s) mirroring the chunk's own structure>

<full detail: the taxonomy of three high-level categories and twelve skill-use modes (name
them all if listed), the open-coding methodology (8,135 normalized trial records, 238 valid
unique labels from 240 open-coded records — exact numbers as given), and the logic of the
contrastive/paired trajectory analysis.>

## Figure: Taxonomy of Skill-Use Modes

![Taxonomy of skill-use categories and modes](images/02-fig2-taxonomy-page3.png)

<1-2 paragraphs describing what the figure shows, drawn from the description file>

**Covers:** Section 4 (Skill-Use Mechanisms) of arXiv 2608.14036, including Figure 2
```

Write in full prose paragraphs for the detail sections (not just more bullets). Include exact
numbers, category/mode names, and percentages verbatim where given. No line limit — be
thorough; do not compress the whole chunk into the Key points block alone.

## Definition of done

- Output file written at the exact path above, non-trivial (well over 40 lines), covering the
  chunk's ENTIRE content (not just its opening paragraphs), and embedding the figure exactly as
  shown above.
- No git commands — do not run git anything. `.ai` auto-syncs on its own.
- Touch ONLY the one output file. Do not run any fleet commands other than closing your own bead.
- When done: `bd close <own-id> --reason "chunk 03 extracted"`
