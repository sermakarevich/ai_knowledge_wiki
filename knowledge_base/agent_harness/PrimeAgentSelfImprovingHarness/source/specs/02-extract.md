# Extract wiki page 02 — Prime Agent Architecture

## Context is tight on this model

Read ONLY the input files listed below. Nothing else. Do NOT read this task's own fleet
artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`,
`PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. If this is a retry,
do not try to diagnose the previous failure by reading logs; just re-read the inputs and write
directly.

## Input

- `/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/source/chunks/02.txt`
  (Section 2 "Prime Agent Architecture" of the paper "Prime Agent: A Self-Improving RLM
  Harness", arXiv:2608.23552 — subsections 2.1 Architecture overview, 2.2 Information
  hierarchy and persistent state, 2.3 Programmatic computation with RLMs, 2.4 Recursive
  orchestration and interaction, 2.5 Continual Harness, 2.6 Long-horizon execution and
  evaluation semantics.)
- Figure descriptions (vision-model text, use to write informed figure captions):
  - `/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/wiki/images/fig1-overview-description.md`
  - `/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/wiki/images/fig2-state-hierarchy-description.md`
  - `/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/wiki/images/fig3-orchestration-lifecycle-description.md`
  - `/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/wiki/images/fig4-long-horizon-control-description.md`

## Output

Write the full page to:
`/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/wiki/02-prime-agent-architecture.md`

**If this file already exists (a retry), overwrite it completely** — do not append or merge.

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Prime Agent Architecture

**In one sentence:** <the whole architecture's job, in one sentence>

## Key points

- <complete claim 1 — a real fact/mechanism/number, not "discusses X">
- <complete claim 2>
- ... (5-8 bullets total, each a standalone claim)

---

## Architecture overview (2.1)

...

## Information hierarchy and persistent state (2.2)

...
![Prime Agent state hierarchy](images/fig2-state-hierarchy.png)
<one-sentence caption grounded in the figure description file>

## Programmatic computation with RLMs (2.3)

...

## Recursive orchestration and interaction (2.4)

...
![Multi-agent orchestration lifecycle](images/fig3-orchestration-lifecycle.png)
<one-sentence caption grounded in the figure description file>

## Continual Harness (2.5)

...

## Long-horizon execution and evaluation semantics (2.6)

...
![Long-horizon control mechanisms](images/fig4-long-horizon-control.png)
<one-sentence caption grounded in the figure description file>

**Covers:** Section 2 (2.1-2.6), Figures 1-4
```

Rules:
- Also embed `![Prime Agent overview](images/fig1-overview.png)` near the top of the
  architecture-overview subsection (2.1) — it is the overall system diagram.
- Every one of the 4 figures (fig1, fig2, fig3, fig4) MUST be embedded with `![...](images/<file>.png)`
  at the point in the text that discusses it — this is mandatory, not optional. Use the
  matching `-description.md` file's content to write an accurate one-sentence caption; do not
  guess what the figure shows.
- The `## Key points` bullets must each be a complete, standalone claim with real content
  (numbers, mechanisms, conclusions) — never a vague topic label.
- Use Obsidian `[[wikilink]]` syntax exactly as shown in the backlink line.
- No line limit — be thorough; cover all six subsections (2.1-2.6), not just the first two.
- Do not invent facts not present in the input files.

## Done condition

Output file written to the exact path above. Then `bd close <own-id> --reason "chunk 02 extracted"`.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet/git commands other than
`bd close`. No git commands — `.ai` auto-syncs on its own.
