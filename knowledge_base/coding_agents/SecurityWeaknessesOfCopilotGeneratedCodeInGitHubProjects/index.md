---
type: Paper
title: "Security Weaknesses of Copilot-Generated Code in GitHub Projects: An Empirical Study"
description: Empirical study of 733 Copilot/CodeWhisperer/Codeium-generated Python and JavaScript snippets from GitHub finds 27.3% contain security weaknesses across 43 CWE types, and Copilot Chat fixes up to 55.5% when fed static-analysis warnings.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-23T20:48:36Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2310.02059v4
  - id: local-copy
    resource: source/source.md
tags: [github-copilot, static-analysis, cwe, ai-generated-code]
---

# Security Weaknesses of Copilot-Generated Code in GitHub Projects: An Empirical Study

Fu et al. (arXiv:2310.02059v4) mine GitHub for 733 Python and JavaScript snippets developers attributed to Copilot, CodeWhisperer, and Codeium, scan them with CodeQL plus Bandit/ESLint, and find 27.3% hold confirmed weaknesses averaging three per vulnerable snippet. A Copilot Chat repair experiment shows warning-fed prompts fix 55.5% of weaknesses, with stark per-CWE variance from near-total repair to zero.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to AI code assistants or CWE categories? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole paper, shallow
- [[digest|Digest]] — rung 2: the whole paper at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-abstract-introduction\|Abstract and Introduction]] | Headline results: 733 snippets, 29.5% Python / 24.2% JS weak, 43 CWEs, 55.5% fixable with warnings |
| [[wiki/02-background-copilot-usage\|Background: Copilot Usage and Related Work]] | Study scope vs. Pearce et al.; functional and security prior work on code generators |
| [[wiki/03-static-analysis-background\|Static Analysis Background]] | Static vs. dynamic analysis trade-offs; CodeQL + Bandit/ESLint multi-tool rationale |
| [[wiki/04-research-questions-design\|Research Questions and Study Design]] | RQ3 fix-loop; GitHub keyword search, 3,589 deduplicated hits, Kappa 0.84 filtering |
| [[wiki/05-data-collection-filtering\|Data Collection, Labeling Agreement, and Filtering]] | 116 Repo-label projects + 335 Code-label files; 733-file dataset, small low-star projects |
| [[wiki/06-dataset-characteristics\|Dataset Characteristics]] | File sizes (mean 183 LoC) and six application domains per language; dual-tool scanning |
| [[wiki/07-methodology-scan-and-fix\|Scanning Methodology and Copilot Chat Fix Setup]] | Warning/Error verification; 90-snippet / 295-weakness repair subset, three prompt treatments |
| [[wiki/08-rq1-prevalence\|RQ1: Prevalence]] | 200/733 (27.3%) vulnerable; 628 weaknesses, ~3 per snippet, 102 multi-issue snippets |
| [[wiki/09-cwe-classification\|CWE Classification]] | Manual CWE mapping (Kappa 0.82); 43 types led by CWE-330, 233 in Top-25 |
| [[wiki/10-cwe-distribution-by-language\|CWE Distribution by Language]] | Top-5 CWE ranks per language; per-domain Fig. 14/15; RQ3 fix-rate preview |
| [[wiki/11-rq3-copilot-chat-fixes\|RQ3: Copilot Chat Fixes]] | Per-CWE fix counts for /fix vs. basic vs. enhanced prompts; zero-fix CWE list |
| [[wiki/12-discussion-top-cwes\|Discussion: Top CWEs and Severity]] | Top-25 vs. rare CWEs; domain and language risk patterns |
| [[wiki/13-implications-prevention\|Prevention of Security Weaknesses]] | Five preventive practices: targeted, standardized, prompt-aware, complexity-matched repair |
| [[wiki/14-threats-conclusion-references\|Threats, Conclusion and References]] | Bibliography entries [1]–[43]; no threats/conclusion body text present |
| [[wiki/15-appendix-back-matter\|Appendix and Back Matter]] | Bibliography tail [44]–[84]; ACM TOSEM February 2025 back matter |

## Original Source

- [arXiv:2310.02059v4](https://arxiv.org/abs/2310.02059v4) — Paper source
- [source/source.md](source/source.md) — Local copy of the paper source
