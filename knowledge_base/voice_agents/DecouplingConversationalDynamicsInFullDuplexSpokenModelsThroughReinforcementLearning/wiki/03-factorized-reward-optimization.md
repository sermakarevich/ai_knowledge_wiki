> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Factorized Reward and Group-Based Optimization
**In one sentence:** DuplexPO uses a four-component factorized reward (turn-initiation, backchanneling, yielding-after-barge-in, pattern regularization) with bounded ranges plus a GRPO-style group-normalized objective applied only to tokens inside dynamics-critical windows.
## Key points
- Turn-initiation reward `R_on` targets turn initiation with an indicator-times-exponential-decay functional form and range [0, 1].
- Backchanneling reward `R_bc` targets backchanneling with an indicator-plus-max-overlap functional form and range [0, 1].
- Yielding-after-barge-in reward `R_off` is a negated clipped latency-penalty term with range [−1, 0].
- Pattern-regularization reward `R_reg` is a negated clipped weighted event-indicator sum with range [−1, 0].
- DuplexPO optimizes with a GRPO-style objective over sampled continuations within each dynamics-critical window, using group-normalized advantages rather than DPO-style preferences.
- Window advantage is `A_i,k = clip((r_i,k − μ_i) / (σ_i + ε), −5, 5)` (Eq. 9), with mean and std computed within the same window group.
- The loss is `L_GRPO = L_policy + β L_KL` (Eq. 10), applied only to sampled tokens inside the window with a KL penalty toward the rollout behavior policy.
- A DPO-style baseline built from pairwise preferences among continuations from the same window is reported as an ablation in Appendix J.
---
## Reward components: target behavior, functional form, range
| Component | Target behavior | Functional form (as in chunk) | Range |
|---|---|---|---|
| `R_on^i` | Turn initiation | `I[Ŝ_i ≠ ∅] exp(−τ_i² / 2σ_on(τ_i)²)` (rendering garbled in chunk) | [0, 1] |
| `R_bc^i` | Backchanneling | `I[Ŝ_i ≠ ∅] max_{t ∈ Ŝ_i} I[t ∈ B_i] + I[t ∈ B_i] e^{−αd(t,B_i)}` (rendering garbled in chunk) | [0, 1] |
| `R_off^i` | Yielding after barge-in | `−clip(max(0, ℓ_i − ℓ∗) / H_off, 0, 1)` (rendering garbled in chunk) | [−1, 0] |
| `R_reg^i` | Pattern regularization | `−clip(Σ_{k=1}^K β_k I[e_{i,k}], 0, 1)` (rendering garbled in chunk) | [−1, 0] |

> Note: the chunk's table rows are partially garbled by PDF extraction; component names, target behaviors, and ranges above are verbatim, while functional forms are the chunk's visible symbols and may be incomplete.

## Group-based optimization
DuplexPO uses a GRPO-style objective [Shao et al., 2024] to optimize sampled continuations within each dynamics-critical window. Per the chunk:

> "GRPO uses group-normalized advantages over the full set of sampled continuations, providing a denser and more stable optimization signal for dynamics-critical decisions than DPO-style preference optimization."

For window `i`, rewards are normalized across its sampled continuations to obtain a clipped group advantage:

```
A_{i,k} = clip((r_{i,k} − μ_i) / (σ_i + ϵ), −5, 5)   (9)
```

where `r_{i,k}` is the reward of the k-th continuation, and `μ_i`, `σ_i` are the reward mean and standard deviation within the same window group. A policy-gradient loss is then applied only to sampled tokens inside the window, with a KL penalty toward the rollout behavior policy:

```
L_GRPO = L_policy + β L_KL   (10)
```

A DPO-style baseline is implemented by constructing pairwise preferences among continuations from the same window, with the ablation reported in Appendix J.

## Data and training context in this chunk
- Fisher [Cieri et al., 2004] and Seamless-Naturalistic-HQ (Seamless) [Agrawal et al., 2025] provide natural two-party conversations with word-level timing; Fisher is closer to symmetric peer-to-peer conversation while Seamless contains more role-asymmetric, question-answer-oriented interactions.
- Training conversations, derived windows, and timing annotations are disjoint from evaluation conversations and annotations; reconstruction, filtering, and sampling details are in Appendix A.
- The training pipeline has four stages: pre-training, SFT, RL with DuplexPO, and speech-synthesis SFT; DuplexPO optimizes conversational dynamics with explicit rewards over dynamics-critical windows, then speech-synthesis SFT freezes all parameters except the speech generation module and trains streaming TTS on the same speech dataset [Du et al., 2024], with details in Appendices A and B.

## Evaluation framing in this chunk
- SDLMs are evaluated on conversational dynamics (turn-taking, backchanneling) and model intelligence (factual knowledge, instruction following, speech understanding, reasoning).
- Dynamics evaluation covers Fisher, Seamless, and Full-Duplex-Bench v3 (FDB-v3) [Lin et al., 2026a], reporting window-level initiation rate, onset MAE, and yield rate for full-turn and backchannel events (`<BOS>` occurrence, `<BOS>` timing error, timely `<EOS>` emission).
- FDB-v3 reports Turn-taking Latency, Voiced Interrupt Rate (VIR), and Yield Rate; VIR excludes onsets during internal user pauses and within the final 0.5s of a voiced user segment.
- A blinded matched-window LLM-as-a-Judge evaluation with Gemini 3.0 Pro compares DuplexPO with the SFT Baseline, with prompts and per-dimension results in Appendix F.

**Covers:** reward-component table (R_on / R_bc / R_off / R_reg) through §3.5 Group-based Optimization (Eqs. 9–10) into §4 Data and Model Training and §5–5.2 evaluation framing
