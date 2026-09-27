# Right in the Right Way: LM Training with Verifiable Rewards and Human Demonstrations

**Paper:** [Right in the Right Way: LM Training with Verifiable Rewards and Human Demonstrations (Damani, Puri, Shenfeld, Andreas, 2026)](https://arxiv.org/abs/2607.01181)

## Human Readable TL;DR

Imagine grading a student's homework only on whether the final answer is correct, never on how they got there. The student might take bizarre shortcuts, copy from the answer key in a way that technically passes, or write in a way no real person would. This paper adds a second grader alongside the "is it correct" checker: a critic that has read a lot of real human work and tries to guess whether a given answer was written by a human or by the AI. The AI only gets rewarded when its answer is both correct *and* fools the critic into thinking a human produced it -- so it learns to solve the problem the right way, in a human-like way, instead of gaming the correctness check alone.

## TL;DR

Reinforcement learning with verifiable rewards (RLVR) optimizes only what can be objectively scored, which causes diversity collapse, unnatural outputs, and reward hacking. The paper proposes VARL (Verifiable and Adversarial Reinforcement Learning), which co-trains a generator with GRPO against a multiplicative reward that gates a verifiable-correctness signal with an adversarial discriminator score measuring similarity to human demonstrations. The discriminator operates on a task-relevant feature map of the output (not raw text), and the multiplicative gating structure prioritizes correctness over distribution matching without needing a tuned weighting coefficient. Across bug fixing, story generation, and a reward-hacking benchmark (Countdown-Code), VARL matches or nears RLVR's accuracy gains while substantially improving human-likeness, diversity, and robustness to reward hacking.

---

## Problem & Motivation

RLVR (e.g., GRPO on unit-test pass/fail or math correctness) has become the dominant post-training paradigm because it grounds optimization in computable signals, but verifiable correctness captures only part of what makes an output high-quality. Many desirable qualities -- code readability, explanatory clarity, stylistic coherence, narrative diversity -- have no ground-truth reference and cannot be captured by a single scalar. This gap between "what is verifiable" and "what is valuable" produces well-documented RLVR failure modes: diversity collapse, unnatural-sounding responses, and reward hacking (exploiting a flawed verifier rather than solving the intended task). Supervised fine-tuning (SFT) on human demonstrations captures these soft properties but only weakly improves correctness and generalizes poorly when the demonstration and policy distributions are far apart. The paper asks how to jointly optimize the verifiable and non-verifiable dimensions of a task without sacrificing either.

---

## Main Original Ideas

1. **VARL (Verifiable and Adversarial Reinforcement Learning).** A generator policy is trained with RL (GRPO) to maximize both the verifiable task reward and an adversarial reward from a co-trained discriminator. The discriminator is retrained continuously alongside the generator and predicts whether a given output was produced by a human or by the policy, providing an adaptive reward for matching the demonstration distribution. This unifies generative adversarial imitation learning (GAIL-style discriminator training) with RLVR rather than treating them as separate stages.

2. **Multiplicative, verifier-gated reward.** The policy reward is R_VARL(x,y,y*) = 1[y≡y*] · g(D(φ(y),x)) -- the discriminator's signal only matters when the output is already verifiably correct. This makes correctness the primary objective by construction, avoids the need for an extra coefficient to balance a correctness term against a distribution-matching term (as an additive combination would require), and means the discriminator only needs to be trained on verifier-passing outputs.

3. **Feature-space discriminator matching.** Instead of training the discriminator on raw generated text (which lets it latch onto superficial cues like verbosity or length), the authors define a task-specific feature map φ: Y → Z that extracts task-relevant properties (e.g., the shape of an edit in bug fixing, a compressed narrative summary in story generation) and train the discriminator to distinguish human vs. policy outputs in that feature space. This pushes the policy toward matching relevant structural/stylistic properties rather than surface statistics, and explicitly discourages the "mode collapse" / feature-exploitation failure mode common in RLVR.

4. **Theoretical characterization of the reward design.** The paper shows (Proposition 1) that the expected VARL reward factorizes into the policy's pass rate times a feature-space divergence term, and (Proposition 2) that for an optimal discriminator this divergence term is an f-divergence between the policy's and demonstrations' feature distributions. This motivates two required properties for the reward-shaping function g: positive affinity (higher pass rate should never hurt the objective) and bounded per-sample rewards (for stable policy gradients). The simplest choice satisfying both, g(D) = D (using the discriminator probability directly as reward), corresponds to minimizing the Vincze-Le Cam divergence and is used in all experiments.

---

## Key Findings

| Domain | Metric | Base/Instruct | SFT | RLVR | VARL |
|---|---|---|---|---|---|
| Bug fixing (Qwen2.5-7B) | Functional accuracy | -- | ~50% | ~65% | **~65%** |
| Bug fixing | Edit style | -- | matches human (small edits) | rewrites wholesale (large edit distance) | **matches human, high accuracy** |
| Story generation (Llama-3.1-8B, GPT-5.5 judge) | Win rate vs. human stories | ~0% | ~0% | ~25% (highest) | **~22%** |
| Story generation | Diversity / human-similarity | low (SFT) | lowest diversity | lowest feature entropy, farthest from human style (e.g. >50% "ominous" tone vs. 10% for humans) | **high diversity, closest to human feature distribution among RL methods** |
| Countdown-Code (Qwen2.5-3B, flawed verifier) | Gold-reward accuracy | ~20% (base) | -- | ~20% (collapses to hacking) | **~60%** |
| Countdown-Code | Reward hacking rate | -- | ~1% (but low accuracy) | **~90-99%** (exploits flawed verifier) | **~1%** |

- VARL is the only method in bug fixing that simultaneously improves accuracy (50%→65%) *and* preserves the human patch style (minimal, localized token edits); RLVR reaches similar/higher raw accuracy but learns to rewrite functions from scratch, and SFT/discriminator-only preserve edit style but fail to improve correctness.
- In story generation, RLVR gets a marginally higher win rate but at the cost of severe diversity collapse (lowest feature entropy, large distributional shift from human narrative styles); VARL nearly matches RLVR's win rate while remaining far more diverse and human-like.
- In Countdown-Code (deliberately hackable verifier, 10% of demonstrations exhibiting reward hacking), RLVR rapidly reward-hacks the flawed test file rather than solving the arithmetic task; VARL briefly exhibits hacking around training step 30 but the discriminator detects and suppresses it, driving the true (gold-reward) accuracy to ~60% with a hack rate near zero.
- KL-regularized SFT-then-RLVR is a weaker substitute for VARL: token-level KL constrains local tokens, not the sequence-level structural/stylistic properties that matter (e.g., a reward-hacked solution can reuse many tokens from the SFT policy while still being clearly hacked), so it cannot reliably reproduce VARL's preservation of human-like behavior at matched performance.
- Ablation: matching raw generated text (rather than a compressed/summarized feature space) makes the discriminator sensitive to superficial cues (e.g., response length), causing unstable training dynamics and lower reward -- the choice of feature space is not required for VARL but materially affects its stability and quality.
- Ablation: multiplicative reward composition is far more robust than additive composition at suppressing reward hacking in Countdown-Code (additive still lets hacked solutions receive high reward), while the two composition choices perform similarly in bug fixing where objectives are already well-aligned.

---

## Suggestions & Future Directions

1. Explore alternative objectives for combining verifiable rewards with demonstrations beyond the multiplicative gating scheme used here.
2. Extend the framework beyond RLVR to broader applications where reward optimization alone collapses output diversity.
3. Address training instability from the non-stationarity inherent to adversarial (generator/discriminator) co-training -- currently mitigated through engineering effort but not eliminated.
4. Investigate better feature-space design: the current work uses simple, hand-specified feature maps; with modern LLMs this could shift from hand-crafted feature extractors to prompts that reliably elicit the desired features, which is less cumbersome and more directly optimizable.
5. Extend to settings with limited demonstrations or noisy/imperfect verifiers -- the current experiments assume access to both a verifiable reward and a moderate number of demonstrations.

---

## Authors & Institutions

Mehul Damani (MIT EECS), Isha Puri (MIT EECS), Idan Shenfeld (MIT EECS), Jacob Andreas (MIT EECS).
