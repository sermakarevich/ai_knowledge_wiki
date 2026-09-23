[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Methodology: Uncertainty-Routed Activation Editing
**In one sentence:** AURA freezes the pretrained AED speech model and applies sparse scale-and-shift edits to decoder cross-attention heads, with static Hard-Concrete gates selecting where to edit and a dynamic token-level gate routing edits by cross-attention uncertainty features.
## Key points
- AURA targets decoder cross-attention heads where acoustic conditioning occurs, freezing all pretrained weights and learning only edits, to correct localized grounding failures without broad weight rewrites.
- Each head learns a scale vector `Ah` and bias vector `vh` with effective gates controlling additive/multiplicative/joint/no-op interventions, recovering the frozen output exactly when both gates are zero.
- Static Hard-Concrete gates with location parameter `log α` and stretch interval `(γ, ζ) = (−0.1, 1.1)` provide sparse head selection, initialized from `N(0, 0.012)` and driven to sparsity by an expected-L0 penalty.
- A dynamic per-head gate computed from three causal cross-attention features — Max-Prob (over-concentration), normalized Entropy (diffuse attention), and Shift (abrupt frame jumps) — modulates edits at every decoding step via a 4-scalar projection.
- The effective gate is the product of static and dynamic gates, separating where an edit may occur from when it should activate, so AURA stays mostly dormant during confident recognition and strengthens during unstable grounding.
- AURA is trained with standard ASR cross-entropy plus a ramped sparsity loss, adding only `2d + 6` scalars per decoder cross-attention head, keeping it in the ultra-efficient PEFT regime at roughly 500× fewer trainable parameters than LoRA.
- On non-speech audio AURA reduces hallucination rate from 89.18% to 1.94% without prior hallucination-head identification, and on imperfect-label corpora it approaches LoRA WER.
---
## Background: PEFT and static editing limits
**Covers:** Section I (Introduction tail) – Sections II.A–II.B

Prior analyses show attention heads specialize into distinct functional roles, and for speech models task adaptation and hallucination concentrate in a small subset of heads — motivating head-level activation edits over full-model updates.

Parameter-Efficient Fine-Tuning (PEFT) freezes the pretrained model and updates fewer parameters; LoRA is the standard example but still introduces millions of trainable parameters for large SFMs. The chunk defines a stricter ultra-efficient PEFT regime orders of magnitude smaller than LoRA, including BitFit (bias-only weight updates) and representation-editing methods (RED, LoReFT, JoLA) that transform activations rather than weights.

JoLA learns head-level scale-and-shift edits with static gates deciding which heads to modify, but applies the same intervention at every decoding step. The chunk states this is limiting because hallucinations are localized — the decoder may be grounded most of the time and drift only when cross-attention becomes unstable.

Verbatim claim:

> "This is limiting for hallucination mitigation, because hallucinations are often localized: a decoder may remain well-grounded for most of an utterance and only drift when the cross-attention pattern becomes unstable."

## Head-level activation editing backbone
**Covers:** Section II.B, Eq. (1)–(2)

Let `at,h ∈ Rd` be the decoder cross-attention head output at step `t` before output projection. Per head, AURA introduces scale `Ah ∈ Rd` and bias `vh ∈ Rd`:

`ãt,h = 1 + ĝt,h Ah ⊙ at,h + ĝt,h vh , (1)`

where effective gates `ĝ ∈ [0,1]` control the edits; zero gates recover the frozen output exactly.

Each edit type `i ∈ {1,2}` uses a static Hard-Concrete gate with location `log αh`, sampled during training as:

`gh = clip[0,1] σ((log αh + log u − log(1−u)) / τ)(ζ − γ) + γ, (2)`

with `u ∼ U(0,1)`, temperature `τ`, and `(γ, ζ) = (−0.1, 1.1)`; deterministic gate values are used at inference.

## Uncertainty-routed dynamic gating
**Covers:** Section II.C, Eq. (3)–(8)

AURA adds a per-step dynamic gate from the cross-attention distribution, motivated by approximately monotonic near-diagonal cross-attention during well-grounded recognition. Let `pt,h ∈ RS` be the distribution over `S` encoder frames and `πt,h = arg max_s pt,h,s (3)`.

Three causal features:

- `mt,h = max_s pt,h,s (Max-Prob), (4)` — over-concentration / attention-sink behavior
- `et,h = −1/log S Σ_s pt,h,s log pt,h,s (Entropy), (5)` — diffuse, weakly grounded attention
- `δt,h = 1/(S−1) |πt,h − πt−1,h| (Shift), (6)` — abrupt jumps; strictly causal via a buffered previous argmax reset per utterance

Lightweight per-head projection (4 scalars, zero-initialized, single projection rather than MLP):

`g_dyn_t,h = σ(wh⊤ [mt,h, et,h, δt,h] + bh), (7)`

Effective gates:

`ĝt,h = gh · g_dyn_t,h, i ∈ {1,2}. (8)`

Unlike head-targeted hallucination methods, AURA needs no prior head-identification stage; it learns sparse selection and token-level routing jointly.

## Training objective and cost
**Covers:** Section II.D, Eq. (9)–(10)

All pretrained weights stay frozen; loss is standard ASR cross-entropy plus expected-L0 sparsity on static gates:

`Lsparsity = 1/N Σ_h Σ_i σ(log αh − τ log(−γ/ζ)), (9)`

`Ltotal = LCE + λt Lsparsity, (10)`

with `λt` ramped during training. The dynamic gate is not directly sparsity-regularized. Per-head cost: `2d + 6` scalars (scale, bias, two static-gate parameters, four dynamic-gate parameters).

Reported efficiency and headline results in this chunk:

| Claim | Numbers |
|---|---|
| Non-speech hallucination (Table I, Whisper-Large-v3, UrbanSound8K) | Zero-shot HRnorm 89.18 / HRraw 98.00; AURA (15 epochs) HRnorm 1.94 / HRraw 1.97; AURA (25 epochs) 0.93 / 0.93 |
| Clean-speech preservation (Table I, LibriSpeech WER %) | Zero-shot WERclean 1.91 / WERother 3.57; AURA (15 epochs) 2.29 / 3.65; AURA (5 epochs) 2.05 / 3.59 |
| Controlled ablation JoLA (same placement/budget, no routing) | JoLA (5 epochs) 4.80 / 4.88; JoLA (15 epochs) 2.01 / 2.02 with WER 4.11 / 4.36; JoLA (25 epochs) 0.97 / 0.97 with WER 15.21 / 18.65 |
| Parameter budget | AURA uses roughly 500× fewer trainable parameters than LoRA; Table II header states over two orders of magnitude fewer than LoRA and three to four orders fewer than full fine-tuning |

## Datasets, metrics, and baselines (as present in chunk)
**Covers:** Sections III.A–III.D (partial, through Table II header)

- Non-speech pool (~105 h): AudioSet 32 h, DEMAND 23 h, MUSAN 49 h, all with empty transcripts, chunked ≤30 s at 16 kHz mono; evaluated on UrbanSound8K (9 h) plus LibriSpeech test-clean/other for ASR preservation.
- Child imperfect-label: MyST 240 h conversational child speech, evaluated on harder unfiltered test set.
- Adult imperfect-label: TED-LIUM 3 450 h, trained on official set, evaluated on unfiltered test retaining blank/noisy alignments.
- Disfluent: FluencyBank 5-h Sep-28k subset, ≤30 s mono clips.
- Metrics: non-speech Hallucination Rate (HR) as fraction of non-empty hypotheses (HRraw whitespace-removed; HRnorm after Whisper English normalizer, so HRnorm ≤ HRraw); speech sets use normalized WER as indirect grounding stress metric.
- Baselines: zero-shot, full fine-tuning, LoRA (decoder self/cross-attention query+value adapters), BitFit (decoder cross-attention query/value/output biases), RED (decoder feed-forward affine), LoReFT (residual-stream low-rank), JoLA (matched no-routing ablation sharing placement, edits, data, budget, checkpoint rule).
