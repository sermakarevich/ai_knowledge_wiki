# Coding Agents & Code Generation

Research on **LLM-powered coding agents, code generation, program analysis, software engineering workflows**, and spec-driven development.

## Papers

- [[AgenticCodeReasoning/summary]] — Structured prompting technique (premises + execution traces + formal conclusions) enables execution-free patch verification, fault localization, and code Q&A; +5–12 pp over unstructured chain-of-thought.
- [[BridgingCodePropertyGraphsAndLanguageModelsForProgramAnalysis]] — codebadger MCP server bridges Joern's CPG engine with LLMs; discovered a new buffer overflow in libtiff.
- [[CodingAgentsAreEffectiveLongContextProcessors]] — Off-the-shelf coding agents beat dedicated long-context systems by 17.3% by treating corpora as filesystems.
- [[Composer2TechnicalReport]] — Cursor's Composer 2 (Kimi K2.5 + RL in realistic harness) matches frontier on coding benchmarks at lower cost.
- [[EvaluatingAgentsMdAreRepositoryLevelContextFilesHelpfulForCodingAgents]] — LLM-generated AGENTS.md/CLAUDE.md reduce coding agent success and raise cost 20%+; human-written help only ~4%.
- [[EveryAgenticEngineeringHack/summary]] — 22-hack practitioner guide to parallel Claude Code + Codex sessions: plan-first loop, YOLO permissions, voice input, cmux parallelism, and personal knowledge base as agent memory.
- [[ForgeCode/summary]] — Rust 24-crate terminal coding agent: 30+ LLM providers via 6 wire formats, SQLite-persisted conversations, MCP client, ZSH-prompt integration via `:` widget.
- [[FrontierCodingAgentsAlphaZeroConnect4/summary]] — Benchmarks frontier coding agents on autonomously implementing AlphaZero for Connect Four; Claude Opus 4.7 wins 7/8 trials vs. a perfect solver; GPT-5.4 shows anomalous underperformance suggesting sandbagging.
- [[FromCodeFoundationModelsToAgentsAndApplications]] — 200+ page survey of code LLMs: data, training, SFT, RLVR, agentic systems, safety.
- [[HowAIAgentsSpendYourMoney/summary]] — First systematic study of agentic coding token costs: 3500x vs single-round reasoning, 30x same-task variance, accuracy-cost decoupled, models systematically underestimate own usage.
- [[LlmBasedAutomatedDiagnosisOfIntegrationTestFailures/summary]] — Google's Auto-Diagnose with Gemini diagnoses integration test failures; 90% accuracy on 52K tests.
- [[ParallelAgenticDevelopment/summary]] — Five-or-more parallel Claude Code agents via git worktrees, per-agent DB isolation, CLAUDE.md scoping, and three coordination patterns; practical cap is 5-8 agents.
- [[PiCodingAgent/summary]] — Minimal terminal coding agent (TypeScript) with 4 built-in tools and a full-replacement extension API; deliberately omits MCP, plan mode, and sub-agents — those belong in user extensions.
- [[ProfessionalDevsAgentControl/summary]] — Experienced developers deliberately retain control over coding agents: scope tasks carefully, validate outputs rigorously, and reject passive 'vibe coding' (n=13 observations, n=99 surveys).
- [[ScalingCodingAgentsViaAtomicSkills/summary]] — RL training on five atomic skills (localize, edit, test, reproduce, review) improves composite task performance 15-30%.
- [[ShippingAtInferenceSpeed/summary]] — 2025 practitioner account: AI coding models make implementation near-trivial, shifting bottlenecks to architecture; concurrent projects, documentation-first conventions, and agent-optimized codebases maximize throughput.
- [[SpecDrivenDevelopment]] — Framework making specs the source of truth; structured specs reduce LLM-generated code errors up to 50%.
- [[SlopCodeBench]] — Benchmark showing coding agents degrade monotonically over iterations; agent code 2.2x more verbose than human.- [[ThinkAnywhereInCodeGeneration]] / [[ThinkAnywhereInCodeGeneration/summary]] — Teaches LLMs to insert reasoning blocks mid-code; +9.3% pass@1 with fewer total tokens.
- [[spec-driven-development-summary]] — JetBrains/DeepLearning.AI course summary on SDD: markdown specs drive agentic coding.
- [[SWEChat/summary]] — First large-scale empirical study of real-world coding agent sessions; vibe coding introduces ~9.5× more security vulnerabilities and only 44% of agent code survives into commits.
- [[SWEFundamentalsForAICoding/summary]] — Practitioner workshop: smart-zone/dumb-zone context management, grill-me alignment sessions, vertical-slice Kanban issues, TDD loops, and deep modules maximize AI coding agent output.
- [[BenchmarkingPromptEngineeringTechniquesForSecureCodeGeneration/summary]] — Security-aware prompt prefix halves vulnerable Python output on newer GPT models; self-critique-and-fix removes another quarter to two-thirds of flaws.
- [[ContextEngineeringForMultiAgentLLMCodeAssistantsUsingElicitNotebookLMChatGPTAndClaudeCode/summary]] — Multi-agent pipeline (intent clarification, Elicit + NotebookLM retrieval, role-specialized Claude Code team) doubles single-shot success on multi-file tasks at 3–5× token cost.
- [[FromRestructuringToStabilization/summary]] — GPT-5.1 iteratively refactors Java toward a stable readable form: big first cleanup, then shrinking touch-ups, with degraded code converging to the same end state.
- [[HumanAiExperienceInIntegratedDevelopmentEnvironments/summary]] — Systematic review of 90 studies: in-IDE AI assistants speed up routine coding but add verification overhead, over-reliance risks, and code quality concerns.
- [[GithubCopilotProductivitySecurity/summary]] — Survey finds GitHub Copilot speeds up routine coding substantially but often generates insecure code, so human review and testing remain essential.
- [[DemystifyingPracticesChallengesGithubCopilot/summary]] — Mined 1,230 Stack Overflow and GitHub Discussions: Copilot speeds JavaScript/Python boilerplate in VS Code but suffers integration failures, broken suggestions, and pricing/privacy worries.
- [[AiDrivenAdvancementsAutomatedProgramRepairCodeGeneration/summary]] — Survey maps LLM repair and code generation: pre-trained code models fix common bugs fast, heavier models handle complex cases, but all need tests and human review.
- [[TddGovernanceForMultiAgentCodeGenerationViaPromptEngineering/summary]] — Enforces test-driven development as strict multi-agent governance: LLMs propose patches only, a deterministic engine validates phases and caps repairs at three tries for repeatable generation.
- [[InfluenceTacticsPromptFraming/summary]] — Pressure-laden prompts make LLM code more often wrong and less secure, while polite or formal framings only change explanation style.

