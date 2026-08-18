# Extract wiki page: 03-lessons-from-three-years

## Problem
Write one wiki page from one chunk of the source article "3 Years of Graph Engineering with LangGraph" (Sydney Runkle, Harrison Chase, LangChain blog, July 22, 2026).

## Input
Read ONLY this file: `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/source/chunks/03.txt`

Context is tight on this model — read ONLY that chunk file, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format below is the only convention you need. On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Output
Write exactly this file (create parent dirs if needed): `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/wiki/03-lessons-from-three-years.md`

If this file already exists (a retry), overwrite it completely.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Lessons from Three Years of Building LangGraph

**In one sentence:** <the chunk's whole argument, one sentence>

## Key points

- <complete claim covering: agent graphs are usually not DAGs>
- <complete claim covering: why (cycles: retries, missing info, revision, repeated tool calls, human-in-the-loop pauses)>
- <complete claim covering: loops are simple graphs (David Khourshid's "a loop is just a directed, cyclic graph"; LangChain framework built on LangGraph)>
- <complete claim covering: dynamic transitions matter>
- <complete claim covering: the `Send` mechanism and why it exists (map-reduce, unknown worker count in advance)>
- <complete claim covering: known structure mixed with runtime variability, with an example>

---

## First: agent graphs are usually not DAGs

<full detail prose>

## Second: loops are simple graphs

<full detail prose>

## Third: dynamic transitions matter

<full detail prose, including the Send mechanism and the map-reduce example>

**Covers:** What building LangGraph taught us (three lessons: not DAGs, loops are simple graphs, dynamic transitions)
```

Rules:
- The `## Key points` bullets must stand alone: someone reading only them gets the chunk's substance.
- Use three `##` subsections (one per lesson), not flat prose.
- No meta-commentary, no "as an AI", no repeating these instructions in the output.
- Cover the WHOLE chunk including the closing paragraph about mixing known structure with runtime variability — do not stop after the first lesson.

## DoD
1. Output file written at the exact path above, non-trivial (real prose, not a stub).
2. `bd close <own-id> --reason "chunk 03 extracted"`

## Scope & constraints
- Touch ONLY the one output file listed above.
- No git commands at all — this repo auto-syncs.
- Do not run any fleet commands other than `bd close`.
- Working directory: `/Users/sergii/.kb`
