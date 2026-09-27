---
type: Paper
title: 'CQ4OE: A benchmark for assessing LLM-assisted ontology generation from competency questions'
description: CQ4OE benchmarks LLM-generated OWL ontologies from competency questions with CQ-aligned golds (CQ2Term over 99 CQs, CQ2Onto over 118 CQs), a five-method alignment plus multi-view metric framework, and nine-LLM baselines showing vocabulary recovery far outpacing structural and hierarchy completeness.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-23T13:14:43Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.26029v1
  - id: local-copy
    resource: source/source.md
tags: [ontology-engineering, llm-evaluation, benchmarks, semantic-web]
---

# CQ4OE: A benchmark for assessing LLM-assisted ontology generation from competency questions

CQ4OE is a reusable benchmark that grades LLM-built OWL ontologies against exactly what each competency question requires, via CQ-to-term and CQ-to-axiom provenance over six source ontologies. Its two tasks (CQ2Term term prediction, CQ2Onto full-ontology structure) and explainable per-run reports show models recover explicit vocabulary reliably but collapse on properties, axioms, hierarchies, and per-question completeness. Use this folder to pick the right model per domain and layer, and to copy the minimal-sufficient-gold plus global-vs-CQ-conditioned evaluation pattern.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-cq4oe-overview-and-motivation\|CQ4OE: Overview and Motivation]] | Abstract, introduction gaps and contributions, related-work exclusion, two-task framing, source-ontology selection |
| [[wiki/02-dataset-construction-and-statistics\|Dataset construction and statistics]] | Four-phase annotation workflow, Table 1 counts, CQ2Term/CQ2Onto gold statistics, Ei/Ii/Ri terms, triple-review |
| [[wiki/03-term-alignment-and-evaluation-metrics\|Term Alignment and Evaluation Metrics]] | Five-method alignment pipeline, aggregation and thresholds, Table 2 metric overview, CQ2Term/CQ2Onto scoring, per-run reports |
| [[wiki/04-experimental-setup-and-baselines\|Experimental Setup and Baselines]] | Nine-LLM setup and three strategies, CQ2Term term recovery, CQ2Onto structure and domains, three recurrent limitations |
| [[wiki/05-cq2term-results-by-model-and-domain\|CQ2Term results by model and domain]] | Fig. 2 term-F1 and CQ-conditioned coverage, conceptualization framing vs. CQ2Onto reasoning |
| [[wiki/06-cq2onto-results-and-closure-gains\|CQ2Onto Results and Closure Gains]] | Fig. 3 structural F1 and closure rescue, provenance-traceable reuse, limitations, conclusion, resource links |
| [[wiki/07-discussion-limitations-and-references\|Discussion, limitations and references (refs 9–53)]] | Bibliography tail refs 9–53: LLM reports, OE methods, benchmarks, similarity foundations, domain ontologies |

## Original Source

- [arXiv:2609.26029v1](https://arxiv.org/abs/2609.26029v1) — paper page
- [source/source.md](source/source.md) — local copy of the source text
