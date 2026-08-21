# Task: Extract wiki page 04 — Evaluation Results

## Context

You are one worker in a chain that turns the paper "GraphRAG under Fire" (arXiv:2501.14050) into a wiki. Your job is ONLY to write ONE wiki page from ONE chunk of the paper's text. Context is tight on this model — **read ONLY the input file(s) listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do NOT diagnose the prior failure by reading logs — just re-read the chunk and write directly.

## Input

- Chunk text: `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/source/chunks/04.txt`
- This chunk covers: Experimental Setting (5.1), main results comparing GRAGPOISON to baselines, the Ablation Study (5.3), and additional experiments — Targeted Attacks, Alternative GraphRAG variants, and Three-Hop Questions (5.4).
- Figure descriptions (vision-model output describing full-page renders of the paper's figures — use these to write the figure captions/discussion, you cannot see the images yourself):
  - `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/images/fig5-page9-description.md` → embed as `![Evaluation results, page 9](images/fig5-page9.png)`
  - `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/images/fig67-page10-description.md` → embed as `![Evaluation results, page 10](images/fig67-page10.png)`

## Output

Write the file: `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/04-evaluation-results.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Evaluation Results

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total, each carrying real content: numbers, mechanisms, conclusions>

---

<## subsections mirroring the chunk's own structure: Experimental Setting (datasets,
GraphRAG variants, models, metrics), Main Results (reproduce comparison tables as
markdown tables with exact numbers, bold the best result per row/column), Ablation
Study, and the additional experiments (Targeted Attacks, Alternative GraphRAG,
Three-Hop Questions). Embed the two figures inline next to the text discussing
similar content, using the exact markdown image syntax given above.>

**Covers:** Sec 5 (Evaluation): 5.1 Experimental Setting, main results, 5.3 Ablation Study, 5.4 (Targeted Attacks, Alternative GraphRAG, Three-Hop Questions)
```

Rules:
- Cover the WHOLE chunk, including its ending.
- No meta-commentary, no repetition loops.
- Reproduce every numeric result table you find as a markdown table — this is the paper's evidence, do not paraphrase away the numbers.
- No line limit — be thorough.

## Scope & DoD

- Touch ONLY the one output file above.
- Do not run any fleet commands other than closing this task.
- When the file is written: `bd close <own-id> --reason "chunk 04 extracted"`
