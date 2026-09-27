# Task: chapter 05 writeup — LLM-as-judge (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/05_findings.md`, `project/runs/05_judge_scorecard.md`,
`project/runs/05_judge_disagreements.md` (first 40 lines), `project/runs/results.md`,
`project/src/evals_tutorial/judge.py` (excerpts) and ONE `prompts/judge_*_v2.txt`,
`research/SOURCES_practitioner.md` (sections on LLM-as-judge and the Husain/Yan/Anthropic disagreements
only), and — for style only — `04_code_graded_evals.md`. Nothing else
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The judges are built, aligned and measured (previous task); the chapter is missing.

## Fix
Create `05_llm_as_judge.md` (`# 05 — LLM-as-judge: …`, "## What you will learn"): what an LLM judge is
and why it is *itself a model that needs evaluation*; reference-aware (chapter 03) vs reference-free
judges; one binary judge per failure mode with a critique — and why binary + critique beats a 1–5 score
(Husain FAQ; Yan "LLM-evaluators"; Zheng et al. 2023 on Likert pile-up), shown with our Likert
distribution and AUROC; the alignment loop as a mermaid diagram (labels → judge v1 → TPR/TNR on dev →
edit prompt / add few-shot → v2 → freeze → test); the scorecard table with real numbers and the honest
reading of TPR vs TNR (a judge that says "pass" to everything has TNR ≈ 0); Cohen's kappa in one
paragraph; the nocontext ablation; the disagreement review — who was wrong, with two quoted critiques;
the Anthropic view (rubrics, "grade the outcome not the path"); cost: calls and seconds per ticket, and
the argument for judging a sample in production. "What landed in the results table". Troubleshooting
(verdict before critique → worse; few-shot examples leak into test → choose from dev only; judge
agrees with itself but not with labels → labels or definition problem); Exercises (write a v3 for the
weakest mode; judge `dev` twice at temperature 0.7 and measure self-agreement); `Next:` → chapter 06.

## Tests
`test -s 05_llm_as_judge.md && grep -c "What you will learn" 05_llm_as_judge.md && grep -ci "kappa" 05_llm_as_judge.md && grep -ci troubleshooting 05_llm_as_judge.md`

## DoD
As in COMMON.md. Commit: `05_llm_as_judge.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/05_llm_as_judge.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code or runs; numbers only from committed files. Do not edit `index.md`. Context budget ≈ 40k tokens.
Do not run `fleet serve restart` or `fleet run`.
