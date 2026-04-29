# Agent-World: Scaling Real-World Environment Synthesis for Evolving General Agent Intelligence

**Paper:** [Agent-World: Scaling Real-World Environment Synthesis for Evolving General Agent Intelligence (Dong, Lu, Song, et al., 2026)](https://arxiv.org/abs/2604.18292)

## Human Readable TL;DR

Imagine teaching a personal assistant to navigate dozens of real websites, apps, and databases — not by writing scripts for every single one, but by letting the assistant practice in thousands of realistic copies of those environments. Agent-World is a system that automatically builds nearly 2,000 lifelike digital "playgrounds" (like mock GitHub repos, Notion workspaces, or airline booking systems) from real-world sources, then has an AI agent practice inside them. When the agent struggles with certain tasks, the system notices the weak spots and automatically generates harder practice problems in those specific areas — so the agent keeps getting better on its own, like a student who receives a custom-tailored tutor that constantly adjusts the curriculum.

## TL;DR

Agent-World is a closed-loop framework that couples scalable real-world environment synthesis with continuous self-evolving reinforcement learning for LLM agents. It autonomously mines 1,978 stateful, database-grounded environments with 19,822 executable tool interfaces from MCP servers, tool documentation, and product requirement documents, then synthesizes verifiable agentic tasks via graph-based and programmatic strategies. A diagnostic arena periodically identifies weak environments from agent failures and generates targeted training data, producing monotonic improvements across 23 benchmarks. Agent-World-14B outperforms prior environment-scaling baselines and rivals much larger open-source models (e.g., DeepSeek-V3.2-685B on BFCL-V4).

---

## Problem & Motivation

Training LLM agents to act as general-purpose assistants in real-world settings faces two persistent bottlenecks:

1. **Scarce scalable, realistic environments.** Purely LLM-simulated environments hallucinate and fail to capture real-world state transitions; environments built on small open-source toolchains lack the diversity and complexity needed for long-horizon, state-intensive tasks.
2. **No principled self-improvement loop.** Existing agent RL work focuses on building environments but provides no systematic way for an agent to diagnose its own capability gaps and drive targeted improvement over time.

The paper argues that closing these gaps requires a unified pipeline where environments and agent policies co-evolve, turning the environment ecosystem into an automated curriculum engine rather than a static dataset.

---

## Main Original Ideas

1. **Agentic Environment-Task Discovery.** A deep-research agent autonomously mines topic-aligned databases from three real-world sources (MCP servers from Smithery, open tool-use datasets, industrial PRDs), iteratively complexifies them, and generates executable Python tool interfaces plus unit tests. Tools are cross-validated (compile + pass >50% tests) producing 1,978 grounded environments with 19,822 tools.

2. **Dual-strategy Verifiable Task Synthesis.** Tasks are generated via (a) graph-based synthesis, which random-walks a weighted directed tool-dependency graph to produce sequential tool chains with ground-truth answers and rubrics, and (b) programmatic synthesis, which has an LLM emit complex Python control flows debugged in a sandbox and accompanied by executable validator scripts. Consistency is ensured by requiring a ReAct agent to succeed in ≥2 of 5 runs.

3. **Hierarchical Environment Taxonomy.** 2,000+ environment themes are organized into a 20 first-tier / 50 second-tier / 2,000+ third-tier taxonomy via hierarchical clustering plus LLM labeling and human-verified merging. This enables stratified sampling of the diagnostic arena.

4. **Self-Evolving Agent Arena.** An auto-diagnosis agent (with Python interpreter + search) inspects failure tool logs, error distributions, and environment metadata to rank "weak environments" and emit task-generation guidelines characterizing missing capabilities. The task synthesis pipeline is re-run targeted at those weaknesses, yielding a closed co-evolution loop of agent policies and training environments.

5. **Multi-Environment Agent RL with GRPO.** Policy updates use Group Relative Policy Optimization over structured verifiable rewards -- LLM-as-judge rubrics for graph-based tasks and executable validator scripts for programmatic tasks -- across a sandboxed "agent--tool--database" rollout loop that tracks genuine state transitions.

---

## Key Findings

### Performance across core agentic tool-use benchmarks (%)

| Model | τ²-Bench | BFCL V4 | MCP-Mark |
|-------|---------:|--------:|---------:|
| GPT-5.2 High (proprietary) | -- | -- | 53.1 |
| Gemini-3 Pro (proprietary) | -- | -- | 50.8 |
| GPT-OSS-120B | -- | -- | 4.7 |
| Qwen3-235B-A22B | -- | -- | 5.8 |
| DeepSeek-V3.2-685B | -- | 54.1 | -- |
| EnvScaler-8B | -- | -- | -- |
| **Agent-World-8B** | **61.8** | **51.4** | **8.9** |
| **Agent-World-14B** | -- | **55.8** | -- |

### Self-evolving arena (2 rounds) on Agent-World-14B (%)

| Suite | Round 0 | Round 2 |
|-------|--------:|--------:|
| τ²-Bench | 60.2 | **65.4** |
| BFCL V4 | 52.4 | **55.8** |
| MCP-Mark | 29.5 | **38.1** |

### EnvScaler-8B with the self-evolving loop (%)

| Suite | Round 0 | Round 2 |
|-------|--------:|--------:|
| τ²-Bench | 37.9 | **41.6** |
| BFCL V4 | 47.6 | **50.0** |
| MCP-Mark | 9.5 | **15.1** |

### Other findings

- **Environment scaling is additive**: going from 0 → 1,978 training environments more than doubles the average score (18.4% → 38.5%, +20.1 pts), with the largest jumps in the 10→100 and 100→500 ranges and diminishing but positive returns beyond 500.
- **Generalization preserved**: Agent-World-8B maintains or improves on seven general reasoning benchmarks (MATH500, GSM8K, MATH, etc.) and gains substantially on agentic search/coding (WebWalkerQA, SWE-bench Verified, Terminal-Bench 1.0/2.0, GAIA, HLE).
- **Robust on MCP and knowledge benchmarks**: Agent-World-8B outperforms baselines on five MCP-Universe sub-domains (Browser Automation, Web Searching, …) and on MMLU, SuperGPQA.
- **Stable RL dynamics**: reward curves rise monotonically for both 8B and 14B backbones; entropy remains stable, indicating continued exploration rather than mode collapse.
- **Largest gains where state tracking matters most**: the biggest self-evolving jumps are on MCP-Mark, the benchmark with the deepest stateful interactions.

---

## Suggestions & Future Directions

1. **Scale environment ecosystem further.** Diminishing returns beyond 500 environments suggest the next frontier is not raw count but targeted diversity -- e.g., deeper state-transition complexity and long-tail domain coverage.
2. **More rounds of self-evolution.** Two-round results monotonically improve but shrink over iterations; exploring annealing schedules, curriculum pacing, or harder failure-mining heuristics could extend gains.
3. **Stronger diagnosis signal.** The auto-diagnosis agent currently uses tool logs, error distributions, and environment metadata; richer signals (e.g., counterfactual rollouts, latent-space clustering of failures) could yield more precise capability-gap localization.
4. **Broader task primitives.** Graph-based and programmatic synthesis cover sequential and non-linear reasoning but may under-represent interactive-user dialog, long-horizon memory, or multi-agent coordination.
5. **Transfer to other model families.** Experiments focus on Qwen3-8B/14B backbones; validating on other base models (Llama, Mistral, DeepSeek) would confirm generality of the co-evolution paradigm.
6. **Safety and contamination.** Autonomously mined environments may reflect real-world biases or leakage with downstream evaluation sets; principled filtering and contamination audits are acknowledged as open work.

---

## Authors & Institutions

**Renmin University of China, Gaoling School of Artificial Intelligence:** Guanting Dong*, Xiaoshuai Song, Xiaoxi Li, Jiajie Jin, Yutao Zhu, Ji-Rong Wen, Zhicheng Dou*.
**ByteDance Seed:** Junting Lu, Junjie Huang, Wanjun Zhong*, Longxiang Liu, Shijue Huang, Zhenyu Li, Yang Zhao, Hanbin Wang, Fangyu Lei, Qinyu Luo, Mingyang Chen, Zehui Chen, Jiazhan Feng.

(* corresponding authors; several RUC authors contributed during internships at ByteDance Seed.)
