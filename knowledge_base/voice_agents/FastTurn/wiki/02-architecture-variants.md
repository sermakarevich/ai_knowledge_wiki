> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# FastTurn Architecture Variants: Cascaded, Semantic, Unified

**In one sentence:** FastTurn builds turn detection in three steps — FastTurn-Cascaded routes a fast streaming CTC transcript into an LLM for low-latency decisions, FastTurn-Semantic adds Conformer acoustic embeddings via an LLM adapter to reduce transcript dependence, and FastTurn-Unified fuses Conformer-derived acoustic features with LLM hidden states in an MLP turn detector.

## Key points

- FastTurn consists of three components: FastTurn-Semantic, an acoustic adapter, and a turn detector.
- FastTurn-Cascaded introduces a CTC branch for fast alignment and greedy decoding to enable streaming transcription, formatted as a CTC prompt fed into the LLM (Qwen3-0.6B) for turn prediction with minimal decoding overhead.
- Cascaded predictions are sensitive to CTC errors under speech overlap and noise because the LLM input is dominated by the CTC transcript.
- FastTurn-Semantic projects Conformer encoder acoustic representations plus the CTC prompt into the LLM input space through an LLM adapter, so the LLM reasons over both and mitigates CTC errors while preserving early textual conditioning.
- FastTurn-Unified processes intermediate Conformer encoder hidden states through an acoustic adapter, fuses them with the LLM's hidden states, and forwards the result to a multi-layer perceptron turn detector that predicts whether the current speech segment is a complete turn.
- The framework is trained with a four-stage pipeline (semantic pretraining, modality alignment, joint training, modality fusion) that establishes speech-text alignment and combines prosodic and semantic cues.
- Joint training applies prompt dropout with probability p < 0.5, randomly dropping the CTC prompt to prevent overfitting to the CTC branch and preserve language modeling ability.

---

## FastTurn-Cascaded

FastTurn-Cascaded routes a fast CTC transcript to an LLM for low-latency decisions. Turn decisions rely on a transcript, but generating it introduces decoding latency; the CTC branch with greedy decoding enables streaming transcription. The transcription is formatted as a CTC prompt and fed into the LLM (Qwen3-0.6B) [20] for turn prediction.

> "However, as the LLM input is dominated by the CTC transcript, predictions are sensitive to CTC errors, especially in the presence of speech overlap and noise."

## FastTurn-Semantic

FastTurn-Semantic extends the Cascaded design by incorporating speech-derived features into the LLM to reduce reliance on transcript quality. The Conformer encoder extracts high-level acoustic representations, which along with the CTC prompt are projected into the LLM input space through an LLM adapter. The LLM then uses both for turn-related reasoning.

> "This approach allows FastTurn-Semantic to mitigate CTC errors while preserving the latency advantage of early textual conditioning."

## FastTurn-Unified

FastTurn-Unified fuses semantic and streaming acoustic cues before the final decision. Intermediate hidden states from the Conformer encoder are processed by an acoustic adapter to extract fine-grained acoustic features, fused with the LLM's hidden states, and forwarded to the turn detector (a multi-layer perceptron) predicting whether the current speech segment is a complete turn.

> "By combining streaming acoustic cues from CTC, LLM-conditioned semantic modeling, and acoustic-semantic fusion, the framework improves turn prediction when lexical evidence is ambiguous and prosodic cues are critical, while maintaining efficient inference."

| Variant | LLM input | Decision mechanism |
|---|---|---|
| FastTurn-Cascaded | CTC prompt only → LLM (Qwen3-0.6B) | LLM turn prediction from transcript |
| FastTurn-Semantic | CTC prompt + Conformer embeddings via LLM adapter → LLM | LLM turn reasoning over text + acoustics |
| FastTurn-Unified | Conformer intermediate states via acoustic adapter fused with LLM hidden states | MLP turn detector on fused features |

## Four-stage training pipeline (overview)

| Stage | What happens (per chunk) |
|---|---|
| Semantic pretraining | Train Conformer encoder + CTC branch on ASR data; fine-tune LLM on text-only data with turn state inserted as a special token to reduce generated tokens |
| Modality alignment | Train LLM adapter under ASR objective to map encoder outputs into LLM input space |
| Joint training | Jointly train LLM + LLM adapter conditioned on acoustic embeddings and CTC prompt, with prompt dropout (p < 0.5) |
| Modality fusion | Train acoustic adapter + turn detector on the same dataset, combining Conformer representations with LLM hidden states |

**Covers:** Section 2 (2.1 Architecture: Cascaded / Semantic / Unified; 2.2 training pipeline overview) plus Figure 1 architecture diagram
