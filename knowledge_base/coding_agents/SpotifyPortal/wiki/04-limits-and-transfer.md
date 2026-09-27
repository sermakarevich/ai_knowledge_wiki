> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Limits, Failure Modes, and Transferability

**In one sentence:** Delegation fails for editing and reasoning and adds delay, but the mode-based routing pattern transfers to any harness that can shell out and enforce hooks.

## Key points

- Editing cannot be delegated because worker summaries do not include reliable line numbers, so Claude must still do targeted reads with offset and limit before changing code.
- Reasoning cannot be delegated because the worker missed a subtle thread-safety bug that Claude found in seconds, so debugging, architectural decisions, and safety-critical code stay with the main model.
- Each delegation adds 10 to 30 seconds of network delay, Portal caps a single call at 30 seconds, so large generations must be split into smaller pieces.
- Small files are not worth delegating because the delay costs more than the saving, which is why the line threshold exists and only large reads are blocked.
- What transfers is the pattern: modes are reusable, shareable, and composable, the router that decides when to delegate is separate from the worker that decides how to respond, any tool that can shell out to the Command Line Interface (CLI) can use it, and you can swap the model, prompt, or Model Context Protocol (MCP) tools without changing the plugin.
- To try it, run `claude plugin marketplace add spotify/portal-ai-plugins`, `claude plugin install portal@portal`, and `claude plugin install shunt@portal`, then run `/portal:setup` to authenticate, use the public modes with no creation step, and fork a public mode if you want your copy to take precedence.

---

## Cannot delegate editing

Worker summaries describe the code but do not give line numbers you can trust. That makes them unsafe as a base for edits. If Claude tried to edit from a summary alone, it would change the wrong lines or break the file.

The setup keeps a safe path for this case. Hooks block only large full-file reads. Targeted reads with offset and limit still pass through, so Claude can read the exact section it needs to change.

## Cannot delegate reasoning

The worker is good at surface patterns and poor at deep reasoning. In the article test it described the code correctly but missed a subtle thread-safety bug. Once Claude received the right context, Claude spotted the bug in seconds.

Because of this limit, routing excludes three kinds of work: debugging, architectural decisions, and safety-critical code. Those stay with the strong main model.

## Latency and the 30-second cap

Each delegation is a network round trip from Claude Code to the Portal backend to the worker model and back. In practice this takes 10 to 30 seconds per call.

Portal also caps a single call at 30 seconds. A large generation that needs more time cannot finish in one call, so it must be split into smaller pieces.

## Why the threshold exists

For a large file, a 10 to 30 second wait is acceptable because reading the whole file with the main model would cost far more. For a small file, the same wait is wasteful because a direct read is fast and cheap.

The line threshold enforces this trade-off. Reads above the threshold are blocked and routed to the worker. Small targeted reads pass through. The default is 350 lines, and it can be changed with the SHUNT_MIN_LINES setting.

## What transfers to other harnesses

The durable idea is not the two demo modes but the mode-based routing pattern. Modes are reusable across projects, shareable as public modes, and composable into new helpers such as a doc writer, reviewer, or translator.

Routing and working are decoupled. The plugin decides when to delegate. The mode decides how to respond. That means you can swap the model, prompt, or MCP tools without changing the plugin, and any harness that can shell out to the CLI and enforce hooks can copy the pattern.

## Try-it-yourself setup

Install both plugins from the marketplace: `claude plugin marketplace add spotify/portal-ai-plugins`, then `claude plugin install portal@portal` for the Portal CLI, then `claude plugin install shunt@portal` for routing.

Then open a new Claude Code session and run `/portal:setup` to authenticate against your Portal instance. Ask a question spanning multiple files. The modes are public so no creation step is needed, and if you fork a public mode your copy takes precedence automatically.

**Covers:** article sections "What doesn't work", "Token savings are just the starting point", "Try it yourself".
