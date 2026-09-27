> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# From Restructuring to Stabilization: Overview
**In one sentence:** A large-scale experiment iteratively refactoring 230 Java snippets with GPT-5.1 over five iterations under three prompts finds a consistent "restructuring, then stabilizing" dynamic that converges toward an apparently internalized notion of readable code, robust across degraded starting variants and only slightly steered by targeted prompts.
## Key points
- Large-scale design: 230 Java files from TheAlgorithms-Java × 3 variants (Original, Meaningless, NoComment) × 3 prompts × 5 iterations = 10,350 generated snippets, using GPT-5.1 at temperature 0 with stateless API calls.
- Main dynamic (RQ1, Original + PromptGeneral): unchanged lines rise 45% (v0→v1) → 76% → 86% → 89% → 92% (v4→v5), with early restructuring (9% renames, 11% code insertions in v0→v1) fading to no dominant type and all types <1% later.
- Structural drift on already-good code: code lines rise 58 → over 73 (v0→v5), empty lines and method counts rise and stabilize from v3 onward, comment lines fall slowly and inline comments are almost completely removed.
- Convergence without full stability: adjacent-version changed-line similarity rises 0.86 (v0→v1) → 0.90 (v4→v5), early-to-late pairs (v1→v4 = 0.87, v2→v5 = 0.88) show early convergence, but no pair reaches 1.00, indicating persistent micro-changes / over-refactoring tendency.
- Robustness across degraded inputs (RQ2): Meaningless starts at 31% unchanged (v0→v1, 24% renames) and NoComment at 44% unchanged (14% renames), then both follow the Original trajectory to 90% and 89% unchanged by v4→v5, with code lines converging 56 → ~73 and methods 3.1 → ~6 across all variants.
- Prompting and guardrails: targeted prompts steer change types without altering overall convergence, naming-focused prompts may induce oscillatory renaming, and functionality breaks are rare but non-zero per iteration, motivating explicit stopping criteria and care with valuable comments.
---
## Abstract and framing
Paper: "From Restructuring to Stabilization: A Large-Scale Experiment on Iterative Code Readability Refactoring with Large Language Models" — Norman Peitek, Julia Hess, Sven Apel (Saarland University), arXiv:2602.21833v1 [cs.SE] 25 Feb 2026.
> "Our results reveal three main insights: First, iterative code refactoring exhibits an initial phase of restructuring followed by stabilization. This convergence tendency suggests that LLMs possess an internalized understanding of an "optimally readable" version of code. Second, convergence patterns are fairly robust across different code variants. Third, explicit prompting toward specific readability factors slightly influences the refactoring dynamics."
Contributions claimed: (1) empirical evidence of convergence with occasional back-and-forth changes; (2) insights on prompt-strategy influence and need for careful prompt engineering; (3) reusable LLM-agnostic framework (sequence-, token-, AST-based similarity + DiffParser) for exact and non-exact replication across models; (4) online replication package at https://github.com/brains-on-code/IterativeRefactoringLLM.
Research gap: prior work shows single-shot refactoring ability but not what happens when LLMs repeatedly refactor their own outputs — convergence to stable higher-quality solutions versus superficial/oscillating/regressive changes — nor how unguided vs. targeted prompts or varying initial quality affect multi-iteration trajectories.

## 1 Introduction
Motivation: readable code eases maintenance, debugging, and collaboration; poorly written code raises costs and bug risk; LLMs promise to generate clear code and to transform convoluted human/AI code into readable versions, but "Do LLMs truly have the capability to refactor code meaningfully and in a consistent way?"
Previewed findings in chunk: "restructuring, then stabilizing" — early iterations make substantial changes (identifier renaming, decomposition into more methods, comment pruning), later iterations converge; holds even for degraded inputs (meaningless identifiers, removed comments) with starting-point-dependent changes; targeted prompts steer change types without altering convergence; naming-focused prompts may oscillate; functionality breaks rare but non-zero; follow-ups support robustness.
Practical takeaways previewed: LLMs can normalize diverse snippets toward consistent style but need guardrails — explicit stopping criteria against over-refactoring, careful prompt phrasing against rename oscillations, mechanisms to preserve valuable explanatory comments.

