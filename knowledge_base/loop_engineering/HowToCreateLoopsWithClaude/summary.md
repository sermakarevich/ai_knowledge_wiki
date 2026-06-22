# How to Create Loops with Claude

**Article:** [How to Create Loops with Claude (MIKE @mikenevermiss, Jun 15, 2026)](https://x.com/mikenevermiss/status/2066401066518802637)

## Human Readable TL;DR

Imagine instead of asking your assistant one question at a time, you built a machine that asks questions for you, checks the answers, remembers what happened last time, and keeps going while you sleep. That is what a "loop" is -- an automated system that runs your AI agent on a schedule, tracks progress in a file, checks its own work, and stops only when something real is accomplished. Your job shifts from crafting perfect questions to designing the machine that asks them.

## TL;DR

This article argues that the leverage point in AI-assisted development has moved from prompt engineering to loop design: autonomous, recursive agent pipelines that fire without human input, maintain persistent state in a memory file, use a separate evaluator agent to check work against objective criteria, isolate parallel tasks with git worktrees, and enforce hard stop conditions. It synthesizes patterns from Boris Cherny (Anthropic), Peter Steinberger, Addy Osmani, and Geoffrey Huntley into a concrete six-part framework and a progressive autonomy ladder.

---

## Problem & Motivation

Crafting individual prompts delivers one response and stops. As AI coding agents become capable of multi-step work, the bottleneck is no longer the quality of a single message but the absence of infrastructure that sends messages continuously, reviews results, and decides what happens next. Boris Cherny (head of Claude Code at Anthropic) and Peter Steinberger both independently state they no longer prompt agents -- they write loops that do the prompting for them.

---

## Main Original Ideas

1. **The Loop as the Unit of Leverage** -- A loop is a recursive goal: an automation fires, the agent iterates against a purpose, and a stopping condition ends the run. The agent forgets between runs; the loop's memory file does not. This asymmetry is the entire architecture.

2. **Six-Part Loop Anatomy (Osmani's Framework)** -- Every working loop combines some subset of: automations (cron, webhooks, hooks), worktrees (git isolation for parallel agents), skills (procedure manuals the agent reads), connectors (integrations to external systems), sub-agents (delegated task runners), and memory (a state file on disk that survives between runs).

3. **The PROGRESS.md Pattern** -- A single markdown file readable and writable by every loop iteration is the loop's only memory. It holds: what was done last run, what is in progress, what is blocked, what to try next. Without it every run starts from zero.

4. **Evaluator-Optimizer Separation** -- The agent that writes code is too optimistic grading its own work. A second agent verifies against a hard objective gate (test suite, type checker, build command) rather than giving an opinion. A second agent with no objective signal just adds a second optimist.

5. **Hard Stop Conditions and the Ralph Wiggum Anti-Pattern** -- A loop without a real exit condition fails quietly: the agent emits a completion signal before the work is done and the loop exits believing success. Stop conditions must be verifiable by something other than the agent's own claim, plus a maximum iteration ceiling as backstop.

6. **The Autonomy Ladder** -- New loops start at level 1 (suggest only) or level 2 (draft for human to apply), graduate to level 3 (apply low-risk changes, require approval before publish), and only earn level 4 (fully autonomous with audit logs) after consistently producing work that requires no corrections.

7. **Compounding Loops** -- The second loop connects to the first: a triage loop writes findings to a shared state file; an action loop reads that file and picks the highest-priority item. Skills compound too -- a skill file written once for CI failure triage is read by every future loop that touches CI.

---

## Key Findings

- One automation writing one state file already provides more leverage than hundreds of well-crafted prompts because it runs without the user present.
- Worktrees are mandatory once more than one agent touches the same codebase -- without isolation, concurrent edits corrupt each other's changes.
- A command allowlist (restricting agents to specific shell commands like `npm`, `git`, `ls`, `cat`) is the first security control for any loop with shell access.
- Token cost compounds: a bad single iteration wastes a prompt; a bad unattended loop running overnight generates a bill. Manual test for 3--5 iterations to establish per-iteration token cost before releasing a loop to run unsupervised.
- The daily work of the loop author shifts from opening a chat window to opening a triage inbox: reviewing overnight findings, correcting what the loop got wrong, and designing the next loop.

---

## Suggestions & Future Directions

1. Start with a single cron-triggered automation that writes one state file -- resist building the full six-part system immediately.
2. Run every new loop at autonomy level 1 or 2 for a week before promoting it; correct errors in output before trusting it at level 3.
3. Build the second loop to connect to the first rather than run in isolation, so discoveries flow automatically into action queues.
4. Define run-that-finds-nothing behavior explicitly (silent archive) so the triage inbox only surfaces real signal.
5. Invest in skill files early -- they compound across every future loop that touches the same domain.

---

## Authors & Institutions

MIKE (@mikenevermiss) -- independent; synthesizing patterns from Boris Cherny (Anthropic / Claude Code), Peter Steinberger (PSPDFKit), Addy Osmani (Google), Geoffrey Huntley (independent).
