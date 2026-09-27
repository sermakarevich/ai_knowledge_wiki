# Task: Write wiki page 02 for "Loops vs. Graphs" (Prefect blog)

## Input
Read ONLY this file (absolute path):
`/Users/sergii/.ai/knowledge/research/PrefectLoopsVsGraphs/source/chunks/02.txt`

**Context is tight on this model — read ONLY the chunk file listed above, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Output
Write this file (absolute path), overwriting completely if it already exists (a retry):
`/Users/sergii/.ai/knowledge/research/PrefectLoopsVsGraphs/wiki/02-security-humans-and-strategy.md`

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Security, Human Checkpoints, and Prefect's Strategic Bet

**In one sentence:** <the chunk's whole argument in one sentence>

## Key points

- <5-8 bullets, each a complete, standalone claim carrying real content (numbers,
  mechanisms, definitions, conclusions) — not a topic label>

---

## <## subsections mirroring the chunk's own section headings>

<Full detail: hierarchical prose under headings matching the chunk's structure
(the refund-agent "bazooka" example and capability segregation by decision path;
humans-in-the-loop modeled as ordinary graph nodes; how directed agentic graphs
relate to LangGraph/Pydantic AI (macro multi-agent orchestration vs. single-agent
internals); the Peter Steinberger tweet this piece responds to and Prefect's
"boring way that works" framing; the Dagster acquisition and the 95%/5% established-
vs-new-practice framing; the PyData London talk and closing call for engagement).
Use exact terms and the refund-agent example from the chunk. No tables or code
needed — this chunk is conceptual, not tabular.>

---

**Covers:** Sections "Don't hand your agent a bazooka" through "Wrapping up" of
the source article. (Omit the page's generic product call-to-action boilerplate —
it is marketing, not article content.)
```

## Rules

- Cover the WHOLE chunk — including its last section ("Wrapping up"), not just the opening.
- No meta-commentary, no "as an AI", no repetition-loop padding. If you find yourself repeating a sentence, stop and move to the next section instead.
- Self-contained: a reader must understand this page without reading the other wiki page.
- Target ~60-100 lines.

## Done

1. Write the output file above.
2. `bd close <own-id> --reason "chunk 02 extracted"`

Scope: touch ONLY the one output file. Do not run any fleet/git commands other than `bd close`.
