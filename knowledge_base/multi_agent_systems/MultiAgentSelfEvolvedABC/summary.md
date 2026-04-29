# Autonomous Evolution of EDA Tools: Multi-Agent Self-Evolved ABC

**Paper:** [Autonomous Evolution of EDA Tools: Multi-Agent Self-Evolved ABC (Cunxi Yu, Haoxing Ren, 2026)](https://arxiv.org/abs/2604.15082)

## Human Readable TL;DR

Chip-design software (the programs engineers use to turn a circuit idea into actual silicon layouts) has been hand-tuned by experts for decades, and one of the most important ones -- ABC -- has grown into a 1.2-million-line tangle that is extremely hard to improve. The authors set a team of AI agents loose on ABC's source code, letting them propose, compile, and test their own edits automatically, with a "referee" that mathematically proves each change still produces the correct circuit. After many cycles the AI team quietly made ABC about 8% better at its job -- faster chips, smaller area -- without a human writing a line of code. It's like a crew of robot mechanics continuously retuning an engine overnight, each specializing in one part, while a supervisor checks the dyno results.

## TL;DR

The paper introduces the first self-evolving logic synthesis framework in which multiple specialized LLM agents (all Claude Sonnet 4.5) autonomously modify the full 1.2M-line ABC EDA codebase under a unified QoR objective. A planning agent coordinates subsystem-specific coding agents (FlowTune, Mapper, Logic Minimization), each constrained to its own directory, with combinational equivalence checking (CEC) as a formal correctness gate between code edits and benchmark evaluation. Distributed evaluation on 87 CPU nodes across 8 synthesis flows and standard benchmarks (ISCAS, ITC'99, EPFL, VTR DSP, arithmetic) yields ~8.3% QoR improvement over the vanilla ABC baseline, with 8-9% average worst-negative-slack gains and 3-8% AIG node reductions. Total LLM spend was roughly $2,400, and agents converged to ABC's native C coding style.

---

## Problem & Motivation

EDA tools like ABC encode decades of expert heuristic design but are extremely hard to evolve: ABC alone spans >1.2M lines of deeply interdependent C across 4,000+ files, with many built-in heuristics (cut selection, refactoring conditions, cost estimates) statically designed and rarely revisited despite governing NP-hard decisions. Prior LLM-driven code evolution (AlphaEvolve, SATLUTION) worked on hundreds to tens of thousands of lines -- far below ABC's scale and without its multi-objective area/delay trade-offs. The paper addresses whether autonomous LLM agents can improve a full-scale, monolithic, multi-objective EDA codebase, unlocking QoR gains that are prohibitively expensive for humans to search manually.

---

## Main Original Ideas

1. **Repository-scale self-evolution of a real EDA tool.** First demonstration of LLM agents autonomously evolving a 1.2M-line production-grade logic synthesis system (ABC), pushing code-evolution far beyond prior kernel- or mid-scale-repo scope.

2. **Multi-agent subsystem decomposition.** Instead of one monolithic agent, specialized Claude Sonnet 4.5 coding agents are each bound to a specific ABC directory -- Flow Agent (`src/opt/flowtune/`), Mapper Agent (`src/map/mapper/`), Logic Minimization Agent (`src/base/abci/`) -- coordinated by a central Planning Agent. Directory locking prevents cross-subsystem conflicts and preserves architectural invariants.

3. **Knowledge-bootstrapping pre-evolution phase.** Before editing, an autonomous agent profiles ABC itself and relevant external prototypes (FlowTune, ML-augmented mappers, Orchestration), producing a structured tutorial, API reference, and flow explanations that seed the evolution loop. This one-time cost absorbs 79% of all tokens used.

4. **Formal correctness feedback via CEC.** Every candidate edit must pass ABC's combinational equivalence check (`cec`, `dsat`); sequential designs use BMC depth 1. Failures immediately abort the iteration and feed a counterexample back into planning. This gate keeps >90% of token spend on semantically valid code states.

5. **QoR-driven iteration with rollback and partial acceptance.** A scalar reward plus a detailed QoR delta vector (timing, post-buffer/sizing area, AIG nodes/depth, mapper estimates, per-pass deltas) decides whether to integrate, roll back, or conditionally keep a partial improvement (e.g., lower depth with slight area regression).

6. **Self-evolving rulebase.** The planner continuously evaluates subsystem-specific coding policies; rules that systematically block beneficial edits can be relaxed over time under global safety constraints, shifting the system from conservative to exploratory as it matures.

7. **Style-preserving agent output.** Agents converge to ABC's native header layout, naming, `Abc_Print` usage, and `module.make` conventions despite exposure to heterogeneous external repositories -- an empirical finding that makes agent-generated patches directly mergeable.

---

## Key Findings

**Quality-of-Result (normalized to vanilla baseline = 1.000; lower is better):**

| Configuration | Normalized QoR | Improvement |
|---|---|---|
| Vanilla baseline (FlowTune + AIG Syn + Map) | 1.000 | -- |
| Evo Map only | 0.988 | 1.2% |
| Evo AIG Syn only | 0.957 | 4.3% |
| Evo FlowTune only | 0.962 | 3.8% |
| Evo FlowTune + Evo AIG Syn | 0.924 | 7.6% |
| Evo FlowTune + Evo Map | 0.939 | 6.1% |
| Evo AIG Syn + Evo Map | 0.942 | 5.8% |
| **All Evo (full co-evolution)** | **0.917** | **8.3%** |

Additional findings:
- **Worst negative slack** improved ~8-9% on average, with 12-15% gains on EPFL arithmetic circuits.
- **Area-delay product** reduced ~8.3%, tracking the overall QoR.
- **AIG node counts** decreased 3-8% on arithmetic-heavy designs.
- **Post-mapping depth** decreased 4-6% via autonomously introduced depth-aware heuristics.
- **Complementary agent roles** observed: FlowTune agent strengthens upstream structural simplification; Orchestrate reduces mid-level redundancy; Mapper adds depth-sensitive tie-breakers.
- **Compute cost:** ~$2,400 total LLM spend; $60-80 per evolution cycle; 2-3 hours per iteration on 87 CPU nodes running 8 flows across all benchmarks.
- **Token distribution:** 68% initial ABC profiling, 11% external codebase profiling, 21% actual evolution cycles.
- **Code output:** ~45% of artifacts were C source (87,749 lines); remainder was Markdown, bash, Python, logs.
- **Agents excel at refinement, not invention:** reliably tune thresholds, add conditional heuristics, and improve scoring, but struggle to introduce wholly novel algorithms without existing invariant anchors -- failures there manifest as compile errors, segfaults, or subtle correctness violations.

---

## Suggestions & Future Directions

1. **Broader EDA domains.** Extend the multi-agent, correctness-gated methodology to physical design, verification, and high-level synthesis where similar monolithic codebases and multi-objective optimization exist.
2. **Stronger scaffolding for novel algorithms.** Current agents amplify existing priors effectively but falter at genuinely new paradigms; richer problem formulations or structured search spaces may unlock that capability.
3. **Reduce bootstrapping cost.** 79% of token spend is one-time profiling; reusable repository knowledge artifacts and incremental profiling could lower adoption cost for other tools.
4. **Richer correctness gates for sequential designs.** BMC depth 1 is a pragmatic but limited proxy; deeper bounded or unbounded sequential equivalence could enable evolution of sequential-only optimizations.
5. **Tighter human-agent collaboration.** The authors note agents rely on decades of human domain contributions; a principled mix of human-curated priors and agent exploration is an open design axis.
6. **Rulebase learning theory.** The self-evolving rulebase is introduced empirically; formal analysis of when to relax versus tighten policies remains open.

---

## Authors & Institutions

Cunxi Yu (NVIDIA Research; University of Maryland, USA), Haoxing Ren (NVIDIA Research, USA).
