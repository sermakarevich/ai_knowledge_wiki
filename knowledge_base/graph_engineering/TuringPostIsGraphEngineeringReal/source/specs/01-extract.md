# Extract wiki page 01: Core argument and definitions

## Context

is not part of a book — it's a short article. Read ONLY the file below, nothing else.
Do not read this task's own fleet artifacts/log/event files, and do not read sibling wiki
pages "for style reference" — the format contract below is the only convention you need.
Context is tight on this model.

## Input

Read this file in full (plain text, small):

`/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/source/chunks/01.txt`

## Output

Write the file:

`/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/wiki/01-core-argument-and-definitions.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Core Argument and Definitions

**In one sentence:** <one sentence capturing the chunk's whole point>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>

---

<## subsections with the full detail from the chunk, hierarchical, not flat prose.
Include the loop definition, the graph definition (nodes/edges/state), and the framing
of graph-as-loop-with-branches, in full detail from the chunk text.>

**Covers:** Core argument; loop vs. graph definitions (source chunk 01)
```

Key points must be complete standalone claims (not topic labels like "discusses loops") —
someone reading only the key points should have the chunk's substance. Use exact wording
close to the source where it states a definition (loop, graph, node, edge, state) so the
definitions are precise.

## DoD

1. Output file written at the path above.
2. `bd close <own-id> --reason "chunk 01 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
