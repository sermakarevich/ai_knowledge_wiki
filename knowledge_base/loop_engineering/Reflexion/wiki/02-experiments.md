> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Experiments across decision/reasoning/programming
**In one sentence:** Reflexion turns binary success signals into verbal self-reflections stored in a small sliding memory and re-tried over trials, lifting AlfWorld to 130/134, HotPotQA reasoning and search substantially, and HumanEval Python to 91% pass@1 while ablations show self-reflection beats episodic memory alone and test quality bounds code gains.
## Key points
- Reflexion improves over strong baselines by 22% in AlfWorld, 20% in HotPotQA, and 11% on HumanEval Python (80.1% GPT-4 to 91.0% Reflexion pass@1).
- In AlfWorld over 134 tasks, ReAct + Reflexion solves 130/134 with a simple heuristic evaluator, keeps learning across 12 consecutive trials while ReAct-only stalls between trials 6 and 7 and converges at a 22% hallucination rate.
- AlfWorld uses ReAct as actor, memory truncated to last 3 reflections, 2 domain few-shot trajectories, and self-reflection triggers when the same action plus same response repeats for more than 3 cycles or actions exceed 30.
- On 100 HotPotQA questions, baselines with temperature 0.7 never solve any first-trial failure in later trials, while Reflexion CoT with ground-truth context fixes enough of the 39% initially wrong to gain 14%, including an 8% absolute boost over episodic-memory-only.
- For programming, Reflexion generates up to 6 self-written unit tests per problem via Chain-of-Thought filtered by AST validity, uses max memory of 1 experience, and reports pass@1; it sets new SOTA on HumanEval PY 91.0, HumanEval RS 68.0, MBPP RS 75.4, LeetcodeHard PY 15.0 vs 7.5, but trails GPT-4 on MBPP PY 77.1 vs 80.1.
- The MBPP Python gap is explained by flaky internal tests: false-positive rate P(fail | tests pass) is 16.3% for MBPP Python versus 1.4% for HumanEval Python despite similar baselines near 80-82%, and false negatives are preferred because the agent can reflect and keep correct code.
- Ablation on 50 hardest HumanEval Rust problems gives 0.60 baseline, 0.52 with test-generation omitted (forced harmful edits with no early stop), 0.60 with self-reflection omitted, and 0.68 full Reflexion; StarChat-Beta shows no gain (0.26 vs 0.26), indicating self-correction is emergent in stronger models.
---
## 4 Experiments setup
Evaluates natural-language RL setups on decision-making, reasoning, and code generation: search-based QA on HotPotQA, multi-step household tasks in AlfWorld, and competition-like code writing with interpreters/compilers on HumanEval, MBPP, and LeetcodeHard, a new benchmark.
Headline deltas stated in chunk: +22% AlfWorld, +20% HotPotQA, +11% HumanEval.
## 4.1 Sequential decision making: AlfWorld
### Environment and actor
AlfWorld suite of text-based environments based on TextWorld; run on 134 environments across six task types including finding hidden objects (e.g. spatula in drawer), moving objects (e.g. knife to cutting board), and manipulating objects with other objects (e.g. chilling tomato in fridge).
Action generator is ReAct with explicit intermediate thoughts, following Yao et al. success on long trajectories.
### Self-evaluation and loop
AlfWorld only signals task completion, so autonomous self-evaluation is required. Two techniques implemented:
1. Natural-language classification using an LLM (GPT).
2. Hand-written heuristic: trigger self-reflection if the agent executes the same action and receives the same response for more than 3 cycles, or if actions in current environment exceed 30 (inefficient planning).
Baseline runs: if reflection suggested, skip reflection, reset environment, start new trial.
Reflexion runs: reflect to find mistake, update memory, reset environment, start new trial.
Memory truncated to last 3 self-reflections to avoid exceeding prompt limits.
To avoid syntactic errors, provide two domain-specific few-shot trajectories, same as Yao et al. GPT-3 examples.
### Results
Figure 3 referenced: (a) cumulative proportion solved across 134 tasks with Heuristic vs GPT evaluators; (b) classification of trajectories by failure reason.
ReAct + Reflexion significantly outperforms ReAct by completing 130 out of 134 tasks using the simple heuristic to detect hallucinations and inefficient planning.
Reflexion learns to solve additional tasks by learning in 12 consecutive trials. ReAct-only performance increase halts between trials 6 and 7.
### Analysis
Common baseline failure: agent thinks it possesses an item but does not, then executes a long trajectory without backtracking to the mistake. Reflexion distills long failed trajectories into relevant experiences used as self-hints, eliminating almost all such cases.
Two main cases where long-term memory helps:
1. Early mistake in long trajectory is easily identified; agent can suggest new action choice or new long-term plan.
2. Too many surfaces/containers to check; agent exploits experience memory over several trials to thoroughly search a room.
Learning curve suggests learning over several experiences: immediate spike between first two trials (balancing cases 1 and 2), then steady increase over next 11 trials to near-perfect performance. ReAct-only converges at 22% hallucination rate with no long-term recovery.
## 4.2 Reasoning: HotPotQA
### Setup
HotPotQA is Wikipedia-based with 113k QA pairs requiring parsing and reasoning over several supporting documents.
Reasoning-only test: Reflexion + Chain-of-Thought for Q to A and Q, C_gt to A, where Q is question, C_gt is ground-truth context, A is final answer. CoT is not multi-step decision-making, so C_gt is given to isolate reasoning over large text.
Holistic QA test: Reflexion + ReAct that retrieves context via Wikipedia API and infers answers with step-by-step explicit thinking.
Prompting: 6-shot for CoT, 2-shot for ReAct, 2-shot for self-reflection. Examples in appendix.
Evaluation: exact-match grading via environment gives binary success between trials; self-reflection loop amplifies binary signal as in AlfWorld 4.1, memory size 3 experiences.
### Results
Figure 4 referenced: Reflexion improves search, information retrieval, and reasoning on 100 HotPotQA questions; (a) Reflexion ReAct vs Reflexion CoT, (b) Reflexion CoT (GT) reasoning-only, (c) Reflexion vs episodic-memory ablation.
Reflexion outperforms all baselines by significant margins over several learning steps. ReAct-only, CoT-only, and CoT (GT)-only fail to probabilistically improve on any tasks: no failed task from first trial was solved in later trials at temperature 0.7.
Reflexion runs allow gathering experience and retrying failed tasks until 3 consecutive failed attempts on that task. CoT (GT) naturally scores higher because it sees ground-truth context, yet still misses 39% of questions; Reflexion corrects mistakes without ground-truth answers to improve accuracy by 14%.
### Analysis and ablation
Ablation isolates self-reflective step using CoT (GT) baseline, which tests reasoning over long contexts. Add episodic memory (EPM) by including most recent trajectory. Full Reflexion agent adds standard self-reflection as final pass, testing whether first-person verbal explanation learns more effectively than just repeating history.
Self-reflection improves learning by 8% absolute over the episodic-memory advantage. Supports claim that refinement-only is less effective than self-reflection-guided refinement.
## 4.3 Programming: MBPP, HumanEval, LeetcodeHardGym
### Benchmarks and languages
Evaluate Python and Rust code writing on MBPP, HumanEval, and LeetcodeHardGym. MBPP and HumanEval test function-body generation from natural-language descriptions. Use MultiPL-E benchmark language compiler to translate subsets of HumanEval and MBPP to Rust; MultiPL-E translates Python questions to 18 other languages. Rust tests show language-agnostic behavior for interpreted and compiled languages.
LeetcodeHardGym is a new interactive gym with 40 Leetcode hard-rated questions released after October 8, 2022, the GPT-4 pre-training cutoff date.
### Self-generated test suite method
Programming allows grounded self-evaluation via self-generated unit tests, enabling pass@1 reporting. Steps:
1. Use Chain-of-Thought prompting to produce diverse, extensive tests with natural-language descriptions.
2. Filter for syntactically valid statements by attempting to construct a valid abstract syntax tree (AST) for each proposed test.
3. Sample n tests to form suite T = {t_0, t_1, ..., t_n}, with n capped at maximum 6.
Aside from test suite, learning loop is identical to reasoning and decision-making agents with max memory limit of 1 experience. All instruction-based models follow zero-shot code generation; base strategy is single code-generation sample.
### Results Table 1: pass@1 accuracy
| Benchmark + Language | Prev SOTA Pass@1 | SOTA Pass@1 | Reflexion Pass@1 |
|---|---|---|---|
| HumanEval (PY) | 65.8 (CodeT + GPT-3.5) | 80.1 (GPT-4) | 91.0 |
| HumanEval (RS) | - | 60.0 (GPT-4) | 68.0 |
| MBPP (PY) | 67.7 (CodeT + Codex) | 80.1 (GPT-4) | 77.1 |
| MBPP (RS) | - | 70.9 (GPT-4) | 75.4 |
| Leetcode Hard (PY) | - | 7.5 (GPT-4) | 15.0 |
Reflexion outperforms all baselines and sets new SOTA on all Python and Rust benchmarks except MBPP Python.
### Results Table 2: test-generation confusion
Definitions: TP = tests pass, solution passes; FN = tests fail, solution passes; FP = tests pass, solution fails; TN = tests fail, solution fails. For Rust, HumanEval is hardest 50 problems translated via MultiPL-E.
| Benchmark + Language | Base | Reflexion | TP | FN | FP | TN |
|---|---|---|---|---|---|---|
| HumanEval (PY) | 0.80 | 0.91 | 0.99 | 0.40 | 0.01 | 0.60 |
| MBPP (PY) | 0.80 | 0.77 | 0.84 | 0.59 | 0.16 | 0.41 |
| HumanEval (RS) | 0.60 | 0.68 | 0.87 | 0.37 | 0.13 | 0.63 |
| MBPP (RS) | 0.71 | 0.75 | 0.84 | 0.51 | 0.16 | 0.49 |
### Analysis: false positives vs false negatives
Self-reflecting code agents are bound by ability to write diverse comprehensive tests. Flaky suite can pass all tests on incorrect solution, causing false-positive completion. Incorrectly written suite can fail on correct solution, causing false-negative completion conditioned reflection.
False negatives are preferred over false positives: agent may use self-reflection to identify incorrect test(s) and keep original completion intact, while false-positive completion causes premature invalid submission.
Evidence: HumanEval and MBPP Python baselines are similar (82% and 80%), but false-positive execution rate P(not pass@1 correct | tests pass) is 16.3% for MBPP Python versus 1.4% for HumanEval Python, leading to 91% overall for HumanEval in Table 1.
### Ablation Table 3: test generation vs self-reflection on 50 hardest HumanEval Rust
| Approach | Test Generation | Self-reflection | Pass@1 (Acc) |
|---|---|---|---|
| Base model | False | False | 0.60 |
| Test generation omission | False | True | 0.52 |
| Self-reflection omission | True | False | 0.60 |
| Reflexion | True | True | 0.68 |
Rust compiler provides verbose logs and debugging hints, good playground for compromised approaches.
Omitting internal test generation and execution (reflect without guidance): 52% vs 60% baseline, agent cannot tell if implementation is correct without unit tests, must participate in all iterations without early return, performing harmful edits.
Omitting natural-language explanation after failed suites (combine error identification and fix without reflection): no improvement over baseline; test generation and compilation catch syntax/logic errors but fixes do not reflect indications.
Conclusion: blind trial-and-error debugging without self-reflection is ineffective on harder tasks like complex Rust programs.
## 5 Limitations
Reflexion is optimization via natural language for policy optimization; may still fall into non-optimal local minima. Study limits long-term memory to sliding window with maximum capacity; future work encouraged on vector embedding databases or SQL databases. For code, test-driven development limits include non-deterministic generators, impure API-interacting functions, hardware-dependent outputs, and parallel/concurrent behavior that is hard to predict.
## 6 Broader impact
LLMs increasingly interact with external environments (Internet, software, robotics) and humans. Work can reinforce automation and efficiency but amplifies misuse risks, requiring safety and ethics effort. Conversely, verbal RL may improve interpretability and alignment over black-box RL; self-reflections could be monitored to ensure proper intent before hard-to-understand tool use.
## 7 Conclusion
Presents Reflexion, verbal reinforcement to learn from past mistakes; empirically outperforms widely used decision-making approaches via self-reflection. Future work could add value learning in natural language or off-policy exploration from traditional RL.
## 8 Reproducibility
Strong advisory to use isolated execution environments when running autonomous code-writing experiments because generated code is not validated before execution.
## Appendix A Evaluation with additional models
Tests trial-and-error problem-solving across model strengths; ability to specify self-corrections appears emergent in stronger, larger models.
Table 4 Pass@1 on HumanEval Python using StarChat-Beta:
| Approach | Pass@1 avg over 8 trials | Pass@1 std |
|---|---|---|
| Baseline | 0.26 | 0.00481 |
| Reflexion | 0.26 | 0.00305 |
No improvement with weaker model.
Table 5 Pass@1 on 100 HotPotQA using various models:
| Model | Baseline accuracy | Reflexion accuracy |
|---|---|---|
| CoT (GT) + text-davinci-003 | 0.60 | 0.77 |
| CoT (GT) + gpt-3.5-turbo | 0.57 | 0.71 |
| CoT (GT) + gpt-4 | 0.68 | 0.80 |
| ReAct + text-davinci-003 | 0.30 | 0.55 |
| ReAct + gpt-3.5-turbo | 0.26 | 0.38 |
| ReAct + gpt-4 | 0.39 | 0.51 |
Reflexion gains hold across davinci, 3.5-turbo, and GPT-4 for both CoT (GT) and ReAct, with largest ReAct jump on davinci 0.30 to 0.55.
**Covers:** chunk 02
