> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# A 3-step AI coding workflow for solo founders | Ryan Carson (5x founder) — In Plain Language

## What is this about?

This is a simple, repeatable way to build big software features with an AI coding assistant, without the AI going off the rails.

The speaker, a five-time startup founder, shows how he builds features of around 10,000 lines of code by himself using Cursor, an AI-powered code editor.

His main point is short: most people fail with AI coding because they rush. They give the AI a vague request and hope for the best. The AI then guesses, makes mistakes, and the person ends up stuck in a mess they have to undo.

His fix is to slow down and follow three steps, every time:

1. Write a clear plan of what to build.
2. Break that plan into small checked-off tasks.
3. Build one small task at a time, with a human checking each step.

Think of it like cooking with a very smart but literal helper. If you say "make dinner," you get chaos. If you write the recipe, chop it into steps, and taste after each step, dinner actually works.

## Why does it matter?

If you are building a startup alone, or on a tiny team, you cannot hire a product manager, a team of engineers, and a tester for every idea.

This workflow gives you leverage. It lets one person do work that used to need many people: deciding what to build, breaking it into steps, and writing the code.

It also solves the most common pain of AI coding: the AI is brilliant but forgets obvious things. The speaker compares it to a genius student who misses simple details that every human knows. Without clear instructions, it fills in the blanks wrongly.

Slowing down at the start feels slower, but it actually saves hours. You avoid the classic trap: the AI writes a lot of code fast, introduces small errors, and you spend half a day untangling it or throwing it away.

The payoff he claims is large: reliable big features, built solo, with far fewer reversals. Not as deep as a great product manager or chief technology officer, but good enough to build a whole company alone — where his last company needed about 110 people.

## How does it work?

The whole loop runs inside Cursor, in its "agent mode," using three short instruction files called rules. Each rule tells the AI exactly how to behave at one stage.

**Step 1 — Write the plan.**

You point the AI at the first rule file and give a one-sentence feature idea. His demo example: "add a report showing all boat names of yacht-club members and how many emails they were sent."

The AI must ask clarifying questions before writing anything. For example: what problem does this report solve? Who will use it? Where should it live in the app?

You answer briefly. If a question does not matter, you say "you pick" or "use your best judgment."

One formatting trick: force the AI to number its questions like 2.1, 2.2, 2.3. Otherwise it bundles several questions into one bullet and they are hard to answer one by one.

The result is a plan document, sometimes called a PRD, written in plain markdown and saved in a `tasks/` folder. It lists what to build, the functional requirements, what is explicitly out of scope, and design notes. The rule frames it as "clear enough for a junior developer to implement," which keeps it concrete.

**Step 2 — Break the plan into tasks.**

You point the AI at the second rule file, attach the plan, and ask it to generate tasks.

The output is a markdown checklist with parent tasks, subtasks, and sub-subtasks, plus a list of relevant files in the codebase. For example: task 1, subtask 1.1, subtask 1.2, and so on.

The rule tells the AI to pause and wait for you to say "go" before expanding into fine detail. This alone is valuable even before any code is written, because many teams get stuck turning a vague plan into concrete steps that fit their actual codebase.

**Step 3 — Build one subtask at a time.**

You point the AI at the third rule file plus the task list, and say "let's start."

Now the strict rules kick in:

- Do exactly one subtask at a time, never everything at once.
- Mark it done in the checklist immediately.
- Then stop and wait for your go-ahead, often just typing "y" or "yes."

In the demo, the first subtask reads the existing database schema file, makes the change, and ticks off item 1.1 with a chime sound. Then the human checks it before allowing 1.2.

After each step you check for small mistakes, because the AI often introduces a minor error. You commit your code after finishing a larger parent task, whenever the app is in a working state. His rule of thumb: "if I had to undo this now, how bad would it be?"

Around this core loop are a few helper habits: ask the database directly instead of writing query code by hand, shrink the code sent to the AI so it only sees what matters, keep the task list as a simple editable text file, stick with one AI model long enough to learn its strengths, and nudge a stuck AI politely, like coaching a person, rather than scolding it.

## Where can this be used?

- A solo founder adding a real feature to a startup app without hiring engineers.
- A small team turning a rough idea into a concrete, checkable build plan.
- Anyone whose AI coding sessions keep derailing into errors and reverts.
- Breaking a scary 10,000-line feature into safe half-day chunks with checks after each step.
- Keeping database, browser-testing, and code-context helpers plugged into the same chat where the code is written.
- Learning AI coding by practice: narrowing each request until the AI can actually do it well.

What it is not for: replacing careful product or technical leadership on hard decisions, or running fully on autopilot. The human check after every subtask is the point.

## Conclusions & takeaways

- Slow down to speed up: patience with instructions beats fast vague prompts.
- Always plan before coding: a short written plan plus clarifying questions prevents most failures.
- Small steps win: one subtask at a time, checked off, with a pause for approval.
- Check everything: expect small AI mistakes and catch them early while they are cheap to fix.
- Save working states: commit after each solid chunk so you can always go back safely.
- Keep it simple: a plain markdown checklist you can see and edit beats a fancy tracking tool at the start.
- Solo leverage is real: with this loop, one disciplined founder can ship what once took a team.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| PRD (plan document) | A short written plan saying what to build, who it is for, and what is out of scope. |
| Task list | The plan broken into numbered checkboxes: big tasks, smaller subtasks, and tiny sub-steps. |
| Cursor rule | A saved instruction file that tells the AI how to behave at one stage of the work. |
| Agent mode | A setting where the AI can read files, write code, and take actions, not just chat. |
| Context | The background info the AI can see: your instructions, rules, and selected code. |
| Context window | How much text the AI can consider at once; smaller and relevant is better. |
| MCP | A plug-in that lets the AI coding tool talk to outside services like a database or browser. |
| Prisma schema | A file describing the shape of your database tables, which the AI reads before changing them. |
| Commit | Saving a working snapshot of your code so you can safely return to it later. |
| Linter error | A small automatic complaint about code style or simple mistakes, easy to fix if caught early. |
| Vibe-coded | Built fast by describing what you want to the AI, without carefully planning first. |
| Token | A small chunk of text the AI reads; fewer relevant tokens means cheaper and more focused work. |
