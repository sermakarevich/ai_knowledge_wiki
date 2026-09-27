---
type: index
title: "EvoOntology: A Self-Evolving Ontology Layer for Data Agents"
description: "Folder index for EvoOntology: orientation, reading order, and links to summary, digest, explainer, critical thinking, questions, and all wiki pages."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T07:29:22Z
sources:
  - id: original
    resource: https://arxiv.org/pdf/2609.15779
  - id: local-copy
    resource: source/source.md
tags: [data-agents, ontology, self-evolution, text-to-sql]
---

# EvoOntology: A Self-Evolving Ontology Layer for Data Agents

EvoOntology inserts a self-evolving ontology layer between heterogeneous data sources and ReAct data agents to close the agent–data gap. It combines a typed Content graph, a Schema layer, and an MCP Tool layer built by probing and refined through gated trajectory-grounded evolution. Start with the summary, deepen with the digest, then use the wiki pages for section-level detail.

## How to work through this

1. Read the [summary](summary.md) (~2 min) for the TL;DR, main ideas, and key findings.
2. Read the [digest](digest.md) (~10 min) for the full argument in twelve verbatim bullet sections plus the five-move arc.
3. Work through the wiki pages in order for per-chunk detail, then test yourself with the questions and check the explainer and critical analysis for plain-language and evaluative views.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, ideas, findings, future directions.
- [Digest](digest.md) — twelve verbatim sections plus the argument in five moves.
- [Explainer](explainer.md) — plain-language guide with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — fifteen retrieval-practice questions covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01-evoontology-overview](wiki/01-evoontology-overview.md) | Paper title/authorship header + Abstract opening (agent–data gap statement) + Figure 1 fragments (heterogeneous sources, ontology layer node/edge types, self-evolving Diagnose–Refine–Update–Evaluate loop) |
| [02-agent-data-gap](wiki/02-agent-data-gap.md) | Introduction (agent–data gap; raw querying vs semantic layers) + Related Work (Data Agents on Heterogeneous Data; Semantic Layers) |
| [03-architecture-overview](wiki/03-architecture-overview.md) | Figure 2 overview range per plan.md (builder agent, evolution agent, grounded ontology construction flow); cost-in-constant-currency analyse-schema OCR with fact_cost table and currency constraint conflict |
| [04-tool-layer](wiki/04-tool-layer.md) | Chunk 04-tool-2-resolve-mappings-tool-1 (Tool 2: resolve Mappings / Tool 1: browse), Figure 2 label OCR only + Figure 2 caption |
| [05-content-schema-layers](wiki/05-content-schema-layers.md) | Content Layer node/edge families; Schema Layer Γt; Tool Layer Rt fbrowse/fresolve + manifest; evidence-grounded initialization Eq. 1 with L0 = (S0, Γ0, R0); trajectory-grounded evolution opening (attribution, localized intervention, paired-validation gating Eq. 2) |
| [06-evolution-loop](wiki/06-evolution-loop.md) | Reciprocal Score formula and validation gating through DDR-Bench / InsightBench / BIRD main results to Baseline / Initial / Evolved comparison (chunk file 06 lines 1–131; Table 4 body and Figure 3 values beyond extracted lines truncated) |
| [07-experiments-main](wiki/07-experiments-main.md) | Main experimental results (overall EX scores) across benchmarks and backbones; Figure 3 primary metric under Baseline, Initial, Evolved conditions + Baseline (ReAct w/o Ontology) comparison table |
| [08-model-analysis](wiki/08-model-analysis.md) | Per-backbone analysis and insight metrics (BIRD Table 4 EX/VES, Figure 4 iterative evolution, Table 5 evolution-loop ablation, Table 7 content-family masking) |
| [09-ablation-study](wiki/09-ablation-study.md) | Table 6 caption and three reported rows (Tool-only 82.7/+13.2, Schema-only 73.1/+3.6, Full 89.5/+20.0) + Jaccard overlap heading and pairwise matrix fragments (axes garbled) |
| [10-evolution-dynamics](wiki/10-evolution-dynamics.md) | Figure 5a pairwise Jaccard overlap + Figure 5b cross-backbone transfer plus adjoining single-level ablation, structure-masking ablation, Divergence across Backbones, and Conclusion text |
| [11-efficiency-scaling](wiki/11-efficiency-scaling.md) | Figure 6 content-growth section, Table 8 cost section, Figure 7 attribution section, Figure 8 card-legality case opening |
| [12-conclusion](wiki/12-conclusion.md) | Closing recap of schema/content layers and conclusions (chunk 12: Figure 8 card-legality evolution case — Legality Status Code term, mapping, evidence, format-dependent constraint) |

## Original Source

- ArXiv PDF: [EvoOntology: A Self-Evolving Ontology Layer for Data Agents](https://arxiv.org/pdf/2609.15779)
- Local copy: [source/source.md](source/source.md)
