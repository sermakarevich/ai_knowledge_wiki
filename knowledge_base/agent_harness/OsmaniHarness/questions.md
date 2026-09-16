---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# OsmaniHarness — Retrieval Practice

## Section 1: Foundations: what a harness is, ratchet, behaviour-first

### Q1 (core recall): What is a harness, and what two numbers prove a decent model with a great harness beats a great model with a bad harness?

<details>
<summary>Answer</summary>

A harness is all non-model code, configuration, and execution logic around the model: system prompts, CLAUDE.md / AGENTS.md / skills / subagent prompts, tools / MCP servers and descriptions, filesystem / sandbox / browser, orchestration (spawning, handoffs, routing), hooks and middleware, plus observability (logs, traces, cost/latency). Proof: on Terminal Bench 2.0, Claude Opus 4.6 scores far lower inside Claude Code than inside a custom harness, and Viv's team moved a coding agent from Top 30 to Top 5 by changing only the harness. Same shared models (Claude Code, Cursor, Codex, Aider, Cline) behave differently because of harness design, and models are post-training-coupled to their training harness.

</details>

### Q2 (elaboration): Why add a harness constraint only after a real failure — what breaks if you add rules preemptively?

<details>
<summary>Answer</summary>

The ratchet habit: every agent failure gets permanently engineered into the harness as a rule (e.g. a merged PR with a commented-out test yields an AGENTS.md rule, a pre-commit grep for `.skip(` and `xit(`, and a reviewer-subagent blocker). Adding constraints only after real failures keeps the harness lean and tied to observed behaviour. Preemptive rules bloat the harness, add unneeded context and friction, and rot: remove constraints when a capable model makes them redundant. Most failures are configuration ("skill issues"), so the fix is targeted — missing conventions go into AGENTS.md, destructive commands get blocking hooks, 40-step tasks get split into planner plus executor, false "done" outputs get typecheck back-pressure.

</details>

## Section 2: Primitives and production: filesystem to HaaS

### Q3 (core recall): What are the four context-rot defences, and what are the three numbers attached to hooks, AGENTS.md, and tool counts?

<details>
<summary>Answer</summary>

Four context-rot defences: compaction (summarize/offload old context), tool-call offloading (head/tail in context, full 2,000-line outputs on disk), skills with progressive disclosure, and full context resets with a hand-off file for long jobs. Numbers: AGENTS.md stays short (HumanLayer rule: under 60 lines, earn each line), ten focused tools beat fifty overlapping ones, and hooks follow "success is silent, failures are verbose" — running on lifecycle points (before tool call, after edit, before commit, session start).

</details>

### Q4 (core recall): What are Ralph Loops and the four HaaS pillars, and what did Opus 4.6 kill and create?

<details>
<summary>Answer</summary>

Ralph Loops: a hook intercepts exit and re-injects the original prompt into fresh context against a completion goal, with state kept via the filesystem — used with plan files plus self-verification for long-horizon work. Harness-as-a-Service (Claude Agent SDK, Codex SDK, OpenAI Agents SDK) gives you the loop, tools, context, hooks, and sandboxes; you configure the four pillars (system prompt, tools, context, subagents) and iterate from a v0.1. Anthropic's rule: every harness component encodes an assumption about what the model cannot do alone — so Opus 4.6 killed context-anxiety scaffolding but created need for multi-day memory and multi-agent coordination. Production proof is Claude Code (Fareed Khan breakdown): context injection, memory store, worktree isolator, permission gate with destructive-action hooks, subagent context firewalls, tool dispatch registry.

</details>

### Q5 (elaboration): Why split generator from evaluator instead of letting an agent grade itself — what breaks with self-grading?

<details>
<summary>Answer</summary>

Self-grading skews positive: the same agent that produced the work overrates it, so false "done" outputs pass. The split (generator/evaluator, plan files plus self-verification, typecheck back-pressure wired into the loop) adds independent verification. Design working backwards from behaviour — behaviour wanted (or to fix) → harness piece that delivers it — so any component without a named behavioural job should not exist. Bash plus code execution stays the default tool strategy (ReAct loop: reason → tool call → observe → repeat) because pre-building every tool is infeasible; filesystem plus Git is the foundational primitive (workspace, offload, coordination surface, with versioning for tracking, rollback, branching).

</details>

### Q6 (transfer): Your file-watching coding agent keeps corrupting the repo with untested edits and getting lost after 50+ steps. Which harness pieces from the digest would you add, in what order?

<details>
<summary>Answer</summary>

Working backwards from the two behaviours: (1) stop destructive untested edits — add a permission gate with destructive-action hooks plus an after-edit hook that runs typecheck/tests as back-pressure, and a pre-commit grep blocking `.skip(` / `xit(` style cheats; (2) survive 50+ steps — split into planner plus executor with plan files, run a Ralph Loop (fresh context re-injected against a completion goal, state on filesystem/Git), compact or fully reset context with a hand-off file, and offload long tool outputs (head/tail in context, full output on disk). Keep AGENTS.md under 60 lines with only earned rules, prefer ten focused tools over fifty, and ratchet each new rule from a real failure.

</details>

### Q7 (evaluation, see [[critical_thinking|Critical Analysis]]): The article claims "harness beats model choice," backed by qualitative examples (a Terminal Bench score gap, a Top 30 to Top 5 jump). Why is this weaker evidence than it looks, and what would make it strong?

<details>
<summary>Answer</summary>

The examples are borrowed from Viv Trivedy's write-up and stated as directional facts ("far lower," "Top 30 to Top 5") with no benchmark table, no control for prompt/tool differences between harnesses, and no run-to-run variance reported — so the claim is asserted by authority, not demonstrated with data in this piece. Stronger evidence would look like [[TheHarnessEffect/summary|The Harness Effect]]: a controlled swap holding tasks and models fixed while only changing the orchestration layer, with quantified deltas (cost, latency, tokens, quality) across multiple models — which is exactly the kind of measurement this article's central claim is missing.

</details>
