# Extract wiki page 01 — Introduction and Motivation

## Context is tight on this model

Read ONLY the one input file listed below. Nothing else. Do NOT read this task's own fleet
artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`,
`PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. If this is a retry,
do not try to diagnose the previous failure by reading logs; just re-read the input and write
directly.

## Input

- `/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/source/chunks/01.txt`
  (Title/abstract + Section 1 "Introduction" of the paper "Prime Agent: A Self-Improving RLM
  Harness", arXiv:2608.23552.)

There are no figures assigned to this chunk.

## Output

Write the full page to:
`/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/wiki/01-introduction-and-motivation.md`

**If this file already exists (a retry), overwrite it completely** — do not append or merge.

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Motivation

**In one sentence:** <the chapter's whole argument, in one sentence>

## Key points

- <complete claim 1 — a real fact/mechanism/number, not "discusses X">
- <complete claim 2>
- ... (5-8 bullets total, each a standalone claim someone could learn without reading further)

---

## <subsection headings mirroring the source's own structure>

<full detail: hierarchical ## subsections, exact numbers, verbatim terms/quotes where useful>

**Covers:** Title/Abstract, Section 1 (Introduction)
```

Rules:
- The `## Key points` bullets must each be a complete, standalone claim with real content
  (numbers, mechanisms, conclusions) — never a vague topic label like "discusses motivation".
- Use Obsidian `[[wikilink]]` syntax exactly as shown in the backlink line.
- No line limit — be thorough and cover the entire chunk, including its ending content, not
  just the opening paragraphs.
- Do not invent facts not present in the input file.

## Done condition

Output file written to the exact path above. Then `bd close <own-id> --reason "chunk 01 extracted"`.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet/git commands other than
`bd close`. No git commands — `.ai` auto-syncs on its own.
