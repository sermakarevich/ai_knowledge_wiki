> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# How They Got Here

**In one sentence:** `/prewalk` did not start as a benchmark-driven design — it started as an informal habit (starting hard tasks on a frontier model and switching to Kimi K27 after a few turns to avoid thought-loops) that got formalized only after a chance conversation revealed other people did the same thing, and three iterations of "when do you swap?" converged on triggering the swap at the first landed edit, gated by a todo list.

## Key points

- Origin: working in an open-source harness exposed the author to many different people's ad hoc habits. Their own habit was to start easy-to-medium tasks with a frontier model, then switch to Kimi K27 after a few turns "so it wouldn't fall into its usual thought loops" — done without ever measuring whether it was rational.
- The trigger to formalize it was social, not analytical: someone else independently mentioned doing the same kind of swap, which prompted the question "are we idiots, or does this actually work, and when?" and a real benchmark.
- **Attempt 1 — swap at a fixed turn (e.g. turn 4):** rejected as "obviously bad in hindsight" — sometimes the frontier model is still lost at turn four, sometimes it has already finished the whole fix, so a fixed turn count ignores task variance.
- **Attempt 2 — swap after the first edit:** better, since the model has "demonstrated the pattern once, in place, in style," but still finicky — small executor models would sometimes declare the task done "out of nowhere," with no real signal to stop that from happening.
- **Final design — plan + todo list, swap on first edit:** the frontier model is asked to spell out a plan step by step, then, once ready to execute, initialize a TODO list with a validation step for each item; the swap triggers on the first edit that follows.
- The todo list is not incidental — it is the actual steering mechanism. A small executor model "can forget the plan, a validation step, or what it's doing entirely, but it cannot forget the todo reminder that bugs it endlessly," which is what stops premature "done" declarations.
- A model-specific failure mode surfaced during tuning: GPT-5.6 as the frontier "guide" tends to create 60-item TODO lists and complete them in batches — "do they just hand out rewards for anything?" — so the production prompt needs an explicit item-count limit.
- The technique shipped as `--prewalk`, `--prewalk-into <model>`, or `/prewalk` in the open-source harness `omp` referenced throughout the article (see [[05-cheating-and-prefill|Cheating and the Prefill Connection]] for its lineage back to the "prefill" trick).

---

## Why gating on "any edit" alone is not enough

The article is explicit that edit-gating by itself is insufficient — "gating on any edit alone is no good; the todo list still has a very important role here." The insight is that a bare edit event tells you the model took *an* action, but not that it is still oriented toward the plan; the todo list is what keeps a small model's remaining turns tethered to the original intent even after the handoff, which the earlier "swap after first edit" attempt lacked.

## Covers

The article's "How we got here" section, from the informal Kimi K27 habit through the three swap-timing iterations to the shipped `--prewalk` flags.
