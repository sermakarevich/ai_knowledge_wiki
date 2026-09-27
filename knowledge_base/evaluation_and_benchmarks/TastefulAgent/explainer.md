> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# The Tasteful Agent: Measuring and Improving Taste in Long-Horizon Tasks — In Plain Language

## What is this about?

"Taste" here means one specific skill: picking a good direction when the payoff only shows up much later.

Think of an agent on a long coding or research task. Sooner or later it faces a fork: which hypothesis is worth testing, which half-working implementation to build on, or which experiment to run next?

Today's benchmarks mostly check the final score — did the task succeed? They do not grade the quality of the choices made along the way.

This paper fills that gap with Taste-Bench: 502 multiple-choice questions mined from real agent runs. Each question freezes a run at a decision fork, hides everything afterwards, and asks: which direction was better?

Forks come from two natural sources: parallel attempts (two runs of the same task start alike, then split, and one works out better) and detours (inside one run, the agent goes down a wrong path, hits a wall, and corrects itself).

Headline result: the best frontier model gets only 59.7% of these two-way choices right.
Almost half the time, the strongest available model picks the worse road.

## Why does it matter?

Long tasks live or die on a handful of direction choices. One bad fork can waste hours of otherwise competent work.

A final pass/fail score cannot tell you whether the agent was smart or merely lucky. Two agents can fail for different reasons, or one can succeed despite sloppy judgment. Taste-Bench isolates judgment from execution luck by comparing branches that started from the same place.

Three findings make this urgent. First, errors pile up where the deciding clue appears late: accuracy falls from 62.3% to 21.0% as the key evidence moves further into the future. Second, letting the model "think longer" does not fix it — bigger reasoning budgets leave scores roughly flat. Third, taste separates top models that ordinary coding benchmarks squash together: the top four models sit within 4 points on one popular benchmark but spread over 10.7 points on taste.

In short: we have been measuring finish lines, not route choices, and route choices are where agents fail.

## How does it work?

The core trick is judging with hindsight. You cannot score one decision from one outcome, because bad luck, sloppy follow-through, or a flaky environment can spoil even a wise choice.

Instead the method is: find two branches sharing the same starting stretch that split at one decision; look at what each branch actually achieved later (test results, research scores); label the fork with whichever branch turned out better; then at test time show a new model only the shared prefix plus two options — never the future — and ask it to pick the winner.

Building it took heavy filtering. The engineering pool held 2,677 graded runs across 517 coding tasks; the research pool held 1,132 runs across 47 AI research tasks. A generator proposed 4,657 candidate forks, but only 10.8% survived, leaving 390 engineering plus 112 research questions.

Two filters keep quality high. "Trivial" questions answerable without any trajectory are thrown out, and a question ships only when a panel of independent judges unanimously agrees with the label given the full record. Human spot-checks back this up: reviewers agreed with the mined labels 98.8% of the time.

Evaluation is strict about guessing and order bias. Each question is asked twice with the options swapped, and it counts as correct only if the model gets both orders right — so random guessing scores 25% and always picking the first option scores 0%.

The sharpest analysis sorts forks by how far away the deciding evidence sits, from already visible to much more work away. Scores collapse along that slope, and extra reasoning tokens do not rescue the far-horizon cases.

Finally, taste can be taught. A teacher allowed to see the right answer writes out reasoning; a small Qwen student imitates that reasoning without seeing the answer. On unseen tasks the student jumps from 30.0% to 47.9%, and as an adviser to a fixed coding agent it lifts end-to-end success from 14.6% to 33.7%.

## Where can this be used?

- Coding agents: choosing which fix, refactor, or library to commit to before burning hours.
- Research agents: picking which hypothesis, sweep, or repair to try first.
- Training: turning old trajectories into judgment exercises instead of hand-writing every test.
- Model selection: telling apart frontier models that look tied on end-to-end leaderboards.
- Agent design: pairing a small trained "adviser" with an executor, so the adviser steers each fork toward the promising branch.
- Debugging long runs: finding the exact step where a run went wrong rather than blaming the whole trajectory.
- Hiring and review: showing a new hire (human or agent) the fork without the ending, then comparing their pick with what actually worked.

Anywhere a wrong turn is costly and the evidence arrives late, this kind of taste test is worth running.

## Conclusions & takeaways

- Taste is real, narrow, and measurable: choosing the better direction before the outcome is visible.
- Old trajectories already contain the labels — their later outcomes grade their earlier forks.
- Current models have weak taste: under 60% on two-way choices, worst where evidence lies furthest ahead.
- Thinking longer is not the cure; the missing piece is judgment about futures not yet seen.
- Taste is trainable and transfers: distilled judgment improves quiz scores and real task success.
- Practical moral: log your agent runs — every detour and parallel attempt is future training data.

## Jargon decoder

| Term | What it means in plain language |
| ---- | ------------------------------- |
| Taste | Picking the direction that pays off later, not just acting well right now |
| Decision fork | A moment where the run could go two ways and one turns out better |
| Taste-Bench | The paper's 502-question quiz of such forks, with the future hidden |
| Hindsight label | The correct answer, decided by what each branch actually achieved later |
| Parallel attempts | Two runs of one task that start alike then split |
| Detour | One run goes wrong, hits an error, then backtracks and recovers |
| Reasoning budget | How much extra thinking (tokens) a model gets before answering |
| Distillation | A small model learning judgment by copying a teacher's reasoning |
| End-to-end benchmark | A test grading only final success, not the choices along the way |
| Time horizon | How far ahead the deciding clue sits — nearby clues are easy, distant ones are hard |
| Both-orders-correct | The strict rule that a question counts only if the model picks right with the options in either order |
