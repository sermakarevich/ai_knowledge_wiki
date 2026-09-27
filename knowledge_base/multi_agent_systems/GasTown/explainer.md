> [[index|Wiki]] | [[summary|Summary]]

# GasTown — In Plain Language

## What is this about?

Imagine a small town built for robot workers. GasTown is a program that runs many
AI coding assistants at once on your computer, the way a construction office
manages many crews on different job sites.

The "town" is just a folder on your disk (usually called `gt`). Inside it, each
"rig" is one software project — one copy of one codebase plus its workers. Think
of a rig the way you would think of one building site: it has its own plot of
land, its own crew list, and its own task board.

The workers come in two kinds. Polecats are short-term helpers: they are created
for one task, do the work, then their session is shut down. Crew members are
long-term staff: they stay around, like your personal assistants, and work
directly on the main code.

A Mayor is the head coordinator — one always-on assistant with a view of the
whole town. A Witness supervises the short-term workers, and a Refinery acts as
the quality inspector that merges finished work into the main code.

## Why does it matter?

One AI assistant working alone is easy to manage. Ten or fifty of them are not.
They can overwrite each other's files, lose track of who is doing what, crash
without anyone noticing, or merge broken code.

GasTown solves the boring-but-hard parts of teamwork: giving every worker its own
separate workspace, keeping a shared task list, restarting crashed workers,
delivering messages between them, and making sure only checked work reaches the
main codebase. Without this kind of system, running many AI coders at once turns
into chaos. With it, you can treat a crowd of AI helpers like an organized team.

## How does it work?

It works in five everyday steps, like an office workflow:

1. Hand out a task. A task (called a bead) is pinned to a worker. The system
   creates a fresh polecat: its own folder copy of the code, its own branch
   (a named side-copy of the code where it can experiment safely), and its own
   terminal window where the AI program runs.
2. The worker works alone. Because each polecat gets its own isolated folder
   copy, two workers can edit the same project without stepping on each other —
   like giving every cook their own kitchen instead of sharing one stove.
3. Save progress safely. As the worker goes, it writes small snapshots: a
   checkpoint file (a note saying "here is where I got to") plus draft saves of
   its code changes. If the computer crashes, the next worker can read that note
   and pick up roughly where the last one stopped.
4. Check and merge. When the worker finishes, it pushes its branch up and files
   a merge request (a formal ask: "please take my changes"). The refinery
   rehearses the merge first. If the changes clash with someone else's work, the
   merge is refused and the worker is asked to fix it — nothing is ever mashed
   together automatically.
5. Supervise everything. A background supervisor (called the daemon, meaning a
   helper program that never sleeps) checks every few minutes whether workers
   are alive, restarts dead ones with waiting pauses that grow longer after
   repeated failures, and reads a shared task queue so the next ready task is
   always handed out.

Under the surface, two tricks keep this reliable. First, coordination happens
through files and a small database, not through memory: locks (tiny "do not
enter" flags on files) stop two managers from creating the same worker at once.
Second, the task list lives in a real database that keeps its own history, so no
task assignment is ever lost even if machines restart.

GasTown can also drive many different AI coding tools — Claude, Gemini, Codex,
Copilot, and others — from one list. Instead of writing custom code for each
tool, it keeps a simple menu: each tool's name, how to start it, and how to wake
it back up. Adding a new tool mostly means adding one new row to that menu.

## Where can this be used?

- Running many AI coding tasks in parallel on one machine, such as fixing ten
  bugs across several projects overnight.
- Keeping experimental AI work safely separated from the main code, so bad drafts
  never break what already works.
- Organizing long jobs as task chains: a convoy (a group of linked tasks) feeds
  workers one ready item at a time until the whole chain is done.
- Recovering gracefully from crashes: checkpoint notes plus saved code drafts
  let replacement workers continue instead of starting over.
- Switching between AI coding tools without rebuilding the whole system, since
  each tool is just one entry in a shared menu.
- Auditing what happened: mail-style messages between workers, event logs, and
  task history show who did what and when.

## Conclusions & takeaways

- GasTown turns a crowd of AI coders into a supervised team: separate
  workspaces, one shared task list, checked merges, and automatic restarts.
- Isolation is the big idea: one worker, one folder copy, one branch. That
  single rule prevents most collisions.
- Merging is cautious by design: rehearse first, refuse on conflict, keep the
  evidence, and ask the worker to fix it.
- Memory is expendable, records are not: a crashed worker's thinking is lost,
  but its tasks, files, and branches survive.
- Flexibility comes from a menu, not from custom code: supporting a new AI tool
  means adding a settings row, not a new software module.
- The pattern travels well: any system that runs many AI agents at once needs
  the same five pieces — isolation, a task ledger, safe merging, supervision
  with patient restarts, and a tool menu.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| Rig | One managed project site: one codebase copy plus its workers and task list. |
| Polecat | A short-term task worker: created for one job, shut down when done. |
| Hook | Pinning one task to one worker, like clipping a job ticket to someone's shirt. |
| Worktree | A separate folder copy of the code where a worker can edit without disturbing others. |
| Beads | The shared task list: every job, message, and worker identity is one entry. |
| Convoy | A group of linked tasks that are handed to workers one ready item at a time. |
| Daemon | A background supervisor program that keeps checking and restarting workers. |
| Harness | The AI coding tool being driven, such as Claude or Codex. |
| ACP | Agent Client Protocol: a structured message channel for talking to an AI tool instead of typing into its terminal. |
| tmux | A terminal manager that keeps worker sessions alive in the background. |
| Dolt | A database that stores tables like normal but also keeps version history like code. |
| Flock | A file-based "do not enter" flag that stops two managers acting at the same moment. |
