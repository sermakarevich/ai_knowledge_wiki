# Agent Memory

Research on **persistent memory systems for agents** — short-term context management, cross-session memory, associative/graph memory, and cross-domain memory transfer.

## Papers

- [[AIMeetsBrain/summary]] — Unified survey bridging cognitive neuroscience and AI agent memory; proposes episodic/semantic × inside-trail/cross-trail taxonomy, maps biological to artificial storage lifecycles, and covers memory security threats.
- [[ArtifactsAsMemoryBeyondAgentBoundary/summary]] — Formalizes environmental artifacts as external agent memory in RL; proves the Artifact Reduction Theorem showing observable traces lower required internal capacity, validated with Q-learning and DQN in maze tasks.
- [[CodexMemories/summary]] — OpenAI Codex opt-in local memory persists preferences and project conventions in `~/.codex/memories/`.
- [[GaamaGraphAugmentedAssociativeMemoryForAgents]] — Hierarchical KG with concept-mediated nodes + hybrid PageRank+semantic retrieval; 78.9% LoCoMo-10.
- [[MemCollab]] — Contrastive trajectory distillation between heterogeneous agents; Qwen-7B 57.1%→71.6%.
- [[MemFactory/summary]] — Unified training + inference framework for memory-augmented agents with modular Extractors/Updaters/Retrievers; GRPO-based RL training yields 7–15% gains on long-context tasks, single-GPU.
- [[MemSearchO1/summary]] — Replaces cumulative context with seed-anchored memory fragments + path retracing; +21.9% F1.
- [[MementoTeachingLlmsToManageTheirOwnContext/summary]] — Trains LLMs to compress reasoning blocks into dense summaries; 2-3x KV cache reduction.
- [[MemoryIntelligenceAgent]] — Manager-Planner-Executor architecture with bidirectional memory (parametric + non-parametric); +5.5-7.5 points on 11 benchmarks.
- [[MemoryInTheAgeOfAIAgentsSurvey/summary]] — Comprehensive survey proposing the Forms–Functions–Dynamics (FFD) taxonomy to unify fragmented agent memory research; classifies memory by storage form, functional role, and lifecycle process across 200+ systems.
- [[MemoryTransferLearning/summary]] — Cross-domain memory transfer works at high abstraction (Insights) not raw traces; abstract meta-knowledge travels.
- [[RethinkingAgentMemory/summary]] — Comprehensive survey proposing a three-dimensional taxonomy (substrate × cognitive mechanism × subject) for foundation agent memory; synthesizes 218 papers and outlines six open directions for real-world deployment.
- [[StatelessDecisionMemory/summary]] — DPM replaces incremental summarization with an append-only event log + single temperature-0 projection at decision time; 7–15× faster, deterministically replayable, outperforms stateful memory at tight budgets (+0.515 FRP).
- [[StructMem/summary]] — Hierarchical memory organizes events with dual-perspective (factual + relational) extraction and periodic cross-event consolidation; 76.82% on LoCoMo, ~18x fewer tokens than graph-based baselines.
- [[MemoryMechanismLLMAgents/summary]] — First comprehensive survey of LLM agent memory; unified taxonomy of sources, forms, and operations; highlights parametric memory underexploration and multi-agent coordination as key open challenges.
- [[OcrMemory/summary]] — Stores LLM agent interaction histories as compressed visual images (~10× token compression); Locate-and-Transcribe OCR retrieval achieves 100% faithfulness on Mind2Web and AppWorld long-horizon benchmarks.
- [[ContextualAgenticMemoryIsAMemo/summary]] — All deployed agent "memory" is context engineering, not parametric learning; proves Ω(k²) vs O(d) compositional complexity gap and shows persistent memory creates structurally worse cross-session attack surfaces.
- [[MemEvolve/summary]] — Meta-evolutionary framework jointly evolves accumulated experience and memory architecture (Encode/Store/Retrieve/Manage); diagnose-and-design outer loop yields up to 17% gains with cross-task/LLM/framework transfer.
- [[GraphBasedAgentMemory/summary]] — First comprehensive survey of graph-based agent memory; unifies all memory types as graph special cases and organizes the field around a four-stage lifecycle (extraction, storage, retrieval, evolution).
- [[AnatomyOfAgenticMemory/summary]] — Structure-oriented taxonomy of memory-augmented generation plus empirical critique: benchmarks are underscaled (context saturation), F1/BLEU misalign with semantics, results are backbone-dependent, and maintenance imposes a hidden "agency tax."
- [[TheAIHippocampus/summary]] — Brain-inspired three-tier memory taxonomy (implicit/explicit/agentic ≈ neocortex/hippocampus/prefrontal cortex) for LLMs/MLLMs; benchmarks six frameworks, finding simple RAG (ChromaDB) matches complex systems on single-session tasks.
- [[AgentMemoryElasticsearch/summary]] — Persistent agent memory on Elasticsearch split into episodic/semantic/procedural indices; hybrid retrieval (BM25+dense, RRF) + rerank with time-decay scoring, server-side DLS tenant isolation; R@10 0.89, 0 leaks.
- [[DoesAIRememberMemoryAgenticWorkflows/summary]] — Survey tracing agent memory from 1987 SOAR through Generative Agents to ChatGPT's vector-embedding memory mode; maps semantic/episodic/procedural taxonomy and raises AI's erosion of human memory agency.
- [[TheMemoryCurse/summary]] — Expanding LLM agent context/history length degrades cooperation in 18/28 model-game settings; caused by collapse of forward-looking reasoning, not paranoia, and fixable via memory sanitization or LoRA fine-tuning.
- [[ZeroMem/summary]] — Eliminates all LLM calls from memory operations via non-generative entity-context graph + four-level temporal hierarchy over raw traces; beats GAM by ~5 F1 with zero memory-operation tokens.
- [[Swarmvault/summary]] — Local-first LLM wiki compiling docs, code, and transcripts into a markdown wiki plus queryable typed graph, offline by default.
- [[OpenViking/summary]] — Open-source context database exposing knowledge, memory, and skills as browsable viking:// filesystem with layered summaries for token-efficient scoped retrieval.
- [[TencentDBAgentMemory/summary]] — Shared Memory Hub + proxy turning conversations, docs, and code into versioned, permissioned team assets with zero-code agent integration.
- [[OpenSecondBrain/summary]] — Obsidian-native agent memory storing preferences, signals, and audit trails as plain Markdown under Brain/ with deterministic CLI/MCP access.
- [[ClaudeObsidian/summary]] — Local-first Agent Skills package keeping Obsidian vault as plain Markdown with provenance ledgers, content-addressed sources, and single-transaction mutation discipline.
- [[SageWiki/summary]] — Single Go binary compiling docs into Obsidian wiki plus evidenced knowledge graph, served to agents via MCP and humans via TUI/web.
- [[CogSecondBrain/summary]] — Convention-based second brain: versioned Obsidian vault operated by 33 agent skills, 6 workers, and 4 verifiers with Git persistence.
- [[AgentSecondBrain/summary]] — Telegram-fronted second brain filing voice and text into a self-hosted Obsidian vault via one persistent Claude session, with decaying typed knowledge graph, on flat subscription cost.
- [[Chubbyskills/summary]] — Set of 14 Agent Skills plus unified CLI collecting video, podcast, and article material into local Markdown with search and sourced evidence-pack export.
- [[SecondBrainCloudflare/summary]] — Self-hosted shared memory layer on Cloudflare Worker + D1/Vectorize serving all AI clients via MCP/REST with Personal/Shared tenancy.
- [[Mateclaw/summary]] — Self-hosted agent runtime running digital employees with provider failover, wiki knowledge, workspace memory, and durable Goals/Team Runs in one deployment.
- [[DocsAgent/summary]] — Local-first Zotero MCP server pairing resident C++ BM25 engine (~15 ms) with 8 MCP tools for ranked search, reading, citation, and gated writes.
- [[RowBot/summary]] — Local-first desktop AI assistant with parent-led child-agent orchestration, durable knowledge-graph memory, and multi-provider routing under local data custody.
- [[DocMason/summary]] — Local-first compiler turning private Office/PDF files into structured multimodal evidence bundles with strict source provenance.
- [[Agentmemory/summary]] — Local-first shared memory server for coding agents via MCP, hooks, and REST with keyless BM25 recall.
- [[MemU/summary]] — Shared Markdown skill wiki letting coding agents retain workflows across sessions via scheduled log-mining and retrieve-before-answer injection.
- [[VaultCurate/summary]] — Local-first Obsidian plugin with fused semantic search, verdict-driven link suggestions, and Hot/Cold rediscovery for large vaults.
- [[Hindsight/summary]] — Client-server agent memory with retain/recall/reflect over Postgres+pgvector, storing learned facts and mental models; claims LongMemEval SOTA.
- [[OpenWiki/summary]] — Local-first Tauri desktop app turning kept clipboard copies into AI-organized wiki, knowledge graph, and weekly reports.
- [[Makerskills/summary]] — Plugin of 21 documentation-first agent skills for founder workflows (decisions, research, knowledge bases, content, CFO, domains) running on Claude Code, Codex, and Cursor.

## Research

- [[research/AgentBrain/index|AgentBrain]] — Which of 20 agent second-brain projects are worth using for capture, linking, recall, and agentic action, and how they compare.
