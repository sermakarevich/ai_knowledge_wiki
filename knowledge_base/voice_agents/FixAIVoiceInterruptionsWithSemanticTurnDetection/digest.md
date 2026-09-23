> [[index|Wiki]] | [[summary|Summary]]

# Fix AI Voice Interruptions with Semantic Turn Detection — Digest

## 1. [[wiki/01-semantic-turn-detection|Semantic Turn Detection]]

**In one sentence:** Voice-activity-detection-only agents interrupt at every pause, so adding a semantic turn detector that waits for a complete thought dramatically improves conversational quality with only ~20 ms of latency.

## Key points

- VAD-only agents hear a pause and assume the speaker is done, so they answer at every mid-sentence pause even when the human is still thinking, breathing, or changing direction.
- Turn detection decides when the agent should speak versus stay quiet, and its most important job is reducing unwanted interruptions.
- VAD spots human-patterned audio while semantic detection examines sentence meaning and asks, "Does this feel like a complete thought?"
- Complete utterances instead of fragments also improve accuracy for the ST engine, with minimal latency impact of only around 20 milliseconds.
- Setup is a single change: add the turn-detector extra (`UV add lifekit agents turn detector`), import the multilingual model from the turn-detector plugin, and pass it into the agent session, which then emits turn events when the model decides the speaker is finished.
- Tested via `uv run agent.py` in console mode, the agent feels more patient and natural, handling hesitations, interruptions, and topic switches (e.g., octopus and dolphin questions).
- Best practices: combine turn detection with VAD and noise control; rely on the multilingual semantic model to normalize different pause patterns across languages; coordinate with preemptive generation so the LLM starts planning while waiting for a clear end of turn.

## The argument in five moves

1. VAD-only agents mistake every pause for the end of a turn, so they interrupt constantly while humans pause mid-sentence to think, breathe, or change direction.
2. The fix is a turn detector whose core job is deciding when to speak versus stay quiet, with semantic detection judging whether an utterance feels like a complete thought rather than just detecting audio.
3. Waiting for complete thoughts costs only ~20 ms yet reduces interruptions and gives the speech-to-text engine full utterances instead of fragments.
4. Implementation is a single session-level change — add the turn-detector extra, import the multilingual model, pass it into the agent session — verified in console mode where the agent patiently handles hesitations, interruptions, and topic switches.
5. For production quality, layer turn detection with VAD and noise control, use the multilingual model to normalize cross-language pause patterns, and pair it with preemptive generation so the LLM plans while awaiting a clear end of turn.
