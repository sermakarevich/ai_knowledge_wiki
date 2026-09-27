# QUEST: Training Frontier Deep Research Agents with Fully Synthetic Tasks

**Paper:** [QUEST: Training Frontier Deep Research Agents with Fully Synthetic Tasks (Jian Xie et al., 2026)](https://arxiv.org/abs/2605.24218)

## Human Readable TL;DR

Imagine hiring a research assistant who can search the internet, read dozens of sources, and write a well-cited report -- but instead of training that assistant on expensive human-labeled work, you create 8,000 practice tasks entirely by computer. QUEST does exactly this for AI: it trains a family of AI models to do deep internet research by practicing on machine-made tasks, and the resulting AI beats or matches the best commercial research tools, all with its code and weights shared publicly.

## TL;DR

QUEST is a family of open-weight deep research agent models (2B--35B parameters) trained using a fully synthetic data pipeline built around "rubric trees" -- hierarchical, verifiable evaluation criteria that work for both factual and open-ended tasks. With only 8,063 synthesized training tasks and a three-stage training recipe (mid-training + SFT + RL), Quest-35B approaches or surpasses frontier closed-source agents (including OpenAI DeepResearch) across eight deep research benchmarks.

---

## Problem & Motivation

Existing deep research agents are either proprietary black boxes (OpenAI DeepResearch, Gemini Deep Research) or open-weight models lacking the training infrastructure to match them. The core bottleneck is data: long-horizon research tasks require expensive human annotation, and reward signals are hard to define for open-ended outputs like synthesis reports. QUEST addresses this by replacing human annotation with a fully automated rubric-tree-based synthesis pipeline, enabling high-quality training at scale without human labelers.

---

## Main Original Ideas

1. **Rubric-Tree-Based Synthesis Pipeline** -- A unified framework that generates training tasks AND their evaluation criteria simultaneously. Rubric trees decompose task requirements into hierarchical nodes: leaf nodes are verifiable facts (binary scored) for objective tasks; for open-ended synthesis tasks, fixed top-level dimensions (instruction following, comprehensiveness, readability, insight) branch into task-specific sub-criteria. Seeds come from Google Trends for topical relevance; Claude Sonnet 4.5 generates tasks and refines rubrics; Python evaluation scripts automate scoring. 17,000 initial objective tasks filtered to 5,934 after quality checks.

2. **Context Condenser** -- A structured context management module that compresses long interaction histories into a JSON state with three entry categories: *trusted* (verified facts with source URLs), *untrusted* (contradicted claims with reasoning flags), and *uncertain* (partially supported, requiring follow-up). This enables coherent research across trajectories far exceeding native context window limits, and supports unbounded extrapolation at inference time.

3. **Three-Stage Training Recipe** -- Sequential combination of: (a) mid-training on 1M+ auxiliary instances for context summarization and information extraction; (b) session-level SFT on 8,063 synthetic trajectories decomposed between context-condensation events; (c) GRPO-style RL with a combined reward R = 0.75·s_rubric + 0.25·min(s_fact, s_rubric), where s_fact rewards citation verifiability.

4. **Fully Asynchronous RL Infrastructure** -- Decoupled rollout, evaluation, and training with dual caching (FAISS-based semantic similarity for search; URL-based for visits). Evaluation averages 4 minutes per task (up to 30 minutes), so async pooling with timeout control is critical to prevent pipeline stalls.

---

## Key Findings

### Main benchmark results (Quest-35B)

| Benchmark | Quest-35B | OpenAI DeepResearch | Delta |
|-----------|-----------|----------------------|-------|
| BrowseComp | **64.6%** | 51.5% | +13.1pp |
| BrowseComp-Plus | **69.5%** | -- | -- |
| GAIA | **80.8%** | 76.4% (GPT-5) | +4.4pp |
| DeepResearch Bench | **48.2%** | 47.0% | +1.2pp |
| Mind2Web 2 | 30.7% | 28.0% | +2.7pp |
| WideSearch | **60.6%** | -- | -- |
| HLE-Text | 37.2% | -- | competitive |
| LiveResearchBench | 68.2% | -- | competitive |

### Ablation (Quest-35B training stages)

- Vanilla baseline (Qwen3.5-35B-A3B): weakest across all benchmarks
- SFT only: improves fact-seeking, degrades open-ended synthesis
- MT+SFT: consistent improvements
- MT+SFT+RL: best overall; slight sacrifice on expert-reasoning tasks (HLE, GAIA)

### Scaling

- Quest-2B-SFT: competitive on fact-seeking (HLE: 30.3%, GAIA: 72.8%)
- Quest-4B-SFT: 24.4% Mind2Web 2, 36.4% DeepResearch Bench
- Performance gap widens on report synthesis tasks at smaller scales

### Documented failures (negative results)

- Search result prediction in MT caused redundancy with context summarization
- Rubric-based error identification yielded marginal gains without external evidence
- DPO suffered from pairwise comparison ambiguity in long-form outputs
- Pointwise scoring inflated scores; pairwise win/tie/lose collapsed signals

---

## Suggestions & Future Directions

1. Improve open-ended synthesis quality in small models (2B--9B), where capacity limits show most clearly.
2. Extend rubric-tree framework to multimodal research tasks (tables, charts, images).
3. Investigate online rubric refinement where the model's own failures improve rubric coverage.
4. Explore specialization for privacy-sensitive deployments using smaller locally-run models.
5. Study the interaction between RL and expert-reasoning degradation (HLE/GAIA regression with RL stage).

---

## Authors & Institutions

Jian Xie, Tianhe Lin, Zilu Wang, Yuting Ning, Yuekun Yao, Tianci Xue, Zhehao Zhang, Zhongyang Li, Kai Zhang, Yufan Wu, Shijie Chen, Boyu Gou, Mingzhe Han, Yifei Wang, Vint Lee, Xinpeng Wei, Xiangjun Wang, Yu Su, Huan Sun -- The Ohio State University and collaborating institutions.
