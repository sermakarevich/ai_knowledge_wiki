> [[index|Wiki]] | [[summary|Summary]]

# Overstory — In Plain Language

## What is this about?

Imagine you want to renovate a house, but instead of hiring one busy handyman, you hire a whole crew: one manager who plans the work, a few team leaders who break it into jobs, and specialists who each do one small task.

Overstory is software that organizes teams of AI helpers (programs that can read and write code) in exactly that way. Instead of one AI trying to do everything and getting confused, many small AI workers each get one clear job.

Each worker gets its own clean copy of the project to work in, its own written instructions, and a simple mailbox to talk to the others. A set of safety rules stops them from breaking things outside their assigned area.

You can think of it as a construction site with fences between work zones. Everyone sees the overall plan, but each person only builds inside their marked zone. That way, ten people can work at the same time without stepping on each other's work.

## Why does it matter?

When one AI does a big coding task alone, three common problems appear: it forgets earlier details, two changes clash with each other, and a stuck worker can silently stop without anyone noticing.

Overstory tries to fix this with teamwork plus supervision. Work is split so no single worker has to remember everything. Changes are combined carefully, step by step. And a separate watcher checks whether anyone is stuck, first warning them, then helping, and only as a last step replacing them.

If this works, large coding tasks become more reliable, easier to restart after a crash, and less dependent on which specific AI product you use.

A simple example: two AI helpers change the same file at the same time. Without organization, one change quietly erases the other. With Overstory, each change lives in its own copy first, then they are compared and joined carefully, and past mistakes teach the system which joining method to trust.

## How does it work?

Think of a restaurant kitchen during a busy evening. Orders come in, stations divide the work, and plates are assembled at the end. Here is the same flow in Overstory:

1. **The head chef takes the order.** A top manager, called the coordinator, receives the goal from a human, breaks it into large pieces, and hands each piece to a team leader. The coordinator does not cook directly.

2. **Team leaders plan their station.** Each lead (a middle manager) breaks its large piece into small tasks, writes a short recipe card for each one, and calls in specialists.

3. **Specialists work at separate counters.** Explorers (called scouts) only look around and take notes. Cooks (called builders) each work at their own counter with their own copy of the ingredients, so they cannot mess up someone else's dish. Checkers (called reviewers) taste but never change the food.

4. **Everyone leaves notes, not shouts.** Workers do not chat in long confusing messages. They save their work in files and send short typed letters through a shared mailbox stored in a local database. A letter might say "my part is done" or "ready to combine".

5. **A floor manager watches for trouble.** A background checker, called the watchdog, regularly asks: "Is anyone stuck?" First it warns, then it nudges, then it asks another AI for a second opinion, and only then it stops and replaces the stuck worker. Saved progress notes (called checkpoints) let the replacement continue where the last one stopped.

6. **Dishes are combined in order.** Finished work waits in a line (called a merge queue). The combining follows four levels: clean join, simple automatic fix, asking AI for help, and as a last resort rebuilding one change on top of the other. The system remembers which fixes worked before, so it learns over time.

7. **The same kitchen works with different ovens.** Overstory can use many AI products (such as Claude, Codex, Gemini, Copilot, and others). A common adapter layer translates the same instructions into whatever each product needs, so the rest of the system does not have to change.

The key idea is simple: nothing important lives only in a worker's short-term memory. Instructions, progress notes, messages, and work history are all saved as files. So any worker can be stopped and replaced without losing the whole meal.

## Where can this be used?

- **Building large software features:** many small coding tasks can run at the same time without overwriting each other.
- **Fixing many bugs at once:** each bug gets its own worker, reviewer, and safe copy of the code.
- **Exploring unknown code:** read-only explorers can map a large project and write short reports before anyone changes anything.
- **Outside software:** the same pattern fits any work that splits well — for example, a group of AI helpers researching different parts of a report, checking each other's drafts, and combining them in order, with a watcher restarting stuck helpers.
- **Switching AI providers:** a team can move from one AI product to another without rebuilding the whole workflow, because the adapter layer hides the differences.
- **Reviewing homework or documents:** one helper drafts, another checks for errors, a third combines feedback, all without editing over each other.
- **Running repeated jobs overnight:** the watcher keeps patrol while humans sleep, and saved notes make morning restarts painless.

## Conclusions & takeaways

What to remember a month from now: Overstory is a teamwork system for AI coders — strict roles, separate workspaces, short written messages, careful combining, and patient supervision.

Its strengths are isolation (workers cannot easily damage each other's work), restartability (progress is saved in files, not just in memory), and flexibility (it works with several AI products).

Honest limitations: it adds complexity — manager, mailbox, watcher, and combining line all need setup and care. Very small tasks may be slower with a full crew than with one helper. Some AI adapters are still experimental, and conflict repair is not magic: when two changes truly contradict, human judgment is still needed.

In short: use this approach when the work is big, parallel, and worth organizing. Skip it when one person could simply do the job alone faster.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Agent | An AI helper given one role and one task |
| Coordinator / lead / worker | Manager, team leader, and specialist in a three-level hierarchy |
| Worktree | A separate working copy of the project, like a personal counter in a kitchen |
| Overlay | The personal instruction sheet a worker reads when it starts |
| Guard / hook | An automatic safety rule that blocks risky actions before they happen |
| Mailbox (SQLite mail) | Short typed messages stored in a local file database (SQLite, a small database kept in a single file) |
| Watchdog | A background checker that notices stuck workers and wakes, helps, or replaces them |
| Checkpoint / handoff | A saved progress note that lets a new worker continue after a crash or restart |
| Merge queue | An orderly waiting line for combining finished work, first finished is combined first |
| Harness (runtime adapter) | The specific AI product doing the work, plus the translator that connects it to Overstory |
| Quality gates | The required checks before work counts as done, such as tests and style checks |
| FIFO (first-in first-out) | A fairness rule: whoever finishes first gets combined first |
