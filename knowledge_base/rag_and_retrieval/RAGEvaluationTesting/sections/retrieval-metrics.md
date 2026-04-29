> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

## Retrieval Metrics that Predict Quality

Measure retriever performance using precision/recall@k, MRR, nDCG, and RAG-specific metrics. Always report per-bucket to avoid hiding long-tail risk.

### Core Concepts

#### Classic Ranking Metrics

**Precision@k:** Fraction of top-k results that are relevant. Protects against distractors misleading generation.

```
precision@k = (relevant items in top-k) / k
```

**Recall@k:** Fraction of all relevant items that appear in top-k. Protects against missing evidence.

```
recall@k = (relevant items in top-k) / (total relevant items)
```

**MRR (Mean Reciprocal Rank):** Average of 1/rank for the first relevant item. Rewards early-ranked evidence; critical for prompt-pack (LLM may only read top chunks).

```
MRR = (1/rank of first relevant item) averaged across queries
```

**nDCG (Normalized Discounted Cumulative Gain):** Supports graded relevance (partially relevant, fully relevant). Rewards both coverage and ranking quality.

```
DCG = sum(relevance_i / log2(rank_i + 1))
nDCG = DCG / ideal_DCG
```

#### RAG-Specific Twist

Standard ranking metrics assume "good if relevant." RAG adds constraints:

- **Limited context:** LLM reads only top-k chunks due to token budget → early ranking matters more than coverage
- **Ordering matters:** Prompt packs top chunks first → irrelevant chunks in top-k mislead generation even if relevant chunks exist
- **Citation dependency:** Generator must cite the chunks it uses → missing chunks later in ranking can't be cited

**Key insight:** In RAG, a relevant chunk buried at rank 50 is almost worthless if top-k=10 and token budget is tight.

#### Bucketed Reporting

**Always report per-bucket metrics.** Averages hide long-tail risk:

- **Factoid vs multi-hop:** Multi-hop queries may need multiple chunks; factoids may need just one
- **Recency-sensitive:** Recent query types may have different retrieval patterns than historical
- **Entity type/jargon:** Rare entities or domain jargon may have worse retrieval
- **Injection/adversarial:** Adversarial queries may have high false-positive rates

**Example:** Overall recall@5 = 92%, but recall@5 for "recency + jargon" bucket = 78%. Average hides the problem.

---

## Decision Framework: Choosing Retrieval Metrics

1. **Do you have gold passages?** 
   - Yes → use recall@k, MRR, nDCG (all supported by gold labels)
   - No → label top-10 retrieved chunks on a small set; bootstrap recall@k

2. **How tight is the context budget?**
   - Small k (top-5 or top-10) → prioritize MRR (early relevance) and precision@k (distractor control)
   - Large k (top-50+) → can emphasize recall@k (coverage)

3. **Is distractor risk high?**
   - Yes (e.g., legal, medical) → track precision@k and "context precision" (fraction of relevant in packed context)
   - No → focus on recall and coverage

4. **Choose k based on reality:** Don't optimize k you can't reach; set k to match prompt-pack limits and reranker candidate size

5. **Gate by bucket:** Enforce stricter tolerances for high-risk buckets (recency, jargon, multi-hop, injection)

---

## Debugging Retrieval Failures

**When retrieval metrics drop, debug coverage vs. ordering vs. noise:**

1. **Reproduce on a frozen snapshot:** pin corpus, index build, embedding model, chunker
2. **Classify misses:** wrong entity, synonym/jargon, chunk boundary, recency, multi-hop
3. **Check candidate coverage first:** if relevant chunk not in top-N, reranker and prompt-pack can't recover
4. **Inspect ordering:** if relevant chunk exists but buried, focus on ranking (embeddings, index, reranking)
5. **Add hard negatives:** encode failure patterns (e.g., near-duplicates, distractors) into test set; measure their ranking

---

## Interview Q&A

**Q: Precision@k vs Recall@k in RAG -- what's the tradeoff?**

A: Recall@k protects against missing evidence (if right chunk not in top-k, generation fails). Precision@k protects against distractors (irrelevant chunks mislead LLM). In RAG with tight token budgets, low precision (many distractors in top-5) harms grounding even if overall recall is high.

Rubric: 2 = connects to generation/grounding + token budget constraint.

---

**Q: What does MRR measure and why is it useful?**

A: MRR rewards placing the first relevant chunk early. This matters in RAG because LLMs often use top-ranked evidence first and may truncate. Prompt packing shows top chunks first; if first relevant rank is 50, it may not be packed.

Rubric: 2 = mentions truncation/prompt-pack + early ranking.

---

**Q: Why use nDCG instead of MRR?**

A: nDCG supports graded relevance (partially relevant, fully relevant) and multiple relevant chunks. It measures both that you have relevant chunks AND that they're ranked well. MRR only cares about the first relevant chunk.

Rubric: 2 = graded relevance + multiple evidence.

---

**Q: How do you label retrieval relevance quickly?**

A: Use binary rubric: "Would this chunk help answer the query?" Add 0/1/2 scale if you need graded. For weak labels, use LLM-assisted labeling (LLM proposes, human spot-checks) on a small calibration set, then apply to full eval set. Validate correlation on holdout.

Rubric: 2 = binary or graded + weak labels + validation.

---

**Q: Design robust query buckets for retrieval eval.**

A: Factoid, entity disambiguation, multi-hop, recency-sensitive, jargon-heavy, contradictory sources, long-context, injection/adversarial. Report metrics per-bucket; enforce stricter thresholds for high-risk buckets.

Rubric: 2 = includes risk buckets + stratified thresholds.

---

## Cheat Sheet

**Metrics quick map:**
- **precision@k:** Distractor control (protect groundedness)
- **recall@k:** Miss control (protect coverage)
- **MRR:** First relevant early (protect truncation)
- **nDCG:** Graded + multiple (protect ranking quality)

**Always:**
- Report per-bucket metrics (avoid hiding tail risk)
- Validate k matches real token/candidate budget
- Use bucketed thresholds (high-risk buckets stricter)

