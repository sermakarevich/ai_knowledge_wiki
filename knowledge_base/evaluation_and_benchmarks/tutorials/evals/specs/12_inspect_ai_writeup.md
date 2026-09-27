# Task: chapter 12 writeup — Inspect AI (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/12_findings.md`, `project/runs/12_reconcile.md`,
`project/runs/results.md`, `project/src/evals_tutorial/inspect_tasks.py` (excerpts),
`project/runs/12_inspect/log_excerpt.json`, `research/SOURCES_tools.md` (Inspect entry only), and — for
style only — `11_model_benchmarks.md`. Nothing else (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The Inspect tasks ran and were reconciled (previous task); the chapter does not exist.

## Fix
Create `12_inspect_ai.md` (`# 12 — Inspect AI: …`, "## What you will learn"): the dataset → solver →
scorer model with a mermaid diagram; the helpdesk task code excerpt (custom solver injecting our
retrieval, the three scorers) and the exact run command; the log viewer (what it shows, how to start it
on port 7575, the log excerpt); built-in scorers vs model-graded (which template text we reused and
why frozen); the results with CIs; **reconciliation** with chapter 05 (same judge wording, kappa, the
disagreements and their causes) and with chapter 11 (GSM8K, harness vs Inspect, extraction/template
differences) — the lesson that "the same eval" in two frameworks is rarely the same; when a framework
beats a hand-rolled harness (logs, retries, parallelism, sharing) and when it does not (custom data
contracts, alignment loop). "What landed in the results table". "Advantages and disadvantages" table for
Inspect AI grounded in the findings. Troubleshooting (provider/base URL env; grader template
placeholders; log dir growth); Exercises (add a `model_graded_fact` scorer; run the agent tasks of
chapter 10 as an Inspect `react` agent); `Next:` → chapter 13.

## Tests
`test -s 12_inspect_ai.md && grep -c "What you will learn" 12_inspect_ai.md && grep -ci "scorer" 12_inspect_ai.md && grep -ci "advantages and disadvantages" 12_inspect_ai.md`

## DoD
As in COMMON.md. Commit: `12_inspect_ai.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/12_inspect_ai.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code or runs; numbers only from committed files. Do not edit `index.md`. Context budget ≈ 40k tokens.
Do not run `fleet serve restart` or `fleet run`.
