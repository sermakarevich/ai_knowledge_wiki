# Task: chapter 10 writeup — agent evals (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/10_findings.md`, `project/runs/results.md`,
`project/src/evals_tutorial/agent.py` (excerpts), `project/data/agent_tasks.jsonl` (3 rows),
`research/SOURCES_practitioner.md` (Anthropic agent-evals section only), `research/SOURCES_papers.md`
(agent evaluation section only), and — for style only — `09_hallucination_detectors.md`. Nothing else
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The agent, tasks and trials exist (previous task); the chapter does not.

## Fix
Create `10_agent_evals.md` (`# 10 — Agent evals: …`, "## What you will learn"): what makes agents
different to grade (state, paths, stochasticity); the mock shop and tools with a code excerpt; a task
row explained field by field; grading the **final state** plus path constraints (Anthropic,
"Demystifying evals for AI agents", 2026) — a real trajectory walked through step by step with the grade;
pass@k vs pass^k in plain words with our numbers and CIs (Yao et al. 2024, τ-bench) and why reliability
is what production needs; trajectory metrics (steps, tool errors, violations); transcript grading vs
state grading — the kappa and what the judge missed; the simulated user for multi-turn tasks and its
limits; a mermaid diagram of the episode loop. "What landed in the results table". Troubleshooting
(model does not emit tool calls → format/temperature; infinite loops → step cap; assertions on state
too strict); Exercises (add a task where the correct answer is to refuse; compute pass^5 with two more
trials); `Next:` → chapter 11.

## Tests
`test -s 10_agent_evals.md && grep -c "What you will learn" 10_agent_evals.md && grep -c "pass^" 10_agent_evals.md && grep -ci troubleshooting 10_agent_evals.md`

## DoD
As in COMMON.md. Commit: `10_agent_evals.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/10_agent_evals.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code or runs; numbers only from committed files. Do not edit `index.md`. Context budget ≈ 40k tokens.
Do not run `fleet serve restart` or `fleet run`.
