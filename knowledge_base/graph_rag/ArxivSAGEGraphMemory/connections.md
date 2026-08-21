> [[index|Wiki]] | [[summary|Summary]]

# Connections

Related entries elsewhere in this knowledge base, organized by relationship to SAGE.

## Direct baselines (compared against in SAGE's own experiments)

- [[ai_papers/graph_rag/ArxivHippoRAG/summary|HippoRAG]] — the neurobiologically-inspired predecessor SAGE compares hardest against (HippoRAG 2 at 45.6/78.0 R@2/5 on NQ vs. SAGE's 82.5/91.6); HippoRAG uses fixed Personalized PageRank propagation over an LLM-extracted graph, exactly the "static index" pattern SAGE's writer–reader co-training is built to move past.
- [[ai_papers/graph_rag/ArxivLightRAG/summary|LightRAG]] — a dual-level (entity + community) GraphRAG baseline in SAGE's Table 9/10 comparisons; LightRAG's graph is built once by LLM extraction with no reader-derived feedback, the same static-construction gap SAGE targets.
- [[ai_papers/graph_rag/ArxivGraphRAGLocalToGlobal/summary|From Local to Global (Microsoft GraphRAG)]] — the foundational hierarchical-community GraphRAG architecture SAGE's "Graph-enhanced RAGs" baseline family (Table 13) descends from; SAGE's Challenge II (structure treated as a fixed index) is a direct critique of this design.

## Same problem, different mechanism (agentic/learned GraphRAG)

- [[ai_papers/graph_rag/ArxivPersonalAI20/summary|PersonalAI 2.0]] — also rejects fixed-index GraphRAG, but by having an LLM plan and adapt its traversal step by step at *query time*, rather than SAGE's approach of RL-training the graph-construction policy itself; complementary axes of "make retrieval adaptive" (PAI-2, query-time) vs. "make the graph itself adaptive" (SAGE, construction-time).
- [[ai_papers/graph_rag/ArxivGraphScout/summary|GraphScout]] and [[ai_papers/graph_rag/ArxivPathRouter/summary|PathRouter]] — both train models to navigate/route over existing graph structure more intelligently (fuzzy search tools; reward-aligned trajectory routing) rather than optimizing the graph-writing process — useful contrast points for isolating how much of SAGE's gain plausibly comes from better *reading* (which these papers also improve) vs. its distinctive better *writing*.
- [[ai_papers/graph_rag/ArxivGraphReasoningAgentGRA/summary|GRA]] and [[ai_papers/graph_rag/ArxivAgentGL/summary|AgentGL]] — agentic graph-navigation systems (unix-style tools; RL-trained traversal) that, like SAGE's reader, use learned policies over graph structure instead of heuristic expansion, but leave graph construction itself unlearned.

## Closest graph-memory-for-agents lineage (same "write + read + evolve" framing)

- [[papers/ArxivMemGraphRAG/summary|MemGraphRAG]] — diagnoses the same upstream problem from a different angle: independent, chunk-isolated extraction produces thematically irrelevant, logically inconsistent, structurally fragmented graphs. Its fix is a shared Three-Layer Global Memory and a multi-agent conflict-detection/resolution society during *construction* — a non-RL, consistency-focused answer to "how do you build a better graph," directly comparable to SAGE's reward-driven answer to the same question.
- [[papers/ArxivGraphPlanner/summary|GraphPlanner]] — applies graph memory to multi-agent *routing* rather than QA retrieval, but shares SAGE's core move of using a live graph (workflow + historical memory graphs, GARNet) as the substrate a trained policy reads from; both papers use graph structure as a persistent, learned decision surface rather than a one-shot index.
- [[papers/ArxivHiGram/summary|HiGram]] — hierarchical graph memory with localized MicroGraphs and single-path evidence selection for cheap, targeted retrieval and rewrite; where SAGE learns *how to write and read* the whole graph via RL, HiGram focuses on hierarchical organization and dependency-aware rewriting of an already-built graph — a candidate architectural addition if SAGE's writer needed to scale to much larger corpora.
- [[papers/ArxivSodaMem/summary|SodaMem]] — an evidence-grounded temporal knowledge graph with provenance tags and a planner–reader retrieval loop; SodaMem's planner–reader split is conceptually close to SAGE's query-planning-plus-propagation reader, but SodaMem is purpose-built for temporal currency/conflict resolution — precisely the kind of memory-*updating* strength that SAGE's own results (Section 5, RQ2) admit it hasn't yet matched on LongMemEval/HaluMem.

## Evaluation and failure-mode context

- [[ai_papers/graph_rag/ArxivGraphRAGBench/summary|GraphRAGBench]] and [[ai_papers/graph_rag/ArxivRAGvsGraphRAG/summary|RAG vs. GraphRAG]] — both establish that GraphRAG's benefit over flat RAG is method- and domain-specific, not universal; useful calibration for reading SAGE's own benchmark selection (it wins big on multi-hop/open-domain, is only competitive on specialized long-term-memory tasks — consistent with this broader finding rather than an outlier).
- [[ai_papers/graph_rag/ArxivGraphRAGUnderFire/summary|GraphRAG Under Fire]] — shows GraphRAG systems are vulnerable to targeted relation-poisoning attacks; SAGE's appendices don't discuss adversarial robustness of the writer's RL training or the reader's structural gates, an open question this paper flags as worth checking against SAGE's design.
- [[ai_papers/graph_rag/ArxivSevenFailurePointsRAG/summary|Seven Failure Points in RAG]] — catalogues recurring RAG failure modes (missing content, wrong specificity, incomplete answers); several map onto the exact challenges SAGE's introduction motivates its design around (Challenge I/II), giving independent, deployment-derived support for the problems SAGE is solving.
