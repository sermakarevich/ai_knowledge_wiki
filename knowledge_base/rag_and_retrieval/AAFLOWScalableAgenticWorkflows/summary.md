# AAFLOW: Scalable Patterns for Agentic AI Workflows

**Paper:** [AAFLOW: Scalable Patterns for Agentic AI Workflows (Sarker et al., 2026)](https://arxiv.org/abs/2605.02162)

## Human Readable TL;DR

Imagine you're running a very busy library where robots fetch books (retrieve), read and summarize them (reason), and file new ones (upsert). Current robot management systems are slow because every book gets wrapped and unwrapped in plastic each time it changes hands. AAFLOW redesigns the whole library so books flow hand-to-hand without wrapping, robots work in organized assembly lines instead of wandering freely, and the entire operation runs like a factory floor rather than an improvised relay race. The result: the same work gets done nearly twice as fast overall, and up to 24 times faster for heavy filing tasks.

## TL;DR

AAFLOW is a unified distributed runtime for agentic LLM workflows that models RAG pipelines as a composition of five formal operators (embed, retrieve, reason, memory, upsert), each mapped to explicit distributed communication patterns. It eliminates serialization overhead via a zero-copy data plane built on Apache Arrow and Cylon, and decouples agent logic from physical scheduling for reproducible execution. Benchmarks show up to 4.64x ingestion speedup over Dask-based baselines and 1.88x end-to-end speedup over LangChain/LangGraph, with 93.8% latency reduction in hybrid retrieval.

---

## Problem & Motivation

Modern LLM agentic workflows (RAG pipelines, multi-step reasoning) chain together retrieval, embedding, memory, and tool invocation on distributed infrastructure. Two fundamental problems emerge:

1. **Data orchestration bottlenecks** -- document chunking, embedding, indexing, and vector retrieval require massive data movement. Frameworks like Dask and Spark incur heavy serialization, object-management, and fragmentation overhead.
2. **Execution non-determinism** -- LangChain/LangGraph delegate control flow to LLM decisions, producing dynamic execution paths that are hard to replicate, profile, or optimize in HPC environments.

No single existing solution covers both: agentic frameworks optimize reasoning flexibility while ignoring data costs; distributed data systems optimize throughput for static workloads. The result is disjointed, hard-to-scale architectures.

---

## Main Original Ideas

1. **Agentic Operator Algebra** -- Five operators formalize every agentic action: `Op_embed` (embarrassingly parallel batched map), `Op_retrieve` (shuffle-compute with distributed top-k), `Op_reason` (reduction to merge context), `Op_memory` (broadcast/exchange for state), `Op_upsert` (shuffle-reduce into partitioned indices). Each has an explicit communication pattern, enabling static analysis and optimization.

2. **Zero-Copy Distributed Data Plane** -- Apache Arrow provides a columnar in-memory format shared without serialization across all pipeline stages. Cylon acts as the distributed dataframe substrate supporting MPI, UCX, GLOO, and InfiniBand. No data is ever converted between framework containers.

3. **Resource-Deterministic Scheduling** -- Agent logic (what to retrieve/reason about) is decoupled from physical execution (which worker, which partition, which batch). Workloads are expressed as batched operator schedules compiled before runtime, enabling reproducible traces and predictable latency.

4. **Compiled DAG Execution** -- An agentic workflow is compiled into a DAG with resource domains assigned per operator (CPU partitions for preprocessing, batched workers for embedding, distributed FAISS shards for retrieval), ensuring the physical plan is fixed and communication-aware.

5. **Dual-Path Memory-Aware Retrieval** -- Retrieval queries both a persistent knowledge index and a hierarchical memory index (long-term summaries, intermediate artifacts, short-term state), merged via weighted ranking (semantic score + source type + recency).

6. **Asynchronous Batched Ingestion Engine** -- Load → Transform → Embed → Upsert stages run as non-blocking, stage-local worker pools connected by bounded queues, overlapping computation to mask latency and amortize fixed overheads.

---

## Key Findings

### End-to-End RAG Pipeline vs. Agentic Frameworks

| Framework | Total (s) | Embed (s) | Upsert (s) | Speedup vs. AAFLOW |
|-----------|-----------|-----------|------------|-------------------|
| **AAFLOW** | **0.875** | **0.486** | **0.049** | -- |
| LangChain | 1.645 | 1.13 | 0.13 | 1.88x slower |
| LangGraph | 1.614 | 1.14 | 0.13 | 1.84x slower |
| CrewAI | 1.626 | 1.15 | 0.14 | 1.86x slower |
| AutoGen | 1.614 | 1.13 | 0.13 | 1.84x slower |

### Hybrid Parallel Ingestion (10M chunks, 4096 files, 16 workers)

| System | Total (s) | Speedup |
|--------|-----------|---------|
| **AAFLOW** | **3.487** | -- |
| HigressRAG | 4.439 | 1.28x slower |
| AsyncParallelOnly | 11.641 | 3.34x slower |
| DaskScalableRAG | 16.188 | 4.64x slower |
| RayScalableRAG | 84.136 | **24.12x slower** |

### Retrieval & Reasoning Latency vs. HigressRAG

| Scenario | HigressRAG (ms) | AAFLOW (ms) | Reduction |
|----------|-----------------|-------------|-----------|
| LLM Generation | 68.23 | 28.12 | **58.8%** |
| Non-Cached Complex Queries | 70.31 | 30.18 | **57.1%** |
| Hybrid Retrieval | 21.45 | 1.33 | **93.8%** |
| Semantic Cache Lookup | 0.03 | 0.03 | ~0% |

### Scaling
- **Strong scaling:** Latency drops from 30.9s (128 workers) to 4.5s (1024 workers), near-linear until compute-bound.
- **Weak scaling:** Latency increases from 3.1s to 5.2s as load and workers scale proportionally -- shallower degradation than all baselines.
- Total execution time < sum of stage times, confirming effective latency masking via async overlap.

### Key qualitative findings
- All gains come from data flow, batching, and communication efficiency -- not from faster LLM token generation (throughput held constant across systems).
- Semantic cache lookup is framework-agnostic; AAFLOW does not change caching behavior.

---

## Suggestions & Future Directions

1. Extend the operator algebra to support dynamic, multi-turn agentic workflows where execution graphs may change at runtime based on intermediate LLM outputs.
2. Integrate with LLM serving runtimes (e.g., vLLM, SGLang) to co-optimize inference acceleration alongside data pipeline efficiency.
3. Evaluate AAFLOW on real scientific computing workloads (genomics, climate modeling) where HPC integration is most impactful.
4. Explore adaptive scheduling policies that can re-compile execution DAGs mid-workflow when resource availability changes.
5. Investigate fault-tolerance mechanisms for long-running agentic workflows on large HPC clusters.
6. Extend zero-copy data plane support to GPU memory to reduce CPU-GPU transfer overhead for embedding-heavy workloads.

---

## Authors & Institutions

Arup Kumar Sarker (University of Virginia), Mills Staylor (University of Virginia), Aymen Alsaadi (Rutgers University), Gregor von Laszewski (University of Virginia), Shantenu Jha (Rutgers University / Princeton Plasma Physics Laboratory), Geoffrey Fox (University of Virginia)
