---
type: Paper
title: "SodaMem: Evidence-Grounded Temporal Graph Memory for LLM Agents"
description: An evidence-grounded temporal knowledge-graph memory for LLM agents, using typed FactEvents with mandatory provenance, write-time supersession edges, and a planner-reader answering loop, reaching 92.8% on LongMemEval-S at $0.00161/question.
generated: { by: claude/claude-sonnet-5, at: 2026-08-21T06:50:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2608.08055
  - id: local-copy
    resource: source/source.md
tags: [agent-memory, temporal-graph, graph-rag, provenance, longmemeval]
---

# SodaMem: Evidence-Grounded Temporal Graph Memory for LLM Agents

SodaMem is a 2026 paper (Wan, Wu, Lyu — Peking University) proposing that long-horizon personal-agent memory should be modeled as an evidence-grounded temporal knowledge graph rather than a flat RAG store or Markdown diary. Its central claim is a cost–accuracy result: on LongMemEval-S, a store-of-record configuration reaches 92.8% accuracy at roughly one-sixth of a cent per question using a cheap Flash-tier model, landing near the accuracy frontier while strictly dominating several higher-cost public systems. It was ingested because it sits directly in the agentic-GraphRAG / long-term-memory research vein already tracked in this KB (temporal graphs, provenance, supersession).

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole paper, shallow
- [[digest|Digest]] — rung 2: the whole paper at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-motivation-and-related-work\|Motivation & Related Work]] | Why flat RAG/Markdown fail (P1–P4), design principles, and how SodaMem positions itself against LoCoMo/LongMemEval benchmarks and MemGPT/Mem0/HippoRAG/Zep-style prior work |
| [[wiki/02-method-sodamem\|Method: SodaMem]] | The FactEvent schema, ingest with provenance hard constraint, hybrid store with typed edges, three-tunnel connection-density retrieval, and the planner–reader answering loop |
| [[wiki/03-evaluation-and-results\|Evaluation & Results]] | LongMemEval-S setup, the 92.8%/$0.00161 headline result, the 22-method cost–accuracy table, and stated limitations |

## Original Source

- [source/source.md](source/source.md) — provenance pin (PDF over the 2 MB size guard; full extracted text kept at `source/fulltext.txt`), retrieved 2026-08-21
