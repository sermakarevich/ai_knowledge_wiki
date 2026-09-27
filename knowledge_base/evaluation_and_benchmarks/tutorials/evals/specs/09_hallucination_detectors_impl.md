# Task: chapter 09 impl — hallucination detectors on RAGTruth: HHEM, LettuceDetect, NLI, SelfCheckGPT vs an LLM judge; applied to our replies (code + runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md`, `project/data/public/README.md` (RAGTruth part),
`project/src/evals_tutorial/{results,stats,llm}.py` (signatures), `research/SOURCES_tools.md` (entries for
HHEM-2.1-Open, LettuceDetect, SelfCheckGPT, NLI cross-encoders) and `research/SOURCES_papers.md`
(hallucination detection / RAGTruth section). Do not read chapter markdown
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
An LLM judge costs 20–60 s per call. Small purpose-built detectors run on CPU in milliseconds and claim
to flag unsupported claims in RAG answers. `project/data/public/ragtruth_test_subset.jsonl` (480 rows:
`id, source_id, task_type, source, prompt, source_info, model, response, labels (spans), quality,
hallucinated (bool)`) has human span labels. Measure the detectors at the response level (does the
response contain any hallucination?) with precision/recall/F1/AUROC and CPU speed, compare with the
`qwen3.8:27b` judge on a 100-row subset, then run the best detector over our own helpdesk replies.

## Fix

### `project/src/evals_tutorial/halluc.py` (Typer: `hhem`, `lettuce`, `nli`, `selfcheck`, `judge`, `compare`, `apply`, `all`)
Common: every detector returns a score in [0,1] where higher = more likely hallucinated; threshold
chosen on the first 80 rows (seeded, "dev") to maximise F1, reported on the remaining 400 ("test").
Record seconds per item on the Mac CPU (no GPU). Models download to `~/.cache` (not git). Add
dependencies to pyproject (`transformers`, `torch` CPU, `sentence-transformers`, `lettucedetect` if it
installs cleanly — check the installed version/API; if a package fails to install, skip it, record why).
- `hhem`: `vectara/hallucination_evaluation_model` (HHEM-2.1-Open) via transformers
  (`trust_remote_code`), premise = `source`, hypothesis = `response`; score = 1 − consistency.
  Experiment `09_hhem_ragtruth` (primary `auroc`, n = 400, also f1/precision/recall at the dev threshold,
  `seconds` per item in details).
- `lettuce`: `KRLabsOrg/lettucedect-base-modernbert-en-v1` (or whatever the installed `lettucedetect`
  ships by default) — span-level; response-level score = max span confidence; additionally span-level
  token precision/recall vs the gold `labels` spans on the test rows → `details`. Experiment
  `09_lettuce_ragtruth`.
- `nli`: `cross-encoder/nli-deberta-v3-base` sentence-level: split response into sentences, score each
  against the source (max entailment over source chunks of ~300 words), response score = 1 − min
  entailment. Experiment `09_nli_ragtruth`.
- `selfcheck`: SelfCheckGPT-style consistency **only on 60 rows** (it needs samples): 3 extra sampled
  responses per prompt from `qwen3.8:27b` at temperature 0.7 (180 calls) and the NLI model as the
  consistency scorer between the original response and the samples (no source used — that is the
  point). Experiment `09_selfcheck_ragtruth` (n = 60).
- `judge`: `prompts/halluc_judge_v1.txt` — the LLM judge given source + response, output
  `{unsupported_claims: list[str], hallucinated: bool}`; run on the first 100 test rows (100 calls).
  Experiment `09_llm_judge_ragtruth` (n = 100, primary `f1`).
- `compare`: one table on the 100 rows all methods share: AUROC/F1/precision/recall, s/item, and
  pairwise agreement; plus per `task_type` (QA / Summary / Data2txt) breakdown → `runs/09_compare.md`.
- `apply --run answer_v1|answer_v2`: run HHEM and the best detector over our 60 test replies with the
  retrieved sections as source; compare with the chapter-03 `unsupported_claim` (or equivalent) failure
  mode: AUROC and the 3 most-flagged replies with the flagged sentence. Experiment
  `09_detector_helpdesk_v1` (primary `auroc_vs_label`).

### `project/justfile`
`halluc-all`, `halluc-apply`.

### Tests `project/tests/test_09_halluc.py`
Threshold selection and metrics on canned scores; sentence splitting + chunking; span-level precision/
recall on a hand example; the RAGTruth file loads with the contract fields and 480 rows; model-loading
paths are `@pytest.mark.slow`. No downloads, no network.

### Findings note `project/runs/09_findings.md` (REQUIRED)
The comparison table (all methods, AUROC/F1/P/R, s/item, n), per-task-type breakdown, the SelfCheck
result and cost, the LLM judge vs detectors on the shared 100, helpdesk application results with the 3
examples, model sizes and load times, what failed to install/ran out of time; LLM calls and seconds.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/halluc.py`, `project/src/evals_tutorial/prompts/halluc_judge_v1.txt`,
`project/pyproject.toml`, `project/uv.lock`, `project/runs/09_*/**`, `project/runs/09_compare.md`, `project/runs/results.md`,
`project/data/cache/**`, `project/justfile`, `project/tests/test_09_halluc.py`, `project/runs/09_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "09_hhem_ragtruth"` ≥ 1.

## Scope & constraints
Detectors run on the Mac CPU; only SelfCheck sampling and the judge use Ollama (≤ ~300 calls; gpu-check
first). No model weights in git. Context budget ≈ 55k tokens. Do not run `fleet serve restart` or
`fleet run`.
