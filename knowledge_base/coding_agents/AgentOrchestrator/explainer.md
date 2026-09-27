> [[index|Wiki]] | [[summary|Summary]]

# Agent Orchestrator (AO) — In Plain Language

## What is this about?

Imagine hiring ten builders to renovate ten rooms of your house at the same time. Normally that is chaos: they bump into each other, paint over each other's work, and you spend all day answering questions. Agent Orchestrator (AO) is the foreman with a clipboard. Each builder gets their own locked room (a separate copy of the code), their own to-do card on one big board, and a rule that nothing counts as finished until the inspector (automatic tests and code review) signs off. You only step in when the foreman raises a flag.

In technical terms: AO is a desktop app for running fleets of AI coding assistants in parallel. One background program (the daemon) keeps all records; the window you see, the terminal commands, and an optional phone view are just thin displays of those records.

## Why does it matter?

Running several AI assistants in one copy of the code creates the exact mess the builders make: mixed-up files, nobody knowing who broke the tests, review comments landing in the wrong conversation, and merge conflicts discovered late. AO's answer is isolation plus ownership: separate rooms, one proposal-to-merge per builder, and automatic routing so the right builder fixes their own failed tests. Testimonials cite going from 2–3 finished code proposals a day to 5+.

## How does it work?

Step by step, in everyday terms:

1. **Hand out locked rooms.** Starting a task creates a fresh copy of the code (a git worktree) on its own branch. No two agents share a room.
2. **Pin one proposal per builder.** Each task claims exactly one pull request (a formal "please merge my work" proposal). Everything that happens to that proposal belongs to that builder.
3. **Watch the inspectors centrally.** A watcher checks the test results and review comments on every proposal and writes down only facts (which test failed, who asked for changes).
4. **Send the note to the right room.** Failed tests or change requests go back to the owning builder automatically — but only once per new problem, not spammed every five minutes.
5. **Keep the merge decision human.** When tests pass and reviewers approve, you get a "ready to merge" flag. You press the button; nothing merges itself.
6. **Protect messy rooms.** Shutting a task down never throws away unsaved work; a preview command shows what cleanup would remove before it removes anything.

## Where can this be used?

- Any team running multiple AI coding assistants at once (inside one company or open-source).
- Human teams that want the same discipline: one branch per task, one owner per pull request, automatic routing of test failures.
- Fleet-style supervisors (like ours): the seven borrowable ideas — derived status, dirty-work protection, deduplicated nudges, mode-aware delivery, per-role defaults, claim-PR fallback, append-only change log — transfer directly.
- Outside coding: any parallel-worker setup where workers must not share state but one coordinator must route feedback (e.g. parallel document review, data-labeling fleets).

## Conclusions & takeaways

What to remember a month from now: isolate first (separate copies beat after-the-fact conflict resolution); store facts and compute status when asked (stored status always goes stale); route feedback to owners automatically but keep irreversible actions human-gated; and prefer built-in lifecycle behavior over user-scripted workflow languages. Honest limits: restart works at the whole-task level (no resuming a half-finished thought), only GitHub is fully watched, and nothing merges on its own — by design.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Worktree | A separate checked-out copy of the code, each on its own branch — a "locked room" |
| Pull request (PR) | A formal proposal to merge one branch's work into the main code |
| Daemon | A background program that keeps running and owns all records and logic |
| SQLite | A small database stored in a single file on your computer |
| CI (Continuous Integration) | Automatic tests that run on every proposed change |
| SCM observer | The watcher component that polls GitHub and records PR/test/review facts |
| Derived status | Computing labels like "ready to merge" when asked, instead of storing them |
| CDC / change log | A list of "what changed" that clients replay to stay up to date |
| SSE (Server-Sent Events) | One-way live updates pushed from the server to the display |
| Harness / adapter | The connector that lets AO drive one specific AI assistant |
| TUI (Terminal UI) | The assistant's own text screen inside a terminal window |
| ACP (Agent Client Protocol) | A standard way for apps to hold structured conversations with coding assistants |
