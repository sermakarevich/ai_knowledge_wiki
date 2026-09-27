# COMMON rules for every task of the `rag` tutorial (read fully before starting)

You are writing one chapter of a tutorial in a knowledge base. The cwd is
`/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag` (a folder inside the git repo `~/.ai`).
**Read `index.md` first** — it is the contract (settings, ports, models, corpus, scoreboard columns)
and must not be changed except where a spec explicitly says so. Read the previous chapters
(`0N_*.md`) and the code they added before writing yours: every chapter builds on the previous ones
and every experiment must be comparable with the earlier scoreboard rows.

## Research notes — prefer these over memory
`specs/research/frameworks.md` (LangChain/LangGraph, LlamaIndex, Haystack, DSPy: versions, package
names, current APIs, advanced features), `specs/research/systems_and_infra.md` (RAGFlow, LightRAG,
Open WebUI, …; vector stores; parsers/chunkers), `specs/research/models_eval_papers.md` (Ollama
embedding models, rerankers, RAGAS & metrics, the paper corpus with licences, technique notes).
They were verified on the web on 2026-08-30 with source URLs. Libraries move fast: **always check the
installed version and its actual API** (`uv run python -c "import X; print(X.__version__)"`, `help()`,
`inspect.signature`) before writing code; if a research note disagrees with the installed package,
the package wins — say so in the chapter.

## How the LLM is reached
- Ollama runs on the `rtx` GPU box and is reachable from the Mac at `http://127.0.0.1:11435` through
  an SSH tunnel. If `curl -s http://127.0.0.1:11435/api/tags` fails, run `fleet tunnel` (it starts the
  tunnel if needed) and retry. Never change `OLLAMA_URL` to anything else.
- Chat/judge model: `qwen3.8:27b`. Default embedding model: `nomic-embed-text`. Chapter 06 may
  `ollama pull` additional **embedding** models (≤ 2 GB each) via `ssh -o ClearAllForwardings=yes rtx
  'ollama pull <name>'`. Never pull chat models, never `ollama rm`, never touch the Ollama service
  or `~/.ollama` on `rtx`. Never kill processes on `rtx`.
- **The GPU is shared.** Another tutorial (`llm_training`) runs training jobs on the same 4090 and
  unloads the Ollama model before them; our requests reload it (17 GB). Before starting any batch
  of more than ~100 LLM calls, check `ssh -o ClearAllForwardings=yes rtx nvidia-smi
  --query-compute-apps=pid,used_memory --format=csv`: if a non-Ollama process holds more than 6 GB,
  wait (sleep 10 min, retry, up to 6 h) instead of starting. Single calls and embeddings are fine at
  any time. Chapter 00 implements this as `just gpu-check`.
- **Everything is cached.** `rag_tutorial.llm` (chapter 00) caches every chat response and every
  embedding on disk under `project/data/cache/` keyed by a hash of (model, options, input). The cache
  is committed to git so that re-running a chapter, a test or `just scoreboard` costs zero LLM calls.
  Always call the LLM through this module (also from inside LangChain/LlamaIndex/Haystack — wrap or
  point them at the same cache where feasible, otherwise document the extra calls). Keep temperature
  0 and a fixed seed for everything that is evaluated.
- Budget: one full evaluation of the 40-question test set costs ≈ 40 generations + ≈ 80–120 judge
  calls ≈ 10–15 minutes. Plan each chapter for ≤ ~1,500 LLM calls in total (≈ 2–3 hours of GPU time).
  If a technique needs more (e.g. contextual retrieval over every chunk), say what it costs in the
  chapter and keep the result cached.

## Chapter writing style (match `../neo4j/*.md` and `../graph_rag2/*.md`)
- Simple language a non-expert can follow; explain every abbreviation the first time it is used in
  the chapter (RAG, LLM, BM25, HNSW, MRR, …), even if an earlier chapter explained it.
- Start with `# 0N — Title` then `## What you will learn` (bullets). End with `## Troubleshooting`
  (table: symptom | cause | fix) and `## Exercises` (2–4 short ones). Cross-link previous/next chapters.
