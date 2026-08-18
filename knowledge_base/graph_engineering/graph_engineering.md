# Graph Engineering

Structuring agentic systems as explicit graphs — nodes (agents/tools), edges (routing/control flow), and shared state — as the layer above loop engineering. Covers the mid-2026 "graph engineering" discourse: what is genuinely new vs. recycled orchestration, topology generation, framework practice (LangGraph, Claude Code subagents), enterprise governance, and the token-cost/reliability trade-offs of multi-agent graphs.

## Papers

- [[AIBuilderClubGraphEngineeringClaudeCode/summary]] — Claude Code already has graph engineering's parts: subagents = nodes, orchestrator routing = edges, returned results = shared state.
- [[AIBuilderClubGraphEngineeringGuide2026/summary]] — Graph engineering is nodes+edges+state above loop engineering; mostly recycled term, use only when one loop can't hold the task.
- [[ArxivGoAgentTopologyGeneration/summary]] — GoAgent builds multi-agent topologies from whole groups (not agents), using a task-conditioned info bottleneck; 93.84% acc, ~17% fewer tokens.
- [[ArxivGraphAugmentedLLMAgents/summary]] — Survey: graphs augment LLM agent planning, memory, tools, and multi-agent coordination; first taxonomy of "Graph-augmented LLM Agents."
- [[GraphEngineeringKimiK3/summary]] — Knowledge-graph RAG (triples, not chunks) answers causal multi-hop questions; Kimi K3 chosen for 1M-token context economics, not raw capability.
- [[GraphEngineeringVsLoopEngineering/summary]] — Graph engineering is a real 5th layer above loops, fixing flaws (context rot, error cascades) via V/E/S/P structure and verifier nodes.
- [[LangGraph3YearsGraphEngineering/summary]] — 3 years of LangGraph: graphs suit predictable workflows, cycles not DAGs, loops are a special case of graphs, not a rival.
- [[MarkTechPostPromptLoopGraph/summary]] — Prompt/loop/graph engineering are nested control layers, not competitors; graphs cost ~15x tokens for ~90% gains on hard tasks.
- [[TrueFoundryGraphEngineeringEnterprise/summary]] — Enterprise graph engineering = identity, cost, and governance across heterogeneous agent/tool nodes, distinct from knowledge-graph engineering.
- [[TuringPostIsGraphEngineeringReal/summary]] — "Graph" conflates 4 distinct concepts (control/knowledge/trace/improvement graphs); viral adoption and gain claims don't hold up.
- [[YouTubeWhatIsGraphEngineering/summary]] — Not new: LangGraph/ADK/AutoGen already coordinate agent-pairs as nodes; graph ≠ GraphRAG; agents cost ~4x, graphs ~15x tokens.
