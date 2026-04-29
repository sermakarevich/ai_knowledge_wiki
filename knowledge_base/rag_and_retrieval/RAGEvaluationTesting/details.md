> **Paper:** [[summary]]

# RAG Evaluation & Testing in Production -- Deep Dive

A comprehensive exploration of production-grade evaluation strategies for retrieval-augmented generation systems, covering offline quality gates, online monitoring, LLM-as-judge calibration, regression testing, canary deployments, and drift detection.

## Sections

| Section | Description |
|---------|-------------|
| [[sections/component-wise-evaluation\|Component-Wise Evaluation]] | Isolate retriever, reranker, generator failures; define signals and failure taxonomy |
| [[sections/offline-online-strategy\|Offline vs. Online Strategy]] | Align repeatable offline tests with real user outcomes; handle distribution shift |
| [[sections/retrieval-metrics\|Retrieval Metrics]] | precision/recall@k, MRR, nDCG, bucketed reporting, RAG-specific constraints |
| [[sections/rerankers-hybrid-retrieval\|Rerankers & Hybrid Retrieval]] | Two-stage candidate generation + reranking; win-rate, latency budgets, BM25+dense fusion |
| [[sections/answer-relevance-scoring\|Answer Relevance Scoring]] | Intent satisfaction, partial credit, over-refusal tracking, constraint-following |
| [[sections/groundedness-citation\|Groundedness & Citation Accuracy]] | Chain-level grounding, hallucination detection, claim-to-chunk mapping |
| [[sections/llm-as-judge\|LLM-as-Judge Prompt Engineering]] | Few-shot patterns, evidence-only scoring, variance control, prompt design patterns |
| [[sections/judge-calibration\|Judge Calibration & Meta-Evaluation]] | Calibration sets, stability measurement, threshold uncertainty, weekly retraining |
| [[sections/judge-failure-modes\|Judge Failure Modes & Attacks]] | Leakage detection, gaming patterns, injection hardening, test suite design |
| [[sections/regression-testing-ci\|Regression Testing for RAG in CI]] | Golden sets, snapshot assertions, flake control, per-component gates, CI integration |
| [[sections/canary-rollback\|Canary Evaluation & Rollback Policy]] | Shadow scoring, threshold gates, automatic rollback, incident playbook |
| [[sections/drift-detection\|Drift Detection for RAG]] | Distribution shift signals, corpus monitoring, auto-curation, continuous rebaselining |

---

## How to Navigate

- **Start with components:** [[sections/component-wise-evaluation]] explains the pipeline anatomy and failure taxonomy
- **Design offline/online:** [[sections/offline-online-strategy]] covers the alignment problem and decision framework
- **Choose metrics:** [[sections/retrieval-metrics]], [[sections/answer-relevance-scoring]], [[sections/groundedness-citation]] show what to measure
- **Build judges:** [[sections/llm-as-judge]], [[sections/judge-calibration]], [[sections/judge-failure-modes]] cover LLM scoring end-to-end
- **Deploy safely:** [[sections/regression-testing-ci]], [[sections/canary-rollback]], [[sections/drift-detection]] cover production rollout and monitoring

## Key Interview Questions by Section

Each section includes interview Q&A with strong answer rubrics. Use these to:
- Prepare for Model Evaluator / AI QA / SDET interviews
- Benchmark team competency
- Design evaluation protocols for your system

## Practical Lab Exercises

Hands-on exercises (8 total) are paired with chapters:
1. Build a golden set in 60 minutes
2. Retrieval evaluation with buckets
3. Citation verifier rules + escalation
4. Oracle-context debugging
5. LLM judge JSON schema
6. CI gate in GitHub actions
7. Canary evaluation simulation
8. Drift monitoring probes

See [[summary#appendices|Appendices]] for lab details.

