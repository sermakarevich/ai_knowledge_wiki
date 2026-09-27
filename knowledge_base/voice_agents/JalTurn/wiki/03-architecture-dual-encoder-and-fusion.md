> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Architecture: dual encoders, fusion, and classifier
**In one sentence:** JAL-Turn jointly models turn-taking with a frozen SenseVoice encoder for high-level semantic/linguistic cues and a frozen CPC encoder for low-level acoustic regularities, fused via cross-attention and processed by an ALiBi Transformer, temporal pooling, and a sigmoid classification head.
## Key points
- Dual-path encoders produce frame-level features `hl = EncoderSense(x)` with `d1 = 512` and `ha = EncoderCPC(x)` with `d2 = 256` from waveform `x ∈ R1×L`, then map them via linear projections into a shared latent space.
- Both CPC and SenseVoice encoders are kept frozen during training to preserve pre-trained knowledge; SenseVoice emphasizes high-level semantic/linguistic elements while CPC emphasizes low-level acoustic regularities via self-supervised contrastive learning.
- The SenseVoice encoder is shared between ASR and JAL-Turn, so turn-taking predictions are computed synchronously with ASR in parallel from a single forward pass of the shared encoder with no extra stages before or after ASR decoding.
- Fusion uses `L = 2` stacked cross-attention layers where SenseVoice features act as queries and CPC features serve as keys/values, with `Q = LayerNorm(h′l)`, `K/V = LayerNorm(h′a)`, model dimension `d = 256`, and `H = 4` heads plus residual connections and position-wise FFN.
- On top of the fused representation sits a causal self-attention Transformer using Attention with Linear Biases (ALiBi), which adds a distance-dependent bias to attention logits, aids length extrapolation, and encodes a recency bias suited to local turn-taking patterns.
- An attention-based temporal pooling layer computes `αt = softmax(w⊤ht + b)` and `hpool = Σt αt · ht` to focus on the most informative segments before a linear head outputs shift logit `ŷ` with sigmoid activation and a fixed `τ = 0.5` hold-vs-shift threshold trained with binary cross-entropy (`1` = shift, `0` = hold).
---
## Dual-path encoders
**Covers:** Section 3.1-equivalent; input waveform through frozen encoders and shared-latent projection

| Item | Value |
|---|---|
| Input | waveform `x ∈ R1×L`, `L` = waveform length |
| SenseVoice output | `hl = EncoderSense(x) ∈ RT1×d1`, `d1 = 512` |
| CPC output | `ha = EncoderCPC(x) ∈ RT2×d2`, `d2 = 256` |
| Training status | both encoders frozen |
| Projection | linear layers into a shared latent space |

> "The secondary encoder is a pretrained contrastive predictive coding (CPC) model [22], which emphasizes low-level acoustic regularities via self-supervised contrastive learning."
> "Overall, this design allows JAL-Turn to jointly exploit high-level linguistic cues from SenseVoice and fine-grained acoustic patterns from CPC, yielding richer and more informative representations for turn-taking detection."
> "Importantly, the SenseVoice encoder is shared between ASR and JAL-Turn, enabling turn-taking predictions to be computed synchronously with ASR during inference."

## Cross-attention-based fusion
**Covers:** Section 3.2; L = 2 stacked cross-attention layers

SenseVoice features `h′l` act as queries; CPC features `h′a` serve as keys and values:

`CrossAttn(Q, K, V) = softmax(QK⊤ / √dk) V` (4)
`Q = LayerNorm(h′l)` (5)
`K/V = LayerNorm(h′a)` (6)

where `dk = d/H`, with `d = 256` and `H = 4`. Each layer additionally incorporates residual connections and a position-wise feed-forward network (FFN).

## Transformer-based module
**Covers:** Section 3.3; causal self-attention with ALiBi

> "Notably, we adopt Attention with Linear Biases (ALiBi) [23] as the positional bias mechanism, which replaces conventional absolute positional embeddings by adding a distance-dependent bias directly to the attention logits."
> "The intuition behind is that ALiBi has been shown to improve length extrapolation and naturally encodes a recency bias, which aligns well with the local temporal patterns that govern turn-taking behavior."

## Attention-based temporal pooling
**Covers:** Section 3.4; utterance-level representation over `htt = 1T`

`αt = softmax(w⊤ht + b)` (7)
`hpool = Σt=1T αt · ht` (8)

where `w ∈ Rd` and `b ∈ R` are trainable parameters, and `αt` denotes the normalized attention weight for time step `t`.

## Classification head and training objective
**Covers:** Section 3.5; shift logit, threshold, loss

Given `hpool ∈ Rd`, a lightweight linear head with `wcls ∈ Rd` and `bcls ∈ R` produces shift logit `ŷ ∈ R`; probability via sigmoid; decision hold vs. shift with fixed threshold `τ = 0.5`. Trained end-to-end with standard binary cross-entropy over mini-batches, `y ∈ {0, 1}` (`1` for shift, `0` for hold).

## Baseline systems noted in chunk tail
**Covers:** chunk-trailing fragment (comparison setups spilling into experiments)

- Three baselines named: an option "fed into the LLMs for turn-state prediction", and "(3) an SLM-based system, represented by EasyTurn [17], which performs turn-taking detection using a speech language model backbone."
- LLM baselines: "GPT-5.1 and Gemini-2.5-Flash are evaluated via their official APIs, whereas Qwen3-0.6B is fine-tuned on the training data and served with vLLM10 [24] for efficient inference."
- "All LLM-based experiments use the same prompt, provided in Appendix ??."
