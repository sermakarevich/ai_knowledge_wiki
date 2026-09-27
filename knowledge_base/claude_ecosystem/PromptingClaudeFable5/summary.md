# Prompting Claude Fable 5

**Source:** [Prompting Claude Fable 5 -- Anthropic Documentation](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
**Publisher:** Anthropic
**Date:** 2026

## Human Readable TL;DR

Claude Fable 5 is a much more capable AI assistant than previous versions -- think of it like upgrading from a competent contractor to a senior engineer who can independently tackle week-long projects. Because it's more capable, some of the "hand-holding" instructions you wrote for older models can actually slow it down or produce worse results. This guide tells you which old habits to drop, which new controls to use, and how to make sure the AI stays on track during long, unsupervised work sessions.

## TL;DR

Claude Fable 5 introduces significant behavioral shifts -- longer autonomous runs, stronger instruction following, more proactive parallel agent delegation, and improved self-verification -- that require prompt and scaffolding updates when migrating from Claude Opus 4.8. The primary controls are the `effort` parameter (low/medium/high/xhigh), concise steering instructions rather than exhaustive behavior lists, explicit constraints on scope and side-effects, and a structured memory system. Several safety classifiers covering offensive cybersecurity and life sciences can trigger `stop_reason: "refusal"`, requiring fallback configuration.

---

## Problem & Motivation

Claude Fable 5 represents a capability step large enough that prompts and harnesses tuned for Claude Opus 4.8 may produce suboptimal results or unexpected behaviors. The model sustains multi-hour autonomous runs, dispatches parallel subagents more readily, and follows intent rather than just literal instructions -- qualities that create new failure modes (over-planning, unrequested side-effects, context-budget anxiety) alongside new opportunities (first-shot complex implementations, week-long goal-directed runs). Teams migrating from prior models need concrete guidance on which patterns require tuning and which guardrails can be retired.

---

## Main Original Ideas

1. **Effort as the primary intelligence/cost dial.** A new `effort` parameter (`low` / `medium` / `high` / `xhigh`) replaces coarser controls. `high` is the recommended default; `xhigh` for maximum capability; lower levels for interactive or routine work. Lower effort on Fable 5 still outperforms `xhigh` on prior models.

2. **Single-instruction behavioral steering.** Because instruction-following is substantially improved, a one-line directive ("lead with the outcome") controls entire behavioral classes that previously needed per-pattern enumeration. Over-specified instructions from older prompts actively degrade output.

3. **Explicit scope constraints prevent unrequested actions.** Fable 5 can draft emails, create git branches, or refactor surrounding code without being asked. Explicit "don't act until asked" and "check evidence before changing system state" instructions are necessary.

4. **Tool-call audit before progress reports.** On long autonomous runs, instructing the model to verify each progress claim against an actual tool result in the current session nearly eliminates fabricated status reports.

5. **Structured memory system for cross-session learning.** Providing a write-accessible location (even a single Markdown file) and a format rule ("one lesson per file, one-line summary at top") enables lessons to persist and be referenced across runs. The model can bootstrap this from prior session history using subagents.

6. **Parallel subagents as first-class primitives.** Fable 5 dispatches subagents more readily than prior models. Harnesses should prefer asynchronous communication, long-lived subagents that retain context across subtasks, and explicit delegation instructions.

7. **`send_to_user` tool for verbatim mid-task messages.** Tool inputs are never summarized by the model, so a dedicated tool with a single `message` field guarantees that deliverables, progress numbers, and direct replies arrive in the UI exactly as written without ending the agent's turn.

8. **Refusal stop reason and fallback routing.** Safety classifiers covering offensive cybersecurity and biology/life sciences return `stop_reason: "refusal"`. Scaffolding should configure automatic fallback to Claude Opus 4.8 for requests in those domains rather than surfacing errors.

---

## Key Findings

### Recommended prompt snippets

| Behavior to control | Prompt instruction |
|---|---|
| Prevent over-planning / re-deriving | "When you have enough information to act, act. Do not re-derive facts already established in the conversation..." |
| Prevent unrequested refactoring/abstractions | "Don't add features, refactor, or introduce abstractions beyond what the task requires..." |
| Output brevity | "Lead with the outcome. Your first sentence after finishing should answer 'what happened' or 'what did you find'..." |
| Checkpoint behavior | "Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide." |
| Progress grounding | "Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for..." |
| Scope constraints | "When the user is describing a problem... the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one." |
| Subagent delegation | "Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track." |
| Early stopping in autonomous mode | "For reversible actions that follow from the original request, proceed without asking... Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question... do that work now with tool calls." |
| Context-budget anxiety | "You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits." |
| Final-message readability | "Your final summary is different: it's for a reader who didn't see any of [the working context]. Write complete sentences. Spell out terms..." |

### `send_to_user` tool schema

```json
{
  "name": "send_to_user",
  "description": "Display a message directly to the user. Use this for progress updates, partial results, or content the user must see exactly as written before the task finishes.",
  "input_schema": {
    "type": "object",
    "properties": {
      "message": { "type": "string", "description": "The content to display to the user." }
    },
    "required": ["message"]
  }
}
```

### Safety classifier domains that trigger refusal

- Offensive cybersecurity: exploits, malware, attack tooling
- Biology and life sciences: lab methods, molecular mechanisms
- Extraction of summarized thinking from the model

Benign work in adjacent domains may also trigger these. Configure server-side or client-side fallback to Claude Opus 4.8.

---

## Suggestions & Future Directions (Recommended Scaffolding Changes)

1. **Start at the top of your difficulty range.** Test Fable 5 on tasks harder than what you'd assign to prior models. Testing only on simple workloads undersells the model's range.

2. **Make self-verification explicit in long-run prompts.** Fresh-context verifier subagents outperform self-critique. Instruct: `Establish a method for checking your own work at an interval of [X]... verify with subagents against the specification.`

3. **Refactor existing prompts and skills.** Prompts developed for prior models are often over-prescriptive and degrade output on Fable 5. Review and remove instructions where default performance is already better. Fable 5 can update skills on the fly from task learnings.

4. **Audit for show-your-thinking instructions.** Prompts that tell the model to echo or explain its internal reasoning can trigger the `reasoning_extraction` refusal category. Remove reflection/transcription instructions; use structured `thinking` blocks from adaptive thinking instead.

5. **Create a send-to-user tool.** For long, asynchronous agents, implement the tool above to deliver messages verbatim without ending the agent turn.

6. **Prefer async harness patterns.** Individual hard-task requests can run for many minutes at `high`/`xhigh` effort. Adjust client timeouts, add streaming, surface progress indicators, and consider checking on runs via scheduled jobs rather than blocking.

7. **Memory bootstrap prompt.** To seed a new memory system from prior history: `Reflect on the previous sessions we've had together. Use subagents to identify core themes and lessons, and store them in [X].`

---

## Authors & Institutions

Anthropic (documentation team)
