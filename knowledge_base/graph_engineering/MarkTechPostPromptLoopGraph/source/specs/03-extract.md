# Extract wiki page 03: Decision framework and numbers

## Context

This is a short article, not a book. Read ONLY the file below, nothing else. Do not read this
task's own fleet artifacts/log/event files, and do not read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. Context is tight on
this model.

## Input

Read this file in full (plain text, small):

`/Users/sergii/.kb/papers/MarkTechPostPromptLoopGraph/source/chunks/03.txt`

## Output

Write the file:

`/Users/sergii/.kb/papers/MarkTechPostPromptLoopGraph/wiki/03-decision-framework-and-numbers.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Decision Framework and Numbers

**In one sentence:** <one sentence capturing the chunk's whole point>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>

---

<## subsections with the full detail from the chunk, hierarchical, not flat prose.
Cover: the four-question ordered checklist for picking a layer (with the "first no wins"
rule), the composition claim (loops are prompts with scaffolding, graphs are built from
loops), the closing caution about operator skill vs. architecture, the headline cost/
performance numbers (+90% eval gain at ~15x token cost, ~80% variance explained by token
spend), and a short list of the sources the article cites.>

**Covers:** Decision checklist for choosing a layer; headline numbers; cited sources (source
chunk 03)
```

Key points must be complete standalone claims (not topic labels) — someone reading only the
key points should have the chunk's substance. Preserve the four checklist questions and the
cited numbers exactly as given in the chunk.

## DoD

1. Output file written at the path above.
2. `bd close <own-id> --reason "chunk 03 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
