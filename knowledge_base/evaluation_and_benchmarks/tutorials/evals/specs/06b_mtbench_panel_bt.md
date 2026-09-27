# Task: chapter 06b — MT-Bench: gemma4 and Selene-Mini as judges, panel, Bradley–Terry ratings, findings (runs + BT code, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/06_judges_under_the_microscope_impl.md` (full design — this task is its
SECOND HALF), `project/runs/06a_findings.md`, `project/src/evals_tutorial/mtbench.py` (`--help` and
`grep -n "^def \|^@app"`; open bodies only when needed), and `research/SOURCES_tools.md` (the `evalica`
entry only). (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. Pull the one allowed model: `ssh -o ClearAllForwardings=yes rtx 'ollama pull atla/selene-mini'` (if it
   fails, skip selene and record). Add a selene prompt variant if its card requires a specific format
   (`ollama show atla/selene-mini`).
2. `judge` for `gemma4:latest` and `atla/selene-mini` on the **first 100 pairs** of `runs/06_pairs.jsonl`,
   both orders (≤ 400 calls total; gpu-check first, background + log); `agreement` and `bias` for each →
   experiments `06_agreement_<model>`, `06_bias_<model>` (n = 100; note the different n in `notes`).
3. Implement `panel` (majority vote of the available judges on the shared 100 pairs → `06_panel`) and `bt`
   (Bradley–Terry with `evalica` — add to pyproject, check its API, fallback own implementation — from all
   3355 human votes and from qwen's 150-pair votes; Spearman between the two model rankings →
   `06_bradley_terry`, primary `spearman_vs_human`, plot `runs/06_bradley_terry/ratings.png`). `just results`.
4. Add tests to `project/tests/test_06_mtbench.py`: panel majority with 2 and 3 judges; BT ranking on a
   synthetic tournament with a known winner. No network.
5. `project/runs/06_findings.md` (REQUIRED; merge 06a's note): every table from the original spec's
   findings list, the BT rating tables, calls and seconds per model, what was skipped.

Files to commit: `project/src/evals_tutorial/mtbench.py`, new prompt files, `project/pyproject.toml`, `project/uv.lock`,
`project/runs/06_*/**`, `project/runs/results.md`, `project/data/cache/**`, `project/justfile`,
`project/tests/test_06_mtbench.py`, `project/runs/06_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "06_bradley_terry"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: ≤ 420 calls. Do not run `fleet serve restart` or `fleet run`.
