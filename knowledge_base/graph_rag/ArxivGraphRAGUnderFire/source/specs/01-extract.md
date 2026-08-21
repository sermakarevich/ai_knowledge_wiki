# Task: Extract wiki page 01 — Introduction and Threat Model

## Context

You are one worker in a chain that turns the paper "GraphRAG under Fire" (arXiv:2501.14050) into a wiki. Your job is ONLY to write ONE wiki page from ONE chunk of the paper's text. Context is tight on this model — **read ONLY the input file(s) listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do NOT diagnose the prior failure by reading logs — just re-read the chunk and write directly.

## Input

- Chunk text (plain text, extracted from the PDF with `pdftotext -layout`, cleaned of LaTeX artifacts): `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/source/chunks/01.txt`
- This chunk covers: Introduction (Sec 1), Preliminaries incl. GraphRAG background (Sec 2.1-2.2), and the Threat Model (Sec 2.3).
- Figure descriptions (vision-model output describing full-page renders of the paper's figures — use these to write the figure captions/discussion, you cannot see the images yourself):
  - `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/images/fig1-overview-description.md` → embed as `![Overview of poisoning attacks on GraphRAG](images/fig1-overview.png)`
  - `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/images/fig2-graphrag-schematic-description.md` → embed as `![Schematic illustration of GraphRAG concepts](images/fig2-graphrag-schematic.png)`

## Output

Write the file: `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/01-introduction-and-threat-model.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Threat Model

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total, each carrying real content: numbers, mechanisms, conclusions>

---

<## subsections mirroring the chunk's own structure, hierarchical, with exact numbers,
terminology, and the three research questions (RQ1/RQ2/RQ3) stated verbatim.
Embed the two figures inline next to the text discussing them, using the exact
markdown image syntax given above.>

**Covers:** Sec 1 (Introduction), Sec 2.1-2.2 (Preliminaries / GraphRAG background), Sec 2.3 (Threat Model)
```

Rules:
- Cover the WHOLE chunk, including its ending (do not stop after the opening paragraphs).
- No meta-commentary, no "as an AI...", no repetition loops.
- Use the exact GraphRAG/GRAGPOISON terminology from the source text.
- No line limit — be thorough.

## Scope & DoD

- Touch ONLY the one output file above.
- Do not run any fleet commands other than closing this task.
- When the file is written: `bd close <own-id> --reason "chunk 01 extracted"`
