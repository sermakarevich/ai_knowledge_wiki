> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Coding Agents are Strong Prompt Optimizers — In Plain Language

Think of an AI agent as a new employee and the system prompt as its handbook.
This paper asks: what is the cheapest, most reliable way to write a better handbook?

## What is this about?

Most methods for improving prompts work like trial and error.
You rewrite the handbook, send the employee out on new jobs,
check the scores, and keep only the edits that help.
Each round needs fresh practice jobs and a grading step, so it gets expensive fast.

This paper proposes a different recipe called CASD (Coding-Agent Skill Distillation).
Instead of running new trials, you hand an ordinary, unmodified coding agent
a folder of past job logs — a frozen collection of old trajectories —
plus one short instruction: "study these logs and write a handbook
of behavioral rules for future agents."

The coding agent does the rest on its own: it explores the log folder,
writes small programs to count what went wrong and how often,
reads the most informative episodes, and produces a short handbook file.
That file is used directly as the new system prompt. No new practice runs,
no grading gate, no second round. One pass, about $1.60.

The headline result: across four agent benchmarks (household tasks,
two customer-service tasks, spreadsheet tasks), this single cheap pass
beat the leading trial-and-error optimizers on three of four tests.

## Why does it matter?

Three reasons: better results, much lower cost, and wider applicability.

First, results. Under identical data access, the distilled handbooks lifted
accuracy by 16.6 percentage points on average, versus 10.9 for the best
search-based rival (GEPA) and 5.3 for a validation-gated search method (SkillOpt).
Even when the rivals were given extra validation data and unlimited practice runs
that CASD never got, CASD still won on two of four benchmarks.

Second, cost. One distillation pass costs roughly $1.60 — about 22 times cheaper
than the validation-gated search over the same four benchmarks.
The old logs are treated as a free byproduct of work already done,
so there is no new trial bill at all.

Third, reach. Because CASD never touches a live environment or simulator,
it works in places where trial-and-error methods cannot run at all —
where no simulator, grader, or spare validation data exists.

## How does it work?

The process has three stages, all performed by the stock coding agent
in a single session of roughly 16–51 tool calls (about 34 on average).

Step 1 — Look around. The agent first explores the log folder layout:
what files exist, what each episode records (messages, tool calls, outputs, scores).
About a third of its effort happens in the first fifth of the session.

Step 2 — Count, then read. The agent writes and runs analysis code
over the whole log collection: pass rates overall and per task category,
tool-use histograms, duplicated calls, early exits, invented arguments.
These whole-collection statistics point it at the most informative episodes,
and it flips back and forth between counting and reading (typically ~5 times).
Every studied run computed scores and episode lengths; nearly all also
tabulated failure modes and tool usage.

Step 3 — Write the handbook. At the end of the session the agent writes
a compact 5–8 KB handbook of behavioral rules, backed by measured evidence
such as "16 of 50 episodes invented an identity-lookup argument"
or "123 of 284 detail lookups were exact duplicates."
The studied handbooks averaged 4.6 such numeric citations per thousand words,
versus essentially zero in rival prompts.

The paper's theory frames this as a variance-versus-bias tradeoff.
Trial-and-error methods learn from small random samples each round,
so their feedback is noisy and they need many rounds to average it out.
CASD reads the entire log collection at once with exact counts,
so its feedback is stable and cheap — but it can only learn what the old logs
actually contain. When practice runs are scarce, stability wins;
when unlimited fresh practice is available, the trial-and-error approach
is expected to catch up.

## Where can this be used?

Anywhere you already have logs of an agent doing a repeated task family:

- Customer-support agents: turn past chat-and-tool transcripts into rules
  like "always verify identity with this exact call before touching billing."
- Data-wrangling and spreadsheet agents: distill frequent formatting,
  formula, and copy-paste mistakes into a checklist the agent follows.
- Household and navigation agents: convert repeated dead ends
  (wrong rooms, skipped steps) into search-order and double-check rules.
- Cutting inference bills: a distilled handbook given to a fast,
  non-reasoning model recovered most or all of the accuracy gap
  to a slower reasoning model — over 100% on two benchmarks, 78% and 55%
  on the other two — while using 3–4x fewer tokens per task.
- Teams with no simulator: anywhere fresh practice runs are impossible
  or costly, the frozen-log approach still applies.

The requirement is modest: a log collection with enough failures to learn from.
Very small or failure-free logs leave nothing to distill.

## Conclusions & takeaways

- An off-the-shelf coding agent, pointed at frozen logs with a one-paragraph
  instruction, is a strong prompt optimizer — no custom pipeline needed.
- Whole-collection counting beats small-sample anecdotes: frequencies,
  cross-episode duplicates, and even behaviors that never happened
  (like a payment call nobody ever made) become visible only at full scope.
- Skipping the accept-or-reject grading gate avoids overfitting to tiny
  validation sets — a concrete failure mode that sank a rival to below baseline.
- Much of what slow step-by-step reasoning re-derives every episode is
  reusable policy that can be written down once, offline, into a handbook.
- The distilled handbook does not need expensive reasoning traces to learn from;
  plain failure-rich logs work just as well.
- Limits: the handbook inherits the logs (blind to unlogged behaviors),
  some instance-specific deduction resists any static handbook,
  and results were shown with one target model and one distiller agent.
- Practical rule of thumb: use offline distillation as the cheap default first step;
  reserve expensive trial-and-error search for final gains when fresh practice is cheap.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| System prompt | The handbook text an agent reads before starting work |
| Trajectory / rollout | The full log of one attempt: messages, tool calls, and outcome |
| Prompt optimizer | Any method that rewrites the handbook to raise future scores |
| Search-based optimizer | A method that tries handbook edits one by one and keeps winners |
| Validation gate | A grading step that accepts an edit only if fresh practice scores rise |
| CASD | The paper's method: one offline study of old logs, then a handbook |
| Skill file | The short handbook document the coding agent writes |
| Reflection scope | How much log history the optimizer looks at before rewriting |
| Minibatch reflection | Judging from a small random sample of episodes per round |
| Corpus-scale reflection | Counting patterns across the entire log collection with code |
| Reasoning gap | The accuracy difference between slow thinking and fast answering |
| Bias vs. variance (here) | Stable-but-limited-by-old-logs versus noisy-but-eventually-thorough |
