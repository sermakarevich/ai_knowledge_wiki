> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Reflexion: Language Agents with Verbal Reinforcement Learning — In Plain Language

## What is this about?

Imagine a student who never rewrites their brain after a failed exam — instead, they write a short sticky note to themselves: "Next time, check the lamp first before wandering around the room." Then they keep just one to three of these notes in their pocket and re-read them before the next try. That is Reflexion in a nutshell.

In technical terms, Reflexion is a way to make AI language agents improve over several attempts without retraining them (without updating their internal weights). Instead of a numeric score alone, the agent writes down a verbal self-reflection about what went wrong, stores it in a small memory, and uses it as extra context on the next attempt.

The big claim: this simple loop of try, judge, reflect, and retry gives large gains on decision-making tasks, question-answering with reasoning, and writing code — all without expensive fine-tuning.
It does this over a handful of trials (for example, up to about 12 in the household tasks), reusing only the most recent notes each time.

## Why does it matter?

- It is lightweight: no retraining or fine-tuning of the large language model (LLM, the big AI text engine) is needed. Improvement comes from words stored as memory, not from changing the model's weights (its internal settings).
- It gives richer feedback than traditional reinforcement learning (RL, learning from numeric rewards): instead of just "you got 0 points," the agent gets actionable hints like "you searched too narrowly" or "you wasted steps."
- The memory is explicit and readable: humans can read the stored reflections, unlike hidden numeric updates.
- The reported gains are large: 91% pass@1 (solving the task on the first submitted answer) on HumanEval Python coding problems versus 80% for the previous best GPT-4 result, +22% absolute on AlfWorld household decision tasks over 12 trials, and +20% on HotPotQA reasoning questions.
- It separates judging from doing: one component acts, another evaluates the result, and a third reflects — so even a simple pass/fail signal can be turned into useful verbal advice.

## How does it work?

1. **Act.** The Actor model (the "doer") tries the task: it moves around a simulated house, searches Wikipedia, or writes a piece of code. Its full trace of actions and observations is called the trajectory.
2. **Evaluate.** The Evaluator model (the "judge") scores that attempt — for example, success or failure, or whether the code passes tests. In some tasks this is a simple heuristic rule; in others it uses self-written tests or ground-truth checks.
3. **Reflect.** The Self-Reflection model (the "coach") looks at the failure, the trajectory, and past reflections, and writes a short verbal summary: what went wrong and what to try next time.
4. **Remember (a little).** That reflection is saved in long-term episodic memory (a small notebook of past lessons), while the raw trajectory is short-term memory. Only the last 1–3 reflections are kept, so they fit inside the model's context window (the limited amount of text it can read at once).
5. **Retry with memory.** On the next trial, the Actor sees the past reflections as extra context and tries again. The loop repeats until the Evaluator passes the answer or a maximum number of trials is reached.
6. **Coding bonus step.** For programming tasks, the agent first writes up to 6 of its own unit tests (small checks) per problem, filtered for basic validity, then debugs against them. For decision tasks like AlfWorld, reflection triggers when the agent repeats the same action with the same result more than 3 times or exceeds about 30 steps.
7. **What the ablations show.** On the hardest HumanEval Rust problems, removing test generation hurts (score drops from 0.60 to 0.52 because the agent makes harmful edits with no early stop), removing self-reflection gives no gain (0.60), and full Reflexion reaches 0.68. Self-reflection adds about 8% over plain memory replay on HotPotQA.

## Where can this be used?

- **Household and sequential decision tasks (AlfWorld):** navigating rooms, finding objects like a mug and a desklamp, and using them correctly. Reflexion solved 130 out of 134 tasks and kept improving across 12 trials, while the non-reflecting baseline stalled early and kept hallucinating (making up invalid actions) about 22% of the time.
- **Multi-step question answering (HotPotQA):** searching Wikipedia and combining facts. Baselines that failed the first attempt never recovered in later tries, while Reflexion fixed enough of the 39% initially wrong answers to gain about 14% overall.
- **Writing code (HumanEval, MBPP, LeetCode):** generating Python and Rust functions. Reported bests include HumanEval Python 91.0, HumanEval Rust 68.0, MBPP Rust 75.4, and hard LeetCode Python 15.0 versus 7.5 — though it trailed GPT-4 on MBPP Python (77.1 vs 80.1).
- **Anywhere binary feedback exists:** the framework accepts varied feedback types (simple scores or free-form language) from outside or self-generated, so any task with a pass/fail check plus room for verbal diagnosis is a candidate.

## Conclusions & takeaways

- Verbal self-reflection stored in a tiny sliding memory can turn failures into wins across very different tasks — without retraining the model.
- Test quality sets the ceiling for code: the MBPP Python shortfall is attributed to flaky self-written tests (about 16.3% false positives, meaning tests pass but the code is actually wrong, versus only 1.4% on HumanEval Python), not to weaker reasoning.
- Self-correction seems to need a strong enough model: a smaller model (StarChat-Beta) showed no gain (0.26 vs 0.26), suggesting the ability to reflect usefully emerges with capability.
- Honest limits: there is no formal guarantee of success since it relies on the model's own judgment; it can get stuck when a task needs wildly creative exploration. On WebShop shopping tasks (100 tasks, 4 trials), it showed no improvement and reflections were unhelpful, because ambiguous shop search punishes imprecise queries while house and Wikipedia tasks tolerate them.
- Bottom line: a cheap, readable "sticky-note" memory is a surprisingly strong substitute for retraining — as long as the task gives clear feedback and the model is strong enough to judge itself.
- Two concrete illustrations from the digest: an AlfWorld agent that wandered drawers in Trial 1 and then succeeded in 3 steps in Trial 2, and a HotPotQA agent that answered from one show's cast first and then intersected both casts correctly.
- Full code is published alongside the work, with figures showing the AlfWorld correction, the flat WebShop curve, and a two-trial HotPotQA search fix.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Verbal reinforcement | Improving through written advice instead of numeric scores or retraining |
| Actor | The part of the system that acts: moves, searches, or writes code |
| Evaluator | The judge that scores an attempt as pass or fail |
| Self-reflection | A short written note on what failed and what to try next |
| Episodic memory | The small notebook of past reflections reused on the next try |
| Trajectory | The full step-by-step record of one attempt |
| Pass@1 | Share of problems solved on the first submitted answer |
| Fine-tuning | Retraining a model's internal weights; Reflexion avoids this |
