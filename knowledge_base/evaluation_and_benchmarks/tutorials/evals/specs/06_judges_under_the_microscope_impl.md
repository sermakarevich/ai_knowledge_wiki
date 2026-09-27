# Task: chapter 06 impl — judges vs 3.3K human votes on MT-Bench: agreement, biases, a specialised judge, a panel, Bradley–Terry (code + runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md`, `project/data/public/README.md`,
`project/src/evals_tutorial/{results,llm}.py` (signatures only), `research/SOURCES_papers.md` (sections
on LLM-as-judge: Zheng et al. 2023 MT-Bench, position/verbosity/self-preference bias, PoLL panels,
Selene-Mini, Bradley–Terry / Chatbot Arena) and `research/SOURCES_tools.md` (entry for `evalica`).
Do not read chapter markdown (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Chapter 05 aligned judges against *our* labels. Here we test the local model as a judge against **real
human votes**: `project/data/public/mt_bench_human_votes.jsonl` (3355 pairwise votes; fields
`question_id, model_a, model_b, winner ∈ {model_a, model_b, tie, tie (bothbad)}, judge, turn`) and
`mt_bench_answers.jsonl` (480 rows: `question_id, model, questions[2], answers[2]`), plus GPT-4's votes
`mt_bench_gpt4_votes.jsonl` for reference. Questions to answer with numbers: how often does `qwen3.8:27b`
agree with humans; what is the human–human ceiling; does it prefer the first position (position bias),
the longer answer (verbosity bias), or its own family (self-preference — none of the 6 MT-Bench models is
Qwen, so test verbosity and position; note self-preference cannot be tested here and why); does a
purpose-built judge (`atla/selene-mini`, the one model you may pull) do better; does a panel help; and
do Bradley–Terry ratings from judge votes reproduce the human ranking.

## Fix

### `project/src/evals_tutorial/mtbench.py` (Typer: `sample`, `judge`, `agreement`, `bias`, `panel`, `bt`, `all`)
- `sample`: pick **150 turn-1 pairs** (seed 0) from human votes where `winner` is not a tie, at most one
  vote per (question_id, model_a, model_b) — save `runs/06_pairs.jsonl` with the two answers attached.
  Also compute **human–human agreement**: over all (question, pair) with ≥ 2 human votes, the fraction of
  vote pairs that agree (ties excluded and included, both reported). No LLM calls.
- `judge --model qwen3.8:27b|gemma4:latest|atla/selene-mini --order ab|ba`: the MT-Bench pairwise
  prompt (`prompts/pairwise_judge_v1.txt`, verdict `A`/`B`/`tie` after a short explanation; for
  selene-mini use its documented prompt format — check `research/SOURCES_papers.md` / the model card via
  `ollama show`); run both orders → 300 calls per model. Models: qwen (required), selene-mini
  (`ssh -o ClearAllForwardings=yes rtx 'ollama pull atla/selene-mini'` — if the pull fails, skip and
  record), gemma4 (required, cheaper). Total ≤ ~900 calls — run in the background, `just gpu-check` first;
  if time is short cut to 100 pairs for gemma4/selene and say so.
- `agreement --model X`: agreement with the human vote (position-averaged: a pair counts as agreeing if
  the majority of the two orders matches), vs the human–human ceiling and vs GPT-4's agreement on the
  same pairs (from `mt_bench_gpt4_votes.jsonl`, where available). Experiment `06_agreement_<model>`
  (primary `agreement_with_humans`, n = 150).
- `bias --model X`: **position bias** = share of pairs where the verdict flips when the order is swapped,
  and the share of first-position wins; **verbosity bias** = P(judge picks the longer answer) vs P(humans
  pick the longer answer), and agreement conditioned on "longer wins" vs "shorter wins". Experiment
  `06_bias_<model>` (primary `position_flip_rate`).
- `panel`: PoLL-style majority vote of {qwen, gemma4, selene-mini} (or the two available) → agreement with
  humans; experiment `06_panel` (primary `agreement_with_humans`).
- `bt`: Bradley–Terry ratings with `evalica` (add to pyproject; check its actual API at install time,
  fall back to a 40-line own implementation if the API differs and say so) from (a) all 3355 human votes,
  (b) qwen's votes on the 150 pairs; Spearman correlation between the two rankings of the 6 models plus
  the two rating tables; experiment `06_bradley_terry` (primary `spearman_vs_human`). Plot both rating
  bars to `runs/06_bradley_terry/ratings.png`.

### `project/justfile`
`mtbench-sample`, `mtbench-judge model=…`, `mtbench-all`.

### Tests `project/tests/test_06_mtbench.py`
Sampling is deterministic and tie-free on a 30-row synthetic vote file; human–human agreement on a
hand-made case; position-flip and verbosity metrics on canned verdicts; BT ranking on a synthetic
tournament with a known winner (evalica or fallback); panel majority with 2 and 3 judges. No network.

### Findings note `project/runs/06_findings.md` (REQUIRED)
Human–human agreement (with/without ties); agreement per judge and GPT-4's; position-flip rate and
first-position win share per judge; verbosity numbers; panel result; BT rating tables and Spearman;
one concrete pair where qwen flips with order (question, both answers' first line, both verdicts); LLM
calls and seconds per model; what was skipped (selene pull etc.).

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/mtbench.py`, `project/src/evals_tutorial/prompts/pairwise_judge_v1.txt`
(+ selene variant), `project/pyproject.toml`, `project/uv.lock`, `project/runs/06_*/**`, `project/runs/06_pairs.jsonl`,
`project/runs/results.md`, `project/data/cache/**`, `project/justfile`, `project/tests/test_06_mtbench.py`,
`project/runs/06_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "06_agreement_qwen"` ≥ 1.

## Scope & constraints
Only the public MT-Bench files — no helpdesk traces. No CIs (07). Never pull any model other than
`atla/selene-mini`. Context budget ≈ 55k tokens. Do not run `fleet serve restart` or `fleet run`.
