# Task: Extract wiki page 03 — Evaluation Protocol, Metrics & Core Results

## Context

You are one worker in a pipeline turning an academic paper into a knowledge-base wiki. This task covers ONE chunk of the paper. Context is tight on this model — **read ONLY the chunk file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files, do NOT read sibling wiki pages "for style/convention reference," and do NOT try to diagnose a prior failure by reading logs — the format contract below is the only convention you need. If this is a retry, just re-read the chunk and write directly.

## Input

Read this file (plain text, extracted from the paper "GraphRAG-Bench: Challenging Domain-Specific Reasoning Benchmark for GraphRAG"):

`/Users/sergii/.kb/papers/ArxivGraphRAGBench/source/chunks/03.txt`

This chunk covers: the start of Section 4 (Experiments), the Metrics subsection (graph construction, retrieval, generation, rationale metrics), Experiment setups (the 9 GraphRAG methods compared and shared config), Section 4.1 Evaluation of graph construction (Table 2), Section 4.2 Evaluation of knowledge retrieval (Table 3), Section 4.3 Evaluation of generation accuracy (Table 4), Section 4.4 Evaluation of reasoning capabilities (Table 5). There are no figures in this chunk, but it contains dense data tables — reproduce them.

## Output

Write the wiki page to this exact path (if it already exists — a retry — overwrite it completely):

`/Users/sergii/.kb/papers/ArxivGraphRAGBench/wiki/03-evaluation-protocol-and-core-results.md`

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Evaluation Protocol, Metrics & Core Results

**In one sentence:** <the whole argument of this chunk in one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total>

---

## Metrics

<full detail on each metric family: Graph construction (efficiency=time, cost=tokens, organization=non-isolated node ratio), Knowledge retrieval (indexing time, average retrieval time, retrieval operators), Generation (new Accuracy metric — scoring rules for OE/FB via LLM judge, MC/TF exact, MS partial credit), Rationale (R score via LLM judge comparing to gold rationale, plus the AR metric distinguishing lucky guesses from real reasoning)>

## Experiment setup

<the 9 compared methods: RAPTOR, LightRAG, GraphRAG, G-Retriever, HippoRAG, GFM-RAG, DALK, KGP, ToG. Shared config: GPT-4o-mini as base LLM, no max token limit, top-k=5, chunk size 1200 tokens, other hyperparameters at paper-reported optima>

## Graph construction results (Table 2)

<reproduce Table 2 as a markdown table: method, token cost, time cost, organization %. Explain the 4 graph-structure classes (Tree/RAPTOR, Passage Graph/KGP, Knowledge Graph/G-Retriever+HippoRAG+GFM-RAG+DALK, Rich Knowledge Graph/GraphRAG+LightRAG) and the cost/quality tradeoffs the paper draws out>

## Knowledge retrieval results (Table 3)

<reproduce Table 3: method, retrieval operators, indexing time, average retrieval time. Explain why GFM-RAG indexes fastest, why RAPTOR retrieves fastest, why HippoRAG indexes slowest>

## Generation accuracy results (Table 4)

<reproduce Table 4: per-method accuracy by question type (FB/MC/MS/TF/OE) and average, with the up/down arrow vs GPT-4o-mini baseline. Call out RAPTOR as top performer, DALK/G-Retriever as degraders>

## Reasoning capability results (Table 5)

<reproduce Table 5: per-method R and AR scores by question type and average. Call out that GPT-4o-mini's reasoning (R/AR) drops even when generation accuracy is high, and that GraphRAG methods substantially close that gap; HippoRAG and RAPTOR remain top performers here too>

**Covers:** Section 4 intro, Metrics, Experiment setups, 4.1-4.4 of GraphRAG-Bench (arXiv:2506.02404)
```

Rules:
- The `## Key points` bullets must stand alone at medium depth — include the 4 metric families, the 9 compared methods, and the headline finding that RAPTOR/HippoRAG lead on accuracy+reasoning while DALK/G-Retriever can hurt generation accuracy.
- Tables must reproduce the exact numbers from the chunk text — do not round or approximate. If a table cell is ambiguous in the raw text, make your best-effort faithful transcription rather than omitting the row.
- No meta-commentary about your own process. Write only the finished page.
- Be thorough — no line limit.

## Scope & DoD

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than closing your own bead.
- When the file is written, close your own bead: `bd close <your-bead-id> --reason "chunk 03 extracted"`
