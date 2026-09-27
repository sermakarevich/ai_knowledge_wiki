> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Documentation Index
**In one sentence:** Claude Code is an AI coding assistant that works across terminal, IDE, desktop, and web surfaces to build features, fix bugs, and automate development tasks, with the full documentation index discoverable at /docs/llms.txt.
## Key points
- Claude Code "understands your entire codebase and can work across multiple files and tools to get things done," handling features, bug fixes, tests, lint fixes, merge conflicts, dependency updates, and release notes.
- It runs on five main surfaces — Terminal CLI, VS Code, Desktop app, Web, and JetBrains — all sharing the same underlying engine, CLAUDE.md files, settings, and MCP servers.
- Native install is recommended via `curl -fsSL https://claude.ai/install.sh | bash` (macOS/Linux/WSL), `irm https://claude.ai/install.ps1 | iex` (PowerShell), or CMD installer; Homebrew (`brew install --cask claude-code`, stable channel ~1 week behind) and WinGet (`winget install Anthropic.ClaudeCode`) do not auto-update.
- Customization rests on CLAUDE.md project instructions (plus AGENTS.md compatibility and auto memory), shareable skills such as `/review-pr` or `/deploy-staging`, and hooks that run shell commands before/after actions.
- MCP (Model Context Protocol) connects Claude Code to external sources such as Google Drive, Jira, Slack, or custom tooling.
- Automation paths include Unix-style piping (`tail -200 app.log | claude -p ...`), CI via GitHub Actions or GitLab CI/CD, background/parallel agents, the Agent SDK, scheduled Routines, `/schedule`, `/loop`, and `claude --teleport` / `/desktop` handoffs.
- Work moves between surfaces via Remote Control, message dispatch from phone, Slack `@Claude` mentions returning PRs, Chrome debugging, and Channels for Telegram/Discord/iMessage/webhooks.
---
## Documentation index pointer
**Covers:** chunk lines 9–15

Fetch the complete documentation index at: `/docs/llms.txt`. Per the chunk: "Use this file to discover all available pages before exploring further."

## Get started — surfaces and install
**Covers:** chunk lines 23–101

Claude Code runs on the terminal, IDE extensions, a desktop app, and the web. "Most surfaces require a Claude subscription or Anthropic Console account. The Terminal CLI, VS Code, and JetBrains also support third-party providers."

- **Terminal (full-featured CLI):** native install recommended; native installs "automatically update in the background"; Git for Windows recommended on native Windows so Claude Code can use the Bash tool (otherwise PowerShell); WSL needs no Git for Windows. Start with `cd your-project` then `claude`; first use prompts login unless `ANTHROPIC_API_KEY` is set (then it asks to approve the key).
- **VS Code:** inline diffs, @-mentions, plan review, conversation history; install via marketplace links or searching "Claude Code" in Extensions view, then Command Palette → "Claude Code" → Open in New Tab.
- **Desktop app:** standalone app with visual diff review, multiple side-by-side sessions, scheduled recurring tasks, cloud sessions; downloads for macOS (Intel and Apple Silicon), Windows x64, Windows ARM64, plus Ubuntu/Debian via apt (beta); includes Claude Code so no separate CLI install; paid subscription required; launch and click Code tab.
- **Web:** no local setup at claude.ai/code; for long-running tasks, parallel tasks, repos not held locally, or projects coordinating parallel sessions; desktop browsers and Claude iOS/Android app.
- **JetBrains:** plugin for IntelliJ IDEA, PyCharm, WebStorm and others with interactive diff viewing and selection context sharing; requires separately installed CLI.

## What you can do
**Covers:** chunk lines 107–175

- **Automate deferred work:** "writing tests for untested code, fixing lint errors across a project, resolving merge conflicts, updating dependencies, and writing release notes." Example: `claude "write tests for the auth module, run them, and fix any failures"`.
- **Build features and fix bugs:** "Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works." For bugs, paste the error or symptom; it traces, finds root cause, and fixes.
- **Commits and PRs:** stages changes, writes messages, creates branches, opens PRs; example `claude "commit my changes with a descriptive message"`; CI review/triage via GitHub Actions or GitLab CI/CD.
- **MCP tools:** "The Model Context Protocol (MCP) is an open standard for connecting AI tools to external data sources."
- **Customize:** `CLAUDE.md` in project root read at session start for standards, architecture, libraries, checklists; Agent SDK and background agents for parallel/custom workflows; CLI piping examples: `tail -200 app.log | claude -p "Slack me if you see any anomalies"`, `claude -p "translate new strings into French and raise a PR for review"`, `git diff main --name-only | claude -p "review these changed files for security issues"`.
- **Recurring tasks:** morning PR reviews, overnight CI analysis, weekly dependency audits, post-merge doc syncs; cloud Routines (triggerable via API calls or GitHub events; created from web, Desktop app, or `/schedule`), Desktop scheduled tasks (local files/tools), `/loop` for in-session polling.
- **Work from anywhere:** Remote Control from phone/browser; message dispatch creating Desktop sessions; `claude --teleport` to pull web/mobile tasks into terminal (requires claude.ai subscription); `/desktop` to continue terminal sessions in Desktop app (requires claude.ai subscription; macOS and x64 Windows); Slack `@Claude` mentions returning a PR.

## Use Claude Code everywhere
**Covers:** chunk lines 181–203

| What I want to do | Best option |
|---|---|
| Continue a local session from my phone or another device | Remote Control |
| Push events from Telegram, Discord, iMessage, or my own webhooks into a session | Channels |
| Start a task locally, continue on mobile | `claude --cloud`, then the Claude mobile app |
| Run Claude on a recurring schedule | Routines or Desktop scheduled tasks |
| Automate PR reviews and issue triage | GitHub Actions or GitLab CI/CD |
| Get automatic code review on every PR | GitHub Code Review |
| Route bug reports from Slack to pull requests | Slack |
| Debug live web applications | Chrome |
| Build custom agents for your own workflows | Agent SDK |

## Next steps
**Covers:** chunk lines 209–235

Once installed: Quickstart (first task to committed fix), storing instructions/memories (CLAUDE.md and auto memory), common workflows and best practices, Claude Academy (Claude Code 101, Claude Code in Action), "A harness for every task" (dynamic multi-subagent workflows), Settings, Troubleshooting, and code.claude.com for demos, pricing, and product details.
