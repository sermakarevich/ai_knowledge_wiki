# Task: write wiki page 01 — Introduction and Motivation

## Problem
We are building an LLM-wiki summary of an academic paper. This task covers one section of the paper: the Introduction and Motivation.

## Fix
1. Read ONLY this file: `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/source/chunks/01.txt`
   (plain text, one section of the paper "Why Neighborhoods Matter: Traversal Context and Provenance in Agentic GraphRAG"). Do not read any other file.
2. Write the wiki page to: `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/01-introduction-and-motivation.md`
3. If that file already exists (this is a retry), overwrite it completely with fresh content.

The wiki page MUST follow this exact structure (fill in the angle-bracket parts from the chunk text; keep the literal markdown otherwise):

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Motivation

**In one sentence:** <the section's whole argument in one sentence>

## Key points

- <complete-claim bullet 1>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5, up to 8 total>

---

## <subsection heading mirroring the source, e.g. "Problem: citation faithfulness in agentic GraphRAG">

<full-detail prose covering everything in this chunk: the problem being addressed, why it matters,
what gap in prior work it fills, and the paper's high-level approach. Use exact terms, numbers, and
claims from the chunk text — do not invent anything not present in the chunk.>

## <further subsection(s) as needed to cover the whole chunk>

...

---

**Covers:** Section 1 (Introduction), source/full.txt lines 1-73
```

Rules:
- The `## Key points` bullets must be complete, standalone claims (not topic labels like "discusses motivation").
- Cover the ENTIRE chunk — do not stop after the first paragraph.
- Do not fabricate citations, numbers, or claims not present in the chunk text.
- Do not read any other file — not this task's own fleet artifacts/log/event files, not sibling wiki pages, not `PLAN_AND_STATUS.md`/`KNOWLEDGE.md`. Context is tight on this model; only the chunk file above is needed.

## Tests
- `test -s /Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/01-introduction-and-motivation.md` (file exists and is non-empty)
- The file contains the string `**In one sentence:**` and the string `## Key points`

## DoD
1. `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/01-introduction-and-motivation.md` written per the structure above.
2. No git commands — this repo auto-syncs.
3. `bd close <own-id> --reason "chunk 01 extracted"` — never exit rc=0 without closing.

## Scope & constraints
- Touch ONLY `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/01-introduction-and-motivation.md`.
- Do not run fleet commands other than `bd close`.
- cwd: /Users/sergii/.kb
