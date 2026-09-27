# Reflexion: Language Agents with Verbal Reinforcement Learning

**Paper:** [Reflexion: Language Agents with Verbal Reinforcement Learning (Shinn et al., 2023)](https://arxiv.org/abs/2303.11366)

## Human Readable TL;DR

Imagine a student who never rewrites their brain after a failed exam — instead they stick a small note on the fridge ("check the lamp first, then grab the mug") and read it before trying again. Reflexion gives computer helpers the same trick: after each failed attempt, the helper writes itself a short note about what went wrong, keeps the last few notes in a tiny notebook, and rereads them before the next try. Nothing inside the helper gets rebuilt or rewired — it just gets better instructions from its own past mistakes. With only a few rounds of notes, it goes from wandering around the room to solving the task almost every time.

## TL;DR

Reflexion reinforces language agents through linguistic feedback instead of weight updates: an Actor generates a trajectory, an Evaluator scores it, and a Self-Reflection model converts the sparse reward plus trajectory into a verbal summary stored in a bounded episodic memory (usually 1–3 experiences) that is replayed as context on the next trial. It accepts scalar or free-form feedback from external or self-simulated sources and needs no fine-tuning. Across benchmarks it lifts AlfWorld decision-making to 130/134 tasks (+22% absolute over ReAct in 12 trials), HotPotQA reasoning by +20% (+14% on reasoning-only CoT with ground-truth context), and HumanEval Python coding to 91% pass@1 versus 80% prior GPT-4 SOTA. Ablations show self-reflection — not episodic memory alone — drives the hard-task gains, and the method stalls when tasks demand highly diverse exploration (WebShop) or the base model is too weak to self-correct (StarChat-Beta).

---

## Problem & Motivation

Large language models increasingly act as goal-driven agents that play text games, call tools and APIs, write code with compilers, and search the web — but teaching them from trial and error with traditional reinforcement learning needs huge numbers of samples plus expensive, slow fine-tuning of massive weights.

Existing prompt-level tricks fall short: single-generation refiners (Self-Refine, prompt-optimization) do not keep a persisting memory across trials; search-based deciders (beam search, multi-generation voters) lack reflective memory; coding helpers (AlphaCode, CodeT, Self-Debugging, CodeRL) either need hidden ground-truth tests (invalidating pass@1) or have no self-learning reflection step bridging error identification to improvement.

Reflexion matters because it offers a lightweight, interpretable alternative: turn binary or scalar environment feedback into an explicit verbal "semantic gradient" — a concrete, human-readable lesson stored in episodic memory and reused as context — so the same frozen model improves rapidly over a handful of trials on decision-making, reasoning, and programming tasks.

---

## Main Original Ideas

1. **Verbal reinforcement paradigm** — The policy is parameterized as theta = {M_a, mem}: the frozen Actor LLM plus an explicit memory of verbal reflections, not updated weights. After each trial the sparse reward and trajectory are amplified into a natural-language summary that acts as a semantic gradient pointing to what to do differently next episode.

2. **Actor–Evaluator–Self-Reflection loop** — Three LLM roles run Algorithm 1 (Figure 2): the Actor samples actions from pi_theta(a_i|s_i) conditioned on observations and memory; the Evaluator scores trajectories via exact match (reasoning), hand-written heuristics (decision-making), or another LLM instance (decision-making, programming); the Self-Reflection model generates the stored lesson sr_t. The loop repeats until the Evaluator passes or max trials are reached.

3. **Split short-term / long-term memory with sliding window** — Short-term memory is the fine-grained trajectory history tau_t = [a_0, o_0, ..., a_i, o_i]; long-term memory is the distilled reflection list mem = [sr_0, ..., sr_t], bounded to Omega = 1–3 experiences (3 for AlfWorld/HotPotQA, 1 for programming) to respect context limits. Both condition the Actor, giving it lesson-shaped context no prior action-choice work provides.

4. **Flexible feedback amplification including self-generated tests** — Three failure-signal routes are unified: plain binary environment feedback, pre-defined heuristics for common failures (e.g. same action plus same response for >3 cycles, or >30 actions in AlfWorld), and LLM self-evaluation such as binary classification or self-written unit tests. For code, Chain-of-Thought proposes diverse tests filtered by abstract syntax tree (AST) validity and capped at 6 per problem, enabling grounded pass@1 reporting without hidden tests.

5. **LeetcodeHardGym benchmark and cross-domain empirical study** — A new interactive gym of 40 hard-level Leetcode questions (post GPT-4 cutoff, October 8 2022) across 19 programming languages via the MultiPL-E compiler, plus a systematic study of emergent self-reflection over a few trials across decision (AlfWorld), reasoning (HotPotQA), and coding (HumanEval, MBPP, LeetcodeHard) domains.

---

## Key Findings

| Benchmark + Language | Prev SOTA Pass@1 | SOTA Pass@1 (GPT-4) | Reflexion Pass@1 |
|---|---|---|---|
| HumanEval (PY) | 65.8 (CodeT + GPT-3.5) | 80.1 | 91.0 |
| HumanEval (RS) | — | 60.0 | 68.0 |
| MBPP (PY) | 67.7 (CodeT + Codex) | 80.1 | 77.1 |
| MBPP (RS) | — | 70.9 | 75.4 |
| Leetcode Hard (PY) | — | 7.5 | 15.0 |

| Benchmark + Language | Base | Reflexion | TP | FN | FP | TN |
|---|---|---|---|---|---|---|
| HumanEval (PY) | 0.80 | 0.91 | 0.99 | 0.40 | 0.01 | 0.60 |
| MBPP (PY) | 0.80 | 0.77 | 0.84 | 0.59 | 0.16 | 0.41 |
| HumanEval (RS) | 0.60 | 0.68 | 0.87 | 0.37 | 0.13 | 0.63 |
| MBPP (RS) | 0.71 | 0.75 | 0.84 | 0.51 | 0.16 | 0.49 |

| Approach (50 hardest HumanEval Rust) | Test Generation | Self-reflection | Pass@1 |
|---|---|---|---|
| Base model | False | False | 0.60 |
| Test generation omission | False | True | 0.52 |
| Self-reflection omission | True | False | 0.60 |
| Reflexion (full) | True | True | 0.68 |

- **AlfWorld sequential decision-making (134 tasks, ReAct actor, 2 few-shot trajectories):** ReAct + Reflexion with a simple heuristic evaluator solves 130/134, keeps learning across 12 trials while ReAct-only stalls between trials 6–7 and converges at a 22% hallucination rate. Typical baseline failure (thinking it holds an item it does not, then wandering without backtracking) is distilled into short hints that eliminate almost all such cases; early-mistake identification and multi-trial room search are the two main ways memory helps.
- **HotPotQA reasoning (100 questions, CoT and ReAct):** temperature-0.7 baselines never solve any first-trial failure in later trials, while Reflexion CoT with ground-truth context fixes enough of the 39% initially wrong to gain +14%. Self-reflection adds +8% absolute over episodic-memory-only (repeating the last trajectory), proving guided verbal explanation beats mere history replay. Gains hold across text-davinci-003, gpt-3.5-turbo, and GPT-4 (e.g. ReAct + davinci 0.30 to 0.55; CoT-GT + GPT-4 0.68 to 0.80).
- **Programming test-quality bound:** HumanEval and MBPP Python baselines are similar (~80–82%), but the false-positive rate P(fail | tests pass) is 16.3% on MBPP Python versus 1.4% on HumanEval Python, explaining 91% versus 77.1%. False negatives are preferred because the agent can reflect, spot the bad test, and keep correct code — while false positives cause premature invalid submission.
- **Ablation insight:** reflecting without test guidance drops to 0.52 (harmful edits, no early stop); tests without reflection stay at 0.60 (syntax caught but fixes ignore the lesson). Blind trial-and-error debugging without self-reflection is ineffective on hard Rust programs where compiler logs alone do not suggest the fix.
- **Worked corrections:** AlfWorld "examine the mug with the desklamp" fails in Trial #1 by wandering drawers and using the lamp remotely, then succeeds in 3 steps in Trial #2 after reflecting to find the lamp first; HotPotQA "Grown-Ups / 'Allo 'Allo!" answers Rene Artois (Gorden Kaye) in Trial #1 then correctly answers Captain Hans Geering via Sam Kelly in Trial #2; CoT fixes novelist-versus-novelist-and-screenwriter, single-battle-versus-campaign (White Plains vs New York and New Jersey campaign), band-count, and degree-field errors.
- **Failure modes:** WebShop e-commerce (100 tasks, two-shot ReAct + Reflexion) shows no improvement after four trials with unhelpful reflections — AlfWorld exposes permissible actions and Wikipedia search tolerates imprecise queries, but ambiguous shop search demands diverse exploration Reflexion cannot escape. Weaker StarChat-Beta shows 0.26 vs 0.26 on HumanEval Python, indicating self-correction is emergent in stronger models.

---

## Suggestions & Future Directions

1. **Scale memory beyond a sliding window** — replace the Omega = 1–3 cap with vector-embedding or SQL databases so agents retain many more lessons without overflowing context.
2. **Add natural-language value learning and off-policy exploration** — borrow classic reinforcement-learning ideas (value functions, exploration from off-policy data) expressed in language to escape non-optimal local minima such as WebShop.
3. **Fix diversity-starved exploration** — design reflection or search variants that propose genuinely different behaviors when ambiguous queries punish repetition, since current reflections are unhelpful there.
4. **Harden test-driven code evaluation** — address non-deterministic generators, impure API-interacting functions, hardware-dependent outputs, and parallel or concurrent behavior that make self-written suites flaky and bound gains by false positives.
5. **Monitor reflections for safety and alignment** — use the explicit, interpretable self-reflections as a checkpoint on agent intent before hard-to-understand tool use, and invest in misuse-risk mitigation as agents touch the Internet, software, robotics, and humans.
6. **Require isolated execution and stronger base models** — run autonomous code-writing only in isolated sandboxes since generated code executes unvalidated, and expect the method to improve as underlying self-evaluation ability improves, given no formal success guarantee.

---

## Authors & Institutions

Shinn et al. (2023) — full author roster and affiliations are not listed in the verified wiki pages; paper reference as cited above (Reflexion: Language Agents with Verbal Reinforcement Learning).
