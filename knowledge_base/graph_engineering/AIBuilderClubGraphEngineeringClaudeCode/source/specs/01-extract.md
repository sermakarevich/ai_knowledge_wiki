# Extract wiki page 01: Claude Code as a Graph Engine

## Context

This is a short article, not a book. Read ONLY the file below, nothing else. Do not read this
task's own fleet artifacts/log/event files, and do not read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. Context is tight on
this model.

## Input

Read this file in full (plain text, small):

1. `/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringClaudeCode/source/chunks/01.txt`

## Output

Write the file:

`/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringClaudeCode/wiki/01-claude-code-as-a-graph-engine.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not
append or merge with old content.

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Claude Code as a Graph Engine

**In one sentence:** <one sentence capturing the chunk's whole point>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5>

---

<## subsections with the full detail from the chunk, hierarchical, not flat prose.
Cover: the framing that "graph engineering with Claude" does not require a new framework
because Claude Code already ships the primitives, and that Anthropic's "Building Effective
Agents" five patterns (prompt chaining, routing, parallelization, orchestrator-workers,
evaluator-optimizer) are graphs under a plainer name — orchestrator-workers being a graph in
all but name; the three-part mapping of graph concepts onto Claude Code — nodes → subagents
(separate context window, own system prompt, scoped tool access), edges → the orchestrator's
runtime routing decisions (dynamic, not hand-drawn), shared state → a subagent's returned
result flowing back to the orchestrator; the three primitives in order of commitment —
subagents defined as markdown files with YAML frontmatter in `.claude/agents/` (fastest,
version-controlled by default), hooks as deterministic/guaranteed edges (vs. "the agent
usually does X"), and the Claude Agent SDK's `agents` parameter for programmatic, unattended,
testable graphs; the "hand-roll first, then lift into the SDK" ordering and why reaching for
the SDK too early means debugging orchestration you never watched work; and Anthropic's own
multi-agent research system as proof this already ships — a lead agent (orchestrator node)
spinning up parallel subagents (worker nodes) plus a citation pass, reporting a 90.2%
improvement over a single-agent Claude Opus 4 baseline on an internal research eval, at
roughly 15x the token cost of a normal chat turn, with early orchestrator versions
over-spawning subagents for simple questions — the real tradeoff being quality/parallelism
bought with tokens and coordination overhead, which only pays off when the job genuinely has
separable parts.>

**Covers:** What "graph engineering with Claude" means; nodes/edges/state mapped onto
subagents/orchestrator routing/returned results; the three primitives (subagents, hooks, Claude
Agent SDK) and hand-roll-then-lift ordering; Anthropic's orchestrator-workers system as existing
proof (90.2% improvement, 15x tokens, over-spawn failure mode) (source chunk 01)
```

Key points must be complete standalone claims (not topic labels like "discusses subagents") —
someone reading only the key points should have the chunk's substance. Preserve exact numbers
(90.2%, 15x) verbatim.

## DoD

1. Output file written at the path above.
2. `bd close <own-id> --reason "chunk 01 extracted"`

## Scope & constraints

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than `bd close`.
- No git commands — this repo auto-syncs.
