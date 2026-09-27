# Agentic Auto-Scheduling: An Experimental Study of LLM-Guided Loop Optimization

**Paper:** [Agentic Auto-Scheduling: An Experimental Study of LLM-Guided Loop Optimization (Merouani, Kara Bernou, Baghdadi, 2025)](https://arxiv.org/abs/2511.00592)

## Human Readable TL;DR

Imagine you have a very smart assistant who doesn't know how to drive but can suggest turns, and a car's navigation system that tells the assistant "that road is blocked" or "that route saved you 5 minutes." Together they find faster routes than the navigation system would alone. This paper does the same for computer programs: an AI suggests code speed-ups, a compiler checks if the suggestions are safe and measures improvement, and they iterate together -- no special training of the AI required.

## TL;DR

ComPilot is a closed-loop framework where an off-the-shelf LLM proposes loop transformation sequences to the Tiramisu compiler, which validates legality via polyhedral dependence analysis and returns empirical performance feedback. Without any task-specific fine-tuning, ComPilot achieves 2.66x geometric mean speedup (single run) and 3.54x (best-of-5) on PolyBench, outperforming the Pluto polyhedral optimizer on 119 of 150 benchmark instances.

---

## Problem & Motivation

Loop optimization on modern hardware is hard: compiler heuristics, polyhedral methods (Pluto), and autotuning frameworks all struggle to generalize across diverse applications and hardware configurations. Direct LLM code generation can produce semantically incorrect code without expensive formal verification. The question is whether off-the-shelf LLMs, grounded by iterative compiler feedback, can guide fine-grained loop transformation sequencing effectively.

---

## Main Original Ideas

1. **Agentic compiler interaction** -- The LLM acts as an optimization agent that proposes schedules (transformation sequences) to the compiler rather than rewriting code directly. The compiler handles legality (via polyhedral dependence analysis) and provides execution time feedback. This separates concerns: LLM reasons, compiler verifies.

2. **Nine-primitive transformation space** -- Loop Fusion, Shifting, Interchange, Parallelization, 2D Tiling, 3D Tiling, Unrolling, Skewing, and Reversal. The LLM proposes sequences of these primitives; the compiler determines feasibility parameters (e.g., skewing factors) automatically.

3. **Context initialization with anonymization** -- Loop nests are annotated with computation IDs; variable names are anonymized (a, b, c...) to prevent semantic bias. Chain-of-thought program analysis precedes transformation proposals.

4. **In-context learning via feedback** -- Full dialogue history (proposals + feedback) acts as episodic memory. Feedback is category-specific: invalid syntax, illegal transformation, solver failure, compiler crash, or successful speedup with metrics. No weight updates -- purely in-context adaptation.

5. **Multi-run stochasticity exploitation** -- Independent runs across the same instance are combined (best-of-K), converting LLM non-determinism from a bug into a feature for exploring the transformation search space.

---

## Key Findings

| Metric | Value |
|--------|-------|
| ComPilot@30 (single run, geomean) | **2.66x** (95% CI: [2.60, 2.77]) |
| ComPilot_5@30 (best-of-5, geomean) | **3.54x** (95% CI: [3.45, 3.58]) |
| vs. Pluto (best-of-5) | **2.94x** (outperforms on 119/150 instances) |
| vs. Tiramisu autoscheduler (8 benchmarks) | **3.23x** |
| Top instance: correlation_XLARGE | **339x** |
| Wall-clock per instance | ~8.9 min average |
| Runnable schedules | 36.1% |
| Invalid schedules | 31.4% |
| Illegal schedules | 32.5% |

- **Feedback ablation**: removing feedback drops geomean from 2.66x to 2.01x (~23% loss); best-of-5 gap is ~28%.
- **Direct code generation ablation**: 14-16% lower speedup, 5.3x more tokens, and 17.9% of "correct" outputs later found semantically wrong under random inputs.
- **Hardware context ablation**: providing CPU model/core/cache specs in prompts yields no statistically significant gain -- empirical feedback dominates.
- **CoT ablation**: removing initial program analysis loses ~8-14% depending on model; removing per-iteration reasoning has smaller but non-zero effect.
- **Pluto comparison detail**: ComPilot's advantage comes partly from avoiding regressions (Pluto sometimes slows small inputs); when Pluto is capped at no-regression, ComPilot's advantage falls from 2.94x to 1.78x.
- **LLM comparison** (T=30, single run): gemini-2.0-flash 2.66x > gpt-4o 2.63x > llama3.3-70B 2.47x > qwq-32B 2.36x > qwen2.5-coder-32B 2.14x > gemma3-27B 2.03x > codestral 1.75x. Instruction-following matters more than "reasoning" specialization.
- **Iteration scaling**: T=1 → 1.41x, T=10 → 2.15x, T=30 → 2.66x, T=75 → 3.06x. Diminishing returns after T=30.
- **Run scaling**: K=1 → 2.66x, K=5 → 3.54x, K=10 → 3.75x, K=13 → 3.82x. Most gain K=1→5.
- **Weakness**: Kernels with complex loop-carried dependencies (cholesky, durbin, ludcmp) show <5% runnable schedules and near-zero speedup with current primitive set.

---

## Suggestions & Future Directions

1. **Richer feedback signals** -- Include specific dependency violation details, hardware performance counter data (cache miss rates, vector utilization) beyond current speedup metrics.
2. **Hybrid search** -- Combine LLM guidance with systematic search algorithms (e.g., beam search, evolutionary methods) to escape local optima and cover the space more efficiently.
3. **Dialogue summarization** -- Context grows non-linearly (full history re-sent each turn); compression/summarization would reduce token cost and latency.
4. **Broader transformation space** -- Loop distribution, computation reordering, and other non-affine transformations could unlock improvements on dependency-heavy benchmarks.
5. **Backend generalization** -- The framework is backend-agnostic; adapt to GCC/Clang flag selection, LLVM pass orchestration, or tensor-level autoschedulers (TVM/Halide).

---

## Authors & Institutions

Massinissa Merouani, Islem Kara Bernou, Riyadh Baghdadi (institution not specified in paper metadata; paper under cs.PL, cs.DC, cs.LG, cs.PF categories).
