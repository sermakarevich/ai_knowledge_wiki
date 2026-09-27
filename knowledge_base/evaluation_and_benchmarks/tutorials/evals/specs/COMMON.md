# COMMON rules for every task of the `evals` tutorial (read fully before starting)

You are writing one piece of a tutorial in a knowledge base. The cwd is
`/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals` (a folder inside the git repo `~/.ai`).
**Read `index.md` first** — it is the contract (settings, models, data contracts, results-table columns)
and must not be changed except where a spec explicitly says so. Your spec tells you exactly which other
files to read; do not read more than that (the worker context is small).

## Research notes — prefer these over memory
`research/SOURCES_practitioner.md` (Hamel Husain / Shreya Shankar methodology, Eugene Yan, Anthropic and
OpenAI guides — with the key ideas and the disagreements between them), `research/SOURCES_papers.md`
(LLM-as-judge papers, benchmark methodology, RAG evaluation, agent evaluation, standard benchmarks) and
`research/SOURCES_tools.md` (every eval library: version, licence, how to connect it to Ollama, verdict).
The full text of the practitioner articles is next to them (`research/*.md`) and the papers are under
`research/research/*.pdf` — open a specific one only when your spec says so. They were verified on the web
on 2026-09-03. Libraries move fast: **always check the installed version and its actual API**
(`uv run python -c "import X; print(X.__version__)"`, `help()`, `inspect.signature`) before writing
code; if a research note disagrees with the installed package, the package wins — say so in the chapter.

## How the LLM is reached
- Ollama runs on the `rtx` GPU box and is reachable from the Mac at `http://127.0.0.1:11435` through an
  SSH tunnel. If `curl -s http://127.0.0.1:11435/api/tags` fails, run `fleet tunnel` and retry. Never
  change `OLLAMA_URL`. Third-party tools use the OpenAI-compatible endpoint `http://127.0.0.1:11435/v1`
  with any non-empty API key (e.g. `ollama`).
- System-under-test and default judge model: `qwen3.8:27b`. Embeddings: `nomic-embed-text`. Other chat
  models already on the box: `gemma4:latest`, `tiny-qwen35-110m-sft:latest`, `tiny-qwen35-110m-dpo:latest`.
  The ONLY model a task may pull is `atla/selene-mini` (chapter 06, ≈ 5 GB) via
  `ssh -o ClearAllForwardings=yes rtx 'ollama pull atla/selene-mini'`. Never pull anything else, never
  `ollama rm`, never touch the Ollama service or `~/.ollama` on `rtx`, never kill processes on `rtx`.
- **The GPU is shared.** Other tutorials run training jobs and RAG experiments on the same 4090. Before a
  batch of more than ~100 LLM calls run `just gpu-check` (chapter 00): if a non-Ollama process holds more
  than 6 GB, wait (sleep 10 min, retry, up to 6 h) instead of starting. Single calls are fine at any time.
- **Everything is cached.** `evals_tutorial.llm` (chapter 00) caches every chat response and every
  embedding on disk under `project/data/cache/` keyed by a hash of (model, options, input). The cache is
  committed to git so that re-running a chapter, a test or `just results` costs zero LLM calls. Always
  call the LLM through this module; when a third-party library (RAGAS, DeepEval, lm-eval, Inspect,
  Langfuse) must talk to Ollama itself, point it at the OpenAI-compatible endpoint, keep temperature 0,
  and record the number of calls it made in `metrics.json`. Keep temperature 0 and a fixed seed for
  everything that is evaluated, except where a spec asks for repeated sampled trials.
- Budget: `qwen3.8:27b` needs ≈ 20–60 s per call. Plan each task for **≤ ~400 LLM calls** (≈ 3 h of GPU
  time); the specs give per-experiment sample sizes — do not enlarge them. If a technique would need
  more, run it on the sample size given, say what the full run would cost, and keep the result cached.
- Run long batches in the background with a log file and poll it (`nohup uv run … > runs/<x>.log &`, then
  `tail` every few minutes) so a dropped SSH tunnel does not kill your work; if the tunnel drops, run
  `fleet tunnel` and re-run — the cache makes the re-run resume where it stopped.

## Chapter writing style (match `../neo4j/*.md` and `../rag/*.md`)
- Simple language a non-expert can follow; explain every abbreviation the first time it is used in the
  chapter (LLM, RAG, CI, TPR, MRR, …), even if an earlier chapter explained it.
- Start with `# 0N — Title` then `## What you will learn` (bullets). End with `## Troubleshooting`
  (table: symptom | cause | fix) and `## Exercises` (2–4 short ones) and a `Next:` line.
