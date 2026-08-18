> [[index|Wiki]] | [[summary|Summary]]

# Connections

This paper is an academic survey of graph-augmented LLM agents. The KB also holds several practitioner/industry pieces on the same underlying idea, popularized under the "graph engineering" label — this survey gives that buzzword its academic backbone: a formal taxonomy, named methods, and citations, rather than a framework pitch.

- [[GraphEngineeringVsLoopEngineering/summary|Graph Engineering vs. Loop Engineering]] — Frames "graph engineering" as the layer above agent loops, fixing relational failures a single loop can't reach; this survey substantiates that framing with concrete taxonomy (planning/memory/tool graphs, MAS orchestration graphs) rather than a five-layer-stack pitch.
- [[AIBuilderClubGraphEngineeringGuide2026/summary|AI Builder Club: Graph Engineering Guide 2026]] — A practitioner's plain-language decode of what an agent graph is and when it beats a single loop; this survey supplies the research lineage (AFlow, MacNet, G-Designer, etc.) behind that same claim.
- [[LangGraph3YearsGraphEngineering/summary|LangGraph: 3 Years of Graph Engineering]] — LangChain's production experience report that agent graphs are usually cyclic and dynamic fan-out is essential; this survey's static → task-adaptive → process-dynamic MAS topology progression ([[wiki/04-graph-augmented-multi-agent-systems]]) is the academic mirror of that same maturation path.
- [[TuringPostIsGraphEngineeringReal/summary|Turing Post: Is Graph Engineering Real?]] — A skeptical fact-check of the "graph engineering" buzzword's overstated adoption claims; this survey's own critical gaps (fragmented, small-scale, mostly static graphs — see [[critical_thinking]]) corroborate that skepticism from the academic side rather than contradicting it.
- [[ASurveyOfWorkflowOptimizationForLlmAgents|A Survey of Workflow Optimization for LLM Agents]] — Unifies 77 works via an "Agentic Computation Graph" abstraction and argues graph-level optimization beats prompt tuning; a closely related survey covering similar ground to this paper's MAS orchestration section, from a workflow-optimization rather than agent-module angle.

Not linked: several other "graph engineering" entries in `/Users/sergii/.kb/papers/` (`GraphEngineeringKimiK3`, `MarkTechPostPromptLoopGraph`, `TrueFoundryGraphEngineeringEnterprise`, `PrefectLoopsVsGraphs`, `YouTubeWhatIsGraphEngineering`) cover the same buzzword but are largely redundant with the four above in framing; not force-linked here to avoid a wall of near-duplicate references.
