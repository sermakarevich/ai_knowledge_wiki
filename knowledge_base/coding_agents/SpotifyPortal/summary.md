# Portal by Spotify Cut My Claude Code Token Usage by 90%

**Article:** [Portal by Spotify cut my Claude Code token usage by 90%](https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90) — Spotify Engineering, 2026-09-03

## Human Readable TL;DR

Think of a top chef who spends most of the day chopping vegetables instead of cooking. This article gives the chopping work to a cheaper kitchen helper, so the chef only tastes and decides. The helper reads big piles of files and returns a short note, or writes plain routine drafts straight to disk. On one large code store test this cut what the top chef had to read by about 90% on average. It does not work when careful editing or deep thinking is needed, and each handoff adds waiting time.

## TL;DR

Portal by Spotify routes grunt work through declarative AI agents called AiKA modes, enforced by a Claude Code plugin called shunt. Bulk reading and routine writing go to a cheap worker running Gemini 2.5 Flash at temperature 0.2, while Claude keeps the reasoning. The worker reads large files sent as plain text and returns only a short summary, so most bulk text never enters Claude's context. On a Java monorepo across four scenarios this gave around 90% mean saving in Claude tokens for bulk reads; code-write saving was real but not given a number. Limits remain: no trusted line numbers for edits, missed reasoning like a thread-safety bug, 10–30 seconds delay per call, and a 30-second cap per call.

---

## Problem & Motivation

Coding helpers cost the most in tokens, not in seat licenses. Much of what the main model does is not hard thinking: it opens five files to answer one question, copies test patterns, or updates routine text, burning thousands of tokens with almost no reasoning. A frontier model — the most capable and most expensive — is overqualified for this simple work. Cost pressure makes this urgent: Gartner in June 2026 expects AI coding costs by 2028 to pass the average developer salary, a quarter of engineering leaders already spend $200–500 per developer per month on tokens, and some spend over $2,000. The goal is to keep the strong model for thinking and move reading and routine writing to a cheaper worker, reached through the Portal CLI or API using shared tools connected over MCP.

---

## Main Original Ideas

1. **AiKA modes as declarative workers** — An AiKA mode is a small declared agent where you write instructions, pick a model, set temperature, and attach MCP tools. Portal runs it on a short-lived runtime, like AWS Lambda but for agents, with no servers or keys to manage. Each mode is callable from the Portal CLI or API, public for the whole company or kept private.

2. **Bulk-reader mode for heavy reads** — Bulk-reader answers one question from many large files using Gemini 2.5 Flash at temperature 0.2. Its rules are strict: output structured bullets only, no greetings or prose, lead every bullet with the exact name, type, or line number, use nested bullets for details, and skip anything not asked. Only the short answer returns to Claude, so the large file text never enters Claude's context.

3. **Code-writer mode for routine output** — Code-writer makes tests, config scaffolding, type stubs, and other predictable output using Gemini 2.5 Flash at temperature 0.2. It takes a task description plus a required reference file, matches existing patterns and style exactly, and outputs only code. The output-only-code rule matters because without it the worker adds markdown fences and explanations that Claude must read and clean up.

4. **Enforced routing with the shunt plugin through hooks, scripts, and skills** — The first try put routing rules in CLAUDE.md, but those were advice only: Claude could ignore them, and every project needed its own copy. The shunt plugin fixes this with three layers that work with any Portal setup that has the AiKA plugin enabled. Hooks stop costly calls before they happen, scripts build the Portal CLI request and report token use, and skills tell Claude when and how to call the scripts, with mode names resolved case-insensitively in own, then team, then public order.

---

## Key Findings

- Mean saving for bulk reads was around 90% on a Java monorepo across four scenarios — Claude used about one tenth of the tokens it would have spent reading full files itself.
- The saving happens because large files go to the cheap Gemini 2.5 Flash worker wrapped in XML tags, and only a short summary enters Claude's context.
- The article gave no per-scenario table, so results for each of the four scenarios separately are not known.
- Code-write saving is real but unmeasured: without delegation Claude both reads reference files and produces new code as costly output tokens, while with delegation the code goes straight to disk and Claude never sees it.
- Enforcement beats advice: PreToolUse hooks guarantee the cheap path is used, while CLAUDE.md rules could be skipped.
- The check-file-size hook blocks Read calls over a set line limit (default 350 lines, changeable with SHUNT_MIN_LINES), while small targeted reads with offset and limit still pass through.
- The check-bash-read hook catches shell workarounds such as cat, head, tail, less, and more on large files, while piped filter commands such as grep pass through as targeted reads.
- Editing cannot be delegated because worker summaries do not include reliable line numbers, so Claude must still read exact sections before changing code.
- Reasoning cannot be delegated: the worker described code correctly but missed a subtle thread-safety bug that Claude found in seconds, so debugging, architectural decisions, and safety-critical code stay with the main model.
- Each delegation adds 10–30 seconds of network delay, Portal caps a single call at 30 seconds, small files are not worth delegating, and calls are one-shot and stateless so follow-ups must re-send files.
- These are author-run benchmarks on one single repo, so they show what is possible in that setup rather than a promise for every codebase.

---

## Suggestions & Future Directions

1. **Build more modes like doc-writer, reviewer, and translator** — Modes are reusable across projects, shareable as public or private, and composable into new helpers. The same pattern that made bulk-reader and code-writer can make a doc writer, a reviewer, or a translator in a few steps. Forking a public mode makes your copy take precedence automatically.

2. **Swap models, prompts, and tools without changing routing** — Routing and working are kept separate: the plugin decides when to delegate and the mode decides how to respond. You can change the model, the instructions, or the MCP tools without rewriting the plugin, which keeps the setup flexible as cheaper or stronger models appear.

3. **Adopt hook-enforced routing in other harnesses** — Any tool that can shell out to the CLI and enforce checks before tool calls can copy the pattern. Use automatic hooks instead of advisory prompt rules, keep one shared plugin instead of per-project copies, and let small targeted reads pass through. Scripts can handle request building, error handling, and token reporting the same way.

4. **Split large generations to stay under the 30-second cap** — Portal caps a single call at 30 seconds and each call already takes 10–30 seconds. Break large writes into smaller pieces that each finish in time, and keep the line threshold so only large reads pay the delay cost.

---

## Authors & Institutions

- Dimitri Mazmanov, Principal Product Manager, Spotify.
- Institution: Spotify, through Spotify Engineering.
- The work was published as a Spotify Engineering field report, based on author-run tests on one Java monorepo, not an outside lab study.