- Show the *real* code from `project/src/evals_tutorial/…` (excerpts, not the whole file) and the *real*
  output of the commands you ran (numbers, tables, example tickets and replies). Never invent numbers —
  if you could not run something, say so explicitly in the chapter.
- Every experiment chapter ends with a **"What landed in the results table"** section: the new rows, 3–6
  sentences of interpretation with the confidence intervals, and one or two concrete examples (ticket,
  output, grade, why).
- Every library chapter ends with an **"Advantages and disadvantages"** table (what it did well for us,
  where it hurt, learning curve, when to choose it) grounded in what you actually ran.
- Cite the source behind each method in one line (`(Hamel Husain, "Your AI Product Needs Evals", 2024)`,
  `(Zheng et al. 2023, arXiv 2306.05685)`) — the research notes give the references.
- One mermaid diagram where a picture helps. Length target 300–500 lines.

## Code conventions
- Package `evals_tutorial` under `project/src/`; one module per chapter (names given in each spec); each
  module is a Typer CLI (`uv run python -m evals_tutorial.<module> --help` works) and exposes plain
  functions that tests can import. Settings come from `project/.env` through `evals_tutorial.config`
  (Pydantic model; `.env.template` documents every variable).
- Experiments write `project/runs/<experiment>/metrics.json` (schema in `index.md`), `predictions.jsonl`
  (one line per item: id, output, grade/score, judge critique where relevant) and `config.json`
  (everything needed to reproduce: model, prompt version, sample size, seed). `just results` (chapter
  04) rebuilds `project/runs/results.md` from all `metrics.json` files. Experiment names are
  `<chapter>_<short-name>`, e.g. `05_judge_faithful_v2`.
- Prompts live in `project/src/evals_tutorial/prompts/<name>_v<N>.txt` (plain text with `{placeholders}`),
  never inline in code, so that versions can be compared. Never edit a committed prompt version — add
  `v<N+1>`.
- Tests (`project/tests/`) run on the Mac on CPU **without network**: they use `evals_tutorial.testing.
  FakeLLM` / `FakeEmbedder` and tiny in-memory data made in the test, or read committed caches and
  committed `runs/` files. Anything that needs Ollama, Docker or the network is `@pytest.mark.slow` and
  NOT part of the DoD test command. Total CPU test time must stay under 2 minutes. Never call a live LLM
  inside a test loop.
- Add every new recipe to `project/justfile` with a one-line comment above it. Docker services live in one
  `project/docker-compose.yml` with **profiles**; ports and container names are fixed in `index.md`.
- Big binaries never go to git: model downloads (`~/.cache`), `.venv`, Langfuse volumes. Handbook, tickets,
  labels, caches, `metrics.json`, `predictions.jsonl`, plots (PNG ≤ 300 KB) and traces are committed.

## Two-part tasks (impl → writeup)
Most chapters are two tasks. The **impl** task writes code, runs experiments and ends with a findings note
`project/runs/<NN>_findings.md` (terse bullets: every number and table produced, what ran vs was skipped
and why, 3–5 observations worth highlighting). The **writeup** task reads only the findings note, the
result files and ONE previous chapter for style, and writes the chapter Markdown. Never do the other
half's work.

## Definition of Done (every task)
1. `cd project && uv run pytest tests/ -q -m "not slow"` is green on the Mac.
2. The experiments named in the spec were actually run; their `runs/<experiment>/metrics.json` exist,
   `just results` was re-run (from chapter 04 on) and the findings note / chapter quotes the real numbers.
3. Stage ONLY the files you created/edited for this task, by explicit path (`git add <p1> <p2> …` —
   directories such as `project/data/cache` and `project/runs/<experiment>` may be added by path), then
   `git commit -m "evals: <chapter> …"`. NEVER `git add -A`/`git add .`/`commit -a`; NEVER `git reset`,
   `git checkout -- .`, `git stash`, `git restore` — the tree is shared with other workers (other
   tutorials are being written in `../rag` and `../llm_training` at the same time) and an auto-sync job
   also commits here every minute; leave their files alone. If auto-sync already committed some of your
   files, that is fine — commit whatever remains.
4. Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/<file> | grep -c "<token>"` ≥ 1 (paths in `git show`
   are relative to the repo root `~/.ai`; the spec names the file and token).
5. `bd close <your-id> --reason "<one-line summary with the key numbers>"`. Close only your task. Do not
   run `fleet serve restart` / `fleet run`. Do not create new fleet tasks. If your prerequisites (files a
   previous task should have produced) do not exist, exit WITHOUT changing files or closing the bead.
