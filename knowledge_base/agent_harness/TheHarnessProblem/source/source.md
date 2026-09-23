> PDF location (no local PDF under 2 MB): https://stencil.so/blog/the-harness-problem
# We improved 15 LLMs at coding in one afternoon. Only the harness changed. — Stencil
Source: https://stencil.so/blog/the-harness-problem
Kind: article
Fetched: 2026-09-18T17:51:23.136817+00:00
Tool: urllib

We improved 15 LLMs at coding in one afternoon. Only the harness changed. — Stencil

In fact only the edit tool changed. That's it.

+15ptsavg over patch, 16 models

10×Grok Code Fast 1

−61%output tokens, best case

$0training compute

SORTΔ PATCHΔ REPLACEHASHLINE % PATCH REPLACE HASHLINE V2

MODEL0255075100Δ PATCHΔ REPLTOK

01Grok Code Fast 1+64.6+4.6−49%

02MiniMax M2.1+41.7+10−42%

03Devstral Medium+40.5+3.8—

04GLM-4.5 Air+27+0.4−17%

05GLM-4.7+23.3+8.3−32%

06GPT-5.1 Codex Mini+20.3+4.2—

07Grok-4.1 Fast+19.2+2.5−20%

08Grok 4 Fast+17.4−0.4−61%

09Qwen Turbo+16.6−1.7—

10Claude Sonnet 4.5+14.4+3.3−24%

11Claude Haiku 4.5+13+11.3−22%

12Gemini 2.5 Flash Lite+10±0—

13Kimi K2.5+10+5−26%

14Gemini 3 Flash+8+11.3−21%

15GPT-5.2 Codex+4.6−0.4+26%

16DeepSeek V3.2−5−8.3+20%

Pass rate per model per edit format · 3 runs × 180 tasks, fresh session each ·
hashline beats patch in 14/16 models; the v2 revision improves further in 12/16 —
largest gain GPT-5.1 Codex Mini, 60.0% → 77.5%

## The Wrong Question

The conversation right now is almost entirely about which model is best at coding, GPT-5.3 or Opus. Gemini vs whatever dropped this week. This framing is increasingly misleading because it treats the model as the only variable that matters, when in reality one of the bottlenecks is something much more mundane: the harness.

Not only is it where you capture the first impression of the user (is it uncontrollably scrolling, or smooth as butter?), it is also the source of every input token, and the interface between their output and every change made to your workspace.

Why bother, you ask? Opus may be a great model, but Claude Code to this day leaks raw JSONL from sub-agent outputs, wasting hundreds of thousands of tokens. In an open harness, we get to just fix that: subagents output structured data now.

Tool schemas, error messages, state management, everything between "the model knows what to change" and "the issue is resolved." This is where most failures happen in practice.

Being model agnostic, it is a great testing ground, as the model is but a parameter. The real variable is the harness, which you have unimaginable control over.

Anyhow — about that one variable we changed yesterday.

## Edit Tool!

Before we explain what we built, it's worth understanding the state of the art.

Codex uses apply_patch: It takes a string as input, which is essentially an OpenAI-flavored diff, and instead of relying on a structured schema, the harness just expects this blob to follow a strict set of rules. Since OpenAI folks are without a doubt smart, the token selection process is almost certainly biased to fit this structure at the LLM gateway for the Codex variants of GPT, similar to how other constraints like JSON schemas or required tool calls work.

But give this to any other model, completely unaware of it? Patch failures go through the roof. Grok 4's patch failure rate in our benchmark was 50.7%, GLM-4.7's was 46.2%. These aren't bad models — they just don't speak the language.

Claude Code (and most others) use str_replace: find the exact old text, swap in the new text. Very simple to think about. But the model must reproduce every character perfectly, including whitespace and indentation. Multiple matches? Rejected. The "String to replace not found in file" error is so common it has its own GitHub issues megathread (+27 other issues). Not exactly optimal. Gemini does essentially the same thing plus some fuzzy whitespace matching.

Cursor trained a separate neural network: a fine-tuned 70B model whose entire job is to take a draft edit and merge it into the file correctly. The harness problem is so hard that one of the most well-funded AI companies decided to throw another model at it, and even then they mention in their own blog post that "fully rewriting the full file outperforms aider-like diffs for files under 400 lines."

