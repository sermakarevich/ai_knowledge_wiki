# Task: chapter 01 — Concepts: what evals are, the three levels, graders, the lifecycle, the tool landscape (markdown only)

Read: `index.md`, `specs/COMMON.md`, `research/SOURCES_practitioner.md` (all), `research/SOURCES_papers.md`
(section "Key findings a tutorial must teach" and the benchmark table), `research/SOURCES_tools.md`
(section 1 comparison table and section 7). For style only: `../rag/01_concepts.md` first 100 lines.
Nothing else (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The reader needs the vocabulary and the map before any code: what an eval is, what kinds exist, how
they fit together, and which tools exist.

## Fix
Create `01_concepts.md` (`# 01 — Concepts: …`, "## What you will learn"), covering, in simple language
with every abbreviation explained:
1. **What an eval is and is not** — eval vs unit test vs model benchmark vs monitoring vs A/B test; "evals
   measure *your* pipeline on *your* data" (Hamel Husain & Shreya Shankar FAQ); why generic benchmarks do
   not tell you whether your app works.
2. **The three levels** (Hamel, "Your AI Product Needs Evals"): level 1 code checks on every change,
   level 2 human + model grading on logged traces, level 3 A/B tests in production; cadence and cost of
   each.
3. **Graders**: code / human / LLM (Anthropic docs order: fastest reliable first); reference-based vs
   reference-free; pointwise (direct score) vs pairwise; binary pass/fail vs Likert — state the
   disagreement between sources honestly (FAQ says binary; Anthropic examples use Likert) and the
   recommendation used in this tutorial (binary + critique).
4. **The lifecycle** used by this tutorial as a mermaid diagram: look at data → open/axial coding →
   failure taxonomy → code graders → LLM judges aligned to labels (TPR/TNR) → statistics with CIs → CI gate
   → production monitoring → back to data; "criteria drift" (Shankar et al. 2024) as the reason it is a
   loop.
5. **LLM-as-judge in one page**: what it is, the known biases (position, verbosity, self-preference —
   cite Zheng et al. 2023; Wang et al. 2023; Dubois et al. 2024), why a judge is a classifier that must
   itself be measured (JudgeBench), panels of judges (PoLL).
6. **Model benchmarks in one page**: the table from `SOURCES_papers.md` (MMLU, GSM8K, HumanEval, IFEval,
   MT-Bench, Arena, SWE-bench, τ-bench, HLE, …) with what each measures; contamination, saturation and
   why prompt formatting changes scores (Biderman et al. 2024).
7. **The tool landscape** — a table (tool | category | licence | runs against Ollama | used in chapter)
   built from `SOURCES_tools.md` section 1, with a first pros/cons paragraph and which ones this tutorial
   runs (lm-evaluation-harness, DeepEval, RAGAS, Inspect AI, Langfuse, evalica, HHEM, LettuceDetect).
8. **How this tutorial measures things**: the SUT, the ticket set with gold-by-construction labels, the
   two public datasets, the results table and the CI rule — a plain-language walk through the tables in
   `index.md`.
End with Troubleshooting (conceptual pitfalls as a table: "my judge agrees with itself 100 %" → position
bias / temperature; "score went up 3 points" → inside the CI; …), Exercises, `Next:` → chapter 02.
Length 300–450 lines.

## Tests
`test -s 01_concepts.md && grep -c "What you will learn" 01_concepts.md && grep -ci troubleshooting 01_concepts.md && grep -ci exercises 01_concepts.md`

## DoD
As in COMMON.md. Commit: `01_concepts.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/01_concepts.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code. Do not edit `index.md`. Do not open the PDFs. Context budget ≈ 50k tokens. Do not run
`fleet serve restart` or `fleet run`.
