PDF: https://docs.anthropic.com/en/docs/claude-code (no source.pdf in run; use Source URL)
# Overview - Claude Code Docs
Source: https://docs.anthropic.com/en/docs/claude-code
Kind: article
Fetched: 2026-09-24T04:56:33.483936+00:00
Tool: urllib
Topic: coding_agents

Overview - Claude Code Docs

## Documentation Index

Fetch the complete documentation index at:/docs/llms.txt

Use this file to discover all available pages before exploring further.

Skip to main content

Claude Code is an AI-powered coding assistant that helps you build features, fix bugs, and automate development tasks. It understands your entire codebase and can work across multiple files and tools to get things done.

##

​

Get started

Claude Code runs on several surfaces: the terminal, IDE extensions, a desktop app, and the web. Choose one from the tabs below to get started. Most surfaces require a Claude subscription or Anthropic Console account. The Terminal CLI, VS Code, and JetBrains also support third-party providers.

Terminal

VS Code

Desktop app

Web

JetBrains

The full-featured CLI for working with Claude Code directly in your terminal. Edit files, run commands, and manage your entire project from the command line.To install Claude Code, use one of the following methods:

Native Install (Recommended)

Homebrew

WinGet

macOS, Linux, WSL:

curl -fsSL https://claude.ai/install.sh | bash

Windows PowerShell:

irm https://claude.ai/install.ps1 | iex

Windows CMD:

curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd

If you see The token '&&' is not a valid statement separator, you’re in PowerShell, not CMD. If you see 'irm' is not recognized as an internal or external command, you’re in CMD, not PowerShell. Your prompt shows PS C:\ when you’re in PowerShell and C:\ without the PS when you’re in CMD.If the install command fails with syntax error near unexpected token '<', a 403, or another curl error, see Troubleshoot installation to match the error to a fix and for alternative install methods.Git for Windows is recommended on native Windows so Claude Code can use the Bash tool. If Git for Windows is not installed, Claude Code uses PowerShell as the shell tool instead. WSL setups do not need Git for Windows.

Native installations automatically update in the background to keep you on the latest version.

brew install --cask claude-code

Homebrew offers two casks. claude-code tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. claude-code@latest tracks the latest channel and receives new versions as soon as they ship.

Homebrew installations do not auto-update. Run brew upgrade claude-code or brew upgrade claude-code@latest, depending on which cask you installed, to get the latest features and security fixes.

winget install Anthropic.ClaudeCode

WinGet installations do not auto-update. Run winget upgrade Anthropic.ClaudeCode periodically to get the latest features and security fixes.

You can also install with apt, dnf, or apk on Debian, Fedora, RHEL, and Alpine.Then start Claude Code in any project. Replace your-project with the path to a project directory on your machine:

cd your-projectclaude

You’ll be prompted to log in on first use. If you’ve set the ANTHROPIC_API_KEY environment variable, Claude Code skips the login prompt and asks you to approve the key instead. That’s it! Continue with the Quickstart →

See advanced setup for installation options, manual updates, or uninstallation instructions. Visit installation troubleshooting if you hit issues.

The VS Code extension provides inline diffs, @-mentions, plan review, and conversation history directly in your editor.

Install for VS Code

Install for Cursor

Or search for “Claude Code” in the Extensions view (Cmd+Shift+X on Mac, Ctrl+Shift+X on Windows/Linux). After installing, open the Command Palette (Cmd+Shift+P / Ctrl+Shift+P), type “Claude Code”, and select Open in New Tab.Get started with VS Code →

A standalone app for running Claude Code outside your IDE or terminal. Review diffs visually, run multiple sessions side by side, schedule recurring tasks, and start cloud sessions.Download and install:

macOS (Intel and Apple Silicon)

Windows (x64)

Windows ARM64

On Ubuntu or Debian, where the app is in beta, install it with apt by following the Linux install instructions

After installing, launch Claude, sign in, and click the Code tab to start coding. The app includes Claude Code, so you don’t need to install the CLI separately. A paid subscription is required.Learn more about the desktop app →

Run Claude Code in your browser with no local setup. Kick off long-running tasks and check back when they’re done, work on repos you don’t have locally, or run multiple tasks in parallel. For a longer body of work, create a project and let Claude coordinate the parallel sessions for you. Available on desktop browsers and the Claude app for iOS and Android.Start coding at claude.ai/code.Get started →

A plugin for IntelliJ IDEA, PyCharm, WebStorm, and other JetBrains IDEs with interactive diff viewing and selection context sharing.Install the Claude Code plugin from the JetBrains Marketplace and restart your IDE. The plugin requires the Claude Code CLI, installed separately; see the JetBrains setup steps.Get started with JetBrains →

##

​

What you can do

Here are some of the ways you can use Claude Code:

Automate the work you keep putting off

Claude Code handles the tedious tasks that eat up your day: writing tests for untested code, fixing lint errors across a project, resolving merge conflicts, updating dependencies, and writing release notes.

