# Extract wiki page: 01-modeling-agents-as-graphs

## Problem
Write one wiki page from one chunk of the source article "3 Years of Graph Engineering with LangGraph" (Sydney Runkle, Harrison Chase, LangChain blog, July 22, 2026).

## Input
Read ONLY this file: `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/source/chunks/01.txt`

Context is tight on this model — read ONLY that chunk file, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format below is the only convention you need. On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Output
Write exactly this file (create parent dirs if needed): `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/wiki/01-modeling-agents-as-graphs.md`

If this file already exists (a retry), overwrite it completely.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Modeling Agents as Graphs

**In one sentence:** <the chunk's whole argument, one sentence>

## Key points

- <complete claim, not a topic label>
- <complete claim>
- <complete claim>
- <complete claim>
- <complete claim>

---

## <subsection mirroring the chunk's own structure>

<full detail prose, hierarchical ## subsections mirroring "Modeling agents as graphs" and "When to represent agents as graphs">

**Covers:** Modeling agents as graphs; When to represent agents as graphs
```

Rules:
- The `## Key points` bullets must stand alone: someone reading only them gets the chunk's substance.
- Use hierarchical `##` subsections below the `---`, not flat prose.
- No meta-commentary, no "as an AI", no repeating these instructions in the output.
- Cover the WHOLE chunk, including its final paragraph/example (the knowledge-base agent example) — not just the opening.

## DoD
1. Output file written at the exact path above, non-trivial (real prose, not a stub).
2. `bd close <own-id> --reason "chunk 01 extracted"`

## Scope & constraints
- Touch ONLY the one output file listed above.
- No git commands at all — this repo auto-syncs.
- Do not run any fleet commands other than `bd close`.
- Working directory: `/Users/sergii/.kb`
