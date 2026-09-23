> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Data Preprocessing — Remove Non-Dialogue Sessions and Low-Quality Fragments
**In one sentence:** The chunk filters out non-dialogue sessions and low-quality utterance fragments to leave 24.6K Fisher and 43.1K Seamless training samples with leak-free session-level splits, then details acoustic augmentation, the Nemotron-VoiceChat-based training stack, SFT controls, AdamW schedules, the full Table 5 RL/reward hyperparameters, and the frame-level SIR/SRR metric definitions.
## Key points
- Non-dialogue sessions and low-quality utterance fragments are removed before sampling, leaving a processed training set of 24.6K Fisher samples and 43.1K Seamless samples.
- Splits are fixed at the conversation or session level before reconstruction so no evaluation conversation contributes SFT examples, RL windows, reward targets, or timing annotations; Fisher evaluation uses a held-out Fisher test SHAR view and Seamless evaluation uses a held-out eval-clean view.
- Training balances the two sources with a randomized round-robin sampler and truncates each sample at 210 seconds.
- Acoustic robustness combines SpecAugment on user speech features with waveform mixing from 10K Freesound/MUSAN noise clips, applied with probability 0.5 and SNR sampled uniformly between 0 dB and 60 dB.
- The stack builds on the Nemotron-VoiceChat recipe with the NeMo Toolkit, a Qwen2.5-7B-Instruct backbone, a frozen 600M-parameter causal Parakeet-based streaming encoder plus 1024-dim Transformer adapter, frozen CosyVoice2 codec/generator, 12.5 Hz encoder/LLM vs 25 Hz codec (two speech tokens per LLM frame), on 64 A800 80 GB GPUs.
- SFT follows speech-continuation pre-training with an instruction-QA + ASR-QA + synthetic-interruption mixture; SFT Baseline excludes dynamics-aware dialogue data while SFT Dynamics adds the Section 4.1 reconstructed dynamics-aware data as the data-matched control for DuplexPO.
- Optimization uses AdamW with β = (0.9, 0.98), weight decay 0, inverse-square-root schedule, peak LR 5 × 10−4 (pre-training, 2,500-step warm-up) and 5 × 10−5 (SFT), bfloat16 mixed precision, and gradient clipping to norm 1.0.
- Appendix C defines Suppressed Intent Rate (SIR, Eq. 11) and Suppression Release Ratio (SRR, Eqs. 12–13) at frame level on the agent text head for a⋆ ∈ {<BOS>, <EOS>} with intent threshold τ = 0.1 on a shared SFT-generated trajectory.
---
## Data filtering, splits, and sampling
**Covers:** data-pipeline tail (chunk pp. 16): "remove non-dialogue sessions and low-quality utterance fragments before sampling"

> "remove non-dialogue sessions and low-quality utterance fragments before sampling. The processed training set contains 24.6K Fisher samples and 43.1K Seamless samples."

| Fact | Value (verbatim) |
|---|---|
| Processed Fisher samples | 24.6K |
| Processed Seamless samples | 43.1K |
| Split unit | fixed at the conversation or session level before reconstruction |
| Leakage guard | "no evaluation conversation contributes SFT examples, RL windows, reward targets, or timing annotations" |
| Fisher evaluation view | held-out Fisher test SHAR view |
| Seamless evaluation view | held-out eval-clean view (not the naturalistic training split) |
| Source balancing | randomized round-robin sampler |
| Per-sample truncation | 210 seconds |

## Acoustic augmentation
**Covers:** acoustic augmentation paragraph (chunk p. 16)

- Feature level: "User speech features are augmented with SpecAugment".
- Waveform level: "the waveform stream is mixed with a curated set of 10K noise clips from Freesound [Fonseca et al., 2017] and MUSAN [Snyder et al., 2015]".
- "Noise is added with probability 0.5, with the signal-to-noise ratio sampled uniformly between 0 dB and 60 dB."

## Training details — implementation
**Covers:** Appendix B, Implementation (chunk p. 16)

