# Task: Extract wiki page 02 — RQ1: Existing Attacks Fail Under GraphRAG

## Context

You are one worker in a chain that turns the paper "GraphRAG under Fire" (arXiv:2501.14050) into a wiki. Your job is ONLY to write ONE wiki page from ONE chunk of the paper's text. Context is tight on this model — **read ONLY the input file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do NOT diagnose the prior failure by reading logs — just re-read the chunk and write directly.

## Input

- Chunk text: `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/source/chunks/02.txt`
- This chunk covers: RQ1 — Performance of conventional RAG poisoning attacks under GraphRAG (Sec 3, including 3.1 Experimental Setting and 3.2 Experimental Results).
- No figures in this chunk.

## Output

Write the file: `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/02-rq1-existing-attacks-fail.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# RQ1: Existing Attacks Fail Under GraphRAG

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total, each carrying real content: numbers, mechanisms, conclusions>

---

<## subsections mirroring the chunk's own structure: the experimental setting
(datasets, baselines like PoisonedRAG, models, metrics), and the experimental
results showing why existing poisoning attacks degrade under GraphRAG.
Reproduce any tables/numbers from the text exactly as markdown tables.>

**Covers:** Sec 3 (RQ1: Performance of Conventional RAG poisoning attacks), Sec 3.1-3.2
```

Rules:
- Cover the WHOLE chunk, including its ending.
- No meta-commentary, no repetition loops.
- Use the exact terminology from the source text (e.g. PoisonedRAG).
- No line limit — be thorough.

## Scope & DoD

- Touch ONLY the one output file above.
- Do not run any fleet commands other than closing this task.
- When the file is written: `bd close <own-id> --reason "chunk 02 extracted"`
