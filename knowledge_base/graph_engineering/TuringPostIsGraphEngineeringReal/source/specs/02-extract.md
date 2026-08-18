# Extract wiki page 02: Four graph types and fact-check

## Context

Read ONLY the file below, nothing else. Do not read this task's own fleet artifacts/log/
event files, and do not read sibling wiki pages "for style reference" — the format
contract below is the only convention you need. Context is tight on this model.

## Input

Read this file in full (plain text, small):

`/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/source/chunks/02.txt`

## Output

Write the file:

`/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/wiki/02-four-graph-types-and-fact-check.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Four Graph Types and Fact-Check

**In one sentence:** <one sentence capturing the chunk's whole point>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>
- <complete-claim bullet 6>

---

## The four graph types

A table with columns Type | Purpose | Example, listing all four types (control graph,
knowledge graph, execution trace, improvement graph) exactly as given in the source chunk.

## Fact-check of viral claims

Full detail on both debunked claims (the "Microsoft/Stanford/Anthropic adopted graph
engineering" claim and the "18% accuracy / 85% cost reduction" claim), including the
article's specific rebuttal reasoning for each.

**Covers:** Four graph types; fact-check of viral adoption and performance claims (source chunk 02)
```

Key points must be complete standalone claims (not topic labels) — someone reading only
the key points should have the chunk's substance, including that both viral claims were
debunked and why.

## DoD

1. Output file written at the path above.
2. `bd close <own-id> --reason "chunk 02 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
