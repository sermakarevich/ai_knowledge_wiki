# Extract wiki page 01: Prompt and loop layers

## Context

This is a short article, not a book. Read ONLY the file below, nothing else. Do not read this
task's own fleet artifacts/log/event files, and do not read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. Context is tight on
this model.

## Input

Read this file in full (plain text, small):

`/Users/sergii/.kb/papers/MarkTechPostPromptLoopGraph/source/chunks/01.txt`

## Output

Write the file:

`/Users/sergii/.kb/papers/MarkTechPostPromptLoopGraph/wiki/01-prompt-and-loop-layers.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Prompt and Loop Layers

**In one sentence:** <one sentence capturing the chunk's whole point>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>

---

<## subsections with the full detail from the chunk, hierarchical, not flat prose.
Cover: the gist of the three-layer stack (prompt/loop/graph as nested units of control),
why layers get added (breakdown of manual review at volume/multi-step/no-grader conditions),
the loop layer's building blocks (automations, worktrees, skills, connectors, checker
sub-agent, external state), and the loop layer's central thesis about the stop condition.>

**Covers:** Gist of the three-layer stack; the prompt layer; the loop layer and its building
blocks and stop-condition thesis (source chunk 01)
```

Key points must be complete standalone claims (not topic labels like "discusses loops") —
someone reading only the key points should have the chunk's substance. Use precise wording for
the loop-layer building blocks and the stop-condition concept, since those are the chunk's
most specific technical content.

## DoD

1. Output file written at the path above.
2. `bd close <own-id> --reason "chunk 01 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
