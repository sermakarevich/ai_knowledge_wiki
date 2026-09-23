> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# 4.6 Training recipe: Realtime-Venus-Omni and Realtime-Venus-Audio
**In one sentence:** Realtime-Venus-Omni and Realtime-Venus-Audio share a single unified post-training pass for multimodal streaming that mixes full-duplex and offline turn-based formats with sparse response-only supervision, differing only in input modalities and data coverage.
## Key points
- One unified post-training pass supports video, audio-only, and text-only inputs and combines full-duplex and offline turn-based formats.
- Training data mixes proactive duplex data (including speech-in queries), delegation data, and general understanding data (detailed in Section 4.5).
- Realtime-Venus-Omni's user stream interleaves projected visual and audio tokens and uses both video and audio data; Realtime-Venus-Audio keeps only audio segments and trains on the audio group.
- Supervision is sparse: loss covers only response spans, excluding system, user, and media-placeholder tokens.
- In offline multi-turn data, assistant history is supervised together with the final turn; in full-duplex data, supervision covers per-second `<|listen|>`/`<|speak|>` decision tokens plus spoken text, with long replies supervised continuously across multiple units.
- Loss is normalized per sample (weighted loss divided by total supervision weight before batch averaging) so a sample's contribution does not scale with its supervised-token count.
- Long-answer LM-head cross-entropy is evaluated in chunks with recomputation to bound activation memory without changing the objective; undecodable or over-budget samples are discarded in preprocessing.
- Only the Thinker is updated; the acoustic decoder that synthesizes audible speech from Thinker hidden states stays fixed and is excluded from the objective.
---
## Unified post-training recipe
**Covers:** Section 4.6, unified recipe and data mix
- Realtime-Venus-Omni and Realtime-Venus-Audio "use a unified post-training recipe for multimodal streaming."
- Single post-training pass supports video, audio-only, and text-only inputs and combines full-duplex and offline turn-based formats.
- Mixes proactive duplex data (including speech-in queries), delegation data, and general understanding data, "as detailed in Section 4.5."
- "The two variants share the training recipe but differ in input modalities and training-data coverage."
## Modality handling per variant
**Covers:** Section 4.6, Omni vs Audio inputs
- Omni: "The user stream of Realtime-Venus-Omni interleaves projected visual and audio tokens, and the model uses both video and audio data."
- Audio: "In contrast, Realtime-Venus-Audio retains only the audio segments and is trained on the audio group."
## Supervision objective
**Covers:** Section 4.6, sparse supervision, normalization, Thinker-only update
- "Supervision is sparse: loss is computed only on response spans, excluding system, user, and media-placeholder tokens."
- Offline multi-turn data: "assistant history is supervised together with the final turn."
- Full-duplex data: "supervision covers the per-second <|listen|>/<|speak|> decision tokens together with the spoken text, and a long reply is supervised continuously across multiple units."
- "Loss is normalized per sample: each sample's weighted loss is divided by its total supervision weight before averaging over the batch, preventing its contribution from scaling with the number of supervised tokens."
- "For long answers, the LM-head cross-entropy is evaluated in chunks with recomputation, bounding activation memory without changing the objective."
- "Samples that fail to decode or exceed the length budget are discarded during preprocessing and excluded from training."
- "Only the Thinker is updated. The acoustic decoder, which synthesizes audible speech from Thinker hidden states, remains fixed and is excluded from the training objective."
