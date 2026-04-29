# AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness

**Paper:** [AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness (Lou et al., 2026)](https://arxiv.org/abs/2603.03329)

## Human Readable TL;DR

Imagine you have a brilliant chess player who knows great strategies but keeps accidentally making moves that break the rules -- like moving a rook diagonally. Instead of retraining the player from scratch, you give them a personal referee who checks every move before it's played. This paper shows how to automatically build that "referee" using the AI's own ability to write code. The referee catches illegal moves, tells the AI to try again, and the result is a cheaper AI that beats more expensive ones. In the most extreme version, the AI writes the entire game strategy as code, eliminating the need for the AI brain during actual play -- like a chess player writing down a complete playbook and handing it to a robot.

## TL;DR

AutoHarness uses an LLM's code-generation ability to automatically synthesize a code harness that validates action legality, preventing illegal moves in rule-based environments. Using iterative refinement with Thompson-sampling-guided tree search, Gemini-2.5-Flash+Harness achieves 100% legal actions across 145 TextArena games and beats Gemini-2.5-Pro (56.3% vs 38.2% win rate in 2P games). The harness-as-policy variant -- where the entire strategy is compiled to code -- achieves the highest 1P reward (0.870) at near-zero inference cost.

---

## Problem & Motivation

LLM agents frequently violate environment rules despite strong strategic reasoning. In the Kaggle GameArena chess competition, 78% of Gemini-2.5-Flash losses came from illegal moves, not bad strategy. Traditional mitigations -- fine-tuning or hand-coded harnesses -- are either expensive/slow or brittle/unscalable. The paper asks: can LLMs automatically generate their own rule-enforcement code?

---

## Main Original Ideas

1. **Code-as-Harness Framework** -- The LLM generates auxiliary code (an `is_legal_action()` function) that acts as an external verifier for its own proposed actions. Illegal actions trigger re-prompting with error feedback, functioning as a rejection sampler.

2. **Harness-as-Policy** -- Taken to the extreme, the LLM synthesizes the entire decision-making policy as executable Python code, eliminating LLM inference calls at test time entirely.

3. **Thompson-Sampling Tree Search for Code Refinement** -- An iterative refinement loop uses tree search guided by Thompson sampling to efficiently explore the space of code variants. Each node represents a code hypothesis scored by legal-action accuracy, balancing exploration of new logic structures against exploitation of partially working harnesses.

4. **Critic-Refiner Loop with Environmental Feedback** -- Failed rollouts produce error messages that a Critic consolidates and a Refiner (the LLM itself) uses to propose targeted code fixes, creating a self-correcting synthesis pipeline.

5. **Three Harness Modalities** -- The paper formalizes a spectrum: harness-as-action-verifier (primary), harness-as-action-filter (generates legal move sets for LLM ranking), and harness-as-policy (full code policy). This taxonomy clarifies the design space for externalizing LLM agent constraints.

---

## Key Findings

### Harness Synthesis

- Achieved **100% legal action rate** across all 145 TextArena games
- Average convergence in **14.5 tree search iterations**; 19/32 key games needed fewer than 10 iterations

### Two-Player Games (16 games)

| Agent | Overall Win Rate | Games Won |
|---|---|---|
| **Gemini-2.5-Flash+Harness (ours)** | **56.3%** | **9/16** |
| Gemini-2.5-Pro | 38.2% | -- |
| Gemini-2.5-Flash (vanilla) | -- | -- |

- Against vanilla Flash, the harnessed version won 12/16 games (64.8% win rate)

### One-Player Games (16 games)

| Agent | Avg Reward |
|---|---|
| **Harness-as-Policy** | **0.870** |
| GPT-5.2-High | 0.844 |
| Gemini-2.5-Flash+Harness | 0.745 |
| Gemini-2.5-Pro | 0.707 |
| Gemini-2.5-Flash | 0.673 |
| GPT-5.2 | 0.635 |

- Harness-as-Policy runs at **near-zero inference cost** (no LLM calls), vs ~$640 for GPT-5.2 experiments
- Flash+Harness beat Pro in 8/16 1P games, tied in 5

---

## Suggestions & Future Directions

1. **Harness-as-Policy for 2P games** -- Learning full policies for adversarial games remains challenging; the authors suggest it may require learning a code-based world model to handle opponent modeling.

2. **Recursive self-improvement** -- Distilling learned domain-specific harnesses back into the base LLM could enable continuous self-improvement cycles.

3. **Beyond text games** -- The framework is transferable to robotics (safety constraints), software engineering (code compliance), healthcare (guideline adherence), and legal/financial systems (regulatory compliance).

4. **Scaling to more complex environments** -- While 145 games demonstrate breadth, real-world environments have richer state spaces and partial observability that remain open challenges.

---

## Authors & Institutions

Xinghua Lou, Miguel Lazaro-Gredilla, Antoine Dedieu, Carter Wendelken, Wolfgang Lehrach, Kevin P. Murphy -- all at Google DeepMind.
