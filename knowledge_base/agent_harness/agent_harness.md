# Agent Harness & Engineering

Research on the **harness** — the deterministic scaffolding around an LLM that handles tool routing, context management, permissions, and execution. Central thesis of this category: agent quality is mostly a harness problem, not a model problem.

## Papers

- [[AI_Harness_Engineering/summary]] — Seven-layer harness model (Instruction, Tools, Memory, Execution, Policy, Observability, Evaluation) for production-grade agents.
- [[AGENTIC_ENGINEERING_PATTERS]] — Practitioner guide: harness quality, review discipline, and reusable knowledge as the engineer's new core responsibilities.
- [[AgentHarnessEngineering]] / [[AgentHarnessEngineering/summary]] — Two practitioners converge on: Agent = Model + Harness. Harness quality is the new competitive moat.
- [[AgenticHarnessForCompilers]] — First agentic harness (llvm-autofix) for LLVM compiler bug repair; best model only 20% correctness, exposing reasoning gaps.
- [[AutoHarness]] — LLM auto-synthesizes a code harness via Thompson-sampling tree search; Gemini-Flash+Harness beats Gemini-Pro.
- [[AutoHarnessImprovingLLMAgents]] — Duplicate of AutoHarness; same paper on automatic harness synthesis.
- [[BuildingEffectiveAICodingAgents]] — OPENDEV: open-source terminal coding agent with 5-layer safety, adaptive context compaction, multi-model routing.
- [[ClaudeManagedAgents]] — Anthropic's production platform abstracts agent infrastructure; 10x faster deployment with self-evaluation loops.
- [[code-review-graph-analysis]] — MCP server persisting a SQLite code knowledge graph (tree-sitter parse, 28 tools) so AI coding agents fetch targeted review context instead of re-reading files.
- [[ExternalizationInLLMAgents]] / [[ExternalizationInLLMAgents/summary]] — Survey: agent progress comes from externalizing memory, skills, and protocols into persistent runtime.
- [[HermesAgent/summary]] — Nous Research's self-hosted, provider-agnostic personal agent: ~54 tools, SQLite+FTS5 session store, plugin/skill extensibility, 200+ models via OpenRouter, MIT-licensed.
- [[HowMuchLlmDoesASelfRevisingAgentActuallyNeed]] — Decomposing agent competence shows explicit world-model planning matters most; LLM's marginal contribution is small.
- [[MetaHarness]] — Outer-loop harness code optimization via agentic proposer with full trace access; +7.7pp over SOTA context engineering.
- [[MetaHarnessEndToEndOptimizationOfModelHarnesses]] — Duplicate of MetaHarness.
- [[MtaAgentOpenRecipeForMultimodalDeepSearchAgents/summary]] — Open 32B agent trained on 21K multimodal multi-hop trajectories; beats GPT-5 and Gemini-2.5-Pro.
- [[NativeEvolution/summary]] — Agents spontaneously explore and distill "World Knowledge" docs with no reward; ~20% accuracy gains with cross-model transfer.
- [[NaturalLanguageAgentHarnesses]] — Formalizes harnesses as portable natural-language specs interpreted by a shared runtime.
- [[NemoClawLocalAgent/summary]] — NVIDIA's local agent: 120B model + sandbox + messaging on local GPU with interactive policy approval.
- [[SmallLanguageModelsAreTheFutureOfAgenticAi/summary]] — SLMs (<10B) match 30–70B LLMs on agent sub-tasks at 10–30x lower cost; 6-step migration algorithm.
- [[TheEvolutionOfToolUseInLLMAgents]] — Survey unifying single→multi-tool orchestration across six dimensions; topology-aware planning is the frontier.
- [[ToolAttentionIsAllYouNeed/summary]] — MCP middleware scoring tools by Intent–Schema Overlap, state-gating, and lazy-loading full schemas only for top-k; cuts per-turn tool tokens 95% (47.3k→2.4k) on a 120-tool simulated benchmark.
- [[TowardsEndToEndAutomationOfAIResearch]] — End-to-end AI research pipeline from ideation to manuscript; produced a paper that passed ICLR workshop review.
- [[UltraLongHorizonAgenticScience/summary]] — ML-Master 2.0: Hierarchical Cognitive Caching memory runs 24h Kaggle ML tasks at 56.4% medal rate.
