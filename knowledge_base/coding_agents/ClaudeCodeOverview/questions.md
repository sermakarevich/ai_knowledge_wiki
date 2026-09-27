---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Overview - Claude Code Docs

### Q1. What is Claude Code and what kinds of development work does it handle?

> [!tip]- Answer
> Claude Code is an AI coding assistant that understands the entire codebase and works across multiple files and tools to get things done. It builds features from plain-language descriptions, traces and fixes bugs, and automates deferred work such as writing tests, fixing lint errors, resolving merge conflicts, updating dependencies, and writing release notes. See [[wiki/01-documentation-index|Documentation Index]].

### Q2. What are the five main surfaces Claude Code runs on, and what do they share?

> [!tip]- Answer
> Claude Code runs on the Terminal CLI, VS Code, the Desktop app, the Web, and JetBrains, all sharing the same underlying engine, CLAUDE.md files, settings, and MCP servers. Most surfaces require a Claude subscription or Anthropic Console account, while the Terminal CLI, VS Code, and JetBrains also support third-party providers. See [[wiki/01-documentation-index|Documentation Index]].

### Q3. How should Claude Code be installed on each platform, and what is the tradeoff of package managers?

> [!tip]- Answer
> Native install is recommended via `curl -fsSL https://claude.ai/install.sh | bash` on macOS/Linux/WSL, `irm https://claude.ai/install.ps1 | iex` in PowerShell, or the CMD installer, because native installs update automatically in the background. Homebrew (`brew install --cask claude-code`, stable channel about a week behind) and WinGet (`winget install Anthropic.ClaudeCode`) do not auto-update. See [[wiki/01-documentation-index|Documentation Index]].

### Q4. How do the VS Code, Desktop, Web, and JetBrains surfaces differ in setup and strengths?

> [!tip]- Answer
> VS Code offers inline diffs, @-mentions, plan review, and conversation history via the marketplace extension; JetBrains provides interactive diff viewing and selectioncontext sharing but requires a separately installed CLI. The Desktop app is standalone with visual diff review, multiple side-by-side sessions, and scheduled tasks but needs a paid subscription, while the Web at claude.ai/code needs no local setup and suits long-running, parallel, or non-local repo tasks. See [[wiki/01-documentation-index|Documentation Index]].

### Q5. How do CLAUDE.md, skills, hooks, and MCP turn Claude Code into project-specific workflows?

> [!tip]- Answer
> A `CLAUDE.md` file in the project root is read at session start for standards, architecture, libraries, and checklists, with AGENTS.md compatibility and auto memory; shareable skills such as `/review-pr` or `/deploy-staging` encode repeatable routines and hooks run shell commands before or after actions. MCP (Model Context Protocol), an open standard for connecting AI tools to external data sources, links Claude Code to sources like Google Drive, Jira, Slack, or custom tooling. See [[wiki/01-documentation-index|Documentation Index]].

### Q6. What automation paths does Claude Code support, from one-liners to scheduled routines?

> [!tip]- Answer
> One-shot automation uses Unix-style piping such as `tail -200 app.log | claude -p "Slack me if you see any anomalies"` and CI via GitHub Actions or GitLab CI/CD for commits, PRs, and triage. Recurring and long-running work uses background/parallel agents, the Agent SDK, cloud Routines triggerable via API or GitHub events, Desktop scheduled tasks, and in-session `/schedule` and `/loop` polling. See [[wiki/01-documentation-index|Documentation Index]].

### Q7. A solo developer splits time between terminal, phone, and Slack and wants PR review plus scheduled dependency audits: which options should they pick?

> [!tip]- Answer
> They should use Remote Control or `claude --cloud` with the mobile app to continue local sessions from the phone, Slack `@Claude` mentions to route bug reports into pull requests, and GitHub Actions or GitLab CI/CD for automatic PR review and triage. For the audits they should choose cloud Routines or Desktop scheduled tasks over `/loop`, since Routines persist on a schedule while `/loop` only polls within a live session. See [[wiki/01-documentation-index|Documentation Index]].
