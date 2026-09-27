> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Overview - Claude Code Docs — In Plain Language

## What is this about?

Claude Code is an AI coding assistant that works with your whole project, not just one file at a time.

You describe what you want in plain words — "add this feature," "fix this bug," "write tests for this module" — and it plans the work, edits several files, and checks that the result works.

It is not a single tool in a single place. It is one engine that shows up in five places: the terminal, VS Code, JetBrains editors, a desktop app, and the web.

All five share the same memory, settings, and connections, so you can start work in one place and pick it up in another.

The docs page this explainer is based on is mostly a map: it tells you where to install each version, what each one is good at, and where to go next to learn more.

## Why does it matter?

Most coding helpers only finish your current line or answer questions about one snippet.

Claude Code matters because it takes on the boring, multi-step jobs developers usually postpone.

It can write tests for code that has none, fix lint errors across a whole project, sort out merge conflicts, update dependencies, and draft release notes.

It can also do the everyday loop: find the cause of an error, change the code, run the checks, stage a commit, open a pull request, and help review someone else's.

Because the same assistant follows you from terminal to editor to phone, unfinished work does not get stuck on one machine.

And because you can teach it your project's rules once, it stops giving generic answers and starts working the way your team works.

## How does it work?

Think of it in three layers: the engine, your instructions, and outside connections.

The engine is the shared core. Whether you type `claude` in the terminal or open the Code tab in the desktop app, the same assistant reads your files and makes changes.

Your instructions are how you shape it. The main one is a file called `CLAUDE.md` in your project folder. It holds things like coding standards, architecture notes, allowed libraries, and checklists, and Claude reads it at the start of every session.

On top of that you can add reusable skills — saved routines with names like `/review-pr` or `/deploy-staging` — and hooks, which are small shell commands that run automatically before or after Claude does something.

Outside connections come through something called MCP, the Model Context Protocol. That is just a standard plug that lets Claude reach data outside your files, such as Google Drive, Jira, or Slack.

Automation is the last piece. You can pipe data into it from the command line, run it inside CI pipelines, launch background or parallel agents, schedule repeating jobs, or hand a session from one device to another.

A simple example from the docs: `tail -200 app.log | claude -p "Slack me if you see any anomalies"` means "read the end of this log and message me only if something looks wrong."

## Where can this be used?

Each surface fits a different moment. Pick by where you are and what the job needs.

- **Terminal (CLI):** the full-power option. Best for multi-file changes, scripting, piping data in and out, and CI-style work. Start with `cd your-project`, then `claude`. Native install is recommended because it updates itself in the background.
- **VS Code:** best for day-to-day editing, with inline diffs, @-mentions of files, plan review, and conversation history. Install it from the Extensions view by searching "Claude Code."
- **JetBrains (IntelliJ, PyCharm, WebStorm, and others):** similar to VS Code — diff viewing and sharing selected code — but it needs the CLI installed separately.
- **Desktop app:** best for visual review, running several sessions side by side, and scheduling repeating tasks. It already includes Claude Code, so no separate install. A paid subscription is required.
- **Web (claude.ai/code):** best when there is no local setup, for long-running or parallel tasks, or for repos you do not keep on your machine. Works from desktop browsers and the Claude mobile app.
- **On the go:** Remote Control and message dispatch let you steer or start sessions from your phone. `claude --teleport` pulls a web or mobile task into your terminal; `/desktop` sends a terminal session to the desktop app.
- **Team touchpoints:** Slack `@Claude` mentions can turn a bug report into a pull request; GitHub Actions or GitLab CI/CD run reviews and triage; Channels push events from Telegram, Discord, iMessage, or custom webhooks into a session; Chrome support helps debug live web apps.
- **Custom builds:** the Agent SDK lets you build your own agents and workflows on top of the same engine.

## Conclusions & takeaways

If you remember nothing else, remember these five points.

1. Claude Code is a whole-project helper, not an autocomplete. Give it goals, and it plans, edits, and verifies.
2. One engine, five doors. Terminal, VS Code, JetBrains, desktop, and web all share memory and settings — choose the door closest to the job.
3. Teach it once with `CLAUDE.md`, skills, and hooks, and every session gets better. Connect it with MCP when the answer lives outside your code.
4. Start small, then automate. Try one task by hand, then pipe data, schedule repeats, or run it in CI once the pattern works.
5. Install the native version if you can. It updates itself, while Homebrew and WinGet copies lag behind and need manual updates.

A good first week: install it, add a short `CLAUDE.md`, ask it to write one test file and fix one bug, then try a commit or a review with it.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| CLI | A text-based window where you type commands instead of clicking buttons. |
| CLAUDE.md | A note file in your project that tells Claude your rules and standards. |
| MCP (Model Context Protocol) | A standard plug that lets Claude read outside tools like Drive, Jira, or Slack. |
| Skill | A saved, reusable routine you can run by name, e.g. `/review-pr`. |
| Hook | A small command that runs automatically before or after Claude acts. |
| Agent SDK | A toolkit for building your own custom AI helpers on Claude's engine. |
| CI (Continuous Integration) | Automatic checks and builds that run whenever code is pushed. |
| Pull request (PR) | A packaged proposal to merge your changes, open for review first. |
| Lint | Automatic style and error checking for your code. |
| Routine / scheduled task | A job Claude runs on a repeating timetable, like a morning review. |
| Remote Control / teleport | Ways to move or steer a session between phone, web, terminal, and desktop. |
| Diff | A side-by-side view showing exactly what changed in the code. |
