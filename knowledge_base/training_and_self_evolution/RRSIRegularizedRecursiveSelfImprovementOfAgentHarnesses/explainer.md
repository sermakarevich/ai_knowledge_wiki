> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# RRSI: Regularized Recursive Self-Improvement of Agent Harnesses — In Plain Language

## What is this about?

An AI agent is not just the language model. It is the model plus a
"harness": the prompts, step-by-step control flow, tools, memory, and
context management wrapped around it.

The harness decides whether the agent reads the right file before editing,
recovers after a failed command, or keeps its working notes tidy.
A good harness makes the same frozen model much more capable.

Recent work automates harness engineering: an LLM proposes edits to the
harness, keeps the ones that score well on a practice task set
(the "evolve set"), and repeats. This is recursive self-improvement
at the system level — the agent setup improves itself.

The catch: evolving against one fixed practice set causes overfitting.
Scores on the practice set jump, but scores on new tasks shrink,
vanish, or even drop below where you started.

RRSI (Regularized Recursive Self-Improvement) fixes this. It keeps every
kind of edit allowed, but adds guardrails on *how* the search uses
practice-set feedback — so what survives is a reusable mechanism,
not a memorized trick.

## Why does it matter?

Without guardrails, self-improvement is an illusion:

- Prior methods post big practice-set gains but keep little of it
  on new benchmarks. On office-style tasks, several end up *worse*
  than the starting harness they evolved from.
- The failures come from three habits: fitting quirks of one benchmark,
  chasing lucky scores caused by grading noise, and piling on complexity
  (extra steps, extra tool calls) that helps the practice set but
  nothing else.

RRSI matters because it is the version of self-improvement that
actually transfers. Evolved once per domain and run unchanged elsewhere,
it improves every held-out test: up to 14.1 points where it trained,
up to 4.7 points on five brand-new benchmarks — while burning about
30% fewer model tokens than unguarded evolution.

In short: it trades the flashiest practice score for the only
new-task average that clearly beats the starting point.

## How does it work?

RRSI leaves the edit space fully open — any prompt, tool, skill, memory,
or sub-agent can be added, changed, or removed. It regularizes the
*search path* instead, in two places.

**1. Smarter proposing (what gets suggested).**

- *Shrinking edit budget.* Early rounds may bundle several coordinated
  changes; later rounds are limited to one or two, so each change can
  be credited or blamed cleanly. The budget follows a cosine schedule
  from wide to narrow.
- *Full-history memory.* Every tried edit is logged with what it changed,
  what it was testing, and whether it worked. Rejected ideas stay
  rejected instead of being retried endlessly.
- *Explore when stuck.* When scores flatline inside the noise band,
  part of the budget is reserved for components never tried before —
  a nudge toward underexplored ideas.

**2. Stricter selecting (what gets kept).**

A candidate replaces the current harness only if it passes every gate:

- *Leakage screen.* A critic reads the diff first and rejects anything
  hardcoding task names, answers, or benchmark-specific logic.
  A cheater never even gets scored.
- *Noise floor.* The candidate must score within a small tolerance of
  the best score so far, where the tolerance is measured by re-running
  the unchanged starting harness. This blocks slow downhill drift.
- *Cost gate.* A real gain above noise must justify its extra token
  cost: extra cost is capped by a formula based on extra score.
  Tiny gains cannot buy big token bills.
- *Pruning.* Components that show no real gain over a recent window
  are flagged for deletion. Dead weight gets cut, like weeding a garden.

If no candidate passes all gates, the old harness stays. Standing still
beats adopting a bad change.

## Where can this be used?

The paper tests three families of work, evolving once per family and
then running the result unchanged on new benchmarks:

- *Coding.* Evolve on Terminal-Bench 2.1 (89 real terminal tasks);
  transfer to SWE-bench Verified bug fixing (+1.8 to +2.2 points,
  never trained on it).
- *Office / agentic workspace.* Evolve on Harvey LAB office tasks
  (Word, Excel, PDF deliverables); transfer to JobBench, GDPval,
  and APEX-Agents (+3.5 to +4.7 points each).
- *Engineering design.* Evolve on EngDesign simulator-graded tasks;
  transfer to Frontier-Eng (+4.3 Medal points, about +24%).

It also generalizes across models: a harness evolved with Gemini 3.5
Flash still helps an unseen weaker model (Gemini 3.1 Flash Lite, +30%
relative), and the same approach works under Claude Opus 4.8.

Practical uses: any team auto-tuning agent scaffolds — code agents,
document assistants, design copilots — where the tuned setup must work
on next month's tasks and next year's model, not just today's test set,
and where inference-token bills matter.

## Conclusions & takeaways

- A reused practice set makes "self-improvement" partly fake: scores
  rise without the underlying mechanism getting better.
- Fixing it means controlling *how feedback becomes permanent change*,
  not shrinking what the agent is allowed to become.
- Removing either guardrail group raises the practice score and lowers
  transfer: no gates at all gives the highest practice score (92.8)
  but near-zero transfer at 3.80M tokens per run vs 2.42M for RRSI.
- The full RRSI harness is the lightest of all evolved harnesses
  (26.3 steps per task vs 27–35 for rivals), yet the only one with
  robust out-of-distribution gains and zero held-out regressions.
- Limits: models stay frozen (no weight updates), results depend on a
  finite practice set plus a few tuning knobs, and longer runs and more
  tool ecosystems still need testing.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| Harness | Everything around the model: prompts, workflow, tools, memory, context handling. |
| Evolve set | The practice task set used to propose and score edits during improvement. |
| Held-out / out-of-distribution | New tasks or benchmarks the harness never trained on; the real test. |
| Overfitting | Scoring higher on practice tasks without getting genuinely better. |
| H0 (base harness) | The starting agent setup before any evolution. |
| Proposer | The part that suggests harness edits each round. |
| Selector / acceptance rule | The gates deciding whether a suggested edit replaces the current harness. |
| Leakage screening | Rejecting edits that hardcode answers or benchmark quirks. |
| Noise floor (delta) | Score wiggle room from grading randomness; changes inside it don't count as real. |
| Policy tokens | Model output tokens per task; a proxy for cost and complexity. |
| Structural pruning | Deleting harness parts that haven't earned their keep recently. |
| Transfer | A harness improved in one place still helping somewhere new, unchanged. |
