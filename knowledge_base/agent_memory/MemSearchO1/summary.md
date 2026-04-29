# MemSearch-o1: Empowering Large Language Models with Reasoning-Aligned Memory Growth in Agentic Search

**Paper:** [MemSearch-o1 (Zhang et al., 2026)](https://arxiv.org/abs/2604.17265)

## Human Readable TL;DR

Imagine a detective solving a complex case by asking questions, reading documents, and forming theories step by step. The problem is that as they gather more notes, their desk gets buried under irrelevant papers, and they lose track of the important clues. This paper proposes a smart note-taking system for AI search: instead of keeping every scrap of retrieved text, the AI identifies the key "seed" words from each question (who, what, when, how-much), grows small focused note cards around each seed, and at the end stitches the most relevant cards into a clean, logical story before answering. The result is a cleaner, faster, more accurate AI researcher.

## TL;DR

MemSearch-o1 is an agentic search framework that mitigates the "memory dilution" problem in iterative LLM search by replacing cumulative context concatenation with three-stage structured memory: (1) extracting fine-grained seed tokens from queries using POS categories, (2) growing focused memory fragments anchored to each seed from retrieved documents, and (3) retracing a globally coherent memory path via a contribution function (relevance + bridge potential) before answer generation. Evaluated on LongBench, LongBench v2, and LongBookQA with Qwen2.5-72B and DeepSeek V3.1, it beats the strongest baselines by up to 21.93% F1 on HotpotQA while reducing token consumption via O(ND) complexity versus O(N^2 D) for traditional deep search.

---

## Problem & Motivation

Deep / agentic search has LLMs iteratively plan, retrieve, reflect, and reason over external knowledge to answer multi-hop questions. But each round piles more thinking history and document fragments into the system memory, and several failure modes emerge:

- **Memory dilution:** The signal-to-noise ratio collapses as irrelevant retrieved text accumulates, and LLM attention overlooks crucial tokens in long inputs.
- **Information loss from summarization:** Existing summarization/filtering methods compress memory but drop critical details or miss evolving query semantics.
- **Suboptimal reasoning paths:** Pruning/distillation approaches optimize for task rewards without modeling the structure and logic connecting memory pieces.
- **Underutilized reasoning potential:** Large LLMs have strong latent multi-hop reasoning, but poor memory management throttles it; prompt engineering alone is not enough.

The authors argue for **explicit, fine-grained, reasoning-aligned memory management** that builds a concise yet comprehensive semantic environment for LLM reasoning.

---

## Main Original Ideas

1. **Memory Seeds Preparation.** Rather than operate on coarse query-document similarity, MemSearch-o1 tokenizes each reformulated search query with spaCy and groups tokens into linguistic "seed" categories: subjects (nouns/pronouns, temporal markers), actions (verbs), and degree modifiers (adjectives/adverbs). These seeds become explicit anchors for retrieving and growing memory, giving fine-grained alignment between query intent and memory content.

2. **Memory Fragments Growth.** For each round, the LLM is prompted with the seeds, the retrieved documents, and task instructions to expand each seed into a focused "memory fragment." This replaces dumping raw passages into context with per-seed distilled content, producing concise fragments tightly tied to query intent rather than superficially relevant text.

3. **Memory Path Retracing via Contribution Function.** After iterative rounds, all fragments are scored by a contribution function combining relevance to the original query (cosine similarity) and "bridge potential" (weighted similarity to other fragments conditioned on the current sub-query). Low-scoring fragments are filtered; a greedy search then constructs an optimal path that maximizes total contribution while penalizing semantic jumps between adjacent fragments -- yielding a coherent narrative used as the final context for answer generation, bypassing the cumulative system memory.

4. **Paradigm shift from stream to structured growth.** The framework replaces "stream-like context concatenation" in prior agentic search with **token-level memory growth + path-based reasoning**, which is both more targeted and more efficient.

5. **Efficiency by design.** Because fragments are extracted only from documents retrieved in the current turn (and only the refined path feeds final generation), time complexity drops from the O(N^2 D) of traditional deep search (where system memory is re-read each round) to O(ND), widening the efficiency gap as iterations grow.

---

## Key Findings

### LongBench (F1 gains for MemSearch-o1 vs strongest baseline, DeepSeek V3.1 backbone)

| Dataset | Relative gain |
|--------|--------------|
| **HotpotQA** | **+21.93%** |
| **MuSiQue** | **+17.38%** |
| **2WikiMQA** | **+16.53%** |

- Consistent SOTA across 8 LongBench datasets (multi-doc and single-doc QA) with both Qwen2.5-72B-Instruct and DeepSeek V3.1.
- Works even on single-document tasks (Qasper, MultiFieldQA-en) without over-searching.
- Holds up on very large corpora: LongBench v2 (15k-129k tokens) and LongBookQA (192k-2.068M tokens). Other agentic baselines become unstable, oversearching or misleading themselves in huge contexts.

### Scaling behavior (2WikiMQA, Qwen2.5-Instruct family)

- Activates deep-search reasoning earlier with scale: clear gains begin around **3B parameters**.
- Amber baseline only takes off beyond 7B; Search-o1 (Refined) scales unstably.

### Retrieval top-k sensitivity

- Moderate k enriches memory and reduces reasoning steps; excessive k introduces redundancy on focused datasets (2WikiMQA) but keeps helping on dispersed-evidence datasets (MuSiQue), because token-level extraction can still distill useful content.

### Ablation

- **w/o memory seeds + fragments growth:** large drop -- LLM gets buried in redundant retrieval.
- **w/o memory path retracing:** also degrades -- fragments accumulate without coherent organization.
- Both fine-grained growth and structured retracing are necessary.

### Qualitative (UMAP) and efficiency

- Memory growth steers the LLM toward regions closer to ground-truth answers and enables broader yet goal-directed exploration.
- Lower average token consumption and reduced inference time vs baselines, with the advantage widening as search rounds grow (O(ND) vs O(N^2 D)).

---

## Suggestions & Future Directions

1. **Smaller LLMs (<3B):** Authors flag performance on small backbones as a key open problem -- the framework currently relies on mid-to-large models to effectively generate and organize fragments.
2. **Better seed preparation:** Refining how query tokens are categorized and weighted into memory seeds (beyond POS-based grouping with spaCy) could sharpen alignment.
3. **Better path optimization:** Moving beyond the greedy contribution-maximization + smoothness penalty toward learned or globally-optimal path construction.
4. **Transfer beyond search:** Extend reasoning-aligned memory growth to other agentic tasks (planning, tool use, multi-agent coordination) where iterative context accumulation causes similar dilution.
5. **Adaptive thresholds:** Thresholds for contribution filtering and bridge-potential weighting are fixed hyperparameters; making them adaptive to query complexity or domain could improve robustness.

---

## Authors & Institutions

Sheng Zhang, Junyi Li, Yingyi Zhang, Pengyue Jia, Xiaowei Qian, Wenlin Zhang, Maolin Wang, Xiangyu Zhao (City University of Hong Kong); Yingyi Zhang (also Dalian University of Technology); Yichao Wang, Yong Liu (Huawei Technologies Ltd.). Corresponding authors: Yichao Wang, Xiangyu Zhao.
