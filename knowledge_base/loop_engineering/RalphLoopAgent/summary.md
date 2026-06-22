# Technical Analysis: ralph-loop-agent

**Repository:** https://github.com/vercel-labs/ralph-loop-agent
**Version analyzed:** 0.0.3
**Date:** 2026-06-22

---

## 1. Overview / What Problem It Solves

Standard LLM tool-calling patterns execute a single pass: the model receives a prompt, calls tools, and returns a final answer. This works for bounded tasks but fails for long-horizon work where the correct answer requires an unknown number of tool calls and the model cannot reliably self-assess completion mid-response.

`ralph-loop-agent` addresses this by wrapping the AI SDK's `generateText` in an outer verification loop -- dubbed the "Ralph Wiggum Technique" -- that re-runs the agent as many times as needed, checking an external `verifyCompletion` predicate after each pass. The primary user is a developer or AI coding agent needing deterministic task completion rather than a single best-effort attempt.

The package is a thin, composable TypeScript library layered on top of Vercel's AI SDK. It adds iteration control, cumulative token/cost accounting, optional context summarization, and Anthropic prompt-caching awareness -- none of which the base AI SDK provides natively.

---

## 2. High-Level Architecture

```
 Caller
   |
   v
RalphLoopAgent.loop() / .stream()
   |
   +-- Outer Loop (Ralph loop)
   |      |
   |      +-- buildSystemMessages()
   |      +-- RalphContextManager.prepareMessagesForIteration()  [optional]
   |      |
   |      v
   |   generateText()  [AI SDK inner tool loop]
   |      |  stopWhen: stepCountIs(20) [default]
   |      |  tools, model, messages, prepareStep
   |      |
   |      +-- aggregateStepUsage()  -- totalUsage accumulation
   |      +-- onIterationEnd() callback
   |      +-- isRalphStopConditionMet()  -- checks: iteration, tokens, cost
   |      +-- verifyCompletion()  -- caller-supplied predicate
   |             +-- complete=true  --> return RalphLoopAgentResult
   |             +-- complete=false --> inject feedback, next iteration
   |
   v
RalphLoopAgentResult { text, iterations, completionReason, totalUsage, allResults }
```

**Data flow (one full pass):**

1. Caller invokes `agent.loop({ prompt })`, starting iteration counter at 0.
2. `buildSystemMessages()` converts `instructions` string/object to `ModelMessage[]`.
3. `RalphContextManager` (if configured) trims or summarizes `currentMessages` to fit token budget; injects summaries and change-log into system message.
4. `generateText` runs the inner tool loop with `stepCountIs(20)` guard; response messages are appended to `currentMessages`.
5. `aggregateStepUsage` accumulates per-step usage into `totalUsage` (more accurate than `result.usage` for multi-step runs).
6. Stop conditions evaluated; if not hit, `verifyCompletion` is called.
7. On `complete=false`, optional `reason` is injected as a user-role feedback message and the outer loop continues.
8. On `complete=true` or stop-condition hit, a `RalphLoopAgentResult` is returned.

Persistent state lives entirely in memory within the `RalphLoopAgent` instance: `currentMessages` array, `allResults` array, and the `RalphContextManager`'s file/changelog maps. There is no database, disk cache, or cross-call persistence between separate `loop()` invocations unless `preserveContext: true` is passed.

---

## 3. The Agent Loop Abstraction

The central abstraction is the **iteration** -- a single `generateText` call (which itself may contain many tool steps) that forms one unit of work within the outer Ralph loop.

**Key types:**

| Type | File | Purpose |
|------|------|---------|
| `RalphLoopAgentSettings<TOOLS>` | `ralph-loop-agent-settings.ts` | Full agent configuration; extends AI SDK `CallSettings` |
| `RalphLoopAgentResult<TOOLS>` | `ralph-loop-agent.ts:55-85` | Return value: text, iteration count, reason, usage |
| `RalphLoopAgentCallParameters` | `ralph-loop-agent.ts:30-50` | Per-call params: prompt, abortSignal, preserveContext |
| `VerifyCompletionContext<TOOLS>` | `ralph-loop-agent-evaluator.ts:7-25` | Context passed to the caller's completion check |
| `VerifyCompletionResult` | `ralph-loop-agent-evaluator.ts:30-45` | `{ complete: boolean, reason?: string }` |
| `RalphStopConditionContext<TOOLS>` | `ralph-stop-condition.ts:10-32` | Context for safety stop conditions |
| `RalphStopCondition<TOOLS>` | `ralph-stop-condition.ts:37-42` | `(context) => boolean | PromiseLike<boolean>` |

