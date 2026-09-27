> [[index|Wiki]] | [[summary|Summary]]
# Overview - Claude Code Docs — Digest

## 1. [[wiki/01-documentation-index|Documentation Index]]
**In one sentence:** Claude Code is an AI coding assistant that works across terminal, IDE, desktop, and web surfaces to build features, fix bugs, and automate development tasks, with the full documentation index discoverable at /docs/llms.txt.
## Key points
- Claude Code "understands your entire codebase and can work across multiple files and tools to get things done," handling features, bug fixes, tests, lint fixes, merge conflicts, dependency updates, and release notes.
- It runs on five main surfaces — Terminal CLI, VS Code, Desktop app, Web, and JetBrains — all sharing the same underlying engine, CLAUDE.md files, settings, and MCP servers.
- Native install is recommended via `curl -fsSL https://claude.ai/install.sh | bash` (macOS/Linux/WSL), `irm https://claude.ai/install.ps1 | iex` (PowerShell), or CMD installer; Homebrew (`brew install --cask claude-code`, stable channel ~1 week behind) and WinGet (`winget install Anthropic.ClaudeCode`) do not auto-update.
- Customization rests on CLAUDE.md project instructions (plus AGENTS.md compatibility and auto memory), shareable skills such as `/review-pr` or `/deploy-staging`, and hooks that run shell commands before/after actions.
- MCP (Model Context Protocol) connects Claude Code to external sources such as Google Drive, Jira, Slack, or custom tooling.
- Automation paths include Unix-style piping (`tail -200 app.log | claude -p ...`), CI via GitHub Actions or GitLab CI/CD, background/parallel agents, the Agent SDK, scheduled Routines, `/schedule`, `/loop`, and `claude --teleport` / `/desktop` handoffs.
- Work moves between surfaces via Remote Control, message dispatch from phone, Slack `@Claude` mentions returning PRs, Chrome debugging, and Channels for Telegram/Discord/iMessage/webhooks.

## The argument in five moves
1. Claude Code is positioned as a codebase-aware agent that executes multi-file development work — features, fixes, tests, and maintenance — rather than a single-file autocomplete.
2. That capability is delivered uniformly across five surfaces (Terminal, VS Code, Desktop, Web, JetBrains) sharing one engine, memory, settings, and MCP layer, so the user picks the surface by context.
3. Entry is via native install with background auto-updates, with package managers as non-auto-updating alternatives, plus per-surface setup from CLI login to IDE extension to subscription-gated Desktop/Web.
4. Power comes from layering project instructions (CLAUDE.md/skills/hooks) and external context (MCP) onto the shared engine, turning generic coding into repeatable, project-specific workflows.
5. Those workflows scale into automation — piping, CI, parallel/background agents, SDK, and scheduled Routines — and stay continuous across devices via Remote Control, teleport/desktop handoffs, Slack, Chrome, and Channels.
