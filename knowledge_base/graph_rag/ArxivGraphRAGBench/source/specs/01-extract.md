# Task: Extract wiki page 01 — Introduction & Motivation

## Context

You are one worker in a pipeline turning an academic paper into a knowledge-base wiki. This task covers ONE chunk of the paper. Context is tight on this model — **read ONLY the chunk file listed below (and the figure description file, if any), nothing else.** Do NOT read this task's own fleet artifacts/log/event files, do NOT read sibling wiki pages "for style/convention reference," and do NOT try to diagnose a prior failure by reading logs — the format contract below is the only convention you need. If this is a retry, just re-read the chunk and write directly.

## Input

Read this file (plain text, extracted from the paper "GraphRAG-Bench: Challenging Domain-Specific Reasoning Benchmark for GraphRAG"):

`/Users/sergii/.kb/papers/ArxivGraphRAGBench/source/chunks/01.txt`

This chunk covers: Abstract, Section 1 (Introduction), Section 2 (Related Work).

Also read this figure description (a vision-model description of Figure 1, which belongs in this chunk):

`/Users/sergii/.kb/papers/ArxivGraphRAGBench/wiki/images/fig1-description.md`

The actual image file already exists at `/Users/sergii/.kb/papers/ArxivGraphRAGBench/wiki/images/fig1-overview.png` — embed it in your page using the description to write accurate surrounding text; you do not need to view the image yourself.

## Output

Write the wiki page to this exact path (if it already exists — a retry — overwrite it completely):

`/Users/sergii/.kb/papers/ArxivGraphRAGBench/wiki/01-introduction-and-motivation.md`

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction & Motivation

**In one sentence:** <the whole argument of this chunk in one sentence>

## Key points

- <complete claim, not a topic label — include numbers/mechanisms/conclusions where present>
- <5-8 bullets total>

---

## <subsection mirroring the source's own structure, e.g. "The problem with flat retrieval">

<full detail prose, hierarchical, mirroring the source's internal structure (Abstract / Introduction / Related Work as sub-sections)>

![Figure 1: sketched overview of GraphRAG-Bench](images/fig1-overview.png)

<a sentence or two describing what Figure 1 shows, based on the description file, placed right where the source discusses it>

## <next subsection>

...

**Covers:** Abstract, Section 1 (Introduction), Section 2 (Related Work) of GraphRAG-Bench (arXiv:2506.02404)
```

Rules:
- The `## Key points` bullets must stand alone as this chunk's substance at medium depth — someone reading only them should get the real content (the paper's central research question, its 3 stated limitations of prior benchmarks, and the 3 GraphRAG method categories from Related Work), not vague topic labels.
- Preserve exact numbers, e.g. paper counts, dataset sizes, citations by first-author name where natural.
- The image path in your markdown is relative: `images/fig1-overview.png` (the page lives in `wiki/`, images live in `wiki/images/`).
- No meta-commentary about your own process. Write only the finished page.
- Be thorough — no line limit.

## Scope & DoD

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than closing your own bead.
- When the file is written, close your own bead: `bd close <your-bead-id> --reason "chunk 01 extracted"`