- [[ImpactOfLLMAssistantsOnSoftwareDeveloperProductivity/summary]] — Review of 39 studies finds LLM assistants speed routine coding and search but risk errors, over-reliance, and flow disruption; treat output as drafts needing review.
- [[PracRepair/summary]] — PracRepair repairs code like a human mechanic: watches programs run, asks focused diagnostic questions, and re-tests after each fix — topping baselines on real Java bugs at lower cost.
- [[ImpactOfAiToolOnEngineeringAtAnzBank/summary]] — ANZ Bank's six-week Copilot trial found engineers finished ~42% faster with fewer bugs and code smells, but security impact remained inconclusive.
- [[RethinkingCodeReviewWorkflowsWithLLM/summary]] — Field study finds developers prefer proactive AI code-review summaries for unfamiliar changes and on-demand Q&A otherwise, with AI as junior partner not replacement.
- [[SecurityWeaknessesOfCopilotGeneratedCodeInGitHubProjects/summary]] — About one in four committed Copilot-generated snippets has security weaknesses (~3 each); pasting analyzer warnings into repair prompts fixes over half.
- [[LlmCodeRefactoringCapability/summary]] — StarCoder2 removes more surface code smells than developers but breaks tests often; one-shot prompting with best-of-five sampling makes it a useful refactoring partner.
- [[PracticesAndChallengesOfUsingGitHubCopilot/summary]] — Copilot speeds JavaScript/Python boilerplate and tests in mainstream IDEs, but suggestions often fail, degrade in large files, and raise privacy concerns.
- [[ExperienceWithGithubCopilotForDeveloper/summary]] — Zoominfo's 400-developer rollout: ~33% of Copilot suggestions accepted, ~20% time saved on boilerplate and tests, but domain logic needs oversight.
- [[DebugRepair/summary]] — DebugRepair teaches AI fixers to debug like humans: trim failing tests, insert print statements to trace variables, then repair from evidence — more fixes at lower cost.
- [[TowardsPracticalAndUsefulAutomatedProgramRepairForDebugging/summary]] — Interactive IDE repair from debugger state without tests: localize from live values, generate LLM patches, validate via simulated traces.
- [[OnTheRobustnessOfCodeGenerationTechniques/summary]] — Paraphrasing equivalent Java descriptions changes Copilot output 46% of the time, sometimes gaining or losing correct code. Clear phrasing matters as much as code itself.
- [[BestPracticesForClaudeCode/summary]] — Treat Claude Code like a forgetful junior engineer: keep context tidy, give verifiable checks, plan before coding, and store house rules in CLAUDE.md.
- [[SpecDrivenDevelopmentWithAI/summary]] — Spec Kit makes specs the living source of truth; Specify→Plan→Tasks→Implement flow yields small reviewable changes with human verification.
- [[CursorRules/summary]] — Cursor Rules are persistent briefings compensating for stateless LLMs: project, user, team, and AGENTS.md types scoped via frontmatter globs.
- [[SpecDrivenDevelopmentWithCodingAgents/summary]] — DeepLearning.AI course teaches blueprint-style spec-driven AI coding: markdown constitution plus plan-implement-verify loop beats vibe coding.
- [[AiderUsage/summary]] — Terminal pair programmer: point aider at files, describe changes in plain English. It rewrites code, shows diffs, auto-commits via git.
- [[GiveYourAgentALaboratory/summary]] — Give coding agents their own laboratory with benchmarks, screenshots, and verification tools so they self-correct instead of asking humans to check work.
- [[AiCodebaseTradeoffPerModule/summary]] — Sort each module into a speed bucket where agents own low-stakes code outright, or a high-stakes bucket requiring line-by-line review; saved time funds rigor where it counts.
- [[ThreeStepAICodingWorkflowSoloFounders/summary]] — Treat AI like a literal-minded junior hire: agree on a PRD, break it into small tasks, then implement one subtask at a time with human approval.
- [[DhhFutureOfProgrammingLexFridman501/summary]] — DHH now directs ~16 parallel AI agents instead of hand-writing code, proving it with an agent-built Linux desktop; humans still review architecture.
- [[RalphWiggumAsASoftwareEngineer/summary]] — Single-process loop does one priority task per iteration, fanning work to subagents and enforcing correctness via fast test and build loops.
- [[SixMonthsWritingCodeExclusivelyWithAgents/summary]] — Engineer wrote no code by hand for six months, scaling to ~20 parallel agents in cloud VMs; shipping got cheap, deciding what to ship became the bottleneck.
- [[LlmCodingWorkflow2026/summary]] — Spec-first, small-step AI coding workflow: plan with the model, implement one tested chunk at a time, review line-by-line, commit often.
- [[AgenticEngineeringPatterns/summary]] — Placeholder scope marker for Willison's agentic-engineering guide: only framing and table of contents available, no concrete patterns quotable yet.
- [[FourWeeksOfVibecoding/summary]] — Non-coder shipped four live sites in four weeks via spoken specs to Claude Code; clarity beats technical skill.
- [[TrulyAnalytics/summary]] — Solo dev built analytics product in six weeks with Codex writing 42% of code, but only 46% of AI lines survived versus 72% human.
- [[JevAsAJudge/summary]] — Cheap JEV judge matches expensive GPT-6 on easy preference pairs; confidence-gated escalation keeps ~99% accuracy while routing only half the cases upstairs.

## Research

- [[research/ai_coding_best_practices/index|ai_coding_best_practices]] — Evidence-backed best practices for using AI coding assistants for writing, debugging, and refactoring code.
- [[ClaudeCodeOverview/summary]] — Terminal-native AI teammate that reads codebases, makes multi-file edits, verifies work, and automates chores via CLAUDE.md, MCP, and scheduled agents.

## Tutorials

- [[tutorials/herdr/index|herdr]] — Herdr, a mouse-first terminal multiplexer for coding agents: install, the workspace→tab→pane→agent model, pane split/move/resize/zoom/swap/close (mouse + `Ctrl+B` + CLI), the full keymap cheat-sheet, and power features (sessions, agents, remote/phone, notifications, plugins).