**Completion reason enum** (`completionReason` field):
- `'verified'` -- `verifyCompletion` returned `{ complete: true }`
- `'max-iterations'` -- a stop condition fired
- `'aborted'` -- `AbortSignal` was triggered

**Key knobs controlling behavior:**

- `stopWhen` -- outer loop guard; defaults to `iterationCountIs(10)`
- `toolStopWhen` -- inner tool loop guard passed directly to `generateText`; defaults to `stepCountIs(20)` from AI SDK
- `verifyCompletion` -- optional async predicate; if omitted, runs to `stopWhen`
- `contextManagement` -- optional `RalphContextConfig`; enables `RalphContextManager`

---

## 4. LLM / External Service Integration

The library does not bundle a provider directly. Model selection uses the AI Gateway string format (`{provider}/{model}`, e.g. `anthropic/claude-opus-4.5`) or a raw `LanguageModel` object from any AI SDK-compatible provider.

**Provider detection:**

`isAnthropicModel()` checks `model.includes('anthropic')` or `model.includes('claude')` -- or `model.provider` for object-form models. When detected, the `prepareStepWithCaching` wrapper adds `providerOptions.anthropic.cacheControl: { type: 'ephemeral' }` to the last message of every step, enabling prompt caching automatically.

**Required env vars:** None in the library itself. The AI SDK resolves credentials via its own provider resolution. The CLI example requires a Vercel Sandbox token.

**Cost accounting:** `ralph-stop-condition.ts` embeds a `MODEL_PRICING` table covering Anthropic (Haiku/Sonnet/Opus), OpenAI (GPT-4o, o1, o3), Google (Gemini 2.5), xAI (Grok 3), and DeepSeek. `costIs(maxDollars)` uses this table to stop the loop when cumulative spend exceeds a threshold. Custom rates can also be passed directly.

**Frameworks used:** Vercel AI SDK v6 (`ai`, `@ai-sdk/provider-utils`). No LangChain, no LangGraph, no other orchestration layer.

---

## 5. The Main Pipeline

The `loop()` method in `packages/ralph-loop-agent/src/ralph-loop-agent.ts` is the primary user-facing workflow.

**Step-by-step:**

1. **Initialize** (`loop():139-150`): Initialize `allResults = []`, `currentMessages = []`, `iteration = 0`, zero-valued `totalUsage`. Optionally call `contextManager.clear()` unless `preserveContext` is true.

2. **Build initial message** (`loop():152-156`): Wrap `prompt` as a `ModelMessage` with `role: 'user'`.

3. **System messages** (`buildSystemMessages():370-390`): Convert `instructions` (string, `SystemModelMessage`, or array) to `ModelMessage[]` with `role: 'system'`.

4. **Context preparation** (`loop():180-225`): If `RalphContextManager` is active, call `prepareMessagesForIteration()`. It trims old iterations, optionally summarizes via an LLM call, and appends a context injection block (change log + file summaries) to the system message.

5. **Continuation prompt injection** (`loop():228-238`): For iterations > 1, push a user message `"Continue working on the task. The previous attempt was not complete."`.

6. **Cache control wrapper** (`loop():240-270`): For Anthropic models, wrap `prepareStep` to tag the last message per step with `cacheControl: { type: 'ephemeral' }`.

7. **Inner tool loop** (`loop():273-300`): `generateText(...)` with all settings forwarded. `toolStopWhen` defaults to `stepCountIs(20)`.

8. **Usage aggregation** (`loop():306-308`): `aggregateStepUsage(result)` sums per-step usage (not just the top-level `result.usage`, which under-counts in multi-step runs).

9. **Message history update** (`loop():311`): `currentMessages = [...currentMessages, ...result.response.messages]`.

10. **Stop condition check** (`loop():318-330`): Evaluate all `stopWhen` conditions against `{ iteration, allResults, totalUsage, model }`. Break on first true.

