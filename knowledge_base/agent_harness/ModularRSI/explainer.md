> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement — In Plain Language

## What is this about?

ModularRSI is a method that lets an AI coding agent get better at its job by fixing its own machinery.

To unpack that: an AI agent is not just the big language model (LLM — the AI that writes text and code).
It also has a "harness" — the surrounding software that runs the loop: sending prompts to the model,
running terminal commands, reading output, managing memory, and deciding when the task is done.

Recursive Self-Improvement (RSI — a system rewriting parts of itself to perform better) here means
the harness rewrites its own code based on its past successes and failures.

ModularRSI does this in a careful, three-part way:

1. It learns from a separate practice set of 2,000 tasks (1,000 software-repair style, 1,000 terminal-use style)
   that never overlaps with the final tests, so it cannot just memorize the exam.
2. It compares successful and failed attempts at the *same* task to find the real cause of failure.
3. It splits the harness into five small parts (modules) and improves each part separately,
   then merges them back together.

The start point is a harness called Terminus-2, and the result is a frozen, improved harness
that is then tested on two hard benchmarks (standard test suites): TerminalBench 2.0 (89 long terminal tasks)
and SWE-Bench Verified (500 real-world software repair tasks).

## Why does it matter?

Older self-improvement methods had three big problems, and this paper tackles all three.

First, the cheating problem. Many methods practiced directly on the test set or on tasks taken from it.
Scores went up, but nobody could tell whether the agent had really improved
or had just memorized the specific test tasks.

Second, the blame problem. A task-level score only says "pass" or "fail."
It does not say *why* it failed. Was the harness broken, or did the model just make
a one-off bad guess on that task? Learning from a single run often baked in
a fix that only helped that one task and hurt everywhere else.

Third, the tangled-machine problem. Most harnesses were treated as one giant block of code.
Changing everything at once makes it hard to know which change helped,
and a fix in one area can easily break something in another area.

ModularRSI matters because it shows the harness can learn fixes that actually transfer:
they still help on brand-new tasks, in new subject areas, and even when plugged
into a different underlying AI model.

## How does it work?

Think of it like a sports coach reviewing game tapes in four steps.

**Step 1: Run and record.** The agent attempts practice tasks several times.
Every attempt (called a trajectory or rollout — the full step-by-step record of what the agent did)
is saved in a Trajectory Memory, along with its score.

**Step 2: Compare in groups.** A helper program, the Code-Modify Agent (an AI that reads the tapes
and edits harness code), sorts each task into one of three groups:

- *Contrastive group (mixed results):* some attempts passed, some failed.
  The agent pairs a pass with a fail on the same task and asks:
  "Where did these two runs diverge, and which harness part caused it?"
  Example: one run kept a filter that removed empty (NULL — missing) rows and passed with 47 rows;
  the other copied old code without the filter, got 52 rows with bad data, and failed.
- *Negative group (all failed):* it first looks in memory for an older success on the same task
  to compare against. If none exists, it diagnoses obvious faults directly:
  going in circles, using a tool wrongly, giving up too early, or declaring victory without checking.
  Example: the agent claimed a video-tool build was finished while a check showed
  only one of three required libraries was actually linked.
- *Positive group (all passed):* everything worked, so it hunts for wasted effort:
  repeated commands, needless exploration, or clumsy tool calls.
  Example: a file-writing helper kept failing on multi-line code and falling back to slow shell retries,
  turning a quick fix into 40+ steps.

Each diagnosis is written as a structured note (a JSON record — a machine-readable form
with fields like which module is suspected, what the evidence is, and what change is proposed).

**Step 3: Vote and edit one module at a time.** Similar notes about the same function are merged,
and each candidate fix gets votes based on how many *different* tasks support it.
Fixes backed by many tasks win; one-task-only fixes are ignored.
The five modules — Agent Loop (the main coordinator), Tool Use (turning model text into commands),
Observation Management (turning raw terminal output into readable feedback),
Context Management (managing conversation memory and summaries),
and Task Completion Detection (deciding when to stop) — are each evolved separately,
so edits in one module cannot silently tangle another.

