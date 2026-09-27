# Task: Write wiki page 01 for "Loops vs. Graphs" (Prefect blog)

## Input
Read ONLY this file (absolute path):
`/Users/sergii/.ai/knowledge/research/PrefectLoopsVsGraphs/source/chunks/01.txt`

**Context is tight on this model — read ONLY the chunk file listed above, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Output
Write this file (absolute path), overwriting completely if it already exists (a retry):
`/Users/sergii/.ai/knowledge/research/PrefectLoopsVsGraphs/wiki/01-directed-agentic-graphs.md`

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Directed Agentic Graphs: From Prompts to Loops to Graphs

**In one sentence:** <the chunk's whole argument in one sentence>

## Key points

- <5-8 bullets, each a complete, standalone claim carrying real content (numbers,
  mechanisms, definitions, conclusions) — not a topic label like "discusses graphs">

---

## <## subsections mirroring the chunk's own section headings>

<Full detail: hierarchical prose under headings matching the chunk's structure
(graph fundamentals; the prompt->loop->graph progression; the Ralph loop; the
formal definition of a directed agentic graph — nodes, edges, cycles allowed,
per-node config; why businesses care more than individuals; the control-vs-autonomy
framing). Use exact terms, definitions, and the customer-lookup example from the
chunk. No tables or code needed here — this chunk is conceptual, not tabular.>

---

**Covers:** Sections "First, what even is a graph?" through "Control versus
autonomy, the central question" of the source article.
```

## Rules

- Cover the WHOLE chunk — including its last section ("Control versus autonomy"), not just the opening.
- No meta-commentary, no "as an AI", no repetition-loop padding. If you find yourself repeating a sentence, stop and move to the next section instead.
- Self-contained: a reader must understand this page without reading the other wiki page.
- Target ~60-100 lines.

## Done

1. Write the output file above.
2. `bd close <own-id> --reason "chunk 01 extracted"`

Scope: touch ONLY the one output file. Do not run any fleet/git commands other than `bd close`.
