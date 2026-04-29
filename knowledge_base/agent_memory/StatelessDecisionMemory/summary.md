# Stateless Decision Memory for Enterprise AI Agents

**Paper:** [Stateless Decision Memory for Enterprise AI Agents (Vasundra Srinivasan, 2026)](https://arxiv.org/abs/2604.20158)

## Human Readable TL;DR

Imagine a court stenographer vs. a journalist. The journalist rewrites their notes after each witness, condensing and interpreting as they go -- but when questioned later, they can't point to the exact transcript. The stenographer records everything verbatim and only writes the summary at the end. This paper argues that for AI systems making high-stakes decisions (like approving a mortgage), you want the stenographer approach: keep a raw log of everything, and generate the summary only when needed. This makes it possible to replay any decision exactly as it happened, prove why a choice was made, and run thousands of decisions at once without them interfering with each other.

## TL;DR

This paper proposes Deterministic Projection Memory (DPM) -- an agent memory architecture that replaces incremental stateful summarization with an append-only event log plus a single task-conditioned LLM projection at decision time. DPM is designed to satisfy four enterprise system properties by construction: deterministic replay, auditable rationale, multi-tenant isolation, and statelessness for horizontal scale. Empirically, DPM matches stateful incremental summarization at moderate/loose memory budgets and substantially outperforms it at tight budgets (FRP +0.515, RCS +0.533, p<0.005) while being 7--15× faster and cheaper.

---

## Problem & Motivation

Enterprise AI deployments in regulated domains (mortgage underwriting, insurance claims, clinical review) overwhelmingly rely on RAG pipelines despite the existence of more sophisticated stateful memory architectures. The paper argues this is not because RAG is better at making decisions -- it's because stateful architectures violate four load-bearing enterprise requirements:

1. **Deterministic Replay** -- reproduce a decision identically from the same input sequence (required for audits, regulators, legal review)
2. **Auditable Rationale** -- trace every reasoning fragment directly back to a source event
3. **Multi-Tenant Isolation** -- guarantee that concurrent decisions for different entities never leak information between them
4. **Stateless Horizontal Scale** -- handle thousands of concurrent decisions without per-request mutable state

Stateful architectures (MemGPT, HyMem, incremental summarization) violate at least one of these by design.

---

## Main Original Ideas

1. **Deterministic Projection Memory (DPM)** -- An append-only event log stores all raw events in arrival order (immutable). At decision time only, a single LLM call at temperature=0 projects the full log + task spec + budget into a structured memory view (facts / reasoning / compliance). Because the projection is a pure function of its explicit inputs, it has no hidden cross-call state.

2. **Single-Call Audit Surface** -- By collapsing all memory processing into one LLM call, the auditable surface shrinks from 83--97 calls (one per event in incremental summarization) to 2 calls per decision. Each rationale fragment cites its source event index directly.

3. **Budget-Conditional Architecture Selection (TAMS)** -- The paper proposes Task-Adaptive Memory Selection: use DPM when enterprise system properties are required *or* when the compression ratio ρ (trajectory length / budget) exceeds ~10×; use incremental summarization otherwise. The crossover emerges naturally from the compounding information-loss problem of chained LLM calls.

4. **Residual Nondeterminism Minimization** -- Even at temperature=0, live LLM APIs are not byte-deterministic. DPM limits nondeterminism exposure to one call; incremental summarization compounds it over N calls. If the backend were deterministic, DPM would achieve byte-exact replay.

---

## Key Findings

Benchmark: LongHorizon-Bench (10 regulated cases -- 5 mortgage, 5 insurance; ~27K chars, 82--96 events per case). Backend: `claude-haiku-4-5-20251001`, temperature=0, seed=20260420.

| Metric | Tight Budget (20× compression) DPM vs Summ | p-value | Cohen's h |
|---|---|---|---|
| Factual Precision (FRP) | **+0.515** | 0.001 | 1.17 |
| Reasoning Coherence (RCS) | **+0.533** | 0.003 | 1.13 |
| Decision Accuracy (EDA) | +0.500 | 0.065 | -- |
| Compliance Reconstruction (CRR) | +0.500 | 0.066 | -- |

- At **moderate and loose budgets**, DPM and Summ-only are statistically indistinguishable across all four axes.
- At **tight budgets**, DPM is **7.4× faster** and substantially cheaper (1 projection call vs. 82--96 summarization calls).
- At **moderate budgets**, DPM is **14.9× faster**.
- DPM's advantage is driven by avoiding compounding information loss from chained LLM summarization steps.
- Determinism experiment: live API at temperature=0 still produces unique SHA-256 hashes across 10 replays on large cases, but DPM's single-call design minimizes the blast radius.

---

## Suggestions & Future Directions

1. **Hierarchical DPM** -- Current architecture has a context-window ceiling for the single projection call; hierarchical or chunked extensions are needed for very long trajectories.
2. **Dedicated deterministic inference backends** -- Full byte-exact replay requires deterministic APIs, which current cloud providers do not guarantee; purpose-built serving infrastructure is a next step.
3. **Re-derive TAMS thresholds for other regimes** -- The ρ≈10 crossover heuristic was derived from two regulated domains with one model family; validation across other domains, models, and trajectory scales is needed.
4. **Multi-agent memory extensions** -- The paper's DPM formulation covers single-agent scenarios; extending the append-only log pattern to multi-agent workflows with shared trajectories is identified as future work.
5. **Formal verification of isolation guarantees** -- Structural isolation arguments should be complemented by formal proofs or red-teaming under adversarial multi-tenant loads.

---

## Authors & Institutions

Vasundra Srinivasan (AI Architect; author of *Data Engineering for Multimodal AI*, O'Reilly; Stanford School of Engineering)
