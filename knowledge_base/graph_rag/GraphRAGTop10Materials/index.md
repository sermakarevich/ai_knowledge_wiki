# GraphRAG — Top 10 Materials (curated 2026-08-20)

A curated reading list on GraphRAG (graph-based retrieval-augmented generation — building a knowledge graph of entities and relationships from documents, then retrieving from that graph instead of, or alongside, plain text chunks). Selected for three lenses:

1. **System understanding** — what works, what doesn't, complexity, best practices, production nuances
2. **Measured retrieval quality** — recall@k, MRR (mean reciprocal rank), NDCG, EM/F1, golden datasets, LLM-as-judge
3. **Failure modes** — ranking drift, hallucination amplification, stale context/index freshness, missing provenance

All arXiv links verified live on 2026-08-20. Blog links marked ⚠ were confirmed to exist via search but were bot-blocked on direct fetch — verify quotes manually before citing.

---

## The Top 10

### 1. From Local to Global: A Graph RAG Approach to Query-Focused Summarization (Microsoft Research)
- **Link:** https://arxiv.org/abs/2404.16130 · Edge et al., 2024 (v2 Feb 2025)
- **Type:** arXiv paper + reference framework (https://github.com/microsoft/graphrag, ~35.6k stars)
- **Why it's here:** The paper that coined "GraphRAG" and the baseline every later paper compares against. Entity/relationship extraction → knowledge graph → Leiden community clustering → pre-computed community summaries → local search (entity-centric) and global search (map-reduce over communities).
- **Lens coverage:** System description (the canonical architecture). Evaluation is LLM-as-judge win-rates on comprehensiveness/diversity — notably *not* recall@k, which later work criticized.
- **What works / doesn't:** Excellent for corpus-level "sensemaking" questions no single chunk answers; expensive indexing (LLM call per chunk per extraction pass), historically no incremental updates (full rebuild to add documents; `graphrag update` added in v0.4.0+), Leiden defaults need domain tuning. LazyGraphRAG mode defers summarization to query time to slash cost.

### 2. Graph Retrieval-Augmented Generation: A Survey
- **Link:** https://arxiv.org/abs/2408.08921 · Peng et al., 2024
- **Type:** arXiv survey
- **Why it's here:** The standard map of the field. Formalizes the pipeline into three stages — Graph-Based Indexing, Graph-Guided Retrieval, Graph-Enhanced Generation — and catalogues methods, training approaches, benchmarks, and industrial systems.
- **Lens coverage:** System description + a taxonomy of approaches; the fastest way to acquire the field's vocabulary. No empirical results of its own; ages fast.

### 3. HippoRAG + HippoRAG 2 (Ohio State)
- **Links:** https://arxiv.org/abs/2405.14831 (NeurIPS 2024) · https://arxiv.org/abs/2502.14802 (2025)
- **Type:** arXiv papers + open-source repo (OSU-NLP-Group/HippoRAG)
- **Why it's here:** The strongest *measured* graph-retrieval results in the literature. Builds a KG from documents and retrieves via Personalized PageRank (graph algorithm ranking nodes by importance relative to query entities) in a single pass — no iterative retrieval rounds.
- **Measured quality:** Multi-hop QA golden datasets (MuSiQue, 2WikiMultiHopQA, HotpotQA). HippoRAG: up to ~20% accuracy gain, 10–30x cheaper and 6–13x faster than iterative-retrieval baselines. HippoRAG 2: MuSiQue F1 ~44.8 → 51.9; 2Wiki Recall@5 ~76.5% → 90.4%; ~7% over the best embedding retriever on associative-memory tasks.
- **Caveat:** Retrieval quality is bounded by graph-extraction quality — a core GraphRAG failure mode in miniature.

### 4. LightRAG: Simple and Fast Retrieval-Augmented Generation (HKU)
- **Link:** https://arxiv.org/abs/2410.05779 (EMNLP 2025) · https://github.com/HKUDS/LightRAG (~39k stars — most-starred GraphRAG project)
- **Type:** arXiv paper + the most-adopted open-source framework
- **Why it's here:** Fixed Microsoft GraphRAG's two biggest production pain points — indexing cost and no incremental updates — and overtook it in adoption. Dual-level retrieval: vector index over entity/relation descriptions (specific facts) + graph traversal (themes); new documents merge into the existing graph without rebuild.
- **Measured quality:** Recall@2/@5 of 56.8/67.5 on HotpotQA, 52.7/63.8 on 2WikiMultiHopQA ("mix" mode), plus latency/cost benchmarks vs GraphRAG and vector RAG.
- **Production nuances:** Users report ingestion throughput bottlenecks at scale (tens of thousands of docs = hours to days), write-locking serializing parallel work, graph-DB backend becoming the bottleneck, LLM rate limits compounding retries (issues #894, #1648).

### 5. RAG vs. GraphRAG: A Systematic Evaluation and Key Insights
- **Link:** https://arxiv.org/abs/2502.11371 · Han et al., 2025 (academia + industry authors)
- **Type:** arXiv paper — controlled head-to-head comparison
- **Why it's here:** The most rigorous answer to "when is GraphRAG worth it." Unified protocol (same preprocessing, retrieval config, generation settings) — fixing the field's habit of incompatible, cherry-picked setups.
- **Key numbers:** No universal winner. Plain RAG wins single-hop lookup (Natural Questions F1 64.8 vs 63.0 for best graph method); GraphRAG wins multi-hop reasoning (MultiHop-RAG accuracy 70.3 vs 67.0). Hybrid selection between the two consistently beats either alone.
- **Lens coverage:** Explicitly analyzes failure modes, efficiency trade-offs, and evaluation biases — not just leaderboard scores.

### 6. GraphRAG-Bench + "When to Use Graphs in RAG" (companion, ICLR'26)
- **Links:** https://arxiv.org/abs/2506.02404 (benchmark) · https://arxiv.org/abs/2506.05690 (analysis) · code: https://github.com/GraphRAG-Bench/GraphRAG-Benchmark
- **Type:** Golden dataset + systematic analysis
- **Why it's here:** The first benchmark scoring the *whole* GraphRAG pipeline — graph construction quality, retrieval, and generation separately — not just final-answer accuracy. Multi-hop, college-level questions across 16 disciplines and 5 answer formats; also scores logical coherence of the reasoning chain. Nine GraphRAG methods benchmarked.
- **Key finding:** GraphRAG's advantage concentrates in multi-hop/complex reasoning; on simple factoid lookup graph traversal adds latency and can *lower* precision by pulling in tangential context via graph edges (converges with #5).

### 7. Seven Failure Points When Engineering a RAG System
- **Link:** https://arxiv.org/abs/2401.05856 · Barnett et al. (Deakin), CAIN 2024
- **Type:** Peer-reviewed experience report from three production deployments
- **Why it's here:** The canonical retrieval failure-mode taxonomy, and every point applies to GraphRAG: (1) Missing Content — answer not in the KB but the system answers anyway; (2) Missed Top-Ranked Documents — right doc exists but falls below the top-k cutoff (classic ranking drift); (3) Not in Context — retrieved but dropped during consolidation/truncation; (4) Not Extracted — in context but the model misses it amid noise; (5) Wrong Format; (6) Incorrect Specificity; (7) Incomplete.
- **Key lessons:** Real-world robustness is only validated against live traffic, not lab evals; robustness evolves through iteration, not upfront design.

### 8. RAG robustness & hallucination-amplification cluster: RGB benchmark + GraphRAG under Fire
- **Links:** RGB: https://ojs.aaai.org/index.php/AAAI/article/view/29728 (AAAI 2024) · GraphRAG under Fire: https://arxiv.org/abs/2501.14050 · (see also CHARM on cascading hallucination in agentic RAG: https://arxiv.org/abs/2606.04435)
- **Type:** arXiv/AAAI papers
- **Why it's here:** Covers how retrieval errors become generation errors. RGB measures four capabilities — noise robustness, negative rejection (saying "I don't know" when retrieval fails), information integration, counterfactual resistance — and finds LLMs consistently weak when retrieved context is distracting or partially wrong. GraphRAG under Fire shows graph structure resists standard corpus poisoning better than vector RAG, but shared relations open a *new* attack surface: GragPoison hits up to 98% attack success with less poison text. CHARM formalizes cascading hallucination — an early retrieval error becoming an intermediate "fact" later steps build on.
- **Lens coverage:** Hallucination amplification, noise robustness, adversarial failure modes.

### 9. Evaluation tooling: ARES + RAGBench + the RAGAS/TruLens/DeepEval landscape
- **Links:** ARES: https://arxiv.org/abs/2311.09476 (NAACL 2024) · RAGBench/TRACe: https://arxiv.org/abs/2407.11005 · RAGAS: https://github.com/explodinggradients/ragas · DeepEval: https://github.com/confident-ai/deepeval · TruLens: https://github.com/truera/trulens
- **Type:** Papers + open-source eval frameworks
- **Why it's here:** The LLM-as-judge toolbox you'd actually use. ARES fine-tunes lightweight judges on synthetic data and corrects judge error with prediction-powered inference over a few hundred human labels; generalizes across domain shift and outperforms RAGAS as a scorer. RAGBench (100k examples, 12 datasets, 5 domains) introduces TRACe (Utilization, Relevance, Adherence, Completeness) — and finds a fine-tuned 400M DeBERTa *beats* GPT-4-class LLM judges at hallucination detection.
- **Critical gap:** None of these frameworks ship graph-native metrics — no entity-linking correctness, path/traversal quality, or community-summary faithfulness. They treat graph-retrieved context as flat text. If you evaluate GraphRAG today, you assemble this yourself.

### 10. Production reality cluster: LinkedIn deployment + cost cliff + incremental-update problems
- **Links:** LinkedIn customer-service GraphRAG: https://arxiv.org/abs/2404.17723 · ⚠ "The GraphRAG Cost Cliff" (Medium/Graph Praxis): https://medium.com/graph-praxis/the-graphrag-cost-cliff-how-33-000-became-33-in-eighteen-months-be1b0fbe37e4 · ⚠ Incremental entity-resolution problems: https://dev.to/hannune/incremental-graph-updates-for-corporate-knowledge-graphs-three-problems-batch-pipelines-cant-solve-2phm
- **Type:** Industry paper + practitioner write-ups
- **Why it's here:** The best production numbers and gotchas in one place.
  - **LinkedIn** (customer-service QA over ticket KG): **+77.6% MRR** and **−28.6% median issue-resolution time** in production — one of the few deployments reporting retrieval-ranking metrics from live traffic. Practitioner caveat: ~2–3x the engineering effort of plain RAG (12–16 weeks vs 6–8).
  - **Cost cliff:** indexing ~5GB of legal documents with Microsoft GraphRAG cost ~$33,000 in LLM calls in early 2024; optimizations (cheaper models, batching, LazyGraphRAG-style deferral) cut the same job to ~$33 within 18 months.
  - **Stale context / entity resolution:** batch pipelines dedupe entities using blocking keys computed over the *whole* corpus; incremental updates lose that global visibility, so the same real-world entity re-enters as duplicate nodes. This is the mechanism behind graph staleness and drift in production.

---

## Cross-cutting conclusions

1. **GraphRAG's benefit is conditional, not general.** Three independent sources (#5, #6, and practitioner write-ups) converge: graphs pay off when *the structure is the answer* (multi-hop reasoning, corpus-level themes) and are overkill — sometimes precision-harmful — for single-fact lookup. Hybrid vector+graph selection beats either alone.
2. **The metric stack is borrowed, not native.** Retrieval is measured with recall@k/F1/EM on multi-hop golden sets (HotpotQA, MuSiQue, 2WikiMultiHopQA); generation with RAGAS-style faithfulness/relevance. Nothing standard yet scores graph-path correctness, entity-linking quality, or community-summary faithfulness. Numbers across papers are self-reported with differing chunking/@k definitions — directional, not comparable.
3. **Cost is a first-class evaluation axis.** Indexing cost varies ~1000x depending on implementation choices ($33k → $33); incremental-update support is what separated LightRAG's adoption curve from Microsoft's original.
4. **Failure modes compound.** Extraction errors bound retrieval quality (HippoRAG caveat) → ranking misses feed noise to the generator (Seven Failure Points) → LLMs are bad at rejecting noisy context (RGB) → in multi-step systems errors cascade into confident hallucination (CHARM). Provenance (LineageRAG-style fact-to-source tracing) and negative rejection are the counters.
5. **LLM-as-judge is useful but not ground truth.** A fine-tuned 400M classifier beat GPT-4-class judges at hallucination detection (RAGBench); ARES-style human-anchored calibration is the safer pattern.

## Honorable mentions

- **Think-on-Graph / ToG 2.0** (https://arxiv.org/abs/2307.07697, ICLR 2024) — LLM-as-agent beam search over a KG; traceable reasoning paths, SOTA on 6/9 KGQA sets, but LLM-call heavy.
- **Graphiti/Zep** (https://github.com/getzep/graphiti) and **Cognee** (https://github.com/topoteretes/cognee) — the agent-memory branch of GraphRAG; Graphiti's bi-temporal edges handle fact invalidation (the stale-context problem) natively; Cognee ships the strongest built-in eval story (DeepEval partnership, 45x repeated runs to control judge variance).
- **LineageRAG** (https://arxiv.org/abs/2608.16004, Aug 2026) — traces every retrieved fact to exact source text; measurable R@5/EM/F1 gains; directly addresses missing provenance.
- **MissDiag** (https://arxiv.org/abs/2608.18489, Aug 2026) — decomposes KG-RAG failures by missing-evidence type instead of one aggregate score.
- **"The Commercial Tax"** (https://arxiv.org/abs/2608.16096, Aug 2026) — audits multi-hop benchmarks; top scores often depend on non-commercially-licensed embeddings; real GraphRAG deployment costs vary 11x for equivalent workloads.
- **LlamaIndex Property Graph Index** and **neo4j-graphrag-python** — the "build on your existing stack" framework options; more assembly required but inherit mature ecosystems.

*Recent-arxiv scan (last 7 days) details: `/Users/sergii/papers/arxiv-scan-2026-08-20.md`.*
