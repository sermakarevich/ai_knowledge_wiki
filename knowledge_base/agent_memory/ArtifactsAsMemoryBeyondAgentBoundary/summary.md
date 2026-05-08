# Artifacts as Memory Beyond the Agent Boundary

**Paper:** [Artifacts as Memory Beyond the Agent Boundary (Martin, Mince, Saleh, Pajak, 2026)](https://arxiv.org/abs/2604.08756)

## Human Readable TL;DR

Imagine you're navigating an unfamiliar city and someone has left chalk arrows on the sidewalk -- you no longer need to remember every turn you've taken because the environment remembers it for you. This paper proves mathematically that AI agents can do the same thing: by reading "breadcrumbs" left in the world, they need less internal memory to accomplish their goals. The researchers tested this in a maze-navigation task, showing that an AI with a small brain plus visible footprints can outperform a bigger-brained AI navigating a clean floor. The upshot: smarter environments can substitute for smarter agents.

## TL;DR

This paper formalizes the situated cognition hypothesis -- that the environment can serve as an agent's external memory -- within Reinforcement Learning. The authors define "artifacts" as observations that provide provable information about an agent's past, prove the Artifact Reduction Theorem (artifacts reduce the mutual information needed to represent history), and empirically show that both Linear Q-learning and DQN agents achieve higher performance with less internal capacity when observable spatial paths or landmarks are present.

---

## Problem & Motivation

Traditional RL treats memory as a purely internal resource (recurrent states, replay buffers, network weights). Cognitive science has long hypothesized that intelligent behavior instead relies on a tight coupling between internal processes and environmental resources -- but this idea had no rigorous mathematical formulation in RL. The paper fills this gap: it asks *how much* internal memory an agent can offload to observable environmental structures, and provides both formal definitions and empirical evidence.

---

## Main Original Ideas

1. **Artifact (Definition 1)** -- An observation `o` is an artifact if observing it at time `t` provides certainty (`P = 1`) that some distinct observation `o'` occurred at an earlier time `t' < t`. This formalizes environmental objects that encode the past.

2. **Artifactual Environment (Definition 2)** -- An environment containing at least one artifact; the paper proves an equivalent probabilistic characterization via Lemma 1.

3. **Artifact Reduction Theorem (Theorem 1)** -- For any history containing an artifact, there exists a shorter history (one observation removed) that carries identical mutual information about the next observation: `I(O_{t+1}; H) = I(O_{t+1}; H')`. Corollary 1 extends this to multiple artifacts, enabling cascaded reductions.

4. **Artifactless Copy (Proposition 1)** -- For any artifactual environment, a control "artifactless copy" can be constructed by injecting noise into artifactual relationships (`P ≤ 1 − ε`), enabling controlled comparison.

5. **External Memory (Definition 3)** -- An agent externalizes memory if a strictly lower-capacity agent achieves strictly lower performance in the artifactless copy. The capacity gap `C' − C` is an upper bound on externalized memory, giving a quantitative measure.

---

## Key Findings

### Memory Externalization Summary

| Experiment | Artifact Type | Learner | Externalization Observed? |
|---|---|---|---|
| 1 | Optimal Path (shortest) | Linear Q-learning | Yes -- C=16 beats No-Path C=64 |
| 1 | Optimal Path | DQN | Yes -- at 3×16 and 3×32 hidden units |
| 2 | Suboptimal Path | Linear + DQN | Yes (3 and 2 instances) |
| 2 | Misleading Path | Linear | Yes (2 instances) |
| 2 | Random Path | Linear + DQN | Yes (2 and 1 instances) |
| 2 | Landmarks (non-behavioral) | Linear + DQN | Yes (1 and 2 instances) |
| 3 | Dynamic Path (self-generated) | Linear | Yes -- C=256 satisfies condition |

- Low-capacity agents (e.g., 16 weights) in the No-Path condition typically fail to find the goal; the same agents with an observable path learn reliably.
- Landmarks (purely geometric structures, not goal-directed traces) also enable externalization -- the effect is not limited to behavioral signals.
- In the dynamic path experiment, agents self-generate a fading path through their own movement; externalization emerges without any explicit artifact-creation objective.
- The observed spatial artifacts satisfy Michaelian's (2012) three qualitative criteria for external memory: survival-relevant, susceptible to change, and subject to selection processes.

---

## Suggestions & Future Directions

1. **Principled artifact design** -- Develop methods to deliberately engineer environments that co-evolve with agents, substituting for internal memory rather than defaulting to larger networks.
2. **Adaptive capacity** -- Explore agents that dynamically adjust their use of external artifacts, turning environmental scaffolding on and off as needed.
3. **Richer artifact formalisms** -- Extend Definition 1 beyond total certainty (`P = 1`) to probabilistic artifacts (`P > threshold`), capturing noisier real-world signals.
4. **Multi-agent artifact ecology** -- Investigate how traces left by multiple agents interact (connecting to stigmergy literature) and how observational learning emerges from artifact accumulation.
5. **Ecological AI design** -- Treat environment structure as a first-class design variable alongside internal capacity, potentially enabling more resource-efficient systems.

---

## Authors & Institutions

John D. Martin (Openmind Research Institute; University of Alberta), Fraser Mince (Cohere Labs Community), Esra'a Saleh (Cohere Labs Community; Université de Montréal; Mila -- Québec AI Institute), Amy Pajak (Cohere Labs Community; University of Pennsylvania). Martin and Mince contributed equally.
