# When to Retrieve During Reasoning: Adaptive Retrieval for Large Reasoning Models

**Paper:** [When to Retrieve During Reasoning: Adaptive Retrieval for Large Reasoning Models (Dongxin Guo, Jikun Wu, Siu Ming Yiu, 2026)](https://arxiv.org/abs/2604.26649)

## Human Readable TL;DR

Imagine a detective solving a case -- they don't run to the evidence room after every single thought, nor do they commit to a conclusion without checking crucial facts. Current AI systems that look things up while reasoning are either too eager (checking constantly) or too lazy (checking only once). This paper teaches AI to be more like that smart detective: it senses when it's genuinely confused mid-thought and only then goes to look something up, cutting unnecessary lookups nearly in half while actually getting more answers right.

## TL;DR

ReaLM-Retrieve introduces an adaptive retrieval framework for large reasoning models that decides *when* to retrieve external knowledge during a multi-step reasoning chain. The system uses a step-level uncertainty detector, a REINFORCE-trained retrieval intervention policy, and an efficiency-optimized integration mechanism. Across three benchmarks it achieves 10.1% absolute improvement in answer F1 over standard RAG while reducing retrieval calls by ~50%.

---

## Problem & Motivation

Standard RAG retrieves once at query time and hands context to the model. Large reasoning models (o1, DeepSeek-R1) generate long chains of intermediate reasoning steps -- meaning a single upfront retrieval often misses knowledge needed mid-chain, while retrieving at every step is prohibitively expensive. The gap is the lack of a principled policy for *when* retrieval maximally benefits ongoing reasoning. Existing adaptive-RAG approaches operate at token or sentence granularity, which is too fine-grained for reasoning-step-length reasoning traces and can't model the sequential decision structure of multi-hop inference.

---

## Main Original Ideas

1. **Step-level uncertainty detector** -- Instead of monitoring token-level confidence, the system tracks uncertainty at reasoning-step granularity. It identifies knowledge gaps at the moment a reasoning step is about to commit to a claim it cannot reliably support, triggering retrieval only then.

2. **Retrieval intervention policy (REINFORCE)** -- A policy network is trained with RL (REINFORCE) to learn binary retrieve/continue decisions at each step. The reward integrates answer correctness, retrieval-count penalty, and reasoning efficiency, so the policy learns cost-aware behavior rather than just accuracy maximization.

3. **Efficiency-optimized integration mechanism** -- A 3.2x reduction in per-retrieval overhead is achieved by restructuring how retrieved context is injected into the ongoing reasoning trace, avoiding full-context reprocessing on each retrieval event.

4. **Retrieval-reasoning co-training** -- The whole pipeline (reasoning model + retrieval policy + uncertainty detector) is trained jointly on multi-hop QA, allowing the reasoning model to develop "retrieval-aware" reasoning habits.

---

## Key Findings

| Metric | Standard RAG | ReaLM-Retrieve | Delta |
|---|---|---|---|
| Answer F1 (avg, 3 benchmarks) | baseline | +10.1 pp | **+10.1%** |
| Retrieval calls | 1.0x | ~0.5x | **-50%** |
| Per-retrieval overhead | 1.0x | ~0.31x | **-3.2x** |

- Gains are consistent across HotpotQA and MuSiQue (2-4 hop reasoning chains).
- The uncertainty detector is the primary driver of retrieval reduction; the RL policy adds the accuracy gains on top.
- Cost-aware variants allow trading answer quality for efficiency, useful when inference budget is constrained.
- Evaluated with ColBERT and DPR retrievers; results hold across both.

---

## Suggestions & Future Directions

1. Extend adaptive retrieval to additional reasoning architectures beyond o1-class and DeepSeek-R1 families.
2. Enable real-time adaptation where retrieval policy adjusts dynamically to inference-time compute constraints (latency SLOs).
3. Apply to long-context reasoning scenarios where retrieval competes with in-context memory.
4. Improve cross-domain generalization -- current learned policies may overfit to multi-hop QA distributions.
5. Analyze failure modes where the adaptive policy incorrectly skips retrieval on needed steps.

---

## Authors & Institutions

Dongxin Guo, Jikun Wu, Siu Ming Yiu

**Venue:** SIGIR 2026 (49th International ACM SIGIR Conference) -- DOI: 10.1145/3805712.3809722
