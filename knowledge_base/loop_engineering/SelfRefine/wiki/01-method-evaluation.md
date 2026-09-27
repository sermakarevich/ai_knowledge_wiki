> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Method and evaluation (1-7)

**In one sentence:** Self-Refine uses a single large language model (LLM — a large neural network trained on text that generates outputs word by word) as its own generator, feedback-giver, and refiner in a loop, and across 7 tasks it lifts strong models like GPT-3.5, ChatGPT, and GPT-4 by ~20% absolute on average without any extra training.

## Key points

- Self-Refine loops three few-shot-prompted steps with one frozen model M: initial generation y0 = M(p_gen || x), self-feedback fbt = M(p_fb || x || yt), and refinement yt+1 = M(p_refine || x || history), stopping after up to 4 iterations or when the feedback contains a stop signal.
- Feedback must be actionable and specific (e.g. "slow for-loop, use n(n+1)/2" rather than "improve efficiency"): with ChatGPT/GPT-3.5, replacing targeted feedback with generic feedback drops Sentiment Reversal 43.2 to 31.2 and Acronym Generation 56.4 to 48.0, and removing feedback entirely collapses Sentiment Reversal to 0.
- Gains hold across all base models and all 7 tasks: GPT-4 + Self-Refine improves over base GPT-4 by 8.7 points on Code Optimization (27.3% to 36.0%), 49.2 points on Dialogue Response preference (25.4% to 74.6%), and 30.0 points on Constrained Generation (15.0% to 45.0%).
- Most improvement comes in early iterations with diminishing returns: averaged over models, Constrained Generation rises 29.0 (y0) to 40.3 (y1) to 46.7 (y2) to 49.7 (y3), while Code Optimization rises 22.0 to 28.8 and Sentiment Reversal 33.9 to 36.8 over three iterations.
- Math Reasoning barely moves (+0.0 to +0.2 points) because the model cannot spot its own errors — ChatGPT says "everything looks good" on 94% of math instances — though an external correctness signal restores 5%+ gains.
- Failure analysis on 70 Code Optimization and Math samples shows feedback is the bottleneck: of failures, 33% mislocalize the error and 61% suggest a wrong fix, with only 6% caused by the refiner botching good feedback; conversely the refiner fixes the output even from partially wrong feedback in 33% of successes.
- The method needs a strong instruction-following model: Vicuna-13B cannot reliably emit feedback in the required format and, even given oracle feedback, repeats outputs or hallucinates conversations instead of refining.

---

## 1 Introduction and core idea

- Motivation: LLMs (large language models) produce coherent first drafts but miss multifaceted requirements (dialogue quality, code readability/efficiency); classic refinement needs domain data or trained reward/refinement models plus costly human labels.
- Human analogy: people self-refine — drafting "Send me the data ASAP" then revising to a polite version, or rewriting quick-and-dirty code into an efficient readable form.
- Claim: the same LLM can generate feedback on its own output and then refine it, iteratively, using only few-shot prompting (showing the model a few input-output examples inside the prompt, also called in-context learning), with no supervised training data, extra training, or reinforcement learning (training by reward signals).
- Reported headline result: ~20% absolute average improvement over one-step generation from the same model; 5–40% absolute per task; up to +13 points absolute on code tasks with Codex (code-davinci-002); code, data, and prompts at https://selfrefine.info/.
- Illustrative examples (Figure 2): a bland table-tennis reply is refined into an engaging question about experience and goals after feedback naming "Engaging" and "User understanding" defects; an O(n) loop summing 1..N is refined into `return (n*(n+1))//2` after feedback diagnosing brute force.

## 2 Iterative Refinement with Self-Refine

### Setup

- Inputs: input x, one model M, three task-specific few-shot prompts {p_gen, p_fb, p_refine}, and a stop condition stop(fbt, t).
- No training; only supervision is the few-shot examples embedded in the three prompts.

### Initial generation (Eq. 1)

- y0 = M(p_gen || x), where || is concatenation.
- p_gen is a task-specific few-shot prompt (or instruction) of input-output pairs <x(k), y(k)>.

### Feedback (Eq. 2)

- fbt = M(p_fb || x || yt) using the same model M on its own output.
- p_fb contains input-output-feedback triples <x(k), y(k), fb(k)>.
- Feedback is prompted to be actionable (names a concrete improving action) and specific (names the concrete span to change); example: "This code is slow as it uses a for loop which is brute force. A better approach is to use the formula n(n+1)/2."
- Feedback can be multi-aspect (e.g. code efficiency, readability, quality).

### Refine (Eq. 3–4)

- Single-step form: yt+1 = M(p_refine || x || yt || fbt).
- History-aware form actually used (Eq. 4 / Algorithm 1 line 8): yt+1 = M(p_refine || x || y0 || fb0 || ... || yt || fbt), so the model sees past outputs and feedback and avoids repeating mistakes.
- p_refine contains quadruples <x(k), yt(k), fbt(k), yt+1(k)> showing how to apply feedback.

