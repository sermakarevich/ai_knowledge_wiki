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
- [[ExternalizationInLLMAgents]] / [[ExternalizationInLLMAgents/summary]] — Survey: agent progress comes from externalizing memory, skills, and protocols into persistent runtime.
- [[HermesAgent/summary]] — Nous Research's self-hosted, provider-agnostic personal agent: ~54 tools, SQLite+FTS5 session store, plugin/skill extensibility, 200+ models via OpenRouter, MIT-licensed.
- [[HowMuchLlmDoesASelfRevisingAgentActuallyNeed]] — Decomposing agent competence shows explicit world-model planning matters most; LLM's marginal contribution is small.
- [[MetaHarness]] — Outer-loop harness code optimization via agentic proposer with full trace access; +7.7pp over SOTA context engineering.
- [[MetaHarnessEndToEndOptimizationOfModelHarnesses]] — Duplicate of MetaHarness.
- [[MtaAgentOpenRecipeForMultimodalDeepSearchAgents/summary]] — Open 32B agent trained on 21K multimodal multi-hop trajectories; beats GPT-5 and Gemini-2.5-Pro.
- [[NativeEvolution/summary]] — Agents spontaneously explore and distill "World Knowledge" docs with no reward; ~20% accuracy gains with cross-model transfer.
- [[NaturalLanguageAgentHarnesses]] — Formalizes harnesses as portable natural-language specs interpreted by a shared runtime.
- [[NemoClawLocalAgent/summary]] — NVIDIA's local agent: 120B model + sandbox + messaging on local GPU with interactive policy approval.
- [[SemaClaw/summary]] — Multi-agent harness framework with DAG orchestration, PermissionBridge runtime safety checkpoints, and three-tier context + wiki-based long-term memory; harness improvements alone yielded +13.7pp task completion with model fixed.
- [[SmallLanguageModelsAreTheFutureOfAgenticAi/summary]] — SLMs (<10B) match 30–70B LLMs on agent sub-tasks at 10–30x lower cost; 6-step migration algorithm.
- [[SynthesizingMultiAgentHarnesses/summary]] — AgentFlow auto-synthesizes multi-agent harnesses via a typed graph DSL (roles, topology, tools, prompts, protocols) guided by runtime diagnostics; discovers 10 Chrome zero-days including 2 Critical CVEs.
- [[TheEvolutionOfToolUseInLLMAgents]] — Survey unifying single→multi-tool orchestration across six dimensions; topology-aware planning is the frontier.
- [[TheLastHarnessYoullEverBuild/summary]] — Two-level meta-learning system: inner loop (Worker/Evaluator/Evolution agents) iteratively improves a harness per task; outer loop optimizes the evolution protocol itself across tasks — zero human harness engineering.
- [[ToolAttentionIsAllYouNeed/summary]] — MCP middleware scoring tools by Intent–Schema Overlap, state-gating, and lazy-loading full schemas only for top-k; cuts per-turn tool tokens 95% (47.3k→2.4k) on a 120-tool simulated benchmark.
- [[TowardsEndToEndAutomationOfAIResearch]] — End-to-end AI research pipeline from ideation to manuscript; produced a paper that passed ICLR workshop review.
- [[UltraLongHorizonAgenticScience/summary]] — ML-Master 2.0: Hierarchical Cognitive Caching memory runs 24h Kaggle ML tasks at 56.4% medal rate.
- [[APracticalGuideToBuildingAgents/summary]] — OpenAI's practical guide covering agent definition, tool taxonomy (data/action/orchestration), single-vs-multi-agent orchestration patterns, and layered guardrails; start simple, add complexity only when needed.
- [[BuildYourOwnAgentHarness/summary]] — iii framework decomposes the harness into ~13 independent WebSocket workers on a shared bus, each exposing capabilities via one `iii.trigger()` primitive; any layer is independently swappable.
- [[AgenticHarnessEngineering/summary]] — AHE auto-evolves coding-agent harnesses using component, trajectory, and decision observability; +7.3pp on Terminal-Bench 2 in ten iterations with cross-model and cross-benchmark transfer.
- [[HarnessEngineering/summary]] — Frames all LLM infrastructure as a deterministic 'harness' via R.E.S.T. + PPAF; treats the harness — not the model — as the differentiating production-grade engineering surface.
- [[BuildingLongRunningAgenticAISystems/summary]] — GAN-inspired Generator-Evaluator-Planner harness for 5+ hour agent runs; live Playwright evaluation and pre-build contract negotiation eliminate self-evaluation blindness; harness complexity shrinks as models improve.
- [[ScalingLawsAgentHarnesses/summary]] — EFC (Effective Feedback Compute) credits harness feedback only when informative, valid, non-redundant, and retained; EFC/D_task hits R² = 0.99 vs 0.33–0.42 for raw tokens/tool calls as a scaling coordinate.
- [[ProactiveAgentTGLTrigger/summary]] — Replaces LLM-as-trigger with a lightweight temporal graph model; joint trigger + entity-routing head in one forward pass gives +16.7 mean F1 across 14 backbones at 11 ms/event, 4–83x faster than LLM triggers.
- [[HarnessUpdatingNotHarnessBenefit/summary]] — Harness-updating is flat across capability tiers (9B matches frontier); harness-benefit is non-monotonic — mid-tier models gain most; weak models fail to load or follow their harness.
- [[AgenticAIOnMacWithMLX/summary]] — Four-layer local agent stack for Mac (MLX → MLX-LM → MLX-LM Server → any OpenAI-compatible framework); Neural Accelerators, continuous batching, and Thunderbolt RDMA enable fully on-device agentic runs.- [[Kernel/summary]] — Managed cloud-browser infrastructure for AI agents; sandboxed Chromium with stealth, auth, and observability built in, billed per second; unikernel architecture claims ~5.8x faster, ~50% cheaper than Browserbase.
- [[ReinforcedAgent/summary]] — Reviewer agent evaluates provisional tool calls before execution, catching errors pre-execution; +5.5% BFCL irrelevance, +7.1% τ²-Bench; reasoning-model reviewers hit 3.1:1 benefit-to-harm ratio.
- [[NOOAObjectOrientedAgents/summary]] — Represents an LLM agent as a plain Python object -- methods are actions, fields are state, docstrings are prompts -- combining six model-facing capabilities no other of 14 surveyed frameworks unify; 82.2% SWE-bench Verified.
