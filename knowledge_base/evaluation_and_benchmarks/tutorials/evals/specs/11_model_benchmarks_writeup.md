# Task: chapter 11 writeup — model benchmarks (markdown only, NO new code)

Read: `index.md`, `specs/COMMON.md`, `project/runs/11_findings.md`, `project/runs/11_notes.md`,
`project/runs/results.md`, `project/src/evals_tutorial/bench.py` (excerpts), `research/SOURCES_papers.md`
(benchmark methodology section only), `research/SOURCES_tools.md` (lm-eval entry only), and — for style
only — `10_agent_evals.md`. Nothing else (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
The harness runs and the sensitivity study exist (previous task); the chapter does not.

## Fix
Create `11_model_benchmarks.md` (`# 11 — Model benchmarks: …`, "## What you will learn"): what GSM8K
(Cobbe et al. 2021) and IFEval (Zhou et al. 2023) measure, one example item each; lm-evaluation-harness
(Gao et al.) and the exact command against Ollama; the score table with CIs for the three models and why
a 110M model scores near zero; **error bars** — 50 items give ±0.13, so what can and cannot be concluded
(Miller 2024); **prompt sensitivity** — the four variants, the flipping items, the example question,
and the lesson that a leaderboard number is a (model, template, extractor, n) tuple; the harness stderr
vs our bootstrap; contamination (Zhang et al. 2024, GSM1k) and saturation with the reported numbers
table; what the 2026 leaderboards are and how to read them (from the research notes, cite); how this
relates to the tutorial's own evals (benchmarks pick a model; your evals pick a prompt/system). Mermaid:
task yaml → prompt → model → extraction → metric. "What landed in the results table". "Advantages and
disadvantages" of lm-evaluation-harness. Troubleshooting (thinking tokens break extraction; base_url
path must include /chat/completions; rate/timeouts → num_concurrent=1); Exercises (run gsm8k with
--limit 200 overnight and compare CI widths; add a fourth template); `Next:` → chapter 12.

## Tests
`test -s 11_model_benchmarks.md && grep -c "What you will learn" 11_model_benchmarks.md && grep -ci "gsm8k" 11_model_benchmarks.md && grep -ci "advantages and disadvantages" 11_model_benchmarks.md`

## DoD
As in COMMON.md. Commit: `11_model_benchmarks.md`. Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/11_model_benchmarks.md | grep -c "What you will learn"` ≥ 1.

## Scope & constraints
No code or runs; numbers only from committed files. Do not edit `index.md`. Context budget ≈ 40k tokens.
Do not run `fleet serve restart` or `fleet run`.