### Iteration and stopping

- Loop feedback then refine; stop via stop(fbt, t): a fixed timestep or a stopping indicator (e.g. scalar stop score) the model is prompted to emit inside p_fb; the criterion is per-task.
- Return the last refinement yt. Figure 1 shows the loop (generate → feedback ① → refine ② → repeat); Algorithm 1 (Figure 3) lists the 11-line pseudocode.
- Prompt examples for p_gen, p_fb, p_refine are in Appendix S.

## 3 Evaluation

### 3.1 Tasks

- 7 diverse generation tasks: Dialogue Response Generation, Code Optimization, Code Readability Improvement, Math Reasoning, Sentiment Reversal, plus two new tasks — Acronym Generation and Constrained Generation (20–30 required keywords, harder than the 3–5 in prior work).
- Dataset statistics and per-task examples are in Table 4 (Appendix A).

### 3.2 Instantiation and base models

- Feedback–refine loop runs until the task criterion is met, up to a maximum of 4 iterations.
- Both feedback and refine are implemented as few-shot prompts for consistency, even for instruction-tuned models (ChatGPT, GPT-4).
- Base LLMs: GPT-3.5 (text-davinci-003), ChatGPT (gpt-3.5-turbo), GPT-4; plus Codex (code-davinci-002) for code tasks. In every task either GPT-3.5 or GPT-4 was the prior state of the art; comparison against other few-shot/fine-tuned baselines is in Appendix F.
- Prompts reuse prior work where available (Code Optimization, Math Reasoning), else Appendix S; greedy decoding with temperature 0.7 everywhere.

### Metrics

- Task-specific automated metrics where available: Math Reasoning solve rate (%), Code Optimization % programs optimized, Constrained Generation keyword coverage (%).
- Human-pref: blind human A/B preference on a subset for Dialogue Response Generation, Code Readability Improvement, Sentiment Reversal, Acronym Generation (details Appendix C).
- GPT-4-pref: GPT-4 as a human proxy; correlation with human-pref is 82% (Sentiment Reversal), 68% (Acronym Generation), 71% (Dialogue); for Code Readability GPT-4 scores the fraction of appropriately renamed variables (e.g. `x = []` → `input_buffer = []`); details Appendix D.

### 3.3 Results (Table 1)

| Task | GPT-3.5 Base | GPT-3.5 + Self-Refine | ChatGPT Base | ChatGPT + Self-Refine | GPT-4 Base | GPT-4 + Self-Refine |
|---|---|---|---|---|---|---|
| Sentiment Reversal | 8.8 | 30.4 (+21.6) | 11.4 | 43.2 (+31.8) | 3.8 | 36.2 (+32.4) |
| Dialogue Response | 36.4 | 63.6 (+27.2) | 40.1 | 59.9 (+19.8) | 25.4 | 74.6 (+49.2) |
| Code Optimization | 14.8 | 23.0 (+8.2) | 23.9 | 27.5 (+3.6) | 27.3 | 36.0 (+8.7) |
| Code Readability | 37.4 | 51.3 (+13.9) | 27.7 | 63.1 (+35.4) | 27.4 | 56.2 (+28.8) |
| Math Reasoning | 64.1 | 64.1 (+0.0) | 74.8 | 75.0 (+0.2) | 92.9 | 93.1 (+0.2) |
| Acronym Generation | 41.6 | 56.4 (+14.8) | 27.2 | 37.2 (+10.0) | 30.4 | 56.0 (+25.6) |
| Constrained Generation | 28.0 | 37.0 (+9.0) | 44.0 | 67.0 (+23.0) | 15.0 | 45.0 (+30.0) |

- Self-Refine beats the same base model on every model–task cell and beats prior state of the art on all tasks; confidence intervals in Appendix J; Codex trends match (Appendix F).
- Largest gains where the first pass often misses pieces: Constrained Generation (up to 30 required concepts) benefits because Self-Refine fixes dropped concepts over iterations and explores the large output space.
- Preference tasks gain most: Dialogue +49.2 points on GPT-4 (25.4% → 74.6%).
- Math gains are near zero because error detection fails on subtle single-line/operator errors and fluent-but-wrong chains; external correctness signal restores 5%+ (Section H.1).
- Stronger bases unlock more: GPT-4 + Self-Refine tops GPT-3.5/ChatGPT + Self-Refine on all tasks even where base GPT-4 started lower, suggesting Self-Refine unlocks latent capability hidden in single-pass decoding.

## 4 Analysis

### Feedback quality ablation (Table 2)

| Task | Self-Refine feedback | Generic feedback | No feedback |
|---|---|---|---|
| Code Optimization (ChatGPT) | 27.5 | 26.0 | 24.8 |
| Sentiment Reversal (ChatGPT) | 43.2 | 31.2 | 0 |
| Acronym Generation (GPT-3.5) | 56.4 | 54.0 | 48.0 |

