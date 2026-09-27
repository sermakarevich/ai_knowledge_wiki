> [[index|Wiki]] | [[summary|Summary]]

# Vibe Kanban — In Plain Language

## What is this about?

Imagine a restaurant kitchen during the dinner rush. Orders come in on tickets,
each ticket goes to its own cooking station, and no cook messes with another
cook's dish. When a dish is ready, the head chef tastes it before it goes out.

Vibe Kanban works the same way, but for writing software with AI helpers.
It is a big visual board covered in task cards, like sticky notes on a wall.
Each card describes one job to be done, for example "fix the login button".

Behind the board, each card gets its own separate kitchen station: a private,
isolated copy of the project where an AI coding assistant does the work.
The human stays in the head-chef role. You plan on the board, the AI assistants
cook in parallel, and you taste-test each result before accepting it.

## Why does it matter?

The hard part of using AI to write software is not asking for help.
It is keeping track of everything that happens after you ask.

Without a system like this, three problems pile up fast.
First, parallel work turns into chaos: five AI assistants editing the same
files at once will overwrite each other, like five cooks stirring one pot.
Second, every AI assistant speaks a slightly different language, so following
their progress means learning five different dashboards.
Third, the connection between the plan and the result gets lost: you forget
what you asked for, what the AI actually changed, and why.

Vibe Kanban exists to fix that planning-and-review bottleneck.
It gives every AI job its own isolated workspace, translates all the different
AI assistants into one common activity feed, and keeps the original task card,
the AI's work, and your review comments tied together in one place.
You spend your time deciding what should be built and whether the result
is good enough, instead of babysitting files and chat windows.

## How does it work?

Think of it like ordering custom furniture from several workshops at once.
You pin order slips to a board, each workshop builds its piece from a copy
of the blueprint, and you inspect each piece when it arrives.

1. Write the order slip. You create a card on the board with a title and
   a short description. That description becomes the instructions the AI
   assistant will follow.

2. Open a private workshop. With one click, the card gets its own isolated
   workspace: a separate copy of the project plus its own work branch.
   Nothing built here can disturb the other cards.

3. Send in the worker. You pick which AI assistant should do the job,
   and it starts working inside that private copy. Its progress, tool use,
   and thinking are translated into a single simple feed you can watch live.

4. Try the product. While the assistant works, you can run the half-built
   result and look at it in a built-in preview window, like test-sitting
   a chair before the varnish dries.

5. Inspect the difference. When the work is done, the app shows you exactly
   what changed compared with the original, file by file. You can leave
   comments, and your notes are stapled to your next instruction when you
   ask the assistant for fixes.

6. Accept or ship it. Happy with the result? You approve it and the changes
   are packaged up as a formal proposal for the team, called a pull request,
   or merged straight in. The card then slides across the board from
   "to do" to "in progress" to "done" automatically.

All of this runs on your own computer by default, and your history is kept
in a single small database file, like a ledger book under the counter.

## Where can this be used?

Anywhere several pieces of skilled work must happen at once and be reviewed
before they count.

A small software team can use it to fix ten bugs in parallel overnight,
with one developer reviewing all ten results in the morning like an editor
checking overnight drafts.

A freelancer juggling three clients can keep each client's work in its own
isolated workspace, switching between them without mixing anything up.

A teacher can give every student the same starting project, let an AI helper
assist each student separately, and then compare what changed in each copy.

Outside coding entirely, the same pattern fits any review-heavy work.
A legal team could draft five contract versions side by side and compare
each against the original. A writing team could develop several chapters
or translations in parallel and keep every comment attached to its draft.
A research lab could run several data-analysis attempts from the same
dataset without letting one experiment contaminate another.

## Conclusions & takeaways

What to remember: Vibe Kanban is a planning board with private workrooms
behind it. The board is for humans, the workrooms are for AI assistants,
and the review screen in between is where quality is decided. Isolation
prevents messes, a shared activity feed prevents confusion, and tying every
change back to its task card prevents forgotten context.

Honest limits: this is a manager, not a genius. It does not write code
itself and it cannot judge quality for you; a careless review still lets
bad work through. Big jobs interrupted by a restart do not resume by
themselves, and running many assistants at once needs a strong computer.
Importantly, the original maker shut the project down in April 2026,
so today it survives only through community volunteers. Expect some rough
edges, outdated connections to AI assistants, and no official support line.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| Kanban board | A wall of columns with task cards that move left to right as work progresses |
| AI coding agent | A program that reads instructions and writes or edits files on its own |
| Workspace | A private copy of the project reserved for one task, like a separate workbench |
| Worktree | The actual folder on disk holding that private copy |
| Diff | A side-by-side list showing exactly what was added, removed, or changed |
| Pull request | A formal proposal saying "here are my changes, please review and accept them" |
| Branch | A named parallel version of the project where experimental work stays separate |
| Preview | A live test window where you can try the half-finished result in your browser |
| MCP config | Settings that give the AI assistant extra tools, like handing a cook new utensils |
| SQLite database | A tiny filing cabinet stored as one file that remembers all tasks and results |
