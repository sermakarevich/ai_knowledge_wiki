> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# We evaluate the VoiceChat-TTS speech decoder

**In one sentence:** VoiceChat-TTS, evaluated standalone, delivers competitive first-turn quality (2.00% WER, 4.380 SQuIM-MOS unseen) with stable multi-turn intelligibility but zero-shot speaker drift, while supporting the persistent silence-and-interruption behavior the full-duplex system requires.

## Key points

- Standalone protocol isolates the decoder from the upstream full-duplex model, testing unseen speakers on LibriTTS test-clean and seen speakers from training, with WER (intelligibility), SECS (speaker similarity), and SQuIM-MOS (predicted overall quality) as metrics.
- First unseen-speaker turn reaches 2.00% WER and 4.380 SQuIM-MOS, beating its streaming-decoder base Audio Flamingo 3-Chat (4.51% WER, 3.600 SQuIM-MOS) with similar first-turn SECS (0.761 vs 0.757).
- Over four consecutive unseen-speaker turns, intelligibility and quality stay stable (WER 2.00% to 2.20%, SQuIM-MOS 4.380 to 4.376) while speaker similarity drifts (SECS 0.757 to 0.685).
- Seen speakers show comparatively stable identity (SECS 0.785 to 0.778 first-to-fourth turn), so the drift is attributed to zero-shot speaker conditioning rather than general persistent-decoding degradation.
- Chatterbox-TTS and Qwen3-TTS-12Hz-1.7B-Base score stronger conventional isolated-response WER, but those results do not test the interaction functionality VoiceChat needs.
- VoiceChat-TTS stays active over the conversation timeline, generates silence under upstream PAD control, and responds to explicit interruption signals without resetting cached state; end-to-end turn-taking is evaluated separately in Table 1.
- The same chunk also reports streaming ASR (80 ms vs 160 ms chunks, average WER 9.02% to 8.28%) and inference efficiency (118 ms per-stream p95 per 160-ms chunk, 1.36x real-time with four concurrent streams on one H100).

---

## Standalone evaluation setup

VoiceChat-TTS is evaluated independently of the upstream full-duplex model "to measure acoustic generation quality and stability under persistent multi-turn decoding," following "the standalone VoiceChat-TTS evaluation protocol [20]." Unseen-speaker condition: LibriTTS test-clean. Seen-speaker condition: speakers observed during training. Metrics: "Intelligibility is measured using word error rate (WER), speaker preservation using speaker encoder cosine similarity (SECS), and predicted overall speech quality using SQuIM-MOS [37]."

**Covers:** VoiceChat-TTS standalone evaluation setup (Table 6 context)

## First-turn quality vs streaming-decoder base

"Table 6 shows that VoiceChat-TTS retains competitive objective speech-generation metrics while supporting the persistent decoding behavior required by NemotronLabs VoiceChat."

| Condition | System | WER | SQuIM-MOS | SECS (first turn) |
|---|---|---|---|---|
| Unseen, first turn | VoiceChat-TTS | 2.00% | 4.380 | 0.761 (reported) / 0.757 (turn-1 in drift series) |
| Unseen, first turn | Audio Flamingo 3-Chat (base streaming decoder) | 4.51% | 3.600 | 0.757 |

"Relative to Audio Flamingo 3-Chat, the streaming decoder on which it is based, VoiceChat-TTS reduces WER from 4.51% to 2.00% and increases SQuIM-MOS from 3.600 to 4.380, with similar first-turn SECS (0.761 versus 0.757)."

**Covers:** first-turn unseen-speaker results vs Audio Flamingo 3-Chat

## Multi-turn stability and speaker drift

"Across four consecutive turns, intelligibility and predicted overall quality remain stable for unseen speakers: WER changes from 2.00% to 2.20% and SQuIM-MOS from 4.380 to 4.376. Speaker similarity, however, decreases from 0.757 to 0.685, indicating identity drift for zero-shot voices over longer continuous contexts."

"For speakers observed during training, SECS remains comparatively stable, changing only from 0.785 to 0.778 between the first and fourth turns. This suggests that the observed long-context speaker drift is primarily associated with zero-shot speaker conditioning rather than a general degradation of persistent decoding."

**Covers:** four-turn stability, unseen vs seen speaker drift

