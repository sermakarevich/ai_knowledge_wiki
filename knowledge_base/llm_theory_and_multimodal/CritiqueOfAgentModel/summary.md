# Critique of Agent Model

**Paper:** [Critique of Agent Model (Eric Xing, Mingkai Deng, Jinyu Hou, 2026)](https://arxiv.org/abs/2606.23991)

## Human Readable TL;DR

Most AI "agents" today are like fancy recipe-followers: they're very good at executing steps someone else laid out, but they have no real inner compass of their own. This paper argues there's a fundamental difference between a system that follows a script (even a clever one) and a system that genuinely decides for itself what it wants, who it is, and how to learn from experience. The authors propose a new blueprint -- the GIC architecture -- that tries to build AI with real inner workings: its own persistent goals, an evolving sense of self, a mental simulator to imagine the future, and the ability to decide when to think hard vs. act quickly.

## TL;DR

The paper distinguishes "agentic" systems (competent at externally scaffolded workflows) from "agentive" systems (capabilities arising endogenously). The authors analyze current AI agents across five dimensions -- goal, identity, decision-making, self-regulation, and learning -- and show all current categories fall short of genuine agency. They propose the Goal-Identity-Configurator (GIC) architecture combining hierarchical goal decomposition, adaptive identity evolution, a separately trained world model for simulative planning, a learned configurator for resource-aware deliberation, and continuous self-directed learning. Three theorems formalize the advantages of fast-slow identity learning, world-model-based planning, and logarithmic MPC horizon scaling.

---

## Problem & Motivation

Current AI systems marketed as "agents" achieve results through external engineering scaffolding (tools, prompts, orchestrated workflows) rather than internal organization. The paper asks: where does automation end and true agency begin? The concern is practical: scaling enumerated behaviors and harness engineering "will not allow AI systems to scale to biological agent diversity." Long-horizon tasks (e.g., managing a project over a year) are beyond reach when goals are supplied step-by-step and identity is fixed at design time. The paper seeks architectural principles -- not just performance benchmarks -- that separate genuine agency from sophisticated task automation.

---

## Main Original Ideas

1. **Agentic vs. Agentive Distinction.** Agentic systems have competence in externally designed workflows; agentive systems possess capabilities that emerge endogenously within the model. The formal agent model is π(a|s,g,i) -- a policy conditioned on world state, goals, and identity -- with a strict separation from the world model (state transitions).

2. **Five-Dimensional Analysis Framework.** Agency is analyzed across goal structure (step-by-step vs. hierarchical), identity (static vs. evolving), decision-making (reactive vs. simulative), self-regulation (fixed workflows vs. learned configurator), and learning (externally scheduled vs. self-directed). Current systems -- including LLM wrappers (AutoGen, DeerFlow), LLM-centered systems (Claude Code, SIMA-2), and embodied-model systems (Figure AI, Waymo) -- fail one or more dimensions.

3. **Fast-Slow Identity Learning (Theorem 1).** A two-timescale identity system outperforms slow-only updates. Fast updates revise the self-model i_t at each step (no retraining); slow updates modify parameters θ_t. Formal result: cumulative regret of the fast-slow agent ≤ slow-only regret minus Ω(∑N_k), a gap that grows with interaction steps and update rounds.

4. **World-Model-Based Planning (Theorem 2).** Given a world model f with total variation prediction error ≤ ε, any baseline policy π can be augmented with f to produce π_mix with V(π_mix) ≥ V(π). Planning is invoked selectively -- only when the world-model-derived value exceeds the baseline by 2·ε_model -- ensuring non-degradation. This is formalized through the Simulation Lemma and Performance Difference Lemma.

5. **MPC Horizon Scaling (Theorem 3).** The horizon H required for model-predictive control to achieve value gap ≤ ε scales as O(log(1/ε)) with constant discount and cost bounds. This formalizes why fixed-depth planning overcommits to uniform reasoning regardless of task difficulty.

6. **GIC Architecture.** Six interacting components: Belief Encoder (h_h), Goal Decomposer (δ), Identity Evolver (ι), Configurator (κ / System III), Simulative Planner (π_f / System II), and Actor (α / System I). The configurator routes among modes (construct new plan / continue plan / act directly) using associative memory to cache plans. Training follows three phases: ground school (component pretraining), simulator hours (simulative RL in the world model), first flights (real-world deployment with live identity and parameter updates).

---

## Key Findings

| Dimension | Current Systems | Agentive Requirement |
|-----------|----------------|----------------------|
| Goals | External, step-by-step g_t | Persistent g + learned decomposer δ |
| Identity | Fixed prompts/configs | Adaptive i_t via evolver ι |
| Decision-making | Black-box policy / CoT | Simulative planning via world model f |
| Self-regulation | Fixed orchestration workflows | Learned configurator κ |
| Learning | Engineer-scheduled retraining | Self-directed, continuous |

- All current LLM agent categories (wrappers, LLM-centered, embodied) fail at least identity evolution, continuous self-directed learning, and explicit world model separation.
- Chain-of-thought reasoning is critiqued as "narrative plausibility rather than grounded dynamics" -- it conflates internal compute with genuine planning.
- Collapsing policy and world model into one network "undermines reliability of both" -- reward-driven action selection and fidelity-driven state prediction are incompatible objectives.
- Rule-based simulators are bounded by 3D engineering scope; learned world models can converge toward real-world dynamics as machine learning scales, analogous to the shift from hand-crafted features to learned representations.

---

## Suggestions & Future Directions

1. Develop GIC implementations with a separately trained world model integrated at inference time, validating the Theorem 2 construction empirically.
2. Build multi-agent GIC systems that self-organize coordination rather than relying on externally prescribed protocols.
3. Scale simulative (Phase 2) RL using efficient world model architectures to reduce real-world sample requirements.
4. Investigate safety mechanisms enabled by self-regulation: context-aware behavioral configuration (the "leisurely walk vs. sprinting for epinephrine" analogy) as a controllability lever.
5. Develop evaluation frameworks measuring agent growth over time (Phase 3 identity evolution) rather than static task benchmarks.
6. Explore whether identity grounding through agent's own deployed experience can replace the significant engineering cost of "harness engineering" in current systems.

---

## Authors & Institutions

Eric Xing, Mingkai Deng, Jinyu Hou -- Institute of Foundation Models, Mohamed bin Zayed University of Artificial Intelligence & Carnegie Mellon University (submitted June 22, 2026)
