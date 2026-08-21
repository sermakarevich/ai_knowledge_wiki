---
type: Paper
title: "PersonalAI 2.0: Enhancing Knowledge Graph Traversal/Retrieval with Planning Mechanism for Personalized LLM Agents"
description: A GraphRAG framework that adds an LLM-planned, dynamic, multistage query-processing pipeline to knowledge-graph-backed LLM agents, beating LightRAG, RAPTOR and HippoRAG 2 on six QA benchmarks (avg +4%) and reaching SOTA (89%) on the MINE-1 information-retention benchmark.
generated: { by: claude/sonnet, at: 2026-08-21T11:10:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2605.13481
  - id: local-copy
    resource: source/chunks/
tags: [agent-memory, knowledge-graph, graph-rag, retrieval-planning, multi-hop-qa, llm-as-a-judge]
---

# PersonalAI 2.0: Enhancing Knowledge Graph Traversal/Retrieval with Planning Mechanism for Personalized LLM Agents

PAI-2 (Menschikov et al., 2026) is a GraphRAG (graph-based Retrieval-Augmented Generation) method for personalized LLM agents. Its central claim is that a *dynamic, LLM-planned* search over a knowledge graph — rather than a single flat retrieval pass or static node-level traversal — is what drives gains on multi-hop QA: an ablation isolates the planning mechanism itself as worth +18% LLM-as-a-Judge accuracy, separate from the +6% contributed by better graph-traversal algorithms. Across six QA benchmarks, PAI-2 beats LightRAG, RAPTOR and HippoRAG 2 by an average +4%, and its graph-construction ("Memorize") pipeline reaches SOTA (89% information retention) on the MINE-1 benchmark. It was ingested as part of the KB's ongoing agentic-GraphRAG research vein (see the `graph_rag` category and [[connections|Connections]] below).

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
| [[wiki/01-introduction-and-related-work\|Introduction & Related Work]] | Motivation, the five stated contributions, and how PAI-2 differs from PAI-1, ToG, RoG, DoG, PDA, and PG&AKV |
| [[wiki/02-methods-pai2-pipeline\|Methods: PAI-2 Pipeline]] | The 13-stage QA pipeline — preprocessing, plan generation, entity/vertex matching, clue-query traversal, answer aggregation — with Figure 1 |
| [[wiki/03-experimental-setup-and-evaluation\|Experimental Setup & Evaluation]] | Research questions, LLM backbone selection, benchmarks, LLM-as-a-Judge + RAGAS metrics, baselines, infrastructure |
| [[wiki/04-experiments-and-results\|Experiments & Results]] | Main benchmark comparison, plan-enhancement and graph-traversal ablations, clue-query-count sweep, latency |
| [[wiki/05-conclusions-limitations-future-work\|Conclusions, Limitations & Future Work]] | Summary of findings, four stated memory-design limitations, proposed fixes, ethics statement |
| [[wiki/06-appendix-prompts-pipeline-stages\|Appendix: Prompts for Pipeline Stages]] | All 17 prompt templates (Tables 7–23) for query preprocessing and graph exploration/answer aggregation |
| [[wiki/07-appendix-pseudocode-datasets-hyperparams-judge\|Appendix: Pseudocode, Datasets, Hyperparameters, Judge]] | Algorithm 1 pseudocode, dataset preprocessing stats, baseline hyperparameters, LLM-as-a-Judge config |
| [[wiki/08-appendix-graph-stats-ablations-mine1-humaneval\|Appendix: Graph Stats, Ablations, MINE-1, Human Eval]] | Memory-graph size/cost stats, clue-query ablation detail, MINE-1 result (Figure 2), human-evaluation agreement |

## Original Source

- [arXiv:2605.13481](https://arxiv.org/abs/2605.13481) — original paper
- [source/chunks/](source/chunks/) — local extracted-text chunks used to generate this wiki (no PDF binary kept)
