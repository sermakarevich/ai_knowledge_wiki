[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# The Wrong Question
**In one sentence:** The "which model is best at coding" debate is the wrong question because changing only the edit tool in the harness improved 16 models by ~15 points on average with zero training compute.
## Key points
- Only the edit tool changed — "In fact only the edit tool changed. That's it" — yielding +15 pts avg over patch across 16 models with $0 training compute.
- Weakest models gained the most: Grok Code Fast 1 went from 6.7% to 68.3%, "a tenfold improvement," because catastrophic patch failures had hidden its actual coding ability.
- Hashline beats patch in 14/16 models, and the v2 revision improves further in 12/16, with the largest v2 gain GPT-5.1 Codex Mini, 60.0% → 77.5%.
- Best-case output tokens fell 61% (Grok 4 Fast), because it "stopped burning tokens on retry loops."
- Patch is the worst format for nearly every model: Grok 4's patch failure rate was 50.7% and GLM-4.7's was 46.2% — "These aren't bad models — they just don't speak the language."
- The harness, not the model, is where most failures happen in practice: "everything between 'the model knows what to change' and 'the issue is resolved.'"
- A +8% success-rate gain for Gemini from the harness alone is "bigger than most model upgrades deliver," costing only "~$300 spent benchmarking."
---
## The Wrong Question
**Covers:** article opening framing (model-vs-harness)

The current conversation "is almost entirely about which model is best at coding, GPT-5.3 or Opus. Gemini vs whatever dropped this week." The chunk calls this framing "increasingly misleading because it treats the model as the only variable that matters, when in reality one of the bottlenecks is something much more mundane: the harness."

The harness is where you capture the user's first impression ("is it uncontrollably scrolling, or smooth as butter?"), the source of every input token, and "the interface between their output and every change made to your workspace."

Example given: "Opus may be a great model, but Claude Code to this day leaks raw JSONL from sub-agent outputs, wasting hundreds of thousands of tokens. In an open harness, we get to just fix that: subagents output structured data now."

Key claim: "Tool schemas, error messages, state management, everything between 'the model knows what to change' and 'the issue is resolved.' This is where most failures happen in practice."

"Being model agnostic, it is a great testing ground, as the model is but a parameter. The real variable is the harness, which you have unimaginable control over."

## Edit Tool!
**Covers:** state of the art — apply_patch, str_replace, Cursor merger model, prior benchmarks

Codex uses apply_patch: "It takes a string as input, which is essentially an OpenAI-flavored diff, and instead of relying on a structured schema, the harness just expects this blob to follow a strict set of rules." The chunk speculates "the token selection process is almost certainly biased to fit this structure at the LLM gateway for the Codex variants of GPT, similar to how other constraints like JSON schemas or required tool calls work." Consequence: "give this to any other model, completely unaware of it? Patch failures go through the roof. Grok 4's patch failure rate in our benchmark was 50.7%, GLM-4.7's was 46.2%. These aren't bad models — they just don't speak the language."

Claude Code (and most others) use str_replace: "find the exact old text, swap in the new text. Very simple to think about. But the model must reproduce every character perfectly, including whitespace and indentation. Multiple matches? Rejected." The '"String to replace not found in file" error is so common it has its own GitHub issues megathread (+27 other issues).' Gemini does "essentially the same thing plus some fuzzy whitespace matching."

Cursor "trained a separate neural network: a fine-tuned 70B model whose entire job is to take a draft edit and merge it into the file correctly," and even then their blog notes that "fully rewriting the full file outperforms aider-like diffs for files under 400 lines."

Prior benchmarks cited:

| Benchmark | Result quoted in chunk |
|---|---|
| Aider | Format choice alone swung GPT-4 Turbo from 26% to 59%, but GPT-3.5 scored only 19% with the same format "because it couldn't reliably produce valid diffs" |
| Diff-XYZ (JetBrains) | "No single edit format dominates across models and use cases" |
| EDIT-Bench | "Only one model achieves over 60% pass@1 on realistic editing tasks" |

Conclusion: "The format matters as much as the model" and "none of these tools give the model a stable, verifiable identifier for the lines it wants to change without wasting tremendous amounts of context and depending on perfect recall. They all rely on the model reproducing content it already saw. When it can't — and it often can't — the user blames the model."

## Hashline!
**Covers:** the proposed edit format — content-hash line tags

Proposal: "when the model reads a file, or greps for something, every line comes back tagged with a 2-3 character content hash":

```text
hello.js — read
1:a3|function hello() {
2:f1|  return "world";
3:0e|}
```

The model then "references those tags — 'replace line 2:f1, replace range 1:a3 through 3:0e, insert after 3:0e.' If the file changed since the last read, the hashes (optimistically) won't match and the edit is rejected before anything gets corrupted."

Rationale: "If they can recall a pseudo-random tag, chances are, they know what they're editing. The model then wouldn't need to reproduce old content, or god forbid whitespace, to demonstrate a trusted 'anchor' to express its changes off of."

## The Benchmark
**Covers:** fixtures, protocol, headline results table

Fixtures: "Take a random file from the React codebase. Introduce mutations, framed as bugs, via an edit whose inverse we can expect (e.g. operator swaps, boolean flips, off-by-one errors, optional chains removed, identifiers renamed). Generate a description of the issue in plain English." Example task description: "Fix the bug in `useCommitFilteringAndNavigation.js` A guard clause (early return) was removed. The issue is in the `useCommitFilteringAndNavigation` function. Restore the missing guard clause (if statement with early return)."

Protocol: "3 runs per task, 180 tasks per run. Fresh agent session each time, four tools (read, edit, write). We simply give it a temporary workspace, pass the prompt, and once the agent stops, we compare against the original file before and after formatting." The chunk notes "we don't expect 100% success rate here, since the model can come up with a unique solution that isn't necessarily the exact same file, but the bugs are mechanical enough that most of the time, the fix is our mutation being reverted."

Results (pass rate per model per edit format; Δ PATCH, Δ REPL, token change as given in chunk):

| # | Model | Δ PATCH | Δ REPL | TOK |
|---|---|---|---|---|
| 01 | Grok Code Fast 1 | +64.6 | +4.6 | −49% |
| 02 | MiniMax M2.1 | +41.7 | +10 | −42% |
| 03 | Devstral Medium | +40.5 | +3.8 | — |
| 04 | GLM-4.5 Air | +27 | +0.4 | −17% |
| 05 | GLM-4.7 | +23.3 | +8.3 | −32% |
| 06 | GPT-5.1 Codex Mini | +20.3 | +4.2 | — |
| 07 | Grok-4.1 Fast | +19.2 | +2.5 | −20% |
| 08 | Grok 4 Fast | +17.4 | −0.4 | −61% |
| 09 | Qwen Turbo | +16.6 | −1.7 | — |
| 10 | Claude Sonnet 4.5 | +14.4 | +3.3 | −24% |
| 11 | Claude Haiku 4.5 | +13 | +11.3 | −22% |
| 12 | Gemini 2.5 Flash Lite | +10 | ±0 | — |
| 13 | Kimi K2.5 | +10 | +5 | −26% |
| 14 | Gemini 3 Flash | +8 | +11.3 | −21% |
| 15 | GPT-5.2 Codex | +4.6 | −0.4 | +26% |
| 16 | DeepSeek V3.2 | −5 | −8.3 | +20% |

Aggregate claims: "hashline beats patch in 14/16 models; the v2 revision improves further in 12/16 — largest gain GPT-5.1 Codex Mini, 60.0% → 77.5%." "Sixteen models, three edit tools, and the outcome is unambiguous: patch is the worst format for nearly every model, hashline matches or beats replace for most, and the weakest models gain the most."

## So What?
**Covers:** interpretation — harness gains vs model upgrades

"+8% improvement in the success rate of Gemini is bigger than most model upgrades deliver, and it cost zero training compute. Just a little experimenting (and ~$300 spent benchmarking)."

"Often the model isn't flaky at understanding the task. It's flaky at expressing itself. You're blaming the pilot for the landing gear."

## Little Bit About the Vendors
**Covers:** vendor actions vs open-harness argument

"Anthropic recently blocked OpenCode, a massively popular open-source coding agent, from accessing Claude through Claude Code subscriptions." Anthropic's position "'OpenCode reverse-engineered a private API' is fair on its face. Their infrastructure, their rules. But look at what the action signals: Don't build harnesses. Use ours."

"While writing this article, Google banned my account from Gemini entirely: Not rate-limited. Not warned. Disabled. For running a benchmark — the same one that showed Gemini 3 Flash hitting 78.3% with a novel technique that beats their best attempt at it by 5.0 pp."

Why backwards: "a different edit format improves their own models by 5 to 14 points while cutting output tokens by ~20%. That's not a threat. It's free R&D."

"No vendor will do harness optimization for competitors' models. Anthropic won't tune for Grok. xAI won't tune for Gemini. OpenAI won't tune for Claude. But an open-source harness tunes for all of them, because contributors use different models and fix the failures they personally encounter."

"The model is the moat. The harness is the bridge. Burning bridges just means fewer people bother to cross. Treating harnesses as solved, or even inconsequential, is very short-sighted."

Closing line in chunk: "All code, benchmarks, and per-run reports:omp"

**Covers:** chunk 01-the-wrong-question — article opening framing plus the full chunk body (headline stats, wrong-question argument, edit-tool survey, hashline proposal, benchmark protocol and 16-model results, interpretation, vendor section).
