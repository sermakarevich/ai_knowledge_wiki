# Agent Memory

Research on **persistent memory systems for agents** — short-term context management, cross-session memory, associative/graph memory, and cross-domain memory transfer.

## Papers

- [[CodexMemories/summary]] — OpenAI Codex opt-in local memory persists preferences and project conventions in `~/.codex/memories/`.
- [[GaamaGraphAugmentedAssociativeMemoryForAgents]] — Hierarchical KG with concept-mediated nodes + hybrid PageRank+semantic retrieval; 78.9% LoCoMo-10.
- [[MemCollab]] — Contrastive trajectory distillation between heterogeneous agents; Qwen-7B 57.1%→71.6%.
- [[MemSearchO1/summary]] — Replaces cumulative context with seed-anchored memory fragments + path retracing; +21.9% F1.
- [[MementoTeachingLlmsToManageTheirOwnContext/summary]] — Trains LLMs to compress reasoning blocks into dense summaries; 2-3x KV cache reduction.
- [[MemoryIntelligenceAgent]] — Manager-Planner-Executor architecture with bidirectional memory (parametric + non-parametric); +5.5-7.5 points on 11 benchmarks.
- [[MemoryTransferLearning/summary]] — Cross-domain memory transfer works at high abstraction (Insights) not raw traces; abstract meta-knowledge travels.
- [[StatelessDecisionMemory/summary]] — DPM replaces incremental summarization with an append-only event log + single temperature-0 projection at decision time; 7–15× faster, deterministically replayable, outperforms stateful memory at tight budgets (+0.515 FRP).
