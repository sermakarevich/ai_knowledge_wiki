> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Evaluation: Code Quality and Maintainability Metrics
**In one sentence:** The study measures non-functional quality with Cyclomatic Complexity, Maintainability Index, PyLint, SLOC/comment density, and Bandit security counts — computed directly for LiveCodeBench but as pre/post-patch deltas for multi-file SWE-bench Verified patches (successful patches only) — and treats them strictly as relative comparison signals across prompt conditions, not absolute quality judgments.
## Key points
- Non-functional quality is measured with Cyclomatic Complexity (CC) [39], Maintainability Index (MI) [43], and PyLint [14], plus Source Lines of Code (SLOC) and comment percentage (comments / SLOC × 100%) for verbosity and documentation density.
- CC is computed with Radon [34] as both CCavg (mean across all functions/methods) and CCmax (single most complex block, the primary maintenance bottleneck); MI is computed with Radon as a single score where higher values denote easier maintainability.
- PyLint uses default parameters for LiveCodeBench but disables import-error, no-name-in-module, wrong-import-position, and ungrouped-imports for SWE-bench Verified to avoid failing imports from files missing as context.
- Security is measured with Bandit [47] counts at low, medium, and high severity, using post-minus-pre-patch differences to isolate the effect of the model's edits.
- For multi-file SWE-bench Verified patches, CC is pooled across blocks in all modified files (CCavg as pooled mean, CCmax as pooled max), MI as mean-across-files delta, and PyLint/Bandit as whole-input post-minus-pre deltas, following Chen & Jiang (2025) [10].
- Only successful (compiling, validation-passing) SWE-bench Verified patches enter metric analysis, with valid-python rates of 28% (Llama 3.1 8B) versus 57% (DeepSeek R1 Distill Llama 70B); patches creating only a new file are skipped.
- Metrics are explicitly relative signals, not standalone quality judgments, because metric assessments can diverge from perceived quality [44] and readability/structure/comprehensibility resist static capture [6]; a qualitative codebook analysis (tone, structure, explanations, commenting, error handling, hallucinations) complements them.
- Tactic framings prefix the problem statement (SWE-bench Verified uses 'prompt-style-3' plus git-diff formatting rules); 15 SWE-bench instances were excluded for context overflow or non-running Docker images, with three inference rounds per tactic for non-reasoning models and one round for DeepSeek R1 Distill Llama 70B across nine prompt conditions.
---
## Metric rationale and interpretation
**Covers:** Section 3.4 intro (Code Quality and Maintainability Metrics)

Non-functional quality is evaluated with static-analysis measures common in software engineering research: CC [39], MI [43], PyLint [14], plus SLOC and comment percentage (comments / SLOC × 100%).

> "Metrics are useful because they provide automatically computable, reproducible signals that can help estimate different aspects of code."

Supporting evidence cited: Chowdhury et al. show code metrics improved change-proneness prediction across 730K Java methods from 47 open-source projects even after controlling for method size [12], and practitioners perceive complexity as negatively influencing readability, understandability, modifiability, and maintenance time [2].

Interpretation rule stated verbatim in spirit:

> "We account for these concerns by avoiding the interpretation of metric values as standalone judgments of code quality. Instead, we use these metrics to analyze relative differences across prompt conditions under the same evaluation procedure."

## Cyclomatic Complexity and Maintainability Index
**Covers:** Section 3.4 (CC and MI definitions)

| Metric | Definition given | Tool | Reported form |
|---|---|---|---|
| Cyclomatic Complexity (CC, McCabe [39]) | Number of linearly independent paths in a program | Radon [34] | CCavg (mean across functions/methods) and CCmax (single most complex block, "often represents the primary maintenance bottleneck") |
| Maintainability Index (MI) [43] | Aggregates lines of code, complexity, and comment density into one score; higher values denote easier maintainability | Radon [34] | Single file/block score |

## PyLint, SLOC, and documentation density
**Covers:** Section 3.4 (PyLint, SLOC, comments)

PyLint [14] is described as "an overall assessment of a file's errors and adherence to code standards."

| Dataset | PyLint configuration |
|---|---|
| LiveCodeBench | PyLint library with default parameters |
| SWE-bench Verified | Same but with import-error, no-name-in-module, wrong-import-position, and ungrouped-imports disabled, "in order to avoid complications due to failing imports from other files potentially missing as context" |

