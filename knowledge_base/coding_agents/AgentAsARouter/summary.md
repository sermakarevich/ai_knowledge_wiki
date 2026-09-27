# Agent-as-a-Router: Agentic Model Routing for Coding Tasks

**Paper:** [Agent-as-a-Router: Agentic Model Routing for Coding Tasks (Zhou et al., 2026)](https://arxiv.org/abs/2606.22902)

## Human Readable TL;DR

Imagine you have several expert consultants, each great at different things: one is best at fixing bugs, another excels at algorithm puzzles, a third shines at writing tests. Instead of always calling the same consultant for every problem, this paper builds a smart dispatcher that learns from experience — tracking which expert solved past problems and routing each new problem to the right one. The more problems it dispatches, the better it gets at choosing. This beats both always calling the most expensive consultant and using a fixed rule like "send all bug fixes to expert A."

## TL;DR

The paper identifies *information deficit* as the core bottleneck in LLM routing: zero-shot routers lack execution-grounded knowledge of which model excels at what. The authors propose Agent-as-a-Router, formalizing routing as a C-A-F (Context→Action→Feedback→Context) loop equivalent to a contextual bandit. Their instantiation, ACRouter, combines a fine-tuned 0.8B Orchestrator, a sandbox Verifier, and an online vector-store Memory. Evaluated on CodeRouterBench (~10K tasks, 8 frontier LLMs), ACRouter achieves the lowest cumulative regret on both in-distribution and out-of-distribution agentic-programming tasks, outperforming all static routers and single-model baselines.

---

## Problem & Motivation

Real-world users access multiple LLMs (Claude, GPT-5, Qwen, Kimi, etc.) whose strengths vary by task type. No single model dominates all coding dimensions: Claude Opus 4.6 leads on code completion and average but falls far behind GLM-5 on algorithm design (25.4% vs. 47.2%) and Qwen3-Max on test generation (39.2% vs. 82.7%). The best model varies per task, yet cost differentials are large (~20× between Opus and MiniMax).

Existing routers treat routing as a static classification problem, but their real bottleneck is *information deficit*: they don't know which model performs well on what. Providing per-dimension performance statistics to a vanilla LLM router gives a **+15.3% relative gain** (41.41% → 47.74% AvgPerf), exceeding a heuristic DimensionBest router with the same priors. This shows the problem is not reasoning capability but information access. Static routers can never close this gap because their information state is frozen after training.

---

## Main Original Ideas

1. **C-A-F Loop Formalization.** Routing is cast as a Context-Action-Feedback loop: `cᵢ → Decide → aᵢ → Execute → fᵢ → Memorize → cᵢ₊₁`. Each completed loop enriches context for the next decision. This maps to a contextual multi-armed bandit with *cumulative regret* as the natural streaming metric -- a departure from accuracy-at-a-snapshot evaluation.

2. **ACRouter -- Loop-Complete Instantiation.** Three cooperating modules: (a) **Orchestrator** -- Qwen3.5-0.8B LoRA fine-tuned + heuristic rules via weighted voting, integrates DimensionBest prior + top-10 kNN neighbors from Memory; (b) **Verifier** -- sandbox-native scoring across AST parsing, execution, prompt-embedded tests, and rule-based signals, producing a unified score committed to Memory; (c) **Memory** -- online vector store keyed by voyage-code-3/BGE-large task embeddings, cosine kNN retrieval (k=10, threshold 0.5), FIFO-capped at 20K entries.

3. **CodeRouterBench.** The first benchmark designed for regret-based router comparison on streaming tasks: ~10K tasks across 10 coding dimensions from 15+ source benchmarks, with execution-verified scores from 8 frontier LLMs, 60/10/30 probing/val/test split, and a held-out OOD split of 176 agentic programming tasks.

4. **Decomposed Routing Taxonomy.** All routing strategies are unified under the C-A-F lens by restricting/removing modules: Single-Model (no components), Heuristic (frozen Memory, no Verifier), Trained Policy (trained Orchestrator, no Memory/Verifier), Online Bandit (parametric Memory, reward-only Verifier), ACRouter (full loop). This enables systematic ablation and comparison.

5. **Coding Ability ≠ Routing Ability.** Empirically, Claude Opus 4.6 (strongest coder) ranks last as a zero-shot router (39.27% AvgPerf), while smaller, cheaper models (Qwen3.5-Plus, GLM-5) outperform it as routers. Routing performance does not correlate with raw coding strength.

---

## Key Findings

| Router | AvgPerf% ↑ | CumReg ↓ | Perf/$ ↑ | OOD AvgPerf% |
|---|---|---|---|---|
| Oracle | 57.00 | 0 | 8.20 | 75.89 |
| **ACRouter (ours)** | **49.98** | **205.5** | 3.79 | **62.50** |
| LinUCB | 46.84 | 296.9 | 4.38 | 49.82 |
| DimensionBest | 47.50 | 277.4 | 3.69 | -- |
| Qwen3.5-0.8B-FT | 46.41 | 309.1 | 6.82 | 55.36 |
| LogReg | 47.26 | 284.4 | 6.27 | 19.64 |
| Always-Opus 4.6 | 43.83 | 387.1 | 1.29 | 57.14 |
| Random | 38.75 | 533.6 | 2.48 | 31.25 |

- **Static trained models collapse on OOD:** LogReg, TF-IDF+MLP, RouteLLM-BERT score 8.93%--21.43% on OOD agentic tasks -- below Random (31.25%). ACRouter scores 62.50%, the only router above Always-Opus.
- **Scale doesn't help static routers:** Qwen router scaling from 0.8B to 27B yields only 0.5 AvgPerf spread (46.21% to 46.74%); the bottleneck is training data, not parameters.
- **Dimension identity explains only ~27%** of per-task oracle entropy; 73% of routing signal lives in per-task content, which ACRouter's embedding Memory directly captures.
- **Cost regimes:** cheap trained classifiers ($6.81--$7.69) near DimensionBest; ACRouter moderate ($13.21) for +2.5% AvgPerf gain; Always-Opus premium ($34.02) with worse performance than ACRouter.

---

## Suggestions & Future Directions

1. **Generalize C-A-F beyond model routing** -- the loop applies identically to tool selection, API endpoint selection, prompt strategy selection, thinking-effort allocation, and sub-agent routing.
2. **Alternative Memory architectures** -- parameter-level memory (gradient updates, neural retrieval) beyond cosine-kNN may yield better generalization.
3. **Living benchmark protocol** -- V2 adds new models (run them on existing task set); V3 adds new coding dimensions (contribute C-A-F triples + scoring function); community-maintained to stay current with the model landscape.
4. **Relaxing the step limit** -- OOD evaluation used a 40-step limit vs. standard 250 for budget reasons; full evaluation may change absolute numbers.
5. **Cost observability** -- provider-side caching makes exact monetary cost estimation unreliable; better cost signals would improve the reward function.

---

## Authors & Institutions

Pengfei Zhou (NUS), Zhiwei Tang (DAMO Academy/Alibaba, Hupan Lab, UC Berkeley), Yixing Ma (Hupan Lab), Jiasheng Tang (DAMO Academy/Alibaba, Hupan Lab), Yizeng Han (DAMO Academy/Alibaba), Zhenglin Wan (NUS), Fanqing Meng (NUS), Wei Wang (HKUST), Bohan Zhuang (Zhejiang University), Wangbo Zhao (HKUST), Yang You (NUS)
