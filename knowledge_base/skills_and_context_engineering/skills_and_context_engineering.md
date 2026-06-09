# Skills & Context Engineering

Research on **agent skills** (reusable procedural modules), prompt/context evolution, and continual learning via externalized artifacts rather than weight updates.

## Papers

- [[AgenticContextEngineering/summary]] — ACE evolves LLM "playbooks" via incremental delta updates; +10% agent gains, 91% lower adaptation latency.
- [[AutomatingSkillAcquisitionThroughLargeScaleMining]] — Mines GitHub for reusable skill cards (SKILL.md); SkillNet cuts steps 30%, boosts reward 40%, 26% have vulns.
- [[GepaReflectivePromptEvolution]] — Prompt optimizer via natural-language reflection + Pareto evolution; +10% over GRPO with 35x fewer rollouts.
- [[HowLovableSelfImprovesEveryHour/summary]] — Stuck-session detector clusters user resolutions into a live knowledge bank injected contextually; agent vent tool self-reports platform failures and doubles as an incident early-warning system.
- [[HyperAgents]] — Self-referential agents where the self-improvement mechanism itself can be modified; recursive domain-general improvement.
- [[MementoSkillsLetAgentsDesignAgents]] — Continual learning for frozen LLMs via evolving executable skill library; +13.7pp GAIA, +20.8pp HLE.
- [[MetaClawJustTalk]] — Dual-timescale learning: fast skill synthesis from failures + opportunistic RL fine-tuning; Kimi-K2.5 21.4%→40.6%.
- [[MetaContextEngineeringViaAgenticSkillEvolution]] — Bi-level optimization co-evolving context strategies and artifacts; 89.1% avg improvement, 13.6x faster.
- [[SkillClawLetSkillsEvolveCollectivelyWithAgenticEvolver]] — Autonomous nightly evolver aggregates multi-user interactions; +42% gains over 6 simulated days.
- [[SokAgenticSkillsBeyondToolUseInLlmAgents]] — SoK formalizing agentic skills: lifecycle, design patterns, taxonomy, security threat model.
- [[TrizGenerativeAiPrompts/summary]] — Handbook mapping ~30 TRIZ innovation tools to prompt templates for ChatGPT/Gemini/Claude; reframes TRIZ tool-chain as Chain-of-Thought; seeds ccTOPP open-prompt project.
- [[AnthropicSelfServiceDataAnalytics/summary]] — Anthropic's four-layer analytics agent stack achieves 95% query automation and ~95% accuracy; skill files alone lift accuracy from 21% to 95%+, outperforming raw SQL corpus retrieval by >74pp.
- [[AgentNativeProductManagementGuide/summary]] — Two Claude Code skills (`ce:strategy` and `ce:product-pulse`) automate PM strategy docs and daily product health reports via MCP, closing the Plan → Ship → Review loop.
- [[SkillTextToSkillStructure/summary]] — SSL three-layer structured encoding for agent skills (scheduling/structure/logic); LLM normalizer converts free-text docs to SSL; improves skill discovery MRR 0.573→0.707 and risk-assessment F1 0.744→0.787.
- [[SkillRetrievalAugmentation/summary]] — Formalizes Skill Retrieval Augmentation (SRA) for agents over a 26K-skill corpus; SRA-Bench reveals the bottleneck is need-aware and relevance-aware skill loading, not retrieval quality.
