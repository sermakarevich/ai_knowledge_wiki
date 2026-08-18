> [[index|Wiki]] | [[summary|Summary]]

# Connections

## Directly related: graph-augmented and graph-based multi-agent topology work

- [[../ArxivGraphAugmentedLLMAgents/index|Graph-Augmented Large Language Model Agents: Current Progress and Future Prospects]] — the broader survey this paper's specific method slots into. Its MAS section ([[../ArxivGraphAugmentedLLMAgents/wiki/04-graph-augmented-multi-agent-systems]]) frames GoAgent-style topology generation as one point in an evolution from static (AutoGen, MacNet, AFlow) to task-adaptive (G-Designer, MaAS) to runtime-adaptive (ReSo, EvoMAC, AnyMAC) MAS topologies, and explicitly discusses AgentPrune/AgentDropout-style edge/node pruning as the "redundancy" analogue GoAgent's group-centric design tries to avoid architecturally instead of pruning after the fact.
- [[../../ai_papers/multi_agent_systems/multi_agent_systems|Multi-Agent Systems (category index)]] — see especially [[../../ai_papers/multi_agent_systems/multi_agent_systems|BrainInspiredGraphMultiAgentSystemsForLLMReasoning]] (task-specific agent graphs with a shared workspace) and [[../../ai_papers/multi_agent_systems/multi_agent_systems|DiversityCollapseMultiAgentLLM]] (shows topology choice affects diversity collapse in MAS — a complementary lens to GoAgent's accuracy/token/robustness framing, both treating the communication graph as the key design lever).
- [[../../ai_papers/multi_agent_systems/multi_agent_systems|RecursiveMultiAgentSystems]] — also replaces something about inter-agent communication (text messages, in that case, replaced with latent-space thought sharing) to cut token cost, structurally parallel to GoAgent's CIB-based compression of inter-group signal, though via a different mechanism.

## Prior work GoAgent directly positions itself against (named in its own Related Work)

GoAgent's Related Work section (see [[wiki/03-experiments-and-related-work]]) names AgentPrune, G-Designer, AgentDropout, ARG-Designer, and EIB-LEARNER as the node-centric/template-based lineage it supersedes — these are the closest prior-art comparisons and worth reading first if evaluating whether GoAgent's gains are incremental or substantial relative to that lineage.

## Not force-linked

No other unfiled `papers/` entries ingested around 2026-08-18 concern multi-agent communication topology specifically (the other same-day ingests — PrefectLoopsVsGraphs, YouTubeWhatIsGraphEngineering, LangGraph3YearsGraphEngineering, TuringPostIsGraphEngineeringReal, MarkTechPostPromptLoopGraph, GraphEngineeringKimiK3, AIBuilderClubGraphEngineeringGuide2026 — are about "graph engineering" as an agent-harness/workflow-design pattern, a distinct concept from GoAgent's learned communication-topology generation, so they are not linked here to avoid conflating the two uses of "graph").
