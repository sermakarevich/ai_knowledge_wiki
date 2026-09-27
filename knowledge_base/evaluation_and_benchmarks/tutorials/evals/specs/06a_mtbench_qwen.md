# Task: chapter 06a — MT-Bench: sampling, human–human agreement, qwen as pairwise judge in both orders, agreement and bias metrics (code + first judge, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/06_judges_under_the_microscope_impl.md` (the full design — this task is
its FIRST HALF), `project/data/public/README.md`, and the signatures of `results.write_metrics` and `llm.chat`.
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. `project/src/evals_tutorial/mtbench.py` with ALL commands from the original spec stubbed, and these
   fully implemented: `sample` (150 turn-1 non-tie pairs, seed 0 → `runs/06_pairs.jsonl`; human–human
   agreement with and without ties), `judge --model qwen3.8:27b --order ab|ba` with
   `prompts/pairwise_judge_v1.txt` (verdict A/B/tie after a short explanation), `agreement`, `bias`.
2. Run `judge` for **qwen only**, both orders (300 calls; `just gpu-check` first, background + log), then
   `agreement --model qwen3.8:27b` → experiment `06_agreement_qwen3.8_27b` (primary
   `agreement_with_humans`, n = 150; GPT-4's agreement on the same pairs in `details`) and `bias` →
   `06_bias_qwen3.8_27b` (primary `position_flip_rate`; verbosity numbers in metrics). `just results`.
3. `project/tests/test_06_mtbench.py`: deterministic tie-free sampling on a 30-row synthetic vote file;
   human–human agreement on a hand-made case; position-flip and verbosity metrics on canned verdicts. No network.
4. `project/runs/06a_findings.md`: human–human agreement, qwen agreement, GPT-4 agreement, flip rate,
   first-position share, verbosity numbers, one concrete flipped pair, calls and seconds.

## Not your part (06b)
gemma4 and selene-mini judging, the panel, Bradley–Terry/evalica, the final `06_findings.md`.

Files to commit: `project/src/evals_tutorial/mtbench.py`, `project/src/evals_tutorial/prompts/pairwise_judge_v1.txt`,
`project/runs/06_pairs.jsonl`, `project/runs/06_agreement_qwen3.8_27b/**`, `project/runs/06_bias_qwen3.8_27b/**`,
`project/runs/results.md`, `project/data/cache/**`, `project/justfile`, `project/tests/test_06_mtbench.py`, `project/runs/06a_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "06_agreement_qwen"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: ≤ 320 calls. Do not run `fleet serve restart` or `fleet run`.
