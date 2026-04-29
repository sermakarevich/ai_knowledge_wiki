# When Is Collective Intelligence a Lottery? Multi-Agent Scaling Laws for Memetic Drift in LLMs

**Paper:** [When Is Collective Intelligence a Lottery? Multi-Agent Scaling Laws for Memetic Drift in LLMs (Tanaka, 2025)](https://arxiv.org/abs/2603.24676v1)

## Human Readable TL;DR

Imagine a room full of people trying to agree on a name for something, but nobody has a preference. You might expect them to stay undecided forever -- but surprisingly, they always end up agreeing on one name anyway, purely by chance snowballing. It is like flipping coins in a crowd: one side gets a tiny random lead, others copy it, and soon everyone is saying the same thing -- not because it was the best choice, but because early luck compounded. This paper shows that AI chatbots talking to each other behave exactly the same way, and provides a formula predicting when agreement comes from genuine reasoning versus pure luck.

## TL;DR

This paper introduces Quantized Simplex Gossip (QSG), a minimal analytically tractable model that explains how LLM agent populations reach consensus through "memetic drift" -- a sampling-noise-driven mechanism analogous to genetic drift in neutral evolution. The authors derive scaling laws showing consensus time scales as mN^2/alpha^2 (where N is population size, m is communication bandwidth, alpha is adaptation rate) and identify a drift-to-selection crossover that determines whether consensus reflects luck or amplified bias. These predictions are validated empirically with GPT-4o and Claude Haiku 4.5 populations.

---

## Problem & Motivation

Multi-agent LLM systems are increasingly deployed in consequential settings (law, finance, healthcare, policy), yet it remains unclear whether their collective outcomes reflect genuine reasoning, systematic bias, or mere chance. Prior work showed that LLM populations can rapidly break symmetry and reach consensus in naming games even when no individual agent favors any label a priori, but the mechanism behind this was not understood. This paper fills that gap by providing a controlled, analytically tractable framework to distinguish between consensus driven by sampling noise ("lottery") and consensus shaped by systematic biases ("collective intelligence").

---

## Main Original Ideas

1. **Memetic Drift** -- By analogy with neutral genetic drift in population genetics, the authors identify a sampling-driven mechanism where discrete communication between agents injects stochasticity that compounds through mutual in-context learning, driving populations toward consensus even without any inherent preference.

2. **Quantized Simplex Gossip (QSG) Model** -- A minimal model where N agents maintain continuous belief distributions on a probability simplex but communicate through quantized (discrete) messages. The speaker samples from their belief, the listener updates toward the received message with adaptation rate alpha, and this mismatch between continuous beliefs and discrete communication is the engine of drift.

3. **Drift--Selection Scaling Laws** -- The paper derives closed-form scaling laws: consensus time t_cons ~ mN^2/alpha^2 (interaction steps), early drift rate ~ 1/N^2, and a crossover condition between drift-dominated and selection-dominated regimes as a function of population size N, communication bandwidth m, adaptation rate alpha, and internal uncertainty.

4. **Drift--Selection Crossover Framework** -- A quantitative framework predicting when weak biases (selection) are strong enough to overcome random drift. Larger populations and higher-bandwidth communication suppress drift, while stronger adaptation paradoxically makes the same weak bias less decisive by amplifying stochastic noise.

5. **Physics-Style Analysis of Multi-Agent LLM Systems** -- The paper proposes synthetic games paired with minimal models as a methodology for mechanistic understanding of collective LLM behavior -- a population-level counterpart to mechanistic interpretability.

---

## Key Findings

**Theoretical predictions validated empirically:**

| Prediction | GPT-4o | Claude Haiku 4.5 |
|---|---|---|
| Polarization U(t) follows mean-field form U(t) = 1 - (1 - 1/K) exp(-alpha^2 t / (mN^2)) | Confirmed with single fitted alpha across all N | Confirmed with single fitted alpha across all N |
| Early drift rate scales as ~1/N^2 | Confirmed across N = 2, 4, 8, 16, 32 | Confirmed across N = 2, 4, 8, 16, 32 |
| Consensus time scales as ~N^2 | Confirmed (quadratic fit matches data) | Confirmed (quadratic fit matches data) |

- In the **drift-dominated regime** (small N), the winning label is essentially random -- consensus is a lottery with each label winning ~1/K of the time regardless of any weak bias.
- In the **selection-dominated regime** (large N), even a small asymmetry (e.g., 9:1 initial bias in a cat-vs-dog naming game) is reliably amplified, and the biased label wins consistently.
- The crossover between regimes depends on the ratio of selection strength to drift strength, which scales with population size.
- Three communication modes were analyzed: **Hard** (single token, m=1), **Top-m** (m tokens), and **Soft** (full distribution) -- Soft communication eliminates drift entirely, confirming that quantized communication is the essential noise source.
- QSG simulations match LLM experimental trajectories in polarization dynamics, early drift rates, and consensus times.

---

## Suggestions & Future Directions

1. **Structured networks** -- Extend the analysis beyond fully connected (well-mixed) populations to realistic network topologies, which may create local consensus pockets or alter drift dynamics.

2. **Heterogeneous agents** -- Study populations with agents of varying capabilities, biases, or adaptation rates, rather than homogeneous populations.

3. **Training-data priors as selection forces** -- Investigate how pre-training biases act as selection pressures in collective dynamics and whether they compose predictably.

4. **Alignment composition under social interaction** -- Determine whether a society of individually aligned agents can still produce misaligned collective outcomes -- a key safety question.

5. **Population-level sycophancy** -- The framework highlights a failure mode where strategically injected or socially reinforced signals steer groups toward distorted conventions, analogous to sycophancy at the individual level.

6. **Beyond the "ideal gas" approximation** -- The authors position QSG as analogous to the ideal gas law in thermodynamics: a deliberately simplified starting point. Future models should incorporate richer agent-level dynamics, memory effects, and structured interactions.

---

## Authors & Institutions

Hidenori Tanaka -- CBS-NTT Program in Physics of Intelligence, Center for Brain Science, Harvard University; Physics of Artificial Intelligence Group, NTT Research, Inc.
