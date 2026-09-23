> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Audio Assembly, Background/Event Mixing, and Quality Validation
**In one sentence:** DuplexDrama assembles dual-track long-form speech with full-duplex overlap, mixes script-placed sound events at forced-alignment onsets with configurable SNR, and filters everything through a dual-LLM script check plus four objective audio metrics with a SpkCons < 0.9 discard rule.
## Key points
- The pipeline produces persona- plus behavior/emotion/event-tagged scripts, dual-track long-form speech waveforms with full-duplex behaviors surfaced as acoustic overlap, and script-aware event mixing, followed by a quality validator.
- Sound-event realization matches assets from the audio bank against the event-class tag emitted by Stage 2 (§2.2), aligns the asset to the trigger word's onset by forced alignment of the synthesized speech, and mixes it in at the configured SNR.
- The worked example in the chunk is Turn 4 (HM, A) ". . . the pen slipped out and hit the floor." with event class `object hit`, FA onset 2.34 s, and mixed audio speech + event; listed bank assets include doorbell, page turn, footstep, object hit, and cup glass.
- Script quality uses a dual-LLM framework (DeepSeek-v4.1-pro and Gemini-3.1-pro-preview) on three dimensions — asset rationality of the manually curated audio bank, tag rationality in scripts, and script-scenario consistency — with only asset rationality judged by the single Gemini-3.1-pro-preview multimodal model and the latter two cross-checked by both LLMs.
- Synthesized audio is evaluated on four objective metrics: WER via Qwen3-ASR, audio quality via UTMOSv2 and NISQA (MOS), and SpkCons via SpeechBrain cosine similarity, discarding dialogues with SpkCons below 0.9 following [4].
- WER and SpkCons are performed on clean TTS audio without background, since those two metrics evaluate speech itself.
- The chunk's OCR of the dataset overview reports 6,400 dialogues, 800 total audio hours, 460 s average dialogue length, ~362k turns, 8 s average turn length, and 64 voice timbres; behavior-tag counts visible are `<user interrupt>` 8,996 (2.4%), `<user backchannel>` 2,455 (0.6%), and `<user incomplete>` 2,271 (0.7%).
- Part of this chunk is garbled OCR (an environment-distribution figure with percentages 32.55%, 23.68%, 19.52%, 11.40%, 5.60%, 3.69%, 3.56% whose labels are unreadable, and a truncated §3.1 lead sentence), so those figures are reported here without interpreted labels.
---
## Pipeline figure (Fig. 2)
**Covers:** Fig. 2 pipeline caption as present in chunk

| Item | Value (verbatim/from chunk) |
|---|---|
| Input stages | Persona & Scenario; Behavior, Emotion & Event; TTS & Audio Assemble; background channel |
| Output stages | Quality Validator; Dialogue |
| Mechanism | Persona, behavior/emotion/event-tagged scripts, dual-track long-form speech waveforms with full-duplex behaviors surfaced as acoustic overlap, and script-aware event mixing, followed by a quality validator |

Verbatim:

> "Fig. 2. DuplexDrama pipeline generating persona, behavior/emotion/event-tagged scripts, dual-track long-form speech waveforms with full-duplex behaviors surfaced as acoustic overlap, and script-aware event mixing, followed by a quality validator."

## Sound-event realization (Fig. 3)
**Covers:** Fig. 3 + §2.2 trigger-tag reference

| Item | Value (verbatim/from chunk) |
|---|---|
| Match source | Assets from the audio bank matched against the event class tag emitted by Stage 2 (§2.2) |
| Alignment | Aligned to the trigger word's onset by forced alignment of the synthesized speech |
| Mixing | Mixed in at the configured SNR |
| Example turn | Turn 4 (HM, A): ". . . the pen slipped out and hit the floor." |
| Example tag | event class: object hit; FA onset: 2.34 s; mixed audio: speech + event |
| Listed assets | doorbell, page turn, footstep, object hit, cup glass |

