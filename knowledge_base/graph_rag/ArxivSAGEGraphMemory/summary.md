# SAGE: A Self-Evolving Agentic Graph-Memory Engine for Structure-Aware Associative Memory

**Paper:** [SAGE: A Self-Evolving Agentic Graph-Memory Engine for Structure-Aware Associative Memory (Wang et al., 2026)](https://arxiv.org/abs/2605.12061)

## TL;DR

SAGE treats agent long-term memory as a coupled write–read–evolve problem instead of a fixed-index retrieval problem. A **policy-based memory writer** builds a heterogeneous entity–relation graph from raw text via reinforcement learning (GRPO), rewarded by how well a **Graph-Foundation-Model (GFM) memory reader** can actually recover gold evidence and derive the answer from that graph. The reader itself is structure-aware: it plans the query into associative probes (entities, aliases, relation clues, pseudo-queries) to counter "tip-of-the-tongue" retrieval failures, uses synapse-inspired edge gating to inhibit noisy hub edges while preserving long-distance bridge edges, and separates a graph-specific "context" channel from a cross-graph "schema" channel that stays stable as the graph evolves. Writer and reader are trained in alternating rounds — freeze the reader, RL-train the writer against it; freeze the writer, retrain the reader on the improved graphs — an approximate coordinate-ascent loop with a supporting theory (SNR bounds, retrieval-budget bounds, Lipschitz stability under graph drift) spanning roughly 40 of the paper's 62 pages.

Empirically, SAGE's biggest win is zero-shot transfer: trained only on multi-hop QA data, it reaches 82.5/91.6 Recall@2/5 on Natural Questions, far above HippoRAG 2 (45.6/78.0) and RAPTOR (40.3/68.3), and it is the fastest retriever among the systems compared. On specialized long-term-memory benchmarks (LongMemEval, HaluMem) it is competitive but does not yet beat the strongest purpose-built memory systems (Memobase, Supermemory, MemU) — the authors attribute the gap to memory updating and extraction coverage, not to the core reader/writer mechanism.

## Why it matters

Most GraphRAG systems treat the graph as a fixed index built once by heuristics (chunk → LLM extraction → static graph), then spend all their cleverness on the retrieval trajectory over that frozen structure. SAGE's core bet is that the graph itself is the thing worth optimizing, and that you can do so with a reader-derived reward signal rather than hand-labeled graph quality — closing the loop between "how memory is written" and "how memory is used."

## Reading ladder

1. [[digest|Digest]] (~10 min) — every wiki page's headline and key points, in order.
2. [[explainer|Plain-Language Explainer]] — no jargon, analogy-first.
3. [[index|Wiki hub]] for the full page map (deep, one per source chunk) — start with [[wiki/01-challenges-and-related-work|01]] and [[wiki/02-method-writer-and-reader|02]] for the core method; the appendices ([[wiki/04-appendix-writer-analysis-snr|04]]–[[wiki/07-appendix-additional-results-case-studies|07]]) carry the theory, ablations, and case studies.
4. [[questions|Retrieval Practice]] and [[critical_thinking|Critical Analysis]] once you've read the wiki.
