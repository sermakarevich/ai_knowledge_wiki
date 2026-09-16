# Extract wiki page 03 — ARC-AGI-3 and Long-Context Evaluation

## Context is tight on this model

Read ONLY the input files listed below. Nothing else. Do NOT read this task's own fleet
artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`,
`PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. If this is a retry,
do not try to diagnose the previous failure by reading logs; just re-read the inputs and write
directly.

## Input

- `/Users/sergii/.ai/knowledge/papers/PrimeAgentSelfImprovingHarness/source/chunks/03.txt`
  (Start of Section 3 "Evaluation" — the RQ1/RQ2/RQ3 framing — plus subsections 3.1
  "Interactive reasoning at test-time scale" (ARC-AGI-3 results) and 3.2 "Long-context
  information management", from the paper "Prime Agent: A Self-Improving RLM Harness",
  arXiv:2608.23552.)
- Figure description (vision-model text):
  - `/Users/sergii/.ai/knowledge/papers/PrimeAgentSelfImprovingHarness/wiki/images/fig5-arc-agi3-scaling-description.md`

## Output

Write the full page to:
`/Users/sergii/.ai/knowledge/papers/PrimeAgentSelfImprovingHarness/wiki/03-arc-agi3-and-long-context-evaluation.md`

**If this file already exists (a retry), overwrite it completely** — do not append or merge.

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# ARC-AGI-3 and Long-Context Evaluation

**In one sentence:** <the chapter's whole argument, in one sentence>

## Key points

- <complete claim 1 — a real fact/mechanism/number, not "discusses X">
- <complete claim 2>
- ... (5-8 bullets total, each a standalone claim)

---

## Research questions

<summarize RQ1, RQ2, RQ3 as framed in the source>

## Interactive reasoning at test-time scale (3.1, ARC-AGI-3)

...
![ARC-AGI-3 test-time scaling](images/fig5-arc-agi3-scaling.png)
<one-sentence caption grounded in the figure description file>

## Long-context information management (3.2)

<include the long-context results table if numbers are present in the source text>

**Covers:** Section 3 intro, 3.1, 3.2, Figure 5
```

Rules:
- Figure 5 MUST be embedded with `![...](images/fig5-arc-agi3-scaling.png)` at the point that
  discusses ARC-AGI-3 scaling — this is mandatory. Use the `-description.md` file's content to
  write an accurate one-sentence caption; do not guess what the figure shows.
- If the source text contains a results table (e.g. long-context comparison numbers), render
  it as a markdown table with exact numbers — do not paraphrase numeric results into prose.
- The `## Key points` bullets must each be a complete, standalone claim with real content
  (numbers, mechanisms, conclusions) — never a vague topic label.
- Use Obsidian `[[wikilink]]` syntax exactly as shown in the backlink line.
- No line limit — be thorough; cover both 3.1 and 3.2 fully, not just 3.1.
- Do not invent facts not present in the input files.

## Done condition

Output file written to the exact path above. Then `bd close <own-id> --reason "chunk 03 extracted"`.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet/git commands other than
`bd close`. No git commands — `.ai` auto-syncs on its own.
