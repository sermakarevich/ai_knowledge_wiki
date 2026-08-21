> [[index|Wiki]] | [[digest|Digest]]

# GraphRAG-Bench — Summary

**Paper:** [GraphRAG-Bench: Challenging Domain-Specific Reasoning Benchmark for GraphRAG (Xiao et al., 2025)](https://arxiv.org/abs/2506.02404)

GraphRAG organizes a document corpus as a graph of concepts and relations instead of flat text chunks, on the theory that this lets an LLM traverse explicit relational paths and handle multi-hop questions that plain retrieval can't. But the benchmarks used to prove this — HotpotQA, 2WikiMultiHopQA, MuSiQue — are built from short, commonsense, single-hop-ish questions that the LLM may already know from training, so nobody had actually shown GraphRAG improves *reasoning*.

GraphRAG-Bench closes that gap. It's a 1,018-question benchmark drawn from 20 core computer-science textbooks (7 million words, 16 subfields), extracted through a 4-stage OCR/layout pipeline, with five question types (multiple-choice, multi-select, true/false, fill-in-blank, open-ended) and — critically — an expert-written rationale for every question, so evaluation can score not just "is the answer right" but "is the reasoning right."

Nine GraphRAG methods (RAPTOR, LightRAG, Microsoft GraphRAG, G-Retriever, HippoRAG, GFM-RAG, DALK, KGP, ToG) were run on this benchmark with a shared GPT-4o-mini backend, scored across graph construction cost/speed, retrieval speed, generation accuracy, and a gold-rationale reasoning score (R/AR).

The results are mixed by design, not noise: RAPTOR and HippoRAG top both accuracy and reasoning; DALK and G-Retriever actually make GPT-4o-mini *worse* than not using retrieval at all; GraphRAG hurts Mathematics questions universally and barely moves Ethics; and reasoning quality improves almost everywhere even when raw accuracy doesn't. The headline conclusion: graph augmentation genuinely helps reasoning, but the benefit is method- and domain-specific, not a blanket win — which is exactly the nuance flat-recall benchmarks couldn't have shown.

For the full argument with all tables and numbers, see [[digest|the digest]] or the [[wiki/01-introduction-and-motivation|wiki pages]].
