# WTF Is a Loop? Peter Steinberger vs. Boris Cherny

**Paper:** [WTF Is a Loop? Peter Steinberger vs. Boris Cherny (Matt Van Horn, 2026)](https://x.com/mvanhorn/status/2063865685558903149)

## Human Readable TL;DR

Imagine you stop cooking each dish to order and instead write a recipe-plus-checklist that a kitchen full of robot cooks follows on their own: they cook, taste, fix, and repeat while you sleep. That is what AI coders mean by a "loop" -- a little automatic manager you write once that keeps instructing the AI for you until the job is done, so you are no longer the one typing every instruction. A viral six-word tweet ("you should be designing loops that prompt your agents") kicked off a fight this week because almost nobody quoting it could explain it. The surprising twist: now that the AI writes code for almost nothing, running these tireless managers is the costly part, so the real skill is making sure they know when to stop.

## TL;DR

A "loop" in 2026 AI-coding parlance is a small supervisory program that repeatedly prompts a coding agent, reads its output, decides whether the task is done, and re-prompts until it is -- moving the human from prompt-writer to loop-author, with the model demoted to a subroutine. Matt Van Horn ran a `/last30days` research sweep to settle a viral Steinberger-vs-Cherny argument, tracing a real five-year lineage (ReAct 2022 -> AutoGPT 2023 -> ralph 2025 -> `/goal` spring 2026 -> multi-agent orchestration now) and arguing the genuinely new layer is durable, scheduled, multi-agent orchestration ("loops supervising loops"). The punchline: with inference now cheap, the loop itself -- its scheduling, supervision, and halting guarantees -- is the expensive part, and the durable asset is the reusable "skills" a loop calls, not the prompts.

---

## Problem & Motivation

The most-repeated sentence in AI coding this week -- Peter Steinberger's "you shouldn't be prompting coding agents anymore; you should be designing loops that prompt your agents" -- cleared 2.2M views, yet almost nobody boosting it could define a "loop." The replies turned into a brawl (the most-liked answer was literally "nobody knows but him and boris"). The article exists to cut through that definitional confusion: to give a plain, correct definition, separate the genuinely new idea from rebranded old ones, and answer the skeptics who call it "just a cron job."

---

## Main Original Ideas

This is an opinion/research essay, so the "original ideas" are the author's framings and arguments rather than experimental contributions.

1. **A loop is "cron plus a decision-maker in the body."** A cron job runs a fixed script; a loop runs a model that inspects current state, picks the next action, executes, checks whether it worked, and decides whether to continue. The decision is the agent's, not a hardcoded branch -- that middle is exactly what cron never had.

2. **The altitude shift.** You stop being the thing inside the loop typing prompts and become the author of the loop. The job did not vanish -- it moved up an abstraction level, "from writing the code to writing the thing that writes the code." Engineers who decide what to build matter more, not less.

3. **The five-stage lineage (the ladder).** The word "loop" hides at least five distinct things; placing yourself on the ladder is the fastest way to stop talking past people. Single-agent ralph is "old hat"; the new layer is multi-agent supervision built on top of it.

4. **What is actually new (Stage 5).** Four things changed at once: the loop (not the task) became the unit of work; loops began supervising other loops concurrently and on a schedule; scheduling replaced the human kickoff (runs on infrastructure time, not your attention); and durability became explicit (git-backed state, crash recovery). Ralph assumed your terminal stayed open; the 2026 version assumes it does not.

5. **The cost inverted -- the loop is now the expensive part.** Once the model writes code for almost nothing, cost moves to running the loop. "The costliest thing in AI coding is no longer writing code, it's managing the agent loop." Most of the job becomes making loops halt.

6. **"It's not loops. It's skills." (the author's own landing take).** The loop is plumbing; the asset is the reusable skill it calls. A loop with no reusable skills is "just a while-true around a stranger"; a loop that calls a library of sharp, tested, named skills is a system that compounds.

---

## Key Findings

The article is reportage rather than measurement, but it marshals a structured "ladder" and concrete receipts.

### The loop lineage (oldest -> newest)

| Stage | Name | When | What it is |
|-------|------|------|------------|
| 1 | **ReAct** (academic while-loop) | 2022 | Model reasons, calls a tool, reads result, repeats until done. One model, one loop, a human watching. |
| 2 | **AutoGPT** | 2023 | Gave the loop a goal and let it prompt itself; became famous for spinning forever doing nothing -- seeded "agents are a toy." |
| 3 | **ralph loop** (Geoffrey Huntley) | Jul 2025 | A bash one-liner piping the same prompt file into the agent repeatedly; key innovation is *discipline* -- every iteration resets context to a fixed set of anchor files instead of letting the conversation grow. |
| 4 | **`/goal` command** (Codex & Claude Code) | Spring 2026 | Productized ralph: runs the loop until a small validator model confirms the task is done. |
| 5 | **Orchestration loops** (Steinberger/Cherny) | Now (2026) | Durable, scheduled, multi-agent supervision -- "loops supervising loops." The genuinely new layer. |

### Concrete receipts

- **Boris Cherny:** created Claude Code as a side project (Sep 2024); it now reportedly sits behind ~**4% of all public GitHub commits**. In the last 30 days **100% of his contributions to Claude Code were written by Claude Code -- 259 PRs landed** (via Simon Willison, Dec 27 2025). He deleted his IDE in November and has not reopened it; a couple hundred agents read his GitHub, Slack, and Twitter to decide what to build next.
- **Huntley's ralph** built an entire programming language for about **$297**.
- **Uber** capped engineers at **$1,500 per person, per tool, per month** for Claude Code and Cursor after burning its annual AI budget in **four months**.
- **Gartner** places agentic AI at the **peak of inflated expectations**, with only **~17%** of organizations actually deploying agents -- the gap between timeline hype and the receipts.
- **Steve Yegge's "Gas Town"** (launched January): 20-30 Claude Code instances coordinated by a **Mayor agent**, with patrol agents running continuous loops and state stored in git so work survives a crash -- a shipped, open-source orchestration loop.
- **Verification is the fastest-growing sub-theme**, e.g. `roborev` (Dan Kornas) reviews every commit in the background and feeds findings back to the agent while context is still fresh. "An open loop that writes code with no feedback is a machine for generating confident mistakes."

### Five key patterns (the author's distilled list)

- A loop is cron plus a decision-maker in the body: the model, not a hardcoded branch, picks the next action each tick.
- The lineage is real (ReAct -> AutoGPT -> ralph -> `/goal` -> orchestration); single-agent ralph is old hat, multi-agent supervision is the new layer.
- A loop is only as good as its feedback; continuous review and validation gates are what make it trustworthy.
- The expensive resource shifted from tokens to loop management.
- The reusable unit inside the loop is a **skill**, not a prompt.

---

## Suggestions & Future Directions

How to actually build one, per the article (largely Boris Cherny's and Steinberger's advice):

1. **Stop being the thing in the loop.** Write the loop once; encode the *intent and the stopping behavior*, and let the loop prompt the agent each tick. The on-ramp is one slash command, e.g. `/loop babysit all my PRs. Auto-fix build issues, and when comments come in, use a worktree agent to fix them.`
2. **Cherny's five tips for running an agent autonomously for hours/days:** (a) use auto mode for permissions so it does not stop to ask; (b) use dynamic workflows to orchestrate hundreds/thousands of agents; (c) use `/goal` or `/loop` to nudge it to keep going until done; (d) run in the cloud so you can close your laptop; (e) make sure it can self-verify its work end to end.
3. **Verification is the non-negotiable** -- "a loop is only as trustworthy as its ability to check its own work."
4. **Always cap the loop -- the three hard stops every serious 2026 write-up converges on:** a maximum iteration count, no-progress detection, and a token/dollar budget ceiling (guarding against infinite loops and "billing surprises orders of magnitude over budget").
5. **Build skills, not one-off prompts.** If you do something more than once, turn it into an automated skill; if you do something hard, turn it into a skill afterward so next time is free. Loops that call sharp, named skills compound; loops that re-derive everything just burn money.

**Open tension / limitation acknowledged:** the skeptic line "cronjobs have funny re-branding rn" is "half right" -- the scheduling layer genuinely is cron (Claude Code's `/loop` uses cron under the hood; Boris runs his on cron). The honest framing is neither "new magic" nor "just cron," but "cron plus a decision-maker," where the interesting engineering is everything wrapped around that decision so it does not run off a cliff. The hype version (write loops, a thousand agents build your company overnight) versus the production version (most of your job is making sure they halt) is the real state of play.

---

## Authors & Institutions

**Matt Van Horn** ([@mvanhorn](https://x.com/mvanhorn)) -- author of this X long-form article (Jun 8, 2026, ~1.9M views). Co-founded a self-driving oven company (acquired by Weber) and the company that became Lyft; describes running nightly loops that open pull requests across ~30 open-source repos, written with `/last30days` research running in the background. The piece compiles `/last30days` runs (dated 2026-06-07) across Reddit, X, YouTube, TikTok, Instagram, Hacker News, and GitHub; the principal figures it quotes are **Peter Steinberger** (@steipete) and **Boris Cherny** (@bcherny, creator of Claude Code), with supporting voices including Matthew Berman, Geoffrey Huntley, Steve Yegge, and Dan Kornas.
