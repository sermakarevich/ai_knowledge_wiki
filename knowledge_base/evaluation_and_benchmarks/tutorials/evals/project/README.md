# Evals tutorial — runnable project

The code behind the [evals tutorial](../index.md): measure with trustworthy numbers whether an
LLM application works, and whether a change made it better or worse. One small customer-support
assistant (*Northwind Outdoor*) is the system under test; thirteen chapters each add a grader or a
benchmark, and every result lands as one row in a single table — `runs/results.md`. Everything runs
locally: Python 3.12 via `uv`, a `justfile`, open-weight models from **Ollama** on the `rtx` GPU box,
and Docker only for the chapter-13 observability stack. No paid API anywhere.

## Prerequisites
- `uv` (0.11.x) and `just` (1.53.x) on PATH.
- `python` ≥ 3.12 (uv selects it; this install is 3.14.6).
- Ollama reachable at `http://127.0.0.1:11435`. It runs on the `rtx` box (RTX 4090);
  `just tunnel` (or `ssh -N -L 11435:127.0.0.1:11434 rtx`) brings it up.
- Docker — **only for chapter 13** (Langfuse). Chapters 00–12 need nothing but Python + Ollama.

## Quickstart (5 commands)
```
cd project
just sync        # uv sync: create .venv, install the exact locked versions
just check       # one status table: Ollama, chat, chat_json, embed, data rows, cache
just test        # fast offline tests (CPU, no network; skips @pytest.mark.slow)
just results     # rebuild runs/results.md from every runs/*/metrics.json (0 LLM calls)
```
`just --list` shows every recipe; the `default` recipe prints the same list.

## How caching works
`src/evals_tutorial/llm.py` is the only thing that talks to Ollama. Every `chat()`, `chat_json()`
and `embed()` call is keyed on its arguments and the result is written to `data/cache/` (committed).
A second run — this session, the test suite, or a chapter's experiment — reads the byte-identical
response from disk, so it makes **zero GPU calls** and is byte-for-byte reproducible. `just check`
costs 3 live calls only because its three probes are not yet cached; the 36 MB of cache covers every
later recipe. `just cache-stats` reports the current size. Because the cache is keyed content-address,
rebuilding an *existing* result never misses.

## Module ↔ chapter
| module | chapter | what it does |
|---|---|---|
| `check.py`, `gpu.py`, `llm.py`, `config.py` | 00 | setup gate, GPU check, cached Ollama client, settings |
| `handbook.py`, `tickets.py`, `helpdesk.py` | 02 | SUT data (gold labels), `triage` + `answer` tasks, run over 80 tickets |
| `viewer.py`, `labels.py` | 03 | trace viewer, reference-aware grader → the label set |
| `code_evals.py`, `results.py` | 04 | code-graded metrics; shared `results_table` plumbing (`just results`) |
| `judge.py`, `judge_dev_report.py` | 05 | LLM judges, dev alignment, test scorecard |
| `mtbench.py` | 06 | judge vs 3.3K human votes, position/verbosity bias, panel, Bradley–Terry |
| `stats.py` | 07 | bootstrap CIs, paired v1 vs v2, power table |
| `rag_evals.py` | 08 | retrieval IR metrics, RAGAS, DeepEval, evaluator agreement |
| `halluc.py` | 09 | HHEM / Lettuce / NLI / SelfCheck on RAGTruth (+ judge comparison) |
| `agent.py` | 10 | τ-bench-style agent, pass@k/pass^k, trajectory, simulated user |
| `bench.py` | 11 | `lm-evaluation-harness` (GSM8K, IFEval), prompt sensitivity |
| `inspect_run.py`, `inspect_tasks.py` | 12 | the same evals as Inspect AI `Task`s, reconcile vs ch-11 |
| `prod.py`, `tracing.py` | 13 | Langfuse tracing/datasets/scores, `just eval-ci` gate, monitoring |
| `testing.py` | — | shared CPU-only test fixtures |

## Run one chapter's experiment
Each recipe's doc line (see `just --list` / this file) states the LLM cost. E.g. chapter 09:
```
just gpu-check           # politely verify the 4090 is free before a batch
just halluc-selfcheck    # 180 cached calls
just halluc-judge        # 100 cached calls
just halluc-compare      # 0 calls — reads the two above
just results             # add the chapter's rows to runs/results.md
```

## Run the Docker profile (chapter 13 only)
```
just langfuse-up        # docker compose --profile langfuse up -d, wait for health
just prod-trace answer_v1   # replay committed traces (0 calls)
just langfuse-down      # stop; volumes kept (never committed)
```
UI at http://localhost:3030. Set `LANGFUSE_*` keys in `.env` (from `.env.template`).

## Add a new experiment
1. Write your runner to call `evals_tutorial.results.write_metrics(...)` — it writes
   `runs/<experiment>/{metrics.json, predictions.jsonl, config.json}` exactly to the data contract.
2. Add a `just` recipe (with a doc line) that calls it.
3. Run `just results` — `runs/results.md` picks up the new row. Done. (No LLM calls, no new deps.)
