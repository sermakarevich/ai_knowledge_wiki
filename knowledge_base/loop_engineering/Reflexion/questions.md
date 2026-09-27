---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# Reflexion — Retrieval Practice

## Section 1: Intro, related work, Reflexion method

### Q1 (core recall): What are the three Reflexion LLMs, how is memory split and bounded, and what headline gains are claimed?

<details>
<summary>Answer</summary>

Actor M_a generates text/actions from policy pi_theta(a_i|s_i) with theta = {M_a, mem}; Evaluator M_e scores trajectories tau; Self-Reflection M_sr turns sparse rewards plus trajectory plus memory into stored verbal summaries sr_t. Memory is split into short-term trajectory history tau_t = [a_0, o_0, ..., a_i, o_i] and long-term stored reflections, with long-term memory bounded to Omega = 1-3 experiences to fit context limits; the loop runs until M_e passes or t reaches max trials. Headline claims: 91% pass@1 on HumanEval (vs 80% previous SOTA GPT-4), +22% absolute on AlfWorld in 12 trials, +20% on HotPotQA, up to +11% on HumanEval Python.

</details>

### Q2 (elaboration): Why does Reflexion use verbal reinforcement with episodic memory instead of scalar-reward weight updates — what breaks if you remove the reflection memory?

<details>
<summary>Answer</summary>

Scalar rewards say pass/fail but not what to change; verbal reflections give nuanced, actionable, interpretable hints stored as episodic memory and reused as context, with no LLM fine-tuning. Without persisting reflection memory (the gap vs Self-Refine and beam search, which lack it), the agent repeats the same failure — like ReAct-only stalling between trials 6 and 7. The limitation: it relies on LLM self-evaluation with no formal success guarantee.

</details>

## Section 2: Experiments across decision/reasoning/programming

### Q3 (core recall): What AlfWorld and HotPotQA numbers show Reflexion learning across trials?

<details>
<summary>Answer</summary>

AlfWorld over 134 tasks: ReAct + Reflexion solves 130/134 with a simple heuristic evaluator, keeps learning across 12 consecutive trials while ReAct-only stalls between trials 6 and 7 and converges at a 22% hallucination rate. Setup: ReAct actor, memory truncated to last 3 reflections, 2 domain few-shot trajectories; self-reflection triggers when the same action plus same response repeats for more than 3 cycles or actions exceed 30. HotPotQA on 100 questions: baselines with temperature 0.7 never solve any first-trial failure later, while Reflexion CoT with ground-truth context fixes enough of the 39% initially wrong to gain 14%, including an 8% absolute boost over episodic-memory-only.

</details>

### Q4 (core recall): What programming scores, test-quality numbers, and ablation numbers bound Reflexion's code gains?

<details>
<summary>Answer</summary>

Programming: up to 6 self-written unit tests per problem via Chain-of-Thought filtered by AST validity, max memory of 1 experience, pass@1 metric. Scores: HumanEval PY 91.0 (vs 80.1 GPT-4), HumanEval RS 68.0, MBPP RS 75.4, LeetcodeHard PY 15.0 vs 7.5, but trails GPT-4 on MBPP PY 77.1 vs 80.1. Gap explained by flaky internal tests: false-positive rate P(fail | tests pass) 16.3% MBPP Python vs 1.4% HumanEval Python despite similar ~80-82% baselines; false negatives preferred since the agent can reflect and keep correct code. Ablation on 50 hardest HumanEval Rust: 0.60 baseline, 0.52 test-generation omitted (forced harmful edits, no early stop), 0.60 self-reflection omitted, 0.68 full Reflexion; StarChat-Beta no gain (0.26 vs 0.26), so self-correction is emergent in stronger models.

</details>

## Section 3: Appendices C-D and extra evals

### Q5 (elaboration): Why does Reflexion fix the AlfWorld mug and HotPotQA cast errors in Trial #2 yet fail on WebShop — what breaks if the task needs diverse exploration?

<details>
<summary>Answer</summary>

The mug trial fails in Trial #1 by wandering drawers/desks and using the desklamp remotely with no effect, then succeeds in Trial #2 with a concise 3-step trace after reflecting to find the lamp first; HotPotQA fails Trial #1 by answering Rene Artois (Gorden Kaye) instead of intersecting the Grown-Ups cast, then succeeds Trial #2 by searching Sam Kelly and answering Captain Hans Geering. Both are local fixes within the same search neighborhood. WebShop on 100 shopping tasks shows no improvement after four trials with unhelpful reflections and early termination, because e-commerce search ambiguity punishes imprecise queries while AlfWorld exposes permissible actions and Wikipedia search tolerates them. If the optimum needs highly diverse exploration, Reflexion cannot escape the local minimum.

</details>

### Q6 (transfer): You are building a coding assistant that keeps breaking correct code on flaky self-written tests. How would you apply the Reflexion appendix lessons?

<details>
<summary>Answer</summary>

Apply the MBPP-vs-HumanEval and ablation lessons: prefer false negatives over false positives — require strict function-body-only output (4-space indented first line, no signature, as in the minSubArraySum O(n^2) example conditioned on previous code + test results + reflection), filter self-written tests by AST validity and cap at ~6, keep max memory of 1 experience, and add an early-stop so missing tests do not force harmful edits (ablation dropped 0.60 to 0.52 without tests). Log the self-reflection so a human can see whether the edit was test-driven or genuine, and only deploy self-correction on a strong enough model since weak models like StarChat-Beta show zero gain.

</details>

## Section 4: Evaluation (see [[critical_thinking]])

### Q7 (evaluation): The paper reports 91% pass@1 on HumanEval Python by comparing multi-trial Reflexion against a single-shot GPT-4 baseline, and it never reports cost or variance across the ablations. Why does this matter, and what would you want to see before trusting the 91% number as a fair comparison?

<details>
<summary>Answer</summary>

The 91% vs 80% comparison confounds "verbal reflection helps" with "multiple retries with test feedback beats one attempt" — the paper's ablation isolating self-reflection from test-generation is only run on a 50-problem HumanEval Rust subset, not on the flagship Python number, so it is unclear how much of the headline gain is reflection-specific. Combined with the complete absence of cost (token/dollar/latency for up to 12 trials across three separate LLM calls per trial) and variance reporting (no confidence intervals despite temperature-0.7 sampling), a fair comparison would need: the ablation repeated on the actual HumanEval Python set, a cost-matched baseline (e.g., GPT-4 given the same total inference budget as Reflexion's multi-trial loop), and repeated runs with reported variance. See [[critical_thinking|Critical Analysis]] for the full claims-vs-evidence breakdown.

</details>
