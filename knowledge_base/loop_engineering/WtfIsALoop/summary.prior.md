# WTF Is a Loop? Peter Steinberger vs. Boris Cherny

**Source:** [WTF Is a Loop? (@mvanhorn, Jun 8 2026)](https://x.com/mvanhorn/status/2063865685558903149)
**Referenced article:** [Loop Engineering -- Addy Osmani](https://addyosmani.com/blog/loop-engineering/)

## Human Readable TL;DR

Imagine hiring a contractor who needs you to hand them each nail one at a time and say "now hammer." Loop Engineering is the shift to building a machine that loads the nails, swings the hammer, inspects the result, and calls you only when something goes wrong. Two prominent AI engineers -- one at OpenAI, one at Anthropic -- both stopped typing prompts to AI assistants and started writing small programs whose job is to do the prompting for them. This article examines what they actually mean, why the idea spread so fast, and what it takes to build one safely.

## TL;DR

"Loop Engineering" is a paradigm shift where developers stop manually prompting coding agents and instead design automated systems -- loops -- that discover work, issue prompts, execute, verify results, and iterate. The viral catalyst was Peter Steinberger (OpenAI) saying "you should be designing loops that prompt your agents" and Boris Cherny (head of Claude Code, Anthropic) saying "I don't prompt Claude anymore. I have loops running that prompt Claude." A loop is defined by five components: automations (scheduled discovery), worktrees (parallel isolation), skills (reusable project context), plugins/connectors (MCP integrations), and sub-agents (specialized verifiers separate from implementers). The primary risk is unattended loops producing unattended mistakes.

---

## Problem & Motivation

Manual prompting creates a human bottleneck in agentic workflows: every task requires an engineer to formulate context, issue commands, evaluate outputs, and decide the next step. As AI coding agents become capable of multi-step tasks, this interruption loop degrades throughput and shifts engineering effort toward prompt crafting rather than system design. The article addresses the gap between one-shot agent invocations and fully autonomous continuous workflows that can run unsupervised, handle multiple concurrent tasks, and escalate to humans only at decision boundaries.

---

## Main Original Ideas

1. **Loop as the Unit of Automation** -- A loop is not a prompt, a script, or an agent -- it is an orchestration layer with a trigger, scope, action budget, stop condition, and reporting path. The hierarchy escalates from "fix this bug" (single task) → "fix the billing webhook validation, only touch app/api/billing" (scoped task) → "every 15 minutes inspect open PRs labeled codex-watch, fix CI failures, stop if the same failure repeats twice" (loop workflow).

2. **Replacing Yourself as the Prompter** -- The core mental model: "Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead." This shifts leverage from prompt quality to system design -- the engineer architects the discovery, execution, verification, and escalation logic rather than typing commands.

3. **Five Essential Loop Components**
   - **Automations:** Scheduled tasks that discover and triage work (Codex Automations tab, Claude Code `/loop` and `/goal` commands)
   - **Worktrees:** Isolated working directories so parallel agents don't cause file collisions
   - **Skills:** Reusable `SKILL.md` files capturing project conventions, build procedures, and context -- eliminating repetitive setup across sessions
   - **Plugins/Connectors:** MCP-based integrations (issue trackers, databases, Slack) enabling loops to act within real environments
   - **Sub-agents:** Specialized agents by role (explorer, implementer, verifier) -- critically, the agent that wrote the code should not grade its own work

4. **Four Production Loop Patterns**
   - **PR Babysitter:** Every 15 min on labeled PRs -- rebase, fix deterministic CI failures, summarize blockers; stops on repeated failure
   - **CI Health Loop:** Every 30 min on main -- cluster failures, distinguish flakes from deterministic issues, open fix branches
   - **Deploy Verification:** Post-push -- verify health endpoints, confirm page elements, report live links
   - **Feedback Clustering:** Every 30-60 min -- aggregate GitHub issues, social posts, support channels; map patterns to content gaps

5. **Loop Safety Requirements** -- Production loops require hard budgets (max attempts, runtime, file changes, tool calls), state refresh on each cycle (never trust cached context), single ownership per responsibility area, and explicit escalation rules -- stop conditions that hand control back to a human rather than retrying indefinitely.

---

## Key Findings

- The shift is already underway: Boris Cherny frames it as "the transition we're going to see for the rest of the year" in AI-assisted engineering
- Loop failures differ qualitatively from one-shot failures -- they keep spending, accumulate stale assumptions, and can create race conditions; failure modes are sustained rather than isolated
- 74.4% positive sentiment among practitioners who engaged with Cherny's statements; skepticism clusters around code quality and skill degradation in production settings
- The paradigm shift moves leverage from the quality of individual prompts to the quality of system design -- harder intellectually, easier operationally

---

## Warnings & Risks

1. **Verification remains human responsibility** -- Unattended loops produce unattended mistakes; verification cannot be fully automated without introducing new failure modes
2. **Comprehension debt** -- Faster code delivery outpaces engineers' ability to understand what was built; knowledge gaps accumulate at the speed of the loop
3. **Cognitive surrender** -- Comfortable automation can atrophy critical thinking; the ease of delegation is the most insidious risk
4. **Race conditions without ownership** -- Multiple loops touching overlapping areas create conflicts that are harder to debug than any individual agent error

---

## Suggestions & Future Directions

1. Start with scoped, single-responsibility loops before composing multi-step workflows
2. Always instrument loops with explicit logging, budgets, and escalation paths before running unsupervised
3. Treat the "sub-agent that verifies" as a first-class architectural requirement, not an afterthought
4. The strategic bet: platforms that answer "can you maintain workflows over time with verification and escalation?" will win over platforms that answer only "can you write code?"

---

## Authors & Institutions

**Matt Van Horn** (@mvanhorn) -- Co-founder of June (acquired by Weber) and early Lyft; writing on X/Twitter.
Referenced voices: **Peter Steinberger** (OpenAI), **Boris Cherny** (Head of Claude Code, Anthropic), **Addy Osmani** (Google Chrome, Loop Engineering article).
