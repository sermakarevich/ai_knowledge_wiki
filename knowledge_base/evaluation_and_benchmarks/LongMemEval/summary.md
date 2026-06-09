# LONGMEMEVAL: Benchmarking Chat Assistants on Long-Term Interactive Memory

**Paper:** [LONGMEMEVAL: Benchmarking Chat Assistants on Long-Term Interactive Memory (Wu et al., 2024)](https://arxiv.org/abs/2410.10813)

## Human Readable TL;DR

Imagine hiring a personal assistant who forgets everything after each meeting. That's the problem with today's AI chatbots -- they struggle to remember what you told them weeks ago. This paper creates a rigorous test (like a standardized exam) to measure how well AI assistants can actually remember long-term conversations, and then shows practical tricks to make them significantly better at it. The result: a clear recipe for building AI assistants with genuinely lasting memory.

## TL;DR

LONGMEMEVAL is a benchmark for evaluating five core long-term memory abilities of LLM-based chat assistants: information extraction, multi-session reasoning, knowledge updates, temporal reasoning, and abstention. Evaluation reveals that commercial systems (ChatGPT, Coze) and long-context LLMs suffer 30--64% accuracy drops on memory tasks. A proposed unified indexing-retrieval-reading framework, augmented with session decomposition, fact-expanded keys, time-aware queries, and Chain-of-Note reading, substantially recovers this lost performance.

---

## Problem & Motivation

LLM-based chat assistants fail at tasks requiring long-term accumulated personal knowledge -- recalling user preferences, past events, or evolving facts across many sessions. Existing benchmarks (MSC, LoCoMo, MemoryBank) are too short (few-thousand tokens), focus on human-human dialogue rather than task-oriented human-AI sessions, and omit critical abilities like temporal reasoning, knowledge updates, and intelligent abstention. This leaves developers without a reliable way to measure or improve real-world long-term memory.

---

## Main Original Ideas

1. **LONGMEMEVAL Benchmark** -- 500 human-curated questions across 7 question types (single-session-user, single-session-assistant, single-session-preference, multi-session, knowledge-update, temporal-reasoning, false-premise). Histories reach up to 1.5M tokens (500 sessions in LONGMEMEVAL_M), generated via a "needle-in-a-haystack" style pipeline using a 164-attribute user ontology.

2. **Five Core Memory Abilities** -- Formally defines Information Extraction (IE), Multi-Session Reasoning (MR), Knowledge Updates (KU), Temporal Reasoning (TR), and Abstention (ABS) as the axes along which any memory-augmented assistant should be evaluated.

3. **Unified Memory Framework** -- Breaks memory-augmented systems into three stages (Indexing → Retrieval → Reading) and four control points: Value (what to store), Key (what to index by), Query (how to search), and Reading Strategy (how to generate answers from retrieved items).

4. **Fact-Augmented Key Expansion** -- Augments raw session/round content with LLM-extracted user facts as the retrieval key (document expansion), improving Recall@k by 9.4% and end-to-end QA by 5.4% on average.

5. **Time-Aware Query Expansion** -- An LLM extracts an explicit time range from temporal queries; only memory items within that range are searched, improving temporal recall by 6.8--11.3%.

6. **Chain-of-Note + JSON Structured Reading** -- Prompts the reader LLM to first extract relevant notes from retrieved items (CoN), with items serialized as JSON for clear boundary recognition, yielding up to 10 absolute point gains over naive reading even under oracle retrieval.

---

## Key Findings

| System | Setting | Accuracy Drop vs. Full-Context Oracle |
|---|---|---|
| ChatGPT (GPT-4o) | Short history (3-6 sessions) | **-37%** |
| Coze (GPT-4o) | Short history (3-6 sessions) | **-64%** |
| GPT-4o (long-context) | LONGMEMEVAL_S (~115k tokens) | **-30 to -60%** |
| Llama 3.1 70B | LONGMEMEVAL_S | **-30 to -60%** |

- Round-level value granularity outperforms full-session storage for strong reader LLMs; fact decomposition helps specifically for multi-session reasoning.
- Condensed keys (summaries/facts only, no original value) do not improve retrieval -- completeness of the original value matters.
- Weaker LLMs (Llama 3.1 8B) degrade past ~3k retrieved tokens; GPT-4o continues improving beyond 20k tokens.
- "Correct retrieval, wrong generation" accounts for 40--50% of all errors for weaker LLMs, making the reading stage a first-class bottleneck.
- Time-aware query expansion requires a capable LLM (GPT-4o); Llama 3.1 8B hallucinates time ranges and hurts performance.

---

## Suggestions & Future Directions

1. Develop memory deletion and update mechanisms to address privacy concerns (personal information leakage, malicious injection).
2. Investigate better reading strategies for weaker LLMs to reduce "correct retrieval, wrong generation" errors.
3. Explore adaptive token budgets per query type, as optimal retrieved context length varies widely by LLM capability.
4. Extend LONGMEMEVAL to cover non-text modalities and proactive memory (assistant-initiated recall).
5. Design retrieval models natively trained on conversational memory tasks, rather than repurposing generic dense retrievers.

---

## Authors & Institutions

Di Wu (UCLA), Hongwei Wang (Tencent AI Lab Seattle), Wenhao Yu (Tencent AI Lab Seattle), Yuwei Zhang (UC San Diego), Kai-Wei Chang (UCLA), Dong Yu (Tencent AI Lab Seattle)
