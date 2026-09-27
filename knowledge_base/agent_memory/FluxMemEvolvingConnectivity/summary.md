# Rethinking Memory as Continuously Evolving Connectivity

**Paper:** [Rethinking Memory as Continuously Evolving Connectivity (Fang et al., 2026)](https://arxiv.org/pdf/2605.28773)

## Human Readable TL;DR

Imagine giving an AI assistant a filing cabinet where folders are fixed, labels never change, and there is no way to reorganize based on what you have learned. Most AI agents work that way -- their memory is locked into a rigid structure that cannot adapt as tasks change. FluxMem is like replacing that cabinet with a living notebook that rewrites itself: when the AI makes a mistake, it adds missing notes, crosses out irrelevant ones, and eventually promotes frequently useful patterns into permanent cheat sheets. Over time, the notebook organizes itself into the most useful shape for whatever tasks keep coming up.

## TL;DR

FluxMem is a connectivity-evolving memory framework that models LLM agent memory as a dynamically editable heterogeneous graph spanning semantic, episodic, and procedural layers. It evolves through three stages -- initial connection formation, feedback-driven topology refinement, and offline long-term consolidation guided by a Procedure Evolution Maturity Score (PEMS) -- enabling agents to repair missing links, prune irrelevant associations, and distill recurring successful trajectories into reusable skills. Evaluated on LoCoMo, Mind2Web, and GAIA, FluxMem achieves consistent state-of-the-art performance across long-context reasoning, web navigation, and general assistant tasks.

---

## Problem & Motivation

Existing memory-augmented LLM agents treat memory as a static repository with predefined representations and fixed retrieval pipelines. In dynamic agentic environments, feedback, task variation, and heterogeneous signals continuously reshape what should be remembered and how it should be connected. This static paradigm creates two compounding failures:

1. **Adaptive connectivity failure** -- fixed pipelines cause under-connection (missing critical context) and over-connection (irrelevant noise and hallucinations), and cannot reshape memory unit abstraction granularity to match task demands.
2. **Consolidation failure** -- successful trajectories are stored as isolated instances rather than progressively coalesced into stable associative regions, so agents must reconstruct the same patterns repeatedly instead of internalizing them as durable skills.

---

## Main Original Ideas

1. **Heterogeneous Three-Layer Memory Graph** -- Memory is formalized as G = (V, E) with three functional node layers: Semantic Knowledge (V_sem, static facts), Episodic Experiences (V_epi, state-action trajectories), and Procedural Skills (V_proc, distilled reasoning templates). Two edge types link them: E_ground (facts supporting episodes) and E_distill (skills distilled from episodes).

2. **Context as Dynamically Induced Connectivity** -- Rather than retrieving a flat list of memories, the agent's context at each step is a locally induced subgraph G_t(q). Optimizing the working context is reframed as performing targeted topological edits on this subgraph, unifying retrieval and adaptation into a single graph operation.

3. **Stage I -- Initial Connection Formation (online, step-wise)** -- Uses a hybrid relevance score fusing dense embedding similarity, sparse BM25 lexical matching, and LLM-based verification to retrieve top-k semantic nodes. Episodic nodes are retrieved by embedding cosine similarity; procedural skills are inherited by traversing E_distill edges from retrieved episodes.

4. **Stage II -- Feedback-Driven Connectivity Refinement (online, step-wise)** -- A closed-loop mechanism applies targeted graph edits after receiving execution feedback. Three operations: Link Expansion (add edges to unactivated nodes for under-connection), Link Pruning (sever distractor edges for over-connection), and Node Reshape (adaptively rewrite internal memory unit content when abstraction granularity is misaligned).

5. **Stage III -- Long-Term Connection Consolidation (offline)** -- Clusters episodic nodes by semantic trajectory similarity, induces shared procedural skills per cluster, then iteratively verifies and refines those skills via a closed-loop guided by PEMS (Procedure Evolution Maturity Score). PEMS = η * log(ℓ) * (1 − δ), where η = episode success rate, ℓ = skill token length, δ = embedding shift from prior version. The loop terminates when ΔPEMS < ε, ensuring validated, concise skills.

---

## Key Findings

| Benchmark | Metric | FluxMem | Best Baseline | Improvement |
|-----------|--------|---------|---------------|-------------|
| LoCoMo (GPT-4.1-mini) | Avg LMJ | **95.06%** | EverMemOS 93.05% | +2.01% |
| LoCoMo (Qwen3-30B) | Avg LMJ | **93.44%** | Full Context 74.87% | +18.57% |
| Mind2Web Cross-Task (GPT-4.1-mini, realistic) | SR | **8.1%** | AWM 3.6% | +4.5pp |
| Mind2Web Cross-Task (Gemini-2.5-flash, realistic) | SR | **9.6%** | AWM 5.6% | +4.0pp |
| GAIA (Kimi K2) | Avg SR | **64.85%** | Flash-Searcher 52.12% | +12.73pp |
| GAIA Level 3 (GPT-5-mini) | SR | **53.85%** | MemEvolve 53.85% | on par with best |

**Ablation insights:**
- On LoCoMo (fact recall), Stage II is the dominant component -- removing it drops GPT-4.1-mini from 95.06% to 85.32%.
- On Mind2Web (multi-step navigation), Stage III is the dominant component -- removing it drops Cross-Task SR from 8.1% to 3.2%.
- Stage II refinement shows monotonic improvement as T increases from 0 (85.32%) to 5 (95.06%), with diminishing returns after T=4.
- PEMS converges reliably (0.072 → 0.159 over 5 rounds), demonstrating the maturity metric correctly signals when to stop consolidation.

---

## Suggestions & Future Directions

1. **Measure computational costs** -- Current evaluation ignores latency, API cost, and token consumption from iterative LLM calls in Stages II and III; systematic profiling is needed for real-time and resource-constrained deployments.
2. **Dynamic open-world benchmarks** -- Static pre-collected datasets (LoCoMo, Mind2Web, GAIA) do not capture continuous distribution shifts, streaming environments, or memory decay alongside evolution.
3. **Hyperparameter sensitivity analysis** -- Comprehensive sweeps over refinement rounds T, PEMS threshold ε, and retrieval top-k across heterogeneous domains and model families are needed.
4. **Dynamic consolidation scheduling** -- Stage III currently runs in offline periodic batches; future work should explore online or adaptive scheduling strategies and quantify the consolidation-frequency vs. online-performance trade-off for practical lifelong deployment.

---

## Authors & Institutions

Jizhan Fang (Zhejiang University & Alibaba Group), Buqiang Xu (Zhejiang University), Zhixian Wang (Zhejiang University), Haoliang Cao (Alibaba Group), Xinle Deng (Zhejiang University), Baohua Dong (Alibaba Group), Hangcheng Zhu (Alibaba Group), Ruohui Huang (Alibaba Group), Gang Yu (Alibaba Group), Ying Wei (Zhejiang University), Guozhou Zheng (Zhejiang University), Feiyu Xiong (MemTensor), Haofen Wang (Tongji University), Huajun Chen (Zhejiang University), Ningyu Zhang* (Zhejiang University -- corresponding author)
