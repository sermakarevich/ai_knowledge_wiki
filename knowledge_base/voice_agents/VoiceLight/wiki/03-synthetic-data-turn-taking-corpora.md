[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Synthetic Data and Turn-Taking Corpora

**In one sentence:** Synthetic timelines are rendered per-unit with Qwen VoiceDesign-conditioned CosyVoice 3 voices and rebuilt from manifests (V4: 1,092 timelines / 21.84h; V5: 1,097 timelines / 21.80h), while the locked human corpus holds 107 conversations / 36.30 hours prepared as FLAC + Parquet windows, feeding a Qwen3-1.7B rank-16 LoRA tool-use adapter and a ~183k-parameter causal adapter on a frozen Nemotron 0.6B encoder.

## Key points

- Each user unit was rendered and trimmed independently with Qwen VoiceDesign references conditioning CosyVoice 3 zero-shot voices, then measured for active speech, assembled into a timeline, and rasterized as 20-second views into 250 frames at 80 ms.
- A planned pause became HOLD supervision only if the rendered unit contained at least 500 ms of silence followed by resumed speech, preventing future assistant state or clean synthetic timing from leaking into the adapter.
- The public synthetic repository stores lossless speech units plus reconstruction metadata (plans, voice provenance, trim measurements, composition seeds, split assignments, checksums) rather than duplicating every composed waveform.
- Retained V4 and V5 manifests contain 1,092 and 1,097 timelines with approximately 21.84 and 21.80 hours of source timeline respectively, which describe retained run manifests, not a claim that synthetic interaction validation substitutes for natural conversation.
- The locked human corpus manifest records 107 accepted conversations totaling 36.30 hours (MagicHub 8 / 2.77h; TurnBench 37 / 7.31h; additional authorized material 62 / 26.22h) across conversation-disjoint train, validation, and test splits, after excluding one silent TurnBench recording.
- The tool-use experiment fine-tuned Qwen/Qwen3-1.7B with a BF16 rank-16 LoRA on 3,919 training records (80-record balanced validation split), producing 14,391 training histories and 17.84 million rendered tokens (6.86 million assistant targets) over 16 deterministic passes, training 17.43 million parameters in 904 optimizer steps in 47 minutes on an RTX 4090.
- The turn-taking model attaches approximately 183,000 trainable parameters to the frozen Nemotron Speech Streaming 0.6B encoder, tapping layers 6, 12, 18, and 24 (each 1,024-dimensional tap normalized and projected to 32 dimensions, fused to 64 dimensions) through residual causal depthwise-separable convolutions and a single-layer 64-dimensional unidirectional GRU, with convolution and recurrent state persisting incrementally and resetting with the ASR stream.

---

## Synthetic timeline rendering and manifests

The accepted rendering route used Qwen VoiceDesign references to condition CosyVoice 3 zero-shot voices. Each user unit was rendered and trimmed independently; the compiler then measured its active speech, assembled the final timeline, and rasterized 20-second views into 250 frames at 80 ms. A planned pause became HOLD supervision only if the rendered unit contained at least 500 ms of silence followed by resumed speech.

The public synthetic repository stores lossless speech units and reconstruction metadata rather than duplicating every composed waveform. Plans, voice provenance, trim measurements, composition seeds, split assignments, and checksums allow conversation audio and training crops to be rebuilt. The retained V4 and V5 manifests contain 1,092 and 1,097 timelines, approximately 21.84 and 21.80 hours of source timeline respectively. Per the chunk:

> "These counts describe retained run manifests, not a claim that synthetic interaction validation substitutes for natural conversation."

## Automatic preparation of human conversations

The human pipeline separates three artifact layers: authorized source audio, recording-level evidence, and materialized training windows. Each complete speaker track is stored once as lossless FLAC. Typed Parquet rows reference bounded 20-second intervals and contain aligned inputs, targets, and masks; they do not duplicate the recording.

Ingestion registers and hashes both channels, reuses exact cached transcripts, transports only missing material, applies a reviewed inter-speaker offset, and persists a full-duration annotation and quality result transactionally. Multiple ASR and activity systems provide independent evidence for consensus alignment, channel-aware crosstalk filtering, conversation regions, and quality flags. Per the chunk:

> "Supplied TurnBench annotations remain an independent evidence source rather than being copied into model-output fields to manufacture agreement."

The completed preparation pass accepted eight MagicHub conversations (about 2.77 hours) and 37 Mundo TurnBench conversations (about 7.31 hours); a silent TurnBench recording was excluded. These additions joined previously prepared authorized conversational material. The locked corpus manifest records 107 accepted conversations totaling 36.3 hours across conversation-disjoint train, validation, and test splits. A manual pipeline-validation audit reviewed 12 dataset-stratified recordings and applied targeted exclusions.

Table 1: Human conversational material in the locked corpus manifest. Source audio remains subject to its original access terms; only derived manifests and code are distributed by the project.

| Material | Conversations | Hours |
|---|---|---|
| MagicHub | 8 | 2.77 |
| TurnBench | 37 | 7.31 |
| Additional authorized material | 62 | 26.22 |
| Total | 107 | 36.30 |

## A language adapter for spoken tools

The tool-use experiment fine-tuned Qwen/Qwen3-1.7B with a BF16 rank-16 LoRA. Two source records from each combination of eight behavior families and five speech styles formed a balanced 80-record validation split; the remaining 3,919 records were training data. Across 16 deterministic passes, every record appeared once per pass. Intact short segments were regrouped into histories with 8–16 user turns, producing 14,391 training histories and 17.84 million rendered tokens, of which 6.86 million were assistant targets.

The native Qwen chat template rendered the canonical records with thinking disabled. The loss mask retained ordinary assistant speech, the spoken bridge preceding a call, structured call tokens, post-result continuation, and later assistant turns. System text, tool definitions, user messages, tool results, padding, and non-assistant protocol tokens were masked. The adapter targeted all attention and MLP projections, trained 17.43 million parameters, and completed 904 optimizer steps in 47 minutes on an RTX 4090.

The public deployment uses Qwen3-4B Instruct; the trained 1.7B LoRA remains a released experimental artifact. Section 6 of the source reports why the synthetic protocol result was not treated as evidence of general conversational quality.

## A causal adapter on shared Nemotron features

The turn-taking model attaches approximately 183,000 trainable parameters to the frozen Nemotron Speech Streaming 0.6B encoder. Nemotron is a cache-aware streaming FastConformer-RNNT whose activation caches allow new non-overlapping chunks to reuse prior work. Per the chunk, this property:

> "made it possible to share one streaming backbone between ASR and turn inference rather than re-encoding a rolling waveform or loading a second 0.6-billion-parameter model."

The adapter taps encoder layers 6, 12, 18, and 24. Each 1,024-dimensional tap is normalized and projected to 32 dimensions; the streams are fused to 64 dimensions, processed by residual causal depthwise-separable convolutions, combined with assistant-speaking state, and passed through a single-layer 64-dimensional unidirectional GRU. Separate heads emit completion/yield evidence, interaction events including floor take and non-floor feedback, and future activity. Convolution and recurrent state persist incrementally and reset with the ASR stream. The chunk ends mid-sentence at "Synthetic pretraining selected step 2,250. Human fine-" with the remainder not present in this chunk.

**Covers:** synthetic rendering / HOLD rule / V4–V5 manifests; §4.3 human-conversation preparation and Table 1 locked corpus; §5.1 spoken-tool LoRA; §5.2 causal Nemotron adapter (chunk truncates at "Synthetic pretraining selected step 2,250. Human fine-").
