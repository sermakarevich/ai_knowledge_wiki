> [[index|Wiki]] | [[summary|Summary]]

# OpenOrchestrator (`owt`) — In Plain Language

## What is this about?

Imagine you hire five cooks and put each one in a separate kitchen with a copy of the same recipe book. That solves the "too many cooks" problem — until two cooks rewrite the same recipe page, or one cook burns something and nobody notices for an hour. OpenOrchestrator is the head chef's wallboard: every kitchen gets a row on the board, rows are sorted so fires are on top, and each row has big buttons like "taste" (look at the diff), "serve" (merge), or "walk into that kitchen" (attach to the session). The head chef never cooks — they supervise.

In technical terms it is a terminal dashboard plus a command (`owt`) that runs many AI coding assistants in parallel, each isolated in its own git worktree (a separate folder + branch) and terminal session, all tracked in one small database file.

## Why does it matter?

When one AI agent writes code, you watch it. When five do, you drown: which one is stuck? Which two are editing the same file and will collide at merge? Which finished and just needs your approval? Without a cockpit, the operator becomes the bottleneck — exactly the problem fleet-style orchestration exists to solve. OpenOrchestrator's answer is an *attention machine*: sort everything by "needs a human first", hide everything that doesn't, and make every action one keypress. Its second answer is cheap safety: warn about file overlaps *before* merging, and merge in an order (smallest, least-entangled first) that minimizes collisions.

## How does it work?

Step-by-step, in kitchen terms:

1. **Open a kitchen.** You type a task ("add login with JWT"). The system photocopies the recipe book (git worktree + new branch), stocks the pantry (installs dependencies, copies secrets), slips instructions into the cookbook (CLAUDE.md), and seats a cook (starts Claude/Pi/Droid in a terminal session). A row appears on the wallboard marked "cooking".
2. **The cooks phone in.** Each kitchen has a bell system (hooks): "started working", "waiting for you", "blocked". The board updates every couple of seconds.
3. **The board sorts itself.** Kitchens on fire (merge conflicts, errors) jump to the top lane (NEEDS YOU). Finished dishes move to the middle lane (READY TO SHIP, with a note like "3 commits ahead, overlaps 1 file with kitchen B"). Everything still cooking sits at the bottom (IN FLIGHT).
4. **You press buttons.** Walk in (`a`), taste first (`d`), serve (`s`), fix it yourself (`f` — the board steps aside and hands you the kitchen), or combine (`m`).
5. **Serving is careful.** Before mixing a dish into the main menu, the system checks whether two kitchens touched the same pages (Conflict Guard), updates the side dish from the main menu first and only then mixes it in (two-phase merge), and serves small dishes before big ones (queue order). Alternatively it can box the dish for a food critic instead (open a GitHub PR, kitchen left intact).

## Where can this be used?

- Any team running parallel coding agents that needs a human triage surface rather than full autonomy.
- CI/CD: headless mode plus `wait` gives scripted launch-and-block semantics.
- Fleet and similar orchestrators can steal the UX pattern (lanes + verb rows + teaching footer) and the safety plumbing (overlap warnings from already-stored file lists, two-phase merge, smallest-first ship order) without adopting the tool.
- Outside coding: any "many isolated workers, one human approver" setup (parallel data pipelines, review queues) fits the lane model.

## Conclusions & takeaways

What to remember: supervise, don't replace — the cockpit owns prioritization, the agents own execution. Isolation per task (worktree + session + status row) is what makes parallelism sane; the board is what makes it operable; overlap warnings plus ordered two-phase merging are what make shipping safe. Honest limits: warnings are advisory and only as fresh as agents' self-reports; there is no automatic correctness gate (no tests-must-pass before ship); and the board polls rather than reacting to events, so it fits tens of tasks, not hundreds.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| git worktree | A second folder with its own branch of the same code, so two agents never share files |
| tmux / herdr | Terminal session managers — invisible rooms where agents keep running after you look away |
| Conflict Guard | The check that warns when two branches edited the same files |
| two-phase merge | First update the side branch from main, then merge the side branch into main — never the reverse order |
| merge queue | The suggested order for merging finished branches (smallest and least-tangled first) |
| plan-first workflow | Asking the agent to write a plan before coding, by prepending planning instructions |
| harness / AI tool | The actual coding assistant (Claude Code, Pi, Droid, …) — the engine, not the cockpit |
| MCP peer messaging | An optional side-channel letting agents send each other messages |
| headless mode | Running without the dashboard, for scripts and CI |
| autostash | Temporarily shelving uncommitted changes so a merge can proceed, then restoring them |
