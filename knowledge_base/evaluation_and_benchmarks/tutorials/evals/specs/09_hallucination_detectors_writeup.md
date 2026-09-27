# Task: chapter 09 writeup — hallucination detectors (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/09_findings.md`, `project/runs/09_compare.md`,
`project/runs/results.md`, `project/data/public/README.md` (RAGTruth part), `project/src/evals_tutorial/halluc.py`
(excerpts), `research/SOURCES_papers.md` (hallucination section only), and — for style only —
`08_rag_evals.md`. Nothing else (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The detector benchmark and the helpdesk application ran (previous task); the chapter does not exist.

## Fix
Create `09_hallucination_detectors.md` (`# 09 — Hallucination detectors: …`, "## What you will learn"):
what "hallucination" means in RAG (unsupported by the source) vs factual error; RAGTruth (Niu et al.
2024, arXiv 2401.00396) and its span labels with one real example row (source excerpt, response, the
labelled span); how each detector works in two sentences (HHEM-2.1-Open — Vectara 2024; LettuceDetect —
Kovács & Recski 2025; NLI cross-encoders; SelfCheckGPT — Manakul et al. 2023) and a code excerpt for the
common scorer interface; the comparison table with AUROC/F1 and seconds per item, per task type; the
LLM judge on the same 100 rows — quality vs cost; threshold selection on dev and why; applying the best
detector to our helpdesk replies — AUROC vs the chapter-03 failure mode and the three flagged examples;
when to use a detector (online monitoring, sampling for the judge) vs a judge (offline, explanations).
Mermaid: source + response → detector score → threshold → flag. "What landed in the results table".
"Advantages and disadvantages" table across the four detectors. Troubleshooting (trust_remote_code;
CPU too slow → batch/truncate; long sources → chunking); Exercises (tune the threshold for recall 0.9;
run LettuceDetect span-level on 20 helpdesk replies and read the spans); `Next:` → chapter 10.

## Tests
`test -s 09_hallucination_detectors.md && grep -c "What you will learn" 09_hallucination_detectors.md && grep -ci "HHEM" 09_hallucination_detectors.md && grep -ci "advantages and disadvantages" 09_hallucination_detectors.md`

## DoD
As in COMMON.md. Commit: `09_hallucination_detectors.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/09_hallucination_detectors.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code or runs; numbers only from committed files. Do not edit `index.md`. Context budget ≈ 40k tokens.
Do not run `fleet serve restart` or `fleet run`.
