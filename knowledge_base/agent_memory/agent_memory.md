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
