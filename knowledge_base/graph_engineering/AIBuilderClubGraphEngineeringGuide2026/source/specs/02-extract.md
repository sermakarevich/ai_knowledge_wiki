# Extract wiki page 02: When Should You Reach for a Graph?

## Context

This is a short article, not a book. Read ONLY the file below, nothing else. Do not read this
task's own fleet artifacts/log/event files, and do not read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. Context is tight on
this model.

## Input

Read this file in full (plain text, small):

`/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringGuide2026/source/chunks/02.txt`

## Output

Write the file:

`/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringGuide2026/wiki/02-when-to-use-a-graph.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# When Should You Reach for a Graph?

**In one sentence:** <one sentence capturing the chunk's whole point>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>

---

<## subsections with the full detail from the chunk, hierarchical, not flat prose.
Cover: the default answer ("you probably don't" need a graph — a single well-scoped task with
a clear verifier is a loop); the decision-table framing as triggers, not a checklist; the
over-engineered example ("Summarize this PDF" built as an unneeded five-node graph) contrasted
with the right-sized example (a daily market-brief pipeline with parallel research, synthesis,
writing, and a skeptical read-only reviewer node); the tell for whether a graph earns its keep
(can you collapse the nodes back into one loop and lose nothing?); the "Isn't this just
LangGraph?" concession — the prior art (LangGraph's StateGraph, Microsoft AutoGen's GraphFlow,
Google ADK's graph-based architecture and sequential/parallel/loop workflow agents, and the A2A
protocol for cross-team agent delegation) and what's actually new (a shared name for design
decisions those frameworks already required, not a new paradigm); and the 5-layers-of-AI-
engineering stack (prompt, context, harness, loop, graph — cumulative, not a ladder you climb
away from; weak lower layers make the graph fail in a more elaborate way).>

**Covers:** Decision framework for graphs vs. loops; over-engineered vs. right-sized examples;
LangGraph/AutoGen/ADK/A2A prior art; the 5-layer AI engineering stack (source chunk 02)
```

Key points must be complete standalone claims (not topic labels) — someone reading only the key
points should have the chunk's substance. Use precise wording for the decision-table triggers,
the two contrasting examples, and the specific framework names/claims (LangGraph, AutoGen
GraphFlow, Google ADK, A2A), since those are the chunk's most specific technical content.

## DoD

1. Output file written at the path above.
2. `bd close <own-id> --reason "chunk 02 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
