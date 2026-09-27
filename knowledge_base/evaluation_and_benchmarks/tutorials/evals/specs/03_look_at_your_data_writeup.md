# Task: chapter 03 writeup — look at your data (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/03_findings.md`, `project/data/labels/taxonomy.yaml`,
`project/data/labels/review_answer_v1.md`, `research/SOURCES_practitioner.md` (section "Key ideas a
tutorial must teach" only), `project/src/evals_tutorial/labels.py` (excerpts), and — for style only —
`02_system_under_test.md`. Nothing else (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The traces were read, coded and labelled (previous task); the chapter teaching the method does not exist.

## Fix
Create `03_look_at_your_data.md` (`# 03 — Look at your data: …`, "## What you will learn"): why the
first step is reading traces, not picking a metric (Hamel Husain, "Field Guide", 2025; the FAQ); the
custom viewer and why generic dashboards stall teams; **open coding** with 5 real notes quoted; **axial
coding** — the taxonomy table with definitions, counts and one real example each; the difference
between a *failure mode* and a *metric*; the honest section "Who labelled this?" — reference-aware
grader as a stand-in for a domain expert, the manual review numbers, what you would do differently with
a real team (label 100 traces yourself, two annotators, measure agreement — forward-reference chapter
06); "criteria drift" (Shankar et al. 2024) with an example where reading traces changed a definition;
the triage code-graded labels; per-scenario/per-topic tables read as a story ("retrieval or generation?").
Mermaid: traces → notes → taxonomy → graders. Troubleshooting (grader returns pass for empty reply →
rubric wording; notes too vague to cluster → ask for the offending sentence; too many modes → merge
under 5 % frequency); Exercises (relabel 10 traces yourself and compute agreement); `Next:` → chapter 04.

## Tests
`test -s 03_look_at_your_data.md && grep -c "What you will learn" 03_look_at_your_data.md && grep -ci troubleshooting 03_look_at_your_data.md && grep -ci exercises 03_look_at_your_data.md`

## DoD
As in COMMON.md. Commit: `03_look_at_your_data.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/03_look_at_your_data.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code or runs; numbers only from the findings note and committed files. Do not edit `index.md`.
Context budget ≈ 40k tokens. Do not run `fleet serve restart` or `fleet run`.
