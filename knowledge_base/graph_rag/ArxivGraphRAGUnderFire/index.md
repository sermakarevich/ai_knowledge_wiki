---
type: Paper
title: GraphRAG under Fire
description: The first systematic study of GraphRAG's vulnerabilities to knowledge-poisoning attacks — existing RAG attacks fail against it, but a new attack (GRAGPOISON) exploits its graph structure to poison many related queries at once, at up to 98% success rate.
generated: { by: claude/claude-sonnet-5, at: 2026-08-20T19:45:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2501.14050
  - id: local-copy
    resource: source/2501.14050.pdf
tags: [graphrag, rag-security, knowledge-poisoning, adversarial-attacks, retrieval]
---

# GraphRAG under Fire

This paper asks whether GraphRAG — the graph-based flavor of retrieval-augmented generation that indexes a corpus as entities and relations instead of flat vector chunks — is actually safer from data-poisoning attacks than plain RAG, or just differently vulnerable. The answer is both: classic RAG poisoning attacks measurably lose effectiveness against GraphRAG, but the same graph structure that neutralizes them opens a new, more scalable attack surface, exploited here by a novel attack called GRAGPOISON. It was worth ingesting because it's the first paper to characterize this specific security paradox and ships a concrete, reproducible attack with numbers.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10-15 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to GraphRAG or RAG security? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

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
| [[wiki/01-introduction-and-threat-model\|Introduction and Threat Model]] | Motivation, the security paradox, GRAGPOISON's high-level design, GraphRAG fundamentals, multi-hop reasoning, and the black-box/KG-agnostic threat model |
| [[wiki/02-rq1-existing-attacks-fail\|RQ1: Existing Attacks Fail Under GraphRAG]] | Why PoisonedRAG loses 10+ points of ASR against GraphRAG/LightRAG vs NaiveRAG, and the two indexing-time resilience mechanisms responsible |
| [[wiki/03-gragpoison-design\|GRAGPOISON Attack Design]] | The three-stage attack: relation selection (set cover), relation injection (covering narratives), and relation enhancement (ranking manipulation) |
| [[wiki/04-evaluation-results\|Evaluation Results]] | Main results table, ablations (KG-awareness, attack magnitude, injection tricks, graph scale), targeted attacks, cross-system generalization, 3-hop queries |
| [[wiki/05-defenses-related-work-conclusion\|Defenses, Related Work, and Conclusion]] | Five candidate defenses and their limits, positioning vs. prior RAG/KG attack-defense literature, and the paper's conclusion |
| [[wiki/06-appendix-notations-and-attack-examples\|Appendix: Notations, Datasets, and Worked Attack Examples]] | Formal notation, dataset construction (geographic/medical/cyber-security), full prompt templates, and three worked end-to-end attack examples |

## Original Source

- [source/2501.14050.pdf](source/2501.14050.pdf) — arXiv:2501.14050, "GraphRAG under Fire" by Jiacheng Liang, Yuhui Wang, Changjiang Li, Rongyi Zhu, Tanqiu Jiang, Neil Gong, Ting Wang (Stony Brook University, Duke University), 2025, retrieved 2026-08-20.
