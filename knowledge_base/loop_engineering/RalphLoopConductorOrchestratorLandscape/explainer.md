> [[index|Wiki]] | [[summary|Summary]]

# Ralph loop + Conductor + orchestrator landscape — In Plain Language

## What is this about?

Imagine you hire one assistant to write a long report. Halfway through, the assistant forgets your first instructions, starts repeating itself, and confidently declares a half-finished draft "done". That is what happens when a single AI coding agent works too long in one go.

This entry is about three recipes for avoiding that. The **Ralph loop** (named after Ralph Wiggum, the simple cartoon kid) is the simplest: give the worker the same written instruction card over and over, and wipe its memory clean between attempts. The card and the filing cabinet (your files and version history) are the only memory allowed. **Conductor** is the kitchen-counter version: every cook gets a separate workstation (an isolated copy of the code), and you inspect each dish through the glass before it goes out. The **micro-patterns** are four tiny gadgets: a universal loop that works with any AI tool, a fan-out trick for parallel copies, a claim-ticket system so two cooks never grab the same order, and a lock system so two cooks never chop the same carrot.

## Why does it matter?

One AI runs into three walls: it forgets (its short-term memory fills up), it is a generalist (worse at specialist jobs), and it has no teamwork skills (helpers overwrite each other's work). Without a system around them, parallel agents burn money, clobber each other's edits, and serve unreviewed code. The question this landscape answers is practical: how do you run *several* agents at once without chaos — and which tricks are worth importing into our own headless task-runner (called "fleet")?

## How does it work?

Step-by-step, using a restaurant-kitchen analogy:

1. **Write the recipe card (Ralph's prompt file).** One card states the goal and what "done" means — e.g. "all tests pass". One dish per round, then the cook leaves the kitchen.
2. **Wipe the cook's memory every round.** Each attempt starts fresh. Progress survives only because finished dishes (commits) and the order list (a task file) sit in the pantry, not in anyone's head.
3. **Taste before serving (the completion check).** A fixed test — automated tests, a COMPLETE stamp, every order marked passed — decides when to stop looping. The cook never grades its own homework.
4. **Separate workstations (worktrees).** Each cook works at its own counter with its own copy of the ingredients, so nobody bumps elbows mid-shift. Collisions surface only when dishes are combined at the pass.
5. **Claim tickets and tiny locks (swarm-protocol, wit).** A ticket board says who owns which order plus a pulse ("still cooking!"); the finest tool locks individual ingredients down to a single recipe step, warning before two cooks touch the same one.
6. **You are the head chef (Conductor).** In the simplest setup a human watches the counters, tastes every dish (diff review), and can roll a bad dish back. Fancier setups add a written rota (workflows) and a dedicated taster (a reviewer stage) before anything reaches customers.

## Where can this be used?

- **Overnight grind work:** migrations, test-coverage backfill, big refactors — anything with a mechanical pass/fail check — can loop unattended while you sleep.
- **Parallel feature work:** give each agent its own isolated copy of the codebase and review the differences, instead of watching every keystroke.
- **Mixed-model teams:** plan with an expensive smart model, grind with cheap local ones, verify independently — spend the budget on the *check*, not the loop.
- **Outside coding:** any pipeline where workers are forgetful but checks are cheap — data cleanup, document drafting with a checklist, batch content review — fits the same loop-plus-gate shape.

## Conclusions & takeaways

What to remember a month from now: wipe worker memory and keep truth in files; never let the writer declare its own work good; isolate workers but expect merge collisions anyway; cap every loop with a budget; keep shared notes human-approved. Honest limits: the loop only fits well-specified, mechanically checkable work; self-reported overnight success stories are marketing, not benchmarks; and nobody has solved the hard part — slicing work into non-overlapping pieces is still the human's job.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Ralph loop | Re-running the same AI worker from scratch until an automatic check passes |
| Worktree | An isolated copy of the code (own folder + branch) so parallel workers do not collide mid-task |
| Completion check | The automatic taste-test (tests, checks, stamps) that decides when looping stops |
| Prompt file | The written recipe card holding the goal and the definition of done |
| Context window | The AI's short-term memory; wiped clean every Ralph pass |
| PRD | Product requirements document — the order list with a pass/fail flag per item |
| MCP | Model Context Protocol — a standard way for agents to call tools |
| Tree-sitter | A code-parsing library used here to identify single functions for locking |
| Heartbeat | A short "still alive" pulse from a worker so the boss can tell slow from stuck |
| Janitor stage | A dedicated reviewer step between finishing work and merging it |
| HITL | Human in the loop — a person reviews before proceeding |
| AGENTS.md | A shared notes file of project conventions that agents read |
