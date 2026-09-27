# COMMON rules for every task of the `llm_training` tutorial (read fully before starting)

You are writing one chapter of a tutorial in a knowledge base. The cwd is
`/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training` (a folder inside the git repo `~/.ai`).
**Read `index.md` first** — it is the contract (machines, models, datasets, conventions) and must
not be changed except where a spec explicitly says so. Read the previous chapters (`0N_*.md`) and
the code they added before writing yours: every chapter builds on the previous ones.

## Two machines
- **Mac (here)**: edit code, run unit tests, commit. No GPU. `torch` here is the CPU build.
- **`rtx`** (ssh alias; use `ssh -o ClearAllForwardings=yes rtx '<cmd>'` — the alias has port
  forwards that fail noisily when already bound): Ubuntu, RTX 4090 24 GB = GPU 0, `uv` at
  `~/.local/bin/uv` (NOT on PATH for non-interactive ssh — always use the full path or the
  justfile recipes), project mirror at `~/projects/llm_training`, venv at
  `~/projects/llm_training/.venv` (created by `just remote-sync`).
- Code is copied Mac → rtx with `just push` (rsync). Results (`runs/**/*.json|*.png|*.md|*.log`)
  come back with `just pull`. Checkpoints and datasets never leave `rtx`.
- Long GPU jobs run detached in tmux: `just remote-bg <name> "<cmd>"`, follow with
  `just remote-log <name>`, block with `just remote-wait <name>`. Never run a multi-hour job in a
  foreground ssh.

## The GPU is shared with Ollama and with other people’s jobs
`qwen3.8:27b` (17 GB) is often loaded in Ollama on the 4090 and *other sessions may be using it*.
Rules:
1. Before any GPU job run `just gpu-free` (chapter 00 implements it): it waits until Ollama has
   been idle (GPU utilisation < 10 % for 60 s), unloads the model with `ollama stop qwen3.8:27b`,
   and verifies ≥ 20 GB free. It refuses (exit 1) while someone is actively generating — then
   wait and retry (sleep 10 minutes between tries, up to 6 hours). Never kill processes on `rtx`.
2. Never edit the Ollama systemd unit, never `ollama rm`, never touch `~/.ollama`.
3. When your job is done, nothing to do — Ollama reloads its model on the next request.
4. Only ONE training job at a time on the 4090. Check `nvidia-smi` before starting.

## Chapter writing style (match `../neo4j/*.md` and `../graph_rag2/*.md`)
- Simple language a non-expert can follow; explain every abbreviation the first time it is used
  in the chapter (LLM, SFT, LoRA, …), even if an earlier chapter explained it.
- Start with `# 0N — Title` then `## What you will learn` (bullets). End with `## Troubleshooting`
  (table: symptom | cause | fix) and `## Exercises` (2–4 short ones). Cross-link previous/next chapters.
- Show the *real* code from `project/src/llm_tutorial/…` (excerpts, not the whole file) and the
  *real* output of the commands you ran (numbers, tables, sample generations). Never invent
  numbers — if you could not run something, say so explicitly in the chapter.
- One mermaid diagram where a picture helps (pipeline / data flow / memory layout).
- Length target 250–450 lines. Put every number you quote in `runs/<run>/metrics.json` too.

## Code conventions
- Package `llm_tutorial` under `project/src/`; one module per stage; each module is a Typer CLI
  (`uv run python -m llm_tutorial.<module> --help` works) and exposes plain functions that tests
  can import. Configs are YAML in `project/configs/`, loaded into Pydantic models
  (`llm_tutorial.config`). Runs write to `project/runs/<run_name>/` (gitignored except
  `*.json`, `*.png`, `*.md`, `*.log`).
- Timing/logging: use `rich` console, print one line per training log step with tokens/s and
  memory; keep stdout readable when tailed from a log file.
- Tests (`project/tests/`) run on the Mac on CPU **without GPU, network or Hugging Face
  downloads**: use tiny configs (2 layers, hidden 64, vocab 512) and synthetic data made in the
  test. Anything that needs the GPU or the network is `@pytest.mark.slow` and NOT part of the DoD
  test command. Total CPU test time must stay under 2 minutes.
- Add every new recipe to `project/justfile` with a one-line comment above it (`just` shows them).

## Definition of Done (every task)
1. `cd project && uv run pytest tests/ -q -m "not slow"` is green on the Mac.
2. `just pull` was run so the real metrics/plots are in `project/runs/` and quoted in the chapter.
3. Stage ONLY the files you created/edited for this task, by explicit path (`git add <p1> <p2> …`),
   then `git commit -m "llm_training: <chapter> …"`. NEVER `git add -A`/`git add .`/`commit -a`;
   NEVER `git reset`, `git checkout -- .`, `git stash`, `git restore` — the tree is shared with
   other workers and an auto-sync job also commits here every minute; leave their files alone.
   If auto-sync already committed some of your files, that is fine — commit whatever remains.
4. Verify: `git show HEAD:knowledge/research_topics/training_and_self_evolution/tutorials/llm_training/<chapter file> | grep -c "What you will learn"` ≥ 1
   (paths in `git show` are relative to the repo root `~/.ai`).
5. `bd close <your-id> --reason "<one-line summary with the key numbers>"`. Close only your task.
Do not run `fleet serve restart` / `fleet run`. Do not create new fleet tasks.

## Research notes (verified 2026-08-30 with sources — prefer these over memory)
`specs/research/qwen38_family.md` (Qwen3.8/3.5 models, architecture, tooling, QLoRA feasibility),
`specs/research/datasets.md` (every dataset used, licences, sizes, eval task list). A third file,
`specs/research/training_stack.md` (libraries, optimizers, forgetting research, export), is added
when available — check the folder.
