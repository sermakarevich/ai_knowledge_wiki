> [[../../index|Research]] | [[../../overview|Overview]] | [[../../digest|Digest]]

# memory and recall substrate

**In one sentence:** The sources jointly establish that agent memory works best as a durable, inspectable substrate — layered or file-shaped stores of facts, skills, and experience — retrieved through hybrid (BM25 + vector + graph) scoped recall rather than flat chat replay or pure vector search.

## Key points
- Layered distillation is the dominant representation: distilled L0 conversation → L1 atom → L2 scenario → L3 persona assets in TencentDB, and L0 abstract → L1 overview → L2 full content per directory in OpenViking, both so agents judge relevance before loading full text [[research_topics/agent_memory/TencentDBAgentMemory/summary|TencentDBAgentMemory]] [[research_topics/agent_memory/OpenViking/summary|OpenViking]].
- Hybrid recall beats single-method retrieval: BM25 + vector + RRF with budget caps (TencentDB), four-strategy fan-out (semantic, BM25, graph, temporal) plus fusion and cross-encoder reranking (Hindsight), and BM25/vector/graph fusion weights (Agentmemory) are all attested as the recall core [[research_topics/agent_memory/TencentDBAgentMemory/summary|TencentDBAgentMemory]] [[research_topics/agent_memory/Hindsight/summary|Hindsight]] [[research_topics/agent_memory/Agentmemory/summary|Agentmemory]].
- Markdown files are the inspectability substrate: session commits extract editable Markdown memories (OpenViking), an agent-maintained Markdown skill wiki is the whole store (MemU), and Obsidian `Brain/*.md` files with git history replace any daemon or black-box store (OpenSecondBrain) [[research_topics/agent_memory/OpenViking/summary|OpenViking]] [[research_topics/agent_memory/MemU/summary|MemU]] [[research_topics/agent_memory/OpenSecondBrain/summary|OpenSecondBrain]].
- Scoped, permissioned recall replaces global vector pools: subtree-scoped `find`/`search`/`grep` over `viking://` (OpenViking), `bank_id` tenancy over every retain/recall/reflect call (Hindsight), and `private`/`team`/`restricted` plus User/Role/Agent ACLs on versioned assets (TencentDB) [[research_topics/agent_memory/OpenViking/summary|OpenViking]] [[research_topics/agent_memory/Hindsight/summary|Hindsight]] [[research_topics/agent_memory/TencentDBAgentMemory/summary|TencentDBAgentMemory]].
- Learning (consolidated facts, skills, mental models) is positioned against replay: Hindsight stores world facts, experience facts, and mental models rather than transcripts; TencentDB distills executable Skills and CodeGraph impact paths; MemU keeps judgment in the agent and the service embedding-only [[research_topics/agent_memory/Hindsight/summary|Hindsight]] [[research_topics/agent_memory/TencentDBAgentMemory/summary|TencentDBAgentMemory]] [[research_topics/agent_memory/MemU/summary|MemU]].
- Local-first, zero-external-DB operation is viable with opt-in upgrades: keyless BM25 with optional on-device embeddings and LLM compression (Agentmemory), embedding-only service with SQLite/Postgres backends (MemU), and vault-native files with an optional vector lane (OpenSecondBrain) [[research_topics/agent_memory/Agentmemory/summary|Agentmemory]] [[research_topics/agent_memory/MemU/summary|MemU]] [[research_topics/agent_memory/OpenSecondBrain/summary|OpenSecondBrain]].
- Reported benchmark lifts exist but are vendor-reported: LoCoMo 80–83% memory accuracy with 34–91% fewer input tokens (OpenViking), LongMemEval SOTA reproduced by third parties (Hindsight), and claimed 95.2% R@5 with 92% fewer tokens (Agentmemory) [[research_topics/agent_memory/OpenViking/summary|OpenViking]] [[research_topics/agent_memory/Hindsight/summary|Hindsight]] [[research_topics/agent_memory/Agentmemory/summary|Agentmemory]].

---
## What the sources agree on
- Flat chat history and single-method vector retrieval are insufficient; every source adds structure (layers, files, banks, ACLs) and hybrid or scoped retrieval on top.
- Memories must be inspectable and editable by humans (Markdown files, wiki pages, review flows, vault grep/git), not opaque embeddings.
- Recall should be scoped (subtree, bank, team, visibility boundary) and budgeted (tiers, token caps, L0-first scanning) rather than loading everything.
- Capture and recall are separate seams: proxy/hooks/bridging-tasks record experience, while retrieve/search/reflect inject it later, often across agents and sessions.

## Where they differ
- LLM dependence: Hindsight requires an LLM on every retain/recall/reflect path, while MemU forbids any LLM call in the service and Agentmemory runs keyless BM25 by default with LLM compression doubly opt-in.
- Store shape: relational + pgvector banks (Hindsight), virtual filesystem with generated summaries (OpenViking), versioned team asset hub with Wiki + CodeGraph (TencentDB), file-backed SQLite observation store (Agentmemory), shared skill wiki (MemU), Obsidian vault files with no daemon (OpenSecondBrain).
- Governance vs simplicity: TencentDB and OpenSecondBrain invest in ACLs, visibility boundaries, write records, and hash chains; MemU and Agentmemory trade governance for a ~500-line core or a single shared local server.
- Recall machinery weight: Hindsight's four-strategy fan-out with reranking is the heaviest; OpenViking's scan-before-read tiers and MemU's progressive retrieval are the lightest.

## Evidence quality
- Strongest on architecture and API surface: all six summaries ground store shapes, CLI/API calls, and retrieval stages in file:line citations from READMEs and configs.
- Benchmark claims are uneven: OpenViking and Hindsight name harnesses (LoCoMo, tau2-bench, LongMemEval) with versions and reproduction notes; Agentmemory's R@5/token figures are snapshot claims with version discrepancies noted; TencentDB, MemU, and OpenSecondBrain make no quantitative recall claims.
- Coverage gaps are explicit: several summaries note truncated wikis and unmapped internals (`src/`, engine modules, provider lists), so function-level and ranking-formula claims are absent rather than verified.

## Sources in this sub-topic
| source | kind | what it contributes |
|---|---|---|
| TencentDBAgentMemory | fresh | L0→L3 Chat Memory, Skills, Wiki, CodeGraph assets with BM25+vector+RRF recall and team ACL governance |
| OpenViking | fresh | `viking://` context filesystem with L0/L1/L2 scan-before-read tiers and subtree-scoped find/search/grep |
| Agentmemory | fresh | Local-first shared memory server over MCP/hooks/REST with keyless BM25 and opt-in embedding/LLM upgrades |
| Hindsight | fresh | Retain/recall/reflect loop over bank-scoped world/experience facts and mental models with four-strategy fused retrieval |
| MemU | fresh | Embedding-only skill-wiki substrate with record/inject seams and agent-side judgment |
| OpenSecondBrain | fresh | Vault-native Obsidian Markdown store with deterministic CLI/MCP access, visibility boundaries, and attributable writes |
