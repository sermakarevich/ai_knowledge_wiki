# Extract: ARES paper — Experimental Setup

## Problem
Write one wiki page summarizing a chunk of an academic paper about ARES, an automated
evaluation framework for Retrieval-Augmented Generation (RAG) systems.

## Context is tight — read ONLY these files, nothing else
- Input chunk: `/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/source/chunks/03.txt`

Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`,
`events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read
sibling wiki pages "for style/convention reference" — the format contract below is the
only convention needed. On a retry, do not diagnose the prior failure by reading logs;
just re-read the chunk and write directly.

## Fix
Read the chunk file above. It contains Section 4 ("Experiments") of the paper, covering
the datasets (KILT, SuperGLUE, AIS), models, and baselines used to evaluate ARES.

Write the wiki page to this EXACT path (create parent dirs if needed):
`/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/wiki/03-experimental-setup.md`

**If this file already exists (a retry), overwrite it completely.**

### Required format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experimental Setup

**In one sentence:** <the chunk's whole argument in one sentence — what datasets, models,
and baselines ARES is tested against and why they were chosen>

## Key points

- <complete-sentence claim — repeat for 5-8 bullets, e.g. which KILT/SuperGLUE datasets,
  which retrievers/generators, FLAN-T5 XXL and DeBERTa-v3-Large roles, RAGAS as the main
  baseline, the AIS attribution benchmark>
- ...

---

## <subsection headings mirroring the source's 4.1/4.2/4.3 structure — name them from
what the chunk actually covers, e.g. "Datasets", "Models", "Baselines and metrics">

<full detail covering the WHOLE chunk>

**Covers:** Section 4 "Experiments" (4.1-4.3) — arXiv 2311.09476, pages 5-6
```

Guidance:
- Cover the ENTIRE chunk, including its final subsection — do not stop after the
  datasets subsection.
- Use exact dataset names, model names, and any numbers present in the text.
- No figures in this chunk.
- No meta-commentary about being an AI or about this task — write only the wiki page
  content itself.

## Tests
- File exists at the output path above.
- File is well over 40 lines.
- Contains the required backlink line, an `**In one sentence:**` line, a `## Key points`
  section with 5-8 bullets, a `---` divider, and a `**Covers:**` footer line.

## DoD
1. Output file written to the exact path above.
2. `bd close <own-id> --reason "chunk 03 extracted"`

## Scope & constraints
- Touch ONLY the one output file listed above.
- No git commands at all — `.kb` auto-syncs.
- Do not run fleet commands other than `bd close`.
