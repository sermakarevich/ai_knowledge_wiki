# Task: write wiki page 02 — Method

## Input

Read ONLY these files:
- `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/source/chunks/02.txt`
- `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/wiki/images/02-fig1-measurement-protocol-description.md` (a vision-model description of Figure 1, referenced in the chunk)

Context is tight on this model — read ONLY the two files listed above, nothing else. Do NOT
read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`,
`events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling
wiki pages "for style/convention reference" — the format contract below is the only
convention needed. If this is a retry, do not diagnose the prior failure by reading logs;
just re-read the two input files and write directly.

## Output

Write the wiki page to: `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/wiki/02-method.md`

If this file already exists (a retry), overwrite it completely.

Copy the image file `wiki/images/02-fig1-measurement-protocol.png` — it already exists, do
NOT create or move it. Just reference it with a relative path `images/02-fig1-measurement-protocol.png`
in the page at the point where "Figure 1" is discussed, using the vision description as your
caption source.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Method

**In one sentence:** <the whole argument of this section, one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total, each carrying real content: numbers, mechanisms, conclusions>

---

## <subsection mirroring the source's own structure, e.g. protocol, compression operators, retrieval/execution decomposition, oracle interventions>

<hierarchical detail, tables, exact numbers, verbatim definitions/formulas where useful>

![Figure 1: measurement protocol overview](images/02-fig1-measurement-protocol.png)

<a 2-4 sentence caption paragraph based on the vision description file, placed right after
the image, at the point in the text where Figure 1 is first discussed>

## <another subsection>

...

**Covers:** Section 3 (Method)
```

## Rules

- The page must cover the ENTIRE chunk — including the last subsection, not just the opening.
- Key points must stand alone: someone who reads only them has the section's substance.
- Use exact numbers/terms/formulas from the source, do not paraphrase away specifics.
- The figure must actually be embedded (not just named) at the point it is discussed.
- No meta-commentary about this being an extraction task; write the page itself only.

## Scope & constraints

Touch ONLY the one output file listed above (do not touch the image files). Do not run any
fleet commands other than `bd close`. Do not run any git commands — this KB auto-syncs, do
not `git add`/`git commit`.

## Definition of Done

1. Output file written at the path above, following the format contract, with Figure 1 embedded.
2. `bd close <own-id> --reason "chunk 02 extracted"`
