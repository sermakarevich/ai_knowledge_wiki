# Extract wiki page 03: Practical guidance and industry shift

## Context

Read ONLY the file below, nothing else. Do not read this task's own fleet artifacts/log/
event files, and do not read sibling wiki pages "for style reference" — the format
contract below is the only convention you need. Context is tight on this model.

## Input

Read this file in full (plain text, small):

`/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/source/chunks/03.txt`

## Output

Write the file:

`/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/wiki/03-practical-guidance-and-industry-shift.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Practical Guidance and the Industry Shift

**In one sentence:** <one sentence capturing the chunk's whole point>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>

---

## When to keep it a loop vs. adopt a graph

Full detail on the "if the workflow is linear, keep it linear" guidance, the specific
added costs of graphs (state management, routing logic, harder debugging), and the three
conditions that justify the cost (parallel branches, independent verification, different
tools per step).

## The prompt-centric to system-centric shift

Full detail on how the article frames the graph-engineering debate as a proxy for a
larger architectural shift in AI development.

**Covers:** Practical guidance on graph adoption; prompt-centric vs. system-centric framing (source chunk 03)
```

Key points must be complete standalone claims (not topic labels) — someone reading only
the key points should have the chunk's substance.

## DoD

1. Output file written at the path above.
2. `bd close <own-id> --reason "chunk 03 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