Verbatim:

> "Fig. 3. Sound-event realization: assets from the audio bank are matched against the event class tag emitted by Stage 2 (§2.2), aligned to the trigger word's onset by forced alignment of the synthesized speech, and mixed in at the configured SNR."

## Quality validation (§2.5)
**Covers:** §2.5 dual-LLM script check + four objective audio metrics

| Item | Value (verbatim/from chunk) |
|---|---|
| Script judges | Dual-LLM: DeepSeek-v4.1-pro [12] and Gemini-3.1-pro-preview [13] |
| Script dimension 1 | Asset rationality of the manually curated audio bank, judged by the single Gemini-3.1-pro-preview multimodal model |
| Script dimension 2 | Tag rationality in scripts, cross-checked by both LLMs |
| Script dimension 3 | Script-scenario consistency, cross-checked by both LLMs |
| Audio metric 1 | WER (Qwen3-ASR [15]) |
| Audio metric 2 | Audio quality via UTMOSv2 [16] and NISQA [17] (MOS) |
| Audio metric 3 | SpkCons via SpeechBrain [18] cosine similarity |
| Discard rule | Dialogues with SpkCons below 0.9 are discarded following [4] |

Verbatim:

> "We employ a dual-LLM (DeepSeek-v4.1-pro [12] and Gemini-3.1-pro-preview [13]) framework to evaluate scripts on three dimensions: asset rationality of the manually curated audio bank (judged by the single Gemini-3.1-pro-preview multimodal model), tag rationality in scripts, and script-scenario consistency, with the latter two cross-checked by both LLMs."

> "The synthesized audio is then evaluated along four objective metrics: WER (Qwen3-ASR [15]), audio quality via UTMOSv2 [16] and NISQA [17] (MOS), and SpkCons via SpeechBrain [18] cosine similarity. Dialogues with SpkCons below 0.9 are discarded following [4]."

## Dataset analysis framing (§3–§3.2.1, as present in chunk)
**Covers:** §3 intro; Table 1 and Table 2 fragments; §3.2–§3.2.1

In this chunk the dataset-analysis section is only partially legible. What is legible:

- "In this section, we analyse the dataset through intrinsic metrics organized into three sub-sections. Section 3.1 reports dataset statistics; Section 3.2 reports quality validation; Section 3.3 compares with prior corpora."
- "We evaluate each generated dialogue on the four objective audio metrics defined in Section 2.5; script-tag rationality is reported separately in Section 3.2.2."
- "Note that both Word Error Rate (WER) and speaker consistency (SpkCons) are performed on clean TTS audio (without background), since those two metrics evaluate speech itself"

Table 1 fragment (Table 1. Dataset overview of the released corpus):

| Metric | Value (as OCR'd in this chunk) |
|---|---|
| Dialogues | 6,400 |
| Total audio (hours) | 800 |
| Avg. dialogue length (s) | 460 |
| Turns | ∼362k |
| Avg. turn length (s) | 8 |
| Voice timbres | 64 |

Table 2 fragment (Table 2. Full-duplex behavior tag counts and shares across all turns):

| Behavior Tag | Count | Share |
|---|---|---|
| `<user interrupt>` | 8,996 | 2.4% |
| `<user backchannel>` | 2,455 | 0.6% |
| `<user incomplete>` | 2,271 | 0.7% |

Garbled / truncated in this chunk (not interpreted): a percentage distribution figure showing 32.55%, 23.68%, 19.52%, 11.40%, 5.60%, 3.69%, 3.56% with unreadable category labels, and the §3.1 lead sentence breaking off at "We summarize the released corpus through four views: an".

**Covers:** Audio assembly with full-duplex overlap, background/event channel mixing, and quality validator (Fig. 2–Fig. 3, §2.5, plus §3/§3.2–§3.2.1 and Tables 1–2 fragments as OCR'd in chunk 03-scripts-w-long-form-seed-topic-construct)