- "The implementation builds on the released Nemotron-VoiceChat recipe [NVIDIA, 2026] and is trained with the NeMo Toolkit [Kuchaiev et al., 2019]."
- "We select a smaller language backbone Qwen2.5-7B-Instruct [Team, 2024] than Nemotron-VoiceChat."
- "Streaming speech is encoded by a 600M-parameter Parakeet-based encoder with causal convolutional context, followed by a 1024-dimensional Transformer modality adapter that maps acoustic features into the LLM embedding space [Koluguri et al., 2025, Rekesh et al., 2023]."
- "The speech codec and the streaming flow-matching generator follow CosyVoice2 [Du et al., 2024]."
- "The speech encoder and codec remain frozen during training."
- Timing grid: "The speech encoder and LLM advance at 12.5 Hz, whereas the audio codec runs at 25 Hz; each LLM frame therefore predicts two speech tokens to keep the text and audio streams temporally aligned."
- Compute: "All runs use 64 A800 80 GB GPUs."

## Training details — supervised fine-tuning
**Covers:** Appendix B, Supervised fine-tuning (chunk p. 16)

- "SFT is applied after speech-continuation pre-training to adapt the model to assistant-style spoken interaction."
- "The base SFT mixture uses the instruction-following QA data in Appendix A, together with ASR-QA and synthetic-interruption examples that expose the model to real acoustics and basic barge-in handling."
- "SFT Baseline uses this mixture and excludes dynamics-aware dialogue data."
- "SFT Dynamics keeps the same schedule but adds the reconstructed dynamics-aware dialogue data from Section 4.1, making it the data-matched SFT control for DuplexPO."

## Training details — optimization
**Covers:** Appendix B, Optimization (chunk p. 16)

| Setting | Value (verbatim) |
|---|---|
| Optimizer (pre-training, SFT, RL) | AdamW |
| β (pre-training and SFT) | (0.9, 0.98) |
| Weight decay | 0 |
| LR schedule | inverse-square-root |
| Pre-training peak LR | 5 × 10−4 after a 2,500-step warm-up |
| SFT peak LR | 5 × 10−5 |
| Precision | bfloat16 mixed precision |
| Gradient clipping | maximum norm of 1.0 |
| RL/reward hyperparameters | "summarized in Table 5" |

## DuplexPO RL and reward hyperparameters (Table 5)
**Covers:** Table 5 (chunk pp. 16–17): "DuplexPO RL and reward hyperparameters used for the reported run. Time values are in seconds unless otherwise noted."

| Group | Hyperparameter | Value | Role |
|---|---|---|---|
| Windowing | Frame duration ∆ | 0.08 | LLM decision grid |
| Windowing | Training lead time L | 1.0 | Context before annotated agent onset |
| Windowing | Training buffer B | 2.0 | Rollout region after annotated agent offset |
| Windowing | Validation lead / buffer | 2.0 / 2.0 | Wider evaluation context for testing early starts and yielding behavior |
| Windowing | Full-turn windows per conversation | 3 | Maximum sampled non-backchannel segments |
| Windowing | Backchannel windows per conversation | 1 | Maximum sampled backchannel segments |
| Rollout | Samples per window | 4 | GRPO group size for reward normalization |
| Rollout | Temperature / top-p | 1.0 / 0.9 | Sampling policy for continuations |
| Rollout | Maximum rollout steps | 200 | Maximum generated frames inside a window |
| Rollout | Rollout chunk size | 128 | Chunk size for rollout processing |
| Optimization | RL learning rate | 1 × 10−5 | AdamW learning rate |
| Optimization | Warm-up / minimum LR | 100 / 1 × 10−6 | Inverse-square-root schedule |
| Optimization | KL coefficient β | 0.2 | Regularization strength toward the reference policy |
| Optimization | Advantage clipping | [−5, 5] | Clip range for group-normalized advantages |
| Reward | Missed-event penalty | −0.5 | Penalty for failing to initiate a target event |
| Reward | False-alarm penalty | −0.5 | Penalty for unwarranted starts |
| Reward | Backchannel overlong penalty | −0.5 | Penalty for floor-grabbing backchannels |
| Reward | No-<EOS> penalty scale | 0.75 | Scale for failure to stop after user takeover |
| Reward | Observable margin | 0.16 | Margin for determining observable turn-end evidence |
| Reward | Interrupt grace | 0.16 | Grace period around user interruption |
| Reward | Stop tolerance | 0.24 | Allowed delay for yielding after target stop time |
| Reward | Explicit <EOS> bonus | 0.05 | Small bonus for explicit yielding |
| Reward | Near-target PAD penalty | −0.02 | Penalty for silence near a target start |
| Reward | Early / late stop penalties | −0.15 / −0.10 | Penalties for mistimed turn offset |

