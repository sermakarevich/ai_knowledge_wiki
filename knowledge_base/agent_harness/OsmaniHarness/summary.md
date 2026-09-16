# Agent Harness Engineering

**Article:** [Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/) — Addy Osmani, addyosmani.com, 2026-04-19

## Human Readable TL;DR

Imagine a talented chef dropped into two kitchens: one with sharp knives, labelled ingredients, and someone cleaning up as they go; the other a mess. Same chef, very different dinner. A coding agent works the same way — the model is the chef, and the harness (everything built around it: prompts, tools, files, checks, logs) is the kitchen. This article argues that most of what makes an AI coding agent good or bad is the kitchen, not the chef, and that every time the agent messes up, you should permanently fix the kitchen so it can't happen again.

## TL;DR

Coding agent = model + harness, and the harness — system prompts, AGENTS.md/CLAUDE.md, tools/MCP servers, filesystem/sandbox, orchestration, hooks, observability — dominates observed behaviour more than model choice: the same model scores very differently across Claude Code, Cursor, Codex, Aider, and Cline, and one team moved from Top 30 to Top 5 on Terminal Bench 2.0 by changing only the harness. Most agent failures are "skill issues" (configuration, not model weights), fixed via the ratchet — turn every real failure into a permanent rule (AGENTS.md line, blocking hook, reviewer-subagent check) and only remove a rule once a capable model makes it redundant. The rest of the piece works backwards from behaviour through the primitives that make up a harness: filesystem+Git (durable state), bash/code execution (the default general-purpose tool, ReAct loop), sandboxes, memory via AGENTS.md and web search/MCP, four defences against context rot (compaction, tool-call offloading, skills with progressive disclosure, full context resets), long-horizon execution (Ralph Loops, plan files, generator/evaluator splits because self-grading skews positive), hooks ("success is silent, failures are verbose"), and short/earned AGENTS.md plus a handful of focused tools. Claude Code's architecture is used as the production proof point, and the piece closes by arguing the industry is shifting from LLM APIs to Harness-as-a-Service (Claude Agent SDK, Codex SDK, OpenAI Agents SDK): you configure four pillars (system prompt, tools, context, subagents) and iterate from a v0.1, because scaffolding doesn't disappear as models improve — it moves to cover new gaps (multi-day memory, multi-agent coordination).

---

## Problem & Motivation

Two years of industry debate have focused on which model is smartest, cleanest at code, or least prone to hallucination — but the model is only one input into a running agent; the rest is the harness. Osmani pulls together Viv Trivedy's "harness engineering" coinage, HumanLayer's "skill issue" framing, Anthropic's long-running-work engineering post, and Fareed Khan's Claude Code architecture breakdown into one argument: the leverage that actually determines whether an agent ships useful work sits in the scaffolding around the model, not in swapping model versions. See [[wiki/01-foundations-behaviour|foundations]].

---

## Main Original Ideas

1. **Agent = Model + Harness, and harness is everything else** — system prompts (CLAUDE.md/AGENTS.md/skills/subagent prompts), tools/MCP servers, filesystem/sandbox/browser, orchestration (spawning, handoffs, routing), hooks/middleware, and observability (logs, traces, cost/latency).
2. **The ratchet** — treat every agent mistake as a permanent signal: a merged PR with a commented-out test becomes an AGENTS.md rule, a pre-commit grep for `.skip(`/`xit(`, and a reviewer-subagent blocker. Add constraints only after a real failure; remove them only when a capable model makes them redundant.
3. **Working backwards from behaviour** — for every harness component, name the specific behaviour it exists to deliver; a component with no named job shouldn't exist.
4. **Four context-rot defences** — compaction, tool-call offloading (head/tail in context, full output on disk), skills with progressive disclosure, and full context resets with a hand-off file.
5. **Long-horizon primitives** — Ralph Loops (a hook re-injects the original prompt into fresh context against a completion goal, state kept on the filesystem), plan files plus self-verification, and generator/evaluator splits because self-grading skews positive.
6. **Harness-as-a-Service (HaaS)** — the industry is moving from LLM APIs (a completion) to harness APIs (a runtime: loop, tools, context, hooks, sandboxes) such as the Claude Agent SDK, Codex SDK, and OpenAI Agents SDK; configure four pillars and iterate from a v0.1.

---

## Key Findings

| Claim | Evidence given |
|---|---|
| Harness dominates model choice | Claude Opus 4.6 scores far lower inside Claude Code than inside a custom harness on Terminal Bench 2.0 |
| Harness-only changes move rankings a lot | Viv's team moved a coding agent from Top 30 to Top 5 by changing only the harness |
| AGENTS.md should stay short | HumanLayer rule of thumb: under 60 lines, earn each line |
| Fewer tools beat more tools | Ten focused tools outperform fifty overlapping ones (model holds the "menu" better) |
| Self-grading skews positive | Motivates the generator/evaluator split and sprint-contract "done" negotiation pattern |
| Scaffolding moves, doesn't vanish | Opus 4.6 killed context-anxiety scaffolding (premature "wrapping up" near context limits) but created need for multi-day memory and multi-agent coordination |

- Production proof point: Fareed Khan's Claude Code breakdown maps almost every harness concept in the piece (context injection, memory store, worktree isolator, permission gate with destructive-action hooks, subagent context firewalls, tool dispatch registry) onto one shipping product.
- A named security note: tool/MCP descriptions are trusted text injected into the prompt every request, so a sloppy or malicious MCP server can prompt-inject an agent before the user has typed anything.

---

## Suggestions & Future Directions

1. Orchestrate many agents working in parallel on a shared codebase.
2. Build agents that analyze their own traces to identify and fix harness-level failure modes.
3. Move from static, pre-configured harnesses toward ones that dynamically assemble the right tools and context just-in-time for a given task.

---

## Authors & Institutions

Addy Osmani, addyosmani.com. Published 2026-04-19. Synthesizes and cites Viv Trivedy ("Anatomy of an Agent Harness"), Dex Horthy, HumanLayer, Anthropic's engineering team, Birgitta Böckeler, Simon Willison, and Fareed Khan's Claude Code architecture breakdown.
