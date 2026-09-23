> [[index|Wiki]] | [[summary|Summary]]
# FreedomIntelligence/LoopSpeech — Digest
## 1. [[wiki/01-overview|Overview]]
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
## The system in five moves
1. Full-duplex speech models can listen and speak at the same time, but async text generation, synthesis, and playback open an anchoring gap between believed output and actually played speech.
2. The gap bites when users interrupt with "What did you just say?", "Repeat the last item.", "Where did you stop?", or "Continue from there."
3. Self-Listening closes it by organizing interaction as three time-aligned streams — user speech, already-played model speech, and model text with control tokens — interleaved on a shared 40 ms timeline.
4. Played model speech is fed back through the speech-input pathway as a causal record of what the user heard, built on the Qwen2.5-Omni-7B Thinker branch with frozen MOSS-TTS-Realtime synthesis and native control tokens.
5. AnchorSpeech-test judges post-interruption responses against the last completed played item rather than generated-only text.
6. The three-channel model reaches 73.0% anchoring accuracy versus 7.8% matched two-channel and 43.8% GPT-Realtime-2.1 with nearly unchanged latencies, so the gain comes from playback grounding — while the repo remains Preprint with code, models, data, and paper link still to come.
