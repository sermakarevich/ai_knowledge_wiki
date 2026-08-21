# Task: write wiki page 03 — Results and Discussion

## Problem
We are building an LLM-wiki summary of an academic paper. This task covers one section of the paper: Results & Discussion, including Table 1 and Table 2.

## Fix
1. Read ONLY this file: `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/source/chunks/03.txt`
   (plain text, one section of the paper). Do not read any other file.
2. Write the wiki page to: `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/03-results-and-discussion.md`
3. If that file already exists (this is a retry), overwrite it completely with fresh content.

The wiki page MUST follow this exact structure:

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Results and Discussion

**In one sentence:** <the section's whole argument in one sentence>

## Key points

- <complete-claim bullet 1, include a concrete number if the chunk has one>
- <complete-claim bullet 2>
- <complete-claim bullet 3>
- <complete-claim bullet 4>
- <complete-claim bullet 5, up to 8 total>

---

## <subsection heading, e.g. "Citation faithfulness is not binary">

<full-detail prose. Reproduce any tables (Table 1, Table 2) from the chunk text as markdown tables,
with the same numbers/columns. Do not invent numbers not present in the chunk.>

## <further subsection(s) as needed to cover the whole chunk>

...

---

**Covers:** Section 3 (Results & Discussion), source/full.txt lines 240-329
```

Rules:
- The `## Key points` bullets must be complete, standalone claims, not topic labels.
- Cover the ENTIRE chunk — do not stop after the first paragraph.
- Reproduce every table in the chunk as a markdown table with its actual numbers.
- Do not fabricate numbers or claims not present in the chunk text.
- Do not read any other file — not this task's own fleet artifacts/log/event files, not sibling wiki pages, not `PLAN_AND_STATUS.md`/`KNOWLEDGE.md`. Context is tight on this model; only the chunk file above is needed.

## Tests
- `test -s /Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/03-results-and-discussion.md`
- The file contains `**In one sentence:**` and `## Key points`

## DoD
1. `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/03-results-and-discussion.md` written per the structure above.
2. No git commands — this repo auto-syncs.
3. `bd close <own-id> --reason "chunk 03 extracted"` — never exit rc=0 without closing.

## Scope & constraints
- Touch ONLY `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/wiki/03-results-and-discussion.md`.
- Do not run fleet commands other than `bd close`.
- cwd: /Users/sergii/.kb
