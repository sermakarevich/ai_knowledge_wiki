# Task: chapter 13 writeup — production (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/13_findings.md`, `project/runs/13_landscape.md`,
`project/runs/13_monitor/rolling.md`, `project/runs/results.md`, `project/src/evals_tutorial/prod.py` (excerpts),
`project/docker-compose.yml`, `project/.github/workflows/evals-ci.yml`, `research/SOURCES_practitioner.md`
(sections on production monitoring / A-B tests / the three levels only), and — for style only —
`12_inspect_ai.md`. Nothing else (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The Langfuse stack, the CI gate and the monitor exist (previous task); the chapter does not.

## Fix
Create `13_production.md` (`# 13 — Production: from scripts to a running system`, "## What you will
learn"): the loop offline eval → ship → trace → sample → label → eval set grows (mermaid, Hamel Husain's
"data flywheel"); Langfuse self-hosted — the compose excerpt, ports/names, first start; tracing our app
(`@observe` excerpt, what a trace shows); datasets and experiment runs — v1 vs v2 side by side, with the
scores attached (judge, checks, human labels) and the run names from the findings; the **CI gate** — the
rule in words, why it uses the CI upper bound and not the point estimate (chapter 07), the actual
summary output, the GitHub workflow excerpt; online monitoring on a sample with a cheap detector and the
rolling table/plot, one alert rule; A/B tests in production (level 3) in one section — what to randomise,
how long, and the link to chapter 07's power table; the **landscape table** with "Advantages and
disadvantages" for each tool (from the committed table only). Troubleshooting (ClickHouse memory; keys
not initialised; SDK v2 vs v3 API; port 3030 taken); Exercises (add a latency score; make the gate also
check the retrieval recall@2); `Next:` → chapter 14.

## Tests
`test -s 13_production.md && grep -c "What you will learn" 13_production.md && grep -ci "langfuse" 13_production.md && grep -ci "advantages and disadvantages" 13_production.md`

## DoD
As in COMMON.md. Commit: `13_production.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/13_production.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code, no containers, no runs; numbers only from committed files. Do not edit `index.md`. Context
budget ≈ 40k tokens. Do not run `fleet serve restart` or `fleet run`.
