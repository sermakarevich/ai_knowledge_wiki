# Designing Loops with Fable 5

**Source:** [Designing loops with Fable 5 (Lance Martin, Jun 9, 2026)](https://x.com/RLanceMartin/status/2064397389189071163)

## Human Readable TL;DR

Anthropic's most advanced AI model (Fable 5) works best not when you carefully write detailed instructions for it, but when you build a feedback loop -- like a self-grading homework system -- that lets it try something, get a score, fix its mistakes, and repeat. The article shows two examples: one where the AI improved a machine learning training script 6x better than the previous model, and another where it built up a reliable notes system across multiple conversations. The key insight is to let the AI correct itself using feedback from the environment, rather than trying to micromanage it.

## TL;DR

Lance Martin (MTS at Anthropic) shares two patterns for maximizing Fable 5's capabilities: self-correction loops and memory management. Self-correction loops use `/goal` (Claude Code) or `Outcomes` (Claude Managed Agents) as rubric-based feedback primitives that let the model hillclimb toward a goal autonomously. Memory enables cross-session learning via a mounted filesystem. Fable 5 showed ~6x better improvement than Opus 4.7 on Parameter Golf, and 73% verification coverage (vs. 7-33% for Opus 4.7) on Continual Learning Bench.

---

## Problem & Motivation

Direct prompting and manual steering of powerful models like Fable 5 underutilizes their capabilities. The article argues that designing feedback environments -- loops with structured goals, rubrics, and memory -- allows Fable 5 to self-correct and compound learnings in ways that earlier models cannot match.

---

## Main Original Ideas

1. **Self-correction loops via goal/rubric primitives** -- Rather than steering Fable 5 step-by-step, provide a rubric or goal that acts as an evaluator. Fable 5 runs, receives feedback from the rubric, self-corrects, and repeats until satisfied. `/goal` in Claude Code and `Outcomes` in Claude Managed Agents (CMA) are the concrete API primitives for this pattern.

2. **Verifier sub-agents outperform self-critique** -- Models struggle to self-critique their own outputs. A separate verifier agent grading in an independent context window produces better results. CMA's `Outcomes` primitive implements this by spawning a dedicated grader sub-agent automatically.

3. **Structural vs. scalar exploration under loops** -- With a self-correction loop, Fable 5 bets on larger structural experiment changes and shows resilience (e.g., pushing through regressions to reach bigger wins). Opus 4.7, by contrast, converges to scalar adjustments after the first positive result.

4. **Memory as an outer loop across sessions** -- Memory enables a progression: fail → investigate → verify → distill → consult. Fable 5 completes this cycle, turning individual errors into verified general rules retrievable in future sessions. Earlier models stall at failure notes or unverified hypotheses.

---

## Key Findings

### Parameter Golf benchmark (ML training optimization, up to 8 hours, 8xH100s)

| Model | Strategy | Outcome |
|-------|----------|---------|
| **Fable 5** | Structural changes; resilient through regressions | **~6x improvement** over baseline |
| Opus 4.7 | First win → scalar adjustments only | ~1x (incremental) |

### Continual Learning Bench 1.0 (sequential SQL Q&A with memory across sessions)

| Model | Memory progression reached | Verification coverage |
|-------|---------------------------|----------------------|
| Sonnet 4.6 | Step 1 (failure notes only) | ~0% |
| Opus 4.7 | Step 3 (schema reference, uncertainty flagged) | 7--33% (median ~17%) |
| **Fable 5** | Step 5 (distilled general rules, consulted) | **Up to 73% (22/30)** |

Memory progression steps: **fail → investigate → verify → distill → consult**

---

## Suggestions & Future Directions

1. Test Fable 5 on your own challenging tasks using self-correction loops (`/goal`, `Outcomes`) before relying on direct prompting.
2. Design rubrics or goals with checkable criteria rather than open-ended instructions -- the Outcomes grader requires discrete verifiable conditions.
3. Provide task-specific memory instructions for smaller models (like Sonnet 4.6) where autonomous memory management is insufficient.
4. Refer to the [Fable 5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) and Claude Managed Agents docs to get started.

---

## Authors & Institutions

Lance Martin (@RLanceMartin) -- Member of Technical Staff, Anthropic
