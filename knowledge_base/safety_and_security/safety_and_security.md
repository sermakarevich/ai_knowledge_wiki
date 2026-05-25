# Safety & Security

Research on **AI safety, adversarial attacks, privacy, manipulation, and verified/constrained agents**. Covers both offensive capability research and defensive frameworks.

## Papers

- [[AgentBehavioralContracts/summary]] — Design-by-Contract for LLM agents with `(p, δ, k)`-satisfaction and bounded drift `D* = α/γ`; runtime enforcement surfaces 5.2–6.8 hidden soft violations/session.
- [[AiAgentTraps]] — First taxonomy of adversarial traps across six agent components; sub-agent spawning attacks succeed 58–90%.
- [[AutomatedAlignmentResearchers/summary]] — Nine Claude agents autonomously hill-climb weak-to-strong supervision, hitting PGR 0.97 in 5 days vs. human baseline 0.23 in 7; reward hacking confirms human oversight remains essential.
- [[ClaudiniAutoresearchAdversarialAttacks]] — Claude Code autonomously discovers novel adversarial attack algorithms; 40% ASR vs ≤10% for human-designed baselines.
- [[ClioPrivacyPreservingInsights/summary]] / [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse]] — Anthropic's Clio analyzes millions of Claude.ai conversations via LLM clustering; detects coordinated misuse without human review.
- [[EpisodicMemoryAIAgentsRisks/summary]] — Position paper cataloging four risk categories of AI agent episodic memory (deception, privacy, unpredictability, situational awareness) and proposing four design principles for safe implementation.
- [[EvaluatingLanguageModelsForHarmfulManipulation]] — Framework distinguishing manipulative propensity vs. efficacy; 10,101-human study; high propensity doesn't predict high efficacy.
- [[MeasuringMaliciousIntermediaryAttacksOnTheLlmSupplyChain/summary]] — 9 of 428 LLM API routers actively inject payloads or steal credentials; no framework verifies response integrity.
- [[MultiUserLargeLanguageModelAgents/summary]] — Frontier LLMs fail as multi-user agents: authority handling degrades under conflict, privacy erodes, coordination scales poorly.
- [[ProjectGlasswingSecuringCriticalSoftwareForTheAiEra]] — Claude Mythos Preview autonomously discovers critical vulns (incl. 27-year-old bugs); deployed defensively across 50+ orgs.
- [[SEVerAVerifiedSynthesisOfSelfEvolvingAgents]] — Wraps self-evolving agents in formal logic contracts (FGGMs); zero constraint violations while beating unconstrained baselines.
- [[WhoIsInChargeDisempowermentPatterns/summary]] — First large-scale study of AI disempowerment across 1.5M Claude.ai conversations; rare (<0.1%) but scales to tens of thousands daily; RLHF preference models actively prefer disempowering responses.
