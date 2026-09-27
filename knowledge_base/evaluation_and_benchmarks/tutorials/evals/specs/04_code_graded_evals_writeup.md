# Task: chapter 04 writeup — code-graded evals (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/04_findings.md`, `project/runs/results.md`,
`project/src/evals_tutorial/{results,code_evals}.py` (excerpts), `research/SOURCES_practitioner.md`
(sections on the three levels of evaluation and on "metrics that don't correlate with quality" only),
and — for style only — `03_look_at_your_data.md`. Nothing else
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The code-graded evals and the results plumbing exist and ran (previous task); the chapter does not.

## Fix
Create `04_code_graded_evals.md` (`# 04 — Code-graded evals: …`, "## What you will learn"): the three
levels of evaluation (unit tests / model-and-human review / A-B tests — Hamel Husain 2024) and where this
chapter sits; the results plumbing (`metrics.json` schema from `index.md`, `just results`, why one table);
`triage` as a classification problem — accuracy vs macro-F1, the confusion matrix picture and the two
most confused categories explained with a ticket; JSON-validity as the cheapest gate; verifiable
instructions (IFEval, Zhou et al. 2023) and our check table with real pass rates; keyword assertions as
a cheap proxy for "covers the answer points" and where they lie; ROUGE-L and embedding similarity —
show the AUROC against the chapter-03 labels and the two counter-examples, and conclude honestly what
they are good for (regression detection) and not good for (quality); how to run these as `pytest`
(a short example test that asserts a threshold on a committed `metrics.json`). Mermaid: trace →
assertions → metrics.json → results.md. "What landed in the results table" with the three rows.
Troubleshooting (JSON parse failures from thinking tokens; confusion matrix unreadable → sort by
frequency; embedding cache misses → tunnel down); Exercises (add a check for "asks a clarifying
question when scenario is ambiguous"; compute F1 per priority); `Next:` → chapter 05.

## Tests
`test -s 04_code_graded_evals.md && grep -c "What you will learn" 04_code_graded_evals.md && grep -ci "results table" 04_code_graded_evals.md && grep -ci troubleshooting 04_code_graded_evals.md`

## DoD
As in COMMON.md. Commit: `04_code_graded_evals.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/04_code_graded_evals.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code or runs; numbers only from the findings note and `results.md`. Do not edit `index.md`.
Context budget ≈ 40k tokens. Do not run `fleet serve restart` or `fleet run`.
