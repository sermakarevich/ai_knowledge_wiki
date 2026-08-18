# Extract wiki page 01: What Is Graph Engineering?

## Context

This is a short article, not a book. Read ONLY the files below, nothing else. Do not read this
task's own fleet artifacts/log/event files, and do not read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. Context is tight on
this model.

## Input

Read these files in full (plain text, small):

1. `/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringGuide2026/source/chunks/01.txt`
2. `/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringGuide2026/wiki/images/01-description.md`
   (a figure description — reference it where the chunk text mentions the starter diagram)

## Output

Write the file:

`/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringGuide2026/wiki/01-what-is-graph-engineering.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# What Is Graph Engineering?

**In one sentence:** <one sentence capturing the chunk's whole point>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>

---

<## subsections with the full detail from the chunk, hierarchical, not flat prose.
Cover: the definition of graph engineering (nodes/edges/state; graph engineering designs how
loops connect, loop engineering designs the cycle inside one node); the three things it is
NOT (not knowledge graphs/GraphRAG, not a new capability, not a default); the X-thread origin
of the term in mid-July 2026 (Peter Steinberger's question, @svpino, @rohit4verse,
@VaibhavSisinty quotes, and the point that nothing new *shipped* — only the vocabulary is new);
the three parts of an agent graph (nodes, edges — straight/conditional/fan-out/fan-in, and
shared state); the org-chart metaphor from @rohit4verse and its limits (when roles are real
business functions, most teams don't need edges); the starter diagram (Researcher → Writer →
Reviewer, with a conditional "pass"/"reject: loop back" edge) — embed it with
`![Starter agent graph](images/01-agent-graph-starter-diagram.png)` and describe what it shows
using the figure description file; and the closing point that a loop is a single-node graph
with an edge back to itself, so a graph is what you get when several loops need to hand off to
each other.>

**Covers:** Definition of graph engineering; what it's not; the term's July 2026 origin on X;
nodes/edges/state mechanics; the org-chart metaphor; the starter diagram (source chunk 01)
```

Key points must be complete standalone claims (not topic labels like "discusses graphs") —
someone reading only the key points should have the chunk's substance. Use precise wording for
the nodes/edges/state definitions and the "loop is a single-node graph" claim, since those are
the chunk's most specific technical content.

## DoD

1. Output file written at the path above, with the figure embedded as instructed.
2. `bd close <own-id> --reason "chunk 01 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
