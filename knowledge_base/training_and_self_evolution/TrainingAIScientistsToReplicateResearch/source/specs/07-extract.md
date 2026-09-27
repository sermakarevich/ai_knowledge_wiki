# Extract task: chunk 07 -- appendix-example-tasks-and-rubrics

## Problem
We are building an LLM-wiki page for one section of the paper "Training AI Scientists to
Replicate Research" (arXiv 2608.13331v1, aka the Replica / Faraday paper). This task covers
one section: **Appendix worked examples: agent system prompt, sample replication task, and rubric examples for specific papers**.

## Input
Read ONLY this file (plain text, extracted from the paper's PDF via pymupdf4llm):
`/Users/sergii/.ai/knowledge/research/TrainingAIScientistsToReplicateResearch/source/chunks/07.txt`

Context is tight on this worker model -- read ONLY the chunk file listed above (+ the figure
description files listed below, if any). Do NOT read this task's own fleet artifacts/log/event
files, do NOT read sibling wiki pages "for style reference", and do NOT read the finalize spec.
The format contract below is the only convention you need. On a retry, do not try to diagnose
a prior failure by reading logs -- just re-read the chunk and write directly.

## Output
Write the finished wiki page to (absolute path):
`/Users/sergii/.ai/knowledge/research/TrainingAIScientistsToReplicateResearch/wiki/07-appendix-example-tasks-and-rubrics.md`

If this file already exists (a retry), overwrite it completely with a fresh, complete page --
do not append or partially edit.

## Wiki page format contract (follow exactly)

- Backlink line: `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`
- `# <Topic Title>` (a short human-readable title for this section)
- `**In one sentence:** <the section's whole argument, in one sentence>`
- `## Key points` -- 5-8 bullets, each a COMPLETE CLAIM (not a topic label like "discusses X").
  Include real content: numbers, mechanisms, conclusions. Someone reading only this block
  should have the section's substance.
- `---`
- Then the FULL DETAIL: `##` subsections mirroring the source's internal structure
  (hierarchical, not flat prose). Preserve exact numbers, tables, and any verbatim
  prompts/configs/quotes from the source. This is an academic ML paper -- keep technical
  precision (equations described in words if needed, metric names, model names, dataset
  names, ablation results).
- If a figure description file is provided below and the source text names that figure
  (e.g. "Figure 2"), embed it at the point it is discussed:
  `![<caption>](images/<file>.png)` followed by 1-2 sentences from its description.
- Footer provenance line: `**Covers:** <one line naming the section(s)/pages of the source>`
- Do not add a top-level `# Title` matching the whole paper -- this is one page of many.
- Write ONLY the wiki page content, nothing else (no preamble, no "Here is the page").


## Scope & constraints
- Touch ONLY the one output file: `/Users/sergii/.ai/knowledge/research/TrainingAIScientistsToReplicateResearch/wiki/07-appendix-example-tasks-and-rubrics.md`.
- No git commands at all -- this is a `.ai` knowledge-base folder that auto-syncs itself.
- Do not run any fleet commands other than the final `bd close`.
- Do not run `fleet serve restart` / `fleet run`.

## Definition of Done
1. The output file `/Users/sergii/.ai/knowledge/research/TrainingAIScientistsToReplicateResearch/wiki/07-appendix-example-tasks-and-rubrics.md` exists and is non-trivial (well over 40 lines),
   follows the format contract above, and covers the WHOLE chunk (including its ending, not
   just the opening).
2. `bd close <own-id> --reason "chunk 07 extracted: appendix-example-tasks-and-rubrics"`
