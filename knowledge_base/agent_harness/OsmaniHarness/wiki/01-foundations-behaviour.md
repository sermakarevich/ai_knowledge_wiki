> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Foundations: what a harness is, ratchet, behaviour-first

**In one sentence:** A coding agent's behaviour is dominated not by which model you pick but by the harness around it, so every agent failure should be permanently engineered into the harness as a rule.

## Key points
- A coding agent equals the model plus everything built around it, and harness engineering means tightening that scaffolding every time the agent slips so the same mistake never recurs.
- A decent model with a great harness beats a great model with a bad harness, because tools like Claude Code, Cursor, Codex, Aider, and Cline share underlying models yet behave differently due to harness design.
- A harness is all non-model code, configuration, and execution logic: system prompts, CLAUDE.md / AGENTS.md / skills / subagent prompts, tools / MCP servers and descriptions, filesystem / sandbox / browser, orchestration (spawning, handoffs, routing), hooks and middleware, plus observability (logs, traces, cost/latency).
- Simon Willison's reduction — an agent is a system that "runs tools in a loop to achieve a goal" — locates the skill in designing both the tools and the loop.
- Most agent failures are configuration ("skill issues"), not model-weight problems: missing conventions go into AGENTS.md, destructive commands get blocking hooks, 40-step tasks get split into planner plus executor, and false "done" outputs get typecheck back-pressure wired into the loop.
- On Terminal Bench 2.0, Claude Opus 4.6 scores far lower inside Claude Code than inside a custom harness, and Viv's team moved a coding agent from Top 30 to Top 5 by changing only the harness, since models are post-training-coupled to their training harness.
- The ratchet habit: add a constraint only after a real failure (e.g. a merged PR with a commented-out test yields an AGENTS.md rule, a pre-commit grep for `.skip(` and `xit(`, and a reviewer-subagent blocker), and remove constraints only when a capable model makes them redundant.

---

## The other half of the system

Two years of debate have centred on models — which is smartest, writes the cleanest React, hallucinates least. That conversation misses the other half: the model is one input into a running agent, and the rest is the harness.

The discipline now has a name. Viv Trivedy coined "harness engineering" and derived what a harness is and why each piece exists in his "Anatomy of an Agent Harness" post. Related threads pulled together here:

- Viv Trivedy — "Anatomy of an Agent Harness"
- Dex Horthy — tracking the pattern as it emerges
- HumanLayer — most agent failures are "skill issues" from configuration, not weights
- Anthropic's engineering team — public breakdown of designing a harness for long-running work
- Birgitta Böckeler — overview from the user's side

Core rule, stated roughly in the chunk:

> Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again.

## What is a harness, really?

Viv's one-liner:

> Agent = Model + Harness. If you're not the model, you're the harness.

A raw model is not an agent. It becomes one once a harness gives it state, tool execution, feedback loops, and enforceable constraints. Concretely, a harness includes:

| Layer | Contents (per chunk) |
|---|---|
| Prompts | System prompts, CLAUDE.md, AGENTS.md, skill files, subagent prompts |
| Tools | Tools, skills, MCP servers, and their descriptions |
| Infrastructure | Bundled filesystem, sandbox, browser |
| Orchestration | Subagent spawning, handoffs, model routing |
| Determinism | Hooks and middleware for deterministic execution (compaction, continuation, lint checks) |
| Observability | Logs, traces, cost and latency metering |

Two framing equations from the chunk:

- `coding agent = AI model(s) + harness` (Viv, echoed by HumanLayer)
- Simon Willison: an agent is a system that "runs tools in a loop to achieve a goal"

The leverage point: the debate over the left-hand side (the model) is loud, but most actual leverage sits on the right-hand side (the harness). Claude Code, Cursor, Codex, Aider, Cline are all harnesses — sometimes over the same model — and the behaviour experienced by the user is dominated by what the harness does. That surface area belongs to the builder, not the model provider.

## The "skill issue" reframe

The familiar anti-pattern: the agent does something dumb, the engineer blames the model, and the fix is filed under "wait for the next version." The harness-engineering mindset rejects that default because the failure is usually legible and fixable in configuration. The chunk's four canonical examples:

1. Agent didn't know a convention → add it to AGENTS.md.
2. Agent ran a destructive command → add a hook that blocks it.
3. Agent got lost in a 40-step task → split it into a planner and an executor.
4. Agent kept "finishing" broken code → wire a typecheck back-pressure signal into the loop.

HumanLayer's summary: "it's not a model problem. It's a configuration problem." Harness engineering is taking that seriously.

The striking data point, appearing in both Viv's write-up and HumanLayer's:

- On Terminal Bench 2.0, Claude Opus 4.6 running inside Claude Code scores far lower than the same model running in a custom harness.
- Viv's team moved a coding agent from Top 30 to Top 5 by changing only the harness.
- Mechanism: models get post-training coupled to the harness they were trained against, so moving them into a different harness — better tools for the codebase, tighter prompt, sharper back-pressure — can unlock capability the original harness left on the floor.

This is the opposite of the "just wait for GPT-6" narrative: the gap between what today's models can do and what is observed is largely a harness gap.

## The ratchet: every mistake becomes a rule

The most important habit: treat agent mistakes as permanent signals, not one-off stories or "bad runs" to retry.

Worked example from the chunk: the agent ships a PR with a commented-out test and it gets merged by accident. The ratchet response has three layers:

1. The next version of AGENTS.md says "never comment out tests; delete them or fix them."
2. The next version of the pre-commit hook greps for `.skip(` and `xit(` in the diff.
3. The next version of the reviewer subagent flags commented-out tests as a blocker.

Rules for the ratchet itself:

- Only add constraints when a real failure has been seen — every line in a good AGENTS.md should be traceable back to a specific thing that went wrong.
- Only remove constraints when a capable model has made them redundant.
- Consequence: harness engineering is a discipline rather than a framework — the right harness for a codebase is shaped by its failure history and can't simply be downloaded.

**Covers:** chunk 01
