# Agent Loops: Complete Guide (Claude Code + Codex)

**Video:** [Agent Loops: Complete Guide (Claude Code + Codex)](https://www.youtube.com/watch?v=RVEaDvh6f5A)
**Channel:** [Owain Lewis](https://www.youtube.com/@owainlewis) | **Published:** June 2026

---

## Human Readable TL;DR

Most people use AI coding assistants like a smarter autocomplete -- you ask, it answers, done. This video explains the next step: instead of you asking the AI every time, you set up a "loop" -- a system that asks the AI automatically, on a schedule or whenever something happens (like a new bug report). Think of it like setting up a reliable employee who checks for problems, fixes them, and sends you a report -- without you having to be awake or nearby. The video covers how to do this with two tools (Claude Code and OpenAI Codex), what can go wrong (mainly: unexpected costs and the AI confidently doing the wrong thing), and how to set up safety checks.

## TL;DR

Agent loops shift AI coding workflows from manual, one-off prompts to automated systems that trigger Claude or Codex on a schedule, event, or condition. The video covers three loop primitives (`/loop`, `/goal`, `/schedule` in Claude Code; `codex exec` wrappers and Automations in Codex), the five essential components of a production loop (trigger, scope, action, budget, stop condition), eleven proven patterns, and two critical failure modes -- uncontrolled token cost and a missing independent verifier. The core design rule: the worker agent must never grade its own output.

---

## Problem & Motivation

Manual AI prompting does not scale. A developer spending hours re-prompting an agent for repetitive tasks (PR reviews, bug triage, test fixes) is not leveraging agentic capability. The gap is a structured way to design *when*, *how*, and *how long* an agent runs -- with cost controls and quality gates -- so useful work happens without continuous human attention.

The shift is from "I prompt Claude" to "I design the system that prompts Claude."

---

## Main Original Ideas

1. **Three Distinct Loop Primitives**
   `/loop` repeats a prompt while the session is alive (dies on terminal close); `/goal` runs until a separately-verified condition is met, then self-terminates; `/schedule` deploys a durable cloud routine that survives machine shutdown and runs via cron, webhook, or API trigger. These are not aliases -- conflating them leads to runaway costs or prematurely stopped work.

2. **External Verification as a First-Class Requirement**
   The worker agent must not evaluate its own output. A separate, cheaper model (or a compiler, test suite, or linter) must judge completion. This single rule prevents compounding errors and agents reporting false success.

3. **The Five-Part Loop Anatomy**
   Every production loop needs: a **trigger** (cron, event, interval), a **scope** (what the agent may touch), an **action** (the task), a **budget** (token/iteration/cost ceiling), and an explicit **stop condition** (measurable success criteria). Missing any one component is a production incident waiting to happen.

4. **Four-Part Role Architecture**
   Each loop defines a JOB (what the agent owns), PERMISSIONS (what it may change), a SCHEDULE (when it activates), and STATE (shared context stored outside the conversation -- e.g. CLAUDE.md, GitHub Issues labels, state files).

5. **Manager/Worker Split for Safety**
   Two cooperating loops: a Manager loop classifies incoming work by risk (low/medium/high) and marks safe items `agent:ready`; a Worker loop picks only `agent:ready` items, implements changes, calls a separate review agent, and opens PRs but never merges. Human merge authority is retained throughout.

6. **Context Minimalism**
   Counter-intuitively, providing too much context can constrain the model. The current best practice is a minimal system prompt, minimal tool access, and retrieval paths for the model to fetch additional context itself rather than front-loading everything.

---

## Key Findings

| Pattern | Mechanism | Use Case |
|---|---|---|
| Build-test-fix pair | Builder writes, checker validates | Fast TDD feedback loop |
| Verifier loop | Independent model reviews before proceeding | Code quality gate |
| Five-minute maintainer | Agent picks one small improvement on timer | Background housekeeping |
| Quality streak loop | Requires N consecutive clean runs, not one | Release readiness |
| Production error sweep | Logs to triage to fix to PR + regression tests | Incident automation |
| Post-commit review hook | Git hook triggers review + agentic fix | Pre-merge safety |
| Overnight PR routine | Scheduled fixes while developer sleeps | Async velocity |
| Human-in-loop approval | Pauses for approve/revise/skip | High-stakes changes |
| Adversarial review | Two independent model families must agree | Critical merges |

**Quantitative reference:** Boris Cherny (Claude Code creator) reported 259 PRs merged autonomously in 30 days by December 2025, 100% via loops.

**Two failure modes to design against:**
- **Unbounded cost** -- community incidents range from thousands to full annual budgets consumed overnight; hardcode iteration caps and dollar budgets before leaving loops unattended.
- **Absent verifier** -- a loop without independent checking produces wrong answers *faster* than a human would; the verifier must be cheaper and more reliable than the action model.

---

## Suggestions & Future Directions

1. Start with one of three low-risk starter patterns: build-test-fix as `/loop`, five-minute maintainer as `/loop`, or overnight PR routine as `/schedule`. Each requires a budget and verifier before first deployment.
2. Capture every agent mistake as a durable instruction in `CLAUDE.md` or a reusable skill rather than re-fixing ad hoc ("correction to durable instruction to better future runs").
3. Adopt pre-execution goal specification: before starting any loop, rewrite the request with an exact measurable end state, verification method, constraints, and an optional turn/time limit.
4. Use worktrees (`--worktree` flag) for parallel agent work to avoid file collisions between concurrent sessions.
5. Add MCP connectors only for tools the loop genuinely needs; connect to external systems (Slack, CI/CD, issue trackers) selectively rather than broadly.
6. Monitor three metrics on every production loop: token cost per run, output quality (spot checks), and comprehension debt -- the risk of shipping work the team does not understand.

---

## Authors & Institutions

**Owain Lewis** -- AI engineer and principal engineer with 20 years in production systems; runs Gradient Work, an AI software consultancy. YouTube: [@owainlewis](https://www.youtube.com/@owainlewis). Referenced practitioners: Boris Cherny (Anthropic, Claude Code), Cat Wu (Anthropic, Claude Code product), Addy Osmani (Google).
