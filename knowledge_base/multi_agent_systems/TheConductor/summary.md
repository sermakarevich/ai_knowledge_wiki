# Learning to Orchestrate Agents in Natural Language with the Conductor

**Paper:** [Learning to Orchestrate Agents in Natural Language with the Conductor (Nielsen et al., 2025)](https://arxiv.org/abs/2512.04388)

## Human Readable TL;DR

Imagine you have a team of specialists -- a math wizard, a coding expert, a science whiz -- and a smart manager who figures out how to split tasks between them. This paper trains that manager automatically. Instead of a human writing rules like "ask the math expert first, then the coder to verify," the manager learns on its own just by seeing whether the team got the right answer. The result is a small 7B-parameter manager model that coordinates a group of powerful AI assistants and beats all of them individually on hard tests.

## TL;DR

The Conductor is a 7B LLM trained via reinforcement learning (GRPO) to dynamically orchestrate a pool of diverse worker LLMs. It outputs natural language subtasks, worker agent assignments, and inter-agent access lists, forming flexible multi-step workflows. Trained end-to-end from binary correctness rewards on 960 problems, it achieves SOTA results on LiveCodeBench (83.93%), GPQA-Diamond (87.5%), and AIME25, outperforming both individual frontier models and fixed multi-agent baselines.

---

## Problem & Motivation

Existing multi-agent LLM systems rely on manually designed communication topologies, rule-based routers, or fixed scaffolds. These are labor-intensive, rigid, and fail to adaptively exploit the specialized strengths of different LLMs. No single model dominates across all domains. The challenge is to automatically discover coordination strategies -- which agents to use, how to prompt them, and how to structure information flow -- without human engineering.

---

## Main Original Ideas

1. **Natural Language Workflow as RL Output** -- The Conductor emits a structured plan as three parallel Python lists: `subtasks` (natural language instructions per step), `model_ids` (which worker to call), and `access_lists` (which prior step outputs each worker sees). This unified representation can express sequential, parallel, tree-structured, or arbitrary DAG workflows.

2. **End-to-End Reward from Task Correctness** -- The Conductor is trained purely from binary rewards (correct final answer = 1, otherwise 0/0.5) using GRPO. No intermediate supervision or manually labeled coordination strategies are needed -- optimal orchestration emerges from outcome feedback alone.

3. **Adaptive Worker Selection via Subset Finetuning** -- To generalize across varying agent pools (e.g., open-source-only environments), a pretrained Conductor is finetuned on random k-model subsets, teaching it to compose effective workflows regardless of which agents are available.

4. **Recursive Topologies for Test-Time Scaling** -- The Conductor can list itself as a worker, enabling recursive calls. In a recursive round, it reviews prior workflow outputs and decides to either accept or spawn a new refinement workflow -- providing a tunable inference-time compute axis.

5. **Prompt Engineering as a Learned Skill** -- Unlike routers that merely route queries unchanged, the Conductor generates targeted natural language subtasks per worker per step. Ablations confirm this prompt engineering capability is the primary driver of performance gains over naive agent selection.

---

## Key Findings

| Benchmark | Conductor (7B) | Best Individual Worker | Best Multi-Agent Baseline |
|---|---|---|---|
| LiveCodeBench V6 | **83.93%** | ~81% | -- |
| GPQA-Diamond | **87.5%** | ~85% | -- |
| AIME25 | SOTA (+3%) | GPT-5 | -- |
| Avg (constrained) | **72.35%** | -- | MoA: 62.13% |
| BigCodeBench (recursive) | **40.0%** | -- | Non-recursive: 37.8% |

- A 7B Conductor outperforms GPT-5 and Gemini-2.5-Pro used individually, and beats them when prompted to act as orchestrators themselves.
- Average workflow length is ~3 steps -- competitive inference cost vs baselines despite higher accuracy.
- Open-source-only Conductor outperforms Claude Sonnet 4 standalone by ~10% in constrained settings.
- 3B vs 7B comparison: both select similar agents, but 7B generates better subtask prompts -- natural language capability of the orchestrator is the bottleneck, not agent selection.
- Difficulty-adaptive behavior emerged: hard coding tasks get multi-step plan/implement/verify workflows; simple MMLU questions get 1--2 step workflows.

---

## Suggestions & Future Directions

1. **Multimodal and Cross-Domain Agents** -- Extend to orchestrating vision, audio, or domain-specialized agents (biology, robotics) where natural language is the unifying interface.
2. **Larger Conductor Models** -- The 7B scale is a practical choice; scaling the Conductor itself is an open axis since better language models should produce better prompt engineering.
3. **Deeper Recursive Scaling** -- Current experiments use shallow recursion depths; systematic study of depth vs. compute tradeoffs is left for future work.
4. **Diverse Training Domains** -- Training covers 4 reasoning domains (math, general knowledge, logic, coding); broader coverage may improve generalization to held-out task types.
5. **Fully Open Agent Pools** -- The strongest results use proprietary frontier models; matching these results in a fully open-source setting is a practical open problem.

---

## Authors & Institutions

Stefan Nielsen (Sakana AI), Edoardo Cetin (Sakana AI), Qi Sun (Sakana AI / Institute of Science Tokyo), Peter Schwendeman (Sakana AI / University of Michigan), Jinglue Xu (Sakana AI), Yujin Tang (Sakana AI)
