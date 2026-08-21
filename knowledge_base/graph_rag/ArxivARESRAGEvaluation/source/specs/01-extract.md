# Extract: ARES paper — Introduction & Related Work

## Problem
Write one wiki page summarizing a chunk of an academic paper about ARES, an automated
evaluation framework for Retrieval-Augmented Generation (RAG) systems.

## Context is tight — read ONLY these files, nothing else
- Input chunk: `/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/source/chunks/01.txt`

Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`,
`events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read
sibling wiki pages "for style/convention reference" — the format contract below is the
only convention needed. On a retry, do not diagnose the prior failure by reading logs;
just re-read the chunk and write directly.

## Fix
Read the chunk file above. It contains the Abstract, Section 1 (Introduction), and
Section 2 (Related Work) of the paper "ARES: An Automated Evaluation Framework for
Retrieval-Augmented Generation Systems" (Saad-Falcon et al., NAACL 2024).

Write the wiki page to this EXACT path (create parent dirs if needed):
`/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/wiki/01-introduction-and-related-work.md`

**If this file already exists (a retry), overwrite it completely.**

### Required format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction & Related Work

**In one sentence:** <the chunk's whole argument in one sentence — why RAG evaluation
is hard and how ARES's approach differs from prior automated evaluators>

## Key points

- <complete-sentence claim, not a topic label — repeat for 5-8 bullets>
- ...

---

## <subsection heading mirroring the source, e.g. "The RAG evaluation problem">

<full detail prose, hierarchical, covering the WHOLE chunk including its final
paragraphs on EXAM and RAGAS — not just the opening>

## <another subsection, e.g. "Related evaluation frameworks">

<...>

**Covers:** Abstract, Section 1 (Introduction), Section 2 (Related Work) — arXiv
2311.09476, pages 1-3
```

Guidance:
- The 5-8 key-point bullets must each be a full claim carrying real content (numbers,
  named methods, conclusions) — not "discusses related work".
- Cover the ENTIRE chunk, including its last paragraphs (EXAM and RAGAS comparison at
  the end of Related Work) — do not stop after summarizing only the opening.
- No figures in this chunk.
- Use exact numbers/percentages from the text where present (e.g. "59.3 and 14.4
  percentage points").
- No meta-commentary about being an AI or about this task — write only the wiki page
  content itself.

## Tests
- File exists at the output path above.
- File is well over 40 lines.
- Contains the required backlink line, an `**In one sentence:**` line, a `## Key points`
  section with 5-8 bullets, a `---` divider, and a `**Covers:**` footer line.

## DoD
1. Output file written to the exact path above.
2. `bd close <own-id> --reason "chunk 01 extracted"`

## Scope & constraints
- Touch ONLY the one output file listed above.
- No git commands at all — `.kb` auto-syncs.
- Do not run fleet commands other than `bd close`.
