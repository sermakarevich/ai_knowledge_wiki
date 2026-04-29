# tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge

**Paper:** [tau-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge (Shi, Zytek, Razavi, Narasimhan, Barres, 2025)](https://arxiv.org/abs/2603.04370)

## Human Readable TL;DR

Imagine you're a new bank customer-service agent on your first day. You have a giant binder of policies, product rules, and internal tools -- but nobody told you what's in it or how to use anything. Customers call with messy, vague requests, and you have to flip through the binder, figure out which rules apply, and use the right internal systems to help them. This paper builds a test that checks how well AI chatbots handle exactly that situation -- and finds that even the best ones only get it right about 1 in 4 times.

## TL;DR

tau-Knowledge extends the tau-Bench framework with a knowledge-grounded banking domain (tau-Banking) that requires agents to jointly retrieve procedural knowledge from ~700 unstructured documents, discover tools referenced only in documentation, reason over cross-document policy dependencies, and execute multi-step state changes in live multi-turn conversations. The best model (GPT-5.2 with high reasoning and terminal search) achieves only 25.52% pass^1, and even with gold documents provided directly, the ceiling is ~40%. Terminal-based document navigation significantly outperforms all dense and sparse retrieval methods.

---

## Problem & Motivation

Existing benchmarks evaluate retrieval and tool use independently -- retrieval benchmarks test query-document matching without measuring downstream decision quality, while tool-use benchmarks assume fully specified tool interfaces provided upfront. No benchmark requires agents to jointly: (1) discover tools from documentation, (2) retrieve procedural knowledge from natural-language corpora, (3) reason over complex policies with cross-document dependencies, and (4) execute multi-step tool-mediated state changes -- all within live, multi-turn conversations with ambiguous and evolving user intent. This gap means we cannot measure how well agents perform in realistic knowledge-intensive deployments.

---

## Main Original Ideas

1. **tau-Knowledge Benchmark Framework** -- Extends tau-Bench to unify retrieval-based, long-context, and tool-augmented evaluation in a single framework. Agents must coordinate external natural-language knowledge with tool outputs to produce verifiable, policy-compliant state changes.

2. **tau-Banking Domain** -- A realistic fintech customer-support environment with ~700 interconnected documents covering 21 product categories, 71 topics, and 51 discoverable tools. Tasks average 18.6 required documents and 9.52 tool calls each.

3. **Discoverable Tools** -- Tools are not pre-loaded; they are referenced only implicitly within documentation. The agent's action space expands dynamically based on successful knowledge retrieval, mirroring real deployments where capabilities depend on accessible documentation rather than hard-coded interfaces.

4. **Structured-to-Unstructured Knowledge Base Generation** -- A multi-stage pipeline converts structured product/policy databases into natural-language documents via LLMs with human-in-the-loop review, ensuring internal consistency while enabling systematic task design via constraint validation.

5. **Retrieval-Agnostic Evaluation** -- The benchmark supports dense retrieval, sparse retrieval (BM25), terminal-based filesystem exploration (grep/cat/find), long-context processing, and gold-document configurations, enabling fair comparison across paradigms.

6. **Flow-Based User Simulation** -- Conditional rules prescribe user behavior at evaluation-critical junctures while preserving linguistic diversity through free LLM generation for non-flow-governed portions.

---

## Key Findings

### Overall Performance

| Model | Best Config | pass^1 | pass^4 |
|---|---|---|---|
| **GPT-5.2 (high reasoning)** | Terminal | **25.52%** | 13.40% |
| Claude-4.5-Opus (high) | Terminal | 24.74% | -- |
| Claude-4.5-Sonnet (high) | Terminal | 22.42% | -- |
| Gemini-3-Flash (high) | Terminal | 20.62% | -- |
| Gemini-3-Pro (high) | Terminal | 15.72% | -- |
| GPT-5.2 (no reasoning) | Qwen3-emb-8b | 12.37% | -- |

### Retrieval Method Comparison (averaged across models)

| Configuration | Avg pass^1 |
|---|---|
| **Gold (oracle)** | **32.18%** |
| Terminal | 19.20% |
| Qwen3-emb-8b | 17.11% |
| BM25 | 17.04% |
| text-emb-3-large | 16.88% |

- Terminal-based search significantly outperforms all dense/sparse retrieval (p < 0.05)
- No significant differences among Qwen3-emb-8b, BM25, and text-emb-3-large
- Even with gold documents, best pass^1 is only **39.69%** (Claude-4.5-Opus)
- No-knowledge baseline: ~2% pass^1 -- confirming tasks genuinely require retrieval
- Long-context baseline (full KB in prompt): ~12% pass^1

### Efficiency

- Claude-4.5-Opus achieves comparable accuracy to GPT-5.2 (high) while being **~9x faster** in terminal mode (21s vs 187s median turn)
- GPT-5.2 (high) uses ~2.3x more shell commands and ~1.7x more tokens than Claude-4.5-Opus
- Document recall varies dramatically by agent: text-embedding-3-large achieves 57% recall with Opus but only 28% with GPT-5.2 (no reasoning)

### Error Analysis

- Search inefficiency and unwarranted assumptions: ~23% of failures
- Complex cross-document policy reasoning failures: ~14.5%
- Failure to respect implicit subtask ordering: ~5%
- Overtrusting user assertions without verification: ~4%

### Ablations

- Adding a reranker: no significant improvement
- Adding grep alongside dense/sparse retrieval: no significant improvement
- Write tools in terminal: no significant effect (models rarely used write commands)
- Retrieval set size k=10 vs k=20: no significant difference; k=5 slightly worse for BM25

---

## Suggestions & Future Directions

1. **Solution efficiency as a first-class metric** -- Progress should be measured not just by task success but by minimal time, tool calls, and conversational backtracking to reach correct outcomes.

2. **More sophisticated context management** -- Current truncation-based approaches are rarely triggered; selective summarization or retrieval-aware compression could help.

3. **Terminal as knowledge management** -- Agents could use write commands for note-taking, state tracking, and knowledge reorganization during long-horizon reasoning, an under-explored capability.

4. **Few-shot search constraints** -- Real systems often limit retrieval calls; evaluating under such constraints would better reflect deployment conditions.

5. **Richer user simulations** -- Current simulations do not capture variation in user expertise, colloquial language, or grammatically imperfect inputs.

6. **Latency metrics are provider-dependent** -- Absolute timing results may not generalize to alternative deployment settings.

---

## Authors & Institutions

Quan Shi (Sierra), Alexandra Zytek (Sierra), Pedram Razavi (Sierra), Karthik Narasimhan (Princeton University), Victor Barres (Sierra)