## 2 Background and Related Work
Program comprehension (Sec. 2.1): cognitive processes (pattern recognition, memory retrieval, abstraction); experts use top-down hypothesis-then-verify, novices bottom-up; methods from self-reports/observation to eye-tracking, fMRI/EEG.
Readability models (Sec. 2.2): readability as ease of understanding, driven by naming, indentation, comments, syntactic simplicity; heuristics (Halstead, McCabe cyclomatic complexity) miss subjectivity/context; ML models add hand-crafted features (line length, identifier complexity, indentation) plus empirical ratings; transformers (CodeBERT, GraphCodeBERT) learn semantic representations; trend toward IDE real-time feedback and LLM dynamic refactoring suggestions.
LLMs in SE (Sec. 2.3): Zheng et al. survey 123 papers — strength in syntactic tasks (summarization), weakness in deep semantic tasks (complex generation, vulnerability detection); Hou et al. note decoder-only dominance in generation/completion and call for better datasets/metrics.
Code generation: Tian et al. — ChatGPT good on common problems, weak on unseen challenges, repair limited by attention span/problem description; Jin et al. (DevGPT) — output suits demos/docs, needs modification for production; Liu et al. — correct pre-2021 but drops on newer problems, multi-iteration fixing raises complexity without fully fixing function, ~half of generated code has maintainability issues (style, needless complexity) and feedback fixes often introduce new problems.
Code refactoring: Martinez et al. (50 papers) — hard to objectively judge "preferable," so indirect proxies (fewer smells, lower cyclomatic complexity, human judgment); Yu et al. — high erroneous self-assessment in self-verification; AlOmar et al. (DevGPT) — programmers use generic refactoring requests while LLMs state intentions (maintainability, readability); DePalma et al. — 319/320 successful trials on 40 Java segments × 8 attributes but superficial on complex tasks, repository-level benchmark success low; Guo et al. — GPT-3.5/4 beat CodeReviewer (CodeT5) on new code-review dataset with low temperature and concise scenario prompts; Hu et al. — models depend on semantic cues, poor on obfuscated/semantically-degraded code; Liu et al. CodeQUEST (GPT-4o evaluator+optimizer, 42 Python/JS examples) — gains in 41 cases, mostly early iterations, better metric alignment, but subjective/stochastic.
Synthesis quoted: "(1) the need for human oversight and the development of more sophisticated verification mechanisms before LLMs can be trusted fully; (2) programmers need to craft more specific prompts to maximize the effectiveness of LLMs in refactoring tasks; and (3) we must investigate the role of LLMs in improving code quality and readability, particularly in the context of automated refactoring."

## 3 Methodology
Research questions (verbatim):
> RQ1: "How do iterative refactoring by LLMs evolve when provided with a code snippet that already adheres to best practices for code readability?"
> RQ2: "When multiple variations of the same code snippet—each changed with respect to a code readability aspect—are independently of each other iteratively refactored, do they converge after a certain number of iterations?"
> RQ3: "Do targeted refactoring become more effective when the prompt explicitly emphasizes a readability aspect?"
Operationalization: RQ1/RQ2 via change counts/types (implementation sub-types access/call/control/literal/operator/other-structural; syntax-only; renames; comment; mixed) and structural stability (total/code/comment/inline-comment/empty lines, method count); RQ2 via unchanged-line proportion, average changed-line similarity, absolute-value correspondence, insertions/deletions per iteration plus cross-variant comparison; RQ3 via same metrics plus hypothesis of stronger aspect alignment and faster stabilization.
Sampling: criteria (1) 50–200 LOC, (2) 1–3 methods per 50 lines, (3) ≥50% code lines, (4) best-practice quality; source TheAlgorithms-Java (diverse algorithms, educational formatting, MIT, reproducible).

Table 1. Distribution of .java files across LOC intervals (valid = meets methods + code/comments ratios):

| LOC Interval | # Files | # Methods Ratio | # Code/Comments Ratio | # Valid Files |
|---|---|---|---|---|
| 0–49 | 209 | 202 | 150 | 143 |
| 50–99 | 287 | 227 | 187 | 148 |
| 100–149 | 75 | 56 | 60 | 45 |
| 150–199 | 45 | 32 | 38 | 28 |
| 200–249 | 18 | 9 | 17 | 9 |
| > 250 | 24 | 13 | 4 | 3 |

230 of 658 files met all criteria. Each yielded three variants: Original (unchanged); Meaningless (variable/method/class names plus JavaDoc/comment content made meaningless, structure preserved); NoComment (all JavaDocs, block and inline comments removed).

Table 2. Wording of the three prompts:

| Prompt ID | Prompt Type | Exact Prompt Wording |
|---|---|---|
| PromptGeneral | Unguided | "Refactor this code for improved readability." |
| PromptMeaning | Targeted | "Refactor this code for improved readability, especially with respect to identifier naming." |
| PromptComments | Targeted | "Refactor this code for improved readability, especially with respect to comments." |

RQ1/RQ2 use PromptGeneral; RQ3 adds PromptMeaning/PromptComments. API: temperature = 0, full gpt-5.1, stateless requests. Total: 230 × 3 variants × 3 prompts × 5 iterations = 10,350 snippets.
DiffParser tool: custom Python scripts output (1) removed-added line-pair mapping, (2) deletions, (3) insertions — full line-level classification.

Table 3. Absolute metric values, exemplary snippet MaximumSumOfNonAdjacentElements in Original:

