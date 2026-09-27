# Training AI Scientists to Replicate Research

**Paper:** [Training AI Scientists to Replicate Research (Falck, Sabri, Surina, Foster, Sims, Devlin, Rogers, Collins, Aleksiev, Kirsch, Hughes, 2026)](https://arxiv.org/abs/2608.13331)

## TL;DR

LLM agents are good at closed-ended coding tasks but bad at open-ended scientific work, because there's no clean reward signal to train on. This paper builds one: **Replica**, an auto-generated task space of 310 "replicate this redacted figure from a real ML/AI-for-science paper" tasks, scored by a **rubric-based LLM judge** validated against expert human rankings. They use it to RL-post-train **Faraday**, a 27B-parameter model that directs a much larger frontier coding agent (Codex GPT-5.5, ~5T params) as a tool — a "Coding Agent as a Tool" (CAT) design. Faraday beats Claude Opus 4.8 and GPT-5.5 on 73% of in-distribution and 60% of held-out replication tasks, generalizes to full-scale compute budgets and swapped-in stronger tools, and behaves more like a careful human scientist (implementing real mechanisms, avoiding shortcuts) than the baselines.

---

## Why it matters

Science has a replication crisis, and AI agents are a candidate scalable fix — but only if you can train them on open-ended research tasks, which historically have no verifiable reward. This paper shows a path: turn replication into a scalable, auto-gradeable task space, and post-train a *small* model to orchestrate a *large* frontier coding model, rather than trying to out-scale it. The result is evidence that "research taste" can live in weights and compound with whatever coding agent it's paired with.

## The core pieces

1. **Replica** — 100 well-known ML and AI-for-science papers (1990–2026) turned into 310 figure-replication tasks by redacting one results figure per task (auto-generated via a 3-stage Gemini 2.5 Pro vision pipeline), each solved under a 60-minute, 1/7-H200-GPU budget.
2. **Rubric judge** — Claude Opus 4.7 writes a task-specific 5-dimension rubric (blind to the "gold" figure); a Codex-based judge scores rollouts against it with 3 samples, achieving much higher agreement with human expert rankings than a generic judge baseline.
3. **Faraday** — Qwen3.6-27B, post-trained with a modified GRPO (turn-level credit assignment, LoRA) to direct a coding-agent tool through a minimal 5-tool harness (apply_patch, read_file, list_dir, grep_files, shell).
4. **Results** — Faraday outperforms both Claude Opus 4.8 and GPT-5.5/Codex on the held-out AI-for-science split (60%) and the in-distribution ML split (73%), generalizes to 8-hour/8-GPU full-scale tasks, and keeps winning when the underlying coding-agent tool is swapped for a stronger one without retraining.

## Read next

- [[digest|Digest]] for the medium-depth, whole-paper pass.
- [[index|Wiki hub]] to navigate all 7 wiki pages, the explainer, questions, critique, and connections.
