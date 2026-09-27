# Evals tutorial — how to measure whether an LLM application actually works

A from-zero, hands-on tutorial on **evals** (evaluations): the practice of measuring, with numbers you can trust, whether a system built on an LLM (Large Language Model) does what you want — and whether a change made it better or worse. It covers both worlds:

1. **Product evals** — evaluating *your own* application on *your own* data: looking at traces, error analysis, code-graded checks, LLM-as-judge (using a model to grade another model's output), judge alignment with human labels, statistics with error bars, RAG (Retrieval-Augmented Generation) metrics, hallucination detectors, agent evals, CI regression gates and production monitoring.
2. **Model benchmarks** — how public leaderboards (MMLU, GSM8K, MT-Bench, Chatbot Arena, SWE-bench, τ-bench, …) are built and run, why their numbers move when the prompt format changes, contamination and saturation, and how to run a benchmark yourself with `lm-evaluation-harness` and Inspect AI.

Every method is *run*, not just described: on one small application, one fixed ticket set and two public datasets with real human labels, and every result lands as a row in one **results table** (`project/runs/results.md`). Everything runs locally: Python 3.12 with `uv`, a `justfile`, Docker for the observability stack, and open-weight models served by **Ollama** on the `rtx` GPU box. No paid API is used anywhere.

Retrieve chapters with `ai show research_topics/evaluation_and_benchmarks/tutorials/evals/<chapter>`.

## The idea that holds the tutorial together
- **One system under test (SUT)**: a small customer-support assistant for a fictional online shop, *Northwind Outdoor* (bikes and camping gear). It has three parts, each built to exercise a different kind of eval: `triage` (classify a ticket → category, priority, escalation flag — a **classification** task, graded by code), `answer` (retrieve the relevant handbook sections and write a reply with citations — a **RAG** task, graded by judges and detectors) and `agent` (a tool-calling agent that looks up orders, refunds, cancels and escalates against a mock database under policy rules — an **agent** task, graded on final state and trajectory). Built in chapter 02 and 10; then never changed except through *versioned prompts* (`v1`, `v2`, …) so that every later chapter can compare versions.
- **One ticket set**: 80 synthetic customer tickets (`project/data/tickets/tickets.jsonl`) generated from a persona × topic × scenario grid so that the *labels are gold by construction* (category, priority, escalation, the handbook sections and the answer points a good reply must contain). Split `dev` (20, for tuning prompts and judges) / `test` (60, everything reported in `results.md`).
- **Two public datasets with human labels** (`project/data/public/`, see the README there): **MT-Bench human judgments** (3.3K pairwise human votes over 6 models on 80 questions, CC-BY-4.0) to study LLM judges against humans, and a 480-example test subset of **RAGTruth** (span-level hallucination labels for RAG answers, MIT) to measure hallucination detectors.
- **One results table**: every experiment writes `project/runs/<experiment>/metrics.json`; `just results` rebuilds `project/runs/results.md`. Every number quoted in a chapter comes from there.
- **One statistics module** (chapter 07): every rate reported after chapter 07 carries a 95 % bootstrap confidence interval, and every "A is better than B" claim is a paired comparison.

## Chapters (read in order)
- [00_setup.md](00_setup.md) — tools (`uv`, `just`, Docker, Ollama over an SSH tunnel), project layout, `.env`, the cached Ollama client (chat + embeddings + JSON-schema output, on-disk cache so re-runs are free), the GPU-politeness check, `just check`.
- [01_concepts.md](01_concepts.md) — what an eval is and is not (evals vs benchmarks vs tests vs monitoring); the three levels (code checks / human & model grading / A-B tests); graders (code, human, LLM), reference-based vs reference-free, pointwise vs pairwise; the eval lifecycle (look at data → error analysis → graders → align → measure → gate); the tool landscape map with a first pros/cons table; how this tutorial measures things.
- [02_system_under_test.md](02_system_under_test.md) — the Northwind Outdoor handbook and the ticket generator (persona × topic × scenario → gold labels by construction), `triage` and `answer` with versioned prompts, the trace format, running v1 on all 80 tickets.
- [03_look_at_your_data.md](03_look_at_your_data.md) — reading traces one by one with a custom viewer, open coding (free-text notes per failure) → axial coding (a failure taxonomy with counts), the reference-aware grader that produces our label set, and why "look at your data" beats any metric at the start.
- [04_code_graded_evals.md](04_code_graded_evals.md) — level-1 evals as `pytest`: JSON-schema validity, classification metrics (precision/recall/F1, confusion matrix) for `triage`, verifiable-instruction checks (IFEval style), exact match, keyword/regex assertions, ROUGE and embedding similarity and why they fail for free text; the first `results.md` rows.
- [05_llm_as_judge.md](05_llm_as_judge.md) — binary judges with critiques for the failure modes of chapter 03, aligned against the labels (TPR/TNR, Cohen's kappa) on `dev`, measured on `test`; prompt iteration with few-shot examples; direct scoring vs pairwise; Likert vs binary; a judge scorecard.
- [06_judges_under_the_microscope.md](06_judges_under_the_microscope.md) — the local model as a judge on MT-Bench pairs versus 3.3K human votes: agreement with humans, human–human agreement as the ceiling, position bias (swap test), verbosity bias, self-preference; a purpose-built judge (Atla Selene-Mini) vs the general model; a panel of judges; Bradley–Terry ratings with `evalica` and how Chatbot Arena's leaderboard works.
- [07_statistics.md](07_statistics.md) — error bars for every number: bootstrap confidence intervals, paired comparison of prompt `v1` vs `v2`, clustered standard errors when tickets share a topic, how many test cases you need (power), multiple comparisons; the `evals_tutorial.stats` module used by every later chapter.
- [08_rag_evals.md](08_rag_evals.md) — retrieval metrics (hit@k, recall@k, MRR, nDCG) against gold handbook sections; the RAGAS triad (faithfulness, answer relevancy, context precision) with a local judge and its rough edges; the same metrics in DeepEval; agreement between RAGAS, DeepEval and our own judge.
- [09_hallucination_detectors.md](09_hallucination_detectors.md) — small local models that flag unsupported claims: Vectara HHEM-2.1-Open, LettuceDetect, NLI cross-encoders, SelfCheckGPT, measured on RAGTruth (precision/recall/F1/AUROC, speed on CPU) and compared with the LLM judge; then applied to our own replies.
- [10_agent_evals.md](10_agent_evals.md) — the order-management agent and its mock database; tasks with expected final state and allowed/forbidden actions; pass@k vs pass^k over repeated trials; trajectory metrics (tool-call correctness, steps, policy violations); transcript grading; a simulated user for multi-turn tasks.
- [11_model_benchmarks.md](11_model_benchmarks.md) — running GSM8K and IFEval with `lm-evaluation-harness` against Ollama (`local-chat-completions`, `--limit`); how the prompt template and answer extraction swing scores; comparing `qwen3.8:27b`, `gemma4` and a 110M-parameter model with error bars; contamination (GSM1k), saturation, what the 2026 leaderboards are.
- [12_inspect_ai.md](12_inspect_ai.md) — the same helpdesk eval as an Inspect AI `Task` (dataset → solver → scorer), built-in and model-graded scorers, the log viewer, running GSM8K in Inspect and reconciling with chapter 11; when a framework beats a hand-rolled harness.
- [13_production.md](13_production.md) — from scripts to a running system: Langfuse self-hosted (tracing our app, datasets, experiment runs, scores), a CI regression gate (`just eval-ci` with thresholds and confidence intervals), online sampling and monitoring, A/B tests; the tool landscape (promptfoo, Opik, Phoenix, LangSmith, Braintrust, MLflow, Weave) with advantages and disadvantages.
- [14_wrapup.md](14_wrapup.md) — the whole results table read as one story, a decision guide (which eval for which situation), an evals checklist for a new project, further reading.
- [Q&A.md](Q&A.md) — questions asked while reading, with answers (appended over time).

## Runnable project
`project/` — `pyproject.toml` (uv, Python 3.12, package `evals_tutorial` under `src/`), `justfile`, `docker-compose.yml` (Langfuse stack behind a profile, chapter 13 only), `.env.template`, `data/handbook/` (the shop's policy documents, generated in chapter 02, committed), `data/tickets/tickets.jsonl`, `data/labels/`, `data/public/` (MT-Bench and RAGTruth subsets, committed), `data/cache/` (Ollama response and embedding cache, committed so re-runs and tests are free), `src/evals_tutorial/` (one module per chapter), `tests/` (CPU-only, no network), `runs/<experiment>/metrics.json` + `runs/results.md`. Start with `cd project && just sync && just check`.

## Local settings (shared by all chapters — never change these)
| setting | value |
|---|---|
| Ollama | `http://127.0.0.1:11435` — an SSH tunnel to the `rtx` GPU box (RTX 4090 24 GB); `fleet tunnel` (or `ssh -N -L 11435:127.0.0.1:11434 rtx`) brings it up. OpenAI-compatible endpoint for third-party tools: `http://127.0.0.1:11435/v1`, any string as API key |
| system-under-test model and default judge | `qwen3.8:27b` (17 GB in VRAM while loaded; shared with other work — see 00) |
| other chat models already on the box (chapter 06, 11) | `gemma4:latest`, `tiny-qwen35-110m-sft:latest`, `tiny-qwen35-110m-dpo:latest`; `atla/selene-mini` may be pulled in chapter 06 |
| embedding model | `nomic-embed-text` (768 dimensions) — used for handbook retrieval and embedding-similarity metrics |
| Langfuse (chapter 13) | Docker compose profile `langfuse`, UI http://localhost:3030 (→ 3000), containers prefixed `evals-` |
| Python | 3.12 via `uv`; exact library versions are recorded in `00_setup.md` once installed |

Ports are shifted from the defaults because other tutorials on this machine use them (Grafana 3000/3001, Neo4j 7474/7687, Qdrant 6343, …). Container names are prefixed `evals-`.

## Data contracts (fixed in chapter 02 / 03, then never changed)
| item | value |
|---|---|
| handbook | `project/data/handbook/<section_id>.md`, 12 sections (`returns`, `shipping`, `warranty`, `payments`, `accounts`, `discounts`, `gift_cards`, `order_changes`, `damaged_items`, `international`, `loyalty`, `privacy`), 200–400 words each |
| tickets | `project/data/tickets/tickets.jsonl` — 80 rows: `id, split, persona, topic, scenario, text, gold: {category, priority, needs_escalation, sections[], answer_points[]}`; `category` ∈ the 12 section ids; `priority` ∈ `low, normal, high, urgent`; split `dev` 20 / `test` 60 |
| traces | `project/runs/traces/<run>/<ticket_id>.json` — `run, version, ticket_id, input, retrieved[{section, score}], prompt, output, latency_s, model, usage` (one file per ticket; `<run>` = `<task>_<version>`, e.g. `answer_v1`) |
| labels | `project/data/labels/answer_v1.jsonl` — one row per ticket: `ticket_id, pass (bool), failure_modes[], note` (chapter 03) |
| metrics | `project/runs/<experiment>/metrics.json` — `experiment, chapter, n, metrics{name: value}, ci{name: [lo, hi]}, llm_calls, seconds, details{}` (+ `predictions.jsonl`, `config.json` next to it) |

## Results table columns (shared by all chapters)
`experiment | chapter | n | primary metric | 95 % CI | LLM calls | s/item | notes` — the primary metric is named per experiment (e.g. `pass_rate`, `f1_macro`, `kappa`, `recall@3`, `pass^3`). Numbers on the table are always on the `test` split (or the public dataset named in the experiment).

Verified on: 2026-09-05 — see the "Verified on" table in `00_setup.md` for exact versions (Ollama 0.32.12, `qwen3.8:27b`, `nomic-embed-text`, `uv` 0.11.22, `just` 1.53.0). Every recipe re-ran from the local cache with zero LLM calls (see `14_wrapup.md`).
