# Loop Engineering: The Anthropic Playbook for Designing Systems That Prompt Your Agents

**Paper:** [Loop Engineering: The Anthropic Playbook for Designing Systems That Prompt Your Agents (HuaShu, 2026)](https://drive.google.com/file/d/1qzKI4DKnyHRpXK1J3ATPqwaqLc0iNu-M/view)

## Human Readable TL;DR

Imagine you've been answering a company's support phones all day, every day. Loop engineering is like building an automated dispatch system that handles the calls for you -- except you don't just record a greeting: you design the whole system, including how it routes work, when it escalates to a human, and how it remembers what happened yesterday. Once that system runs, your job shifts from answering phones to deciding which calls matter most. The insight is that "doing the work" becomes nearly free, while judgment -- knowing which outcome is actually right -- stays stubbornly scarce, and whoever stays sharp on that is the one who's still in control six months later.

## TL;DR

Loop engineering is the fourth layer of the agentic software stack (above prompt, context, and harness engineering) that removes the practitioner from the inner prompt-response cycle by designing the system that prompts agents automatically. A single loop turn decomposes into five moves -- discovery, handoff, verification, persistence, scheduling -- realized by six parts: automations, worktrees, skills, connectors, sub-agents, and memory. The critical structural insight is that generator and evaluator must be separate agents, because an agent grading its own work praises it; tuning an independent skeptical evaluator is far more tractable. Loops accumulate four silent costs (verification debt, comprehension rot, cognitive surrender, token blowout) that reinforce each other and come due all at once. The same loop, built by two people, yields opposite outcomes depending on whether the builder stays the engineer or surrenders judgment to the machine.

---

## Problem & Motivation

The "XX Engineering" terms -- prompt, context, harness -- all assumed a human seated at the keyboard directing agents line by line. Each term taught the practitioner to do the work better but left them inside the loop. Loop engineering deletes that assumption: the practitioner is no longer the human clock inside the loop but the designer of a system that ticks on its own.

The term converged independently in June 2026 among Peter Steinberger (OpenClaw, ~8M-view post), Boris Cherny (Claude Code lead at Anthropic), and Addy Osmani (Google Chrome) -- practice had outrun naming. Coding agents had become reliable enough to finish non-trivial tasks unattended, scheduling primitives appeared in major harnesses, and single-run costs dropped far enough that repeated, timed runs stopped looking wasteful. When all parts are present, the combination becomes obvious to everyone at once.

---

## Main Original Ideas

1. **The Four-Layer Stack.** Prompt minds one sentence; context minds one window; harness minds one run; loop automates the "waiting for you" that harness leaves behind. Each layer up, the blast radius of an error grows -- a loop-layer mistake gets written into the state file, read back the next morning as established fact, and built upon across many turns before anyone notices.

2. **Five Moves of One Turn.** A loop turn is not idle spinning; it does five concrete things: *Discovery* (finds work autonomously, guided by a skill not a pasted instruction wall), *Handoff* (isolates each task in its own git worktree), *Verification* (swaps in a separate skeptical agent to say "no"), *Persistence* (writes state to disk so tomorrow picks up where today left off), *Scheduling* (triggers automatically so no human button-press is needed). Drop any one and the loop turns in place or not at all.

3. **Six Parts Map to Five Moves.** Automations enable Scheduling; Worktrees enable Handoff; Skills enable Discovery (paying off "intent debt" -- the recurring cost of re-explaining a project); Connectors (MCP) enable Persistence and Discovery into external systems; Sub-agents enable Verification (generator vs. evaluator); Memory (disk state) enables Persistence.

4. **Generator/Evaluator Separation.** An agent grading its own output praises it -- not a smarts problem but a "grading one's own homework" problem. The context in which code was written is stuffed with self-persuasion, so the agent sees the chain of reasoning, not the result. The remedy is structural: a separate evaluator agent with entirely different instructions, defaulting to *doubt* not trust, ideally using a different model. Crucially, the evaluator must *act* (run tests, click, screenshot via Playwright MCP) rather than just read -- "does it run right" vs. "does it look right." A fresh small model checks the stop condition (`/goal`) after each turn so completion is decided by something other than the agent that did the work (the maker-checker principle, borrowed from banking).

5. **Five Failure Modes.** Each failure is exactly one move skipped: *Nodding loop* (verification skipped -- agent approves own work at machine speed), *Amnesiac loop* (persistence skipped -- no cumulative progress, rediscovers same work each day), *Manual loop* (scheduling skipped -- works the day it's built, stops the day attention wanders), *Blind loop* (discovery skipped -- human still hands the loop its work each morning), *Tangled loop* (handoff skipped -- parallel agents collide on the same working directory). The disciplined loop installs all five; the hasty loop installs only discovery and handoff -- the two that produce visible output -- and skips the three that produce safety.

6. **Four Silent Costs.** *Verification debt*: every unreviewed PR saves time now and accumulates risk in the gap between "runs" and "right." *Comprehension rot*: the codebase grows while the engineer's mental map stalls; no alarm sounds until a bug burrows into a corner never read. *Cognitive surrender*: the more reliable the loop, the easier it is to outsource judgment entirely. *Token blowout*: a single idle bug can spin all night and produce an unfamiliar invoice rather than fixed code. The four reinforce each other in a cycle -- unverified output erodes understanding, which invites surrender, which lets the loop run longer and spend more -- and come due all at once.

---

## Key Findings

### Loops in Practice

| Loop | Scale | Key Reliability Mechanism |
|------|-------|--------------------------|
| Osmani's morning triage | 1 engineer | Skill-invoked automation; second reviewer sub-agent; state file; human inbox for uncertain items |
| Stripe's Minions | 1,300 PRs/week merged | Deterministic orchestrator assembles context (not the LLM); hard-coded linter gate agent cannot skip; Devbox EC2 "cattle not pets" per-agent sandboxes; humans still review all PRs |
| Claude Code `/loop` + `/goal` | per-session | Fresh small model checks stop condition after each turn; separate evaluator agent with adversarial instructions |

- Stripe's Minions is **not** built on a stronger model -- it is a fork of Goose (open-source). Reliability comes from the quality of the constraints, not model size.
- Those 1,300 PRs are still reviewed by humans. The human did not leave; they changed desks from writing to reviewing.
- Local `/loop` requires the machine on; Cloud Routines run with the machine off but have a 1-hour minimum interval and fresh clone each run. A mature loop often uses both.

### Scheduling Options

| Option | Machine on? | Min interval | Sees local files? |
|--------|-------------|-------------|-------------------|
| Cloud Routines | No | 1 h | No |
| Desktop scheduled | Yes | 1 min | Yes |
| `/loop` | Yes | 1 min | Yes |

### Economics of Judgment

- When generation becomes abundant (code, plans, fixes, PRs approach free), the entire value of the engineer concentrates into judgment -- knowing which output is actually right.
- The amplifier cuts both ways: a bad decision is now executed faithfully in bulk, a hundred times, with no slow gear left to catch it mid-flight.
- Two loops can be 90% identical in code; the difference is one or two checkpoints that determine whether the builder stands on top of the loop or is hollowed out by it.

---

## Suggestions & Future Directions

1. **Start minimal.** A first loop should handle one finding end-to-end before widening. Add parallelism last, after checks are proven to catch real mistakes. The Stripe case is the endpoint, not the entry.
2. **Invest in the evaluator, not the generator.** A strong generator with a weak judge produces confident garbage; a modest generator with a sharp judge produces slow, reliable progress, and the second compounds.
3. **Never remove the human review point.** It is not a scaffold to take down once the loop is trusted -- it is the permanent feature that keeps the loop trustworthy. The day it is removed is when comprehension rot begins.
4. **Set budget caps before first unattended run.** Per-run budget, daily budget, max retries -- these are circuit breakers that convert open-ended risk into a bounded one.
5. **Read a sample, always.** Not everything the loop produces, but a representative sample daily, genuinely examined. Inability to explain a change is a precise signal the mental map has fallen behind.
6. **Use the Toolchain-agnostic framing.** Claude Code's `/loop`, `/goal`, `--worktree`, skills, MCP are one implementation; Codex's automations, background worktrees, `$skill-name` are another. The question is whether all six parts are present, not which brand provides them.

---

## Authors & Institutions

**HuaShu** (independent reformatting into IEEE conference style). Original framework and quoted formulations: **Addy Osmani** (Google Chrome). Generator/evaluator findings: **Prithvi Rajasekaran** (Anthropic). Enterprise case: **Steve Kaliski** (Stripe). Convergent statements: **Peter Steinberger** (OpenClaw), **Boris Cherny** (Anthropic, Claude Code lead).

Source: Independent reformatting of HuaShu's open "Orange Book" guide *Loop Engineering: Stop Asking Me What It Is* (v260615, June 2026); available at huasheng.ai/orange-books.
