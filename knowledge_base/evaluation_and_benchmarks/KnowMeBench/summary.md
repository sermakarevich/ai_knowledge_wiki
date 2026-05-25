# KnowMe-Bench: Benchmarking Person Understanding for Lifelong Digital Companions

**Paper:** [KnowMe-Bench: Benchmarking Person Understanding for Lifelong Digital Companions (Wu et al., 2026)](https://arxiv.org/abs/2601.04745)

## Human Readable TL;DR

Imagine hiring a personal assistant who reads your entire diary, then you test them -- not on trivia like "what did I eat on Tuesday?" but on deeper questions like "why do I always quit just before finishing things?" Most AI assistants can answer the trivia; almost none can answer the deeper question. This paper builds a test suite specifically designed to catch that gap, using dense literary autobiographies (Proust, Knausgård) as stand-ins for real lifelong personal histories. It turns out current AI memory systems are pretty good at the trivia and quite bad at the deeper stuff, topping out around 22% on psychological insight tasks.

## TL;DR

KnowMe-Bench introduces a benchmark that evaluates AI agents on "person understanding" -- evidence-grounded inference of a person's motivations, principles, and evolving self-concept from long-horizon autobiographical narratives. The benchmark converts raw literary autobiographies into structured "lifelogs" with five cognitive primitives and handles non-linear flashback structures via a Mnestic Realignment Protocol. A three-tier, seven-task evaluation (Factual → Narrative Logic → Psychoanalytic Insight) reveals that current RAG and graph-memory systems plateau at ~22% on the deepest insight tasks, validating that retrieval competence does not equal person understanding.

---

## Problem & Motivation

Existing memory benchmarks for AI agents treat memory as a database of facts: retrieve the right snippet, get the right answer. This works for surface-level personalization but fails at genuine "person understanding" -- inferring stable principles, explaining recurring decision patterns, connecting distant experiences into a coherent self-model, or understanding evolving identity over time.

Two structural gaps afflict prior work:
- **Evaluation misalignment:** Retrieval accuracy is a poor proxy for understanding; "deep" questions without evidence constraints invite hallucination.
- **Data substrate misalignment:** Sparse chat logs and synthetic events strip out the internal deliberation and causal micro-structure that make lived experience meaningful.

The authors argue that building lifelong digital companions requires solving these gaps first, and KnowMe-Bench provides the measurement infrastructure to do so.

---

## Main Original Ideas

1. **Person Understanding as Auditable Inference** -- Frames person understanding not as a vague goal but as an evidence-grounded inference task: every answer must be traceable back to source text, eliminating speculative responses and making evaluation objective.

2. **Atomic Narrative Units (ANUs)** -- Decomposes raw narrative into structured tuples `U = (id, t_anch, ℓ, C)` where `C` contains five cognitive primitives: Action, Dialogue, Environment, Background, and Mind (inner monologue). This high-density representation preserves "micro-texture" lost in typical sparse memory stores.

3. **Mnestic Realignment Protocol** -- A stack-based state machine that detects flashbacks and re-anchors recalled events to their chronological origin, while separately preserving the Mnemonic Trigger (the present-moment cue that invoked the memory). This is the first explicit treatment of non-linear temporal structure in memory benchmarks.

4. **Three-Tier Hierarchical Evaluation** -- Seven tasks grouped into three cognitive levels: (L1) Precision & Factuality (entity recall, adversarial abstention, temporal reasoning), (L2) Narrative Logic & Causality (event ordering, mnestic trigger analysis), (L3) Psychoanalytic Depth (mind-body interaction, expert-annotated psychoanalysis). Each level demands qualitatively deeper inference than the last.

5. **"Update Paradox" Discovery** -- Empirically shows that state-updating memory systems (like Mem0) actively hurt performance on flashback-heavy narratives by misinterpreting recalled past states as updates to current state, overwriting correct present information.

---

## Key Findings

| System | Dataset | Temporal Reasoning (T3) | Insight (L3) |
|--------|---------|------------------------|--------------|
| Base (Qwen3-32B) | D1 (Knausgård) | baseline | baseline |
| Mem0 + Qwen3 | D1 | -3.5% | -- |
| MemOS + Qwen3 | D1 | +10.4% | -- |
| Naive RAG + Qwen3 | D3 (Proust) | -- | -0.5% |
| Best system (MemOS + GPT-5-mini) | D2 | -- | 22.3% |

- **Update Paradox confirmed:** Mem0 regresses -3.5% on temporal reasoning in flashback-heavy text (D1); MemOS gains +10.4% on same task by preserving chronological stream.
- **Context pollution:** Naive RAG boosts factual extraction by +9.2% on Proust but causes -0.5% drop on insight tasks -- semantically similar irrelevant fragments pollute inference.
- **Entity graph advantage:** Mem0 leads on adversarial abstention (T2) by +7.3pp over Naive RAG on event-dense text, using its structured knowledge graph as a hallucination anchor.
- **Hard ceiling on insight:** Even the best system (MemOS + GPT-5-mini) caps at 22.3% on Level III tasks, confirming that current architectures are fundamentally insufficient for psychodynamic reasoning.
- **Stronger backbones reduce memory gains:** GPT-5-mini shows smaller relative improvements from memory modules than Qwen3-32B, suggesting advanced base models partially compensate for weak memory architectures.

---

## Suggestions & Future Directions

1. **Cognitive architecture beyond RAG** -- Results explicitly call for architectures that go beyond retrieval-augmented generation, incorporating true temporal reasoning, mnestic realignment, and multi-hop inference over psychological states.
2. **Denser data substrates** -- Future work should explore richer experience representations, possibly incorporating actual user-generated diaries or multimodal logs (voice, images) rather than literary proxies.
3. **Scaling the pipeline** -- The current multi-agent construction pipeline is expensive; automating and scaling it to cover diverse cultures, languages, and personal histories is a key open challenge.
4. **Reduce LLM-as-a-Judge subjectivity** -- While Cohen's Kappa > 0.75 was achieved against human experts, further work on rubric refinement for the most subjective insight tasks is needed.
5. **Privacy-safe personalization** -- The PII de-identification pipeline is a step forward, but production-ready companions require stronger guarantees; this remains an open engineering and policy challenge.

---

## Authors & Institutions

Tingyu Wu, Zhisheng Chen, Ziyan Weng (equal contribution) -- UCAS, QuantaAlpha, PKU, THU, CITYU-DG, HAINNU, UTHealth Houston, NUS.  
Corresponding: Qizhen Lan (UTHealth), Ronghao Chen (PKU), Huacan Wang (UCAS/QuantaAlpha).
