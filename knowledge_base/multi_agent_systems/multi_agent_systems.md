# Multi-Agent Systems

Research on **multi-agent coordination, workflow orchestration, and collective intelligence** across LLM-based agents. Covers cooperation vs. competition, failure attribution, scaling laws, and the specification gap between roles.

## Papers

- [[AIRA2OvercomingBottlenecksInAIResearchAgents]] / [[AIRA2OvercomingBottlenecksInAIResearchAgents/summary]] — Async multi-GPU workers + tamper-proof evaluation + ReAct operators; 76% percentile on MLE-bench-30.
- [[ASurveyOfWorkflowOptimizationForLlmAgents]] — Unifies 77 works via the Agentic Computation Graph abstraction; graph-level optimization beats prompt tuning.
- [[AgenticAiAndTheNextIntelligenceExplosion]] — Argues the next intelligence explosion will be plural/social — communities of agents, not a monolithic ASI.
- [[AgenticRsArchitecture]] — AutoModel: three cooperating evolution agents automate the full recommender system lifecycle.
- [[AutogenesisAgentProtocol/summary]] — AGP adds versioned lifecycle + closed-loop self-evolution on top of A2A/MCP protocols.
- [[BeliefDrivenMultiAgentCollaborationViaApproximatePerfectBayesianEquilibrium]] — BEACOF: agents switch cooperation↔competition via Bayesian belief estimates; +24 accuracy on medical QA.
- [[BrainInspiredGraphMultiAgentSystemsForLLMReasoning]] — BIGMAS: task-specific agent graphs with a shared workspace; up to +36 reasoning accuracy on GPT-5.
- [[CraftGroundedMultiAgentCoordinationUnderPartialInformation]] — CRAFT benchmark: frontier models underperform 7B models on 3D reconstruction due to over-correction.
- [[DiscoveringMultiagentLearningAlgorithmsWithLLMs]] — LLM-driven AlphaEvolve auto-discovers novel multi-agent RL algorithms beating human-designed SOTA.
- [[DiversityCollapseMultiAgentLLM/summary]] — Multi-agent interaction causes diversity collapse via structural coupling; junior-dominated flat teams beat expert hierarchies on diversity (Vendi 8.08 vs. 4.65), and NGT/subgroup topologies robustly prevent premature convergence.
- [[DropTheHierarchyAndRoles]] — 25k-experiment study: hybrid Sequential protocol (fixed order, autonomous roles) beats centralized and fully autonomous.
- [[EffectiveStrategiesForAsynchronousSoftwareEngineeringAgents]] — CAID: git worktree isolation + branch-merge integration for async multi-agent coding; +26.7% on PaperBench.
- [[FromSkillsToTalent/summary]] — OMC decouples agent identity (Talent) from runtime (Container) to orchestrate heterogeneous agents as a company; E2R tree search + DAG tasks achieves 84.67% on PRDBench, +15.48 pp over SOTA.
- [[LLMTeamsAsDistributedSystems/summary]] — Applies distributed systems theory (Amdahl's Law) to multi-agent LLM teams; centralized coordination dominates decentralized in consistency and cost, while speedup is hard-bounded by task parallelizability.
- [[MarchMultiAgentReinforcedSelfCheckForLlmHallucination]] — Multi-agent RL with blinded checker enforcing information asymmetry; reduces RAG hallucination ~20pp.
- [[MassRag/summary]] — MASS-RAG: three role-specialized filter agents (Summarizer, Extractor, Reasoner) + synthesizer; +27% over single-filter.
- [[MultiAgentSelfEvolvedABC/summary]] — Multi-agent LLM system autonomously improves ABC EDA's 1.2M-line C codebase by ~8.3% QoR.
- [[OnTheReliabilityLimitsOfLlmBasedMultiAgentPlanning]] — Formal proof: multi-agent delegation always dominated by centralized agent with same info; 90%→22% over 5-agent chain.
- [[Optimas]] — Framework learning locally aligned reward functions per component; 11.92% avg improvement across 5 tasks.
- [[PaperOrchestraAutomatedAiResearchPaperWriting/summary]] — Multi-agent pipeline turns research notes into LaTeX papers; 84% simulated CVPR acceptance.
- [[RethinkingFailureAttributionInMultiAgentSystems]] — MP-Bench shows LLMs are actually good at MAS failure attribution given multiple valid causes.
- [[SelfOptimizingMultiAgentDeepResearch/summary]] — GEPA applied to 4-agent Deep Research surpasses a year of expert-crafted prompts from one-liners.
- [[SingleAgentLlmsOutperformMultiAgentSystemsOnMultiHopReasoning]] — Single agents match/beat multi-agent systems on multi-hop reasoning at equal compute.
- [[TheConductor/summary]] — 7B Conductor model trained via RL (GRPO) to dynamically orchestrate diverse worker LLMs; achieves SOTA on LiveCodeBench (83.93%) and GPQA-Diamond (87.5%), outperforming frontier models individually.
- [[TheSpecificationGapCoordinationFailureUnderPartialKnowledgeInCodeAgents]] — Persistent 30-35pp "coordination tax" vs. single-agent when specs are partial.
- [[TowardsAScienceOfScalingAgentSystems]] — Scaling laws for 180 agent configs; coordination helps only below ~45% single-agent baseline.
- [[TrizAgents/summary]] — Supervised multi-agent system (LangGraph + GPT-4o) automates 6-step TRIZ innovation workflow via specialized domain-expert agents; exactly reproduced human physical-contradiction derivations on a gantry crane case study.
- [[WhenIsCollectiveIntelligenceALottery]] — Scaling laws for memetic drift; consensus often reflects random noise, not genuine reasoning.
