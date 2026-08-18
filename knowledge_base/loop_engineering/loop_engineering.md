# Loop Engineering

Engineering the **agentic control loop** itself — the discipline named by the mid-2026 shift "stop prompting coding agents; design the loops that prompt them." Covers loop architecture (triggers, verifiable goals, stop/exit conditions), loop safety (sandboxed YOLO mode, scoped credentials, verification gates), self-correction as loop design, fleet-scale operation, and the **Ralph loop** lineage (running an agent in a bash `while` loop, one task per iteration, correctness via test/build backpressure).

Distinct from `agent_harness` (the scaffolding *around* a single run) and from "looped transformers" (an architecture). Here the **loop** is the unit of work.

A curated master list of external resources (articles, videos, repos) lives in [[RESOURCES]].

## Papers

- [[LoopEngineering/summary]] — Designing automated loops -- built on automations, worktrees, skills, connectors, and sub-agents -- to drive coding agents without human-in-the-loop prompting each turn. (Addy Osmani)
- [[TheArtOfLoopEngineering/summary]] — Four stacked loops -- agent, verification (rubric grader), event-driven (Slack/webhooks/cron), and hill-climbing (trace-driven auto-improvement) -- that compound in value the longer they run. (LangChain)
- [[LoopEngineeringCobusGreyling/summary]] — Loop engineering as the third era after context and harness engineering; six primitives (scheduling, worktrees, skills, MCP, sub-agents, memory); you design systems that prompt agents. (Cobus Greyling)
- [[DesigningAgenticLoops/summary]] — Designing safe agentic loops: sandboxed YOLO mode, tightly-scoped credentials, AGENTS.md over MCP, and picking tasks with objective success signals (tests pass). (Simon Willison)
- [[DesigningLoopsWithFable5/summary]] — Rubric-based feedback loops (`/goal` in Claude Code, `Outcomes` in CMA) let Fable 5 hillclimb autonomously; ~6x improvement over Opus 4.7 on ML optimization, 73% cross-session memory verification coverage.
- [[LoopEngineeringFleetRuntime/summary]] — Scaling loop engineering to production fleets: per-agent identity, routing fallbacks, prompt-injection guardrails at four hooks, versioned skills, and GitOps-style fleet policy. (TrueFoundry)
- [[LoopEngineeringWorksOnMemory/summary]] — Argues the loop's memory -- what the agent retains between iterations -- is the single biggest factor in whether long-running automated loops actually work. (mem0)
- [[HowToCreateLoopsWithClaude/summary]] — Practitioner walkthrough of building self-running loops with Claude Code: schedule the agent, track progress in a file, self-check, and stop only on real completion.
- [[WtfIsALoop/summary]] — Explains the viral "design loops that prompt your agents" framing (Steinberger vs. Cherny); since code is now cheap, the real skill is making loops know when to stop.
- [[PowerOfAgenticLoops/summary]] — Flexbox engine (~800 LOC, ~350 tests) built in 3 hours via a VS Code agent loop; feedback-mechanism quality matters more than prompt quality. (Colin Eberhardt, Scott Logic)
- [[LoopEngineeringExplained/summary]] — Reframes agent building: the six-line loop is solved; engineering moved to the harness around it. Four hard parts — stop conditions, context hygiene, a tight tool set, an independent verifier. (Akshay Pachaar)
- [[TheKitchenLoopUserSpecDrivenDevelopmentForASelfEvolvingCodebase]] — Autonomous software evolution via synthetic power-user testing; 285+ iterations, 0 regressions, $0.38/PR.
- [[RalphWiggumSoftwareEngineer/summary]] — The originating Ralph spec: run a coding agent in a bash while-loop, one task per iteration, correctness from test/build backpressure; $50k contract delivered for $297. (Geoffrey Huntley)
- [[EverythingIsARalphLoop/summary]] — Huntley's manifesto that the self-improving loop is the primitive unit of software; monolith over multi-agent, engineer away each failure domain permanently.
- [[BriefHistoryOfRalph/summary]] — Chronology of the Ralph technique (Jun 2025–Jan 2026): fresh isolated context per iteration and spec quality are the real bottlenecks, not loop mechanics. (HumanLayer)
- [[InventingTheRalphWiggumLoop/summary]] — Huntley on inventing Ralph: context window as a managed sliding array, one task per loop to avoid context rot/compaction; ~$10/hr commoditizes software development. (Dev Interrupted podcast)
- [[RalphWiggumLoopFromFirstPrinciples/summary]] — Live first-principles walkthrough of the Ralph loop: spec-first workflow, context-window-as-array, the `specs/README` PIN lookup table, and the Loom platform. (video)
- [[AgentLoopsCompleteGuide/summary]] — Loop primitives across Claude Code + Codex (`/loop`, `/goal`, `/schedule`); five-part loop anatomy; the worker never grades itself -- always use an independent verifier. (video)
- [[HowToRalphWiggum/summary]] — Canonical Ralph reference repo: while-loop + PROMPT.md, IMPLEMENTATION_PLAN.md as persistent shared state, separate plan/build prompts, parallel-read subagents. (repo)
- [[AwesomeRalph/summary]] — Curated awesome-list of Ralph resources: official essays, the "3 phases, 2 prompts, 1 loop" playbook, 15 implementations across tools, and community threads. (repo)
- [[RalphLoopPlugin/summary]] — Anthropic's official Claude Code `ralph-loop` plugin: a Stop hook blocks session exit and re-injects the prompt until a completion promise or max-iterations fires. (repo)
- [[RalphLoopAgent/summary]] — Vercel's ~400-LOC AI SDK wrapper: a while-true outer loop around `generateText` until a `verifyCompletion` predicate passes; composable iteration/token/cost stop conditions. (repo)
- [[LoopEngineeringRepo/summary]] — Vendor-agnostic loop-engineering scaffold: seven loop patterns plus CLI tools (`loop-init`/`loop-audit`/`loop-cost`); `patterns/registry.yaml` defines cadence, risk, gates, cost. (Cobus Greyling, repo)
</content>