| Version | Prompt | Total Lines | Code Lines | Comment Lines | Inline Comments | Empty Lines | Methods |
|---|---|---|---|---|---|---|---|
| 0 | — | 95 | 41 | 35 | 3 | 19 | 2 |
| 1 | PromptGeneral | 82 | 42 | 27 | 0 | 13 | 2 |
| 1 | PromptMeaning | 81 | 41 | 23 | 0 | 17 | 2 |
| 1 | PromptComments | 88 | 40 | 36 | 0 | 12 | 2 |
| 2 | PromptGeneral | 90 | 47 | 27 | 0 | 16 | 4 |
| 2 | PromptMeaning | 79 | 41 | 21 | 0 | 17 | 2 |
| 2 | PromptComments | 94 | 40 | 42 | 8 | 12 | 2 |

Comparison metrics: unchanged lines; changed-line types (Rename; SyntaxOnly; CommentChange; MixedChange; CodeChange sub-types Access/Call/Control/Literal/Operator/OtherStructural); average changed-line similarity sim = (1/n) Σ sim(li, li′); total insertions/deletions split into code/comment/empty lines; relative changes of absolute values.
Comparison strategies: Horizontal (same variant across versions, each version vs. all preceding to catch back-and-forth where v0 = v2 ≠ v1 gives sim(v0,v2) = 1.0 > sim(v0,v1) = sim(v1,v2) < 1); Vertical (variants within same version); Combined (whether variants converge to an "optimal variant" over iterations).

## 4 Results — RQ1 Evolution (Original, PromptGeneral)
Absolute metrics (Fig. 4): v0→v1 total lines rise via sharp empty-line plus code-line increase; comment lines fall slowly, inline comments nearly eliminated; code lines 58 → over 73 by v5; empty lines and method counts rise and stabilize from v3 onward.
Change dynamics (Fig. 5): unchanged 45% → 76% → 86% → 89% → 92%; v0→v1 largest single types renaming (9%) and code insertions (11%); v1→v2 more targeted/balanced at lower frequencies; v2→v3 onward most types <1%, no dominant type. Flow view (Fig. 6): renames and semantic (CodeChange-sum) dominate early and persist; comment/syntax-only/mixed less frequent, more even — diverse types stay active even when marginal late.
Similarity (Fig. 7 heatmap): adjacent similarity 0.86 (v0→v1) → 0.90 (v4→v5); non-consecutive v0→v5 = 0.84; v1→v4 = 0.87, v2→v5 = 0.88; never 1.00.
> "The results show that the iterative refactorings of already well-structured code (Original) largely preserve the original structure and exhibit a clear convergence trajectory. However, the LLM did not strictly limit itself to only necessary changes. Initial iterations introduced a noticeable restructuring phase characterized by reductions in comments, renaming operations, and additional code adjustments."

## 4 Results — RQ2 Convergence across variants (PromptGeneral)
Baseline v0 differences (Fig. 8): Original→Meaningless = 30% renames + 15% comment deletions + 15% comment insertions (full-line comment rewrites classified as delete+insert, not comment change); Original→NoComment = 67% unchanged, 28% comment-line deletions, 3% empty-line insertions (deliberate structural substitute for removed comments); Meaningless→NoComment = 32% unchanged, 35% renames, 28% comment deletions, 3% empty insertions, no CommentChange possible; other residuals ≤1% from parsing.
Absolute trajectories (Fig. 9): v0 totals Original/Meaningless ~101 lines, NoComment 72 (commentless); after v1 LLM strips many Meaningless comments, then all variants gain code + empty lines, totals stabilize at different levels driven by comment-line counts; code lines 56 → ~73 by v5 all variants; inline comments Original/Meaningless 1.3 → 0.2, NoComment 0 → ~0.2; methods 3.1 → ~6 all variants despite different paths.
Change dynamics (Fig. 10): Meaningless unchanged 31% → 65% → 80% → 87% → 90%; NoComment 44% → 71% → 82% → 87% → 89% — both mirror Original with bulk of adjustment in first two iterations. Detail: Meaningless v0→v1 24% renames → 6% in v1→v2 → ≤5% all sub-types from v2→v3; NoComment v0→v1 14% renames, no comment changes/deletions (no v0 comments), then ≤5% mostly minor renames/insertions from v2 onward. Flow (Figs. 11–12): v0→v1 dominated by systematic renames (NoComment also code + syntax-only concentration), then narrowing to small code/rename/syntax-only activity.
Similarity (Figs. 13–14): both variants show rising later-iteration similarity; Meaningless steadies after second iteration, NoComment starts higher (less initial work than Meaningless renames) and ends slightly higher; NoComment converges minimally faster with fewer structural alterations.

**Covers:** Paper title/abstract through Sec. 4.2.4 pairwise similarity (Figs. 13–14); RQ3 targeted-prompt results and Secs. 5–7 not in this chunk.
