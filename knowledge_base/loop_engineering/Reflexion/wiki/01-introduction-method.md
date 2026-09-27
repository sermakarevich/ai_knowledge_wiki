> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Intro, related work, Reflexion method

**In one sentence:** Reflexion replaces weight updates with verbal reinforcement — an Actor, Evaluator, and Self-Reflection LLM loop where textual self-reflections on failures are stored in episodic memory and reused as context, yielding large gains on decision-making, reasoning, and coding tasks without fine-tuning.

## Key points
- Reflexion reinforces language agents not by updating weights but through linguistic feedback: verbal reflections on task feedback are kept in an episodic memory buffer to improve decisions in later trials.
- It accepts varied feedback types (scalar values or free-form language) and sources (external or internally simulated), and improves over baselines on sequential decision-making, coding, and language reasoning.
- Headline results claimed: 91% pass@1 on HumanEval (vs 80% previous SOTA GPT-4), +22% absolute on AlfWorld decision tasks in 12 trials, +20% on HotPotQA reasoning, up to +11% on HumanEval Python tasks.
- Advantages over traditional RL: lightweight with no LLM fine-tuning, nuanced actionable feedback vs scalar rewards, explicit interpretable episodic memory, and direct hints for future actions; limitation is reliance on LLM self-evaluation with no formal success guarantee.
- Prior reasoning/decision methods (Self-Refine, beam search) lack persisting reflective memory, and prior coding methods (AlphaCode, CodeT, Self-Debugging, CodeRL) rely on ground-truth tests or lack a self-learning reflection step — Reflexion is the only compared approach with self-refine + hidden constraints + decision-making + binary reward + memory (reasoning table) and test execution + debugging + self-generated tests + multi-language + self-reflection (coding table).
- The framework uses three LLMs: Actor M_a generating text/actions from policy pi_theta(a_i|s_i) with theta = {M_a, mem}, Evaluator M_e scoring trajectories tau, and Self-Reflection M_sr turning sparse rewards plus trajectory plus memory into stored verbal summaries sr_t.
- Memory is split into short-term (trajectory history tau_t = [a_0, o_0, ..., a_i, o_i]) and long-term (stored reflections), with long-term memory bounded to Omega = 1-3 experiences to fit LLM context limits; the loop runs until M_e passes or t reaches max trials.

---

## Abstract

- Problem: LLMs increasingly act as goal-driven agents interacting with games, compilers, and APIs, but trial-and-error learning via traditional RL needs extensive samples and expensive fine-tuning.
- Proposal: Reflexion, a framework that reinforces language agents through linguistic feedback instead of weight updates — agents verbally reflect on task feedback signals and maintain reflective text in an episodic memory buffer for better subsequent decisions.
- Flexible to various feedback types (scalar or free-form language) and sources (external or internally simulated); significant gains over baseline agents on sequential decision-making, coding, and language reasoning.
- Example: 91% pass@1 on HumanEval, surpassing previous SOTA GPT-4 at 80%.
- Studies ablations over feedback signals, incorporation methods, and agent types.
- Code, demos, datasets released at https://github.com/noahshinn024/reflexion.

## 1 Introduction

- Context: ReAct, SayCan, Toolformer, HuggingGPT, generative agents, and WebGPT show LLM-core autonomous agents that emit text/actions executed as API calls in an environment; massive parameter counts have limited teaching to in-context examples since gradient RL needs heavy compute and time.
- Core idea: verbal reinforcement — convert binary/scalar environment feedback into a textual summary added as extra LLM context next episode; this self-reflective feedback acts as a "semantic" gradient giving concrete improvement direction, mimicking human few-shot learning from failure (Figure 1 covers decision-making, programming, reasoning tasks).
- Generating useful reflection is hard due to credit assignment (where the mistake occurred) plus the need for actionable summaries; three feedback routes explored: simple binary environment feedback, pre-defined heuristics for common failures, and self-evaluation such as LLM binary classification (decision-making) or self-written unit tests (programming); in all cases the signal is amplified into natural-language experience summaries in long-term memory.
- Claimed advantages vs policy/value RL: (1) lightweight, no fine-tuning; (2) nuanced targeted feedback vs hard-to-assign scalar/vector rewards; (3) explicit interpretable episodic memory; (4) explicit hints for future episodes. Disadvantages: depends on LLM self-evaluation or heuristics, no formal guarantee — expected to improve as LLMs improve.
- Experiments: (1) decision-making (long-trajectory sequential actions), (2) reasoning (knowledge-intensive single-step generation), (3) programming (compiler/interpreter tool use); Reflexion improves on AlfWorld by absolute 22% in 12 steps, HotPotQA by 20%, HumanEval Python by up to 11%.
- Contributions:
  - New "verbal" reinforcement paradigm parameterizing policy as agent memory encoding plus LLM parameters.
  - Empirical study of emergent LLM self-reflection over a handful of trials.
  - LeetcodeHardGym: RL gym of 40 hard-level Leetcode questions in 19 programming languages.
  - Improvements over strong baselines and SOTA on code generation benchmarks.

