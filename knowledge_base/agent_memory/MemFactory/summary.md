# MemFactory: Unified Inference & Training Framework for Agent Memory

**Paper:** [MemFactory: Unified Inference & Training Framework for Agent Memory (Ziliang Guo, Ziheng Li, Bo Tang, Feiyu Xiong, Zhiyu Li, 2025)](https://arxiv.org/abs/2603.29493)

## Human Readable TL;DR

Imagine building with Lego bricks -- you can mix and match pieces to build whatever you want. MemFactory does the same thing for AI agents that need long-term memory. Instead of researchers having to reinvent the memory plumbing from scratch each time, MemFactory gives them standardized, swappable pieces (how to store memories, how to update them, how to find them) and a built-in teacher (reinforcement learning) that trains the agent to get better at managing those memories over time. Think of it as a gym + toolbox for AI agents learning to remember things well.

## TL;DR

MemFactory is the first unified training and inference framework for memory-augmented LLM agents, providing a modular "Lego-like" architecture (Extractors, Updaters, Retrievers) and native Group Relative Policy Optimization (GRPO) for RL-driven memory policy training. It standardizes implementations of Memory-R1, MemAgent, and RMM paradigms into one extensible platform, enabling single-GPU training. Empirical validation on Qwen3-1.7B and Qwen3-4B-Instruct shows 7--15% performance gains on long-context tasks over base models.

---

## Problem & Motivation

LLM-based agents increasingly need persistent, adaptive memory across long interactions. Existing approaches -- static RAG, heuristic update rules, or bespoke RL implementations -- are deeply task-coupled and dispersed across isolated repositories. There is no unified infrastructure analogous to LLaMA-Factory for memory-augmented agents, causing redundant engineering effort, poor reproducibility, and a high barrier to entry for researchers wanting to combine or compare memory strategies.

---

## Main Original Ideas

1. **Unified Memory-RL Framework** -- MemFactory is the first platform unifying training, inference, and evaluation for memory-augmented agents. It reduces engineering overhead so researchers focus on algorithms, not plumbing.

2. **Atomic Module Layer** -- The memory lifecycle is decomposed into four plug-and-play classes: `MemoryExtractor` (parse context into facts), `MemoryUpdater` (ADD/DEL/UPDATE/NONE operations), `MemoryRetriever` (semantic + LRM-reranked retrieval), and `AgentModule` (end-to-end recurrent memory, e.g., MemAgent style). Each exposes standardized `generate`, `rollout`, and `inference` interfaces.

3. **Lego-like Agent Layer** -- Agents are assembled by composing modules; the same composition works for RL training (rollout mode) and pure inference (OpenAI-style API + vLLM), enabling fair comparisons between different architectures without code changes.

4. **GRPO-based Trainer Layer** -- Implements Group Relative Policy Optimization, which estimates the advantage baseline by intra-group reward normalization across G sampled responses -- eliminating the need for a separate critic network, cutting memory footprint and enabling single-GPU RL training.

5. **Environment Layer with Multi-Dimensional Rewards** -- Two environment types (`MemoryBankEnv` for explicit long-term memory banks, `LongcontextEnv` for dialogue-history scenarios) with Format Rewards and LLM-as-a-Judge signals provide flexible, task-agnostic reward computation.

6. **Out-of-the-Box Baselines** -- Memory-R1, MemAgent, and RMM are standardized as first-class citizens, lowering reproduction cost and enabling direct comparisons.

---

## Key Findings

| Model | Setting | Base Score | MemFactory RL Score | Delta |
|---|---|---|---|---|
| Qwen3-1.7B | eval_50 | 0.4727 | **0.5684** | +20.2% |
| Qwen3-1.7B | eval_100 | 0.4297 | **0.4863** | +13.2% |
| Qwen3-1.7B | eval_fwe_16384 (OOD) | 0.0332 | 0.0195 | -41.3% |
| Qwen3-1.7B | **Average** | 0.3118 | **0.3581** | **+14.8%** |
| Qwen3-4B-Instruct | eval_50 | 0.6620 | **0.6975** | +5.4% |
| Qwen3-4B-Instruct | eval_100 | 0.6128 | **0.6385** | +4.2% |
| Qwen3-4B-Instruct | eval_fwe_16384 (OOD) | 0.6270 | **0.6426** | +2.5% |
| Qwen3-4B-Instruct | **Average** | 0.6146 | **0.6595** | **+7.3%** |

- The smaller 1.7B model degrades on the OOD benchmark, suggesting the learned policy is less transferable at small scale.
- The 4B-Instruct model generalizes better, achieving gains on all sets including OOD.
- Training ran on a single NVIDIA A800 80GB GPU for 250 steps, confirming single-GPU viability.
- Simplified training data (50--80 docs vs. full-length) still yields meaningful gains, indicating data efficiency.

---

## Suggestions & Future Directions

1. **Broader paradigm coverage** -- Integrate additional Memory-RL methods beyond Memory-R1, MemAgent, and RMM as the field matures.
2. **Scale-up experiments** -- Validate framework gains with larger models (7B+) and full-length training data to confirm scalability.
3. **OOD generalization** -- Address the observed OOD degradation for smaller models, potentially via curriculum learning or diverse training distributions.
4. **Community contributions** -- The modular design is positioned as infrastructure for the community to contribute new extractors, updaters, and retrievers without touching core training logic.
5. **Richer reward signals** -- Explore additional multi-dimensional reward formulations beyond format and LLM-judge to guide more nuanced memory policies.

---

## Authors & Institutions

Ziliang Guo (MemTensor), Ziheng Li (MemTensor), Bo Tang (MemTensor), Feiyu Xiong (MemTensor), Zhiyu Li (MemTensor, corresponding author)
