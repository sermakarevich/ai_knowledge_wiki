> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Dual-Track Streaming Architecture

**In one sentence:** Prompt-based LLM text normalization cannot meet streaming dialogue demands, so StreamTN uses a fine-tuned Qwen3-0.6B dual-track architecture that incrementally converts partial LLM outputs into TTS-readable text with controllable first-packet delay.

## Key points

- Prompt-based TN (e.g., PolyNorm few-shot LLM TN with a multilingual benchmark [16]) requires waiting for sufficient or complete context, adds latency, and risks unstable formatting or hallucinated outputs in cascaded spoken dialogue systems (SDS).
- In cascaded SDS the TN module must process partial LLM outputs and feed normalized text to the TTS module in real time, while both upstream LLM and downstream streaming TTS (cf. [17]) operate incrementally.
- An effective dialogue TN module must satisfy two requirements simultaneously: produce accurate TTS-readable text preserving pronunciation correctness and semantic consistency, and do so incrementally with low latency.
- Existing TN datasets focus on conventional NSW categories, offline sentence-level normalization, or multilingual TTS normalization, and miss the distribution, diversity, and latency requirements of real LLM dialogue responses.
- StreamTN is a lightweight Chinese streaming TN model built on Qwen3-0.6B [19] that decouples raw-text input tokens and normalized-text output tokens into two parallel tracks, starting normalization after only a small number of input tokens.
- Task-specific fine-tuning lets StreamTN learn structured normalization patterns without complex prompting and with reduced hallucination risk.
- A new Chinese dialogue-oriented TN benchmark covers 14 categories — numbers, dates, time, phone numbers, units, plus chemical formulas, mathematical equations, and scientific terms — evaluating accuracy, robustness, and streaming-inference latency.
- Emitting too early risks incorrect readings while waiting too long increases first-packet TTS latency, so StreamTN controls input lookahead with a fixed delay parameter while remaining compatible with standard autoregressive decoding.

---

## Prompt-based TN and its limits for cascaded SDS

Recent progress in LLMs has motivated prompt-based TN; PolyNorm explores few-shot LLM-based TN for TTS and introduces a multilingual benchmark covering diverse normalization phenomena [16].

Directly applying prompt-based LLMs to cascaded SDS remains challenging because:

- the TN module must process partial LLM outputs and provide normalized text to the TTS module in real time;
- prompt-based normalization usually requires waiting for sufficient or complete context;
- it introduces additional latency;
- it may still suffer from unstable formatting or hallucinated outputs.

> "In contrast, our goal is not only to improve TN accuracy, but also to enable streaming input processing and streaming output generation with controllable first-packet delay."

**Covers:** prompt-based TN limits; streaming input/output goal

## Streaming requirements in LLM-centered cascaded SDS

A key challenge is that both the upstream LLM response and the downstream TTS synthesis are expected to operate in a streaming manner, especially as recent TTS systems emphasize scalable and low-latency streaming synthesis [17].

In this setting the TN module is no longer a conventional offline preprocessing component; it must incrementally convert partial LLM outputs into TTS-readable text while preserving pronunciation correctness and semantic consistency.

An effective TN module for dialogue TTS should therefore satisfy two requirements simultaneously:

1. generate accurate and TTS-readable normalized text;
2. do so incrementally with low latency.

Offline TN can access the whole input sentence and use left and right context to disambiguate non-standard words (NSWs); streaming dialogue input instead arrives token by token from the LLM module, forcing a trade-off between emitting too early (incorrect readings) and waiting too long (higher first-packet TTS latency).

**Covers:** streaming SDS setting; two TN requirements; offline vs. streaming trade-off

## Benchmark gap for dialogue-oriented TN

Although dialogue-system evaluation has been broadly studied [18], existing TN datasets and evaluations mainly focus on conventional NSW categories, offline sentence-level normalization, or multilingual TTS normalization, and do not reflect the distribution, diversity, and latency requirements of real LLM-generated dialogue responses.

Dialogue-oriented TTS must handle not only numbers, dates, time, phone numbers, and units, but also increasingly frequent complex outputs involving scientific terms, chemical formulas, and mathematical expressions.

The proposed Chinese dialogue-oriented TN benchmark covers 14 categories, including numbers, dates, time, phone numbers, units, chemical formulas, and mathematical equations, and measures normalization accuracy, robustness across diverse dialogue outputs, and latency under streaming inference.

