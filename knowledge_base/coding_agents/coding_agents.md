# Coding Agents & Code Generation

Research on **LLM-powered coding agents, code generation, program analysis, software engineering workflows**, and spec-driven development.

## Papers

- [[BridgingCodePropertyGraphsAndLanguageModelsForProgramAnalysis]] — codebadger MCP server bridges Joern's CPG engine with LLMs; discovered a new buffer overflow in libtiff.
- [[CodingAgentsAreEffectiveLongContextProcessors]] — Off-the-shelf coding agents beat dedicated long-context systems by 17.3% by treating corpora as filesystems.
- [[Composer2TechnicalReport]] — Cursor's Composer 2 (Kimi K2.5 + RL in realistic harness) matches frontier on coding benchmarks at lower cost.
- [[EvaluatingAgentsMdAreRepositoryLevelContextFilesHelpfulForCodingAgents]] — LLM-generated AGENTS.md/CLAUDE.md reduce coding agent success and raise cost 20%+; human-written help only ~4%.
- [[ForgeCode/summary]] — Rust 24-crate terminal coding agent: 30+ LLM providers via 6 wire formats, SQLite-persisted conversations, MCP client, ZSH-prompt integration via `:` widget.
- [[FromCodeFoundationModelsToAgentsAndApplications]] — 200+ page survey of code LLMs: data, training, SFT, RLVR, agentic systems, safety.
- [[HowAIAgentsSpendYourMoney/summary]] — First systematic study of agentic coding token costs: 3500x vs single-round reasoning, 30x same-task variance, accuracy-cost decoupled, models systematically underestimate own usage.
- [[LlmBasedAutomatedDiagnosisOfIntegrationTestFailures/summary]] — Google's Auto-Diagnose with Gemini diagnoses integration test failures; 90% accuracy on 52K tests.
- [[ScalingCodingAgentsViaAtomicSkills/summary]] — RL training on five atomic skills (localize, edit, test, reproduce, review) improves composite task performance 15-30%.
- [[ShippingAtInferenceSpeed/summary]] — 2025 practitioner account: AI coding models make implementation near-trivial, shifting bottlenecks to architecture; concurrent projects, documentation-first conventions, and agent-optimized codebases maximize throughput.
- [[SpecDrivenDevelopment]] — Framework making specs the source of truth; structured specs reduce LLM-generated code errors up to 50%.
- [[SlopCodeBench]] — Benchmark showing coding agents degrade monotonically over iterations; agent code 2.2x more verbose than human.
- [[TheKitchenLoopUserSpecDrivenDevelopmentForASelfEvolvingCodebase]] — Autonomous software evolution via synthetic power-user testing; 285+ iterations, 0 regressions, $0.38/PR.
- [[ThinkAnywhereInCodeGeneration]] / [[ThinkAnywhereInCodeGeneration/summary]] — Teaches LLMs to insert reasoning blocks mid-code; +9.3% pass@1 with fewer total tokens.
- [[spec-driven-development-summary]] — JetBrains/DeepLearning.AI course summary on SDD: markdown specs drive agentic coding.
