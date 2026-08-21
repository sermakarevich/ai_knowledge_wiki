# Task: Extract wiki page 06 — Appendix: Pipeline Walkthrough, Error Analysis & Prompts (HippoRAG paper)

Context is tight on this model — read ONLY the chunk file and the figure description files listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- Chunk text (source content to summarize): `/Users/sergii/.kb/papers/ArxivHippoRAG/source/chunks/06.txt`
- Figure descriptions (embed each figure at the point the chunk discusses it):
  - `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure3-description.md` (Figure 3 — Pipeline Example: Question & Annotations)
  - `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure4-description.md` (Figure 4 — Pipeline Example: Indexing)
  - `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure5-description.md` (Figure 5 — Pipeline Example: Retrieval)
  - `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure6-description.md` (Figure 6 — Density of similarity scores)
  - `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure7-description.md` (Figure 7 — Prompt for passage NER during indexing)
  - `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure8-description.md` (Figure 8 — Prompt for query NER during retrieval)
  - `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure9-description.md` (Figure 9 — Prompt for OpenIE during indexing)
- The actual figure image files already exist at `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure{3,4,5,6,7,8,9}.png`.

## Output

Write exactly one file: `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/06-appendix-pipeline-errors.md`

If this file already exists (a retry), overwrite it completely.

## What this chunk covers

Appendix material: a full worked example of the HippoRAG pipeline (question, supporting/distractor passages, indexing stage, retrieval stage), a density-of-similarity-scores analysis, an error-type breakdown table (NER/OpenIE failure modes), implementation details, and the actual LLM prompts used for passage NER, query NER, and OpenIE.

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Pipeline Walkthrough, Error Analysis & Prompts

**In one sentence:** <the whole point of this appendix material in one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total>

---

## Full Pipeline Example

<full detail of the worked example: the question, supporting passages, distractor passages>

![HippoRAG Pipeline Example: Question and Annotations (Figure 3)](images/figure3.png)

<integrate figure 3's description into accurate prose>

<the indexing stage discussion>

![HippoRAG Pipeline Example: Indexing (Figure 4)](images/figure4.png)

<integrate figure 4's description into accurate prose>

<the retrieval stage discussion>

![HippoRAG Pipeline Example: Retrieval (Figure 5)](images/figure5.png)

<integrate figure 5's description into accurate prose>

## Similarity Score Analysis

![Density of similarity scores (Figure 6)](images/figure6.png)

<integrate figure 6's description into accurate prose>

## Error Analysis

<full detail of the error-type table — reproduce as a markdown table with exact percentages>

## Implementation Details & Prompts

<implementation details from the chunk>

![Prompt for passage NER during indexing (Figure 7)](images/figure7.png)

<summarize what this prompt does, using figure 7's description>

![Prompt for query NER during retrieval (Figure 8)](images/figure8.png)

<summarize what this prompt does, using figure 8's description>

![Prompt for OpenIE during indexing (Figure 9)](images/figure9.png)

<summarize what this prompt does, using figure 9's description>

**Covers:** Appendix (pipeline example, error analysis, implementation details, prompts), pages 20-31
```

Rules:
- Backlink line, one-sentence headline, and Key points block are mandatory and must come first.
- Every figure named in this chunk (Figures 3-9) MUST be embedded at the point it is discussed, using the exact paths above.
- Reproduce the error-analysis table with exact percentages as a markdown table.
- No meta-commentary about the extraction process itself. No placeholder text.
- Do not fabricate content not present in the chunk.
- This chunk is longer than the others — be thorough, do not compress it into a short page.

## DoD (definition of done)

1. `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/06-appendix-pipeline-errors.md` is written per the contract above, with all 7 figures embedded.
2. Run `bd close <own-id> --reason "chunk 06 extracted"`.

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than the `bd close` above.
