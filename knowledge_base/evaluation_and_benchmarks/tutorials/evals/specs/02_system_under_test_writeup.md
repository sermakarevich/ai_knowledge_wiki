# Task: chapter 02 writeup — the system under test (markdown only, NO new code/experiments)

Read: `index.md`, `specs/COMMON.md`, `project/runs/02_findings.md`, `project/src/evals_tutorial/helpdesk.py`
and `tickets.py` (for code excerpts), the two prompt files, and — for style only — `00_setup.md`.
Nothing else (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The SUT and the ticket set exist (previous task); the chapter explaining them does not.

## Fix
Create `02_system_under_test.md` (`# 02 — The system under test: …`, "## What you will learn"): why a
tutorial on evals needs a *fixed* application with *versioned* prompts; the shop and the handbook (one
real section excerpt with its key facts); **gold labels by construction** — why generating the ticket
*from* the label gives free, reliable labels, and what it cannot give you (real user distribution; cite
Hamel's "synthetic data for cold start" and its dimensions approach); the grid and the split with the
real stats tables; `triage` (schema, prompt v1); `answer` (retrieval, context, prompt v1, citations);
the trace contract and why traces are the raw material of every later chapter; the real example traces
from the findings note; the quick triage-agreement count with an explicit "no confidence interval yet —
chapter 07"; a mermaid diagram of the SUT. Troubleshooting (JSON schema refusals; model naming sections
that were not retrieved; long tickets truncated by `num_ctx`); Exercises; `Next:` → chapter 03.

## Tests
`test -s 02_system_under_test.md && grep -c "What you will learn" 02_system_under_test.md && grep -ci troubleshooting 02_system_under_test.md && grep -ci exercises 02_system_under_test.md`

## DoD
As in COMMON.md. Commit: `02_system_under_test.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/02_system_under_test.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code changes or runs. Numbers only from the findings note and committed files. Do not edit
`index.md`. Context budget ≈ 40k tokens. Do not run `fleet serve restart` or `fleet run`.
