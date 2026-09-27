> [[index|Wiki]] | [[summary|Summary]]

# Reflexion — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-introduction-method|Intro, related work, Reflexion method]]

**In one sentence:** Reflexion replaces weight updates with verbal reinforcement — an Actor, Evaluator, and Self-Reflection LLM loop where textual self-reflections on failures are stored in episodic memory and reused as context, yielding large gains on decision-making, reasoning, and coding tasks without fine-tuning.

- Reflexion reinforces language agents not by updating weights but through linguistic feedback: verbal reflections on task feedback are kept in an episodic memory buffer to improve decisions in later trials.
- It accepts varied feedback types (scalar values or free-form language) and sources (external or internally simulated), and improves over baselines on sequential decision-making, coding, and language reasoning.
- Headline results claimed: 91% pass@1 on HumanEval (vs 80% previous SOTA GPT-4), +22% absolute on AlfWorld decision tasks in 12 trials, +20% on HotPotQA reasoning, up to +11% on HumanEval Python tasks.
- Advantages over traditional RL: lightweight with no LLM fine-tuning, nuanced actionable feedback vs scalar rewards, explicit interpretable episodic memory, and direct hints for future actions; limitation is reliance on LLM self-evaluation with no formal success guarantee.
- Prior reasoning/decision methods (Self-Refine, beam search) lack persisting reflective memory, and prior coding methods (AlphaCode, CodeT, Self-Debugging, CodeRL) rely on ground-truth tests or lack a self-learning reflection step — Reflexion is the only compared approach with self-refine + hidden constraints + decision-making + binary reward + memory (reasoning table) and test execution + debugging + self-generated tests + multi-language + self-reflection (coding table).
- The framework uses three LLMs: Actor M_a generating text/actions from policy pi_theta(a_i|s_i) with theta = {M_a, mem}, Evaluator M_e scoring trajectories tau, and Self-Reflection M_sr turning sparse rewards plus trajectory plus memory into stored verbal summaries sr_t.
- Memory is split into short-term (trajectory history tau_t = [a_0, o_0, ..., a_i, o_i]) and long-term (stored reflections), with long-term memory bounded to Omega = 1-3 experiences to fit LLM context limits; the loop runs until M_e passes or t reaches max trials.

## 2. [[wiki/02-experiments|Experiments across decision/reasoning/programming]]

**In one sentence:** Reflexion turns binary success signals into verbal self-reflections stored in a small sliding memory and re-tried over trials, lifting AlfWorld to 130/134, HotPotQA reasoning and search substantially, and HumanEval Python to 91% pass@1 while ablations show self-reflection beats episodic memory alone and test quality bounds code gains.

- Reflexion improves over strong baselines by 22% in AlfWorld, 20% in HotPotQA, and 11% on HumanEval Python (80.1% GPT-4 to 91.0% Reflexion pass@1).
- In AlfWorld over 134 tasks, ReAct + Reflexion solves 130/134 with a simple heuristic evaluator, keeps learning across 12 consecutive trials while ReAct-only stalls between trials 6 and 7 and converges at a 22% hallucination rate.
- AlfWorld uses ReAct as actor, memory truncated to last 3 reflections, 2 domain few-shot trajectories, and self-reflection triggers when the same action plus same response repeats for more than 3 cycles or actions exceed 30.
- On 100 HotPotQA questions, baselines with temperature 0.7 never solve any first-trial failure in later trials, while Reflexion CoT with ground-truth context fixes enough of the 39% initially wrong to gain 14%, including an 8% absolute boost over episodic-memory-only.
- For programming, Reflexion generates up to 6 self-written unit tests per problem via Chain-of-Thought filtered by AST validity, uses max memory of 1 experience, and reports pass@1; it sets new SOTA on HumanEval PY 91.0, HumanEval RS 68.0, MBPP RS 75.4, LeetcodeHard PY 15.0 vs 7.5, but trails GPT-4 on MBPP PY 77.1 vs 80.1.
- The MBPP Python gap is explained by flaky internal tests: false-positive rate P(fail | tests pass) is 16.3% for MBPP Python versus 1.4% for HumanEval Python despite similar baselines near 80-82%, and false negatives are preferred because the agent can reflect and keep correct code.
- Ablation on 50 hardest HumanEval Rust problems gives 0.60 baseline, 0.52 with test-generation omitted (forced harmful edits with no early stop), 0.60 with self-reflection omitted, and 0.68 full Reflexion; StarChat-Beta shows no gain (0.26 vs 0.26), indicating self-correction is emergent in stronger models.

## 3. [[wiki/03-appendices|Appendices C-D and extra evals]]

**In one sentence:** The appendices show Reflexion correcting inefficient AlfWorld plans and HotPotQA search errors across trials, detail strict function-body-only prompts for HumanEval, and report that Reflexion fails on WebShop where diverse creative exploration is required.

- An AlfWorld trial for "examine the mug with the desklamp" fails in Trial #1 through inefficient planning (wandering drawers/desks, using desklamp remotely with no effect), then succeeds in Trial #2 with a concise 3-step trace after reflecting to find the lamp first.
- Reflexion struggles on WebShop: a two-shot ReAct + Reflexion agent tested on 100 shopping tasks shows no improvement after four trials, runs are terminated early, and self-reflections are unhelpful.
- The authors conclude Reflexion cannot escape local minima requiring highly diverse exploration; AlfWorld exposes permissible actions in observations and HotPotQA Wikipedia search tolerates imprecise queries, while e-commerce search ambiguity punishes Reflexion.
- Programming experiments require strict instructions to emit function bodies only; the C.1 HumanEval example uses `minSubArraySum(nums)` with an O(n^2) nested-loop implementation tracking `min_sum` from infinity.
- The Reflexion Actor instruction forces output of only the improved function body with 4-space indented first line and no signature, conditioned on previous implementation, unit-test results, and self-reflection.
- HotPotQA full example (Grown-Ups / "'Allo 'Allo!") fails in Trial #1 by answering Rene Artois (Gorden Kaye) instead of intersecting the Grown-Ups cast, then succeeds in Trial #2 by searching Sam Kelly and answering Captain Hans Geering.
- Chain-of-Thought + Reflexion corrects overgeneralization errors: novelist vs novelist-and-screenwriter (Lanchester/Foster), single battle vs campaign (White Plains / New York and New Jersey campaign), and band-count comparisons (Craig/Doherty) plus degree-field confusion (M.Sc. in Engineering).
- Full code is at https://github.com/noahshinn024/reflexion, with Figures 5, 6, and 7 illustrating the AlfWorld correction, the flat WebShop Reflexion-vs-ReAct curve, and the two-trial HotPotQA search fix.

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. Language agents stall on sequential tasks because sparse binary rewards teach nothing without weight updates.
2. Reflexion replaces weight updates with verbal self-reflection stored as episodic memory for future trials.
3. An Actor–Evaluator–Self-Reflection loop retries each task, conditioning every attempt on past reflections.
4. A tiny sliding memory of 1–3 reflections plus heuristic or self-generated tests suffices to steer corrections.
5. This loop lifts AlfWorld to 130/134, HotPotQA reasoning by 20 points, and HumanEval Python to 91% pass@1.
6. Gains vanish where diverse exploration is required (WebShop) or where models and tests are weak, bounding the method.
<!-- FIVE_MOVES_END -->
