# GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning

**Paper:** [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning (Singhvi, Opsahl-Ong, Zhang et al., 2025)](https://arxiv.org/abs/2507.19457)

## Human Readable TL;DR

Imagine you're teaching someone a new job. Traditional AI training is like giving them a score after each attempt ("7 out of 10") without explaining what went wrong -- they'd need thousands of tries to improve. GEPA instead works like a good mentor: it watches the AI's work, writes down what went well and what didn't in plain language, then rewrites the instructions to be clearer next time. This "learn from written feedback" approach gets better results with up to 35 times fewer practice attempts, saving enormous amounts of time and money.

## TL;DR

GEPA (Genetic-Pareto) is a prompt optimizer for compound AI systems that uses natural language reflection on execution traces combined with Pareto-based evolutionary search. It outperforms both GRPO (a leading RL method) by +10% on average with up to 35x fewer rollouts, and MIPROv2 (a leading prompt optimizer) across all benchmarks, while generating prompts up to 9.2x shorter. The key insight is that rich textual feedback from system traces provides a far stronger learning signal than sparse scalar rewards.

---

## Problem & Motivation

Reinforcement learning with verifiable rewards (RLVR) methods like GRPO are the standard approach for adapting LLMs to downstream tasks, but they suffer from severe sample inefficiency -- requiring tens to hundreds of thousands of expensive rollouts. This makes them impractical for resource-constrained settings or proprietary LLMs whose weights cannot be fine-tuned. The authors observe that LLMs produce highly interpretable natural language traces during execution (reasoning chains, tool calls, error messages) that contain far richer diagnostic information than scalar reward signals. GEPA exploits this insight to achieve superior performance with dramatically fewer samples.

---

## Main Original Ideas

1. **Reflective Prompt Mutation** -- Instead of learning from scalar rewards, GEPA uses an LLM to reflect on full execution traces (reasoning, tool calls, outputs, errors) and propose targeted prompt refinements. This implicit credit assignment through natural language yields much denser learning signals than traditional RL.

2. **Pareto-Based Candidate Selection** -- Rather than greedily following the single best prompt candidate, GEPA maintains a diverse frontier of non-dominated candidates (each excelling on different task instances). Stochastic sampling from this frontier prevents local optima and improves generalization.

3. **Feedback Functions** -- A specialized mechanism that extracts diagnostic textual traces from the evaluation process (e.g., compiler errors, module-specific feedback) and injects them into the reflection loop, significantly boosting the LLM's ability to propose targeted improvements.

4. **System-Aware Merge (Crossover)** -- A genetic crossover strategy that identifies complementary optimization lineages (e.g., one that improved Module A, another that improved Module B) and combines them into a single superior candidate system.

5. **Instruction-Only Optimization Surpassing Joint Optimization** -- GEPA demonstrates that reflectively evolved instructions alone outperform methods that jointly optimize instructions and few-shot examples, suggesting modern LLMs' instruction-following capabilities have matured enough to make few-shot demos less critical.

---

## Key Findings

### Performance vs. Baselines (Qwen3 8B and GPT-4.1 Mini)

| Method | Avg. Gain over Baseline | Rollouts Used | Prompt Length |
|--------|------------------------|---------------|---------------|
| **GEPA+Merge** | **+14.29%** (GPT-4.1 Mini) | 678--3,200 | Up to **9.2x shorter** than MIPROv2 |
| **GEPA** | **+12.44%** (Qwen3 8B) | 678--3,200 | Compact instructions |
| MIPROv2 | +7.04% (avg) | Similar budget | Long (includes few-shot examples) |
| GRPO | Lower than GEPA by ~10% | 24,000 (fixed) | N/A (weight-based) |

### Key Quantitative Results

- On HotpotQA, GEPA outperformed GRPO by **+19%** (Qwen3 8B), with GEPA+Merge achieving **+21%**
- On IFBench, GEPA used **35x fewer rollouts** (678 vs. 24,000) while outperforming GRPO
- GEPA matched GRPO's best validation scores with as few as **6 training rollouts** (HoVer) and **32 rollouts** (IFBench) -- up to **78x greater sample efficiency**
- GEPA showed a lower generalization gap (validation-to-test performance difference) than MIPROv2

### Ablation Insights

- Pareto-based selection maintained a **+6.4% aggregate margin** over naive best-candidate selection
- The naive approach frequently got stuck in local optima; Pareto sampling enabled diverse exploration
- GEPA+Merge showed up to +5% additional gains over GEPA on GPT-4.1 Mini but was less consistent on Qwen3 8B

### Inference-Time Search (Code Optimization)

- NPU kernel optimization: GEPA boosted GPT-4o's vector utilization from **4.25% to 30.52%**, surpassing RAG+MIPROv2 (19.03%)
- CUDA kernel optimization: GEPA iteratively refined code to achieve >20% `fast_p` score on KernelBench

---

## Suggestions & Future Directions

1. **Hybrid optimization** -- Integrating GEPA's language-based prompt insights with weight-space adaptation (e.g., distilling reflectively evolved instructions into fine-tuned weights) could combine the best of both paradigms.

2. **Feedback engineering** -- Designing optimal feedback functions that extract maximally diagnostic textual signals from system traces is a promising research direction for further boosting sample efficiency.

3. **Scaling to larger compound systems** -- Extending GEPA to optimize systems with many more modules and complex inter-module dependencies.

4. **Crossover timing and budget allocation** -- The GEPA+Merge variant showed sensitivity to the underlying LLM; further research into when and how to apply crossover operations could improve robustness.

5. **Broader inference-time applications** -- Expanding GEPA's use as an inference-time search strategy beyond code optimization to other domains requiring iterative refinement from detailed feedback (e.g., scientific discovery, hardware design).

6. **Limitations acknowledged** -- GEPA's effectiveness depends on the quality of the reflecting LLM and the informativeness of available textual feedback; tasks with opaque evaluation signals may benefit less.

---

## Authors & Institutions

Arnav Singhvi (Stanford), Krista Opsahl-Ong (Databricks), Shangyin Tan (UC Berkeley), Jiatong Yu (UC Berkeley), Michael Ryan (UC Berkeley), Peter Hartog (BespokeLabs.ai), Silas Alberti (Stanford), Jasper Xian (UC Berkeley), Caleb Winston (Stanford), Keshav Ramji (UC Berkeley), Karl Stratos (UC Berkeley), Alexandros G. Dimakis (BespokeLabs.ai), Meng Jiang (Notre Dame), Matei Zaharia (UC Berkeley / Databricks), Christopher Potts (Stanford), Christopher Re (Stanford), Omar Khattab (MIT)