## Interaction functionality vs isolated-TTS baselines

"Chatterbox-TTS and Qwen3-TTS-12Hz-1.7B-Base achieve stronger conventional isolated-response WER, but these results do not evaluate the interaction-specific functionality required by NemotronLabs VoiceChat."

"VoiceChat-TTS remains active over the conversation timeline, generates silence under upstream PAD control, and responds to explicit interruption signals without resetting its cached state [20]. End-to-end turn-taking and interruption behavior are evaluated separately in Table 1."

**Covers:** isolated-response baselines vs persistent/interruption behavior

## User transcription (ASR) benchmark

Table 7 reports WER (%) on Hugging Face OpenASR Leaderboard datasets [38], "computed using the scoring scripts from the leaderboard," for chunk sizes 80 ms and 160 ms:

| Dataset | 80 ms | 160 ms |
|---|---|---|
| AMI | 15.32 | 13.54 |
| Earnings22 | 14.82 | 14.04 |
| Gigaspeech | 12.25 | 11.65 |
| LS Clean | 3.58 | 3.19 |
| LS Other | 8.15 | 7.19 |
| SPGISpeech | 3.91 | 3.56 |
| Tedlium | 5.25 | 4.89 |
| VoxPopuli | 8.85 | 8.17 |
| Average | 9.02 | 8.28 |

"A smaller chunk-size reduces the amount of audio that must be observed before the model produces the user transcription, thereby enabling lower-latency streaming ASR. In contrast, a larger chunk-size provides additional local acoustics and linguistics context which improves the accuracy of decoded words." The 80-to-160 ms increase "consistently improved the ASR performance across all the evaluation sets reducing the average WER from 9.02% to 8.28%."

"Importantly, nemotron-speech-streaming-0.6b [19] uses a cache-aware streaming architecture that seamlessly supports multiple chunk-size specified in the model training configuration. Consequently, the same trained model can be deployed under different latency requirements without the need to retrain separate models for different latency."

**Covers:** Appendix C.3, Table 7 ASR benchmark

## Inference efficiency

"All inference measurements for the baseline system were conducted on a single NVIDIA H100 PCIe GPU with 80 GB of memory. The perception encoder and LLM backbone run in BF16, whereas the TTS backbone and cached Mamba recurrent states remain in FP32. On supported GPUs, TF32 execution is enabled for eligible FP32 matrix multiplications. Lower-precision and quantized variants were not evaluated."

"With four concurrent streams, the per-stream p95 inference latency is 118 ms per 160-ms audio chunk. This corresponds to 1.36x real-time processing throughput."

**Covers:** Appendix C.4 inference efficiency

## Tool specification

Tool definition with filler message (verbatim example):

```json
{
  "name": "calculate_bmi",
  "description": "Calculate the Body Mass Index (BMI)",
  "parameters": {
    "type": "object",
    "properties": {
      "weight": {"type": "number", "description": "The weight in kilograms"},
      "height": {"type": "number", "description": "The height in meters"}
    },
    "required": ["weight", "height"]
  },
  "ack_message": "Sure, let me calculate that for you"
}
```

Spoken-tool-call flow in the chunk: user asks "What's the weather in Tokyo?" → model emits `[{"name": "get_weather", "arguments": {"city": "Tokyo"}}]` → agent speaks ack_message ("Let me check the weather for you.") → tool returns `{"temperature": "22° C", "condition": "Sunny"}` → agent speaks "It's 22 degrees and sunny in Tokyo right now."

The Jinja template (Listing 1) renders only the system prompt with tool definitions injected (audio user turns are not rendered): it serializes tool schemas inside `<AVAILABLE_TOOLS>[...]</AVAILABLE_TOOLS>`, declares the call format `<TOOLCALL>[{"name": "tool_name1", "arguments": "tool_args1"}, ...]</TOOLCALL>`, the response format `<TOOL_RESPONSE>[...]</TOOL_RESPONSE>`, and the instruction "Based on the tool responses, you can call additional tools if needed, correct tool calls if any errors are found, or just respond to the user." Adapted from the Nano v2 chat template (`nano_v2_chat_template.jinja`, NVIDIA-Nemotron-Nano-9B-v2).

**Covers:** Appendix D.1–D.2 tool filler-message spec and Jinja template
