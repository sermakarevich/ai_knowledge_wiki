# RAG Evaluation & Testing in Production (Offline + Online)

**Author:** Lamhot Siagian (@growth.ideology)  
**Published:** February 2026  
**Deep dive:** [[details]]

## Human Readable TL;DR

Imagine you're managing a library that answers questions about books. You need two types of checks: repeatable tests (like verifying the card catalog is correct) and real-world monitoring (like watching if people actually find the answers helpful). This playbook teaches you exactly how to design both. It covers how to measure if your retrieval system finds the right books, if your ranking system orders them well, if your answer generator writes good responses, and how to catch problems before they reach users.

## TL;DR

A production-ready framework for evaluating Retrieval-Augmented Generation (RAG) systems covering component-wise metrics (retrieval, reranking, generation, citation), dual offline/online strategies, LLM-as-judge calibration, regression testing in CI/CD, canary deployments, and drift detection. Includes 120 interview questions, 8 hands-on labs, production case studies, and Python reference implementations for each evaluation approach.

---

## Problem & Motivation

RAG systems have multiple failure modes across distinct stages (retrieval → reranking → generation → citation), and end-to-end metrics hide which component broke. Production systems must:

- **Isolate failures** to the correct stage so fixes are targeted, not speculative
- **Catch regressions** before they reach users via offline gates + regression tests
- **Align offline signals** with real user outcomes (satisfaction, re-queries, incidents)
- **Detect production drift** (corpus changes, embedding shifts, prompt evolution) with online monitoring
- **Calibrate LLM judges** so they reliably score examples consistently and correlate with user feedback
- **Scale evaluation** across retrieval metrics, ranking quality, answer relevance, groundedness, citations, and failure taxonomy

---

## Main Evaluation Dimensions

1. **Component-wise evaluation** -- isolate retriever, reranker, generator, citation resolver
2. **Offline quality metrics** -- precision/recall@k, MRR, nDCG, relevance, groundedness, citation accuracy
3. **Online signals** -- user satisfaction, deflection, complaint rate, re-query rate, incident rate
4. **Offline ↔ Online alignment** -- correlate offline scores with real user outcomes
5. **Evaluation cadence** -- PR gates (fast), nightly (broad), canary (risk-aware), post-deploy (ongoing)
6. **LLM-as-Judge** -- prompt patterns, evidence-only scoring, variance control, calibration sets
7. **Judge meta-evaluation** -- stability, threshold uncertainty, failure modes (leakage, gaming, injection)
8. **Regression testing** -- golden sets, snapshot assertions, flake control in CI
9. **Canary & rollback** -- shadow scoring, threshold gates, automatic rollback on critical errors
10. **Drift detection** -- distribution shifts in queries, corpus, rankings, or model outputs

---

## Key Concepts

### Signal Definition & Failure Taxonomy

- **Failure taxonomy:** RETRIEVAL_MISS, WRONG_EVIDENCE, HALLUCINATION, CITATION_WRONG, CITATION_MISSING, FORMAT_FAIL, REFUSAL_ERROR
- **Isolated evaluation:** change one variable at a time (chunker only, reranker only, prompt only, model only)
- **Controlled diffs:** compare baseline vs. new snapshot with oracle context to root-cause quickly

### Offline vs. Online Strategy

- **Offline:** Powers benchmarking, regression tests, quality gates in CI; requires pinned versions and stable datasets
- **Online:** Catches drift and long-tail failures; uses sampling + risk-based audits + canary cohorts
- **Alignment problem:** Offline may pass but users unhappy; caused by distribution shift, judge misalignment, long-tail failures, or feedback loops

### Retrieval Metrics

- **precision@k, recall@k:** Distractor control (precision) and coverage (recall)
- **MRR, nDCG:** Reward early-ranked evidence; nDCG supports graded relevance
- **Bucketed reporting:** Always report per-bucket metrics (recency, risk tier, entity type, jargon) to detect long-tail risk

### Rerankers & Hybrid Retrieval

- **Candidate generation ≠ reranking:** Reranker can't fix missing chunks; validate first-stage recall first
- **Win-rate:** Fraction of queries where reranker improves evidence ordering
- **BM25 + dense fusion:** Hybrid retrieval reduces tail misses across query types and jargon-heavy domains
- **Latency budgets:** Tiered approach (fast reranker most traffic; strong reranker high-risk queries)

### Answer Relevance Scoring

- **Intent satisfaction:** Does the response answer what the user asked? Includes correctness, completeness, directness, constraint-following
- **Partial credit:** Decompose into required facts; score coverage and correctness separately
- **Over-refusal:** Track refusal rate per bucket; enforce safe-answer patterns to avoid silent failures