11. **Completion verification** (`loop():333-360`): Call `verifyCompletion` if configured. On `complete=false` with a `reason`, push that reason as `role: 'user'` feedback and log to `contextManager`.

12. **Return** (`loop():363-374`): Pack final text, iteration count, reason, and aggregated usage into `RalphLoopAgentResult`.

---

## 6. Key Files

| File | Lines | What It Does |
|------|-------|--------------|
| `packages/ralph-loop-agent/src/ralph-loop-agent.ts` | ~390 | Core `RalphLoopAgent` class; `loop()` and `stream()` methods; message assembly |
| `packages/ralph-loop-agent/src/ralph-stop-condition.ts` | ~260 | Stop condition types, `iterationCountIs`, `tokenCountIs`, `costIs`, `MODEL_PRICING` table, `calculateCost`, `aggregateStepUsage` |
| `packages/ralph-loop-agent/src/ralph-context-manager.ts` | ~300 | `RalphContextManager`: file tracking, change log, iteration summarization, LRU eviction |
| `packages/ralph-loop-agent/src/ralph-loop-agent-settings.ts` | ~80 | `RalphLoopAgentSettings<TOOLS>` type; all configuration fields |
| `packages/ralph-loop-agent/src/ralph-loop-agent-evaluator.ts` | ~50 | `VerifyCompletionContext`, `VerifyCompletionResult`, `VerifyCompletionFunction` types |
| `packages/ralph-loop-agent/src/index.ts` | ~30 | Public exports |
| `packages/ralph-loop-agent/src/ralph-loop-agent.test.ts` | ~310 | Vitest unit tests; covers loop, stream, callbacks, feedback injection |
| `examples/cli/index.ts` | ~400 | Full CLI coding agent using the library; sandbox management, interrupt handling |
| `examples/cli/lib/sandbox.ts` | ~300 | Vercel Sandbox lifecycle, file copy with secret filtering, dev tools installation |
| `examples/cli/lib/judge.ts` | ~150 | Claude Opus 4.5 judge agent that approves/rejects completed tasks |
| `examples/cli/lib/tools/` | unknown | CLI agent tools (file read/write, command execution, screenshot, etc.) |
| `packages/ralph-loop-agent/package.json` | ~35 | Package manifest; version `0.0.3`, peer dep `zod ^4.0.0` |

---

## 7. Dependencies

**Package: `ralph-loop-agent`**

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `ai` | `^6.0.0` | Vercel AI SDK; `generateText`, `streamText`, `stepCountIs`, types |
| `@ai-sdk/provider-utils` | `^4.0.0` | `ModelMessage` type for message construction |
| `zod` | `^4.0.0` (peer) | Schema validation (passed through to AI SDK tools) |

**Dev dependencies:**

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `typescript` | `^5.9.3` | Compiler |
| `vitest` | `^4.0.0` | Test runner |
| `@types/node` | `^22.0.0` | Node type definitions |

**CLI example additional dependencies:**

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `@vercel/sandbox` | `^1.1.2` | Isolated sandbox VM for running agent-generated code |
| `dotenv` | `^17.2.3` | Environment variable loading |
| `ignore` | `^7.0.5` | Gitignore-aware file filtering for sandbox sync |
| `just-bash` | `1.4.2` | Shell command utilities |
| `prompts` | `^2.4.2` | Interactive CLI prompts |
| `tsx` | `^4.19.4` | TypeScript executor for dev |

---

## 8. CLI / Usage Surface

**Entry points:**

- Library: ESM-only via `packages/ralph-loop-agent/dist/index.js` (compiled from `src/index.ts`)
- CLI example: `examples/cli/index.ts` run via `tsx`; invoked with `pnpm examples:cli`

**Basic usage:**

