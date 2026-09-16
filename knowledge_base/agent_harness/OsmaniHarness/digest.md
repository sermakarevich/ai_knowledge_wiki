> [[index|Wiki]] | [[summary|Summary]]

# OsmaniHarness — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-foundations-behaviour|Foundations: what a harness is, ratchet, behaviour-first]]

**In one sentence:** A coding agent's behaviour is dominated not by which model you pick but by the harness around it, so every agent failure should be permanently engineered into the harness as a rule.

- A coding agent equals the model plus everything built around it, and harness engineering means tightening that scaffolding every time the agent slips so the same mistake never recurs.
- A decent model with a great harness beats a great model with a bad harness, because tools like Claude Code, Cursor, Codex, Aider, and Cline share underlying models yet behave differently due to harness design.
- A harness is all non-model code, configuration, and execution logic: system prompts, CLAUDE.md / AGENTS.md / skills / subagent prompts, tools / MCP servers and descriptions, filesystem / sandbox / browser, orchestration (spawning, handoffs, routing), hooks and middleware, plus observability (logs, traces, cost/latency).
- Simon Willison's reduction — an agent is a system that "runs tools in a loop to achieve a goal" — locates the skill in designing both the tools and the loop.
- Most agent failures are configuration ("skill issues"), not model-weight problems: missing conventions go into AGENTS.md, destructive commands get blocking hooks, 40-step tasks get split into planner plus executor, and false "done" outputs get typecheck back-pressure wired into the loop.
- On Terminal Bench 2.0, Claude Opus 4.6 scores far lower inside Claude Code than inside a custom harness, and Viv's team moved a coding agent from Top 30 to Top 5 by changing only the harness, since models are post-training-coupled to their training harness.
- The ratchet habit: add a constraint only after a real failure (e.g. a merged PR with a commented-out test yields an AGENTS.md rule, a pre-commit grep for `.skip(` and `xit(`, and a reviewer-subagent blocker), and remove constraints only when a capable model makes them redundant.

## 2. [[wiki/02-primitives-production|Primitives and production: filesystem to HaaS]]

**In one sentence:** Every harness component exists to deliver a specific desired behaviour, from filesystem and bash through memory, context management, hooks, and verification loops, and as models improve the scaffolding moves rather than disappears — converging on Harness-as-a-Service runtimes you configure instead of build.

- Design working backwards from behaviour: behaviour wanted (or to fix) → harness piece that delivers it; any component without a named behavioural job should not exist.
- Filesystem plus Git is the foundational primitive — workspace for code/data/docs, offload for intermediate work, coordination surface for agents and humans — with versioning giving progress tracking, rollback, and branching.
- Bash plus code execution is the default general-purpose tool strategy (ReAct loop: reason → tool call → observe → repeat), because agents excel at shell and pre-building every tool is infeasible.
- Context rot is fought with four mechanisms: compaction (summarize/offload old context), tool-call offloading (head/tail in context, full 2,000-line outputs on disk), skills with progressive disclosure, and full context resets with a hand-off file for long jobs.
- Long-horizon work needs Ralph Loops (hook intercepts exit, re-injects original prompt into fresh context against a completion goal, state via filesystem), plan files plus self-verification, and generator/evaluator splits because self-grading skews positive.
- Hooks are the enforcement layer (run on lifecycle points: before tool call, after edit, before commit, session start) with the rule "success is silent, failures are verbose"; AGENTS.md stays short (HumanLayer: under 60 lines, earn each line) and ten focused tools beat fifty overlapping ones.
- Production proof is Claude Code (Fareed Khan breakdown): context injection, memory store, worktree isolator, permission gate with destructive-action hooks, subagent context firewalls, tool dispatch registry — and the Anthropic rule that every harness component encodes an assumption about what the model cannot do alone, so Opus 4.6 killed context-anxiety scaffolding but created need for multi-day memory and multi-agent coordination.
- The industry is moving from LLM APIs (give you a completion) to Harness-as-a-Service APIs (Claude Agent SDK, Codex SDK, OpenAI Agents SDK give you loop, tools, context, hooks, sandboxes); configure the four pillars (system prompt, tools, context, subagents) and iterate from a v0.1.

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. Agent behaviour is dominated by the harness around the model, not the model choice.
2. Every agent failure gets permanently engineered into the harness as a ratchet rule.
3. Each harness component earns its place by delivering one named desired behaviour.
4. Context, memory, hooks, and verification loops carry long-horizon work to done.
5. As models improve the scaffolding moves rather than disappears, converging on configurable Harness-as-a-Service.
<!-- FIVE_MOVES_END -->
