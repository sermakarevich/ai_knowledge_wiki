> [[index|Wiki]] | [[summary|Summary]]

# Best practices for Claude Code - Claude Code Docs — Digest

## 1. [[wiki/01-documentation-index|Documentation Index]]

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

## 2. [[wiki/02-claude-md-code-style-and-workflow|CLAUDE.md Code Style and Workflow]]

**In one sentence:** Put broadly-applicable code-style rules (ES modules with destructured imports) and workflow rules (typecheck after a series of changes, run single tests for performance) in a concise CLAUDE.md, cutting anything that fails the "would removing this cause mistakes?" test.

## Key points

- Use ES modules (`import`/`export`) syntax, not CommonJS (`require`), as a CLAUDE.md code-style rule.
- Destructure imports when possible, e.g. `import { foo } from 'bar'`.
- Typecheck when done making a series of code changes.
- Prefer running single tests rather than the whole test suite, for performance.
- CLAUDE.md is loaded every session, so include only broadly-applicable rules; put sometimes-relevant domain knowledge or workflows in skills that Claude loads on demand.
- Keep CLAUDE.md concise with the cut test: "Would removing this cause Claude to make mistakes?" — if not, cut it, because bloated files cause Claude to ignore actual instructions.
- Run `/context` to confirm Claude loaded the file; check CLAUDE.md into git so the team can contribute and value compounds; import additional files with `@path/to/import` syntax.

## 3. [[wiki/03-non-interactive-mode-output-formats|Non-interactive mode output formats]]

**In one sentence:** Use `claude -p` for non-interactive one-off queries, defaulting to plain text, using `--output-format json` for a single JSON object with a `result` field for scripts, and `--output-format stream-json --verbose` for line-delimited JSON starting with an `init` event for real-time processing.

## Key points

- Run one-off non-interactive queries with `claude -p` plus a quoted prompt, e.g. `claude -p "Explain what this project does"`.
- The default (first) command prints plain text with no output-format flag.
- Use structured output for scripts via `claude -p "List all API endpoints" --output-format json`.
- The `json` format returns a single JSON object with a `result` field.
- Use streaming for real-time processing via `claude -p "Analyze this log file" --output-format stream-json --verbose`.
- The `stream-json` format prints one JSON object per line, starting with an `init` event.

## The argument in five moves

1. Claude Code is agentic but bounded by context, so every best practice is context management: discover docs first, then work in ways that conserve the window.
2. Make Claude self-verifying by giving it a runnable check — tests, build, linter, diff script, or screenshot comparison — so iteration happens in-conversation instead of through you.
3. Separate research and planning from implementation via Explore → Plan → Implement → Commit, using plan mode for read-only understanding before any code changes.
4. Feed Claude precise, rich input — scoped prompts, source pointers, existing patterns, symptom plus done-state, `@`-referenced files, images, URLs, and piped data — to cut corrections.
5. Persist the reusable part of that context in a concise, checked-in CLAUDE.md (broadly-applicable commands, style, and workflow rules only; on-demand knowledge goes in skills), pruning anything that fails the would-removing-this-cause-mistakes test.
6. Extend the same workflow beyond interactive sessions with `claude -p` one-off queries, choosing plain text by default, single-`result` JSON for scripts, and line-delimited `stream-json` starting with `init` for real-time processing.
