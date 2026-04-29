> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

## Offline vs. Online Evaluation Strategy

The fundamental challenge: offline tests can pass while users are unhappy. Design an evaluation program that aligns offline signals with real user outcomes.

### Core Concepts

#### Offline Evaluation

**Purpose:** Repeatability. Powers benchmarking, regression tests, and quality gates in CI/CD.

**Characteristics:**
- Uses pinned versions (model, prompt, index, embeddings, chunker)
- Requires stable datasets (golden sets, snapshots)
- Controlled failure labels from human consensus or strong rubrics
- Fast (seconds to minutes); deterministic
- Runs on every commit

**Typical signals:**
- Retrieval recall@k, precision@k
- Reranker win-rate
- Answer relevance (human-scored or LLM-judged)
- Groundedness (chain-level hallucination)
- Citation accuracy (claim-to-chunk mapping)

**Limitations:**
- Golden sets become stale; real queries diverge
- LLM judges drift silently (same input, different output)
- Distribution shift in corpus/queries not caught
- Long-tail failures rare in small test sets

#### Online Evaluation

**Purpose:** Truth. Catches drift, long-tail failures, and real user behavior feedback.

**Characteristics:**
- Uses live production traffic
- Sampling-based (can't label everything)
- Risk-weighted audits (high-stakes queries sampled more)
- Slower feedback loop (days to weeks)
- Continuous monitoring

**Typical signals:**
- User satisfaction (1-5 star rating, thumbs up/down)
- Deflection (user immediately re-queries, searches competitor)
- Complaint rate (feedback, tickets, escalations)
- Re-query rate (user reformulated their question)
- Latency, cost per query
- Critical error rate (unsupported claims, policy violations)

**Limitations:**
- Sparse labels (most queries unlabeled)
- Noisy (user preference ≠ quality)
- Feedback loops (bad results → changed behavior → harder to measure)
- Long lag to actionability (need days of data)

#### The Alignment Problem

**Scenario:** Offline metrics improve (retrieval recall +2%, relevance +3%) but user complaints rise.

**Root causes:**
- Judge misalignment (LLM judge drifted; scores no longer correlate with user satisfaction)
- Distribution shift (golden set queries ≠ real traffic; index grew; corpus updated)
- Long-tail regressions (average metrics hide failures in minority query types)
- Feedback loops (users behaved differently after prior poor results; now past behavior is baseline)
- Metric selection (wrong metric for user goals; optimizing the wrong thing)

**Solution:** Continuously correlate offline metrics with online signals. When correlation breaks, reweight metrics, rebaseline judge, or investigate distribution change.

---

## Decision Framework: Offline vs. Online

### What Type of Change?

1. **Code/prompt/model changes?** → Use offline evaluation (deterministic; runs on every PR)
2. **Corpus/index/embedding changes?** → Use online monitoring (distribution shifts; need real traffic)
3. **Query distribution shifting?** → Use online monitoring (stale golden set; rebaseline regularly)
4. **Ongoing health?** → Use online canary (shadow score live traffic; compare vs baseline)

### Which Signals?

| Signal | Offline Use | Online Use |
|--------|---------|----------|
| Retrieval recall@k | PR gate (golden set) | Nightly audit (drift detection) |
| LLM relevance score | CI test (calibrated judge) | Weekly revalidation (judge drift) |
| User satisfaction | Baseline correlation study | Real-time monitoring (North Star) |
| Latency/cost | Shadow canary | Prod monitoring + alerts |
| Critical error rate | Regression test on known cases | Incident playbook + auto-rollback |

### Evaluation Schedule

- **PR gates (fast):** Small golden set; snapshot assertions; flake-controlled; per-component
- **Nightly (broad):** Larger eval set; full pipeline; bucketed analysis; baseline comparison
- **Canary (safe):** Shadow score live traffic; compare to previous version; threshold gates
- **Post-deploy (ongoing):** Continuous monitoring; drift detection; judge calibration refreshes; auto-curation

---

## Common Pitfalls

- **Optimizing to a single average metric** -- hides long-tail failures (recency, multi-hop, jargon)
- **No version pins** -- "it worked yesterday" debugging; can't reproduce failures
- **No negative/adversarial cases** -- offline tests pass; production finds edge cases
- **No calibration for LLM judges** -- judge drift silently; scores change without system changes
- **Offline→online mismatch** -- golden set queries ≠ real traffic (distribution shift)

---

## Interview Q&A

**Q: What does offline evaluation miss that online evaluation catches?**

A: Offline evaluation misses distribution shift (real queries differ from golden set, corpus evolved), long-tail failures (rare but critical edge cases), feedback loops (user behavior changed after poor results), and judge drift (same input, different score over time).

Rubric: 2 = includes shift + long-tail + feedback loop + judge drift.

---

**Q: Design a north-star quality metric for RAG.**

A: A risk-weighted composite of answer relevance (intent satisfied), groundedness (no hallucinations), citation accuracy (claims supported), and critical error rate (unsupported claims, policy violations, refusal failures), reported per-bucket (recency, entity type, jargon level, injection risk).

Rubric: 2 = risk-weighted + bucketed.

---

**Q: When should you use sampling vs. exhaustive labeling in online evaluation?**

A: Use sampling for low-stakes metrics (latency, cost). Use stratified/risk-based sampling for quality metrics (high-stakes queries, high-error buckets sampled more). Use exhaustive labeling for critical error rate (incidents, safety).

Rubric: 2 = stratified + critical error logic.

---

**Q: How do you prevent gold sets from going stale?**

A: Version datasets; retire outdated queries monthly; continuously add production failures (auto-curation); refresh recency-sensitive items frequently; compare golden-set metrics quarterly against live distribution.

Rubric: 2 = versioning + auto-curation + continuous refresh.

---

**Q: Design an offline→online alignment plan.**

A: Correlate offline scores with online signals (satisfaction, deflection, complaints) monthly. If correlation breaks, investigate: judge misalignment (recalibrate), distribution shift (rebaseline), long-tail failure (add test cases), or feedback loop (segment analysis).

Rubric: 2 = correlation + investigation triggers.

---

## Cheat Sheet

**Remember:**
- Bucket everything. Averages hide risk.
- Pin versions for reproducibility.
- Convert incidents into tests (auto-curation).

