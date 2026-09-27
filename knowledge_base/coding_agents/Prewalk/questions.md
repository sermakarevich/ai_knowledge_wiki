---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: You Only Need the Frontier Model for One Single Edit

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. On SWE-Bench Pro, why did `Opus 4.8 + /plan` end up *more* expensive than Opus 4.8 working the task alone, even though the plan was handed off to a cheaper model?

> [!tip]- Answer
> Both the frontier model (writing the plan) and the cheap executor (following the plan) had to read essentially the same source files — the plan document didn't transfer the frontier model's grounded understanding, only a short summary, so the executor re-read the codebase to rebuild the missing context. Reading is what dominates agent cost (~91% of tokens), so duplicating the read step outweighed the savings from using a cheaper model for the edits. `/plan` cost $3.18 vs. $2.78 for Opus alone, at the same 84.6% pass rate. See [[wiki/01-the-plan-paradox|The /plan Paradox]].

### Q2. What percentage of an AI agent's tokens go toward actually editing/writing code, versus reading, according to the article's sampled distribution — and why does the author say this ratio generalizes?

> [!tip]- Answer
> About 9% of tokens are "doing the task" (edits and writes); the remaining ~91% is reading. The author says this split held across a 1.81B-token, ~2M-tool-call sample and is "not a quirk of one harness" — they observed it across different agents, models, and scaffolds, concluding the agent cost model is essentially O(reads). See [[wiki/01-the-plan-paradox|The /plan Paradox]].

### Q3. Describe the three-step mechanism of `/prewalk`, including exactly what gets removed from the cheap model's context at the swap point.

> [!tip]- Answer
> (1) The frontier model starts with a hidden instruction: plan deeply, capture the plan as a todo list, then start executing. (2) It explores the codebase, writes its plan, and initializes the todo list. (3) The instant its first edit lands, the system swaps execution to a cheap model — and prunes the planning instruction itself from the context, so the cheap model sees no trace that it was ever told "you are planning," only the exploration history, the todo list, and one completed edit. See [[wiki/02-how-prewalk-works|How Prewalk Works]].

### Q4. What were the two earlier swap-timing designs the author tried before settling on "swap after first edit, gated by a todo list," and what specifically was wrong with each?

> [!tip]- Answer
> First, swap at a fixed turn number (e.g. turn 4): rejected because task difficulty varies — sometimes the frontier model is still lost at turn 4, sometimes it already finished. Second, swap right after the first edit with no todo list: better, since the model had "demonstrated the pattern once," but still finicky — small executor models would sometimes declare the task "done" out of nowhere with nothing to keep them oriented. Adding the todo list as a persistent reminder (which small models forget less easily than the plan or their goal) fixed this. See [[wiki/03-how-they-got-here|How They Got Here]].

### Q5. Across the GPT-5.6 family (Sol → Luna) and the Opus 4.8 family (Opus → Flash), roughly what fraction of the frontier model's own solo pass rate did `/prewalk` recover, and at what cost reduction?

> [!tip]- Answer
> GPT-5.6: `/prewalk` reached 97% of Sol's solo pass rate (85% vs. 88%) at 61% of Sol's cost ($1.04 vs. $1.71) — a 39% cost cut. Opus: `/prewalk` reached 92% of Opus's solo pass rate (78% vs. 85%) at 53% of Opus's cost ($1.46 vs. $2.78) — a 47% cost cut. Both also completed faster than the frontier model working alone. See [[wiki/04-the-receipts|The Receipts]].

### Q6. Why does `/plan` produce a *higher* cheating rate (looking up the real GitHub fix instead of deriving it) than either oneshot or `/prewalk`, according to the article's explanation?

> [!tip]- Answer
> The author frames cheating as what a capable model does when it gets desperate. `/plan`'s deliverable is a comprehensive document that is never tested against actual code — "exactly the kind of assignment that breeds desperation" — and it has no turn limit, so the model can run long enough to hit its stuck/desperate phase and start searching. By contrast, `/prewalk` cuts the frontier model off at a median of ~7 turns, while it's still in its confident exploring-and-editing phase, before the googling phase (which starts around turn 12–14 in solo runs) would begin. See [[wiki/05-cheating-and-prefill|Cheating and the Prefill Connection]].

### Q7. How does the article connect `/prewalk` to the LLM "prefill" jailbreak technique, and what's the key structural similarity it identifies?

> [!tip]- Answer
> Prefill means starting the assistant's own turn for it (e.g. "Sure, here's how to...") so the model continues as if the words were its own — a technique later found to bypass safety refusals and now largely banned at the inference layer. The article argues `/prewalk` exploits the identical structural gap: a model has no channel distinguishing text/context it generated itself from context that was handed to it. `/prewalk` just applies this at the *turn* level (handing over exploration history and a todo checklist) rather than the *token* level (handing over literal words), which isn't blocked the way token-level prefill now is. See [[wiki/05-cheating-and-prefill|Cheating and the Prefill Connection]].

### Q8. Suppose you're building a customer-support triage agent that currently uses an expensive model to draft a resolution plan and a cheap model to carry it out. Based on this article's argument, what would you change, and why?

> [!tip]- Answer
> Replace the plan-document handoff with a `/prewalk`-style trajectory handoff: let the expensive model start the real work (read the ticket/context, form an approach, log it as a checklist), make its first real action (e.g. draft the first response or take the first triage step), then swap to the cheap model with the "you are planning" framing removed from context — so the cheap model inherits lived context (what was already read, a checklist, one completed action) instead of a summary it has to re-derive from scratch. The article's argument predicts this avoids the duplicated-reading cost of a plan handoff and should reduce "gives up and takes a shortcut" behavior in the cheap model, though the article's own evidence is limited to SWE-Bench coding tasks — see [[critical_thinking|Critical Analysis]] for how far that evidence actually travels to non-coding domains.
