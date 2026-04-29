> **Paper:** [[../summary]] | **Deep dive:** [[../details]]

## Component-Wise RAG Evaluation

The core insight: **end-to-end metrics hide which stage broke**. Component-wise evaluation isolates retriever, reranker, generator, and citation resolver failures so fixes are targeted.

### Pipeline Anatomy

A production RAG system has distinct stages that can fail independently:

```
ingest → chunk → index → retrieve → rerank → prompt-pack → generate → cite
```

Each stage can regress: bad chunking hides good search, good retrieval buried by poor reranking, good evidence misused by generation, correct facts wrongly cited.

**Key principle:** Each stage can regress independently. Your evaluation program must isolate them.

---

## Core Concepts

### Pipeline Stages

1. **Ingest & Chunking:** Raw documents → semantic chunks; failures: inconsistent boundaries, lost metadata, truncation
2. **Indexing:** Chunks → embeddings + metadata; failures: stale index, embedding model drift, missing filters
3. **Retrieval:** Query → top-k candidates; measured by recall@k, precision@k, coverage
4. **Reranking:** Candidates → reordered; measured by win-rate, MRR, downstream grounding
5. **Prompt Packing:** Ranked chunks → context window; failures: truncation, chunk order, cite-ability
6. **Generation:** Context + prompt → answer; measured by relevance, hallucination, constraint-following
7. **Citation Mapping:** Answer claims → chunk IDs; failures: wrong mapping, missing citations, format errors

### Failure Taxonomy

Define a stable label set to triage failures and trend regressions:

- **RETRIEVAL_MISS:** Relevant chunk not in top-k
- **WRONG_EVIDENCE:** Top-k includes irrelevant chunks that mislead
- **EVIDENCE_CONFLICT:** Multiple top-k chunks disagree
- **HALLUCINATION_CLAIM:** Answer claims unsupported by any chunk
- **CITATION_WRONG:** Cited chunk doesn't support the claim
- **CITATION_MISSING:** Claim is supported but uncited
- **FORMAT_FAIL:** Citation format broken (missing ID, bad syntax)
- **REFUSAL_ERROR:** System refuses when it should answer

Use these labels consistently across your eval suite and incident reports.

### Controlled Diffs

To isolate root cause, **change one variable at a time**:

- **Chunker only:** Same query, same index, different chunk boundaries → do chunks matter?
- **Index only:** Same query, same chunker, rebuilt index → did indexing drift?
- **Reranker only:** Same retriever output, different reranking order → does reranking help?
- **Prompt only:** Same chunks, different system prompt → is it a prompt issue?
- **Model only:** Same prompt, different LLM → does model matter?
- **Embeddings only:** Same chunker, different embedding model → embedding drift?

This is how you distinguish "retrieval failed" from "reranking failed" from "generation failed."

---

## Common Pitfalls

- **Optimizing to a single average metric** -- hides long-tail failures in rare query types
- **No version pins** -- cannot reproduce or debug failures; "it worked yesterday" is not debugging
- **No negative/adversarial cases** -- system looks great until production (uncovered claims, injection patterns, jargon confusion)
- **No calibration for LLM judges** -- judge drift silently; scores change without system changes
- **Metrics don't match user pain** -- offline scores improve but tickets rise (judge misalignment, distribution shift, feedback loops)

---

## Decision Framework: Which Component to Score First

1. **Start from user-risk tier:** What errors are unacceptable? (unsupported claims, wrong citations, policy violations, refusal failures)
   - High-risk → measure generation/citation first
   - Coverage-risk → measure retrieval first
   - Ordering-risk → measure reranking first

2. **Pick the evaluation target:** retriever (candidate quality), reranker (evidence ordering), generator (intent satisfaction), citation resolver (claim-to-chunk mapping)

3. **Select a stage-specific metric:**
   - Retriever → recall@k, precision@k, coverage by entity/type
   - Reranker → win-rate (vs baseline), MRR, downstream groundedness impact
   - Generator → relevance (intent satisfaction), groundedness (chain-level hallucination), constraint adherence
   - Citation → accuracy (correct chunk), coverage (all claims cited), format correctness

4. **Plan an isolation experiment:** oracle-context (gold evidence) vs normal retrieval; reranker on/off; prompt-pack variants; different LLMs

5. **Set gates per stage:** block merges on critical errors (unsupported claims); allow minor noise with multi-run medians for noisy stages (LLM generation)

---

## Minimal Evaluation Record

Every eval case must log:

- **Query ID, retrieved chunk IDs** (top-k list), scores per chunk, rerank order, final answer, cited chunks, versions (model, prompt, index, chunker, embeddings)
- **Failure labels** (RETRIEVAL_MISS, HALLUCINATION_CLAIM, etc.)
- **Text hashes** for reproducibility (query hash, chunk hash, answer hash) so failures are pinned even if content evolves

---

## Interview Q&A (Key Questions)

**Q: Why do component-wise evals beat end-to-end-only evals?**

A: End-to-end metrics aggregate failures across stages. A 95% retrieval score + 95% generation score masks a 5% edge case where bad retrieval → good generation can't recover. Component-wise evals isolate which 5% regression causes user impact.

Rubric: 2 = isolation + aggregation + edge case example.

---

**Q: List 6 common RAG failure modes.**

A: Retrieval miss (right chunk not ranked), wrong evidence (distractors ranked high), misled generation (conflicting evidence), unsupported claim (hallucination), missing citation (claim uncited), wrong citation (cited chunk doesn't support claim).

Rubric: 2 = includes retrieval + generation + citation failures.

---

**Q: Design an eval to detect chunking regressions.**

A: Hold model/prompt/index fixed; vary chunker only; measure retrieval recall@k, groundedness, and citation accuracy. If these drop, chunking is broken; if they stay same, chunking is not the cause.

Rubric: 2 = controlled diff + multiple metrics.

---

**Q: What should a golden-set failure gallery include?**

A: Query, retrieved chunks, score breakdown, answer, citations, failure label, trace link. Sort by risk tier (unsupported claims first). Link to incident or regression.

Rubric: 2 = diff vs baseline + taxonomy labels.

---

**Q: How do you prevent "de-bugging by vibes"?**

A: Standardize traces (log versions, evidence, answer, failures with taxonomy), label failures consistently, compare against a baseline diff (not just "it's better"), and pin versions so failures are reproducible.

Rubric: 2 = reproducibility + diffing.

---

## Cheat Sheet

**Remember:**
- Bucket everything. Averages hide risk.
- Pin versions for reproducibility.
- Convert incidents into tests (auto-curation).

