# Source copy — Portal by Spotify cut my Claude Code token usage by 90%

- **Title:** Portal by Spotify cut my Claude Code token usage by 90%
- **Author:** Dimitri Mazmanov (Principal Product Manager)
- **Source:** Spotify Engineering
- **URL:** https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90
- **Published:** 2026-09-03
- **Retrieved:** 2026-09-12
- **Method:** webfetch markdown extraction; saved locally to survive link rot.

---

Most of what an AI coding agent does for me isn't thinking. It's I/O.

Reading five files to answer a question about one method. Generating a test file that follows the exact same pattern as the twenty test files next to it. Updating docs after a meeting. Thousands of tokens gone and almost zero reasoning. The seat license isn't what hurts, it's the tokens. And you're feeding all of it to a frontier model that's wildly overqualified. What if you could route the grunt work to something cheaper that handles it just as well, and save the expensive model for the problems that actually need it?

By 2028, AI coding costs are expected (Gartner, June 2026) to blow past the average developer's salary. A quarter of engineering leaders already burn $200–$500 per developer per month on tokens. Some are well past $2,000.

## Two modes, zero code

AiKA Modes in Portal by Spotify. A mode is a declarative agent that runs on an ephemeral runtime (think AWS Lambda, but for agents). You define the instructions, pick a model, set parameters like temperature, and attach MCP tools. Portal handles the rest. No infra to manage, no API keys, no long-running servers. Modes are callable from the Portal CLI or API. They can be public (shared with the whole company) or private.

Two modes created, both using Gemini 2.5 Flash as the worker model (the model field accepts any model configured in the Portal instance):

### Mode 1: bulk-reader

For when Claude would otherwise read multiple large files just to answer one question.

```
name: bulk-reader
description: Bulk file reader for code analysis - delegates I/O from Claude Code
instructions: You are a precise code analyst. Read the provided files and answer the question concisely. Output structured bullets only. No greetings, no prose, no preambles. Lead every bullet with the exact name, type, or line number. Use nested bullets for details. Skip anything the caller did not ask for.
visibility: public
model: gemini-2.5-flash
resourceLimits:
  temperature: 0.2
tags:
  - coding
  - delegation
```

### Mode 2: code-writer

For tests, config scaffolding, type stubs or anything where the output is predictable from existing patterns.

```
name: code-writer
description: Boilerplate code generator - delegates output-heavy work from Claude Code
instructions: You generate code files based on a spec and reference files. Match the existing patterns, conventions, naming, and style exactly. Output only the code — no explanations, no markdown fences unless asked. If the spec is ambiguous, make reasonable choices that match the reference code's patterns.
visibility: public
model: gemini-2.5-flash
resourceLimits:
  temperature: 0.2
tags:
  - coding
  - delegation
```

The "output only the code" instruction matters: without it, the model wraps everything in markdown fences and explanatory prose that Claude then has to parse through.

## Routing

First version: a block of routing rules in CLAUDE.md. Sort of worked but advisory, not enforced — Claude could ignore them, and every project needed its own copy.

Current version: a Claude Code plugin called shunt (github.com/sorantis/portal-ai-plugins tree, shunt plugin). Delegation goes through the Portal CLI actions registry so the plugin works against any Portal instance with AiKA plugin enabled.

### Layer 1: Hooks

Claude Code hooks fire before every tool call. Shunt registers two PreToolUse hooks:

- check-file-size fires on every Read call. If the file exceeds a configurable line threshold (default: 350), the hook blocks the read and tells Claude to use the /bulk-reader skill instead. Targeted reads pass through.
- check-bash-read catches cat, head, tail, less, and more on large files. Piped commands (cat file | grep) pass through since those are targeted reads.

Threshold configurable via SHUNT_MIN_LINES env var (shell profile or .claude/settings.json). Example: `{ "env": { "SHUNT_MIN_LINES": "500" } }`.

### Layer 2: Scripts

Two bash scripts wrap the Portal CLI calls. Claude calls a script with named arguments. Scripts handle building the request, invoking the actions, unwrapping errors, and reporting token usage to stderr.

Modes addressed by name, resolved case-insensitively by Portal: preferring your own mode, then your team's, then public ones. Forking the public bulk-reader means yours takes precedence automatically.

- bulk-read wraps each file in XML tags and sends them to bulk-reader with the question. Example: `bulk-read --question "What does this service do?" --paths src/Service.java src/Handler.java`. Follow-ups re-send the files; every delegation is one shot, ephemeral (nothing stored server-side), and re-sending is free where it matters because the corpus goes to the worker model and never enters Claude's context.
- code-write sends a spec + required reference file to code-writer, strips markdown fences, can write directly to disk. Claude never sees the generated code. Reference required: without it the worker generates context-free code that fits nothing.

### Layer 3: Skills

Two skill files tell Claude when and how to call the scripts. When the hook blocks a read, the block message points Claude to the /bulk-reader skill with exact invocation syntax. Graceful degradation: even if Claude doesn't read the skill description, the hook still blocks the expensive read.

## The benchmarks

Tested against a Java monorepo across four scenarios, measuring tokens Claude would consume reading files directly vs. consuming the bulk-reader's summary or writing code via the code-writer. Mean bulk-read savings around 90%.

The code-write scenario is harder to measure because without shunt, Claude both reads the reference files and generates the output as expensive output tokens; with shunt the code goes straight to disk and Claude never sees it.

## What doesn't work

- You can't delegate editing. Worker summaries don't include reliable line numbers. If Claude needs to make edits, it still reads the specific section directly. Hooks allow targeted reads (offset/limit) for this.
- You can't delegate reasoning. The worker found surface patterns but missed a subtle thread-safety bug; Claude spotted it in seconds once given the right context. Routing excludes debugging, architectural decisions, safety-critical code.
- Latency adds up. Each delegation is a network round-trip (Claude Code → Portal backend → worker model → back), typically 10–30 seconds; Portal caps a single invocation at 30 seconds, so large generations must be split. Acceptable for large reads, counterproductive for small ones — hence the line threshold.

## Token savings are just the starting point

Modes are the load-bearing piece:

- Reusable: same modes work across every project and every tool that can shell out to the Portal CLI.
- Shareable: both modes public in AiKA; anyone can use them without creating their own.
- Composable: doc-writer, reviewer, translator modes each a few clicks away.
- Decoupled: the plugin decides when to delegate; the mode decides how to respond. Swap the model, prompt, or MCP tools without changing the plugin.

Model routing goes from systems engineering problem to configuration problem.

## Try it yourself

1. Install both plugins from spotify/portal-ai-plugins marketplace: `claude plugin marketplace add spotify/portal-ai-plugins`, `claude plugin install portal@portal`, `claude plugin install shunt@portal`. The portal plugin provides the Portal CLI.
2. In a new Claude Code session, run /portal:setup to authenticate against your Portal instance.
3. Ask a question spanning multiple files. Modes are public; fork to customize and yours takes precedence.
