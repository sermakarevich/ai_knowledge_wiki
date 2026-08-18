> [[index|Wiki]] | [[summary|Summary]]

# Graph Engineering with Kimi K3 — Digest

The whole article at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

> **Terminology note:** "graph engineering" here means knowledge-graph / GraphRAG (facts as triples, queried by relationship path) — not the agent-topology sense (wiring multi-agent loops into a graph) used elsewhere in this research batch.

## 1. [[wiki/01-the-problem-and-what-graph-engineering-is|The Problem, and What Graph Engineering Actually Is]]

**In one sentence:** Standard RAG tops out on multi-hop causal questions because vector similarity finds look-alike text, not connecting facts — whereas "graph engineering" (knowledge-graph / GraphRAG: storing facts as triples and querying relationship paths) answers exactly those questions.

- Standard RAG (question → similar-text retrieval → answer from chunks) breaks the moment a question is complicated, because it can only return fragments, never a chain of causes spread across documents that share no keywords.
- The canonical failure case: "why did our sales drop in March?" — the real answer is a causal chain (release delay → supplier problem → warehouse failure → negative reviews → conversion cut by 23%), and no amount of better embeddings recovers it, since semantic similarity finds documents that look alike, not facts that connect.
- The fix is structural: instead of storing text and searching by similarity, store facts and their relationships as triples (Subject → Relation → Object) and query the paths directly — e.g. "Kimi K3 → developed by → Moonshot AI" and "Warehouse → caused → Supplier delay".
- A vector database stores "this paragraph is about supply chains"; a knowledge graph stores "this specific event caused that specific outcome" — the difference is structural, not cosmetic.
- The graph query is not "what text is similar to my question?" but "walk me the path from A to B and show me every link."
- Microsoft's GraphRAG framing distinguishes **local search** (a node plus its immediate connections, e.g. "What happened with supplier X in July?") from **global search** (patterns across the whole graph, e.g. "What are the recurring risk patterns across all suppliers?").
- Standard RAG handles local-style questions badly and global-style questions not at all; graph engineering handles both.
- The article credits the architecture as independently proven by Microsoft, Stanford, and MIT, and presents Kimi K3 as the best available model to run it.

## 2. [[wiki/02-why-kimi-k3-and-the-model-vs-graph-finding|Why Kimi K3, and the Model-vs-Graph Finding]]

**In one sentence:** Kimi K3 is chosen not because it is the strongest model, but because its 1,048,576-token context window, KDA decoding economics, and Attention Residuals make large-graph queries affordable — while evidence from 26 models shows a good graph consistently beats a bigger model.

- A graph query returns subgraphs, evidence chains, and entity paths — not one paragraph — so the 1M-token context window (1,048,576 tokens) is the architectural point: the entire relevant subgraph fits in a single session, versus most models' 128K–200K windows that force you to truncate the graph before the model sees it.
- Kimi Delta Attention (KDA) is a hybrid attention mechanism that Moonshot reports cuts long-sequence cost to up to 6.3x faster decoding in million-token contexts — the difference between "technically possible" and "affordable to run in production."
- Attention Residuals (AttnRes) selectively retrieves representations across layers instead of accumulating them uniformly, so early context is less degraded when reasoning about late context — e.g., connecting something at position 5,000 to something at position 800,000.
- Honest caveat: Moonshot's own blog states K3's overall performance still trails Claude Fable 5 and GPT-5.6 Sol; K3 is the best model for this architecture, not the strongest model overall.
- A paper comparing 26 open-source models on knowledge-graph engineering tasks found: bigger model + bad graph → worse results; smaller model + good graph → better results. The graph beats the model size, consistently.
- The article name-checks "agent graphs" (Anthropic, LangGraph) as a parallel trend showing the same "structure beats scale" principle — but that is the OTHER, agent-topology sense of graph engineering, not what this article itself is about.
- Three integration modes exist: Mode 1 (KG-enhanced LLM) and Mode 2 (LLM-augmented KG) are one-directional; Mode 3 (Synergized), where the model writes facts into the graph and the graph feeds structured context back, is the recommended one — Modes 1 and 2 are components of it, not alternatives.

## 3. [[wiki/03-the-8-layer-architecture-and-5-prompts|The 8-Layer Architecture and the 5 Pipeline Prompts]]

**In one sentence:** A working knowledge-graph pipeline for K3 is a closed loop of eight narrowly-scoped layers — Ingestion, Extraction, Resolution, Storage, Retrieval, Agent, Verification, Update — driven by five prompts, each with one verifiable job.

