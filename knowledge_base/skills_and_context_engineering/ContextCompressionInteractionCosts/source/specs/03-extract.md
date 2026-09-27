# Task: write wiki page 03 — Experiments & Results

## Input

Read ONLY these files:
- `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/source/chunks/03.txt`
- `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/wiki/images/03-fig2-reacquisition-cost-description.md`
- `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/wiki/images/03-fig3-two-axes-description.md`
- `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/wiki/images/03-fig4-retention-interventions-description.md`
- `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/wiki/images/03-fig5-external-environment-description.md`
- `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/wiki/images/03-fig6-oracle-conditions-description.md`

(These are vision-model descriptions of Figures 2-6, referenced in the chunk.)

Context is tight on this model — read ONLY the six files listed above, nothing else. Do NOT
read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`,
`events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling
wiki pages "for style/convention reference" — the format contract below is the only
convention needed. If this is a retry, do not diagnose the prior failure by reading logs;
just re-read the six input files and write directly.

## Output

Write the wiki page to: `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/wiki/03-experiments-and-results.md`

If this file already exists (a retry), overwrite it completely.

The image files already exist — do NOT create or move them. Reference each with a relative
path at the point where the corresponding figure is discussed:
- `images/03-fig2-reacquisition-cost.png` (Figure 2)
- `images/03-fig3-two-axes.png` (Figure 3)
- `images/03-fig4-retention-interventions.png` (Figure 4)
- `images/03-fig5-external-environment.png` (Figure 5)
- `images/03-fig6-oracle-conditions.png` (Figure 6)

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments & Results

**In one sentence:** <the whole argument of this section, one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total, each carrying real content: numbers, p-values, mechanisms, conclusions>

---

## <subsection mirroring the source's own structure, e.g. setup, models/regimes, main results,
retention interventions, ALFWorld environment, statistical tests>

<hierarchical detail, tables reproducing the numeric results, exact numbers and p-values>

![Figure 2: <short caption>](images/03-fig2-reacquisition-cost.png)

<a 2-4 sentence caption paragraph based on the vision description file, placed right after
the image, at the point in the text where Figure 2 is first discussed>

## <another subsection, repeat the embed-with-caption pattern for Figures 3-6 at the point
each is discussed>

...

**Covers:** Section 4 (Experiments)
```

## Rules

- The page must cover the ENTIRE chunk — including the last subsection (statistical
  significance / termination reasons), not just the opening.
- Key points must stand alone: someone who reads only them has the section's substance.
- Use exact numbers/p-values from the source, do not paraphrase away specifics. Reproduce
  key results as markdown tables where the source has tabular data.
- All five figures (2-6) must actually be embedded (not just named) at the point each is
  discussed — this is a hard requirement, do not skip any of them.
- No meta-commentary about this being an extraction task; write the page itself only.

## Scope & constraints

Touch ONLY the one output file listed above (do not touch the image files). Do not run any
fleet commands other than `bd close`. Do not run any git commands — this KB auto-syncs, do
not `git add`/`git commit`.

## Definition of Done

1. Output file written at the path above, following the format contract, with all five
   figures (2-6) embedded.
2. `bd close <own-id> --reason "chunk 03 extracted"`
