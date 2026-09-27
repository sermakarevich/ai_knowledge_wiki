# AutoMem: Automated Learning of Memory as a Cognitive Skill

**Paper:** [AutoMem: Automated Learning of Memory as a Cognitive Skill (Wu, Zhu, Zhang, Wang, Yeung-Levy, 2026)](https://arxiv.org/abs/2607.01224)

## Human Readable TL;DR

Imagine an employee who's great at their job but bad at taking notes -- they forget where they put things, keep re-writing the same reminder, and never learn from past mistakes. This paper teaches an AI agent to get *good at taking notes*, treating "how to manage your notebook" as its own skill separate from "how to do the job." A smarter AI coach reads through the agent's whole workday, redesigns its notebook format (fewer duplicate entries, auto-updated status pages), and then trains the agent specifically on its own best note-taking habits -- without touching how it actually plays the game. The result: a mid-size open AI model gets 2-4x better at long, complicated games just by learning to keep better notes, catching up to much bigger, more expensive commercial AI systems.

## TL;DR

AUTOMEM treats LLM-agent memory management -- file-system read/write/search/create operations -- as a first-class, independently trainable skill rather than a fixed architecture. It uses two sequential meta-LLM-driven outer loops around a frozen inner-loop agent: (1) a scaffold optimizer that reviews complete episode traces and iteratively rewrites the agent's memory code/prompts/file schema, and (2) a training engine that curates the agent's own good memory decisions as supervised data to LoRA-finetune a dedicated "memory specialist" model, leaving the task-action model untouched. Across three procedurally generated long-horizon games (Crafter, MiniHack, NetHack) built on the BALROG benchmark, optimizing memory alone improved a Qwen2.5-32B-Instruct base agent's progression rate ~2x-4x, making it competitive with frontier proprietary systems like Claude Opus 4.5 and Gemini 3.1 Pro Thinking.

---

## Problem & Motivation

LLMs face a fixed context window that acts as working memory, which is quickly exceeded in long-horizon tasks (some NetHack episodes span 10^4-10^5 steps). Prior external-memory approaches (RAG, MemGPT, scratchpads, summary buffers) treat memory as a fixed architectural module designed by humans. Cognitive science instead frames memory expertise as *metamemory* -- a learned skill covering what to encode, when to retrieve, and how to organize knowledge. The paper asks whether this metamemory concept can be operationalized as something LLM agents *automatically learn*, rather than something engineers hand-design. The core obstacle is that memory decisions have delayed consequences (a mistake at step 50 may not surface until step 800), so manual human review of complete trajectories (up to 10^5 steps) is intractable -- motivating automation via a "meta-LLM" that reads full episode traces the way a code reviewer reads an execution log.

---

## Main Original Ideas

1. **Memory as a first-class, trainable action space.** File-system operations (read, write, search, append, create) are promoted to the same action space as task actions, letting the model itself decide what to store, look up, and how to structure records -- rather than being handled by a hidden retrieval module.
2. **Two orthogonal learnable axes: structure vs. proficiency.** Memory skill improves along the *structure* that supports it (prompts, file schema, action vocabulary) and the *proficiency* of the model exercising it (parametric decision-making ability). AUTOMEM automates both independently.
3. **Outer-loop 1 -- scaffold optimizer.** A strong meta-LLM (Claude Opus 4.6, effort=max) reads complete agent trajectories, diagnoses memory-related failure patterns (e.g., an unbounded append-only map file accumulating duplicate coordinates), and rewrites the agent's code/prompts/file schema. A revision is accepted only if it strictly improves average progression on fixed eval seeds versus the prior version (gated iteration, up to one retry on failure).
4. **Outer-loop 2 -- memory proficiency training.** Once the scaffold converges, a second meta-LLM (Claude Opus 4.7) acts as a training engine: it selects which of the agent's own past memory decisions (from up to hundreds of episodes) are worth reinforcing, curates them as supervised training data, and picks a matching LoRA configuration. This data is used to finetune a separate, dedicated **memory specialist** model via LoRA, while the **task/gameplay model stays completely frozen** -- so memory proficiency gains stack without risking existing task competence.
5. **Two-model inference-time split.** At inference, one frozen model commits world/task actions while the LoRA-tuned memory specialist handles only the LOG (what to record) and PLAN (what to recall) memory operations, sharing one conversation history -- isolating the training signal purely to memory behavior.

---

## Key Findings

**Table 1 — Progression rate (%) on BALROG long-horizon games, Qwen2.5-32B-Instruct base:**

| Agent | Crafter (%) | MiniHack (%) | NetHack (%) |
|---|---|---|---|
| Gemini-3-Pro (frontier) | 57.3 ± 4.4 | 40.0 ± 7.7 | 6.8 ± 3.2 |
| Claude-Opus-4.5 (frontier) | 49.5 ± 3.1 | 27.5 ± 7.1 | 2.0 ± 0.5 |
| Gemini-3.1-Pro-Thinking (frontier) | 55.0 ± 6.4 | 27.5 ± 7.1 | 2.6 ± 0.3 |
| Qwen2.5-72B-Instruct (open, larger) | 27.3 ± 3.6 | 5.0 ± 3.4 | 0.3 ± 0.3 |
| Qwen2.5-32B + memory-as-file-system (v0, base) | 25.00 ± 5.50 | 7.50 ± 4.16 | 0.42 ± 0.37 |
| **+ scaffold opt. (loop #1)** | 47.27 ± 2.05 | 27.50 ± 7.06 | 1.57 ± 0.35 |
| **+ memory training (loop #2, full AUTOMEM)** | **51.36 ± 3.81** | **30.00 ± 7.25** | **1.85 ± 0.44** |

- Optimizing memory alone (model weights for task actions untouched) took the 32B model from 25.0%→47.27% on Crafter (×1.89), 7.5%→27.5% on MiniHack (×3.67), and 0.42%→1.57% on NetHack (×3.74) -- purely from scaffold revision.
- Memory-specialist training added a further +4.09 (Crafter), +2.5 (MiniHack), +0.28 (NetHack) points on top of the optimized scaffold.
- The final 32B agent **outperforms Qwen2.5-72B-Instruct** (larger, same family) by a wide margin and beats the same base model under a basic sliding-window context strategy by an even wider margin -- indicating memory management is a higher-leverage axis than model scale or generic context management on these tasks.
- It reaches performance comparable to Claude Opus 4.5 and within a few points of Gemini 3.1 Pro Thinking across all three games.
- Behavioral analysis (Figure 4): scaffold optimization alone (without touching task-action weights) reduces the "unproductive action rate" (stuck/oscillating steps) by 32-65% across all three environments; redundant memory writes drop 68-83%; empty-search rate falls 13-50%; per-step input context shrinks 3-30% tokens.
- Concrete example (NetHack): replacing an append-only `dungeon_map.txt` with a coordinate-keyed `<|UPSERT_MAP|>` dedup operation shrinks per-step memory growth from 138 to 6 characters/step (95% reduction).
- Trained memory specialists show a "consult-before-write" discipline: the write-to-search ratio in the LOG phase falls in every environment (Crafter 0.84→0.39, MiniHack 2.89→0.82, NetHack 4.66→1.31), i.e., -54% to -72% fewer blind writes relative to searches.
- Ablation-style qualitative traces (Figure 6) show e.g. MiniHack's Corridor-R3 task going from 0%→0%→100% progression across base→evolved-scaffold→trained-specialist stages -- neither the base nor the evolved scaffold alone solves it, but the trained specialist does.

---

## Suggestions & Future Directions

1. **Persistent memory across episodes.** Current memory is *episodic* -- the file system resets every episode; extending to memory that carries knowledge across episodes is a natural next step.
2. **Beyond game environments.** Experiments are limited to procedurally generated games; applying the approach to real-world, memory-intensive tasks is proposed as future work.
3. **Shared scaffolds/specialists across environments.** Currently a separate scaffold and memory specialist is optimized per game; whether a single scaffold or specialist can generalize across environments remains unexplored.
4. **Generalizing the "trajectory-level review + targeted revision" workflow** beyond memory to other agent capabilities is suggested as a promising direction.
5. **Broader impacts caveat:** the authors note the released artifacts are not directly applicable to high-stakes deployment without further safety review, since automated scaffold optimization also lowers the model-scale threshold at which long-horizon agents become practical.

---

## Authors & Institutions

Shengguang Wu, Hao Zhu, Yuhui Zhang, Xiaohan Wang, Serena Yeung-Levy -- Stanford University.

Project page: https://autolearnmem.github.io/ · Code: https://github.com/autoLearnMem/AutoMem
