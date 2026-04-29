# MemCollab: Cross-Agent Memory Collaboration via Contrastive Trajectory Distillation

**Paper:** [MemCollab: Cross-Agent Memory Collaboration via Contrastive Trajectory Distillation (Chang et al., 2026)](https://arxiv.org/abs/2603.23234)

## Human Readable TL;DR

Imagine several employees at a company each keeping their own notes on how to solve problems. If one person shares their notes with another, the tips often don't help because they're written in that person's style and habits. MemCollab is like having a neutral editor compare notes from two different employees who solved the same problem -- one successfully, one not -- and extract the universal lessons (like "always double-check dependencies") while stripping out personal quirks. These cleaned-up lessons go into a shared handbook that helps everyone do better work, regardless of their experience level.

## TL;DR

MemCollab constructs agent-agnostic memory by contrasting reasoning trajectories from heterogeneous LLM agents (e.g., 7B and 32B models) on the same tasks, distilling abstract reasoning constraints that separate task-relevant invariants from agent-specific biases. A task-aware retrieval mechanism conditions memory access on task category to reduce noise. On MATH500, GSM8K, MBPP, and HumanEval, the shared contrastive memory improves both weaker and stronger agents -- boosting Qwen-7B from 57.1% to 71.6% average accuracy -- while reducing inference-time reasoning turns.

---

## Problem & Motivation

Existing agent memory systems are tightly coupled to a single model: memory is built from one agent's trajectories and reused only by that same agent. In modern deployments with heterogeneous model ecosystems (different sizes, architectures, roles), this per-agent coupling prevents knowledge sharing. Naive cross-agent memory transfer actually *degrades* performance because stored memories entangle useful task knowledge with agent-specific biases (preferred heuristics, stylistic shortcuts). The paper asks: can we construct a single shared memory that benefits multiple diverse agents?

---

## Main Original Ideas

1. **Contrastive Trajectory Distillation** -- For each training task, two heterogeneous agents generate trajectories independently. The correct trajectory is contrasted against the incorrect one to extract abstract "reasoning invariants" (what the correct solution preserved) and "violation patterns" (what the incorrect solution broke), filtering out agent-specific artifacts.

2. **Normative Reasoning Constraints** -- Memory entries take the form `(enforce invariant; avoid violation)` expressed using abstract reasoning concepts (accumulation, conditioning, case enumeration) rather than task-specific details. This makes them transferable across problems and agents.

3. **Task-Aware Retrieval** -- A two-stage retrieval mechanism first classifies the query into a task category/subcategory, then retrieves the top-p most relevant memory entries within that category. This reduces noise from irrelevant constraints compared to pure embedding-similarity retrieval.

4. **Cross-Architecture Generalization** -- The framework works not only within a model family (Qwen-7B + Qwen-32B) but also across families (LLaMA-3-8B + Qwen-32B), and in some cases cross-family memory outperforms same-family memory.

---

## Key Findings

### Within-Family Results (Qwen-2.5)

| Backbone | Method | MATH500 | GSM8K | MBPP | HumanEval | Average |
|----------|--------|---------|-------|------|-----------|---------|
| Qwen-7B | Vanilla | 52.2 | 85.4 | 47.9 | 42.7 | 57.1 |
| Qwen-7B | Buffer of Thoughts | 45.8 | 86.4 | **57.6** | 62.2 | 63.0 |
| Qwen-7B | w/ Memory (32B) | 50.6 | 86.6 | 48.6 | 34.1 | 55.0 |
| Qwen-7B | **MemCollab** | **67.0** | **87.4** | **57.6** | **74.4** | **71.6** |
| Qwen-32B | Vanilla | 63.8 | 93.0 | 58.0 | 68.3 | 70.8 |
| Qwen-32B | Self-Contrast Memory | 69.6 | 93.4 | 58.7 | **87.8** | 77.4 |
| Qwen-32B | **MemCollab** | **73.8** | **93.6** | **64.3** | 86.6 | **79.6** |

### Cross-Family Results (LLaMA-3-8B + Qwen-32B)

| Backbone | Method | MATH500 | GSM8K | MBPP | HumanEval | Average |
|----------|--------|---------|-------|------|-----------|---------|
| LLaMA-3-8B | Vanilla | 27.4 | 73.0 | 37.0 | 29.3 | 41.7 |
| LLaMA-3-8B | **MemCollab** | **42.4** | **74.4** | **49.8** | **48.8** | **53.9** |
| Qwen-32B | **MemCollab** | **70.6** | **95.2** | 60.3 | **86.6** | **78.2** |

### Inference-Time Efficiency (Qwen-7B avg reasoning turns)

| Dataset | Vanilla | MemCollab |
|---------|---------|-----------|
| MATH500 | 2.7 | 2.2 |
| GSM8K | 1.8 | 1.6 |
| MBPP | 3.1 | 1.4 |
| HumanEval | 3.3 | 1.5 |

- Naive memory transfer from 32B to 7B *hurts* performance (50.6% vs 52.2% on MATH500), confirming that raw memory entangles agent-specific bias
- Cross-architecture contrast can outperform same-family contrast (GSM8K: 95.2% cross-family vs 93.6% same-family for Qwen-32B)
- Optimal retrieval count is p=3; performance degrades beyond task-dependent thresholds due to noise
- Task-aware retrieval outperforms both embedding-based and prompting-based retrieval across all benchmarks

---

## Suggestions & Future Directions

1. **Multi-Agent Extension** -- Extend the pairwise contrastive formulation to settings with more than two agents by selecting one preferred trajectory and treating all others as unpreferred.
2. **Scalable Shared Memory** -- Build memory systems that scale to larger collections of interacting agents beyond the current two-agent setup.
3. **Cross-Domain Transfer** -- Investigate whether reasoning constraints from math tasks transfer to coding tasks or vice versa.
4. **Dynamic Memory Updates** -- The current memory bank is static after construction; future work could explore online memory evolution as agents encounter new tasks.
5. **Limitations acknowledged**: Trajectory diversity depends heavily on initial agent heterogeneity -- homogeneous agents provide minimal collaboration benefits; extreme domain shifts between training and inference reduce effectiveness.

---

## Authors & Institutions

Yurui Chang (Pennsylvania State University), Yiran Wu (Pennsylvania State University), Qingyun Wu (AG2AI), Lu Lin (Pennsylvania State University)
