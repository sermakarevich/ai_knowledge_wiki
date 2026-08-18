# Ask Early, Ask Late, Ask Right: When Does Clarification Timing Matter for Long-Horizon Agents?

**Paper:** [Ask Early, Ask Late, Ask Right: When Does Clarification Timing Matter for Long-Horizon Agents? (Gulati, Gupta, Lumer, Sen, Subbiah, 2026)](https://arxiv.org/abs/2605.07937)

## Human Readable TL;DR

Imagine giving a contractor a vague request to "build a deck." Should they ask "wood or composite?" before starting, halfway through framing, or after the railings are up? This paper proves that the answer depends on *what* they need to know -- asking about the goal ("what kind of deck?") only helps in the first 10% of the job, while asking about materials ("which wood?") still helps halfway through. After the midpoint, asking at all becomes worse than just guessing and continuing. The researchers also caught today's top AI models making this mistake -- some pestering with questions constantly, others never asking at all -- and none of them asking at the right moment.

## TL;DR

The authors introduce a forced-injection framework that supplies ground-truth clarifications at five controlled trajectory points (10%, 30%, 50%, 70%, 90%) across four information dimensions (goal, input, constraint, context), three benchmarks (MCP-Atlas, TheAgentCompany, SWE-Bench Pro), and four frontier models, totaling 6,000+ runs. They find that clarification value decays as a dimension-specific function of trajectory position: goal clarification collapses to baseline after 10% (pass@3: 0.78 -> 0.39), input clarification retains value through ~50%, and asking past mid-trajectory underperforms never asking. Cross-model Kendall tau correlations (0.78-0.87 within-benchmark, 0.34-0.67 across benchmarks) confirm timing profiles are task-intrinsic, and a parallel study of 300 unscripted sessions shows no frontier model asks within the empirically optimal window.

---

## Problem & Motivation

Long-horizon agents now execute hundreds of sequential actions in code repair, enterprise automation, and tool orchestration. When the user's instructions are incomplete, a wrong early assumption compounds into irreversible errors -- imagine an enterprise agent spending 30 actions building a calendar-quarter report when the user meant fiscal quarters. Prior work treated clarification as binary (ask or don't ask) and never measured how the *value* of clarification changes as a function of *when* it arrives during execution. This paper produces the first empirical demand curves for clarification timing, giving designers concrete targets for timing-aware policies.

---

## Main Original Ideas

1. **Forced-injection framework.** Rather than measuring whether agents detect ambiguity, the authors inject oracle-grade clarifications at precise, calibrated trajectory positions. This isolates the causal effect of *timing* on task success, decoupled from the agent's own ambiguity-detection ability.

2. **Information-dimension-specific value curves.** They show that the value-of-information decay profile is not uniform across information types. Goal clarification has a narrow front-loaded window; input clarification decays gradually; constraint and context have benchmark-dependent profiles. This directly contradicts the common "earlier is always better" intuition.

3. **Empirical demand curves as design targets.** The curves provide the quantitative foundation that theoretical frameworks (value-of-information theory, Bayesian experimental design) have assumed but never measured. They function as concrete design targets that timing-aware clarification policies can be evaluated against.

4. **Natural-ask alignment gap.** A complementary 300-session study shows current frontier models exhibit divergent failure modes -- GPT-5.2 asks in 52% of sessions, Claude Sonnet 4.5 in 23%, Gemini 3 Flash in 0% -- and none asks within the empirically optimal window. Claude asks less but more selectively (11% session success vs GPT-5.2's 3%).

---

## Key Findings

### Goal clarification has a narrow front-loaded window
| Condition | pass@3 |
|---|---|
| Oracle (upper bound) | 0.80 |
| **Inject at 10%** | **0.78** |
| Inject at 30% | 0.50 |
| Inject at 50% | 0.44 |
| Inject at 70% | 0.39 |
| Inject at 90% | 0.39 |
| No-clarification baseline | 0.40 |

After 70% of execution, goal clarification provides zero benefit over never asking.

### Input clarification decays gradually, recoverable through ~50%
| Condition | pass@3 |
|---|---|
| Oracle | 0.57 |
| Inject at 10% | 0.46 |
| Inject at 30% | 0.36 |
| **Inject at 50%** | **0.36** |
| Inject at 70% | 0.32 |
| Inject at 90% | 0.25 (below NC) |
| No-clarification baseline | 0.33 |

Agents partially compensate through environment exploration, explaining the gentler slope.

### Cross-model timing profiles are task-intrinsic
- Within TheAgentCompany (3 models, same variants): Kendall tau **0.78-0.87** (all p < 10^-5)
- Across all benchmarks (4 models, mixed coverage): Kendall tau **0.34-0.67** (all p < 0.01)
- Timing effects are substantially driven by task structure, not model identity.

### Natural-ask alignment gap (300 unscripted TheAgentCompany sessions)
| Model | Ask rate | Mean timing | Median timing | Per-session success |
|---|---|---|---|---|
| GPT-5.2 | **52%** | 43% | 50% | 3% |
| Claude Sonnet 4.5 | **23%** | 50% | 50% | **11%** |
| Gemini 3 Flash | **0%** | -- | -- | -- |

- 72% of first-ask events fall between 25-50% of trajectory -- past the goal-optimal window.
- Claude always asks exactly once when it asks; GPT-5.2 averages 1.71 ask-calls per asking session (max 5).
- Selective asking beats volume-asking on success rate.

### Wasted compute when clarification arrives late
| Benchmark | Inj-10 | Inj-30 | Inj-50 | Inj-70 | Inj-90 |
|---|---|---|---|---|---|
| TheAgentCompany (%) | 0.0 | 9.6 | 13.7 | 17.6 | 21.7 |
| MCP-Atlas (%) | 38.4 | 39.7 | 49.2 | 52.6 | 52.9 |
| SWE-Bench Pro (actions) | 0.7 | 4.3 | 5.0 | 8.3 | 10.4 |

### Methodology numbers
- 84 underspecified task variants across 3 benchmarks
- 7 conditions per variant (oracle, no-clarification, 5 injection timings), 3 trials each
- 6,048 forced-injection trials + 300 natural-ask sessions = 6,348 runs
- Temperature 0.0, max 4,096 tokens/turn, seeds 0/1/2, total API cost ~$4,200

---

## Suggestions & Future Directions

1. **Build timing-aware clarification policies** (supply-side mechanisms) that use these VOI curves as design targets. The authors cite the Chronos framework (Sen et al., 2026) as a natural next step.
2. **Extend forced-injection methodology** to other agent benchmarks with underspecified tasks beyond MCP-Atlas, TheAgentCompany, and SWE-Bench Pro.
3. **Investigate question quality vs frequency** trade-offs more rigorously. The observed Claude (11%) vs GPT-5.2 (3%) success-rate gap at different ask-rates is a hypothesis, not yet a controlled finding.
4. **Address limitations:** the study measures demand-side VOI but not supply-side detection; context dimension is underpowered (n=17 combined); behavioral confound exists between forced-injection (ask_user disabled) and natural-ask protocols; natural-ask coverage is limited to TheAgentCompany.

---

## Authors & Institutions

Anmol Gulati, Hariom Gupta, Elias Lumer, Sahil Sen, Vamse Kumar Subbiah -- all at PricewaterhouseCoopers U.S. Corresponding authors: anmol.b.gulati@pwc.com, elias.lumer@pwc.com.