### Groundedness & Citation Accuracy

- **Chain-level grounding:** Answer supported by evidence? Track hallucination, unsupported claims, overgeneralization
- **Citation accuracy:** Right chunk mapped to right claim? Detect mismatch, wrong IDs, missing citations, truncation dropping cited content

### LLM-as-Judge

- **Judge patterns:** Few-shot examples, instruction emphasis, evidence-only (block answer replay), chain-of-thought before scoring
- **Variance control:** Calibration sets (known scores), consensus voting, confidence scoring, threshold uncertainty
- **Failure modes:** Leakage (judge sees answer influences score), gaming (spurious pattern matching), injection (adversarial prompt in chunks)

### Judge Calibration

- **Calibration sets:** Anchor scores from human consensus; measure judge stability and threshold uncertainty
- **Reweight if needed:** If correlation breaks online, adjust metric weights or thresholds
- **Continuous calibration:** Weekly judge fine-tuning with fresh production failures

### Regression Testing in CI

- **Golden sets:** Small deterministic test cases; snapshot assertions on retrieval, ranking, generation, scoring
- **Flake control:** Pin model versions, embeddings, corpus snapshot; use mock scoring to avoid judge variance
- **Per-component gates:** Block merges on retrieval/ranking/generation/citation regressions independently

### Canary Evaluation & Rollback Policy

- **Shadow canary:** Score live traffic with new model; compare metrics vs. baseline
- **Thresholds per stage:** Block on critical errors (unsupported claims, refusal spikes, latency); allow minor noise in medians
- **Incident playbook:** Auto-rollback on critical error spike or metrics threshold violation

### Drift Detection for RAG

- **Drift types:** Distribution shift in queries (topic, length, language), corpus changes (new/stale docs), embedding model shift, reranker output shift
- **Signals:** Top-doc distribution changes, retrieval recall drop, reranker win-rate shift, answer generation length/tone shift, citation format changes
- **Auto-curation:** Monitor for stale/new/harmful docs; continuously refresh golden sets and baselines

---

## Study Plans

- **7 days:** Chapters 1-6 (evaluation foundations), then Chapters 10-12 (regression + canary + drift)
- **14 days:** Add Chapters 7-9 (LLM judge, calibration, attacks) + calibration drills + judge reliability benchmarks
- **30 days:** Implement full Python harness with all evaluation stages; publish repository with case studies

---

## Appendices

- **A. Templates & Schemas:** RAG trace record, golden test case, LLM judge output schema
- **B. System Design Interview:** Full capstone prompt + reference architecture diagram + what strong answers include
- **C. Interview Master Bank:** 120 questions covering retrieval, ranking, generation, LLM-as-judge, regression, canary, drift
- **D. Hands-On Labs:** 8 practical exercises (build golden set, retrieval eval with buckets, citation verifier, Oracle-context debug, judge JSON schema, GitHub CI gate, canary simulation, drift probes)
- **E. Rubrics & Quality Gates:** Relevance rubric (1-5), groundedness rubric (chain-level), citation accuracy checklist, critical error definitions, quality gate matrix
- **F. Production Case Studies:** 6 regressions and their fixes (index rebuild, prompt update, embedding upgrade, keyword stuffing, prompt injection, canary failure)
- **G. Glossary:** Practical definitions of RAG concepts

---

## Who This Is For

- **Model Evaluators:** Design and defend evaluation strategies in interviews and production
- **AI QA / Test Engineers:** Build regression test harnesses and canary pipelines
- **Software Development Engineers (SDETs):** Implement evaluation in CI/CD and monitoring systems
- **Hiring managers:** Benchmark evaluator + AI QA competency with 120-question bank

---

## Interview Signals Tested

The playbook aligns with what interviewers assess:

- Can you define a signal and its failure modes?
- Can you design a repeatable offline test AND a monitoring plan?
- Can you debug regressions using traces and controlled diffs?
- Can you justify thresholds and rollback policies with risk tiers?
- Can you spot leakage, gaming, or injection in judge prompts?
- Can you argue why buckets matter (avoid hiding tail risk)?

---

## How to Use This Playbook

1. **For interview prep:** Read relevant chapters, study decision frameworks and rubrics, answer the Q&A (15 per chapter)
2. **For implementation:** Follow the Python reference snapshots; adapt templates to your schema
3. **For production rollout:** Use the case studies to preempt common regressions; follow the canary policy
4. **For team onboarding:** Start with Mini-Labs; pair them with chapters for hands-on learning