- Show the *real* code from `project/src/rag_tutorial/…` (excerpts, not the whole file) and the *real*
  output of the commands you ran (numbers, tables, example answers with citations). Never invent
  numbers — if you could not run something, say so explicitly in the chapter.
- Every experiment chapter ends with a **"What changed on the scoreboard"** section: the new rows
  next to the three anchors (no retrieval / naive RAG / oracle), 3–6 sentences of interpretation,
  and one or two concrete failure or success examples (question, retrieved passages, answer).
- Every library/system chapter ends with an **"Advantages and disadvantages"** table (what it did
  well for us, where it hurt, learning curve, when to choose it) grounded in what you actually ran.
- One mermaid diagram where a picture helps (pipeline / data flow). Length target 300–500 lines.

## Code conventions
- Package `rag_tutorial` under `project/src/`; one module per chapter (names given in each spec); each
  module is a Typer CLI (`uv run python -m rag_tutorial.<module> --help` works) and exposes plain
  functions that tests can import. Settings come from `project/.env` through `rag_tutorial.config`
  (Pydantic model; `.env.template` documents every variable).
- Experiments write `project/runs/<experiment>/metrics.json` (the scoreboard columns from `index.md`
  plus a free `details` dict), `predictions.jsonl` (one line per question: retrieved chunk ids,
  answer, judge output) and `config.json` (everything needed to reproduce). `just scoreboard`
  (chapter 02) rebuilds `project/runs/scoreboard.md` from all `metrics.json` files. Experiment names
  are `<chapter>_<short-name>`, e.g. `04_semantic_512`.
- Chunk objects everywhere carry `id, paper, section, text, start, end, meta`. Chunk ids are
  deterministic (hash of paper + start + end) so retrieval metrics work across strategies.
- Tests (`project/tests/`) run on the Mac on CPU **without network**: they use a fake LLM/embedder
  (`rag_tutorial.testing.FakeLLM`, `FakeEmbedder` — deterministic hashing embeddings) and tiny
  in-memory corpora made in the test, or read committed caches. Anything that needs Ollama, Docker or
  the network is `@pytest.mark.slow` and NOT part of the DoD test command. Total CPU test time must
  stay under 2 minutes. Never call a live LLM inside a test loop.
- Add every new recipe to `project/justfile` with a one-line comment above it (`just` shows them).
  Docker services live in one `project/docker-compose.yml` with **profiles** (`qdrant`, `pgvector`,
  `openwebui`) so `just up qdrant` starts only what a chapter needs. Ports and container names are
  fixed in `index.md`.
- Big binaries never go to git: PDFs (`data/corpus/pdf/`), vector indexes (`data/indexes/`), model
  downloads (`~/.cache`) are gitignored. Parsed Markdown, the golden set, caches, `metrics.json`,
  `predictions.jsonl` and plots are committed.

## Definition of Done (every task)
1. `cd project && uv run pytest tests/ -q -m "not slow"` is green on the Mac.
2. The experiments named in the spec were actually run; their `runs/<experiment>/metrics.json`
   exist, `just scoreboard` was re-run and the chapter quotes the real numbers.
3. Stage ONLY the files you created/edited for this task, by explicit path (`git add <p1> <p2> …`
   — directories such as `project/data/cache` and `project/runs/<experiment>` may be added by path),
   then `git commit -m "rag: <chapter> …"`. NEVER `git add -A`/`git add .`/`commit -a`; NEVER
   `git reset`, `git checkout -- .`, `git stash`, `git restore` — the tree is shared with other
   workers (another tutorial is being written in `../llm_training` at the same time) and an
   auto-sync job also commits here every minute; leave their files alone. If auto-sync already
   committed some of your files, that is fine — commit whatever remains.
4. Verify: `git show HEAD:knowledge/research_topics/rag_and_retrieval/tutorials/rag/<chapter file> | grep -c "What you will learn"` ≥ 1
   (paths in `git show` are relative to the repo root `~/.ai`).
5. `bd close <your-id> --reason "<one-line summary with the key scoreboard numbers>"`. Close only
   your task. Do not run `fleet serve restart` / `fleet run`. Do not create new fleet tasks.