```typescript
import { RalphLoopAgent, iterationCountIs, tokenCountIs, costIs } from 'ralph-loop-agent';

const agent = new RalphLoopAgent({
  model: 'anthropic/claude-opus-4.5',
  instructions: 'You are a coding assistant.',
  tools: { readFile, writeFile },
  stopWhen: iterationCountIs(10),           // outer loop guard
  toolStopWhen: stepCountIs(20),            // inner tool loop guard
  verifyCompletion: async ({ result }) => ({
    complete: result.text.includes('DONE'),
    reason: 'Task marker found',
  }),
  onIterationStart: ({ iteration }) => console.log(`Iteration ${iteration}`),
  onIterationEnd: ({ iteration, duration, result }) => { /* logging */ },
});

// Non-streaming
const { text, iterations, completionReason, totalUsage } = await agent.loop({
  prompt: 'Migrate all usages of deprecated API X to Y',
});

// Streaming (only final iteration is streamed)
const stream = await agent.stream({ prompt: 'Refactor this module' });
for await (const chunk of stream.textStream) { process.stdout.write(chunk); }
```

**Stop condition combinators:**

```typescript
// Stop when any condition fires
stopWhen: [iterationCountIs(20), tokenCountIs(500_000), costIs(5.00)]

// Cost guard with explicit rates for unlisted models
stopWhen: costIs(2.00, { inputCostPerMillionTokens: 3, outputCostPerMillionTokens: 15 })
```

**Environment variables (CLI example):**

| Variable | Default | Purpose |
|----------|---------|---------|
| `ANTHROPIC_API_KEY` | -- | Required for Claude models via AI Gateway |
| `VERCEL_SANDBOX_TOKEN` | -- | Required for Vercel Sandbox execution |

---

## 9. Extensibility Points

- **Custom stop conditions:** Implement `RalphStopCondition<TOOLS>` -- a function `(ctx: RalphStopConditionContext) => boolean | Promise<boolean>`. Pass one or an array to `stopWhen`. No subclassing required; the built-ins (`iterationCountIs`, `tokenCountIs`, `costIs`) are plain functions in `ralph-stop-condition.ts`.

- **Custom completion verification:** Supply any async function as `verifyCompletion`. It receives the full `GenerateTextResult`, the current iteration, all prior results, and the original prompt. This is where domain-specific success criteria live -- e.g., running a test suite, calling a linter, or prompting a second "judge" model (as the CLI example does in `lib/judge.ts`).

- **Context management extension:** `RalphContextManager` exposes `trackFileRead()`, `trackFileWrite()`, `addChangeLogEntry()`, and `createContextAwareTools()`. The `createContextAwareTools()` wrapper can be applied to any AI SDK-compatible tool set to automatically log file operations without manual instrumentation.

- **Tool integration:** `tools` accepts any `ToolSet` from the AI SDK. The `activeTools` field (array of tool name keys) can restrict which tools are available per-agent without redefining the tool set.

- **Model provider:** Any `LanguageModel` object or AI Gateway string is accepted. Anthropic prompt-caching is wired in automatically via `isAnthropicModel()`. To add caching for a new provider, extend the `prepareStepWithCaching` logic in `ralph-loop-agent.ts`.

---

## 10. Limitations and Gotchas

- **`stream()` omits context management.** The `stream()` method duplicates most of `loop()` but omits the `RalphContextManager` integration. Long streaming runs can exceed token limits silently.

- **Continuation prompt is hardcoded.** Every iteration > 1 injects `"Continue working on the task. The previous attempt was not complete."` with no way to override it from `RalphLoopAgentSettings`. This can confuse models on multi-phase tasks.

- **Token estimation is a rough heuristic.** `RalphContextManager.estimateTokens()` divides character count by 3.5. This underestimates code-heavy content and tool-call JSON, potentially letting messages exceed context windows before the budget check fires.

- **Stop condition fires after, not before, an iteration.** The stop condition is checked after `generateText` returns, meaning the N-th iteration always runs even if the budget was already exceeded entering it. A $0.10 per-iteration model can overshoot a `costIs(1.00)` guard by one full iteration.

- **No resume across process restarts.** `preserveContext: true` only avoids clearing `currentMessages` between multiple `loop()` calls on the same in-memory instance. There is no serialization or disk persistence.

- **`MODEL_PRICING` table will go stale.** Hardcoded pricing in `ralph-stop-condition.ts` is not fetched from any API. Unknown models throw an error at runtime (not at construction time).

- **`stream()` callback gap.** `onIterationStart` / `onIterationEnd` are called for non-streaming pre-pass iterations; the final streamed iteration emits no `onIterationEnd`.

