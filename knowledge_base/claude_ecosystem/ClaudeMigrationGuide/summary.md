# Claude Model Migration Guide

**Source:** [Anthropic Claude Migration Guide (Anthropic, 2026)](https://platform.claude.com/docs/en/about-claude/models/migration-guide)
**Document type:** Official API migration documentation (not an academic paper)

## Human Readable TL;DR

Anthropic released new Claude models (Opus 4.7, Sonnet 4.6, Haiku 4.5) and this guide is the official playbook for updating your code so it keeps working. Think of it like the changelog when your phone's OS gets a major update -- most apps keep running, but a few settings moved, some old toggles are gone, and a couple of default behaviors changed in ways that can catch you off guard. The biggest shifts: "how hard should the model think" is now a dedicated knob (`effort`), several tuning dials like `temperature` are gone on Opus 4.7, and the model's reasoning is hidden by default so users might see a long pause before the answer appears. Switching the model name alone is usually not enough -- you need to adjust a few API fields and re-test.

## TL;DR

Anthropic's migration guide documents the API and behavioral changes required to move from Claude Opus 4.6, Opus 4.5/4.1, Sonnet 4.5, Sonnet 4, Sonnet 3.7, Haiku 3.5, or Haiku 3 to the current generation: **Opus 4.7**, **Sonnet 4.6**, and **Haiku 4.5**. The flagship changes on Opus 4.7 are: (1) `thinking: {type: "enabled", budget_tokens: N}` is removed in favor of `thinking: {type: "adaptive"}` + `output_config.effort`, (2) `temperature`/`top_p`/`top_k` are rejected as 400 errors, (3) prefilling assistant messages is blocked, (4) thinking content is omitted by default (silent change), and (5) a new tokenizer yields up to 35% more tokens for the same text. Pricing for Opus 4.7 stays at `$5 / $25` per MTok. Sonnet 4.6 (`$3 / $15`) and Haiku 4.5 (`$1 / $5`) have similar but smaller breaking sets. The `effort` parameter is GA with a new `xhigh` level recommended for coding/agentic use cases, and a beta `task_budget` offers advisory token caps across agentic loops.

---

## Scope & Migration Paths

| From | To | Key Action |
|------|-----|-----------|
| Opus 4.6 | **Opus 4.7** | Rename `thinking.type` to `adaptive`, remove sampling params, remove prefill |
| Opus 4.5 / 4.1 / Sonnet 4 / Sonnet 3.7 | **Opus 4.7** | Above + update tool versions, handle new stop reasons |
| Sonnet 4.5 | **Sonnet 4.6** | Remove prefill, set effort explicitly (new default `high`) |
| Sonnet 4 / 3.x | **Sonnet 4.6** | Above + update tool versions, remove double-sampling |
| Haiku 3.5 / 3 | **Haiku 4.5** | Model ID swap, new rate limits, same breaking-change set as Sonnet 3.x→4.6 |

Applies to **Messages API** code. Claude Managed Agents users only update the model name.

---

## Target Models at a Glance

| Model | Model ID | Input $/MTok | Output $/MTok | Context | Max Output |
|-------|----------|--------------|----------------|---------|------------|
| **Claude Opus 4.7** | `claude-opus-4-7` | $5 | $25 | 1M (no premium) | 128k |
| **Claude Sonnet 4.6** | `claude-sonnet-4-6` | $3 | $15 | (see overview) | (see overview) |
| **Claude Haiku 4.5** | `claude-haiku-4-5-20251001` | $1 | $5 | (see overview) | 64k |

Opus 4.7 supports: 1M context, 128k output, adaptive thinking, prompt caching, batch, Files API, PDF, vision (now high-res up to 2576px), all server+client tools (bash, code execution, computer use, text editor, web search/fetch, MCP, memory), and the new beta `task_budget`.

---

## Main Breaking Changes

### Opus 4.7 (from Opus 4.6)

1. **Extended thinking removed.** `thinking: {type: "enabled", budget_tokens: N}` returns 400. Replace with `thinking: {type: "adaptive"}` plus `output_config={"effort": "high"}`.
2. **Sampling parameters removed.** `temperature`, `top_p`, `top_k` at any non-default value returns 400. Omit them.
3. **Prefill blocked.** Prefilling assistant messages returns 400. Use structured outputs, system prompt instructions, or `output_config.format`.
4. **Thinking content omitted by default.** Thinking blocks still stream but the `thinking` field is empty. Set `thinking.display: "summarized"` to restore Opus 4.6 behavior.
5. **New tokenizer.** Up to 1.35x more tokens for the same text. Re-run `count_tokens`, re-budget `max_tokens`, re-tune compaction triggers.

### Opus 4.7 (from Opus 4.5 / 4.1 / Sonnet 4 / 3.7)

All of the above, plus:
- **Tool version updates required:** `text_editor_20250124` -> `text_editor_20250728` (and name `str_replace_editor` -> `str_replace_based_edit_tool`); `code_execution` -> `code_execution_20250825`. The `undo_edit` command no longer exists -- remove all code that uses it.
- **New stop reasons to handle:** `refusal` and `model_context_window_exceeded`.
- **Trailing newlines preserved** in tool-call string parameters (previously stripped on 4.5+).

### Sonnet 4.6

- Prefilling assistant messages returns 400.
- Tool parameter JSON escaping may differ (forward slashes, Unicode escapes) -- use a real JSON parser.
- When migrating from 3.x: only `temperature` OR `top_p`, not both. Tool version updates apply.
- **Default effort is now `high`** (Sonnet 4.5 had no effort parameter) -- explicitly set effort when migrating.

---

## Main Original Ideas / New Capabilities

1. **`xhigh` effort level.** New tier added to `effort` (`max`, `xhigh`, `high`, `medium`, `low`). Recommended as the best setting for most coding and agentic use cases. `max` may show diminishing returns and can be prone to overthinking.

2. **Task budgets (beta).** `output_config.task_budget = {"type": "tokens", "total": N}` with minimum 20k tokens. Beta header: `task-budgets-2026-03-13`. Unlike `max_tokens` (hard ceiling, model unaware), task budget is an **advisory cap across the full agentic loop** that the model sees and paces against. Not recommended for open-ended agentic work where quality matters most.

3. **Adaptive thinking as the default reasoning mode.** `thinking: {type: "adaptive"}` replaces manual `budget_tokens`. Automatically enables interleaved thinking (remove `interleaved-thinking-2025-05-14` header). Steerable via prompting and `effort`.

4. **High-resolution vision on Opus 4.7.** Max image resolution 2576px on long edge (up from 1568px); up to ~4,784 tokens per image (up from ~1,600). **Coordinates from pointing / bounding-box are now 1:1 with image pixels** -- remove any scale-factor conversion code. Automatic, no opt-in required. Downsample before sending if high-res fidelity isn't needed -- costs up to 3x more tokens per image.

5. **Real-time cybersecurity safeguards on Opus 4.7.** Legitimate pen testing, vuln research, and red-teaming work may be refused. Apply to the [Cyber Verification Program](https://claude.com/form/cyber-use-case) for reduced restrictions.

6. **Automated migration via Claude Code.** Run `/claude-api migrate this project to claude-opus-4-7` to invoke the bundled Claude API skill -- it applies the model ID swap, breaking parameter changes, prefill replacement, and effort calibration across the codebase, then produces a checklist.

---

## Behavioral Changes on Opus 4.7

- **Response length calibrates to task.** Simple lookups get shorter responses; open-ended analysis gets longer ones. Positive examples of concision ("Provide concise, focused responses. Skip non-essential context") work better than negative instructions.
- **More literal instruction following** at lower effort levels. No silent generalization across items, no inferring unstated requests. Better for structured extraction pipelines.
- **More direct tone.** Less validation-forward phrasing, fewer emoji. Re-evaluate style prompts.
- **Built-in progress updates.** Regular, higher-quality user updates in long agentic traces. Scaffolding that forced interim status messages can often be removed.
- **Fewer subagents spawned by default.** Steerable via explicit prompting.
- **Stricter effort calibration.** At `low`/`medium`, work is scoped tightly. Risk of under-thinking on moderately complex tasks at `low` -- remedy: raise effort or add "This task involves multi-step reasoning. Think carefully before responding."
- **Fewer tool calls by default.** Uses reasoning more than tools. Raise effort or prompt explicitly to increase tool usage.

---

## Code Examples

### Opus 4.6 -> Opus 4.7 (extended thinking)

```python
# Before (Claude Opus 4.6):
client.messages.create(
    model="claude-opus-4-6",
    max_tokens=64000,
    thinking={"type": "enabled", "budget_tokens": 32000},
    messages=[{"role": "user", "content": "..."}],
)

# After (Claude Opus 4.7):
client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # or "max", "xhigh", "medium", "low"
    messages=[{"role": "user", "content": "..."}],
)
```

### Restore visible thinking

```python
thinking = {"type": "adaptive", "display": "summarized"}
```

### Task budget (beta)

```python
output_config = {
    "effort": "high",
    "task_budget": {"type": "tokens", "total": 128000},
}
```

### Stop-reason handling

```python
response = client.messages.create(...)
if response.stop_reason == "refusal":
    # Handle refusal
    pass
if response.stop_reason == "model_context_window_exceeded":
    # Handle context limit (distinct from max_tokens hit)
    pass
```

### Tool version bump (from 3.x)

```python
# Before
tools = [{"type": "text_editor_20250124", "name": "str_replace_editor"}]
# After
tools = [{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
```

---

## Recommended Changes & Best Practices

- **Effort selection for Opus 4.7:**
  - `xhigh` -- best for most coding and agentic use cases (new)
  - `high` -- minimum recommended for intelligence-sensitive work
  - `medium` -- cost-sensitive, trades off intelligence
  - `low` -- short scoped tasks, latency-sensitive
  - `max` -- diminishing returns; can overthink
- At `max`/`xhigh`, set `max_tokens` >= 64k so the model has room to think and act across subagents and tool calls.
- **Re-benchmark cost and latency** under the new tokenizer -- up to 35% more tokens, uneven by content type.
- **Re-tune context compaction triggers** for the same reason.
- **Update client-side token estimators.**
- **Remove deprecated beta headers:** `effort-2025-11-24`, `fine-grained-tool-streaming-2025-05-14` (both now GA). `token-efficient-tools-2025-02-19` and `output-128k-2025-02-19` have no effect on Claude 4+ and should be removed.
- **Downsample images** before sending if you don't need full-resolution fidelity on Opus 4.7.
- **Remove scale-factor math** for vision coordinates -- they're now 1:1 with image pixels.
- **Explicit effort on Sonnet 4.6.** The default is `high` -- set it consciously when coming from Sonnet 4.5.
- **For Sonnet 4.6 adaptive thinking**, start at `high` effort for autonomous multi-step agents and computer use agents. Bimodal workloads (mix of easy and hard tasks) benefit the most.

---

## Gotchas & Warnings

- **`temperature = 0` was never deterministic** on prior models and is now a 400 error on Opus 4.7. Use prompting, not sampling, for determinism-adjacent behavior.
- **Silent thinking-display change.** If your product streams reasoning to users, they'll see a long pause before output on Opus 4.7 unless you opt in with `display: "summarized"`.
- **Vision cost jump.** High-res support is automatic -- image-heavy workloads may see ~3x token cost per image with no code change.
- **Tool-call JSON escaping differs** on Sonnet 4.6 / Opus 4.7. Standard parsers are fine; custom string-based parsers may break.
- **Trailing newlines preserved** in tool-call string parameters (Claude 4.5+). Exact string matching may break.
- **Task budget is advisory, not a hard cap.** If the cap is too tight, the model may complete less thoroughly and reference the budget as the constraint.
- **Haiku 4.5 has separate rate limits** from Haiku 3.5 and Haiku 3.
- **`budget_tokens` on Sonnet 4.6 is deprecated** -- still works but will be removed in a future model release. During transitional migration, ~16k budget gives headroom without runaway usage.

---

## Deprecation Timeline

Anthropic does not publish explicit removal dates -- items are flagged as "deprecated, to be removed in a future model release."

- `thinking: {type: "enabled", budget_tokens: N}` -- **removed** on Opus 4.7 (400 error). **Deprecated** on Sonnet 4.6.
- `output_format` parameter -- **deprecated** in favor of `output_config.format`.
- `effort-2025-11-24` beta -- **GA**, remove header.
- `fine-grained-tool-streaming-2025-05-14` beta -- **GA** on Sonnet 4.6 and Opus 4.7, remove header.
- `interleaved-thinking-2025-05-14` -- subsumed by adaptive thinking; remove header.
- `token-efficient-tools-2025-02-19`, `output-128k-2025-02-19` -- no effect on Claude 4+.
- `undo_edit` text-editor command -- removed.

---

## Document Structure (for reference)

The original migration guide is organized by target model:

1. Migrating to Claude Opus 4.7
2. Migrating to Claude Opus 4.7 from Opus 4.5 or earlier
3. Migrating to Claude Sonnet 4.6
4. Migrating to Claude Sonnet 4.5
5. Migrating to Claude Haiku 4.5
6. Get help

Each section follows the same pattern: update model name -> breaking changes -> recommended changes -> migration checklist.