## 2 Related work

### Reasoning and decision-making

- Self-Refine: iterative self-refinement via self-evaluation conditioned on task constraints (e.g. "more positive way"); effective but single-generation only.
- Pryzant et al.: semantic prompt-writing optimization, also single-generation only.
- Paul et al.: fine-tuned critic models for intermediate in-trajectory feedback.
- Xie et al.: stochastic beam search over actions for efficient search with self-evaluation foresight.
- Yoran et al. and Nair et al.: decider models reasoning over several generations; Kim et al.: fixed-step retry without evaluation; Goodman: qualitative evaluation proposing optimizations.
- Claim: these concepts are enhanced with self-reflection into persisting memory of reflective experiences for error identification and self-suggested lessons over time.

| Approach | Self-refine | Hidden constraints | Decision-making | Binary reward | Memory |
|---|---|---|---|---|---|
| Self-refine [15] | yes | no | no | no | no |
| Beam search [27] | yes | yes | yes | yes | no |
| Reflexion (ours) | yes | yes | yes | yes | yes |

### Programming

- AlphaCode: evaluates generation sets on hidden test cases.
- CodeT: self-generated unit tests scoring implementations.
- Self-Debugging: debugging component improving implementations from execution feedback.
- CodeRL: actor-critic RL debugging from execution feedback.
- Critique: AlphaCode, Self-Debugging, CodeRL fix simpler bugs but need ground-truth tests (invalidating pass@1) and lack self-reflection bridging error identification to improvement; CodeT avoids hidden tests but has no self-learning step.

| Approach | Test execution | Debugging | Self-generated tests | Multiple languages | Self-reflection |
|---|---|---|---|---|---|
| AlphaCode [14] | yes | no | no | yes | no |
| CodeT [5] | yes | no | yes | no | no |
| Self-debugging [7] | yes | yes | no | no | no |
| CodeRL [12] | yes | yes | no | no | no |
| Reflexion (ours) | yes | yes | yes | yes | yes |

## 3 Reflexion: reinforcement via verbal reflection

### Algorithm (Algorithm 1, Figure 2)

- Init Actor, Evaluator, Self-Reflection: M_a, M_e, M_sr; policy pi_theta(a_i|s_i) with theta = {M_a, mem}.
- Generate initial trajectory tau_0 with pi_theta; evaluate with M_e; generate initial reflection sr_0 with M_sr; set mem = [sr_0]; set t = 0.
- While M_e not pass and t < max trials: generate tau_t = [a_0, o_0, ..., a_i, o_i] with pi_theta; evaluate tau_t with M_e; generate sr_t with M_sr; append sr_t to mem; increment t.
- Return.

### Actor

- LLM prompted to generate text/actions conditioned on state observations; samples action a_t from pi_theta at time t, receives observation o_t.
- Actor variants explored: Chain of Thought and ReAct, giving insight into generation performance.
- Adds memory component mem as extra context, inspired by Brooks et al. policy iteration via in-context learning.

### Evaluator

- Scores Actor trajectories with a reward reflecting task performance; semantic value/reward design is hard so several variants tried.
- Reasoning: exact match (EM) grading; decision-making: pre-defined heuristic functions; decision-making and programming: another LLM instantiation as Evaluator.
- Multi-faceted design compares scoring strategies across tasks.

### Self-reflection

- LLM generating verbal self-reflections as feedback for future trials from sparse reward (e.g. success/fail), current trajectory, and persistent mem; more informative than scalar rewards, stored in mem.
- Example mechanism: on failure infer action a_i caused bad follow-ups a_{i+1}, a_{i+2}, verbally state it should have taken a_i' leading to a_{i+1}', a_{i+2}', store it, then reuse it at time t in later trials.
- Iterative trial-error-reflection-memory loop enables rapid improvement.

### Memory

- Short-term memory = trajectory history (fine-grain recent detail); long-term memory = Self-Reflection outputs (distilled important experiences), like human recall.
- Both condition Actor decisions, giving specific context shaped by lessons over trials — key edge over other LLM action-choice work.

### The Reflexion process

- Formalized as iterative optimization: trial 1 Actor produces tau_0; Evaluator computes scalar r_0 = M_e(tau_0), improving with task performance.
- Self-Reflection amplifies {tau_0, r_0} into verbal summary sr_0 stored in mem; sr_t is verbal experience feedback for trial t.
- Actor, Evaluator, Self-Reflection loop until M_e deems tau_t correct; after each trial sr_t appended to mem, bounded to max Omega stored experiences (usually 1-3) for LLM context limits.

**Covers:** chunk 01
