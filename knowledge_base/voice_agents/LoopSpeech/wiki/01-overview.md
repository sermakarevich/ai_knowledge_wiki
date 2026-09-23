[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** LoopSpeech introduces Self-Listening, a playback-grounded approach that lets a full-duplex speech model track its own realized speech and recover consistently after interruptions.
## Key points
- The repo is the official repository for "What Did I Just Say? Self-Listening for Full-Duplex Speech Models" and is currently Preprint status with code, models, data, and paper link still to be added (README.md:9, README.md:11).
- Full-duplex models can listen and speak simultaneously, but async text generation, synthesis, and playback create an anchoring gap between what the model believes it said and what was actually played (README.md:21, README.md:23).
- The gap matters for interruption queries such as "What did you just say?", "Repeat the last item.", "Where did you stop?", and "Continue from there." (README.md:23-28).
- Self-Listening organizes interaction as three time-aligned streams — user speech, played model speech (only waveform already reaching user-side playback), and model text with control tokens — interleaved on a shared 40 ms timeline (README.md:40-46).
- Played model speech is fed back through the model's speech-input pathway, giving a causal record of what the user actually heard without delaying generation or playback (README.md:46).
- The system builds on the Thinker branch of Qwen2.5-Omni-7B with a frozen MOSS-TTS-Realtime streaming synthesizer, plus native control tokens for overlap, interruption stopping, backchannel continuation, waiting, and silence (README.md:48).
- AnchorSpeech-test measures whether post-interruption responses stay consistent with the last completed played item rather than internally generated-only text (README.md:54).
- The three-channel Self-Listening model reaches 73.0% anchoring accuracy on AnchorSpeech-test versus 7.8% (matched two-channel) and 43.8% (GPT-Realtime-2.1), with nearly unchanged stop/response latencies in the controlled comparison (README.md:60-71).
---
## Anchoring gap
Full-duplex speech models "can listen and speak at the same time, enabling interruptions and backchannels" (README.md:21). However, "text generation, speech synthesis, and audio playback run asynchronously: a model may have generated content that the user has not actually heard" (README.md:21). This creates "an **anchoring gap** between what the model believes it has said and what was really played to the user" (README.md:23). The motivating interruption requests are verbatim (README.md:25-28):
- "What did you just say?"
- "Repeat the last item."
- "Where did you stop?"
- "Continue from there."
The stated fix: "LoopSpeech introduces **Self-Listening**, a playback-grounded approach that lets a full-duplex model track its own realized speech and recover consistently after interruptions" (README.md:30). The figure caption states: "Self-Listening feeds the model speech already played to the user back into the listening pathway, mirroring human speech self-monitoring" (README.md:17).
## Method — three-channel Self-Listening
Self-Listening "organizes an interaction as three time-aligned streams" (README.md:40):
1. "**User speech** - the incoming audio from the user" (README.md:42).
2. "**Played model speech** - only the model waveform that has already reached user-side playback" (README.md:43).
3. "**Model text** - response tokens and full-duplex control tokens" (README.md:44).
"The streams are interleaved on a shared 40 ms timeline" (README.md:46). "Played model speech is fed back through the model's speech-input pathway, giving the model a causal record of what the user has actually heard without delaying generation or playback" (README.md:46). Figure caption: "The three-channel architecture interleaves user speech, played model speech, and model text on a shared timeline while handling overlap and interruption control" (README.md:38). Base stack: "built on the Thinker branch of **Qwen2.5-Omni-7B**" with "a frozen **MOSS-TTS-Realtime** model for streaming synthesis" (README.md:48). "Native control tokens support overlap handling, interruption stopping, backchannel continuation, waiting, and silence" (README.md:48).
## AnchorSpeech
"The paper also introduces **AnchorSpeech**, a time-aligned collection for training and evaluating anchoring-sensitive interruptions" (README.md:52). "AnchorSpeech-test measures whether a model's response after an interruption is consistent with the last completed item that was actually played, rather than with text that may only have been generated internally" (README.md:54).
## Main results
"On AnchorSpeech-test:" (README.md:58):
| Model | Anchoring accuracy | Stop latency | Response latency |
|---|---|---:|---:|
| GPT-Realtime-2.1 | 43.8% | 0.296 s | 1.548 s |
| Two-channel full-duplex model | 7.8% | 0.425 s | 0.567 s |
| **Three-channel Self-Listening model** | **73.0%** | **0.434 s** | **0.564 s** |
(Table values README.md:60-64.) Gains stated verbatim (README.md:66-69):
- "**65.2 percentage points** over the matched two-channel model."
- "**29.2 percentage points** over GPT-Realtime-2.1, the strongest evaluated commercial baseline."
Interpretation given in source: "The nearly unchanged stopping and response latencies in the controlled two-channel/three-channel comparison indicate that the improvement comes from playback-grounded context rather than a slower interruption strategy" (README.md:71). Additionally, "Experiments on Full-Duplex-Bench v1.5 further show sub-second response latency in interruption and backchannel scenarios, while revealing a trade-off between anchoring and conventional turn-management performance" (README.md:73).
## Status, roadmap, and contact
Status: "> **Status:** Preprint. Code, models, data, and the public paper link will be added as they become available" (README.md:11). Authors: "Xuanning Zhou*, Junyi Ao*, Xiaotong Liu, Tom Ko†, Benyou Wang, and Haizhou Li" with "Shenzhen Loop Area Institute, China" and "The Chinese University of Hong Kong, Shenzhen, China", "* Equal contribution", "† Corresponding author" (README.md:77-83). Citation key `zhou2026loopspeech`, title "What Did I Just Say? Self-Listening for Full-Duplex Speech Models", year 2026, note Preprint (README.md:89-96). Roadmap checklist verbatim (README.md:102-106): Paper link; Inference and training code; Model checkpoints; AnchorSpeech data and evaluation scripts; Reproducible examples and demos — all unchecked. Contact: "Please open an issue in this repository for questions and updates" (README.md:110). No truncated files were noted in the chunk; the chunk's macro-components section reports "(no component directories)" (README.md:112-114).
**Covers:** README.md (repo overview, anchoring gap, three-channel method, AnchorSpeech, results, authors/citation, roadmap, contact); assets/self-listening-overview.png and assets/self-listening-architecture.png (figure references only)
