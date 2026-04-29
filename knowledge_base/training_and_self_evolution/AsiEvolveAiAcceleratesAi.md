# ASI-Evolve: AI Accelerates AI

**Paper:** [ASI-Evolve: AI Accelerates AI (Xu et al., 2026)](https://arxiv.org/abs/2603.29640)

## Human Readable TL;DR

Imagine a self-improving factory where the robots not only build cars but also redesign their own assembly line, retrain themselves, and improve their own raw materials -- all automatically. ASI-Evolve is a software system that does exactly this for AI research: it autonomously designs better AI model structures, figures out which training data is highest quality, and invents improved training algorithms. Instead of waiting for human researchers to try thousands of experiments, the system runs them itself, learns from each one, and keeps getting better. It even absorbed lessons from 100+ academic papers before starting, the way a new PhD student reads existing literature before beginning their own research.

## TL;DR

ASI-Evolve is a closed-loop agentic framework that autonomously accelerates AI development across three foundational pillars: neural architecture design, pretraining data curation, and RL algorithm design. It augments evolutionary search with a **Cognition Store** (human prior knowledge encoded from literature) and an **Analyzer** (distills multi-dimensional experimental feedback into actionable insights). Across all three domains, ASI-Evolve discovers improvements that outperform strong human-designed baselines -- achieving +0.97 over DeltaNet in architecture (3x better than recent SOTA), +3.96 points in data curation over raw data, and +12.5 points on AMC32 in RL algorithm design.

---

## Problem & Motivation

Traditional AI research relies on human researchers to form hypotheses, run experiments, and accumulate insights -- a process bottlenecked by limited parallelism, demanding experimental workflows, and inefficient knowledge transfer across iterations. Existing AI-for-science systems either operate on small-scale tasks with simple feedback (e.g., FunSearch, AlphaEvolve) or address bounded, single-pillar objectives (e.g., MLE-bench, AI Scientist). No unified framework tackles all three foundational AI development components simultaneously while handling high execution cost, vast search spaces, and complex multi-dimensional feedback.

---

## Main Original Ideas

1. **L_task Framework** -- A taxonomy characterizing scientific research tasks along three axes: Execution Cost (C_exec), Search Space Complexity (S_space), and Feedback Complexity (D_feedback). ASI-Evolve is the first system positioned at the high end of all three simultaneously.

2. **Cognition Store** -- A retrieval-augmented knowledge base populated from domain literature (e.g., 150 entries from 100 papers on linear attention and SSMs). Each round, semantically similar entries are retrieved and injected into the Researcher's context, dramatically accelerating cold-start exploration and encoding human priors.

3. **Dedicated Analyzer Module** -- Rather than feeding raw logs to the next iteration, a specialized LLM-based Analyzer distills verbose experimental outputs (training curves, benchmark scores, efficiency traces) into compact, decision-oriented reports stored in the database. This prevents context overflow and enables sustained directed improvement.

4. **Closed Learn-Design-Experiment-Analyze Cycle** -- Five-stage pipeline per round: sample past nodes from a Database (via UCB1/MAP-Elites/random), retrieve cognition, generate a candidate program (Researcher), execute with early rejection and budget constraints (Engineer), and analyze results (Analyzer).

5. **Evolution of Cognition Paradigm** -- Unlike pure evolutionary search (which searches program space), ASI-Evolve evolves the reasoning process itself -- accumulated insights from runs are stored back as new cognition entries, making the system progressively smarter about where to search.

---

## Key Findings

### Architecture Design (Linear Attention)

| Model | Dev Benchmarks (avg) | OOD Benchmarks (avg) |
|---|---|---|
| DeltaNet (baseline) | 55.76% | 44.74% |
| **ASI-Evolve best** | **57.28%** | **45.40%** |
| Gain over DeltaNet | +1.52pp | +0.66pp |

- 1,350 candidate architectures explored across 1,773 rounds; 105 surpassed DeltaNet
- Best architecture gain (+0.97 points overall) is ~3x recent human SOTA improvements (Mamba2: +0.34)
- Top architectures share a theme: adaptive multi-scale routing that dynamically allocates compute based on input content
- 51.7% of all architectures and 44.8% of SOTA-level ones derived from the Cognition Store

### Pretraining Data Curation (Nemotron-CC, 672B tokens)

| Dataset | Avg Benchmark Score | MMLU | CSQA | MedQA |
|---|---|---|---|---|
| Raw Nemotron-CC | 40.17 | -- | -- | -- |
| DCLM | ~43 | -- | -- | -- |
| FineWeb-Edu | ~43 | -- | -- | -- |
| **Nemotron-CC_ASI+** | **44.13** | **+18.64** | **+18.80** | **+13.48** |

- Evolved strategies consistently focused on noise removal, format normalization, and domain-aware preservation -- without explicit guidance to do so

### RL Algorithm Design (post-GRPO variants)

| Benchmark | GRPO | Best ASI-Evolve | Gain |
|---|---|---|---|
| AMC32 | 67.5 | **80.0** | +12.5 |
| AIME24 | 20.00 | **31.67** | +11.67 |
| OlympiadBench | 45.92 | **50.96** | +5.04 |

- 3 algorithms showed statistically significant improvements across all domains
- Key innovations: pairwise asymmetric advantage estimation, Global Update Budget (z_cap) for guaranteed policy update magnitude

### Circle Packing (Benchmark vs Baselines)

| System | Rounds to SOTA (2.636) |
|---|---|
| OpenEvolve | ~460 |
| GEPA | never converged past 2.630 |
| **ASI-Evolve (UCB1 + GPT-4.1-mini)** | **17** |

### Drug-Target Interaction (Generalization)

- +6.94 AUROC for unseen drugs, +3.56 for unseen proteins vs DrugBAN baseline
- Demonstrates that "AI-for-AI" discoveries transfer to biomedical domains

**Ablation insights:**
- Removing Analyzer: early plateau, limited sustained improvement
- Removing Cognition: slower cold-start but eventually recovers -- Cognition accelerates, not enables

---

## Suggestions & Future Directions

1. **Hardware-optimized kernel generation** -- Current architecture search operates at the attention mechanism level, not low-level kernel implementation. Future work should integrate hardware-aware efficiency directly into the fitness signal.

2. **Scaling the framework** -- Larger cognition bases, more powerful LLMs, and higher-compute validation stages could unlock further improvements; the current results are likely a lower bound.

3. **Longer-horizon multi-task co-evolution** -- Jointly evolving architecture, data, and algorithm in a coupled loop (rather than independently) could yield synergistic gains.

4. **Broader scientific domains** -- DTI results suggest generalizability; the authors suggest mathematics and biomedicine as immediate next targets.

5. **Human-AI collaboration model** -- As ASI-Evolve automates implementation and iteration, human researchers can shift from executors to problem definers, focusing on high-level conceptualization and evaluation criteria.

6. **Sample efficiency of Cognition retrieval** -- Better RAG strategies (e.g., structured reasoning over retrieved entries) could further reduce cold-start cost.

---

## Authors & Institutions

Weixian Xu (SJTU, GAIR), Tiantian Mi (Shanghai AI Lab), Yixiu Liu (GAIR), Yang Nan (GAIR), Zhimeng Zhou, Lyumanshan Ye, Lin Zhang (Shanghai AI Lab), Yu Qiao (Shanghai AI Lab), Pengfei Liu (SJTU, GAIR, corresponding author)