Note: the chunk repeats the full-turn (3) and backchannel (1) window rows twice with slightly different role phrasings ("Maximum sampled non-backchannel segments" / "Maximum number of sampled non-backchannel windows", and likewise for backchannel); both wordings are preserved above as one row each.

## SIR and SRR definitions (Appendix C)
**Covers:** Appendix C, "Definition of Suppressed Intent Rate (SIR) and Suppression Release Ratio (SRR)" (chunk pp. 16–17)

- Purpose: "To quantify a full-duplex agent's ability to start speaking when appropriate and to stop speaking when the user takes the floor, we introduce two complementary metrics."
- Scope: "Both are computed at the frame level on the agent's text head and are defined symmetrically for the two control actions a⋆ ∈ {<BOS>, <EOS>}."
- Policies: "Let πSFT and πRL denote the SFT and DuplexPO policies. Let pSFT_t(a) and pRL_t(a) denote the probability each policy assigns to token a at frame t."
- Shared context: "To isolate differences attributable to the policy head rather than to trajectory divergence, both quantities are evaluated on a single shared context, namely the SFT-generated trajectory. Let ŷSFT_t and ŷRL_t denote the corresponding arg max tokens."
- Intent rule: "We say that the SFT policy has an intent for action a⋆ at frame t when pSFT_t(a⋆) > τ, with τ a fixed threshold (we use τ = 0.1 throughout)."
- Frame sets: "We define F<BOS> = {t | ŷSFT_t = PAD} as the set of frames at which the SFT model remains silent, where the intent is the impulse to start speaking. We define F<EOS> = {t | ŷSFT_t ≠ <EOS> and the agent is mid-utterance at t} as the set of frames at which the SFT model continues speaking, where the intent is the impulse to stop speaking."
- SIR (Eq. 11): "SIR is the fraction of frames in Fa⋆ at which the SFT policy holds a latent intent for a⋆ but is overridden by a different action", SIRa⋆ = |{t ∈ Fa⋆ \| pSFT_t(a⋆) > τ}| / |Fa⋆|. "A higher SIRa⋆ indicates that the SFT model has internalised the relevant action intent at the representational level, yet its decision boundary fails to translate that intent into behaviour."
- SRR (Eqs. 12–13): suppressed set Sa⋆ = {t ∈ Fa⋆ \| pSFT_t(a⋆) > τ} (Eq. 12); "On this same frame set, SRR measures how often the RL policy actually takes action a⋆", SRRa⋆ = |{t ∈ Sa⋆ \| ŷRL_t = a⋆}| / |Sa⋆| (Eq. 13). "A higher SRRa⋆ indicates that RL's behavioural change is concentrated precisely on frames where the SFT model already exhibited a latent intent, rather than reflecting an indiscriminate shift toward more action-taking."

## Attention analysis note (Appendix D)
**Covers:** Appendix D, Attention Analysis opening (chunk p. 17)

> "This appendix provides additional analysis for the model behaviour analysed in Section 5. The attention statistics in Figure 4 and Table 6 should be read as supporting evidence about context usage, not as a mechanistic proof of the learned timing policy."
