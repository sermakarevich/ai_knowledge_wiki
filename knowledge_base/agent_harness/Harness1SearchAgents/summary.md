# Harness-1: Reinforcement Learning for Search Agents with State-Externalizing Harnesses

**Paper:** [Harness-1: Reinforcement Learning for Search Agents with State-Externalizing Harnesses (Jiang et al., 2026)](https://arxiv.org/abs/2606.02373)

## Human Readable TL;DR

Imagine you're a detective working a complex case. A less experienced partner has to remember every lead they've followed, every suspect they've ruled out, and every clue they've verified -- all from memory. A well-designed case management system, however, handles all that bookkeeping automatically, letting the detective focus purely on deciding what to investigate next. Harness-1 applies this idea to AI-powered document search: instead of making the AI model remember everything it's searched and evaluated across a long conversation, a specialized "harness" system does all that tracking automatically. The AI just decides what to look for. This makes the system dramatically better at finding relevant documents -- even across domains it was never trained on -- with far less training data than competing approaches.

## TL;DR

Harness-1 is a 20B search agent trained via reinforcement learning within a stateful environment harness that externalizes search state management. By offloading mechanical bookkeeping to the harness (candidate pools, importance-tagged curated sets, evidence graphs, verification records, budget-aware rendering), the policy focuses on semantic decisions alone. The result: 0.730 average curated recall across 8 diverse benchmarks, outperforming the next-best open search agent by +11.4 points and remaining competitive with much larger frontier models, with especially strong generalization to held-out domains (+17.0 pts vs. +7.9 pts on training domains).

---

## Problem & Motivation

Current retrieval-augmented search agents train LLMs to simultaneously make semantic search decisions (what to query, which documents to keep) AND maintain complex bookkeeping (tracking seen documents, unmet constraints, verified claims) from an ever-growing append-only transcript. This dual burden causes RL training to be inefficient and poorly conditioned:

- Hard queries yield nearly identical empty-set rewards, providing little discriminative learning signal.
- Large tool vocabularies collapse to repeated search calls when state isn't managed.
- Cross-document structure is present in transcripts but too diffuse for reliable use.
- When the final curated set is wrong, the reward signal cannot distinguish whether failure came from bad search, forgotten evidence, missing verification, or poor curation.

---

## Main Original Ideas

1. **Stateful Cognitive Offloading** -- The foundational principle: the retrieval policy should make only semantic decisions (what to search, which documents to keep, what to verify, when to stop), while the environment-side harness maintains all recoverable state. This gives RL a stable interface for improving search behavior instead of asking the model to rediscover bookkeeping from raw observations.

2. **WORKINGMEMORY Harness Architecture** -- A comprehensive per-episode state machine with seven components: candidate pool (P_t, with compression and deduplication), importance-tagged curated set (C_t/I_t, capped at 30 docs with eviction), full-text store (D_t), evidence graph (G_t, entity-to-doc mapping), verification cache (V_t, claim entailment records), search history (H_t), and budget-aware renderer (B_t). Policy actions edit this state via structured "Harmony actions" rather than extending a transcript.

3. **Three Trainability Requirements for Stateful Harnesses**:
   - *Warm-started curation*: Auto-seed the curated set from the first successful search (top k=8 reranked results at "fair" importance) to prevent early rollouts from producing indistinguishable empty-set rewards.
   - *Compact derived-state rendering*: Sentence-BM25 compression (top K=4 sentences per retrieval), two-level deduplication (chunk ID + MinHash-LSH with Jaccard threshold 0.85), and a 5-pass progressive context degradation algorithm to stay within 30,720 token budget.
   - *Diversity-preserving incentives*: RL reward includes a tool-diversity bonus (w_div) forcing a balanced rhythm of search, curation, review, and verification -- without it, the policy collapses to search-only.

4. **Harmony Action Set** -- Structured actions that operate as edits over WORKINGMEMORY: `fan_out_search` (parallel multi-query with RRF + reranking), `search_corpus` (single hybrid BM25+dense), `grep_corpus` (regex), `read_document`, `curate` (add/remove/retag with importance levels), `verify` (LLM-based entailment check stored in V_t), `review_docs` (re-render without new search), `end_search`.

5. **Teacher-Augmented SFT + CISPO RL Training Pipeline** -- GPT-5.4 generates 899 high-quality trajectories as a live agent running within the full Harness-1 harness (with turn-level guidance injected), used for LoRA SFT (rank 32, 3 epochs on gpt-oss-20b). RL then refines with on-policy CISPO using within-group advantage normalization on SEC data (128 batch × 8 rollouts, 80 steps ≈ 82K rollouts). Reward combines F_beta (β=2), trajectory recall, final-answer recall, answer bonus, tool-diversity bonus, answer-miss penalty, and turn penalty.

---

## Key Findings

| Method | Size | Avg Curated Recall | Avg Trajectory Recall |
|--------|------|-------------------|----------------------|
| **Harness-1** | **20B** | **73.0%** | **80.7%** |
| Opus-4.6 | frontier | 76.4% | 79.4% |
| GPT-5.4 | frontier | 70.9% | 75.2% |
| Sonnet-4.6 | frontier | 68.8% | 72.5% |
| Kimi-K2.5 | frontier | 64.7% | 79.4% |
| Tongyi DeepResearch | 30B | 61.6% | 67.3% |
| Context-1 | 20B | 60.3% | 75.6% |
| GPT-OSS-120B | 120B | 49.6% | 76.9% |
| Qwen3 | 32B | 21.6% | 44.6% |
| Search-R1 | 32B | 28.9% | 28.9% |

- **Transfer is stronger than in-domain gains**: +17.0 pts mean on held-out benchmarks (LongSealQA, Seal0QA, FRAMES, HotpotQA) vs. +7.9 pts on source-family -- a 2.2x gap -- indicating domain-general operations were learned over explicit search state.
- **Training-efficient**: 4,352 unique training items (899 SFT trajectories + 3,453 RL queries) vs. Context-1's >17K and Search-R1's 221K+ RL rows.
- **Diversity reward is essential**: Without w_div, tool diversity collapses from ~6 to ~3.5 and curated recall plateaus at ~0.53; with it, diversity stabilizes at ~4.30 and recall reaches ~0.60.
- **Harness alone contributes**: Running GPT-5.4 under Harness-1's environment (no RL training) yields +4.2 recall points over Context-1 harness, validating the harness as a compute-allocation mechanism.
- **Six of seven harness components contribute positively**: Disabling any single mechanism reduces Final-Answer Recall by 3.9--7.9%; disabling all simultaneously reduces Recall by 12.2%.
- **Discovery vs. selection gap**: Harness-1 typically discovers the relevant evidence (high trajectory recall) but lags Opus-4.6 on BC+ final-answer recall mainly due to selection quality, not discovery.
- **Downstream RAG accuracy improves**: Better curated sets translate directly to higher answer accuracy when passed to frozen frontier generators (GPT-5.4, Sonnet-4.6, Opus-4.6, Kimi-2.5).

---

## Suggestions & Future Directions

1. **Smarter evidence graph**: Replace the current regex-based entity extraction (proper nouns, four-digit years, numeric dates) with learned entity linking and relation extraction for richer cross-document structure.
2. **Uncertainty-aware evidence organization**: Incorporate uncertainty signals into how the harness organizes and renders evidence, enabling better prioritization of unverified vs. confirmed claims.
3. **Harness engineering as a research axis**: Generalize the stateful cognitive offloading principle to other agentic tasks beyond retrieval -- any domain where the environment can reliably maintain state that the policy would otherwise have to reconstruct.
4. **Policy-harness co-design**: Move beyond hand-designed harnesses toward joint optimization of the harness interface and the policy, possibly via meta-learning or automated harness search (e.g., AutoHarness, Meta-Harness).
5. **Abstention and open-ended research**: Extend to settings requiring abstention under missing evidence or adversarial corpora, which the current system is not designed for.

---

## Authors & Institutions

Pengcheng Jiang (UIUC), Zhiyi Shi (UIUC), Kelly Hong (UC Berkeley / Chroma), Xueqiang Xu (UIUC), Jiashuo Sun (UIUC), Jimeng Sun (UIUC), Hammad Bashir (Chroma), Jiawei Han (UIUC)
