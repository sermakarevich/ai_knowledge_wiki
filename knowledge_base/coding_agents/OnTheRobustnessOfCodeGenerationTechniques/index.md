---
type: Paper
title: 'On the Robustness of Code Generation Techniques:'
description: Empirical study of GitHub Copilot on 892 Java methods showing ~46% of semantically equivalent paraphrased descriptions change the recommendation, with automated paraphrasers viable as robustness probes and both CodeBLEU and tests imperfect evaluators.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-23T21:36:37Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2302.00438v1
  - id: local-copy
    resource: source/source.md
tags: [code-generation, github-copilot, robustness, evaluation]
---

# On the Robustness of Code Generation Techniques:

This folder distils an empirical study of GitHub Copilot asking whether semantically equivalent descriptions produce equivalent code. Across 892 high-coverage Java methods, about 46% of paraphrased descriptions changed the recommendation, sometimes gaining or losing a correct solution. Use the summary for the headline result, the digest and wiki pages for the method-by-method evidence, and the explainer and critical analysis for plain-language and skeptical views.

## How to work through this

Three depths — stop at whichever answers your question:

1. [Summary](summary.md) (~2 min) — the whole paper, shallow: problem, ideas, findings, takeaways.
2. [Digest](digest.md) (~10 min) — the whole paper, medium: one headline plus key points per wiki section, plus the argument in five moves.
3. Wiki pages below (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

New to the topic? Start with [the plain-language explainer](explainer.md) instead. Coming back after a break? Read [the digest](digest.md), then [self-test](questions.md) — do not re-read the wiki.

## Read This Folder

- [Summary](summary.md) — rung 1: the whole paper, shallow
- [Digest](digest.md) — rung 2: the whole paper at medium depth; the file to re-read on review
- [Explainer](explainer.md) — plain-language explanation, applications, conclusions
- [Critical Thinking](critical_thinking.md) — claims vs. evidence, applicability, what it changes, verdict
- [Questions](questions.md) — retrieval-practice questions; answer from memory before re-reading anything

## Wiki

| Page | Covers |
|------|--------|
| [01 — Overview and Research Questions](wiki/01-overview-and-research-questions.md) | Paper framing: title/abstract, robustness question for Copilot code generation |
| [02 — Study Design and Data Collection](wiki/02-study-design-and-data-collection.md) | RQ0–RQ1, 892 Java methods, PEGASUS/TP/manual paraphrases, Full vs Non-full Copilot invocations |
| [03 — Data Analysis Metrics](wiki/03-data-analysis-metrics.md) | NTLev description distance, CodeBLEU/code-Levenshtein, RQ0 equivalence rates, replication package |
| [04 — Illustrative Examples](wiki/04-illustrative-examples.md) | Fig. 4 target vs recommended methods, CodeBLEU 0.45 passing case, generation outcome counts |
| [05 — Results: CodeBLEU and Tests](wiki/05-results-codebleu-and-tests.md) | CodeBLEU/test distributions, Fig. 4–6, 408/892 (46%) paraphrase impact, Answer to RQ1, threats |
| [06 — Discussion](wiki/06-discussion.md) | Training-data overlap, Java/high-coverage limits, Fig. 6, prior empirical work on recommenders |
| [07 — Implications and Conclusions](wiki/07-implications-conclusions.md) | Copilot literature, ~46% different recommendations, proper-description implication, future work |

## Original Source

- [Original paper on arXiv](https://arxiv.org/abs/2302.00438v1) — On the Robustness of Code Generation Techniques: An Empirical Study on GitHub Copilot (v1).
- [Local copy](source/source.md) — full source text stored with this folder.
