# Memory Intelligence Agent

**Paper:** [Memory Intelligence Agent (Qiao, Meng, Cheng et al., 2026)](https://arxiv.org/abs/2604.04503)

## Human Readable TL;DR

Imagine a research assistant who not only searches the web for answers but also keeps a personal notebook of past searches -- remembering what worked, what didn't, and developing better strategies over time. This paper builds exactly that for AI agents: a system with a "manager" who organizes past experiences, a "planner" who creates search strategies based on those memories, and an "executor" who carries out the plan. The clever part is that the system teaches itself to get better at research by reviewing its own work, even without anyone grading it -- like a student who improves by re-reading their own essays critically.

## TL;DR

MIA introduces a Manager-Planner-Executor architecture for Deep Research Agents that combines non-parametric memory (compressed trajectory storage) with parametric memory (RL-trained planner internalization). A two-stage alternating GRPO training aligns planning and execution, while test-time learning enables continuous self-evolution. MIA outperforms prior memory-based methods by 5.5--7.5 points across 11 benchmarks and approaches closed-source frontier models using only a 7B executor.

---

## Problem & Motivation

Deep Research Agents (DRAs) that combine LLM reasoning with web search tools struggle with memory. Current approaches either stuff long search histories into context -- causing attention dilution, noise, and ballooning costs -- or store factual knowledge that doesn't help with *process*-level strategy reuse. Planners lack task-specific training, executors don't follow plans well, and there's no mechanism for agents to autonomously improve in unsupervised settings. MIA addresses all of these by decoupling memory management, strategic planning, and execution into a collaborative multi-agent framework with continuous learning.

---

## Main Original Ideas

1. **Manager-Planner-Executor Architecture** -- Decouples memory storage (Manager with non-parametric buffer), strategic planning (Planner as parametric memory), and task execution (Executor with ReAct loop), preventing long-context degradation while enabling specialized optimization of each role.

2. **Bidirectional Memory Conversion** -- Establishes a loop between non-parametric memory (compressed trajectories) and parametric memory (Planner weights). Episodic experiences are internalized into the Planner via RL training, while high-value trajectories are preserved explicitly for in-context few-shot learning.

3. **Two-Stage Alternating RL Training** -- Uses GRPO to alternately train the Executor (plan following, tool use, reasoning) and then the Planner (memory absorption, plan generation, reflection), ensuring mutual alignment rather than independently optimized components.

4. **Hybrid Memory Retrieval** -- Scores stored memories across three dimensions: semantic similarity, value reward (success rate), and frequency reward (encouraging exploration of underused memories), balancing exploitation and exploration.

5. **Reflect-Replan Mechanism** -- When the Executor hits an impasse, it reports back to the Planner, which adjusts the search plan dynamically (triggered at most once per query), enabling adaptive recovery from execution failures.

6. **Unsupervised Self-Evolution via Peer Review** -- Introduces an LLM-based evaluation framework mimicking scientific peer review with three specialized reviewers and an area chair, providing approximate supervision for continuous self-improvement without ground-truth labels.

7. **Continual Test-Time Learning (TTL)** -- Updates the Planner's parameters on-the-fly during inference using GRPO over multiple rollouts, enabling the agent to internalize new experiences without retraining from scratch.

---

## Key Findings

| Benchmark Type | Method | Avg Accuracy |
|---|---|---|
| **Multimodal (open-source)** | MIA | **53.6** |
| | Memento (prev. best) | 48.1 |
| | No Memory baseline | ~47 |
| **Text-only** | MIA | **53.5** |
| | Memento | 46.0 |

- Traditional contextual memory methods (RAG, Mem0, A-Mem) *underperformed* the no-memory baseline, confirming that naive long-context memory introduces harmful noise
- MIA with a 7B Executor approached or surpassed GPT-4o, Gemini-2.5-Pro, and GPT-5.4 on multimodal benchmarks despite using only basic search tools
- Generalization to closed-source executors: MIA's Planner improved GPT-5.4 by +8.9 on LiveVQA and +6.4 on HotpotQA without any TTL
- Ablation results show each module contributes: memory-guided planning (+3.2), reflection (+1.1), alternating RL training (+2.5), and TTL (+2.1) on multimodal tasks
- Unsupervised MIA matched supervised baselines on multimodal benchmarks and *surpassed* them on text-only benchmarks
- Multi-epoch self-evolution showed consistent gains (59.6 -> 61.1 -> 61.7), demonstrating progressive improvement from accumulated experience

---

## Suggestions & Future Directions

1. **Extend to more dynamic environments** -- The authors note MIA could be applied to even more complex, real-time domains beyond the current benchmark suite.
2. **Scale the unsupervised evaluation framework** -- The peer-review-style judgment mechanism could be refined with more diverse reviewer specializations or calibrated against human evaluations.
3. **Explore richer tool ecosystems** -- MIA currently uses basic text and image search; integrating code execution, database queries, or domain-specific APIs could amplify its capabilities.
4. **Investigate longer-horizon self-evolution** -- While multi-epoch TTL showed consistent gains, studying convergence behavior and potential degradation over many more epochs remains open.
5. **Cross-domain transfer of parametric memory** -- Whether a Planner trained on one domain's search strategies can transfer effectively to new domains is an open question.

---

## Authors & Institutions

Jingyang Qiao (East China Normal University), Weicheng Meng (East China Normal University), Yu Cheng (East China Normal University), Zhihang Lin (Xiamen University), Zhizhong Zhang (East China Normal University, corresponding author), Xin Tan (East China Normal University), Jingyu Gong (Shanghai Innovation Institute), Kun Shao (Harbin Institute of Technology), Yuan Xie (East China Normal University, Shanghai AI Lab, project leader)
