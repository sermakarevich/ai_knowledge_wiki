> [[index|Wiki]] | [[summary|Summary]]

# Portal by Spotify Cut My Claude Code Token Usage by 90% — Digest

The whole source at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-portal-and-modes|Portal, AiKA Modes, and the Two Worker Modes]]

**In one sentence:** Portal's AiKA modes let a cheap worker model absorb input/output (I/O)-heavy grunt work so the frontier model only does reasoning.

- Portal by Spotify is a platform for running small task-specific agents, so the main coding agent can hand off grunt work instead of spending expensive tokens on it.
- An AiKA mode is a declarative artificial intelligence (AI) agent that runs on an ephemeral runtime like AWS Lambda for agents: you define instructions, pick a model, set temperature, and attach Model Context Protocol (MCP) tools, while Portal handles servers, keys, and infrastructure, and each mode is callable from the Portal command-line interface (CLI) or application programming interface (API) as public (shared company-wide) or private.
- The article creates two worker modes, bulk-reader and code-writer, both using gemini-2.5-flash with temperature 0.2, where bulk-reader answers a question from many large files and code-writer generates tests, configs, stubs, and other predictable output.
- The exact bulk-reader instructions are: You are a precise code analyst. Read the provided files and answer the question concisely. Output structured bullets only. No greetings, no prose, no preambles. Lead every bullet with the exact name, type, or line number. Use nested bullets for details. Skip anything the caller did not ask for.
- The exact code-writer instructions are: You generate code files based on a spec and reference files. Match the existing patterns, conventions, naming, and style exactly. Output only the code — no explanations, no markdown fences unless asked. If the spec is ambiguous, make reasonable choices that match the reference code's patterns.
- The rule Output only the code matters because without it the worker wraps results in markdown fences and explanatory prose that the main model must then read and parse, which wastes tokens and adds cleanup work.
- Cost pressure is the motive: Gartner (June 2026) expects AI coding costs by 2028 to pass the average developer salary, a quarter of engineering leaders already spend $200-500 per developer per month on tokens, and some spend over $2,000.

## 2. [[wiki/02-shunt-routing|Enforced Routing: the Shunt Plugin]]

**In one sentence:** The shunt Claude Code plugin enforces delegation through hooks, scripts, and skills so routing is automatic, not advisory.

- The first try put routing rules in CLAUDE.md, but those rules were advisory only, Claude could ignore them, and every project needed its own copy.
- The current fix is a Claude Code plugin called shunt, which sends work through the Portal CLI (command-line interface) actions registry so it works with any Portal instance that has the AiKA plugin enabled.
- The check-file-size hook watches every Read call and blocks files over a set line limit, by default 350 lines, while small targeted reads pass through.
- The check-bash-read hook catches shell workarounds such as cat, head, tail, less, and more on large files, while piped commands such as filtering with grep pass through as targeted reads.
- The line limit can be changed with SHUNT_MIN_LINES, for example `{ "env": { "SHUNT_MIN_LINES": "500" } }`.
- The bulk-read script wraps each file in XML (eXtensible Markup Language) tags plus a question as a one-shot short-lived call with nothing stored, so follow-ups re-send files for free because the full text goes only to the cheap worker model and never enters Claude context; the code-write script needs a spec plus a required reference file, strips markdown fences, writes straight to disk so Claude never sees the output, and modes resolve own > team > public.
- When a hook blocks a read, the block message points Claude to the /bulk-reader skill with exact call syntax, so even if Claude never read the skill text the costly read stays blocked.

## 3. [[wiki/03-benchmarks-savings|Benchmarks and the 90% Saving]]

**In one sentence:** On a Java monorepo across four scenarios, delegating bulk reads to the worker mode cut the tokens Claude consumes by about 90% on average.

- The test setup was a Java monorepo with four scenarios that compared tokens Claude would use when reading files directly against tokens Claude used when receiving the bulk-reader summary or using the code-writer path.
- Mean saving for bulk reads was around 90%, meaning Claude consumed only about one tenth of the tokens it would have used by reading the full files itself.
- The code-write case was harder to measure because without delegation Claude both reads the reference files and produces the new code as costly output tokens.
- With delegation for code-write, the new code goes straight to disk and Claude never sees it, so both the reference reads and the output tokens are avoided.
- The saving happens because the large set of files goes to the cheap worker model, and only a short summary comes back into Claude's context.
- The article did not publish a per-scenario table, so individual results for each of the four scenarios are not known.
- These are author-run benchmarks on one single repo, so they show what is possible in that setup rather than a promise for every codebase.

## 4. [[wiki/04-limits-and-transfer|Limits, Failure Modes, and Transferability]]

**In one sentence:** Delegation fails for editing and reasoning and adds delay, but the mode-based routing pattern transfers to any harness that can shell out and enforce hooks.

- Editing cannot be delegated because worker summaries do not include reliable line numbers, so Claude must still do targeted reads with offset and limit before changing code.
- Reasoning cannot be delegated because the worker missed a subtle thread-safety bug that Claude found in seconds, so debugging, architectural decisions, and safety-critical code stay with the main model.
- Each delegation adds 10 to 30 seconds of network delay, Portal caps a single call at 30 seconds, so large generations must be split into smaller pieces.
- Small files are not worth delegating because the delay costs more than the saving, which is why the line threshold exists and only large reads are blocked.
- What transfers is the pattern: modes are reusable, shareable, and composable, the router that decides when to delegate is separate from the worker that decides how to respond, any tool that can shell out to the Command Line Interface (CLI) can use it, and you can swap the model, prompt, or Model Context Protocol (MCP) tools without changing the plugin.
- To try it, run `claude plugin marketplace add spotify/portal-ai-plugins`, `claude plugin install portal@portal`, and `claude plugin install shunt@portal`, then run `/portal:setup` to authenticate, use the public modes with no creation step, and fork a public mode if you want your copy to take precedence.

## 5. [[wiki/targeted|Targeted Analysis: the 90%, What Generalizes, What Got Worse]]

**In one sentence:** The roughly 90% saving comes from keeping bulk file contents out of Claude's context by sending them to a cheaper worker model that returns only a short summary, and while this routing pattern generalizes to other setups, editing, reasoning, and latency do not improve.

- The measured saving (about 90% on average) comes from bulk reading: large files go to the Gemini 2.5 Flash worker, and only a short structured summary enters Claude's context.
- Code writing saves tokens too by keeping reference reads and generated code out of Claude's context, with code written straight to disk, but this part was not measured with a number.
- Enforcement matters: automatic hooks (triggered checks before a tool call) make the saving happen, while advisory prompt rules in CLAUDE.md could be ignored.
- The pattern that transfers elsewhere is simple: send heavy Input/Output (I/O, reading and writing lots of text) grunt work to a cheaper model and keep the frontier (most capable, most expensive) model for reasoning.
- Small files are left out on purpose with a line-count threshold, because delegation adds delay and is not worth it for small reads.
- What got worse or did not work: editing with bad line numbers, reasoning misses such as a thread-safety bug, extra latency of 10–30 seconds per call, and stateless (no memory between calls) one-shot calls that must re-send files on follow-up.

## The argument in five moves

1. Token costs for AI coding are exploding because frontier models burn tokens on I/O-heavy grunt work.
2. Two cheap worker modes absorb that grunt work while the frontier model keeps only reasoning.
3. The shunt plugin enforces the routing automatically via hooks, scripts, and skills.
4. On a Java monorepo this measured about 90% fewer Claude tokens on bulk reads.
5. Editing, reasoning, and latency set the limits, leaving a reusable route-cheap-work-elsewhere pattern.
