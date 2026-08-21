# Task: Extract wiki page 01 — HiGram method (chunk 01/02)

Context is tight on this model — read ONLY the chunk file (+ figure description file) listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- Chunk text: `/Users/sergii/.kb/papers/ArxivHiGram/source/chunks/01.txt`
  (covers the paper's Introduction, Related Work, and Method sections: 3.1 Hierarchical Memory Organization, 3.2 MicroGraph-based Path-Level Localization, 3.3 Coordinated Rewriting)
- Figure description: `/Users/sergii/.kb/papers/ArxivHiGram/wiki/images/fig1-description.md`
  (describes `images/fig1-overview.png`, captioned "Figure 1: An overview of HiGram")

## Output

Write: `/Users/sergii/.kb/papers/ArxivHiGram/wiki/01-hierarchical-memory-and-method.md`

If this file already exists (a retry), overwrite it completely.

## Format contract

Write a single self-contained wiki page in this exact structure:

```markdown
[[../index|Wiki]] | [[../summary|Summary]]

# Hierarchical Memory and the HiGram Method

**In one sentence:** <one sentence headline capturing the core idea of this chunk>

## Key points

- <bullet>
- <bullet>
- <bullet>
(4-8 bullets covering the chunk's main claims/ideas)

## Full detail

<the full deep-dive content: explain the problem HiGram addresses (why flat/unstructured
memory graphs fail LLM agents on long-horizon tasks), the two-tier hierarchical graph memory
organization (upper-level nodes vs. MemoryUnits), how MicroGraph-based path-level localization
works (anchor extraction, support subgraph assembly, candidate path scoring, evidence path
selection), and how coordinated rewriting updates the evidence path (input & matching,
intra-unit vs inter-unit rewrites, accept/reject). Cover related work positioning briefly
(how HiGram differs from flat/unstructured memory graph baselines). Be thorough — this page
is one of two that jointly cover the entire paper; do not leave out details found in the
chunk text.>

![Figure 1: An overview of HiGram](images/fig1-overview.png)

<embed the figure directly after the passage that discusses the hierarchical architecture,
using the figure description below to write 2-4 sentences of caption/explanation around it>
```

Use the figure description file's content to write the explanation around the embedded image — do not just paste the description verbatim, integrate it into the surrounding prose.

The page must cover the WHOLE chunk, including its ending (Coordinated Rewriting, section 3.3) — do not stop after the introduction/related-work material.

## Scope & constraints

- Touch ONLY the one output file listed above.
- No git commands at all — `.kb` auto-syncs.
- Do not run fleet commands other than `bd close`.

## DoD

1. Output file written at the path above, following the format contract, non-trivial (well over 40 lines).
2. `bd close <own-id> --reason "chunk 01 extracted"`
