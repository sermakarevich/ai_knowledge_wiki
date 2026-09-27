> [[index|Wiki]] | [[summary|Summary]]

# Bernstein — In Plain Language

## What is this about?

Bernstein is an open-source tool that manages teams of AI coding helpers.

Think of it like a foreman on a building site. The AI helpers do the
actual writing of computer code. Bernstein decides who does what,
in which order, and checks that the work is done well.

It does not write the code itself. It organizes the work.

## Why does it matter?

One AI helper working alone is easy to manage. Ten helpers working
at the same time is chaos.

Without a manager, they can:

- take the same task twice,
- overwrite each other's work,
- break the project without anyone noticing,
- leave no trace of who changed what.

Bernstein fixes this. It gives every helper a clear task, a separate
workspace, and a quality check. It also keeps a full record, so you can
replay what happened and prove who did what.

In short: it makes AI teamwork safe, repeatable, and honest.

## How does it work?

Imagine a big kitchen cooking a wedding dinner.

Bernstein is the head chef. The AI helpers are the cooks. Here is
what happens, step by step:

1. **The recipe is split into tasks.** The big goal ("build this feature")
is cut into small cards: "make the login page", "save passwords safely",
"write a test". Some cards depend on others, so the order matters.

2. **A cook claims one card.** Cards sit on a shared board. A cook takes
a card and marks it "mine". The system is careful here: two cooks can
never grab the same card, even if they reach at the same second.

3. **Each cook gets their own counter.** Every cook works at a separate
kitchen counter with their own copy of the ingredients. In software,
this is called a separate copy of the project. So nobody bumps into
anyone else or spills soup into someone else's pot.

4. **The head chef watches the clock.** Bernstein keeps walking around,
checking progress in a simple loop: "Is anyone stuck? Is a task done?
What is next?" This check uses plain fixed rules, not AI guesses,
so it always behaves the same way.

5. **Finished dishes go through tasting.** Before a dish reaches the
guests, it is tasted. Bernstein runs automatic checks: does the code
look tidy, does it follow the rules, do the tests pass? Bad work is
sent back to be fixed.

6. **One dish at a time goes to the table.** Even if five cooks finish
together, their dishes are served one by one. This avoids collisions
in the main project. If two cooks changed the same line, the conflict
is spotted and paused for a human.

7. **Everything is written in the logbook.** Every step — who cooked what,
when, with which result — is written in a tamper-proof notebook. If
someone changes one old page, the seal breaks and you can see exactly
where. You can replay the whole evening later, bite by bite.

If a task fails, Bernstein retries it, first with more effort, then
with a stronger helper. If it still fails after a few tries, it goes
to a special "gave up" list for a human to review.

## Where can this be used?

- **Software teams using AI coders.** Let many AI helpers work in parallel
without breaking the shared code.
- **Companies that need proof.** Banks, hospitals, and big firms must show
who changed what and when. The sealed logbook gives them that proof.
- **Trying many AI tools.** Bernstein speaks to 40+ different AI coding
tools through one simple plug system, so you can swap tools without
rebuilding everything.
- **Repeated, boring work.** Updates, migrations, tests, document writing —
any job you want to run the same way every time and replay if needed.

## Conclusions & takeaways

- Bernstein is a manager, not a worker. AI helpers write; it organizes.
- Separation prevents mess: one task, one worker, one private copy.
- Checks happen before merging, not after the damage is done.
- Failures are handled calmly: retry smarter, then ask a human.
- The record is the superpower: replayable, checkable, hard to fake.
- The result is AI coding that is faster but still controlled.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| Orchestrator | The head chef — the part that hands out tasks and checks progress |
| Worktree | A private copy of the project for one worker, like a separate kitchen counter |
| Deterministic scheduler | A task planner that follows fixed rules, so the same input always gives the same plan |
| Adapter | A plug that lets Bernstein talk to one specific AI tool, like a travel adapter for a socket |
| Merge gate | The tasting step — automatic checks the work must pass before joining the main project |
| Lineage receipt | A signed slip that says "this worker made this file at this time" |
| Audit chain | A notebook where each page seals the previous one, so you can spot any erased page |
| Backlog claim | Raising your hand and marking a task card "mine" so nobody else takes it |
| Dead-letter queue | The "gave up" list — tasks that failed too many times and wait for a human |
| Policy-as-code | House rules written as a settings file, enforced automatically instead of by nagging |
