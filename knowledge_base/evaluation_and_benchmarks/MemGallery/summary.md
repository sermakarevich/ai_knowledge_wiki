# Mem-Gallery: Benchmarking Multimodal Long-Term Conversational Memory for MLLM Agents

**Paper:** [Mem-Gallery: Benchmarking Multimodal Long-Term Conversational Memory for MLLM Agents (Bei et al., 2025)](https://arxiv.org/abs/2601.03515)

## Human Readable TL;DR

Imagine you have a personal assistant who you talk to every day, sharing photos and stories. Most AI assistants today either remember your words but forget your pictures, or only pay attention to recent conversations. This paper creates a rigorous test -- like a school exam -- to measure whether AI assistants can truly remember both pictures and words across many separate conversations over a long period. The tests revealed that today's AI assistants are decent at recalling facts but struggle badly when they need to reason about pictures over time, or figure out when old information has been replaced by new information.

## TL;DR

Mem-Gallery is the first comprehensive benchmark for evaluating multimodal long-term conversational memory in MLLM agents. It introduces a multi-session dataset with tightly coupled visual and textual information, a 3×3 evaluation framework covering memory extraction, reasoning, and knowledge management, and benchmarks 13 existing memory systems. Key finding: simple multimodal RAG (MuRAG) outperforms complex architectures by 11.85% F1, while all systems struggle severely with knowledge conflict resolution, temporal reasoning over vision, and answer refusal.

---

## Problem & Motivation

Existing long-term memory benchmarks (LoCoMo, LongMemEval, MemoryAgentBench) are text-only, while multimodal benchmarks (MMDU, MMRC) evaluate only single-session short-horizon understanding. No benchmark tests how MLLM agents maintain, update, and reason over both vision and language across multiple sessions. Even LoCoMo -- the closest prior work -- shows only marginal gains from visual clues because its tasks can be solved without them. Real-world agents must handle evolving multimodal information where visual evidence is essential, facts get updated, and contradictions must be resolved.

---

## Main Original Ideas

1. **Multimodal Long-Term Conversational Memory Scenario** -- Defines a new evaluation setting where agents must retain and reason over interleaved visual and textual information across multiple sessions with temporal gaps, where information can be updated or contradicted over time.

2. **Two-Strategy Dataset Construction** -- Combines (a) human-authored story outlines + LLM-generated dialogues with manually inserted images, and (b) topic-clustering of existing single-session dialogues into multi-session sequences, ensuring both coverage and genuine multimodal dependencies.

3. **3×3 Evaluation Framework** -- Nine tasks across three functional dimensions: Memory Extraction & Adaptation (Factual Retrieval, Visual-centric Search, Test-Time Learning), Memory Reasoning (Temporal, Visual-centric, Multi-entity), and Memory Knowledge Management (Knowledge Resolution, Conflict Detection, Answer Refusal).

4. **Evidence Annotation** -- Each QA pair carries explicit evidence markup pointing to which dialogue turns or visual content are required, enabling fine-grained retrieval diagnostics beyond end-to-end QA scores.

5. **Unified Benchmarking Protocol** -- Thirteen memory systems (8 textual + 5 multimodal) evaluated under a consistent incremental accumulation + top-K retrieval pipeline, with both answer quality metrics (F1, BLEU-1, EM, LLM-judge) and retrieval metrics (Recall@K, Precision@K, Hit@K).

---

## Key Findings

| Method | Type | Overall F1 | Notes |
|--------|------|-----------|-------|
| MuRAG | Multimodal | **Best** (+11.85% over best text) | Simple multimodal RAG wins overall |
| UniversalRAG | Multimodal | 2nd best multimodal | Simple beats complex |
| A-Mem | Textual | Best textual | Agentic memory org helps |
| MemoryOS | Textual | 2nd best textual | -- |
| Full Memory (Multimodal) | Multimodal | Below Full Memory (Text) | Token overhead hurts |
| FIFO | Textual | High AR score | Refusal by default, not intelligence |

- Explicit visual preservation beats high-quality caption proxies, especially for Factual Retrieval, Visual-centric Search, and Test-Time Learning.
- Complex multimodal architectures (NGM, AUGUSTUS) do not outperform simple multimodal RAG -- alignment quality matters more than architecture complexity.
- Naive multimodal accumulation (Full Memory Multimodal) underperforms text-only full context due to token bloat and visual noise crowding out text.
- All systems perform poorly on Knowledge Resolution and Conflict Detection -- current designs fundamentally cannot handle dynamic information updates.
- Answer Refusal shows inverse correlation with memory strength: better memory systems over-retrieve and hallucinate rather than refuse.
- Increasing retrieval size K improves recall but sharply degrades precision; diminishing returns plateau around K=10--15 for most systems.
- Multimodal systems carry substantially higher computational overhead than textual counterparts, an unsolved deployment challenge.

---

## Suggestions & Future Directions

1. **Principled multimodal memory organization** -- Develop structured condensation and organization strategies (analogous to A-Mem/MemoryOS for text) to manage heterogeneous visual+text entries over long horizons without token explosion.
2. **Multimodal reasoning beyond retrieval** -- Current work focuses on storage/retrieval; genuine temporal, cross-session visual reasoning requires new architectural approaches beyond RAG.
3. **Robust knowledge management** -- Build mechanisms for detecting conflicts, resolving contradictions, and maintaining consistency in evolving multimodal memory rather than naive append-only storage.
4. **Calibrated answer refusal** -- Decouple retrieval capability from hallucination avoidance; systems should refuse when evidence is absent, not just when retrieval fails.
5. **Efficiency optimization** -- Reduce multimodal memory overhead (compression, hierarchical indexing) to make long-horizon agents practical in real-time settings.
6. **Retrieval quality over quantity** -- Invest in selective, relevance-aware retrieval rather than increasing K; precision degrades sharply with larger retrieval windows.

---

## Authors & Institutions

Yuanchen Bei (UIUC), Tianxin Wei (UIUC), Xuying Ning (UIUC), Yanjun Zhao (UIUC), Zhining Liu (UIUC), Xiao Lin (UIUC), Jingrui He (UIUC), Hanghang Tong (UIUC), Yada Zhu (MIT-IBM Watson AI Lab, IBM Research), Hendrik Hamann (Stony Brook University, Brookhaven National Laboratory)
