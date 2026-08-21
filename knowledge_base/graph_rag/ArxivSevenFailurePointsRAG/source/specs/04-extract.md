# Task: extract wiki page 4 — Lessons learned and future research

## Context is tight on this model
Read ONLY the one input file listed below. Nothing else.
Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input
- Full paper text: `/Users/sergii/.kb/papers/ArxivSevenFailurePointsRAG/source/chunks/01.txt`

## Your scope within the paper
Cover ONLY:
- Section 6 — LESSONS AND FUTURE RESEARCH, including Table 2, and subsections:
  - 6.1 Chunking and Embeddings
  - 6.2 RAG vs Finetuning
  - 6.3 Testing and Monitoring RAG systems
- Section 7 — CONCLUSION

Ignore all other sections of the input file (background/RAG pipeline, case studies, failure points) — those become other wiki pages, not this one.

## Output
Write exactly one file: `/Users/sergii/.kb/papers/ArxivSevenFailurePointsRAG/wiki/04-lessons-and-future-research.md`

If this file already exists (a retry), overwrite it completely with fresh content — do not append or merge.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Lessons Learned & Future Research

**In one sentence:** <the whole point of this section, one sentence>

## Key points

- <complete claim, not a topic label — 5-8 bullets total, covering the lessons AND the two key overall takeaways of the paper>

---

## Lessons learned (Table 2)

<Reproduce Table 2's content as a markdown table: the lessons learned from the three case studies with key takeaways.>

## Chunking and Embeddings

<full detail>

## RAG vs Finetuning

<full detail>

## Testing and Monitoring RAG systems

<full detail>

## Conclusion

<full detail — include the paper's two key takeaways: 1) validation of a RAG system is only feasible during operation, 2) robustness evolves rather than being designed in upfront>

**Covers:** Section 6 (Lessons and Future Research), Table 2, Section 7 (Conclusion)
```

Each key-point bullet must be a complete, content-bearing claim — not "discusses X". Reproduce Table 2 faithfully as markdown.

## Definition of done
1. Output file written at the exact path above, non-trivial (>40 lines), covering all three lesson subsections, Table 2, and the conclusion.
2. `bd close <own-bead-id> --reason "chunk 04 (lessons/conclusion) extracted"`

## Scope constraints
- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than the `bd close` above.
- No git commands.
