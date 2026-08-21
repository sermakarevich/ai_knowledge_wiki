# Agentic GraphRAG — Recent Materials Scan (Feb 21 – Aug 21, 2026)

GraphRAG used with LLM **agents**: agents traversing knowledge graphs, graph-based agent memory, multi-agent shared graphs. All arXiv dates verified against arXiv itself; industry items date-verified where possible (⚠ = date or content verified only via search snippets, fetch blocked).

Companion to [[../GraphRAGTop10Materials/index|GraphRAG Top 10 Materials]] (the canonical/foundational list).

---

## arXiv papers (12, all date-verified)

### Benchmarks & "do we even need the graph"
1. **Do We Still Need GraphRAG? Benchmarking RAG and GraphRAG for Agentic Search** — https://arxiv.org/abs/2604.09666 (2026-04-01). "RAGSearch" benchmark: fixed LLM + retrieval budget across dense RAG, GraphRAG, and iterative agentic search (training-free and RL-trained). Finding: agentic search closes much of the gap, but GraphRAG still wins on complex multi-hop questions and amortizes its graph-build cost over many repeated queries.
2. **Why Neighborhoods Matter: Traversal Context and Provenance in Agentic GraphRAG** — https://arxiv.org/abs/2605.15109 (2026-05-14). Ablations show answer trustworthiness depends on the whole traversal path, not just cited facts — evaluate the retrieval trajectory, not only final sources.

### Agents traversing graphs
3. **Schema-Agnostic Graph Reasoning Agent (GRA)** — https://arxiv.org/abs/2608.15834 (2026-08-16). Agent explores hybrid text+relational KG with 7 generic tools; 88.4% vs 83.3% for stuff-everything-in-context on UFK-M (258 industrial questions) at <⅓ the tokens. Gain comes mostly from step-wise tool use, not graph schema.
4. **GraphScout** — https://arxiv.org/abs/2603.01410 (2026-03-02). Distills large-LLM graph-exploration behavior into Qwen3-4B; +16.7% avg over larger-LLM baselines across 5 KG domains.
5. **AgentGL** — https://arxiv.org/abs/2604.05846 (2026-04-07). RL-trained native graph tools (no text flattening); +17.5% node classification, +28.4% link prediction.
6. **PathRouter** — https://arxiv.org/abs/2606.16409 (2026-06-15). Fixes RL reward hacking in agentic graph retrieval (lucky-shortcut answers, uninformative step rewards); +3.1/+4.9 F1 (3B/7B) over six QA benchmarks.
7. **PersonalAI 2.0** — https://arxiv.org/abs/2605.13481 (2026-05-13). Multi-step query planning over personal KGs; planning module alone +18% (LLM-judged) across NQ/TriviaQA/HotpotQA/2Wiki/MuSiQue/DiaASQ.

### Graph-based agent memory
8. **SodaMem** — https://arxiv.org/abs/2608.08055 (2026-08-08). Temporal KG memory with SUPERSEDES/CONTRADICTS/UPDATES edges (mention vs event vs validity time); 92.8% on LongMemEval-S at ~$0.0016/question.
9. **HiGram** — https://arxiv.org/abs/2608.05095 (2026-08-05). Two-level (topic → memory-unit) graph memory with path-level localization and joint content+link rewrites; better contradiction handling than flat memory graphs.
10. **SAGE** — https://arxiv.org/abs/2605.12061 (2026-05-12). Self-evolving memory graph (writer builds, graph-aware reader feeds signals back); Recall@2/5 of 82.5/91.6 on NQ zero-shot; improves with use.

### Multi-agent + shared graphs
11. **MemGraphRAG** — https://arxiv.org/abs/2606.00610 (2026-05-30). Agent "society" with shared memory during graph extraction fixes fragment-level inconsistency; beats SOTA GraphRAG baselines at comparable cost.
12. **GraphPlanner** — https://arxiv.org/abs/2604.23626 (2026-04-26). Graph-memory-augmented routing of queries to model/role in multi-agent LLMs; +9.3% accuracy while cutting memory 186 GiB → 1 GiB across 14 tasks.

