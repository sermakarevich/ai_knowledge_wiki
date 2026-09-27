# Overview - Claude Code Docs

**Article:** [Overview - Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code) — Anthropic Docs

## Human Readable TL;DR

Claude Code is like a handy teammate who lives inside your terminal, editor, and phone and can actually do the chores on your to-do list instead of just talking about them. Tell it in plain words to add a feature, chase down a bug, or clean up tests and lint, and it will read across many files, make the edits, and check its own work. It remembers your house rules in a CLAUDE.md file, plugs into outside tools like Drive or Slack, and can keep working on a schedule or while you are away from your desk.

## TL;DR

Claude Code is Anthropic's AI coding assistant that understands whole codebases and acts across multiple files and tools to build features, fix bugs, write tests, manage commits and PRs, and automate deferred and recurring development work. It runs on five surfaces sharing one engine — Terminal CLI, VS Code, Desktop app, Web, and JetBrains — with native install recommended and auto-updates, plus third-party provider support on CLI and some IDEs. Customization and extension rest on CLAUDE.md project instructions with AGENTS.md compatibility and auto memory, shareable skills, hooks, and MCP connections to external data sources. Automation spans Unix-style piping, CI via GitHub Actions or GitLab, parallel and background agents, the Agent SDK, Routines and scheduled tasks, and cross-surface handoffs such as Remote Control, message dispatch, Slack mentions, Channels, Chrome debugging, and teleport between terminal, desktop, web, and mobile.

---

## Problem & Motivation

Development teams carry a long tail of valuable but deferred work — untested modules, lint errors spread across a project, merge conflicts, dependency updates, and release notes — alongside the everyday pressure to ship features and fix bugs quickly. Traditional assistants that only suggest single-file snippets leave the developer to do the planning, cross-file editing, verification, and process wiring by hand. The overview is motivated by this gap: it presents a tool that can take a plain-language request, plan an approach, work across the codebase and surrounding toolchain, and verify the result, while staying reachable from wherever the developer happens to be and running unattended when work is recurring or long-lived.

## Main Original Ideas

1. **One engine, many surfaces.** The documentation frames Terminal, VS Code, Desktop, Web, and JetBrains not as separate products but as views onto the same underlying agent, sharing CLAUDE.md instructions, settings, and MCP servers, so work can start in one place and continue in another via Remote Control, teleport, and message dispatch.

2. **Project memory as configuration.** CLAUDE.md files stored in the project root and loaded at session start, together with AGENTS.md compatibility and automatic memory, turn coding standards, architecture notes, libraries, and checklists into persistent, shareable behavior rather than repeated prompting.

3. **Composable customization with skills, hooks, and MCP.** Shareable skills such as review or deploy routines, shell-command hooks that run before or after actions, and the open-standard Model Context Protocol for connecting to sources like Google Drive, Jira, Slack, or custom tooling make the assistant extensible without forking it.

4. **Unix-native and CI-native automation.** Piping through the CLI, background and parallel agents, the Agent SDK, GitHub Actions and GitLab CI/CD integration, scheduled Routines, and in-session loops treat AI coding as scriptable infrastructure for PR review, issue triage, audits, and doc syncs rather than only an interactive chat.

## Key Findings

The overview establishes that Claude Code handles the full loop from description to verified change across multiple files, covering features, bug triage and root-cause fixes, test authoring and repair, commits, branches, and PR creation. It confirms native installation as the recommended path with background auto-updates, documents each surface's strengths from CLI full-featured use through IDE diffs and mentions to desktop multi-session and scheduled-task support and web-based parallel long-running sessions, and maps common intents to best options such as Remote Control for continuing sessions from a phone, Channels for Telegram, Discord, iMessage, and webhook inputs, and dedicated paths for Slack, Chrome, and the Agent SDK. Recurring work is treated as a first-class use case, with cloud Routines triggerable by API or GitHub events alongside desktop scheduled tasks and loop-based polling. Discovery of the wider documentation set is centralized through the llms.txt index, with pointers onward to quickstart, memory, workflows, settings, troubleshooting, and learning resources.

## Suggestions & Future Directions

The page points readers toward concrete next steps rather than open research questions: install and run a first task through to a committed fix, set up CLAUDE.md and memory, adopt the documented common workflows and best practices, and work through Claude Academy and the multi-subagent harness material. It further suggests deepening use of settings and troubleshooting references and following product demos, pricing, and updates on the companion site. Implicit in the surface mapping is a direction of ever more continuous and ambient operation — recurring reviews, overnight analyses, event-triggered routines, and work dispatched from anywhere — with cross-surface continuity as the mechanism for getting there.

## Authors & Institutions

The material is product documentation published by Anthropic for Claude Code, with no individual authors named in the wiki source. Institutional context is the Claude and Claude Code product and documentation ecosystem, including the API and Console accounts, subscription surfaces, and related integration points such as GitHub, GitLab, Slack, Chrome, and the Agent SDK.