- Actionable example: "Avoid repeated calculations in the for loop" vs generic "Improve the efficiency of the code".
- Code Optimization degrades gracefully (27.5 → 26.0 → 24.8); Sentiment Transfer collapses without targeted feedback (43.2 → 31.2 → task fails); Acronym drops 56.4 → 48.0 without actionable feedback despite continued iteration.

### Multiple iterations (Figure 4)

- Averaged over ChatGPT, GPT-3.5, GPT-4: Code Optimization y0=22.0, y1=27.0, y2=27.9, y3=28.8; Sentiment Reversal 33.9 → 34.9 → 36.1 → 36.8; Constrained Generation 29.0 → 40.3 → 46.7 → 49.7.
- Biggest delta is y0 → y1 (e.g. +11.3 on Constrained Generation), then diminishing (+6.4, +3.0); pattern holds for Code Optimization (+~5 early) and Sentiment Reversal (+0.9-range steps).
- Non-monotonicity is possible in multi-aspect tasks (Acronym Generation) where one aspect improves while another regresses; mitigation is generating numeric scores per aspect and selecting a balanced output.

### 1-vs-k: refinement vs just sampling more

- ChatGPT generating k=4 independent samples (no feedback/refine) still loses: human judges prefer the single Self-Refine output over all k initial outputs (Figure 9, Appendix H), so the gain is from feedback-driven refinement, not extra samples.

### Weaker models

- Vicuna-13B can generate y0 but fails at the loop: it does not emit feedback in the required format and, even with oracle (perfect, externally supplied) or hard-coded feedback, ignores refine prompts — repeating outputs or hallucinating conversations — attributed to conversation-tuning generalizing poorly to few-shot test-time feedback tasks (Appendix G).

### Qualitative analysis and Figure 5 example

- Manual review of 70 samples (35 success + 35 failure) across Code Optimization and Math Reasoning: feedback is mostly actionable and correctly localizes problems in successes.
- Failure breakdown: 33% feedback mislocalizes the error, 61% suggests a wrong fix, only 6% is the refiner mishandling good feedback.
- Resilience: in 61% of successes the refiner applies accurate feedback precisely; in 33% of successes it still recovers despite partially incorrect feedback.
- Figure 5: baseline output keeps six nested coin loops (near-copy of slow input); Self-Refine feedback diagnoses "six nested loops over all coin combinations" and the rewrite is O(amount × coins) dynamic programming (DP — an algorithm that builds answers bottom-up in a table instead of re-enumerating combinations); full example in Appendix H; more dialogue analysis also in Appendix H.

### Beyond benchmarks

- Website-generation case study: from a rudimentary page, Self-Refine iteratively improves HTML, CSS, and JS (webpage structure, styling, and interactivity) for usability and aesthetics from a high-level goal; examples, discussion, and societal impact in Appendix I.

## 5 Related work

- Landscape: NL (natural language) and non-NL feedback have improved summarization, script generation, program synthesis, and others; dimensions are feedback source, feedback form, and how the refiner is obtained (Table 3; Appendix B).
- Feedback sources: humans (costly), scalar reward functions as human surrogates, domain tools (compilers, Wikipedia edits), and recently LLMs; this work is unique in using the same LLM to give feedback on its own output for refining with that same LLM.
- Feedback form: non-NL (example pairs, scalar rewards) vs NL feedback; NL is chosen because it lets the same generative model do self-feedback while reusing pretrained models like GPT-4.
- Refiner types: learned supervised refiners (PEER, Self-critique, CodeRL, Self-correction) need costly pairs or per-domain training even when bootstrapped from model generations; prompted refiners (Augmenter, Re3, Reflexion) avoid training but Re3 is story-specific; Self-Refine uses one prompted model as feedback source and refiner across domains.
- Non-refinement reinforcement-learning alternatives optimize a scalar reward and update weights without exposing intermediate feedback; Self-Refine instead conditions on intermediate NL feedback and changes no parameters.

## 6 Limitations and discussion

- Requires base models with sufficient few-shot or instruction-following ability to learn feedback and refinement in context without supervised models or data.
- Experiments use closed models (GPT-3.5, ChatGPT, GPT-4, Codex) whose pretraining data, sizes, and biases are undisclosed; they cost money to run; authors release code and outputs for reproducibility.
- English-only datasets, so benefits may not transfer to other languages.
- Prompting could be misused by bad actors to steer models toward more toxic or harmful text; no explicit guard is added.

## 7 Conclusion

- Self-Refine lets LLMs iteratively self-critique and self-improve inside a single model with no extra training data or reinforcement learning.
- Demonstrated as simple and easy to use across many tasks, aiming to cut the cost of human creative work; all code, data, and prompts at https://selfrefine.info/.

**Covers:** chunk 01