**Follow-up leads (not fully verified):** LegalGraphRAG (2605.28120), EvoGraph-R1 (2607.12764), HAGE (2605.09942), TACTIC-KG (2607.05001); SSRN "A Survey of Agentic GraphRAG".

---

## Industry articles & frameworks (8)

1. **GraphRAG makes AI agents 80% more truthful** (NICD study, Neo4j blog, 2026-07-22) — https://neo4j.com/blog/agentic-ai/study-graphrag-ai-agents-80-percent-more-truthful/ — independent comparison: GraphRAG agents 80% more truthful, attempted 65.3% vs 28.9% of complex questions vs vector-only, better precision+recall, fewer hallucinations.
2. **Graphiti: KG memory for an agentic world** (Zep/Daniel Chalef via Neo4j, 2026-06-04) — https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/ — real-time incremental bi-temporal KG: updates only affected subgraph, hybrid vector+BM25+traversal in <200ms, MCP server for direct agent access.
3. **Temporal KGs for AI agent memory** (Zep, 2026-05-31) — https://www.getzep.com/ai-agents/temporal-knowledge-graph/ — bi-temporal tracking (valid vs ingestion time); superseded facts invalidated, not deleted — the stale-context fix.
4. ⚠ **Cognee 2026 review** (WeavAI, 2026-05-09) — https://weavai.app/blog/en/2026/05/09/cognee-2026-review-graphrag-ontology-ai-memory-layer/ — ECL pipeline + RDF/OWL ontology validation for entity dedup; reviewer-reported 0.93 on HotPotQA.
5. ⚠ **Open-source agent memory framework comparison** (Cognee blog, 2026-05-28) — https://www.cognee.ai/blog/guides/open-source-memory-frameworks-llm-agents — 7 frameworks compared (Cognee/Mem0/Zep/Letta/MemGPT/Graphiti/LangMem); vendor-authored, read rankings skeptically.
6. ⚠ **State of AI Agent Memory 2026** (Mem0, 2026-08-20) — https://mem0.ai/blog/state-of-ai-agent-memory-2026 — 92.5 LoCoMo / 94.4 LongMemEval at ~6.9k tokens/query; documents industry shift away from external graph DBs toward built-in entity linking ("relationships influence ranking but can't be traversed"); names unsolved problems: temporal abstraction at scale, cross-session identity resolution, memory staleness.
7. ⚠ **NODES AI 2026: Agentic GraphRAG — autonomous KG construction and adaptive retrieval** (Neo4j conf talk, Apr 2026) — https://neo4j.com/videos/nodes-ai-2026-agentic-graphrag-autonomous-knowledge-graph-construction-and-adaptive-retrieval-2/ — multi-agent schema inference, conflict resolution, and retrieval-strategy routing derived from observed failure patterns.
8. ⚠ **GraphRAG + MCP as agentic data architecture** (Hyperight, 2026, date unconfirmed) — https://hyperight.com/agentic-data-architecture-graphrag-mcp-2026/ — MCP servers as the standard interface for agents to traverse graphs.

---

## Main themes across the 6 months

1. **The question shifted from "graph vs vector" to "graph vs agentic search."** An RL-trained iterative-search agent closes much of GraphRAG's multi-hop advantage; the graph still wins on complex multi-hop and amortizes over repeated queries (2604.09666).
2. **Agent tooling beats graph schema.** Several results (GRA, PersonalAI 2.0) show the step-wise traversal/planning loop contributes more than graph structure sophistication.
3. **Temporal graph memory went mainstream.** Bi-temporal edges + fact invalidation (Graphiti, SodaMem, Zep) are now the standard answer to stale context.
4. **RL-trained graph traversal is the new frontier** — with its own failure modes (reward hacking on lucky shortcuts) already being patched (PathRouter, AgentGL, GraphScout).
5. **A counter-trend exists:** Mem0 reports the industry partly retreating from full graph traversal to lightweight entity-linking that only influences ranking — simplicity vs capability.
6. **MCP is becoming the agent↔graph interface** (Graphiti, FalkorDB, conference talks).