- **Version 0.0.3 is explicitly experimental.** `AGENTS.md` is addressed to AI coding agents, not human developers -- signaling the library targets agentic workflows and may change API surface without semver guarantees.

---

## 11. How It Compares to Alternatives

**LangGraph (Python/JS):** LangGraph models agent work as an explicit DAG of nodes and edges, enabling complex branching, human-in-the-loop checkpoints, and persistent state via a checkpointer backend. It requires substantially more upfront graph design. `ralph-loop-agent` is intentionally simpler -- no graph definition needed, no checkpointer infrastructure, drop-in on top of existing AI SDK code -- at the cost of expressing only linear retry loops rather than conditional branches or parallel subgraphs.

**AutoGen (Microsoft):** AutoGen supports multi-agent conversations with role specialization (planner, executor, critic). `ralph-loop-agent` keeps everything in one agent with an external verifier predicate. AutoGen is heavier, Python-first, and requires more configuration for basic loops. Ralph is a TypeScript-native single-agent pattern with a minimal API surface.

**OpenAI Assistants API (with run polling):** The Assistants API handles tool-call iteration server-side, but ties the implementation to OpenAI and manages state opaquely. `ralph-loop-agent` is provider-agnostic, keeps all state in the caller's process, and exposes every intermediate result via `allResults` and callbacks -- better for inspection and debugging.

**Raw AI SDK `generateText` with manual loops:** This is what `ralph-loop-agent` replaces. Writing a `while (true)` loop around `generateText` manually means reimplementing usage accumulation, stop-condition logic, feedback injection, and caching -- all of which Ralph provides. The tradeoff is a new dependency for what is ~400 lines of glue code.

`ralph-loop-agent` occupies the narrow niche of AI SDK users who want autonomous retry loops without adopting a full orchestration framework.

---

## Appendix: Selected Code Snippets

**Outer loop stop-then-verify ordering** (`ralph-loop-agent.ts`, loop body):

```typescript
// Check stop conditions AFTER running iteration
const stopContext: RalphStopConditionContext<TOOLS> = {
  iteration,
  allResults,
  totalUsage,
  model: modelId,
};

if (await isRalphStopConditionMet({ stopConditions, context: stopContext })) {
  completionReason = 'max-iterations';
  break;
}

// Verify completion
if (this.settings.verifyCompletion) {
  const verification = await this.settings.verifyCompletion({
    result,
    iteration,
    allResults,
    originalPrompt: prompt,
  });

  if (verification.complete) {
    completionReason = 'verified';
    reason = verification.reason;
    break;
  }

  if (verification.reason && !verification.complete) {
    currentMessages.push({
      role: 'user',
      content: [{ type: 'text', text: `Feedback: ${verification.reason}` }],
    });
  }
}
```

**Anthropic prompt-cache injection per step** (`ralph-loop-agent.ts`):

```typescript
const addCacheControlToMessages = (messages: ModelMessage[]): ModelMessage[] => {
  if (messages.length === 0) return messages;
  return messages.map((message: ModelMessage, index: number) => {
    if (index === messages.length - 1) {
      return {
        ...message,
        providerOptions: {
          ...message.providerOptions,
          anthropic: {
            ...(message.providerOptions?.anthropic as Record<string, unknown> ?? {}),
            cacheControl: { type: 'ephemeral' },
          },
        },
      };
    }
    return message;
  });
};
```

**`costIs` stop condition with model pricing lookup** (`ralph-stop-condition.ts`):

```typescript
export function costIs(
  maxCostDollars: number,
  ratesOrModel?: CostRates | string
): RalphStopCondition<any> {
  return ({ totalUsage, model }) => {
    let rates: CostRates;
    if (typeof ratesOrModel === 'object') {
      rates = ratesOrModel;
    } else {
      const modelToUse = typeof ratesOrModel === 'string' ? ratesOrModel : model;
      const pricing = getModelPricing(modelToUse);
      if (!pricing) {
        throw new Error(
          `Unknown model "${modelToUse}". Provide explicit rates:\n` +
            `costIs(${maxCostDollars}, { inputCostPerMillionTokens: X, outputCostPerMillionTokens: Y })`
        );
      }
      rates = pricing;
    }
    const currentCost = calculateCost(totalUsage, rates);
    return currentCost >= maxCostDollars;
  };
}
```
