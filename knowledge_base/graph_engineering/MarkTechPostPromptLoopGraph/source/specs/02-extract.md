# Extract wiki page 02: The graph layer

## Context

This is a short article, not a book. Read ONLY the file below, nothing else. Do not read this
task's own fleet artifacts/log/event files, and do not read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. Context is tight on
this model.

## Input

Read this file in full (plain text, small):

`/Users/sergii/.kb/papers/MarkTechPostPromptLoopGraph/source/chunks/02.txt`

## Output

Write the file:

`/Users/sergii/.kb/papers/MarkTechPostPromptLoopGraph/wiki/02-graph-layer.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Graph Layer

**In one sentence:** <one sentence capturing the chunk's whole point>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>

---

<## subsections with the full detail from the chunk, hierarchical, not flat prose.
Cover: the two-graphs claim (org graph vs. work graph, what each answers), the skepticism
about the term's novelty (LangGraph precedent, Anthropic's earlier workflow patterns), what
the article says is actually new (shared vocabulary for nodes/edges/state), and the
edge-carries-state failure mode called out explicitly.>

**Covers:** The graph layer — org graph vs. work graph, novelty skepticism, the edge/state
failure mode (source chunk 02)
```

Key points must be complete standalone claims (not topic labels) — someone reading only the
key points should have the chunk's substance. Preserve the org-graph/work-graph distinction
precisely, since it is the chunk's central technical claim.

## DoD

1. Output file written at the path above.
2. `bd close <own-id> --reason "chunk 02 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