claude "write tests for the auth module, run them, and fix any failures"

Build features and fix bugs

Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works.For bugs, paste an error message or describe the symptom. Claude Code traces the issue through your codebase, identifies the root cause, and implements a fix. See common workflows for more examples.

Create commits and pull requests

Claude Code works directly with git. It stages changes, writes commit messages, creates branches, and opens pull requests.

claude "commit my changes with a descriptive message"

In CI, you can automate code review and issue triage with GitHub Actions or GitLab CI/CD.

Connect your tools with MCP

The Model Context Protocol (MCP) is an open standard for connecting AI tools to external data sources. With MCP, Claude Code can read your design docs in Google Drive, update tickets in Jira, pull data from Slack, or use your own custom tooling. The MCP quickstart connects your first server end to end.

Customize with instructions, skills, and hooks

CLAUDE.md is a markdown file you add to your project root that Claude Code reads at the start of every session. Use it to set coding standards, architecture decisions, preferred libraries, and review checklists. If your repository already has an AGENTS.md for other coding agents, Claude Code can read that on its own or alongside CLAUDE.md. Claude also builds auto memory as it works, saving learnings across sessions without you writing anything.Create skills to package repeatable workflows your team can share, like /review-pr or /deploy-staging.Hooks let you run shell commands before or after Claude Code actions, like auto-formatting after every file edit or running lint before a commit.

Run agents in parallel and build custom agents

Spawn multiple Claude Code agents that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results.To run several full sessions in parallel and watch them from one screen, use background agents. For fully custom workflows, the Agent SDK lets you build your own agents powered by Claude Code’s tools and capabilities, with full control over orchestration, tool access, and permissions.

Pipe, script, and automate with the CLI

Claude Code is composable and follows the Unix philosophy. Pipe logs into it, run it in CI, or chain it with other tools:

# Analyze recent log outputtail -200 app.log | claude -p "Slack me if you see any anomalies"# Automate translations in CIclaude -p "translate new strings into French and raise a PR for review"# Bulk operations across filesgit diff main --name-only | claude -p "review these changed files for security issues"

See the CLI reference for the full set of commands and flags.

Schedule recurring tasks

Run Claude on a schedule to automate work that repeats: morning PR reviews, overnight CI failure analysis, weekly dependency audits, or syncing docs after PRs merge.

Routines run in the cloud, so they keep running even when your computer is off. They can also trigger on API calls or GitHub events. Create them from the web, the Desktop app, or by running /schedule in the CLI.

Desktop scheduled tasks run on your machine, with direct access to your local files and tools

/loop repeats a prompt within a CLI session for quick polling

Work from anywhere

Sessions aren’t tied to a single surface. Move work between them as your context changes:

Step away from your desk and keep working from your phone or any browser with Remote Control

Message Dispatch a task from your phone and open the Desktop session it creates

Start a long-running task on the web or the Claude mobile app, then pull it into your terminal with claude --teleport. Teleport requires a claude.ai subscription.

Run /desktop to continue your current terminal session in the Desktop app, where you can review diffs visually. The /desktop handoff requires a claude.ai subscription. Available on macOS and x64 Windows.

Route tasks from team chat: mention @Claude in Slack with a bug report and get a pull request back

##

​

Use Claude Code everywhere

Each surface connects to the same underlying Claude Code engine, so your repo’s CLAUDE.md files, settings, and MCP servers work across all of them.Beyond the Terminal, VS Code, JetBrains, Desktop, and Web surfaces above, Claude Code integrates with CI/CD, chat, and browser workflows:

What I want to doBest option

Continue a local session from my phone or another deviceRemote Control

Push events from Telegram, Discord, iMessage, or my own webhooks into a sessionChannels

Start a task locally, continue on mobileclaude --cloud, then the Claude mobile app

Run Claude on a recurring scheduleRoutines or Desktop scheduled tasks

Automate PR reviews and issue triageGitHub Actions or GitLab CI/CD

Get automatic code review on every PRGitHub Code Review

Route bug reports from Slack to pull requestsSlack

Debug live web applicationsChrome

Build custom agents for your own workflowsAgent SDK

##

​

Next steps

Once you’ve installed Claude Code, these guides help you go deeper.

Quickstart: walk through your first real task, from exploring a codebase to committing a fix

Store instructions and memories: give Claude persistent instructions with CLAUDE.md files and auto memory

Common workflows and best practices: patterns for getting the most out of Claude Code

Claude Academy: free self-paced courses, including Claude Code 101 and Claude Code in Action

A harness for every task: how the Claude Code team uses dynamic workflows to orchestrate many subagents at once

Settings: customize Claude Code for your workflow

Troubleshooting: solutions for common issues

code.claude.com: demos, pricing, and product details

Was this page helpful?

YesNo

Assistant

Responses are generated using AI and may contain mistakes.
