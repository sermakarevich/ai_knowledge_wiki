> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices — In Plain Language

## What is this about?

PracRepair is a system that automatically fixes software bugs using a large language model (LLM).

Think of it as a robot debugger: instead of just reading the broken code, it watches the program fail, asks itself questions about what went wrong, proposes a fix, tests it, and learns from the result.

Most earlier LLM repair tools only look at static clues — the source code, the error message, and whether tests pass or fail. PracRepair adds what human developers actually use: what happened while the program was running, and how each attempted fix changed its behavior.

In tests on the widely used Defects4J Java bug collections, it fixed 139 bugs (version 1.2) and 136 bugs (version 2.0) with GPT-3.5, and 162 / 171 with GPT-4o — more than previous tools, including many bugs no other tool fixed.

## Why does it matter?

Fixing bugs is one of the most expensive parts of software: developers spend roughly 35–50% of their time, and 50–75% of project budgets, on testing, verification, and debugging — over $100 billion a year.

Older automatic repair relied on hand-written fix patterns or narrow training datasets, so it broke down on new kinds of bugs. Newer LLM tools (ChatRepair, ThinkRepair, RepairAgent, ReInFix) do better, but they still mostly guess from the code text and a pass/fail signal.

That misses two things humans rely on:

1. **Failure dynamics** — which path the program actually took, what values variables held, and which branches went the wrong way when it crashed.
2. **Fix feedback** — exactly how a trial patch changed behavior, not just "it still fails."

Without these, models patch symptoms instead of causes, especially when a bug spans several functions or depends on values that evolve at runtime.

## How does it work?

PracRepair copies a human debugging routine in three stages, each aimed at one known difficulty.

**Stage 1: Gather evidence on demand.**

First it builds two kinds of context. Static context comes from parsing the project with Joern into a Code Property Graph — a map of classes, methods, calls, branches, and where each variable is defined and used. Dynamic context comes from running the failing test with lightweight bytecode instrumentation (JavaAgent/ASM) and recording, statement by statement, what ran, what each variable held, and which branches were taken.

Crucially, it does not dump all of this on the model at once — full traces are huge and noisy. Instead the model pulls what it needs through a small lookup interface (find a method, inspect a definition, trace a variable, replay the execution path, check values at one statement).

**Stage 2: Ask questions, then form a hypothesis.**

Instead of jumping to a patch, the model runs a diagnosis loop of up to 10 rounds, asking one focused question at a time:

- *What* happened? (What did variables do? Which branch misbehaved?)
- *Why* did it happen? (Which logic or dependency caused the bad state?)
- *How* should it be fixed? (What change restores the intended behavior?)

Each answer, with its evidence and implication, is saved. The history is then summarized into a four-part repair hypothesis: faulty behavior, supporting evidence, suspected root cause, and suggested change.

A concrete example: in the Compress-21 `writeBits` bug, a static-only guess masked the output value but still crashed with "Unknown property 128." The trace showed the real problem — bits were flushed too early — which the questions brought into focus.

**Stage 3: Try, test, and refine the fix.**

The hypothesis drives patch generation (a plain zero-shot prompt, no examples). Each candidate is compiled and run against the tests, with a 10-minute limit. A patch counts as plausible only if it compiles and passes every test.

Failures fall into four buckets — won't compile, crashes or times out, original test still fails, or old fix breaks a previously passing test. For each, PracRepair feeds back three things: the diagnostic message, the code diff, and the trace diff (what executed differently after the patch). That feedback re-enters diagnosis, and the hypothesis is updated for the next try, up to 3 refinement rounds.

In the example, the first retry removed the original error but caused "Badly terminated header"; the trace diff showed the final flush was now inconsistent, leading to the passing fix.

## Where can this be used?

- **Everyday Java bug fixing:** single-line, single-hunk, and single-function bugs across projects like Chart, Closure, Lang, Math, Mockito, and Time.
- **Hard multi-function bugs:** where cause and effect span several functions — PracRepair with GPT-4o fixed 27 such bugs on Defects4J V1.2 versus 22 for the only other multi-function tool.
- **New, unseen projects:** it held up on the RWB (Real-World Bugs) benchmark of post-training-cutoff commits, across GPT-4, GPT-3.5, DeepSeek, and Llama-3 models.
- **Cost-sensitive automation:** at about $0.04 per fixed bug on GPT-3.5 (versus $0.06–$0.42 for rivals) and $1.13 on GPT-4o (versus $1.45), it can slot into CI pipelines or IDE assistants without a large bill.
- **Beyond one language:** the paper's future work is extending the same recipe — traces plus questions plus refinement — to other languages and larger codebases.

## Conclusions & takeaways

- Watching the program run beats just reading it: removing execution traces alone dropped fixes from 139 to 120.
- Asking structured what/why/how questions beats free-form reasoning: full diagnosis reached 139 fixes versus 121 with generic tool use and 107 with one-shot reasoning.
- Learning from failed patches matters: refinement lifted fixes from 89 (no retries) to 139 (three rounds), with no gain after that — so three is the sweet spot.
- Every stage earns its keep: stripping all three stages left only 84 fixes, and adding each one back raised the count.
- The bottom line: debugging is not one clever guess but a loop of evidence, questions, and tested retries — and automating that loop is what makes PracRepair win.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Automated program repair (APR) | Software that writes a code fix for a bug by itself. |
| LLM | Large language model — an AI trained on text and code that can read, explain, and write programs. |
| Fault localization | Finding where the bug lives; "perfect" means the answer was handed to the tool. |
| Static context | Information from reading code without running it: structure, calls, data flow. |
| Dynamic / execution trace | A step-by-step recording of what the program actually did when run. |
| Code Property Graph (CPG) | A combined map of a program's syntax, control flow, and data dependencies. |
| Repair hypothesis | A written best guess: what broke, what proves it, what caused it, how to change it. |
| Plausible vs. correct patch | Plausible passes all tests; correct is also judged to truly match the intended fix. |
| Ablation study | Removing parts of a system one by one to see how much each part helps. |
| Defects4J / RWB | Standard collections of real Java bugs used to compare repair tools. |
