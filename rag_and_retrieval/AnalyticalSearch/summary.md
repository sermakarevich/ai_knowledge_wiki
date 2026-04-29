# Analytical Search

**Paper:** [Analytical Search (Tu et al., 2026)](https://arxiv.org/abs/2602.11581)

## Human Readable TL;DR

Imagine you ask a librarian not just to find books on a topic, but to actually read through thousands of documents, connect the dots, and write you a well-sourced report with a clear conclusion. Today's search engines can find relevant pages (like Google) or generate quick answers (like ChatGPT), but neither can do this kind of deep, evidence-based analytical work at scale. This paper proposes a new type of search engine -- "analytical search" -- designed to decompose complex questions, gather evidence from many sources, reason step by step, and produce verifiable conclusions, much like a research analyst would.

## TL;DR

This position paper introduces **analytical search** as a distinct search paradigm for analytical information needs (trend analysis, causal assessment, multi-document synthesis). It formalizes the problem, differentiates it from RAG, Deep Research, and Agentic Databases, and proposes a four-module system framework (Query, Retrieval, Fusion, Verification) with end-to-end RL-based optimization. The paper is conceptual -- no empirical results are presented.

---

## Problem & Motivation

Analytical information needs -- such as identifying trends, assessing causal impact, or synthesizing evidence across thousands of documents -- are common in law, finance, science, and policy. Current IR paradigms fail to address them:

- **Relevance-oriented ranking** (traditional search) returns documents but leaves all reasoning to the user, optimizing for topical relevance rather than analytical utility.
- **RAG + LLMs** treats everything as naive QA, is limited by small top-k retrieval windows, offers no control over reasoning chains, and lacks evidence traceability.
- **Brute-force LLM processing** is infeasible at corpus scale -- the authors show that using Qwen-32B to scan 10,000 legal documents for "voluntary surrender" instances takes >3 hours on 2 A100 GPUs.

No existing paradigm provides the end-to-end, evidence-governed, verifiable analytical workflow that these tasks demand.

---

## Main Original Ideas

1. **Analytical Search as a New Paradigm** -- Defines analytical search as a standalone paradigm distinct from document ranking, RAG, Deep Research, and Agentic Databases. Three defining properties: conclusion-oriented, complex relevance (analytical utility over topical similarity), and evidence-governed (every claim traceable to sources).

2. **Taxonomy of Analytical Information Needs** -- Categorizes needs into Descriptive (what happened), Predictive (what will happen / causal), and Prescriptive (what should be done), each with distinct reasoning depth and evidence requirements.

3. **Four-Module System Framework** -- Proposes a unified architecture: (1) Query Module for intent extraction and task decomposition; (2) Retrieval Module with recall-first, multi-path routing (Text-to-SQL, sparse, dense); (3) Fusion Module for explicit multi-step reasoning with tool invocation; (4) Verification Module for consistency checking and adaptive backtracking.

4. **Reasoning as Sequential Decision Making** -- Formulates the analytical workflow as an RL problem amenable to GRPO-style optimization, with multi-level reward signals (conclusion correctness, evidence quality, reasoning stability, efficiency).

5. **Dynamic Task-Aware Index Evolution** -- Proposes indexes that adapt from analytical workloads, inducing new database views and enriching document indexes based on usage patterns, creating a feedback loop for long-term analytical intelligence.

6. **Five-Dimensional Evaluation Framework** -- Introduces metrics beyond standard relevance: Conclusion Correctness, Critical Evidence Recall, Logical Consistency, Traceability/Explainability, and Efficiency.

---

## Key Findings

This is a **position/framework paper** with no empirical experiments or benchmarks. The key quantitative data point is motivational:

| Setting | Result |
|---------|--------|
| Model: Qwen-32B, Task: identify "voluntary surrender" in 10K legal docs | >3 hours on 2x A100 GPUs |

The paper's contribution is conceptual: defining the paradigm, differentiating it from related approaches, and laying out the system architecture and research agenda.

**Systematic differentiation from related paradigms:**

| Paradigm | Key Limitation for Analytical Tasks |
|----------|-------------------------------------|
| Document Ranking | Returns documents, not conclusions; user does all reasoning |
| RAG | Small retrieval window; naive QA framing; no reasoning control |
| Deep Research | Maximizes breadth/coverage but lacks structured analytical goals |
| Agentic Databases | Structured data only; query execution, not analysis orchestration |

---

## Suggestions & Future Directions

1. **RL-Based Training Under Underspecified Intent** -- Models must infer latent analytical goals rather than imitate query-answer mappings; long-horizon reasoning stability and sparse/delayed reward signals remain open challenges.

2. **Recall-Oriented Multi-Path Retrieval** -- Balancing recall against downstream efficiency; dynamic rebalancing across retrieval paths as reasoning evolves; aligning heterogeneous results (structured vs. unstructured) into coherent evidence spaces.

3. **Dynamic Index Organization** -- Indexes that evolve from workloads pose risks of overfitting to historical query distributions and increased storage/maintenance costs.

4. **Evaluation Methodology** -- No single gold-standard reasoning path exists for analytical tasks; conclusions are conditionally valid with multiple defensible interpretations; human-in-the-loop expert evaluation may be unavoidable for high-stakes domains.

5. **Benchmark Construction** -- No benchmark datasets for analytical search currently exist; the paper implicitly calls for their development.

**Limitations:** No implementation or prototype is presented. The RL/GRPO training approach and evaluation metrics are proposed but not empirically validated.

---

## Authors & Institutions

Yiteng Tu (Tsinghua University, Quan Cheng Laboratory), Shuo Miao (Tsinghua University), Weihang Su (Tsinghua University), Yiqun Liu (Tsinghua University), Qingyao Ai* (Tsinghua University, Quan Cheng Laboratory)
