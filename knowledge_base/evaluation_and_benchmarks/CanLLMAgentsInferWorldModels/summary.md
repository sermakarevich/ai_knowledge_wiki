# Can LLM Agents Infer World Models? Evidence from Agentic Automata Learning

**Paper:** [Can LLM Agents Infer World Models? Evidence from Agentic Automata Learning (Menaged, Lior, Ravfogel, Aharoni, Stanovsky, 2026)](https://arxiv.org/abs/2606.16576)

## Human Readable TL;DR

Imagine giving someone a mysterious vending machine with unknown rules -- they can press buttons and see what comes out, then guess the full rulebook. This paper asks: can modern AI assistants figure out these hidden rules through trial and error? They tested this with simple mathematical rule systems (like "accept any word with at least one letter 'b'") and found that even the best AI systems frequently fail, make redundant guesses, and lose track of what they already learned -- while old-fashioned dedicated algorithms solve the same puzzles perfectly, every time.

## TL;DR

This paper introduces *agentic automata learning*, a controlled benchmark where tool-calling LLM agents must identify a hidden deterministic finite automaton (DFA) by issuing membership queries ("is this string in the language?") and equivalence queries ("is this my hypothesis the correct DFA?"). Evaluated on 6 frontier models across DFAs of 2--9 states, no model exceeds 25% success on 8--9-state DFAs, while classical algorithms (L* and TTT) achieve 100%. Reasoning models substantially outperform non-reasoning variants, but all models exhibit recurring failures in query planning, evidence integration, and hypothesis construction.

---

## Problem & Motivation

LLMs are increasingly deployed as interactive agents in environments with unknown dynamics. A fundamental open question is whether these agents can *infer* a correct world model of their environment through interaction -- or whether they rely on shallow pattern matching and surface-level heuristics. Existing benchmarks (web navigation, software engineering, game playing) involve complex real-world tasks where task complexity is hard to control and agent behavior is hard to analyze. This work needs a rigorous, scalable, and interpretable testbed with formal complexity measures, strong algorithmic baselines, and the ability to observe the discovery process in detail.

---

## Main Original Ideas

1. **Agentic Automata Learning Framework.** Recasts classical active automata learning as an agentic benchmark: an LLM agent is equipped with two tools -- a membership query tool and an equivalence query tool -- and must identify a hidden DFA within a query budget. This yields controllable complexity (via DFA state count), measurable efficiency (query count), and direct comparison to classical algorithms (L* and TTT).

2. **Scalable Procedural Instance Generation.** Task instances are generated automatically at arbitrary scale using Boltzmann sampling over binary-alphabet DFAs, with rejection sampling to filter non-minimal DFAs. This eliminates the need for human annotation and allows continuous difficulty scaling.

3. **Two-Dimensional Performance Measurement.** Evaluates both *success rate* (does the agent find the hidden DFA?) and *interaction efficiency* (how many queries does it take, relative to classical algorithms?), capturing both effectiveness and efficiency of the discovery process.

4. **Planning vs. Reasoning Failure Decomposition.** Introduces a diagnostic decomposition of agent failures: a *planning failure* occurs when no passive learning algorithm can infer the DFA from the accumulated observations (agent gathered insufficient evidence), while a *reasoning failure* occurs when a passive learner *could* infer the correct DFA from what the agent observed (information was there but the agent failed to use it).

5. **Non-Informative Query Analysis.** Measures the rate at which agents issue queries whose answers are already implied by prior interaction history, revealing a fundamental failure mode where agents increasingly fail to organize and exploit accumulated evidence as context grows.

---

## Key Findings

| Model | 2--3 states | 4--5 states | 6--7 states | 8--9 states |
|---|---|---|---|---|
| Gemini 3.1 Pro Preview | ~100% | ~85% | ~50% | ~10% |
| DeepSeek-V4-Pro | ~55% | ~35% | ~10% | ~5% |
| Gemini-3-Flash (thinking) | ~15% | ~15% | ~5% | ~0% |
| GPT-5.4 (without thinking) | ~15% | ~0% | ~0% | ~0% |
| Gemini-3.1-Flash-Lite | ~25% | ~0% | ~0% | ~0% |
| Llama-3.3-70B-Instruct-Turbo | ~0% | ~0% | ~0% | ~0% |
| **Classical algorithms (L*, TTT)** | **100%** | **100%** | **100%** | **100%** |

- **Performance degrades sharply with DFA complexity.** No LLM exceeds 25% success on 8--9-state DFAs; classical algorithms solve all instances.
- **Reasoning vs. non-reasoning gap is large.** In the 4--5 state range, Gemini 3.1 Pro (reasoning) achieves 85% success while GPT-5.4, Gemini Flash-Lite, and Llama-3.3-70B achieve 0%.
- **LLMs do not follow classical algorithms.** No model produces the same query sequence as L* or TTT. Gemini 3.1 Pro occasionally recovers with *fewer* queries than classical algorithms, indicating active problem-solving rather than memorization.
- **LLMs overuse equivalence queries.** Gemini 3.1 Pro exceeds the classical EQ bound (bounded by number of hidden DFA states) in 92.5% of task instances.
- **Monotonicity is violated.** Gemini 3.1 Pro produces non-monotonic hypothesis size sequences in all interactions (classical algorithms always test progressively larger hypotheses).
- **Non-informative queries accumulate.** After ~60 interaction steps, even DeepSeek-V4-Pro issues non-informative queries ~20% of the time; classical algorithms maintain 0% by construction.
- **Efficiency gap on successful runs.** For 8--9-state DFAs, the best model (Gemini 3.1 Pro) uses ~45.8% more tool calls than TTT even when it succeeds.
- **Full evaluation cost: ~$1,200 for 480 runs** (~$2.50 per datapoint); up to 20 hours and $50 per run for large DFAs.

---

## Suggestions & Future Directions

1. **Extend beyond DFAs.** The framework could be applied to non-deterministic or stochastic environments, testing whether agents can identify probabilistic or ambiguous world models.
2. **Relax oracle assumptions.** Introduce noisy, partial, or delayed feedback -- replacing perfect equivalence query oracles with more realistic feedback signals.
3. **Weaker feedback than equivalence queries.** Replace the precise counterexample returned by an EQ with simpler signals (e.g., pass/fail only), making the task harder and more realistic.
4. **Use as a training environment.** The procedural generation and formal evaluation make this framework suitable as a reinforcement learning environment for training agents to improve at interactive world model inference.
5. **Improve memory and planning.** The recurring non-informative query and reasoning failure results suggest that architectures with better long-horizon memory organization and strategic query planning could substantially improve performance.

---

## Authors & Institutions

Reef Menaged (Hebrew University of Jerusalem), Gili Lior (Hebrew University of Jerusalem), Shauli Ravfogel (New York University), Roee Aharoni (Google Research), Gabriel Stanovsky (Hebrew University of Jerusalem)
