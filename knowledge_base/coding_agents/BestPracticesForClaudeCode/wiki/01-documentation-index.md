[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Documentation Index

**In one sentence:** Claude Code is an agentic coding environment whose context window fills fast (tens of thousands of tokens per session) and degrades as it fills, so the guide's core patterns are discovering docs via `/docs/llms.txt`, giving Claude a runnable verification check, separating explore/plan from implementation, and supplying specific, rich context plus environment setup.

## Key points

- Discover all available pages via the complete documentation index at `/docs/llms.txt` before exploring further.
- Claude Code is agentic: it reads files, runs commands, makes changes, and autonomously works through problems while you watch, redirect, or step away.
- The governing constraint is context: the window holds every message, file read, and command output, a single debugging session or exploration can consume tens of thousands of tokens, and performance degrades ("forgetting" earlier instructions, more mistakes) as it fills.
- Give Claude a runnable check (test suite, build exit code, linter, output-diff script, browser screenshot comparison) so it iterates itself instead of making you the verification loop.
- Follow the four-phase workflow Explore → Plan → Implement → Commit, using plan mode (Shift+Tab until `⏸ plan mode on`, or `claude --permission-mode plan`) so Claude reads without making changes.
- Make prompts specific: scope the file/scenario/test preferences, point to sources (e.g. git history), reference existing codebase patterns, and describe the symptom plus what "fixed" looks like.
- Provide rich content directly: `@`-reference files, paste/drag images, give documentation URLs (allowlist via `/permissions`), pipe data (`cat error.log | claude`), or let Claude fetch via Bash/MCP/file reads.
- Configure the environment persistently with `CLAUDE.md` (generate a starter via `/init`), which Claude reads at the start of every conversation for Bash commands, code style, and workflow rules.

---

## Documentation Index

Fetch the complete documentation index at: `/docs/llms.txt`. Use this file to discover all available pages before exploring further.

**Covers:** Documentation index pointer and context-window constraint framing the guide

## Agentic framing and the context-window constraint

Claude Code is an agentic coding environment:

> "Unlike a chatbot that answers questions and waits, Claude Code can read your files, run commands, make changes, and autonomously work through problems while you watch, redirect, or step away entirely."

> "Instead of writing code yourself and asking Claude to review it, you describe what you want and Claude figures out how to build it. Claude explores, plans, and implements."

Most best practices follow from one constraint:

> "Claude's context window holds your entire conversation, including every message, every file Claude reads, and every command output."

> "A single debugging session or codebase exploration might generate and consume tens of thousands of tokens."

> "When the context window is getting full, Claude may start "forgetting" earlier instructions or making more mistakes. The context window is the most important resource to manage."

Related pointers named in the chunk: an interactive walkthrough of what loads at startup and per-file-read cost, a custom status line for continuous context tracking, and "Reduce token usage" strategies.

## Give Claude a way to verify its work

> "Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from."

> "Claude stops when the work looks done. Without a check it can run, "looks done" is the only signal available, and you become the verification loop: every mistake waits for you to notice it."

The check is anything returning a signal Claude can read in-conversation: a test suite, a build exit code, a linter, a script diffing output against a fixture, or a browser screenshot compared against a design. Run `/verify` yourself after Claude's check passes to confirm against the running app.

| Strategy | Before | After |
|---|---|---|
| Provide verification criteria | "implement a function that validates email addresses" | "write a validateEmail function. example test cases: user@example.com is true, invalid is false, user@.com is false. run the tests after implementing" |
| Verify UI changes visually | "make the dashboard look better" | "[paste screenshot] implement this design. take a screenshot of the result and compare it to the original. list differences and fix them" |
| Address root causes, not symptoms | "the build is failing" | "the build fails with this error: [paste error]. fix it and verify the build succeeds. address the root cause, don't suppress the error" |

Gating options and their trade-offs:

- In one prompt: ask Claude to run the check and iterate in the same message (works on any task today).
- Across a session: set the check as a `/goal` condition; a separate evaluator re-checks after every turn. If Claude stalls, Claude Code eventually stops with the goal still set.
- As a deterministic gate: a Stop hook runs the check as a script and blocks the turn from ending until it passes; Claude Code overrides the hook and ends the turn after 8 consecutive blocks.
- By a second opinion: a verification subagent or dynamic workflow with a fresh model tries to refute the result, so the worker isn't its own grader.

> "Have Claude show evidence rather than asserting success: the test output, the command it ran and what it returned, or a screenshot of the result."

## Explore first, then plan, then code

> "Separate research and planning from implementation to avoid solving the wrong problem."

Four phases:

1. **Explore** — Enter plan mode (Shift+Tab until `⏸ plan mode on`, or `claude --permission-mode plan`); Claude reads files and answers questions without making changes. Example prompt: `read /src/auth and understand how we handle sessions and login. also look at how we manage environment variables for secrets.`
2. **Plan** — Ask for a detailed implementation plan (example: `I want to add Google OAuth. What files need to change? What's the session flow? Create a plan.`). Press Ctrl+G to open the plan in a text editor for direct editing.
3. **Implement** — Approve the plan or leave plan mode (Shift+Tab), then implement with verification (example: `implement the OAuth flow from your plan. write tests for the callback handler, run the test suite and fix any failures.`).
4. **Commit** — Ask Claude to commit with a descriptive message and open a PR.

When to skip planning: tasks where scope is clear and the fix is small (typo, log line, variable rename). Plan when the approach is uncertain, multiple files change, or the code is unfamiliar. Rule of thumb: "If you could describe the diff in one sentence, skip the plan."

## Provide specific context in your prompts

> "The more precise your instructions, the fewer corrections you'll need."

> "Claude can infer intent, but it can't read your mind. Reference specific files, mention constraints, and point to example patterns."

| Strategy | Before | After |
|---|---|---|
| Scope the task | "add tests for foo.py" | "write a test for foo.py covering the edge case where the user is logged out. avoid mocks." |
| Point to sources | "why does ExecutionFactory have such a weird api?" | "look through ExecutionFactory's git history and summarize how its api came to be" |
| Reference existing patterns | "add a calendar widget" | "look at how existing widgets are implemented on the home page… HotDogWidget.php is a good example. follow the pattern to implement a new calendar widget that lets the user select a month and paginate forwards/backwards to pick a year. build from scratch without libraries other than the ones already used in the codebase." |
| Describe the symptom | "fix the login bug" | "users report that login fails after session timeout. check the auth flow in src/auth/, especially token refresh. write a failing test that reproduces the issue, then fix it" |

Vague prompts (e.g. "what would you improve in this file?") are useful when exploring and able to course-correct.

## Provide rich content

> "Use @ to reference files, paste screenshots/images, or pipe data directly."

- Reference files with `@` instead of describing where code lives; Claude reads the file before responding.
- Paste images directly (copy/paste or drag and drop).
- Give URLs for documentation and API references; use `/permissions` to allowlist frequently-used domains.
- Pipe in data, e.g. `cat error.log | claude`.
- Let Claude fetch what it needs via Bash commands, MCP tools, or file reads.

## Configure your environment

> "A few setup steps make Claude Code significantly more effective across all your sessions."

Write an effective `CLAUDE.md`: run `/init` to generate a starter based on project structure, then refine over time. `CLAUDE.md` is read at the start of every conversation; include Bash commands, code style, and workflow rules. No required format, but keep it short and human-readable.