**Covers:** benchmark gap; 14-category dialogue benchmark scope

## StreamTN proposal and contributions

To address accuracy, robustness, and streaming-latency requirements, StreamTN is a lightweight LLM-based Chinese streaming TN model for cascaded SDS:

- built on Qwen3-0.6B [19];
- dual-track streaming architecture decouples raw-text input tokens and normalized-text output tokens into two parallel tracks;
- begins normalization after receiving only a small number of input tokens rather than waiting for the complete LLM response;
- task-specific fine-tuning learns structured normalization patterns while avoiding complex prompting and reducing hallucination risks.

Main contributions as stated:

- StreamTN, a dedicated Chinese streaming TN model with dual-track architecture enabling incremental input processing and output generation with controllable first-packet delay.
- A dialogue-oriented Chinese TN benchmark covering 14 categories of practical normalization scenarios.
- Experiments showing competitive normalization quality at low first-packet delay, improving further with additional context.
- Planned release of the trained StreamTN model and benchmark upon publication.

A demonstration is available online: https://supernova-neko.github.io/Stream-TN/

**Covers:** StreamTN proposal; four stated contributions

## Overall architecture: placement and streaming operation

As illustrated in Figure 1, StreamTN is inserted between the upstream LLM module and the downstream TTS module in a cascaded SDS: the LLM generates a textual response from the user's spoken query, and TN converts it into TTS-readable form before synthesis.

In conventional cascaded systems TN is usually a rule-based or lightweight neural module run after the complete textual response is available; StreamTN replaces this offline component and processes the LLM response incrementally, so normalized text can be passed to TTS before the full response is finished [20].

With the dual-track structure:

- the input track provides the currently available raw-text context;
- the output track carries the delayed normalized-text history;
- the model generates normalized tokens autoregressively while still consuming new raw tokens;
- when the LLM stream is active, both tracks are used; when the raw stream has ended, the input track is padded and generation continues from output history until the end-of-sequence token.

This keeps the TN model compatible with standard autoregressive decoding while input lookahead is controlled by a fixed delay parameter. The design is inspired by Qwen3-Omni [21] and delayed-stream modeling [22]; the two tracks' embeddings are fused before the Transformer backbone.

**Covers:** Section II.A, overall architecture and streaming operation

## Dual-track streaming formulation

Given upstream raw text `x = (x1, x2, ..., xn)` and normalized target `y = (y1, y2, ..., ym)`, a conventional autoregressive model learns `pθ(y | x)`, assuming the complete input is available before decoding. In streaming, only a prefix is observed at each decoding step.

Let `d` be the token-delay parameter controlling how many raw input tokens are observed before the first normalized token is emitted. Aligned states:

- Raw-input track: `x̄t = xt` for `1 ≤ t ≤ n`, `<pad>` for `t > n` (Eq. 1).
- Output-history track delayed by `d`: `ȳt = <delay>` for `1 ≤ t ≤ d`, `yt−d` for `d < t ≤ m + d`, `<pad>` for `t > m + d` (Eq. 2).

`<delay>` and `<pad>` are conceptual alignment symbols rather than learned vocabulary tokens: the former means output generation has not started, the latter means a track has ended. Both are realized as zero vectors after embedding:

- `Φ(u) = E(u)`, `Φ(<delay>) = Φ(<pad>) = 0` (Eq. 3), where `E(·)` is inherited from Qwen3-0.6B.
- Fusion by element-wise addition: `zt = Φ(x̄t) + Φ(ȳt)` (Eq. 4).
- Aligned length `T = max(n, m + d)`; the last fused position is removed during training and the sequence is processed with a causal mask: `h1:T−1 = Qwen3θ(z1:T−1; Mcausal)` (Eq. 5).
- Hidden state at aligned step `i+d−1` contains raw prefix `x≤min(n,i+d−1)` and history `y<i`, giving `pθ(yi | x≤min(n,i+d−1), y<i) = softmax(Wo hi+d−1 + bo)` (Eq. 6) and streaming factorization `pθ(y|x) = ∏i=1..m pθ(yi | x≤min(n,i+d−1), y<i)` (Eq. 7).

**Covers:** Section II.B, dual-track streaming formulation (Eqs. 1–7)
