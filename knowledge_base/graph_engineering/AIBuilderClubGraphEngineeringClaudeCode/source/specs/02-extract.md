# Extract wiki page 02: Wiring Your First Graph

## Context

This is a short article, not a book. Read ONLY the file below, nothing else. Do not read this
task's own fleet artifacts/log/event files, and do not read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. Context is tight on
this model.

## Input

Read this file in full (plain text, small):

1. `/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringClaudeCode/source/chunks/02.txt`

## Output

Write the file:

`/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringClaudeCode/wiki/02-wiring-your-first-graph.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Wiring Your First Graph

**In one sentence:** <one sentence capturing the chunk's whole point>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>

---

<## subsections with the full detail from the chunk, hierarchical, not flat prose.
Cover: the step-by-step recipe for wiring a first agent graph in Claude Code — pick a job that
actually splits (a produce step plus an independent check step: draft-then-review,
research-then-write, build-then-test), write one subagent per node with a narrow system prompt
and only the tools it needs (the reviewer should not have write access, the writer should not
search the web), let the orchestrator route between them including a loop-back edge when the
reviewer rejects, fan out multiple subagents in parallel when the work is genuinely parallel
(the same fan-out/fan-in move behind Anthropic's research system's speed), and add a hook for
any edge that must fire every time rather than one the model merely usually takes; the "when
not to reach for a graph" caution — every node must already be a loop that reliably ships on
its own, a graph of weak nodes is "slop produced in parallel," wiring three agents together
when one with a clear verifier already works just costs more tokens for nothing, and the
single loop should be nailed before wiring nodes together (citing that SEO/support functions
are typically converted before anything touching revenue because their output is cheap to
check); the Related Content list (Graph Engineering: The 2026 Guide, Agent Graph vs Loop: When
to Use Which, Is Graph Engineering Just LangGraph?, Loop Engineering Guide) with each item's
one-line description; the FAQ section in full (can you do graph engineering with Claude, what
are Claude Code subagents, is Claude Code a graph framework like LangGraph — and how it differs
by letting the orchestrating agent decide routing at runtime rather than declaring state/nodes/
edges explicitly with checkpointing, do you need the Claude Agent SDK to build a graph, how is
this different from just prompting harder); and the Sources & Verification list (Building
Effective Agents, How we built our multi-agent research system, Subagents — Claude Code
documentation, Graph Engineering Guide, Loop Engineering Guide — all from AI Builder Club /
Anthropic, verified July 2026).>

**Covers:** Step-by-step first-graph recipe (splittable job, one subagent per node, orchestrator
routing, fan-out/fan-in, hooks); when not to reach for a graph; Related Content; full FAQ;
Sources & Verification (source chunk 02)
```

Key points must be complete standalone claims (not topic labels like "explains FAQ") — someone
reading only the key points should have the chunk's substance. Preserve the FAQ content
faithfully rather than paraphrasing it away.

## DoD

1. Output file written at the path above.
2. `bd close <own-id> --reason "chunk 02 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
