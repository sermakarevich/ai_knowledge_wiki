# Safety & Security

Research on **AI safety, adversarial attacks, privacy, manipulation, and verified/constrained agents**. Covers both offensive capability research and defensive frameworks.

## Papers

- [[AgentBehavioralContracts/summary]] — Design-by-Contract for LLM agents with `(p, δ, k)`-satisfaction and bounded drift `D* = α/γ`; runtime enforcement surfaces 5.2–6.8 hidden soft violations/session.
- [[AiAgentTraps]] — First taxonomy of adversarial traps across six agent components; sub-agent spawning attacks succeed 58–90%.
- [[ClaudiniAutoresearchAdversarialAttacks]] — Claude Code autonomously discovers novel adversarial attack algorithms; 40% ASR vs ≤10% for human-designed baselines.
- [[ClioPrivacyPreservingInsights/summary]] / [[ClioPrivacyPreservingInsightsIntoRealWorldAiUse]] — Anthropic's Clio analyzes millions of Claude.ai conversations via LLM clustering; detects coordinated misuse without human review.
- [[EvaluatingLanguageModelsForHarmfulManipulation]] — Framework distinguishing manipulative propensity vs. efficacy; 10,101-human study; high propensity doesn't predict high efficacy.
- [[MeasuringMaliciousIntermediaryAttacksOnTheLlmSupplyChain/summary]] — 9 of 428 LLM API routers actively inject payloads or steal credentials; no framework verifies response integrity.
- [[MultiUserLargeLanguageModelAgents/summary]] — Frontier LLMs fail as multi-user agents: authority handling degrades under conflict, privacy erodes, coordination scales poorly.
- [[ProjectGlasswingSecuringCriticalSoftwareForTheAiEra]] — Claude Mythos Preview autonomously discovers critical vulns (incl. 27-year-old bugs); deployed defensively across 50+ orgs.
- [[SEVerAVerifiedSynthesisOfSelfEvolvingAgents]] — Wraps self-evolving agents in formal logic contracts (FGGMs); zero constraint violations while beating unconstrained baselines.
