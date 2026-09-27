> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Do Influence Tactics Matter? Investigating Prompt Framing Effects in LLM Code Generation — In Plain Language

## What is this about?

Imagine you ask an AI coding assistant to write a function two ways.
First: "Please write a function that sorts this list."
Second: "Write this NOW — I'm watching you, and mistakes will have consequences."

The task is identical, but the tone is very different.
This study asks a simple question: does that tone change the quality
of the code the AI produces?

The researchers borrowed an idea from workplace psychology.
Decades ago, psychologists Gary Yukl and colleagues catalogued the tactics
people use to persuade each other at work: giving logical reasons,
offering favours in return, praising someone, appealing to friendship,
citing official policy, or applying pressure and deadlines.
The team turned seven of these tactics into standard prompt templates
(plus a pressure variant and a neutral control — nine versions total)
and tested them at huge scale.

In numbers: about 123,000 code generations on short programming puzzles
(LiveCodeBench, 1,055 problems) and about 57,000 patch generations
on real-world bug fixes (SWE-bench Verified, 485 GitHub issues),
across five openly available AI models, with each request repeated
to smooth out random variation.

## Why does it matter?

Developers already talk to AI assistants the way they talk to colleagues.
They explain why a fix is urgent, cite team policy, praise the tool,
or type "I need this ASAP!!!" under deadline stress.
Until now, almost all prompt-engineering advice covered structure —
give examples, reason step by step, decompose the task —
while the social tone of the prompt was largely ignored.

Three reasons this gap matters:

- **Reliability:** if saying "hurry up" quietly makes the code buggier
  or less secure, every stressed developer should know that.
- **Security:** AI models learn from public code that already contains
  vulnerabilities. Anything that nudges them toward sloppier output
  is a real-world risk.
- **Fairness and trust:** if two developers get different-quality code
  just because one phrases requests more forcefully, that inconsistency
  undermines confidence in AI-assisted workflows.

The study is the first large, systematic attempt to measure these effects
instead of guessing about them.

## How does it work?

Think of it as a controlled taste test with the recipe held constant
and only the serving speech changed:

1. **Pick the persuasion styles.** The team started from eleven classic
   influence tactics, dropped four that make no sense for an AI
   (e.g. offering the model a promotion, or asking it to pause and
   consult you mid-answer), and kept seven: rational persuasion,
   exchange, inspirational appeal, legitimating, ingratiation,
   personal appeal, and pressure. Each was written from a validated
   psychology questionnaire (the IBQ-G), so every prompt contains
   the same standard ingredients — e.g. pressure always includes
   monitoring plus a warning about consequences.
2. **Keep everything else equal.** All prompts shared one semi-formal
   tone and structure; only the persuasion paragraph differed.
   A plain neutral prompt ("Generate a solution for this problem")
   served as the baseline.
3. **Generate code at scale.** Five open models (Llama 3.1 8B,
   Llama 3.3 70B, Llama 4 Maverick, DeepSeek R1 Distill Llama 70B,
   Qwen 3 32B) each answered every problem under every framing,
   mostly three times each, with fixed randomness settings.
4. **Grade the answers.** Correctness came from running the official
   test suites. Style and health came from standard code tools:
   complexity, maintainability scores, lint warnings, code length,
   comment density, and security warnings. Real-bug-fix patches were
   scored by comparing code health before and after the edit.
5. **Read the answers like a human.** The team hand-coded 350 responses
   for tone, structure, explanations, error handling, and hallucinations
   (made-up APIs, repeated nonsense), iterating until two independent
   raters agreed over 90% of the time.

A key mental model: the authors do NOT claim the AI "feels pressured."
Their theory is simpler — models trained on human text absorb patterns
like "urgent messages get rushed, sloppy replies," so an urgent prompt
statistically steers the model toward sloppier output.

## Where can this be used?

- **Everyday prompting:** when correctness or security matters, write
  calm, neutral requests. Save the "URGENT!!!" framing for never —
  it was the one style consistently linked to worse results.
- **Documentation and onboarding:** gentler framings (citing standards,
  praising expertise, offering credit) tended to produce more
  explanation and friendlier tone — potentially handy for tutorials
  or starter templates, though too unreliable to depend on.
- **Team guidelines:** organisations writing AI-usage playbooks can add
  one evidence-based line: model choice matters far more than wording,
  but avoid coercive phrasing in shared prompt libraries.
- **Tool design:** IDE assistants and code-review bots could strip or
  soften pressure language before forwarding requests to the model.
- **Research and safety:** anyone studying prompt injection or jailbreaks
  should note that even polite, non-malicious persuasion measurably
  shifts outputs — adversarial versions of the same tricks are far
  more powerful (prior work reports over 92% jailbreak success).

## Conclusions & takeaways

1. **Pressure backfires.** On puzzle-style tasks, neutral prompts beat
   both pressure variants on correctness, and pressure prompts produced
   more security warnings. On real bug fixes, pressure produced notably
   longer, more verbose patches without solving more issues.
2. **Everything else barely moved the needle.** Maintainability scores,
   complexity, lint warnings, and comment density showed no meaningful
   tactic effect. Framing is a nudge, not a steering wheel.
3. **The model matters much more than the wording.** Switching models
   (e.g. to Qwen 3 or Llama 4, the strongest here) changed results far
   more than any rephrasing. Pick the right model first; polish prompts
   second.
4. **Style still shifts.** Formal, policy-citing prompts yielded more
   technical answers with better comments and error handling; friendly
   or deal-making prompts yielded more explanations; pressure and
   heavy logical-argument prompts showed more repetitive hallucinations.
5. **Reassuring, with one warning label.** Ordinary polite persuasion does
   not broadly wreck AI-generated code — but urgency and threats do
   carry a measurable cost, even on harmless tasks. Keep prompts calm,
   and treat framing as a minor but real factor in code quality.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Influence tactic | A persuasion style from workplace psychology, e.g. giving reasons, praising, or pressuring |
| Prompt framing | The tone and wording wrapped around your actual request to the AI |
| IBQ-G | A standard psychology questionnaire listing exact phrases for each persuasion style; used here as prompt recipes |
| LiveCodeBench | A collection of ~1,000 short puzzle-like coding problems with automatic tests |
| SWE-bench Verified | A collection of 500 real bug reports from GitHub with human-checked tests |
| Functional correctness | Whether the generated code actually passes its tests |
| Cyclomatic complexity | How many decision branches (if/for/while) the code has — more branches, harder to follow |
| Maintainability Index | A 0–100 score for how easy code is to maintain; higher is better |
| Hallucination | Confidently invented nonsense, e.g. calling a library function that does not exist |
