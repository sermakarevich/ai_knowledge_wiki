# Extract wiki page 05 — Persistent Refinement, Related Work, and Conclusion

## Context is tight on this model

Read ONLY the input files listed below. Nothing else. Do NOT read this task's own fleet
artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`,
`PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. If this is a retry,
do not try to diagnose the previous failure by reading logs; just re-read the inputs and write
directly.

## Input

- `/Users/sergii/.ai/knowledge/papers/PrimeAgentSelfImprovingHarness/source/chunks/05.txt`
  (Subsection 3.5 "Persistent interaction and refinement" (Factorio, MazeBench), Section 4
  "Related Work", and Section 5 "Conclusion" of the paper "Prime Agent: A Self-Improving RLM
  Harness", arXiv:2608.23552.)
- Figure descriptions (vision-model text):
  - `/Users/sergii/.ai/knowledge/papers/PrimeAgentSelfImprovingHarness/wiki/images/fig9-factorio-progress-description.md`
  - `/Users/sergii/.ai/knowledge/papers/PrimeAgentSelfImprovingHarness/wiki/images/fig10-mazebench-description.md`

## Output

Write the full page to:
`/Users/sergii/.ai/knowledge/papers/PrimeAgentSelfImprovingHarness/wiki/05-persistent-refinement-related-work-conclusion.md`

**If this file already exists (a retry), overwrite it completely** — do not append or merge.

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Persistent Refinement, Related Work, and Conclusion

**In one sentence:** <the chapter's whole argument, in one sentence>

## Key points

- <complete claim 1 — a real fact/mechanism/number, not "discusses X">
- <complete claim 2>
- ... (5-8 bullets total, each a standalone claim)

---

## Persistent interaction and refinement (3.5)

### Factorio

...
![Factorio progress and recursive computation](images/fig9-factorio-progress.png)
<one-sentence caption grounded in the figure description file>

### MazeBench

...
![MazeBench exploration versus cost](images/fig10-mazebench.png)
<one-sentence caption grounded in the figure description file>

## Related Work (Section 4)

...

## Conclusion (Section 5)

...

**Covers:** Section 3.5, Section 4 (Related Work), Section 5 (Conclusion), Figures 9, 10
```

Rules:
- Figure 9 MUST be embedded with `![...](images/fig9-factorio-progress.png)` in the Factorio
  subsection, and Figure 10 MUST be embedded with `![...](images/fig10-mazebench.png)` in the
  MazeBench subsection — this is mandatory. Use the `-description.md` files' content to write
  accurate captions; do not guess what the figures show.
- The `## Key points` bullets must each be a complete, standalone claim with real content
  (numbers, mechanisms, conclusions) — never a vague topic label.
- Use Obsidian `[[wikilink]]` syntax exactly as shown in the backlink line.
- No line limit — be thorough; cover the Related Work and Conclusion sections too, not just
  Factorio and MazeBench.
- Do not invent facts not present in the input files.

## Done condition

Output file written to the exact path above. Then `bd close <own-id> --reason "chunk 05 extracted"`.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet/git commands other than
`bd close`. No git commands — `.ai` auto-syncs on its own.