**Step 4: Safety gates, then merge.** Every proposed edit must pass three checks:
a Program Check (does the code still run and follow the rules?),
a Diff Review (is this a general fix or a sneaky task-specific cheat?),
and Execution Validation (does it still work on two random sample tasks?).
Failures are rolled back. Finally, one integration round merges the five improved modules,
removes duplicates, and settles conflicts. The finished harness is then frozen —
no more changes allowed during final testing.

A side detail: medium-difficulty practice tasks teach the most.
Easy tasks never fail (nothing to compare), and brutally hard tasks never succeed (nothing to copy).
A practice mix centered on medium difficulty beat a hard-plus-easy mix by 2.2 points on SWE-Bench Verified.

## Where can this be used?

Anywhere an AI agent repeatedly uses tools in a terminal or a code repository:

- Coding assistants that build, test, and repair large software projects.
- Terminal agents (also called CLI agents — assistants operated through a text-command window)
  that install software, process data, manage systems, or configure networks.
- Teams that maintain agent platforms: the five-module split gives them five clear places
  to inspect, test, and upgrade instead of one opaque block.
- Training pipelines where practice data must stay strictly separate from evaluation data,
  for example to prove an improvement is real and not memorization.
- Efficiency work: the Observation Management upgrades cut average steps sharply (about 35 down to 22 steps
  in one test), which means lower cost and faster answers.
- Reliability work: the share of tasks solved on *all three* tries rose (30.3 to 36.0 on TerminalBench 2.0),
  which matters when you need the agent to succeed consistently, not just occasionally.

## Conclusions & takeaways

- Practicing on separate data, comparing pass-vs-fail pairs, and fixing small modules separately
  beats practicing on the test and rewriting the whole machine at once.
- Numbers: TerminalBench accuracy 47.6 to 52.4; SWE-Bench Verified 73.4 to 76.5.
  Skills crossed domains (terminal practice helped coding tests and vice versa)
  and crossed models (a harness trained with one DeepSeek model still helped other models).
- Modular plus integration won clearly (52.4) over editing everything jointly (44.2)
  or as one block (46.4), which actually scored *below* the starting point.
- Against two earlier self-improvement methods under the same fair (no-memorization) rules,
  both rivals barely moved (+1 point) while ModularRSI gained about +5.6 points.
- Real fixes were concrete and reusable: a checklist that keeps task requirements in view,
  a finish-line guard that re-checks acceptance conditions before quitting,
  and a sturdier file-writing tool that cut wasted retries from ~36 steps to ~25.
- Limits the authors admit: no isolated on/off test of just the comparison step,
  and only a subset of the 2,000 practice tasks was used because full runs are expensive.
  Larger-scale confirmation is left for future work.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Harness | The support software around the AI model that runs the work loop: prompting, tools, memory, and stopping. |
| Recursive Self-Improvement (RSI) | A system improving itself by rewriting its own code from experience, then running on the improved version. |
| Benchmark-disjoint | The practice tasks and the final test tasks never overlap, so good scores prove real learning, not memorization. |
| Trajectory (rollout) | The full step-by-step recording of one attempt at a task: actions, tool outputs, and final result. |
| Contrastive analysis | Comparing a success and a failure on the same task to spot the exact behavior that made the difference. |
| Module | One of five labeled parts of the harness (Agent Loop, Tool Use, Observation Management, Context Management, Task Completion Detection) improved independently. |
| Trajectory Memory | A saved library of past attempts and scores, reused later when a fresh comparison needs an old success. |
| Validation gates | Three safety checks (code runs, fix is general, still works on samples) that every edit must pass or be undone. |
| Cross-module integration | A final merge round that combines the five separately improved parts and fixes conflicts between them. |
| Pass@3 / Pass3 | Two consistency scores over three tries: Pass@3 means at least one try passed; Pass3 means all three passed. |
