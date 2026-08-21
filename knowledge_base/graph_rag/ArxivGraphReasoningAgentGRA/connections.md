> [[index|Wiki]] | [[summary|Summary]]

# Connections

- [[ai_papers/graph_rag/ArxivRAGvsGraphRAG/summary|RAG vs GraphRAG]] — a controlled benchmark finding neither wins outright (RAG for single-hop, GraphRAG for multi-hop); this paper runs the same kind of controlled, same-substrate comparison but pits *agentic navigation* against *full-context serialization* rather than flat RAG against graph RAG, landing on a complementary conclusion: selective access, not structure, drives the gain.
- [[ai_papers/graph_rag/ArxivGraphRAGLinkedInCustomerService/summary|GraphRAG for Customer Service QA]] — a production deployment of a hybrid (intra-ticket + inter-ticket) knowledge graph for support QA, with a similar "structured graph beats flat retrieval" result (MRR 0.522→0.927) but via templated Cypher retrieval rather than an exploratory tool-calling agent; GRA's factory rule-feasibility loop is the more agentic, less deterministic counterpart to LinkedIn's graph-query pipeline.
- [[ai_papers/graph_rag/AgenticGraphRAGRecentScan/index|Agentic GraphRAG — Recent Materials Scan]] — this paper is item 3 in that batch scan's "agents traversing graphs" section; the scan's cross-cutting theme #2 ("agent tooling beats graph schema") is exactly what this paper's RSA ablation demonstrates directly, and sibling papers in the same scan (GraphScout, AgentGL, PathRouter, PersonalAI 2.0) explore the same "agent explores a graph with tools" pattern with RL training or distillation instead of a fixed tool loop.

## External connections (not KB entries)

The paper's own related-work section situates GRA against four lines it does not have KB entries for:
- **ReAct** — the interleaved reason-then-act loop GRA's agent design descends from; ReAct itself left open which tools a given substrate should expose.
- **SWE-agent** — the direct inspiration for GRA's "few generic file-system-like commands suffice for an unfamiliar structure" thesis, transplanted here from code repositories to knowledge graphs.
- **GraphRAG (Microsoft-style)** — contrasted explicitly: GraphRAG builds a graph and community summaries offline and retrieves over that fixed structure, which suits broad thematic questions but doesn't adapt per-question the way GRA's live navigation does.
- **Think-on-Graph and related graph-traversal-primitive work** — cited as giving LLMs node-lookup/neighbor-listing tools, but assuming the graph's vocabulary is already known and that traversal alone answers the question; the paper argues neither holds once tables (not just triples) are part of the substrate.

_No further related entries identified in the KB beyond the three above as of 2026-08-21._
