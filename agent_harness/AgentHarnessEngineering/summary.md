# Agent Harness Engineering

**Paper:** [Agent Harness Engineering (Addy Osmani, 2026)](https://addyosmani.com/blog/agent-harness-engineering/)

## Human Readable TL;DR

Think of an AI agent like a race car driver. The engine (the model) matters, but what really wins the race is everything around the driver -- the car, the pit crew, the safety rails, the rulebook, the radio with the team. This post argues that most of the work to make AI agents actually useful isn't about getting a smarter model; it's about building the garage, track, and rulebook around it. And the best rulebooks aren't written from scratch -- they're written by writing down every mistake the agent has ever made so it never repeats them.

## TL;DR

Osmani reframes agent development around Viv Trivedy's formulation "Agent = Model + Harness," arguing that the harness (prompts, tools, hooks, filesystem, orchestration, observability) carries most of the engineering leverage rather than the underlying model. He introduces the "ratchet principle" -- every rule in `AGENTS.md` should trace to a specific past failure -- and surveys core harness patterns (context compaction, tool-call offloading, progressive disclosure, Ralph loops, planner/generator/evaluator separation, success-silent feedback). He points to Claude Code as the clearest public reference architecture and predicts an industry shift from LLM-API-as-platform to harness-as-a-service, with eventual dynamic harness assembly replacing static pre-configuration.

---

## Problem & Motivation

The dominant narrative treats agent quality as primarily a function of model capability: wait for the next version, get better agents. Osmani argues this misreads where the leverage actually sits. Evidence: on Terminal Bench 2.0, the same Claude Opus 4.6 model performs dramatically differently across harnesses, and Viv Trivedy's team jumped from Top 30 to Top 5 by modifying only the harness. The gap between what models *can* do and what agents *actually* accomplish is largely a harness gap. Practitioners need a framework and vocabulary for engineering that harness deliberately instead of accumulating scaffolding ad hoc.

---

## Main Original Ideas

1. **Agent = Model + Harness (via Trivedy).** A raw model isn't an agent. The harness -- system prompts, `CLAUDE.md`/`AGENTS.md`, tools, MCP servers, sandbox, hooks, orchestration, observability -- is what turns completions into an agent. Osmani promotes this equation from slogan to organizing principle.

2. **The "Skill Issue" Reframe.** Agent failures are configuration problems, not model-capability ceilings. Treat every failure as a legible signal demanding a harness change rather than as a reason to wait for the next model release.

3. **The Ratchet Principle.** Every rule in a good `AGENTS.md` should be traceable to a specific past failure. Mistakes become permanent constraints, so the harness monotonically hardens over time rather than drifting.

4. **Working Backwards from Behavior.** Derive each harness component from the behavior it enables (durable work, safe execution, long-horizon planning, etc.). If you can't name the behavior a component serves, delete it.

5. **Context Rot as Architecture Problem.** Model quality degrades as context fills. This is architectural, not parametric, and demands three mitigations: compaction, tool-call offloading (summary in context, full output on disk), and skills with progressive disclosure.

6. **Ralph Loop Pattern.** A hook intercepts completion attempts and re-injects the original prompt into a fresh context, using the filesystem as cross-iteration state. Makes truly long-horizon work tractable without drowning in context.

7. **Planner / Generator / Evaluator Separation.** Agents skew positive when grading their own work, so split roles across agents. Pair with a "sprint contract" -- negotiate completion criteria before implementation starts.

8. **Success-Silent, Failures-Verbose Feedback.** Successful operations return nothing; failures inject rich error detail. Feedback loops stay efficient, context stays clean during the happy path.

9. **Harness-as-a-Service (HaaS).** The platform boundary is moving up the stack: from LLM APIs that return completions to harness APIs (Claude Agent SDK, Codex SDK, OpenAI Agents SDK) that return runtimes with loops, tools, context management, and hooks built in. Differentiation shifts to domain-specific prompts and tools.

10. **Model-Harness Co-Evolution.** Useful harness primitives get standardized, folded into post-training, and the next model generation is better at those primitives -- a feedback loop that couples model progress to harness design.

---

## Key Findings

- **Same model, different harnesses, drastically different benchmarks.** Claude Opus 4.6 on Terminal Bench 2.0 shows large performance deltas purely from harness changes; Viv's Top 30 → Top 5 jump came from harness, not model.
- **Mature coding agents converge.** Claude Code, Cursor, Codex, Aider, and Cline "look more like each other than their underlying models do," indicating the field is discovering load-bearing harness patterns.
- **Tool count is not neutral.** Ten focused tools beat fifty overlapping ones; model performance degrades when tool menus exceed working memory.
- **Rulebooks stay short.** HumanLayer's `AGENTS.md` stays under ~60 lines -- a pilot's checklist, not a style guide.
- **Tool descriptions are a security boundary.** They populate every prompt; malicious or sloppy MCPs can prompt-inject the agent.
- **Claude Code architecture** (per Fareed Khan) is the clearest public reference, with input / knowledge / integration / execution / output / observability / multi-agent layers around a master loop.

---

## Suggestions & Future Directions

1. **Parallel multi-agent coordination.** Orchestrating many agents working concurrently on a shared codebase without stepping on each other remains an open problem.
2. **Self-improving harnesses.** Agents that analyze their own traces to identify and patch harness-level failure modes automatically.
3. **Dynamic harness assembly.** Shift from static pre-configuration toward something "closer to a compiler" -- selecting tools, skills, and context just-in-time from the task itself.
4. **Harness hygiene as models improve.** When new model capabilities make old scaffolding obsolete, remove it; when new capabilities unlock new failure modes, add scaffolding for those. Harnesses are living systems.
5. **External evaluators over self-grading.** Bake planner/generator/evaluator separation into standard agent architectures rather than trusting self-assessment.
6. **Structured hand-offs for extreme long-horizon work.** When compaction is insufficient, use full context resets with hand-off files on disk (Anthropic's observation).

---

## Authors & Institutions

Addy Osmani (Google Chrome, writing in a personal capacity). Draws extensively on work and framings from Viv Trivedy, HumanLayer, Fareed Khan, and Anthropic.
