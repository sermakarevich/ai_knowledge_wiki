> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Best practices for Claude Code - Claude Code Docs — In Plain Language

## What is this about?

Claude Code is not a chatbot that just answers questions and waits.

It is an assistant that can read your files, run commands, edit code,
and work through a programming problem on its own while you watch,
give directions, or step away.

This guide is a set of habits for using that kind of assistant well.

The short version is: be specific, give it a way to check its own work,
research before changing code, and save your repeating setup in a file
so every session starts smart.

## Why does it matter?

Claude remembers your whole conversation: every message, every file it
read, and every command result.

A single bug hunt or codebase tour can fill that memory with tens of
thousands of pieces of text.

When that memory gets full, Claude starts to forget your earlier
instructions and makes more mistakes.

So every best practice here is really about managing that memory:
give Claude less clutter, clearer goals, and tools that let it correct
itself instead of waiting for you to notice every error.

Without these habits, you become the checker — every mistake pauses
until you spot it.

With them, you get a session you can walk away from and come back to
finished work.

## How does it work?

Think of it as four habits plus one setup file plus one command-line trick.

**1. Give Claude a check it can run.**

Tell Claude how to prove the work is done: a test suite, a build
command, a linter, a script that compares output to an expected result,
or a screenshot comparison for visual work.

For example, instead of "make a function that checks email addresses,"
say what passes and what fails, then ask it to run the tests.

For visual work, paste a design screenshot and ask Claude to build it,
screenshot the result, list the differences, and fix them.

Always ask for evidence — the test output or command result — not just
"it works."

**2. Explore first, then plan, then code.**

Do not jump straight to fixes. Follow four phases:

- Explore: let Claude read and answer questions without changing anything.
- Plan: ask for a step-by-step plan of which files change and how.
- Implement: approve the plan, then build with tests and checks.
- Commit: ask Claude to write a clear commit message and open a pull request.

There is a special read-only mode for the first two phases so Claude
looks but does not touch.

Skip planning only for tiny, obvious tasks — a typo, a log line, a rename.
A good rule: if you can describe the change in one sentence, skip the plan.

**3. Be specific in your requests.**

Vague asks get vague results. Precise asks need fewer corrections.

Name the file and the exact case, point to helpful history or examples,
and describe both the symptom and what "fixed" looks like.

For example, instead of "fix the login bug," say where logins fail,
which folder handles login, and ask for a failing test first, then the fix.

**4. Give Claude rich material directly.**

Do not just describe code — point Claude at it.

You can tag files, paste or drag in images, share documentation links,
pipe in logs and errors, or let Claude fetch things itself with commands.

**5. Save repeating setup in a CLAUDE.md file.**

CLAUDE.md is a short note Claude reads at the start of every session.
It holds the commands, style rules, and workflow habits your project
always needs.

You can generate a starter automatically, then trim it over time.

**6. Use one-off commands for quick questions.**

You do not always need a full chat. A single command can ask one
question and print the answer, either as plain text, as structured
data for scripts, or as a live stream for long tasks.

## Where can this be used?

- Adding a new feature across several files, like a login option.
- Tracking down a bug, such as sessions that break after timeout.
- Writing tests for tricky edge cases, like a logged-out user.
- Cleaning up code style across a project with shared rules.
- Reviewing a design change by comparing screenshots.
- Automating quick jobs in scripts, like listing endpoints or reading logs.
- Onboarding a team: one shared setup file teaches every new session
  the same commands, style, and habits.

## Conclusions & takeaways

- Memory is the scarcest resource. Everything that saves memory —
  short setup files, focused questions, separate research from coding —
  makes Claude smarter for longer.
- A runnable check turns Claude from a guesser into a self-corrector.
  Never leave "looks done" as the only signal.
- Research before repair. A few minutes of reading and planning avoids
  solving the wrong problem.
- Specificity pays. Files, examples, symptoms, and done-states cut
  the back-and-forth.
- Write down what repeats. A short, shared setup file compounds in value
  because every future session benefits.
- Match the tool to the job: full sessions for big work, one-off commands
  for quick answers, structured output when a script needs the result.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Agentic coding | An assistant that reads, runs, and edits on its own, not just chats |
| Context window | Claude's working memory for one session; everything said, read, and run |
| Plan mode | A read-only setting where Claude studies code without changing it |
| Verification check | A test, build, or comparison Claude runs itself to prove the work passes |
| CLAUDE.md | A short project note Claude reads at the start of every session |
| Linter | A tool that scans code for style errors and likely mistakes |
| Test suite | A collection of automatic checks that pass or fail after a change |
| Single test run | Running just one check instead of all of them, to save time |
| Typecheck | An automatic scan that catches wrong data types before running code |
| Non-interactive mode | Asking one question with a single command instead of opening a chat |
| Stream output | Getting the answer piece by piece as it is produced, for long tasks |
| Skill | An extra knowledge pack Claude loads only when needed, keeping memory light |
