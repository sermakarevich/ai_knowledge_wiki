# Rethinking Memory as Continuously Evolving Connectivity

**Paper:** [Rethinking Memory as Continuously Evolving Connectivity (Fang et al., 2026)](https://arxiv.org/pdf/2605.28773)

## Human Readable TL;DR

Imagine an AI assistant that can remember things the same way humans do -- not just filing away facts, but actively reorganizing what it knows based on what worked or failed in the past. Current AI agents store memories in rigid, fixed structures, like a filing cabinet that never gets reorganized. This paper introduces FluxMem, which gives AI agents a living memory network that grows, trims, and restructures itself as the agent uses it -- similar to how the human brain strengthens useful connections and drops irrelevant ones. The result is an AI that gets meaningfully better at complex tasks as it accumulates experience, outperforming all prior memory systems across three very different challenge domains.

## TL;DR

FluxMem proposes modeling LLM agent memory as a dynamically editable heterogeneous graph spanning semantic knowledge, episodic experiences, and procedural skills. Memory evolves through a three-stage pipeline: (1) initial cross-layer link formation via hybrid retrieval, (2) feedback-driven refinement that repairs under-connected and over-connected subgraphs in real time, and (3) offline long-term consolidation that clusters successful trajectories into reusable procedural circuits monitored by a Procedure Evolution Maturity Score (PEMS). FluxMem achieves state-of-the-art results across long-context reasoning (LoCoMo 95.06%), real-world web navigation (Mind2Web 8.1% cross-task SR), and generalist assistant tasks (GAIA 64.85%).

---

## Problem & Motivation

Existing memory-augmented LLM agents treat memory as a static repository with predefined representations and fixed retrieval pipelines. This causes two concrete failure modes in dynamic agentic environments:

1. **Inaccurate Memory Connectivity** -- Static pipelines cannot adapt connections based on feedback, causing *under-connection* (missing critical context) and *over-connection* (retrieving irrelevant associations that hallucinate guidance).
2. **Inflexible Memory Unit Content** -- Memory units are stored at a fixed abstraction level. When granularity is mismatched (too coarse or too fine for the current task), agents cannot adaptively integrate new experiences.
3. **No Memory Consolidation** -- Memories are treated as isolated instances rather than progressively consolidated, so agents repeatedly reconstruct similar associations instead of internalizing durable structural patterns.

---

## Main Original Ideas

1. **Heterogeneous Three-Layer Memory Graph** -- Memory is represented as a graph G = (V, E) with three node layers: *Semantic Knowledge* (V_sem, static facts), *Episodic Experiences* (V_epi, step-by-step task trajectories), and *Procedural Skills* (V_proc, distilled reasoning heuristics). Episodic nodes act as the operational nexus linking the other two layers via grounding edges (V_sem → V_epi) and distillation edges (V_epi → V_proc).

2. **Context as Dynamically Induced Connectivity** -- At each step, the agent's working context is defined by activating a task-specific subgraph G_t(q) ⊂ G. Optimizing the agent's context is reframed as performing targeted topological edits on this local subgraph, not retrieval from a flat list.

3. **Stage I -- Initial Connection Formation (Online)** -- Rapidly seeds the subgraph using a hybrid relevance score combining dense embedding similarity, BM25 sparse lexical matching, and LLM-based verification to populate the initial semantic, episodic, and procedural node sets.

4. **Stage II -- Feedback-Driven Connectivity Refinement (Online)** -- A closed-loop mechanism that diagnoses execution failures as either connection-level (under/over-connection) or unit-level (granularity mismatch) problems and applies targeted edits: *Link Expansion*, *Link Pruning*, or *Content Reshaping* of individual memory nodes until execution succeeds or T refinement rounds are exhausted.

5. **Stage III -- Long-Term Connection Consolidation (Offline)** -- Episodic nodes are clustered by semantic trajectory similarity; an LLM extracts shared reasoning patterns per cluster to induce new procedural skill nodes. Skills are iteratively refined via a test-score-rewrite loop until the PEMS convergence threshold ε is met.

6. **Procedure Evolution Maturity Score (PEMS)** -- A single convergence metric combining skill success rate (η), skill conciseness (log ℓ), and embedding drift from the prior version (δ). PEMS drives the offline refinement loop and provides an automatic stopping criterion.

---

## Key Findings

| Benchmark | Metric | FluxMem | Best Prior Baseline | Improvement |
|-----------|--------|---------|---------------------|-------------|
| LoCoMo (GPT-4.1-mini) | Avg LMJ | **95.06%** | EverMemOS 93.05% | +2.01% |
| LoCoMo (Qwen3-30B) | Avg LMJ | **93.44%** | Full Context 74.87% | +18.57% |
| Mind2Web Cross-Task (GPT-4.1-mini, realistic) | SR | **8.1%** | AWM 3.6% | +4.5% |
| Mind2Web Cross-Task (Gemini-2.5-flash, realistic) | SR | **9.6%** | AWM 5.6% | +4.0% |
| GAIA (Kimi K2) | Avg SR | **64.85%** | Flash-Searcher 52.12% | +12.73% |
| GAIA Level 3 (GPT-5-mini) | SR | **53.85%** | MemEvolve 53.85% | tied SOTA |

**Ablation insights:**
- On LoCoMo (fact retrieval tasks): Stage II (feedback refinement) is the most critical component. Removing it drops GPT-4.1-mini from 95.06% to 85.32%.
- On Mind2Web (multi-step reasoning tasks): Stage III (long-term consolidation) dominates. Removing it drops success rate from 8.1% to 3.2%.
- Stage II refinement rounds scale monotonically: T=0 yields 85.32%, T=5 yields 95.06%, with diminishing returns at T=4→5 (+0.54%).
- PEMS converges reliably: from 0.072 at round 0 to 0.159 at round 5 on LoCoMo, providing a clean automatic stopping signal.

---

## Suggestions & Future Directions

1. **Measure computational overhead** -- Iterative LLM calls in Stages II and III add latency and token cost that the current evaluation does not systematically quantify; future work should profile real-time and cost constraints.
2. **Open-world/streaming evaluation** -- Static benchmarks (LoCoMo, Mind2Web, GAIA) do not capture continuous distribution shifts or memory decay in streaming environments; more realistic lifelong evaluation protocols are needed.
3. **Hyperparameter robustness analysis** -- The framework introduces several control thresholds (T, ε, top-k). A systematic sensitivity analysis across model backbones and heterogeneous domains is a clear next step.
4. **Dynamic consolidation scheduling** -- Stage III currently runs offline in periodic batches; future work should explore adaptive scheduling strategies and quantify the trade-off between consolidation frequency and online performance.
5. **Open-source release** -- The code will be open-sourced at https://github.com/zjunlp/LightMem.

---

## Authors & Institutions

Jizhan Fang (Zhejiang University, Alibaba Group), Buqiang Xu (Zhejiang University), Zhixian Wang (Zhejiang University), Haoliang Cao (Alibaba Group), Xinle Deng (Zhejiang University), Baohua Dong (Alibaba Group), Hangcheng Zhu (Alibaba Group), Ruohui Huang (Alibaba Group), Gang Yu (Alibaba Group), Ying Wei (Zhejiang University), Guozhou Zheng (Zhejiang University), Feiyu Xiong (MemTensor), Haofen Wang (Tongji University), Huajun Chen (Zhejiang University), Ningyu Zhang* (Zhejiang University, corresponding author)
