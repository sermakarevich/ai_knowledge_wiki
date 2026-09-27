---
type: Paper
title: Demystifying Agent Skills: Why They Work-Until They Don't
description: A contrastive trajectory study of 8,135 trials showing agent skills beat workflow memory by working as procedural anchors, not knowledge sources, while introducing their own misapplication failures and suffering a sharp retrieval-precision collapse as skill libraries grow.
generated: { by: claude/claude-sonnet-5, at: 2026-08-18T06:20:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2608.14036
  - id: local-copy
    resource: source/2608.14036.pdf
tags: [agent-skills, procedural-memory, llm-agents, retrieval, workflow-memory]
---

# Demystifying Agent Skills: Why They Work-Until They Don't

This paper (Jiang, Huang, Xing, Wu, Gao, Cao, Wang, Liu, Li — 2026) moves the study of LLM "agent skills" past aggregate success-rate comparisons. It runs the same tasks under matched Raw / Workflow-Memory / Skill conditions built from identical prior trajectories, then uses a human-validated 3-category / 12-mode taxonomy over 528 paired trajectory triples to explain *why* skills help and *where* they fail. It was worth ingesting because it gives a mechanism-level account — procedural anchoring, not knowledge injection — plus a hard number on the retrieval bottleneck (precision collapses from 29.6% to 3.3% as skill pools grow from 5 to 100) that is directly relevant to any skill/procedural-memory system for coding agents.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10-15 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-introduction-and-related-work\|Introduction and Related Work]] | Why aggregate success rates hide the mechanism; positioning against memory-reuse and skill-benchmark literature |
| [[wiki/02-study-design\|Study Design]] | Four research questions, the Raw/Workflow-Memory/Skill contrast, the fixed-budget composition grid, and the 3-arm retrieval study |
| [[wiki/03-skill-use-mechanisms\|Skill-Use Mechanisms]] | The contrastive trajectory-analysis pipeline and the 3-category/12-mode taxonomy over 528 paired triples |
| [[wiki/04-findings\|Findings, Conclusion, and Limitations]] | Skill vs Workflow Memory results, the SC1/SC2/SC3 tradeoffs, retrieval-precision collapse, and study limitations |
| [[wiki/05-implementation-details-and-prompts\|Implementation Details and Prompts]] | Full Appendix A/B/C: protocols per RQ, complete data tables, token-cost analysis, and the prompt templates used |

## Original Source

- [source/2608.14036.pdf](source/2608.14036.pdf) — arXiv paper PDF, retrieved 2026-08-18
