---
type: Paper
title: "Do Influence Tactics Matter? Investigating Prompt Framing Effects in LLM Code Generation"
description: First large-scale study operationalizing Yukl & Falbe influence tactics into prompt templates and testing them across five open-weight LLMs on LiveCodeBench and SWE-bench Verified, finding pressure framings associated with reduced correctness and security.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-23T20:31:48Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2608.11513v1
  - id: local-copy
    resource: source/source.md
tags: [prompt-framing, llm-code-generation, influence-tactics, benchmarking]
---

# Do Influence Tactics Matter? Investigating Prompt Framing Effects in LLM Code Generation

This folder covers the first large-scale empirical study of influence-induced prompt framing in code generation, which wraps identical programming tasks in workplace-psychology framings (flattery, logic, policy, pressure) and measures the effect on correctness, quality, maintainability, and security. Its headline result is cautionary: urgency and pressure phrasing was associated with lower correctness and more security warnings, while model choice mattered far more than wording overall. Use this index to navigate the summary, digest, explainer, critical analysis, self-test questions, and thirteen deep-dive wiki pages.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to prompt framing or influence tactics? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole paper, shallow
- [[digest|Digest]] — rung 2: the whole paper at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-overview-influence-tactics-prompt-framing\|Overview: Do Influence Tactics Matter in LLM Code Generation?]] | Study scope, IBQ-G-grounded tactic templates, five-model two-benchmark design, and the headline pressure/correctness finding |
| [[wiki/02-influence-tactics-background-taxonomy\|Influence Tactics Background and Taxonomy]] | Kipnis-to-Yukl taxonomy evolution, Lee et al. meta-analytic evidence, LLM code-defect literature, and the structural prompt-engineering gap |
| [[wiki/03-pragmatic-prompting-theory\|Pragmatic Prompting Theory]] | Distributional-cue interpretation, non-uniformity expectation, style/role/emotion prompting precedents, RQ1–RQ3 and the four-phase design |
| [[wiki/04-study-design-datasets\|Study Design: Datasets]] | LiveCodeBench release_v6 and SWE-bench Verified datasets, IBQ-G tactic exclusions, nine prompt scenarios, and the five-model execution plan |
| [[wiki/05-prompt-templates-tactics\|Prompt Templates for Influence Tactics (Table 2)]] | Dual-benchmark prompt templates per tactic with IBQ-G item indices, including Pressure variants and the Neutral baseline |
| [[wiki/06-evaluation-metrics-models\|Evaluation: Code Quality and Maintainability Metrics]] | CC, MI, PyLint, SLOC/comment density, and Bandit metrics; SWE-bench delta aggregation and relative-signal reading |
| [[wiki/07-prompt-structure-execution\|Prompt Structure and Execution Setup (Fig. 2)]] | Common prompt structure, ~123k/~57k generation scale, decoding settings, extraction scripts, harnesses, and mixed-model statistics |
| [[wiki/08-quantitative-results-overview\|Quantitative Results Overview]] | IRR-stabilized coding rounds, Table 5 tactic-significance summary per benchmark, and validity limits |
| [[wiki/09-functional-correctness-results\|Functional Correctness Results]] | Neutral-vs-Pressure correctness and security contrasts on LiveCodeBench, the Llama 3.1 worked example, and the SWE-bench SLOC exception |
| [[wiki/10-qualitative-codebook\|Qualitative Codebook (Table 6)]] | 13-topic response codebook and tactic-linked style, documentation, error-handling, and hallucination patterns |
| [[wiki/11-discussion-implications\|Discussion and Implications]] | Minor-but-real framing effects, model-choice dominance, the pressure caution, and benign-vs-adversarial scope |
| [[wiki/12-references-a-m\|References A–M]] | Bibliography refs 1–34: model reports, code benchmarks, influence-tactics literature, prompting work, and quality tooling |
| [[wiki/13-references-l-z\|References L–Z and Authorship]] | Bibliography refs 37–82 plus the five-author UBC block; back matter with no findings |

## Original Source

- [Do Influence Tactics Matter? Investigating Prompt Framing Effects in LLM Code Generation](https://arxiv.org/abs/2608.11513v1) — arXiv abstract page (v1)
- [source/source.md](source/source.md) — local copy of the source text
