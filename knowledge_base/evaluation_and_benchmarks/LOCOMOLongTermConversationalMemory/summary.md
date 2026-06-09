# Evaluating Very Long-Term Conversational Memory of LLM Agents

**Paper:** [Evaluating Very Long-Term Conversational Memory of LLM Agents (Maharana et al., 2024)](https://arxiv.org/abs/2402.17753)

## Human Readable TL;DR

Imagine a friend who remembers every detail you've ever told them -- their favorite recipe, your pet allergies, that book you recommended two months ago. Today's AI chatbots are more like goldfish: they forget almost everything after a short chat. This paper creates a massive collection of very long, realistic AI conversations (like a year's worth of texting), then tests how well AI systems can remember important details from way back. They find that even the best tricks only get AI partway to human-level memory.

## TL;DR

This paper introduces LOCOMO, a benchmark dataset of very long-term dialogues (avg. 300 turns, 9K tokens, up to 35 sessions) generated via a machine-human pipeline using persona-driven agents with event graphs and multimodal (image) capabilities. An evaluation framework with QA, event summarization, and dialogue generation tasks shows that long-context LLMs and RAG strategies improve memory but still fall substantially below human performance -- with observation-based RAG retrieval consistently outperforming raw dialogue retrieval.

---

## Problem & Motivation

Existing long-term dialogue benchmarks evaluate models across at most 5 sessions, leaving the efficacy of LLMs and RAG techniques in truly extended conversations unexplored. Real conversational AI applications (personal assistants, companion chatbots, therapeutic tools) require consistent recall of facts mentioned weeks or months earlier. Without a rigorous benchmark at this scale, it's impossible to measure progress or identify where models break down.

---

## Main Original Ideas

1. **LOCOMO Dataset** -- The first large-scale benchmark for very long-term conversational memory: ~35 sessions, ~300 turns, ~9K tokens per conversation, grounded in persona descriptions and temporal event graphs with multimodal (image-sharing) interactions.

2. **Machine-Human Generation Pipeline** -- Personas and causally-linked event graphs are created first, then LLM agents generate conversations from them, and human annotators edit for long-range consistency and naturalness. This hybrid approach balances scale with quality.

3. **Reflect-and-Respond Memory Architecture** -- Agents maintain short-term (within-session) and long-term (cross-session) memory through periodic "observation" generation: distilling key factual statements about each speaker after each session.

4. **Multi-Task Evaluation Framework** -- Three tasks assess different memory facets: (a) QA with five reasoning subtypes (single-hop, multi-hop, temporal, commonsense, adversarial); (b) event summarization against ground-truth event graphs; (c) multimodal dialogue generation with BLEU and MM-Relevance metrics.

5. **Retrieval Unit Comparison** -- Systematic comparison of three RAG retrieval granularities: raw dialogue history, observation-level summaries, and session-level summaries -- finding that concise observation units consistently outperform raw text.

---

## Key Findings

| Strategy | QA Performance | Notes |
|---|---|---|
| Base LLM (no memory) | Lowest | Forgets cross-session details entirely |
| Long-context LLM (16k) | Moderate improvement | Context length alone insufficient |
| RAG -- Dialog History | Above base | Noise degrades precision |
| RAG -- Observations | **Best automated** | Concise facts boost precision |
| Human | **Upper bound** | All models substantially below |

- **Temporal reasoning** is the hardest QA subtype across all models.
- **Adversarial questions** expose hallucination: models invent plausible but wrong answers.
- For **event summarization**, long-context models do NOT consistently beat base models; incremental summarization works best.
- For **multimodal dialogue**, performance degrades as history grows, but observation-based RAG slows this decline.
- Longer context does not equal better context utilization for complex memory tasks.

---

## Suggestions & Future Directions

1. Design specialized memory architectures beyond simple RAG -- hierarchical or structured stores tailored to long dialogues.
2. Develop better temporal reasoning mechanisms so models understand when events occurred relative to each other.
3. Extend multimodal memory so visual content (shared images) is recalled and referenced accurately across sessions.
4. Build more efficient retrieval systems that discriminate truly relevant history from noise at scale.
5. Explore real-world deployment in personal assistants, therapeutic chatbots, and educational agents that demand consistent long-term personalization.
6. Develop evaluation metrics beyond BLEU that better capture memory fidelity in open-ended conversational settings.

---

## Authors & Institutions

Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, Yuwei Fang -- Snap Research; University of North Carolina at Chapel Hill