SLOC and comment percentage quantify verbosity and documentation density.

## Security: Bandit
**Covers:** Section 3.4 (Security)

Security is evaluated with Bandit [47], "a static analysis tool that detects common Python vulnerabilities and classifies them as low, medium, or high severity." For each solution the chunk records total counts and post-minus-pre-patch differences, following Chen & Jiang (2025) [10], so "differences allows us to isolate the effect of the model's edits by comparing the differences between the pre-patch and post-patch files."

## Multi-file metric aggregation (SWE-bench Verified)
**Covers:** Section 3.4 (Multi-File Metric Aggregation)

LiveCodeBench metrics are computed on the full extracted code block; SWE-bench Verified uses pre/post-patch differences (∆) to isolate generated edits:

- ∆CCavg = mean of pooled per-block CC over Bpost minus mean over Bpre, where B is all code blocks (functions, methods, classes) across modified files.
- ∆CCmax = max CC over Bpost minus max CC over Bpre.
- ∆MI = MIavg(post) − MIavg(pre), where MIavg is the average maintainability across files.
- ∆PyLint = PyLint(post) − PyLint(pre), computed on all files at once before and after edits.
- ∆Bandit_s = Σ|Issues_s(post)(f)| − Σ|Issues_s(pre)(f)| over files f ∈ F, for each severity s ∈ {high, medium, low}.

## Validity filtering
**Covers:** Section 3.4 (SWE-bench Verified inclusion criteria)

> "For SWE-bench Verified, only successful patches (i.e., those that compiled and passed validation tests) were included in these analyses. Non-successful patches were excluded from the statistical analysis of metrics."

Reason: failed/non-compiling/non-parsable patches make pre/post comparisons less comparable and some metrics incalculable; the restriction "reduces the sample size and may bias effect estimates, but strengthens our internal validity by minimizing noise from non-parsable code." Exact rates given: "Llama 3.1 8B has a valid python rate of 28%, while the best and most compute-heavy model, DeepSeek R1 Distill Llama 70B, has a valid python rate of 57%." New-file-only case: "if the only modification is in a newly created file, then it is skipped. Otherwise, metrics are reported for the modified files only."

## Metric limitations
**Covers:** Section 3.4 (Metric limitations)

> "These metrics serve as interpretable proxies rather than exhaustive measures of software quality."

Mapping given: MI and CC emphasize structural maintainability risks; PyLint captures style and static code-quality conventions; SLOC and comment percentage capture verbosity and documentation; Bandit detects only rule-based security vulnerabilities. "No single metric is fully aligned with a professional developer's assessment of whether a snippet is maintainable or high-quality in a production context," so results are interpreted as relative comparisons under the same tasks, models, and procedure. The quantitative metrics are complemented by "a qualitative code-book analysis that captures higher-level stylistic and behavioural patterns," covering "communication style, tone, response structure, presence of code explanations, readability, commenting quality, error handling, and hallucination patterns."

## Experiment setting tail in this chunk
**Covers:** Section 3.5 (Prompt Integration; Model Inference; Fig. 2 prompt structure)

Prompt integration: tactic framings prefix each problem statement (Figure 2); SWE-bench Verified uses the built-in 'prompt-style-3' template with tactic framings in the instruction context, chosen because "it supplies the most helpful structure and an example patch," plus explicit git-diff formatting rules for patch validity. Model inference: "A small subset of SWE-bench tasks (15 instances) was excluded due to context-length overflow or non-running Docker images"; three inference rounds per tactic for non-reasoning models and one round per tactic for the reasoning model (DeepSeek R1 Distill Llama 70B) "due to its higher computational cost, as it generates significantly more tokens"; each model covers all nine prompt conditions across both datasets. Figure 2 (partially in chunk) shows the tactic-influenced prompt structure: tactical influence framing, problem statement/inputs, GitHub codebase, example explanation, patch example (`--- a/file.py` / `+++ b/file.py`), and output formatting with "IMPORTANT DIFF RULES" hunk headers.

**Covers:** Sections 3.4–3.5 (code quality/maintainability metrics: CC, MI, PyLint, SLOC/comments, Bandit; multi-file ∆ aggregation; validity filtering; limitations; prompt integration and inference rounds)