Aider's own benchmarks show that format choice alone swung GPT-4 Turbo from 26% to 59%, but GPT-3.5 scored only 19% with the same format because it couldn't reliably produce valid diffs. The format matters as much as the model.

The Diff-XYZ benchmark from JetBrains confirmed it systematically: no single edit format dominates across models and use cases. EDIT-Bench found that only one model achieves over 60% pass@1 on realistic editing tasks.

As you can see, there is no real consensus on the "best solution" to the simple "how do you change things" problem. Our take: none of these tools give the model a stable, verifiable identifier for the lines it wants to change without wasting tremendous amounts of context and depending on perfect recall. They all rely on the model reproducing content it already saw. When it can't — and it often can't — the user blames the model.

## Hashline!

Now bear with us here. What if, when the model reads a file, or greps for something, every line comes back tagged with a 2-3 character content hash:

hello.js — read

1:a3|function hello() {
2:f1|  return "world";
3:0e|}

When the model edits, it references those tags — "replace line 2:f1, replace range 1:a3 through 3:0e, insert after 3:0e." If the file changed since the last read, the hashes (optimistically) won't match and the edit is rejected before anything gets corrupted.

If they can recall a pseudo-random tag, chances are, they know what they're editing. The model then wouldn't need to reproduce old content, or god forbid whitespace, to demonstrate a trusted "anchor" to express its changes off of.

## The Benchmark

Since our primary concern was real-world performance, the fixtures are generated as follows:

Take a random file from the React codebase.

Introduce mutations, framed as bugs, via an edit whose inverse we can expect (e.g. operator swaps, boolean flips, off-by-one errors, optional chains removed, identifiers renamed).

Generate a description of the issue in plain English.

An average task description looks something like this:

# Fix the bug in `useCommitFilteringAndNavigation.js`A guard clause (early return) was removed.The issue is in the `useCommitFilteringAndNavigation` function.Restore the missing guard clause (if statement with early return).

Naturally, we don't expect 100% success rate here, since the model can come up with a unique solution that isn't necessarily the exact same file, but the bugs are mechanical enough that most of the time, the fix is our mutation being reverted.

3 runs per task, 180 tasks per run. Fresh agent session each time, four tools (read, edit, write). We simply give it a temporary workspace, pass the prompt, and once the agent stops, we compare against the original file before and after formatting.

Sixteen models, three edit tools, and the outcome is unambiguous: patch is the worst format for nearly every model, hashline matches or beats replace for most, and the weakest models gain the most. Grok Code Fast 1 went from 6.7% to 68.3%, a tenfold improvement, because patch was failing so catastrophically that the model's actual coding ability was almost completely hidden behind mechanical edit failures. MiniMax more than doubled. Grok 4 Fast's output tokens dropped 61% because it stopped burning tokens on retry loops.

## So What?

+8% improvement in the success rate of Gemini is bigger than most model upgrades deliver, and it cost zero training compute. Just a little experimenting (and ~$300 spent benchmarking).

Often the model isn't flaky at understanding the task. It's flaky at expressing itself. You're blaming the pilot for the landing gear.

## Little Bit About the Vendors

Anthropic recently blocked OpenCode, a massively popular open-source coding agent, from accessing Claude through Claude Code subscriptions.

Anthropic's position "OpenCode reverse-engineered a private API" is fair on its face. Their infrastructure, their rules. But look at what the action signals:

Don't build harnesses. Use ours.

It's not just Anthropic either. While writing this article, Google banned my account from Gemini entirely:

Not rate-limited. Not warned. Disabled. For running a benchmark — the same one that showed Gemini 3 Flash hitting 78.3% with a novel technique that beats their best attempt at it by 5.0 pp. I don't even know what for.

Here is why that is backwards. We just showed that a different edit format improves their own models by 5 to 14 points while cutting output tokens by ~20%. That's not a threat. It's free R&D.

No vendor will do harness optimization for competitors' models. Anthropic won't tune for Grok. xAI won't tune for Gemini. OpenAI won't tune for Claude. But an open-source harness tunes for all of them, because contributors use different models and fix the failures they personally encounter.

The model is the moat. The harness is the bridge. Burning bridges just means fewer people bother to cross. Treating harnesses as solved, or even inconsequential, is very short-sighted.

All code, benchmarks, and per-run reports:omp
