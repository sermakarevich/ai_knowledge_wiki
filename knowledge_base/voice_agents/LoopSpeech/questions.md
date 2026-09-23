---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: FreedomIntelligence/LoopSpeech

### Q1. What is LoopSpeech and what is Self-Listening in one sentence?
> [!tip]- Answer
> LoopSpeech is the official repository for "What Did I Just Say? Self-Listening for Full-Duplex Speech Models," currently Preprint status with code, models, data, and the paper link still to be added. Self-Listening is a playback-grounded approach that lets a full-duplex speech model track its own realized speech and recover consistently after interruptions. It mirrors human speech self-monitoring by feeding already-played speech back into the listening pathway. See [[wiki/01-overview|Overview]].

### Q2. What is the anchoring gap and why does asynchronous generation cause it?
> [!tip]- Answer
> The anchoring gap is the mismatch between what the model believes it has said and what was really played to the user. It arises because text generation, speech synthesis, and audio playback run asynchronously, so a model may have generated content the user has not actually heard. After an interruption the model may therefore anchor to generated-only text instead of realized playback. See [[wiki/01-overview|Overview]].

### Q3. Which user queries make the anchoring gap matter?
> [!tip]- Answer
> The motivating queries are "What did you just say?", "Repeat the last item.", "Where did you stop?", and "Continue from there." Each demands that the post-interruption reply stay consistent with the last item the user actually heard. A model anchored to un-played generated text fails exactly these requests. See [[wiki/01-overview|Overview]].

### Q4. How does three-channel Self-Listening organize an interaction?
> [!tip]- Answer
> It organizes interaction as three time-aligned streams: user speech, played model speech covering only the waveform already reaching user-side playback, and model text with full-duplex control tokens. The streams are interleaved on a shared 40 ms timeline, and played model speech is fed back through the speech-input pathway. This gives a causal record of what the user actually heard without delaying generation or playback. See [[wiki/01-overview|Overview]].

### Q5. What is the concrete model and synthesis stack behind Self-Listening?
> [!tip]- Answer
> The system is built on the Thinker branch of Qwen2.5-Omni-7B with a frozen MOSS-TTS-Realtime model for streaming synthesis. Native control tokens support overlap handling, interruption stopping, backchannel continuation, waiting, and silence. Playback feedback reuses the existing speech-input pathway rather than adding a separate delayed channel. See [[wiki/01-overview|Overview]].

### Q6. What is AnchorSpeech-test and what are the main results on it?
> [!tip]- Answer
> AnchorSpeech is a time-aligned collection for training and evaluating anchoring-sensitive interruptions, and AnchorSpeech-test measures whether a post-interruption response stays consistent with the last completed played item rather than generated-only text. The three-channel model reaches 73.0% anchoring accuracy versus 7.8% for the matched two-channel model and 43.8% for GPT-Realtime-2.1, gains of 65.2 and 29.2 percentage points. Stop and response latencies are nearly unchanged in the controlled comparison (0.434 s vs 0.425 s; 0.564 s vs 0.567 s), indicating the gain comes from playback-grounded context rather than a slower interruption strategy. See [[wiki/01-overview|Overview]].

### Q7. A team wants interruption-robust voice replies today, but the repo is Preprint with no code, checkpoints, data, or paper link yet — what would you recommend and why?
> [!tip]- Answer
> I would recommend treating LoopSpeech as a design reference rather than a deployable dependency, prototyping playback-grounded context by logging actually-played audio and anchoring replies to the last completed played item. The reported 73.0% anchoring accuracy is promising but rests on unreleased code, models, and AnchorSpeech data, so it cannot yet be reproduced. Until the paper link, inference and training code, checkpoints, and evaluation scripts land, opening a repo issue for updates and benchmarking against a baseline like GPT-Realtime-2.1 is the safer path. See [[wiki/01-overview|Overview]].
