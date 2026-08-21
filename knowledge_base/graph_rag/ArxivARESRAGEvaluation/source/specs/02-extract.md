# Extract: ARES paper — The ARES Method

## Problem
Write one wiki page summarizing a chunk of an academic paper about ARES, an automated
evaluation framework for Retrieval-Augmented Generation (RAG) systems.

## Context is tight — read ONLY these files, nothing else
- Input chunk: `/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/source/chunks/02.txt`
- Figure description (for Figure 1, embed it where the chunk text discusses "Figure 1"):
  the figure image file is at `/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/wiki/images/01-fig1-overview.png`
  and its description is below — use it to write the surrounding prose, do not just repeat it verbatim:

```
**Figure 1 — Overview of ARES.** This is a schematic pipeline diagram (a left-to-right flow
of three stages): Stage 1 (LLM Generation of Synthetic Dataset) generates synthetic
queries/answers from in-domain passages using few-shot examples; Stage 2 (Preparing LLM
Judges) fine-tunes an LLM via contrastive learning on the generated triples to judge
context relevance, answer faithfulness, and answer relevance; Stage 3 (Ranking RAG Systems
with Confidence Intervals) uses the trained judges plus PPI and a small human-preference
validation set (~150+ annotated points) to produce confidence-bounded rankings of RAG
systems.
```

Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`,
`events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read
sibling wiki pages "for style/convention reference" — the format contract below is the
only convention needed. On a retry, do not diagnose the prior failure by reading logs;
just re-read the chunk and write directly.

## Fix
Read the chunk file above. It contains Section 3 ("ARES") of the paper, with subsections
3.1 (LLM Generation of Synthetic Dataset), 3.2 (Preparing LLM Judges), and 3.3 (Ranking
RAG Systems with Confidence Intervals / PPI).

Write the wiki page to this EXACT path (create parent dirs if needed):
`/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/wiki/02-ares-method.md`

**If this file already exists (a retry), overwrite it completely.**

### Required format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The ARES Method

**In one sentence:** <the chunk's whole argument in one sentence — how ARES turns a
passage set + few-shot examples + a small human validation set into confidence-bounded
RAG system rankings via synthetic data, fine-tuned judges, and PPI>

## Key points

- <complete-sentence claim — repeat for 5-8 bullets, e.g. the three required inputs, the
  weak/strong negative generation strategies, the three judge criteria (context relevance,
  answer faithfulness, answer relevance), what PPI buys over pure annotation or pure
  model prediction, the 95% confidence level used>
- ...

---

## Overview

![Overview of the ARES pipeline](images/01-fig1-overview.png)

<1-2 paragraphs describing the three-stage pipeline shown in the figure>

## Synthetic Dataset Generation (3.1)

<full detail: FLAN-T5 XXL generation, filtering by retrieval check, weak negative
generation, strong negative generation — describe both strategies precisely>

## Preparing LLM Judges (3.2)

<full detail: DeBERTa-v3-Large judges, the three criteria, fine-tuning stopping
criterion (three epochs no improvement)>

## Ranking RAG Systems with Confidence Intervals (3.3)

<full detail: why raw judge scores aren't enough, why pure annotation is costly, how
PPI's rectifier function combines both, the 95% confidence level, ranking by CI midpoint>

**Covers:** Section 3 "ARES" (3.1-3.3), Figure 1 — arXiv 2311.09476, pages 3-5
```

Guidance:
- Embed the figure exactly once, near the Overview section, using the markdown image
  syntax shown above (relative path `images/01-fig1-overview.png`).
- Cover the ENTIRE chunk, including subsection 3.3 at the end (PPI) — do not stop after
  3.1.
- Use exact numbers/terms from the text (e.g. DeBERTa-v3-Large, 150+ datapoints, 95%
  alpha).
- No meta-commentary about being an AI or about this task — write only the wiki page
  content itself.

## Tests
- File exists at the output path above.
- File is well over 40 lines.
- Contains the required backlink line, an `**In one sentence:**` line, a `## Key points`
  section with 5-8 bullets, the embedded figure image line, a `---` divider, and a
  `**Covers:**` footer line.

## DoD
1. Output file written to the exact path above.
2. `bd close <own-id> --reason "chunk 02 extracted"`

## Scope & constraints
- Touch ONLY the one output file listed above.
- No git commands at all — `.kb` auto-syncs.
- Do not run fleet commands other than `bd close`.
