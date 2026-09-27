> [[index|Wiki]] | [[summary|Summary]]

# What Does Context Compression Cost an Agent? — In Plain Language

## What is this about?

Imagine an assistant who's been working with you for hours on a big project. Their notebook is full, so at some point they tear out the older pages and either throw them away or replace them with a short bullet-point summary. Later, when they need something that was on those torn-out pages — "wait, which shelf did we say the parts were on?" — they have two choices: guess, or go ask again. Asking again costs time. If you only measure "did the project get finished," you might never notice how much extra asking-around happened along the way — the project still got done, just with more phone calls.

That's exactly the situation with AI agents that use tools (search a database, call an API, check a file) over a long task. Because a language model's "memory" (its context window) is limited, real systems compress the conversation history as it grows — dropping old turns, summarizing them, or filtering what's kept. The standard way people check if this is safe is: did the agent still complete the task? This paper's whole point is that that check hides a cost. The agent might finish the task exactly as often, while quietly making two or three times as many extra tool calls to re-fetch things it used to have.

The paper builds a small, controlled test world — a project-planning game with tools split into "look things up" (retrieval) and "do the work" (execution) — and shows this hidden cost is real, measurable, and depends on *what kind* of information got thrown away.

## Why does it matter?

If you build or operate AI agents, someone eventually asks "can we compress the conversation history to save tokens/cost?" and the go/no-go answer usually comes from a benchmark score: did success rate drop? This paper shows that's the wrong single number to trust. A compression method can look completely safe on that score while silently multiplying how many tool calls (and therefore latency, API cost, and rate-limit exposure) the agent burns per task. If you only watch completion, you could ship a compression strategy that quietly makes your agent 2-3x more expensive to run per task and never see it in your dashboards.

## How does it work?

1. **Split the bill into two parts.** Instead of tracking just "did it finish," the paper tracks a triple: completion rate, retrieval tool calls (re-fetching state), and execution tool calls (doing task work). Think of it like tracking not just "did the errand get done" but also "how many extra trips to the store did it take."
2. **Build a fair test track.** A ten-task project-planning world is built where a seed fully determines the puzzle, so the exact same task can be replayed under different memory conditions — full memory, memory trimmed by deleting old turns ("sliding window"), or memory trimmed but replaced by a short fact-summary. Every turn has a hard cap (24 turns), so there's a real budget being spent.
3. **Compress and count.** Run the same tasks under each memory condition, and count completion, and how many "look things up" vs. "do the work" calls happened. Result: trimming (deleting) makes the "look things up" count jump — sometimes triple — while completion barely moves.
4. **Prove it's causal, not coincidental.** Take the exact piece of information that got deleted and hand it back to the agent as a note ("oracle restoration"). If restoring it makes the extra lookups mostly disappear, that proves the lookups were caused by that specific missing piece — not some unrelated side effect.
5. **Ask what kind of missing information matters.** Some dropped facts can be looked up again from an outside source (like re-reading a task list — call this **D**, for queryable). Others only ever existed in what already happened (like a rule the agent discovered mid-task — call this **R**, for history-only). Losing D causes lots of extra lookups (because the agent *can* look it up, so it does, repeatedly). Losing R doesn't — there's nowhere to look it up, so the agent just proceeds with less certainty.
6. **Test whether the content of a kept summary matters, or just its presence.** Feed the agent a summary containing fabricated, made-up facts instead of real ones (same length, same format). Retrieval cost goes up even higher than with no summary at all — showing the agent isn't just reacting to "is there a note," it's reacting to whether the note is actually trustworthy.
7. **Check the boundary.** Run the identical trimming trick in a completely different environment (a household simulation, ALFWorld) where missing facts can simply be re-observed by looking around. There, trimming causes *no* extra lookups at all — proving this hidden cost isn't an automatic tax on all compression, it only shows up when the missing information can only be recovered by asking, not by looking.

## Where can this be used?

- **Evaluating any agent harness or memory system** that compresses, summarizes, or truncates conversation history — this gives a concrete second metric (tool-call cost, split by type) to check alongside pass/fail rate.
- **Deciding what to keep in a summary** when building a memory/compaction layer: this work suggests prioritizing *validity* of retained facts over clever selection of *which* facts to keep, and prioritizing history-only facts when the summary budget is tight (because they're cheap to keep and expensive to lose).
- **Diagnosing a "why is this agent making so many redundant tool calls" complaint** in production — the oracle-restoration technique here (hand back a suspected missing fact and see if calls drop) is directly usable as a debugging technique, not just a research method.
- **Setting SLAs or cost budgets for agentic pipelines** — a system that "passes" on completion metrics can still be burning 2-3x the tool-call budget; this paper is a reminder to price that in.

## Conclusions & takeaways

- Passing a completion benchmark after adding compression does not mean the compression is cheap — check tool-call cost too, split into "re-fetching" vs. "doing work" if you can.
- The kind of information that gets dropped matters more than how aggressively you compress: information you can re-query is expensive to lose (the agent goes and re-queries it, repeatedly); information that only existed in history is not recoverable by asking, so its loss shows up as completion risk, not extra tool calls.
- If you keep a summary/digest of dropped history, its *content being genuine and correct* matters more than being clever about exactly which facts you pick — a summary full of the wrong (but real-looking) facts is worse than no summary.
- This isn't evidence that compression is bad — the same paper shows a well-designed summary operator can be nearly free. It's evidence that "completion didn't drop" is not proof of "this is cheap."
- Caveat worth remembering: this was tested in two bounded, somewhat synthetic environments and three model families at mostly one compression ratio — treat the mechanism as a real and useful diagnostic, not as settled numbers that transfer unchanged to your own production agent.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Context compression | Any technique (deleting old turns, summarizing, filtering) that shrinks an agent's conversation history so it fits in the model's limited memory window |
| Interaction cost / reacquisition cost | The extra tool calls an agent makes to re-fetch information it used to have before that information was compressed away |
| Task completion | Whether the agent finished the task — the metric everyone checks, and the one this paper says isn't enough on its own |
| Non-identifiability (of completion) | A formal way of saying "completion alone can't tell two situations with very different real costs apart" — like judging a road trip only by "did we arrive," ignoring how many wrong turns it took |
| Sliding-window operator | The simplest compression method: just delete the oldest turns once the history gets too long, keeping only the most recent ones |
| Fact-preserving (extractive) summary | A compression method that keeps a short list of the facts that were observed, instead of deleting them outright — no facts, but also no leftover reasoning text |
| Oracle intervention / oracle restoration | A test where the exact piece of information that was deleted gets handed back to the agent as a note, to prove that its absence (not something else) was causing the extra tool calls |
| D-state (queryable state) | Information that, if lost, the agent could in principle get back by asking an outside source again (e.g. re-reading a task list) |
| R-state (history-dependent state) | Information that only ever existed inside what already happened — nobody to ask, no way to look it up again if it's gone |
| Bounded-horizon agent | An agent that only gets a fixed number of turns/tool calls to finish — so any wasted turns spent re-fetching information directly eat into its chance of finishing |
| Holm correction | A statistical adjustment used when running many significance tests at once, to avoid falsely calling too many results "significant" just by chance |
| Retention intervention | An experiment that deliberately changes what a kept summary contains (how much, which facts, real vs. fake) to isolate exactly which property of the summary drives the agent's behavior |
