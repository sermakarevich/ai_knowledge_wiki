# Scaling Coding Agents via Atomic Skills

**Paper:** [Scaling Coding Agents via Atomic Skills (Ma et al., 2025)](https://arxiv.org/abs/2604.05013)

## Human Readable TL;DR

Instead of teaching an AI coding assistant to do complex jobs like "fix this bug" all at once, this paper breaks coding down into five basic skills -- like finding the right file, editing code, writing tests, reproducing bugs, and reviewing code. Think of it like teaching someone to cook by first mastering chopping, sauteing, and seasoning individually, rather than jumping straight to a full recipe. They then train the AI on all five skills simultaneously using reinforcement learning, and find that mastering these basics makes the AI better at complex tasks it was never explicitly trained on -- a 18.7% improvement across the board.

## TL;DR

This paper proposes training coding agents on five formally defined atomic skills (code localization, code editing, unit-test generation, issue reproduction, code review) via joint reinforcement learning with GRPO, rather than optimizing directly on composite benchmarks. Using GLM-4.5-Air-Base (106B params, 12B active) with execution-grounded rewards in sandboxed environments, joint RL improves atomic skill performance by 18.7% on average and generalizes to unseen composite tasks like SWE-bench Verified (+15.4%), SWE-bench Multilingual (+29.7%), and SEC-Bench (+24.3%).

---

## Problem & Motivation

Current LLM coding agents are trained on composite benchmarks (e.g., SWE-bench for bug fixing), which leads to task-specific overfitting and limited generalization. Directly scaling RL on composite tasks is "practically intractable" given the diversity of real-world software engineering. The paper argues that complex SE tasks can be decomposed into a small set of fundamental, composable atomic skills -- and that training on these skills jointly produces better generalization than training on composite tasks directly.

---

## Main Original Ideas

1. **Atomic Skill Formalization** -- Five fundamental skills are formally defined with explicit input/output specifications and execution-grounded reward functions: code localization, code editing, unit-test generation, issue reproduction, and code review. These serve as "basis vectors" for complex SE tasks.

2. **Joint RL over Atomic Skills** -- A single shared policy is trained across all five skills simultaneously using Group-based Relative Policy Optimization (GRPO). Group-normalized rewards mitigate scale mismatches across heterogeneous skill types, enabling consistent improvement without negative interference.

3. **Generalization from Atomic to Composite** -- The key finding: improvements on atomic skills transfer to unseen composite tasks (bug-fixing, refactoring, ML engineering, security) without any direct training on those tasks. This motivates a new scaling paradigm where you scale the atoms, not the molecules.

4. **Execution-Grounded Reward Design** -- Each atomic skill has a tailored reward computed inside containerized sandboxes (10,000+ concurrent Kubernetes pods, 25,000+ pre-built Docker images). Unit-test generation uses semantic mutation testing against 16 LLM-generated buggy variants rather than coverage metrics.

5. **Minimal Tool Scaffolding** -- The agent uses only bash commands and str_replace file operations -- no skill-specific heads or specialized tools. This forces the model to internalize skills in its policy weights rather than relying on external tooling.

---

## Key Findings

### Atomic Skills Performance (Avg@3, after 100 RL iterations)

| Skill | GLM-4.5-Air | + SFT | + SFT + RL | Improvement (RL vs SFT) |
|-------|-------------|-------|------------|-------------------------|
| Code Localization | 0.666 | 0.665 | **0.712** | +7.1% |
| Code Editing | 0.556 | 0.458 | **0.611** | **+33.4%** |
| Issue Reproduction | 0.555 | 0.542 | **0.605** | +11.6% |
| Unit-Test Generation | 0.423 | 0.359 | **0.472** | **+31.5%** |
| Code Review | 0.536 | 0.563 | **0.622** | +10.5% |

### Out-of-Distribution Composite Tasks (Avg@3)

| Benchmark | GLM-4.5-Air | + SFT | + SFT + RL | Improvement (RL vs SFT) |
|-----------|-------------|-------|------------|-------------------------|
| SWE-bench Verified | 0.559 | 0.507 | **0.585** | +15.4% |
| SWE-bench Multilingual | 0.358 | 0.300 | **0.389** | **+29.7%** |
| Terminal-Bench 2.0 | 0.187 | 0.151 | **0.182** | +20.5% |
| Code Refactoring | 0.159 | 0.146 | **0.171** | +17.1% |
| SEC-Bench | 0.163 | 0.136 | **0.169** | **+24.3%** |

- Joint RL consistently improves all skills without negative interference or trade-offs
- Editing-only RL and Verified-only RL both produce weaker cross-capability improvements, confirming the value of joint training
- SFT alone actually hurts some skills (e.g., editing drops from 0.556 to 0.458), while RL recovers and surpasses the base model
- Improvements compound monotonically across RL iterations (tracked at iter-20, 50, 70, 100)

---

## Suggestions & Future Directions

1. **Expanding the atomic skill library** -- The current five skills are a starting point; additional fundamental skills (e.g., architecture design, documentation, dependency management) could further improve generalization.

2. **Verification bottleneck** -- Defining dense reward functions for new domains remains intractable; future work needs scalable reward engineering or learned reward models.

3. **Model scale dependency** -- Smaller models struggle with the instruction-following required for effective RL exploration; the approach may require a minimum model capacity threshold.

4. **Extending to additional SE workflows** -- The framework could be applied beyond coding to broader software engineering processes like CI/CD, deployment, and project management.

---

## Authors & Institutions

Yingwei Ma (HKUST), Yue Liu (NUS), Xinlong Yang (Peking University), Yanhao Li (Peking University), Kelin Fu (Peking University), Yibo Miao (SJTU), Yuchong Xie (HKUST), Zhexu Wang (BUPT), Shing-Chi Cheung (HKUST)
