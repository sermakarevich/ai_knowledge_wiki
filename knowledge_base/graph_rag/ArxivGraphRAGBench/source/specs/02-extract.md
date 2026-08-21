# Task: Extract wiki page 02 — Benchmark Design & Construction

## Context

You are one worker in a pipeline turning an academic paper into a knowledge-base wiki. This task covers ONE chunk of the paper. Context is tight on this model — **read ONLY the chunk file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files, do NOT read sibling wiki pages "for style/convention reference," and do NOT try to diagnose a prior failure by reading logs — the format contract below is the only convention you need. If this is a retry, just re-read the chunk and write directly.

## Input

Read this file (plain text, extracted from the paper "GraphRAG-Bench: Challenging Domain-Specific Reasoning Benchmark for GraphRAG"):

`/Users/sergii/.kb/papers/ArxivGraphRAGBench/source/chunks/02.txt`

This chunk covers Section 3 in full: 3.1 Question design, 3.2 Corpus collection and processing, 3.3 Expert-crafted rationale. There are no figures in this chunk.

## Output

Write the wiki page to this exact path (if it already exists — a retry — overwrite it completely):

`/Users/sergii/.kb/papers/ArxivGraphRAGBench/wiki/02-benchmark-design.md`

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Benchmark Design & Construction

**In one sentence:** <the whole argument of this chunk in one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total>

---

## Question design

<full detail: the 5 question types (fill-in-blank, multi-choice, multi-select, true-or-false, open-ended) and what each specifically tests, the textbook selection process (100+ publications -> 20 textbooks, 16 subfields), 1,018 questions, expert screening>

Include the question-type table (Table 1) as a markdown table if the source content supports it.

## Corpus collection and processing

<full detail: the 4-stage pipeline — Textbook Preprocessing (PDF classification, metadata extraction), Content Parsing (LayoutLMv3 layout analysis, YOLO-based formula detection, PaddleOCR), Post-Processing (MinerU reordering), Hierarchy Construction (Book -> Chapter -> Section -> Knowledge Content Unit)>

## Expert-crafted rationale

<full detail: what a rationale contains (prerequisite concepts, relationships, inferential operations), the two-level topic labels (Level 1 subfield, Level 2 concept), why this enables assessing reasoning fidelity not just answer correctness>

**Covers:** Section 3 (3.1-3.3) of GraphRAG-Bench (arXiv:2506.02404)
```

Rules:
- The `## Key points` bullets must stand alone as this chunk's substance at medium depth — capture the 5 question types, the corpus scale (1,018 questions, 16 disciplines, 20 textbooks, 7M words), the 4-stage extraction pipeline, and what makes the rationale annotation distinctive.
- Preserve exact numbers and named tools (LayoutLMv3, PaddleOCR, MinerU, YOLO-based formula detector).
- No meta-commentary about your own process. Write only the finished page.
- Be thorough — no line limit.

## Scope & DoD

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than closing your own bead.
- When the file is written, close your own bead: `bd close <your-bead-id> --reason "chunk 02 extracted"`
