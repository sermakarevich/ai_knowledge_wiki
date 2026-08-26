# Extract: 01-introduction-and-benchmark-design

## Context is tight — read ONLY these files, nothing else

- Input chunk text: `/Users/sergii/.kb/papers/SignalOrNoiseAgentSkills/source/chunks/01.txt`

Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`,
`task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention
reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose
the prior failure by reading logs; just re-read the chunk and write directly.

## Task

Read the chunk text (extracted from an academic paper, "Signal or Noise? A Benchmark Study of Agent Skills
in Web Development", arXiv:2608.23067). This chunk covers: Abstract, Section 1 Introduction, Section 2
Related Work, Section 3 Benchmark Design (the WebDev-Skills-Bench methodology: task corpus, Skill suite,
routing protocol, and the four experimental conditions C0/C1/C2/C3).

Write ONE wiki page to:

`/Users/sergii/.kb/papers/SignalOrNoiseAgentSkills/wiki/01-introduction-and-benchmark-design.md`

**If this file already exists (a retry), overwrite it completely.**

## Output format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Benchmark Design

**In one sentence:** <the chapter's whole argument, one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (numbers, mechanisms, definitions) — not "discusses X">

---

## <subsection headings mirroring the chunk's own structure>

<hierarchical detail. Include exact numbers, the definitions of conditions C0/C1/C2/C3, the benchmark's
scale (31 Skills, 50 projects, 1,000 tasks, 117 core pairs), and how the workspace-aware injection
protocol works (SKILL.md only in prompt, auxiliary files mounted to filesystem). Use tables where the
source has tabular data.>

**Covers:** Abstract, Section 1 (Introduction), Section 2 (Related Work), Section 3 (Benchmark Design)
```

No figures belong on this page — do not add an images section.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other than `bd close`.

## DoD

1. Output file written at the exact path above, following the format contract.
2. `bd close <own-id> --reason "chunk 01 extracted"`
