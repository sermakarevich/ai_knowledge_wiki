# Best Practices for Using Claude Opus 4.7 with Claude Code

**Paper:** [Best practices for using Claude Opus 4.7 with Claude Code (Anthropic / Claude Blog, 2026)](https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code)

## Human Readable TL;DR

Imagine you just got a smarter assistant that decides on its own how long to think about each question instead of being told "think for exactly 5 minutes." This guide tells you how to get the best out of that upgraded assistant: set clear goals up front, trust its judgment on when to think harder, and nudge it with plain-English cues like "think carefully" or "answer quickly" instead of fiddling with knobs. The big change: the default "effort" level has moved up a notch, so you get more thoughtful answers by default -- and you can tune it down when you just want speed.

## TL;DR

Opus 4.7 replaces the fixed extended-thinking budget with **adaptive thinking** -- the model decides when to invest reasoning tokens based on context. A new `xhigh` effort level sits between `high` and `max` and is the new default, best for most agentic coding work. The guide recommends front-loading context in the first turn, minimizing interactive clarification, using natural-language cues to bias thinking depth, and explicitly scoping subagent usage. Behavior differs from 4.6: shorter default responses, fewer tool calls, and fewer auto-spawned subagents.

---

## Problem & Motivation

Upgrading from Opus 4.6 to 4.7 shifts token usage because of tokenizer updates and increased reasoning at higher effort levels. Teams porting old prompts and settings verbatim get suboptimal results. The post gives organizations concrete recalibration guidance so they can leverage 4.7's new adaptive thinking and recalibrated defaults without regressing on efficiency or quality.

---

## Main Original Ideas

1. **Adaptive Thinking (replaces fixed extended-thinking budgets).** The model now decides dynamically when to apply extended thinking instead of being given a fixed token budget. It can skip thinking on simple queries and invest tokens strategically on hard ones, and is less prone to overthinking than 4.6.

2. **New `xhigh` effort level, now the default.** A new tier sits between `high` and `max`. It is positioned as "the best setting for most coding and agentic uses" -- API/schema design, legacy code migration, codebase review, multi-file changes, and ambiguous debugging.

3. **Front-load context in turn one.** Instead of an iterative back-and-forth, specify the full task up front with all relevant context. Minimizing user interactions reduces reasoning overhead and helps the model commit to a coherent plan.

4. **Natural-language effort nudges.** Bias thinking depth via plain prompt language rather than config flags: "Think carefully and step-by-step before responding; this problem is harder than it looks" to deepen thinking, or "Prioritize responding quickly rather than thinking deeply. When in doubt, respond directly" to shorten it.

5. **Explicit subagent scoping.** 4.7 spawns fewer subagents by default. If parallelism helps, say so; if not, prevent overuse with cues like "Do not spawn a subagent for work you can complete directly in a single response (e.g., refactoring a function you can already see)."

---

## Key Findings

**Effort level guidance:**

| Effort | When to use |
|--------|-------------|
| `low` / `medium` | Cost-sensitive, latency-sensitive, or tightly scoped work |
| `high` | Balances intelligence and cost |
| **`xhigh` (default)** | **Best setting for most coding and agentic uses** |
| `max` | Squeezes out additional performance on genuinely hard problems |

**Behavior changes from Opus 4.6:**

- Response length now calibrates to task complexity -- less default verbosity
- Fewer tool calls; the model reasons more before acting
- Fewer subagents spawned by default
- Fixed extended-thinking budgets are no longer supported

**Practical tips:**

- Toggle effort levels mid-task to manage token spend
- Prefer positive examples ("do this") over negative instructions ("don't do that") for style guidance
- Use auto mode for trusted long-running tasks to reduce unnecessary check-ins
- Batch questions into a single turn rather than spreading across turns

---

## Suggestions & Future Directions

1. **Don't port 4.6 settings verbatim.** Experiment with effort levels rather than copying old configurations.
2. **Revisit prompts written for fixed thinking budgets.** Remove references to explicit thinking token counts; let adaptive thinking handle depth.
3. **Tune subagent behavior explicitly.** Since 4.7 is more conservative, add guidance when parallel subagents would actually help.
4. **Use natural-language cues as the primary lever** for thinking depth before reaching for settings changes.
5. **Users with unchanged settings auto-upgrade to `xhigh`**, but should review whether that default suits each workload.

---

## Authors & Institutions

Published on the Claude Blog (Anthropic), April 16, 2026. Category: Claude Code. No individual author byline.
