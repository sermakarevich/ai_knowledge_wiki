# AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness

**Paper:** [AutoHarness: Improving LLM Agents by Automatically Synthesizing a Code Harness (Lou et al., 2026)](https://arxiv.org/abs/2603.03329)

## Human Readable TL;DR

Imagine hiring a chess player who knows brilliant strategies but keeps trying to move pieces in ways the rules don't allow -- like sliding a rook diagonally. Instead of replacing that player with a more expensive expert, you give them a pocket rulebook they wrote themselves by practicing against the board. AutoHarness does exactly this for AI game-playing agents: it lets a smaller, cheaper AI write its own "rulebook" code by trial and error, so it stops making illegal moves. The result is a cheaper AI that beats much more expensive ones, and in some cases the AI writes the entire game strategy as a program, so it plays for free with no AI calls needed at all.

## TL;DR

AutoHarness enables an LLM (Gemini-2.5-Flash) to automatically synthesize a code harness -- an action verifier or full policy -- through iterative code refinement guided by Thompson-sampling-based tree search and environment feedback. The synthesized harnesses achieve 100% legal action rates across 145 TextArena games, allowing Gemini-2.5-Flash+Harness to outperform the much larger Gemini-2.5-Pro on both 1-player and 2-player games. Pushed to its limit as a full code policy, the method surpasses GPT-5.2-High on 1-player games at near-zero inference cost.

---

## Problem & Motivation

LLM agents frequently attempt actions that are strictly prohibited by their environment, even when their strategic reasoning is sound. In the Kaggle GameArena chess competition, 78% of Gemini-2.5-Flash losses were caused by illegal moves, not poor strategy. Traditional mitigations -- fine-tuning on game trajectories or hand-coding action validators -- are expensive, brittle, and unscalable. The paper asks: can the LLM itself write the code that enforces the rules, closing the gap between its reasoning ability and its action legality?

---

## Main Original Ideas

1. **Code-as-Harness Framework.** The LLM generates its own "harness" code (an `is_legal_action()` verifier and a `propose_action()` generator) that wraps the agent, acting as a learned rejection sampler that filters out illegal moves before they reach the environment.

2. **Thompson-Sampling Tree Search over Programs.** Harness synthesis is formulated as a search problem over the space of programs. A tree of code hypotheses is maintained and expanded using Thompson sampling, balancing exploration of new logic structures with exploitation of partially working code, guided by legal-action accuracy as the heuristic.

3. **Iterative Critic-Refiner Loop.** Failed rollout steps and error messages are consolidated by a Critic module and passed to a Refiner LLM, which proposes targeted code improvements. This gradient-free optimization loop converges to 100% legal actions in an average of 14.5 iterations.

4. **Harness-as-Policy (Code-Only Agent).** The framework is pushed to its extreme: the LLM synthesizes the entire decision-making policy as pure Python code (using only standard libraries like numpy), eliminating all LLM calls at inference time and achieving near-zero test-time cost.

5. **Available-Moves Removal for Harder Evaluation.** The authors deliberately strip "Available Moves" hints from game observations, forcing the harness to deduce legal actions from the board state alone -- a more realistic and challenging setup.

---

## Key Findings

### Harness Synthesis

- Achieved **100% legal action rate** on all 145 TextArena games.
- Average convergence in **14.5 tree search iterations**; 19/32 key games converged in fewer than 10 iterations.
- Hardest games (Chess, Othello, GermanWhist, Cryptarithm) required up to 64 iterations but all converged.

### Agent Performance -- 2-Player Games (16 games)

| Agent | Overall Win Rate | Games Won (of 16) |
|---|---|---|
| **Gemini-2.5-Flash+Harness (ours)** | **56.3%** | **9** |
| Gemini-2.5-Pro | 38.2% | 5 |
| Gemini-2.5-Flash (vanilla) | -- | -- |

Against vanilla Gemini-2.5-Flash, the harness-augmented agent wins 12/16 games (64.8% win rate).

### Agent Performance -- 1-Player Games (16 games)

| Agent | Avg Reward | Approx. Test-Time Cost |
|---|---|---|
| **Harness-as-Policy (ours)** | **0.870** | **~$0** |
| GPT-5.2-High | 0.844 | ~$640 |
| Gemini-2.5-Flash+Harness (ours) | 0.745 | Low |
| Gemini-2.5-Pro | 0.707 | Moderate |
| GPT-5.2 | 0.635 | ~$640 |
| Gemini-2.5-Flash (vanilla) | 0.673 | Low |

- Harness-as-Policy outperforms all agents including GPT-5.2-High while costing essentially nothing at inference.
- The action-verifier harness alone lets Flash beat Pro in 8/16 games and tie in 5/16.

### Qualitative Insights

- Generated code is sophisticated: the Minesweeper harness implements constraint propagation with subset-rule deduction and probabilistic risk heuristics.
- The Chess harness synthesizes full UCI parsing, piece localization, and attack-checking logic from scratch.
- The method works without access to game source code -- only text observations and environment feedback.

---

## Suggestions & Future Directions

1. **Recursive Self-Improvement.** Distill the domain-specific expert harnesses back into the base LLM so the system becomes recursively self-improving -- each cycle of harness synthesis strengthens the model's internal rule-following.

2. **Reusable Harness Libraries.** Build up a library of reusable harness components across games, reducing the per-game synthesis cost and enabling transfer between similar environments.

3. **Multimodal and More Complex Games.** Apply AutoHarness to challenging multimodal environments such as Craftax and Terra Nova, where observations include images and the action spaces are richer.

4. **2-Player Harness-as-Policy.** Extend the full code-policy approach to 2-player games, which requires strategic reasoning about opponent behavior and may need MCTS-like search or code world models.

5. **Beyond Games.** The authors note the framework is applicable to any domain where LLM agents must operate under strict constraints -- robotics, software engineering, legal compliance, scientific experimentation.

---

## Authors & Institutions

Xinghua Lou (Google DeepMind), Miguel Lazaro-Gredilla (Google DeepMind), Antoine Dedieu (Google DeepMind), Carter Wendelken (Google DeepMind), Wolfgang Lehrach (Google DeepMind), Kevin P. Murphy (Google DeepMind)
