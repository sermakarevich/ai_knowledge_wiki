# Task: chapter wrap-up — README, Q&A seed, cross-links, knowledge-base index entry, consistency pass

Read `specs/COMMON.md`, `index.md` and ALL chapters `00_*.md`–`10_*.md` (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`).

## Problem
Ten chapters were written by different workers over days. The tutorial needs a consistency pass
(names, paths, recipes, numbers), a `project/README.md`, a seeded `Q&A.md`, and an entry in the
parent `../index.md` so `ai show tutorials` lists it.

## Fix
1. **Consistency pass** (edit chapters only where wrong): every `just` recipe mentioned in a chapter exists in `project/justfile` (`just --list` in `project/`); every path (`runs/models/…`, `configs/…`) exists or is described as created by a command; every number quoted in a chapter matches the `metrics.json` it comes from (spot-check at least 3 per chapter; fix the chapter, never the metrics); the chapter list and one-line descriptions in `index.md` match the real chapter contents (edit descriptions in `index.md` if a chapter ended up covering something differently — e.g. the dense fallback, a reduced token budget, a skipped 27B merge); "previous/next" links resolve. Fill in the "Verified on" line in `index.md` with the real dates and versions from the runs.
2. **`project/README.md`** (≤ 80 lines): what this project is, the two-machine setup in 5 lines, quick start (`just sync`, `just remote-sync`, `just check`), the stage → recipe → output folder table (pretrain, sft, dpo, grpo, export, eval, ft, forget), and where the numbers live.
3. **`Q&A.md`**: heading, one sentence explaining the file is appended during Q&A sessions, and 5 seeded Q&As answered from the chapters (e.g. "Why not train the 27B from scratch?", "Why 3 linear-attention layers per full-attention layer?", "Why does DPO use a smaller learning rate than SFT?", "Why can't lm_eval score MMLU through Ollama?", "Which anti-forgetting recipe won here and by how much?").
4. **`../index.md`** (the tutorials index): add under a new section `## Machine learning & LLMs` a line `- [llm_training/index.md](llm_training/index.md) — LLM training and fine-tuning from zero on one RTX 4090: build a ~110M Qwen3.5-architecture model from scratch (tokenizer, pre-training, SFT, DPO, GRPO), export it to Ollama, then fine-tune Qwen3.5-4B and Qwen3.8-27B (QLoRA) to a cybersecurity domain and measure domain accuracy vs general benchmarks, with recipes against catastrophic forgetting.`
5. Run `cd project && uv run pytest tests/ -q -m "not slow"` and `just --list`; fix anything broken.
6. On `rtx`: `rm -rf ~/projects/_llm_check` (a scratch venv from planning) if it still exists; list `du -sh ~/projects/llm_training/runs` and put the total disk footprint in the README.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md, plus: commit `project/README.md`, `Q&A.md`, `index.md`, `../index.md`, any chapter files you corrected. Verify: `git show HEAD:knowledge/tutorials/index.md | grep -c llm_training` ≥ 1. Close with a summary listing which chapters were corrected.

## Scope & constraints
No new features, no new runs on the GPU (read-only on rtx except the scratch-venv cleanup). Do not touch other tutorials' folders except the one line in `../index.md`.

8. In `index.md`, add one line after the "Runnable project" paragraph: "`specs/` holds the build instructions and research notes used by the fleet workers that wrote this tutorial (one spec per chapter, `COMMON.md` shared rules, `research/` sources with links). It is not part of the reading path." (`index.md` edit allowed for this line only.)
