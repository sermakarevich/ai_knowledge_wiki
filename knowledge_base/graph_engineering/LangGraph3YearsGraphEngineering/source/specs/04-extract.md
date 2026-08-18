# Extract wiki page: 04-whats-new-and-the-bigger-idea

## Problem
Write one wiki page from one chunk of the source article "3 Years of Graph Engineering with LangGraph" (Sydney Runkle, Harrison Chase, LangChain blog, July 22, 2026). This is the article's closing chunk.

## Input
Read ONLY this file: `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/source/chunks/04.txt`

Context is tight on this model — read ONLY that chunk file, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format below is the only convention you need. On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Output
Write exactly this file (create parent dirs if needed): `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/wiki/04-whats-new-and-the-bigger-idea.md`

If this file already exists (a retry), overwrite it completely.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# What's Actually New, and the Bigger Idea

**In one sentence:** <the chunk's whole argument, one sentence>

## Key points

- <complete claim: what changed is what you can put inside a node — a node can now be a full agent run>
- <complete claim: coding agents as the example of this shift>
- <complete claim: the deterministic-to-agentic scale — fixed steps, model steps, agent steps, each with what they are in the docs-agent example>
- <complete claim: graph engineering is not new — it is the latest name for a well-established approach>
- <complete claim: it is the same idea behind loop engineering and harness engineering — putting model reasoning in the right places, with the right context, at each step>

---

## What's actually new

<full detail prose, including the three-tier deterministic-to-agentic scale with its concrete examples (slack/linear operations, classifier/synthesize steps, reference-docs/conceptual-docs agents)>

## The bigger idea

<full detail prose, the closing argument tying graph engineering to loop engineering and harness engineering>

**Covers:** What's actually new; The bigger idea
```

Rules:
- The `## Key points` bullets must stand alone: someone reading only them gets the chunk's substance.
- Use two `##` subsections, not flat prose.
- No meta-commentary, no "as an AI", no repeating these instructions in the output.
- Preserve the three-tier example (fixed / model / agent steps) exactly as given — do not invent extra examples.

## DoD
1. Output file written at the exact path above, non-trivial (real prose, not a stub).
2. `bd close <own-id> --reason "chunk 04 extracted"`

## Scope & constraints
- Touch ONLY the one output file listed above.
- No git commands at all — this repo auto-syncs.
- Do not run any fleet commands other than `bd close`.
- Working directory: `/Users/sergii/.kb`
