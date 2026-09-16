---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# LangChainCustomHarness — Retrieval Questions

## Q1 (core recall): What is the `agent = model + harness` formula, and what are the 3 inputs to the minimal `create_agent`?

<details>
<summary>Answer</summary>

An agent is defined as **agent = model + harness**, where the **harness** is the scaffolding that connects the model to the real world and delivers the right context at every step. Agent quality is mainly a function of context delivery fitted to the task.

LangChain's minimal `create_agent` takes just **3 inputs — (1) a model, (2) tools, and (3) a system prompt** — and implements only the core **model-calls-tools loop**. Everything else is added via composable middleware.

</details>

## Q2 (core recall): What are the 4 cooperating levers by which middleware customizes the agent loop?

<details>
<summary>Answer</summary>

The digest names **4 middleware customization levers**: **(1) deterministic logic, (2) tool lifecycle management, (3) custom state, and (4) stream handlers**.

Middleware hooks into the loop at each step — before/after model calls, before/after tool calls, plus agent startup and teardown — with each piece handling one concern and composing freely. LangChain ships prebuilt middleware for common patterns; bespoke behavior is one custom middleware away, and isolated units are reusable across every agent in an organization.

</details>

## Q3 (core recall): What are the 6+ production middleware capability groups a task-fitted harness stacks, and what 3 factors choose them?

<details>
<summary>Answer</summary>

Production agents combine several capabilities at once, chosen by **3 factors: (1) whether the run is long-lived, (2) task complexity, and (3) action sensitivity**. The capability groups from the digest:

1. **Context management** — summarization and context editing against overflow from accumulated history.
2. **Memory** — load relevant knowledge at startup, write it back at end of run, so the agent improves over time.
3. **Action/delegation** — filesystem/shell/code-execution access plus subagents (clean context windows) with a todo list for long runs.
4. **Reliability** — retries with backoff and model fallbacks for transient failures.
5. **Policy/steering** — PII/compliance/approval middleware on every call plus human-in-the-loop gates for consequential actions.
6. **Cost control** — call limits plus prompt caching.

LangChain's own agents (GTM agent, async coding agent, no-code builder) each run `create_agent` with a stack tailored to that mission.

</details>

## Q4 (elaboration): Why does a minimal `create_agent` beat an opinionated pre-assembled harness for a new task — what breaks if you just reuse a fixed stack?

<details>
<summary>Answer</summary>

Because the harness's job is **delivering the right context at the right time for the specific task**, a fixed stack (e.g. Deep Agents / Claude Agent SDK with pre-set memory, context management, sandboxing) ships context machinery the task may not need — extra middleware injects irrelevant context, burns tokens, adds failure modes and policy friction, and obscures what actually drives quality.

What breaks if you reuse it blindly: you pay for unused capabilities, get context bloat instead of task-fitted context, and can't isolate which piece caused a failure. The minimal core (model-calls-tools loop) plus only-the-needed-middleware keeps the harness tightly fitted and debuggable.

</details>

## Q5 (elaboration): What breaks on a long-running agent if the harness has no summarization/context-editing and no retries/fallbacks?

<details>
<summary>Answer</summary>

**Without summarization and context editing**, accumulated message history grows until it exceeds the context window — the run crashes, or the oldest (often most important) context is silently truncated, so the model loses track of goals and repeats work.

**Without retries with backoff and model fallbacks**, any transient failure (rate limit, timeout, flaky tool) kills the whole run instead of being absorbed, which is fatal for long-lived sessions where at least one transient error is near-certain. Both are why reliability and context management are first-class harness concerns, not prompt tweaks.

</details>

## Q6 (transfer): Sketch the middleware stack for (a) a long-running coding agent vs (b) a customer-service agent. Which capabilities does each emphasize?

<details>
<summary>Answer</summary>

**(a) Long-running coding agent** — emphasize context + action + reliability: summarization/context editing for huge histories, memory load/write-back across sessions, filesystem/shell/code-execution tools, subagents with clean context windows + todo-list tracking, retries/fallbacks, call limits + prompt caching to bound long-run spend, plus sandboxing/approval gates for shell side effects.

**(b) Customer-service agent** — emphasize policy + steering + cost: PII/compliance/approval middleware on every external call, human-in-the-loop gates for consequential actions (refunds, account changes), memory for user/account context, prompt caching + call limits for high-volume cheap turns; subagents and code execution are usually unnecessary.

This is task-harness fit: match the stack to each task's actual context needs, likely failures, enforced policies, and environment.

</details>

## Q7 (evaluation): The article claims `create_agent` beats opinionated pre-assembled harnesses (Deep Agents, Claude Agent SDK) for custom fit. What kind of evidence backs this claim, and what's the catch? See [[critical_thinking|Critical Analysis]].

<details>
<summary>Answer</summary>

**No benchmark, cost figure, or user study backs it** — the comparison is purely architectural narrative (minimal core vs. fixed stack), made in a first-party LangChain blog post comparing its own API favorably against named sibling/competitor products. The catch: this is vendor framing, not measured evidence. The underlying `agent = model + harness` thesis and the capability checklist (context, memory, action/delegation, reliability, policy, cost) are useful design vocabulary regardless of framework, but the specific claim that `create_agent`'s minimalism outperforms pre-assembled harnesses in practice is unverified by the article itself.

</details>
