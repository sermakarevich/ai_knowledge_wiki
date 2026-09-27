# Task: chapter 06 writeup — judges under the microscope (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/06_findings.md`, `project/runs/results.md`,
`project/data/public/README.md`, `project/src/evals_tutorial/mtbench.py` (excerpts),
`research/SOURCES_papers.md` (LLM-as-judge and Chatbot Arena sections only), and — for style only —
`05_llm_as_judge.md`. Nothing else (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The MT-Bench experiments ran (previous task); the chapter does not exist.

## Fix
Create `06_judges_under_the_microscope.md` (`# 06 — Judges under the microscope: …`, "## What you will
learn"): what MT-Bench is and what the human votes are (Zheng et al. 2023, arXiv 2306.05685); the
human–human ceiling and why no judge should be expected to beat it; the agreement table (qwen, gemma4,
selene-mini, panel, GPT-4 as reported/available); **position bias** with the concrete flipped pair and the
swap-test recipe; **verbosity bias** with the numbers; **self-preference** explained and why it could not
be measured here (Panickssery et al. 2024); a purpose-built judge vs a general model (Atla Selene-Mini,
2025) — what happened; panels of small judges (Verga et al. 2024, PoLL); Bradley–Terry in plain words,
how Chatbot Arena builds its leaderboard from pairwise votes (Chiang et al. 2024) and our Spearman
between human and judge rankings, with the two rating tables and the plot; what this means for chapter
05's judges (calibrate, swap, sample). Mermaid: pairs → two orders → verdicts → agreement/bias/BT.
"What landed in the results table". "Advantages and disadvantages" of evalica. Troubleshooting (judge
output not parseable → verdict letter extraction; selene prompt format; all-ties); Exercises (run 50
pairs at turn 2; add a length-normalised prompt and re-measure verbosity); `Next:` → chapter 07.

## Tests
`test -s 06_judges_under_the_microscope.md && grep -c "What you will learn" 06_judges_under_the_microscope.md && grep -ci "position bias" 06_judges_under_the_microscope.md && grep -ci troubleshooting 06_judges_under_the_microscope.md`

## DoD
As in COMMON.md. Commit: `06_judges_under_the_microscope.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/06_judges_under_the_microscope.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code or runs; numbers only from committed files. Do not edit `index.md`. Context budget ≈ 40k tokens.
Do not run `fleet serve restart` or `fleet run`.
