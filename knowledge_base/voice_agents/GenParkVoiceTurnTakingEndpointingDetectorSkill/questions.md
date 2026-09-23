---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: alphaparkinc/genpark-voice-turn-taking-endpointing-detector-skill

### Q1. What three functions does the skill perform for real-time conversational voice agents?

> [!tip]- Answer
> It performs acoustic voice activity detection (VAD) to drive turn-taking decisions, dynamic silence endpointing to decide when a user turn is complete, and barge-in interruption arbitration that cuts agent audio when user speech energy exceeds threshold. Endpointing decisions pipe into LLM synthesis dispatch once silence reaches the threshold. See [[wiki/01-overview|Overview]].

### Q2. How does the pipeline decide between barge-in, dispatching synthesis, and continuing to listen?

> [!tip]- Answer
> If the agent is speaking and user speech energy exceeds the threshold, it triggers a barge-in interrupt and cuts agent audio; otherwise it accumulates speech and silence frames. When post-onset silence duration reaches the endpointing threshold the turn is marked complete and dispatched to LLM synthesis, and if silence is below threshold it continues listening. See [[wiki/01-overview|Overview]].

### Q3. What are the three constructor parameters of `VoiceTurnTakingEndpointingDetector` and what role does each play?

> [!tip]- Answer
> The parameters are `min_silence_duration_ms=450`, the post-onset silence required to set `turn_completed`, and `barge_in_energy_threshold_db=-28.0`, the per-frame energy threshold for classifying a frame as speech. The third is `consecutive_speech_frames_threshold=3`, the consecutive speech frames required to set `speech_started` and, when the agent is speaking, `user_interrupted`. See [[wiki/02-top-level-files|top-level-files]].

### Q4. Walk through the per-frame loop in `evaluate_audio_frame_stream`: defaults, classification, and state updates.

> [!tip]- Answer
> Each frame defaults to `energy_db=-60.0` and `duration_ms=20`, and is classified as speech when `energy_db >= barge_in_energy_threshold_db`. Speech frames increment the consecutive-speech counter and reset silence, setting `speech_started` at threshold and `user_interrupted` only if `agent_is_speaking`; non-speech frames after onset accumulate silence milliseconds and set `turn_completed` once the minimum silence duration is reached. See [[wiki/02-top-level-files|top-level-files]].

### Q5. What decision precedence and return payload does `evaluate_audio_frame_stream` produce?

> [!tip]- Answer
> The default decision is `CONTINUE_LISTENING`, overridden to `TRIGGER_BARGE_IN_INTERRUPT` when the user interrupted, else to `DISPATCH_AGENT_SYNTHESIS` when the turn completed. The return payload contains `decision`, `barge_in_detected`, `turn_completed`, `final_silence_ms`, `analyzed_frames_count`, and a per-frame `frame_audit` with energy, speech, silence, interruption, and completion fields. See [[wiki/02-top-level-files|top-level-files]].

### Q6. What do `example_usage.py`, `mcp_server.py`, and the manifest/packaging files each contribute?

> [!tip]- Answer
> `example_usage.py` verifies the detector with a 5-frame speech-then-silence stream (three speech frames then two silence frames, `agent_is_speaking=False`) asserting `turn_completed is True` and `DISPATCH_AGENT_SYNTHESIS`. `mcp_server.py` is a stdio JSON-RPC 2.0 wrapper serving `initialize`, `tools/list` (single `execute_skill_action` tool), and `tools/call`, plus a `--test` self-check mode. `skill.json` declares the v1.0.0 python3 manifest with `client.py` entrypoint while `requirements.txt` pins zero dependencies and `.gitignore` excludes Python, env, log, and macOS artifacts. See [[wiki/02-top-level-files|top-level-files]].

### Q7. Would you recommend this skill as the turn-taking layer for a production voice agent, and what caveat matters most?

> [!tip]- Answer
> Recommend it only as a lightweight heuristic starting layer, not a production-grade endpointing solution, because its energy-threshold VAD with fixed silence and frame-count thresholds cannot distinguish real speech from noise or handle mid-turn pauses and hesitations. Adopt it for zero-dependency prototyping and immediate barge-in handling, but plan to replace or augment it with a neural VAD and adaptive endpointing before production deployment. See [[wiki/01-overview|Overview]].
