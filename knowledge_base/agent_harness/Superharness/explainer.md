> [[index|Wiki]] | [[summary|Summary]]

# superharness — In Plain Language

## What is this about?

Imagine a construction site where five different crews show up to renovate one house. Each crew speaks a different language and has its own tools. Without coordination, two crews paint the same wall different colors, one knocks down what another just built, and nobody remembers what happened yesterday.

Superharness is the site office that prevents that chaos. There is one shared whiteboard everyone must check (a single file that records the true state of all work), one ticket queue that hands out jobs one at a time, and a rulebook posted on the wall that says what each crew is allowed to do and when.

Think of it also like a relay race where the baton carries written notes. When one runner drops out mid-race, the next runner picks up the baton, reads the notes, and knows exactly where to continue — no restarting from zero.

## Why does it matter?

Today, if you ask several AI assistants to help with one project, three everyday problems appear. First, they overwrite each other, like two people editing the same document at once. Second, they forget everything between sessions, so every restart loses progress. Third, nobody watches them, so a stuck helper can sit silently for hours while you assume work is getting done.

If this kind of coordination works, a team of AI helpers can share one project safely: jobs are handed out fairly, crashes lose nothing, stuck work gets noticed and reassigned, and finished work is checked before it counts as done.

## How does it work?

1. **Write the job on the shared whiteboard.** Every task goes into one notebook file that is the single source of truth. Nothing counts unless it is written there.
2. **Put a ticket in the queue.** Each job becomes a ticket in a take-a-number line. The system refuses duplicates, so the same job cannot be handed out twice.
3. **Hand one ticket to one crew.** The supervisor picks the top ticket and gives it to exactly one helper, in its own separate work area — like giving each crew its own room to renovate so they never bump into each other.
4. **Check the rulebook before starting.** Before work begins, the supervisor checks: is this job ready, are its prerequisites done, does this helper have the right skills? If not, the job waits.
5. **Leave notes as you go.** Helpers regularly signal "I am still alive" and leave written handoff notes — a plan first, then a final report. These notes are never erased, only added to, so history survives crashes.
6. **The supervisor walks the site.** A background watcher keeps patrolling: it notices helpers that went quiet, restarts crashed jobs with their notes intact, limits endless retries, and kills work that has been idle or running far too long.
7. **Inspect before you sign off.** Closing a job requires passing checks: the report is ready, smaller sub-jobs are finished, the work was verified, and the right owner approves. Only then is the job marked done and the notes filed for future jobs to learn from.

## Where can this be used?

The obvious use is coding: running several AI coding assistants on one software project without collisions, lost work, or silent stalls.

But the pattern fits any team of AI helpers sharing work. A group of research assistants could split up reading papers and pooling summaries into one notebook. A data-labelling crew could claim labelling tickets from a queue without double-labelling the same item. A fleet-style job system could dispatch analysis, writing, or checking tasks to whatever helper is free, recover from failures automatically, and keep a permanent log of who did what and what was learned.

## Conclusions & takeaways

What to remember in a month: one shared notebook beats five private memories; a ticket queue beats shouting across the site; separate work areas beat stepping on each other; written handoff notes beat starting over; and a patrolling supervisor beats hoping everything is fine.

Honest limitations in plain words: the supervisor itself is a big, complicated piece of machinery that is hard to change safely. If helpers or dashboards look at a different copy of the notebook by mistake, they see a different reality. And past versions show the supervisor itself can once go quiet for many hours without anyone noticing — which is why it now needs its own watchers watching the watcher.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Harness | A wrapper that lets the supervisor start and talk to one brand of AI helper |
| Adapter | A translator plug that converts a generic job ticket into the specific launch instructions one helper brand understands |
| SQLite | A simple filing-cabinet database stored as a single file on your computer, no internet server needed |
| Inbox / queue | The take-a-number ticket line where jobs wait until a helper is free to claim one |
| Dispatch | The act of handing the next waiting ticket to one specific helper and starting it |
| Lifecycle | The allowed life story of a job, from to-do to in-progress to reviewed to done, with rules against skipping steps |
| Handoff | The written note a helper leaves behind (plan first, report at the end) so the next helper can continue |
| Ledger | The permanent diary that records every important event — who did what, when — and is never rewritten |
| Watchdog | The automatic guard that ends jobs left sitting idle too long or running past their absolute time limit |
| Heartbeat | A regular "I am still alive" signal each worker and supervisor sends so silence means trouble |
| Worktree | A separate scratch copy of the project given to one helper so crews never edit the same files at once |
| Fanout / swarm | Sending copies or pieces of one job to several helpers at once, then comparing or combining their answers |
