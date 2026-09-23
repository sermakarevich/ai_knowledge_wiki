> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Architecture and Foundation Training

**In one sentence:** Conversational context — acoustic and linguistic evidence, dialogue history, current turn, reasoning progress, and tool-execution status — drives listen/speak, reason-further, and act decisions in a full-duplex mixture-of-experts system built by three-stage pretraining (32K length, 1.2T tokens) plus 128K-context midtraining for realtime interaction and perception.

## Key points
- Conversational context combines acoustic and linguistic evidence, dialogue history, current speaking turn, reasoning progress, and tool-execution status, retaining what the user says and how it is said.
- Model-side speech is itself context: it helps interpret user utterances that overlap with a response, and newly observed speech or returned tool results can change listen/speak/reason/act decisions.
- Seamless Duplex handles pauses, backchannels, and substantive interruptions; Think-While-Speaking starts spoken delivery before the full reasoning trace is complete; Adaptive Thinking selects when explicit reasoning is useful and MTP accelerates private reasoning.
- The Voice Agent resolves the request and required arguments before execution, incorporates returned evidence into the conversation, and lets the user keep speaking while a task is in progress so external work proceeds alongside dialogue.
- System is mixture-of-experts: audio frontend uses the Audio Transformer (AuT) encoder from Qwen3-Omni with an adapter mapping encoder outputs into the LLM's representation space; LLM decoder jointly conditions on acoustic info plus separate text input; generator output returns to the model audio stream.
- Pretraining runs three stages — modality alignment (acoustic-to-LM interface), multimodal mixed training (joint audio-text modeling at scale), cooldown (greater weight on high-quality data) — at fixed 32K sequence length over 1.2T tokens, with increased pure-text share to preserve base-LM capabilities.
- Midtraining extends context to 128K for longer histories, earlier requirements, and intermediate tool results, and increases audio-understanding (speech, music, environmental sound, audio-grounded reasoning) and agent-interaction data share.
- ASR specialization diverges only at supervised fine-tuning: ASR Max packs examples into 32K-token sequences, freezes the audio encoder, updates adapter plus language decoder with SpecAugment-style time-frequency masking, and fuses multi-system hypotheses with ROVER plus LLM punctuation/consistency restoration.

---

## Conversational context and realtime loop

> "The conversational context includes acoustic and linguistic evidence, dialogue history, the current speaking turn, reasoning progress, and tool-execution status."

- "Perception retains cues about what the user says and how it is said."
- "Model-side speech provides additional context for interpreting user utterances that overlap with a response."
- "This context informs whether to continue listening or speaking, whether to reason further, and whether a request is ready for external action."
- "Newly observed speech and returned tool results can change these decisions as the conversation proceeds."
- Figure 2 labels the loop: DEEP PERCEPTION (ASR · AUDIO UNDERSTANDING), SEAMLESS DUPLEX (LISTEN · SPEAK · YIELD), STEP-AUDIO 3 Realtime CONVERSATIONAL STATE, STREAMING SPEECH, THINK WHILE SPEAKING (ADAPTIVE THINKING, MEDUSA MTP), STREAMING ACTION (INTENT · TOOL CALL · FEEDBACK); user stream carries LEXICAL · EMOTION · ACOUSTIC CONTEXT and model stream carries SPEECH · OVERLAP · TURN STATE.
- Figure 2 caption: "User and model speech inform perception and floor management. Reasoning supports spoken responses and tool use, while returned tool results update the context for subsequent interaction."

## Coordinating speech, reasoning, and action (§2.2)

- "Conversational timing and reasoning progress need not advance at the same pace."
- Seamless Duplex handles pauses, user backchannels, and substantive interruptions; Think-While-Speaking allows spoken delivery before the full reasoning trace is complete; Adaptive Thinking selects when explicit reasoning is useful; MTP accelerates private reasoning (Sections 5 and 6.3).
- Voice Agent: "resolves the request and required arguments before execution, then incorporates returned evidence into the conversation"; "The user can continue speaking while a task is in progress"; coordination described in Section 7.

## System architecture (§3.1)

- Mixture-of-experts architecture; audio frontend uses Audio Transformer (AuT) encoder from Qwen3-Omni [8]; adapter maps encoder outputs into the language model's representation space.
- Full-duplex input path incorporates user and model audio streams; audio representations pass through encoder and adapter to the LLM decoder; text tokens enter through a separate input path so the decoder jointly conditions on acoustic information and textual context.
- Generator produces streaming model audio, which "returns to the model audio stream for subsequent interaction"; Section 5 covers floor management.
- "The speech generator produces incremental output with context-appropriate tone and rhythm"; natural delivery "includes expressive cues such as pauses and hesitation, connecting the content of a response with its communicative intent."
- Figure 3 caption: "The LLM decoder receives audio representations through the audio encoder and adapter, together with a separate text input. User and model audio form the two full-duplex streams, with generator output returning to the model audio stream. Waveforms are schematic."

