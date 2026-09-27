# Task: write wiki page 04 — Discussion & Limitations

## Input

Read ONLY this file: `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/source/chunks/04.txt`

This chunk covers Section 5 (Discussion), Section 6 (Limitations), the Appendix
(Seed-level association), Acknowledgments, and References.

Context is tight on this model — read ONLY the chunk file listed above, nothing else. Do NOT
read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`,
`events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling
wiki pages "for style/convention reference" — the format contract below is the only
convention needed. If this is a retry, do not diagnose the prior failure by reading logs;
just re-read the chunk and write directly.

There are no figures in this chunk.

## Output

Write the wiki page to: `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/wiki/04-discussion-and-limitations.md`

If this file already exists (a retry), overwrite it completely.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Discussion & Limitations

**In one sentence:** <the whole argument of this section, one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total, each carrying real content: numbers, mechanisms, conclusions>

---

## <subsection mirroring the source's own structure, e.g. what the protocol measures,
implications, limitations, seed-level association appendix>

<hierarchical detail, exact numbers, verbatim claims where useful>

## <another subsection>

...

**Covers:** Section 5 (Discussion), Section 6 (Limitations), Appendix A (Seed-level association)
```

## Rules

- The page must cover the ENTIRE chunk, including the appendix — not just the Discussion
  section at the top.
- Key points must stand alone: someone who reads only them has the section's substance.
- Use exact numbers/terms from the source, do not paraphrase away specifics.
- You do NOT need to reproduce the References list — summarize in one line that references
  are omitted from the wiki page, if relevant.
- No meta-commentary about this being an extraction task; write the page itself only.

## Scope & constraints

Touch ONLY the one output file listed above. Do not run any fleet commands other than
`bd close`. Do not run any git commands — this KB auto-syncs, do not `git add`/`git commit`.

## Definition of Done

1. Output file written at the path above, following the format contract.
2. `bd close <own-id> --reason "chunk 04 extracted"`