- The architecture is eight layers in order: Ingestion → Extraction → Resolution → Storage → Retrieval → Agent → Verification → Update.
- The loop closes at Update (step 8) and restarts at Extraction (step 2) — that recirculation is what makes the graph "compound" rather than a one-pass flow.
- Ingestion is raw material only (PDFs, web pages, databases, APIs, Slack, Notion) with no processing.
- Extraction pulls entities and relationships into structured JSON with per-relation confidence scores and evidence excerpts.
- Resolution is "the layer everyone skips and everyone regrets skipping" — unresolved name variants fragment the graph into duplicates and partial query results.
- Retrieval is five cooperating methods (vector, entity, path, community, temporal), not one; the Agent layer plans, generates Cypher, reads subgraphs, and iterates on gaps.
- Verification is what separates the system from "a very sophisticated hallucination machine" — it checks conclusions against retrieved paths, flags contradictions, and verifies sources.
- Each of the 5 prompts has a narrow, verifiable job: Extraction, Entity Resolution, Query Translation, Grounded Answer, and Graph Maintenance — graph engineering does not replace prompting, it constrains each prompt.

## 4. [[wiki/04-stack-week-one-plan-and-troubleshooting|Stack, Week-One Plan, and Troubleshooting]]

**In one sentence:** This closing chunk lays out the concrete stack (Neo4j + Kimi K3 API + Kimi Code CLI + DSPy), a realistic day-by-day week-one build plan, the failure modes and their fixes once the system is running, and cautions that the widely quoted "85% lower cost, 18% better accuracy" figures are not a universal guarantee — build the graph, the model is the easy part.

- The recommended stack has four moving parts: **Neo4j** as the graph database (best docs, best visualization, genuinely readable Cypher), **Kimi K3** via API as the model (OpenAI-SDK compatible, so integration is a base-URL change), **Kimi Code CLI** as the agent/execution layer (reads and edits files, runs shell commands, supports MCP), and **DSPy** for orchestration if you'd rather program the pipeline than hand-tune prompts.
- Week one is a deliberate, day-by-day ramp: install Neo4j and get Cypher comfortable (Day 1), run extraction on one real document set and inspect what it extracted (Day 2), load the triples and build the simplest retrieval — entity lookup plus one-hop traversal (Day 3), add path search (Day 4), close the loop by letting Kimi Code query the graph and write a fact back over MCP (Day 5), and measure accuracy, token cost, and latency on your own data (Day 6–7).
- The single most common failure is **duplicate entities** — "OpenAI," "Open AI," and "OpenAI Inc." each becoming separate nodes so queries return fragments — and the fix is to run the entity-resolution step (Prompt 2) as a batch job over new entities *before* insertion, not after, because retrofitting resolution onto an already-polluted graph is significantly harder.
- Every other failure has a concrete, prompt-anchored fix: make the Prompt 1 evidence field mandatory (an exact quote or the relationship doesn't go in) to kill invented relationships, pass the *literal* schema into Prompt 3 and validate generated Cypher to stop "everything or nothing" queries, forbid inferring causation from co-occurrence and require the model to cite the specific relationship type it relies on, cap traversal depth to two or three hops to control cost, and run a scheduled maintenance pass (Prompt 5) so entropy doesn't quietly accumulate.
- The "85% lower cost, 18% better accuracy" number floating around is not a universal guarantee — it comes from specific research on specific document sets, and the baseline matters ("cheaper than loading structured files directly into context" is a very different claim than "cheaper than your current RAG"); the *direction* is well-supported, but the *magnitude* is something you measure yourself in week one.
- Standard RAG is "a search engine that writes prose"; graph engineering instead answers *why* and *how are these connected*, gets structurally better with every document, can surface what it doesn't know because graph gaps are visible (vector-store gaps are not), and costs less per useful answer because you retrieve the relevant subgraph rather than stuffing twenty documents into context and hoping.
- The real tradeoff is a week of upfront work — you're building extraction, resolution, storage, retrieval, verification, and maintenance instead of just calling an embedding API — and that week is what separates a demo from a system.
- The conclusion inverts the "reach for a bigger model" instinct: the research consistently shows a smaller model with a well-built graph beats a larger model with poor retrieval, because the system around the model matters more than the model — so build the graph, the model is the easy part.

## The argument in five moves

1. Standard RAG retrieves look-alike text, not connected facts, so it cannot answer causal, multi-hop questions.
2. The fix is structural: store facts as subject→relation→object triples and query relationship paths (Microsoft's local/global search framing) instead of similarity.
3. Kimi K3 is the recommended engine not for raw capability but for context-window economics (1M tokens, KDA, AttnRes) — and a 26-model study shows graph quality beats model size regardless of which model you pick.
4. The architecture is concrete: 8 layers (Ingestion → ... → Update, looping) run by 5 narrow, verifiable prompts (Extraction, Resolution, Query Translation, Grounded Answer, Maintenance).
5. Building it takes a real stack (Neo4j + K3 + Kimi Code + DSPy) and about a week of upfront work, with well-known failure modes (duplicate entities above all) each having a specific fix — and the headline cost/accuracy numbers should be measured on your own data, not assumed.