## Three-stage pretraining (§3.2)

- Data curation via automated large-scale audio pipeline [16]: raw audio filtered with sound event detection and voice activity detection, merged and resegmented into semantically complete samples of suitable duration; metadata for quality, synthetic-speech likelihood, speaker count; multiple recognition systems for transcription and language ID with cross-checks and acoustic/semantic quality grading; quality-aware sampling; for StepAudio 3 Realtime extended for broader language coverage and sustained realtime dialogue demands.
- Stages: modality alignment establishes acoustic-to-LM interface; multimodal mixed training develops joint audio-text modeling at scale; cooldown places greater weight on high-quality data.
- Scale: fixed 32K sequence length across three stages, 1.2T training tokens.
- Mixture: increased proportion of pure text "to preserve the general capabilities of the base language model and support subsequent reasoning and agent training."

## Midtraining for realtime interaction (§3.3)

- Uses perception, synthetic conversational, and voice-agent data; context extended to 128K "to accommodate longer dialogue histories, earlier user requirements, and intermediate tool results."
- Mixture substantially increases audio-understanding and agent-interaction data: former covers speech, music, environmental sound, audio-grounded reasoning; latter trains carrying user intent through planning, tool use, and spoken follow-up (Sections 4.2 and 7).

## Deep perception and ASR Max training (§4–4.1.1)

- "Perception combines lexical understanding with cues about the speaker, vocal delivery, acoustic events, and temporal structure"; StepAudio 3 ASR Max specializes in transcription while StepAudio 3 Realtime targets broader audio understanding and spoken interaction; Section 8 compares benchmarks.
- ASR Max and Realtime share pretraining and midtraining; diverge only at supervised fine-tuning (ASR branch for transcription, realtime branch for spoken interaction).
- SFT: examples packed into sequences up to 32K tokens; time-frequency masking per SpecAugment [18]; audio encoder frozen; audio-language adapter and language decoder updated to produce normalized transcripts; optional context evidence (dialogue history, preceding model response, scenario description, task terminology) with target grounded in waveform so model uses relevant context "without simply copying unrelated terms."
- Short- and long-form data: short labeled utterances plus long pseudo-labeled recordings; multiple systems transcribe segmented audio; hypotheses aligned and fused with Recognizer Output Voting Error Reduction (ROVER) [19]; agreement-based filtering selects reliable segments recomposed into longer sessions; LLM restores punctuation and cross-session consistency.
- Long-tail terminology: rare names/technical terms confused with similar-sounding common words; LLM expands knowledge taxonomy to find homophone/uncommon-character/abbreviation/product-identifier-rich categories; candidate terms deduplicated, placed in natural carrier sentences, converted to speech, retained only when pronunciation matches target text; acoustically confusable cases may include dialogue history or entity hints to teach relevant-context use "while avoiding unrelated lexical substitutions."

## Table 1: ASR evaluation (excerpt from chunk)

Table 1 reports lower-is-better error rates; English subsets WER, Mandarin CER; bold = best per row, underline = second-best; ContextASR-Bench uses Contextless setting.

| Test set | StepAudio 3 ASR Max | Doubao 2.0 ASR | Seed 2.0 Lite | HY3.0 ASR Preview |
|---|---|---|---|---|
| LibriSpeech test-clean | 1.18 | 2.94 | 1.47 | 1.38 |
| LibriSpeech test-other | 2.28 | 5.98 | 2.67 | 2.80 |
| AISHELL-1 | 0.49 | 2.07 | 1.66 | 1.22 |
| WenetSpeech test-net | 3.99 | 4.03 | 4.71 | 3.71 |
| WenetSpeech test-meeting | 4.35 | 5.09 | 4.80 | 4.12 |
| ContextASR-Speech-EN | 7.91 | 12.04 | 9.48 | 8.53 |
| ContextASR-Dialogue-EN | 3.43 | 9.09 | 3.65 | 4.66 |
| ContextASR-Speech-ZH | 1.43 | 2.80 | 2.15 | 1.74 |
| ContextASR-Dialogue-ZH | 1.02 | 10.47 | 4.15 | 1.63 |

**Covers:** Conversational-context definition through §4.1.1 (Table 1 header and rows; §4.1.2 evaluation text not in chunk).
