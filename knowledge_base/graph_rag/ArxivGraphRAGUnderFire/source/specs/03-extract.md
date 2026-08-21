# Task: Extract wiki page 03 — GRAGPOISON Attack Design

## Context

You are one worker in a chain that turns the paper "GraphRAG under Fire" (arXiv:2501.14050) into a wiki. Your job is ONLY to write ONE wiki page from ONE chunk of the paper's text. Context is tight on this model — **read ONLY the input file(s) listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do NOT diagnose the prior failure by reading logs — just re-read the chunk and write directly.

## Input

- Chunk text: `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/source/chunks/03.txt`
- This chunk covers: the design of the GRAGPOISON attack — Relation Selection (4.1), Relation Injection (4.2), Relation Enhancement, and Narrative Generation (Sec 4).
- Figure descriptions (vision-model output describing full-page renders of the paper's figures — use these to write the figure captions/discussion, you cannot see the images yourself):
  - `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/images/fig3-gragpoison-overview-description.md` → embed as `![Overview of GRAGPOISON attack pipeline](images/fig3-gragpoison-overview.png)`
  - `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/images/fig4-attack-example-description.md` → embed as `![Example of attacking two related queries: baseline vs GRAGPOISON](images/fig4-attack-example.png)`

## Output

Write the file: `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/03-gragpoison-design.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# GRAGPOISON Attack Design

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total, each carrying real content: numbers, mechanisms, conclusions>

---

<## subsections mirroring the chunk's own structure: Relation Selection, Relation
Injection, Relation Enhancement, Narrative Generation. Explain the three-strategy
attack mechanism precisely, with any formulas/notation and worked examples given
in the text. Embed the two figures inline next to the text discussing them, using
the exact markdown image syntax given above.>

**Covers:** Sec 4 (GRAGPOISON design): 4.1 Relation Selection, 4.2 Relation Injection, Relation Enhancement, Narrative Generation
```

Rules:
- Cover the WHOLE chunk, including its ending.
- No meta-commentary, no repetition loops.
- Use the exact GRAGPOISON terminology and notation from the source text.
- No line limit — be thorough.

## Scope & DoD

- Touch ONLY the one output file above.
- Do not run any fleet commands other than closing this task.
- When the file is written: `bd close <own-id> --reason "chunk 03 extracted"`
