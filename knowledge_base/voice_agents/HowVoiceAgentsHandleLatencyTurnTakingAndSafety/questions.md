---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: How Voice Agents Handle Latency, Turn-Taking, and Safety | Interview With Kræn Hansen

### Q1. What are the three stages of the voice-agent pipeline described in the interview?
> [!tip]- Answer
> Speech is converted to text with speech-to-text, a text-based LLM reasons over it and generates output text, and that text is converted back to speech with text-to-speech. The LLM alone accounts for roughly 40–70% of pipeline latency, making it the central pain point. See [[wiki/01-voice-agents-latency-turn-taking-safety|What a voice agent is]].

### Q2. What does expressive text-to-speech let the model do, and what must the agent say when asked if it is human?
> [!tip]- Answer
> Expressive TTS lets the LLM laugh, whisper, and add expressiveness so the voice sounds human-like rather than robotic — sometimes indistinguishable from a real person when just listening. Pushing expressiveness can add hesitation artifacts that themselves carry unintended meaning, and when asked directly the agent must declare itself non-human per safety guidelines. See [[wiki/01-voice-agents-latency-turn-taking-safety|Expressive text-to-speech]].

### Q3. Why is latency framed as "perceived," and which two audio techniques keep the caller from thinking the call dropped?
> [!tip]- Answer
> Latency is treated as perceived because callers tolerate waiting as long as they hear the connection is alive and work is happening. The agent keeps audible presence (office noise, music) so the user knows the call has not dropped, and narrates slow tool-calling ("I'm gonna look you up in the system") with cues like keyboard clicking so the user does not repeat themselves. See [[wiki/01-voice-agents-latency-turn-taking-safety|Latency: perceived latency and audio cues]].

### Q4. How does the turn-taking model handle a caller speaking while the agent talks?
> [!tip]- Answer
> Turn-taking is currently either-you-talk-or-I-talk, but callers may speak over the agent without necessarily interrupting it. The speech-to-text layer distinguishes backchannel affirmations ("yeah, yeah, okay") from genuine intent to take the turn, so naive cutoffs do not interrupt the agent when the user only meant to affirm. See [[wiki/01-voice-agents-latency-turn-taking-safety|Turn-taking and interruption handling]].

### Q5. How does the sidecar safety LLM work, and how do streaming and blocking modes trade safety against latency?
> [!tip]- Answer
> A second LLM stands on the side and cuts the conversation off if it goes off the rails, for example stopping a banking agent from giving financial advice. Streaming mode lets audio through and cuts on violation for lower added latency, while blocking mode verifies everything before audio for higher safety at the cost of more latency. See [[wiki/01-voice-agents-latency-turn-taking-safety|Tunability: speed vs expressiveness, guardrails, and routing]].

### Q6. How do router-to-sub-agent delegation and the layered SDK and platform tiers fit capacity and integration depth to the use case?
> [!tip]- Answer
> A fast low-intelligence router model (e.g. a secretary) delegates to a higher-capacity sub-agent, keeping or changing the voice to signal the handoff such as a tonality break for loan advice. Builders integrate at three depths — full Agents platform, standalone services with their own STT/LLM/TTS, or a middle speech-engine tier bringing only the brain — through cascading JS → React (hooks, provider) → React Native SDKs with headless or prebuilt chat-bubble UI. See [[wiki/01-voice-agents-latency-turn-taking-safety|SDKs and platform surface]].

### Q7. Evaluation: for a banking voice agent that must never give financial advice, which safety mode and expressiveness tuning would you recommend?
> [!tip]- Answer
> Recommend blocking mode despite its higher latency, because a streaming cutoff can leak the first syllables of forbidden advice before the guardrail reacts. Pair it with moderate rather than maximum expressiveness plus narrated tool-calling cues, accepting slightly slower, clearly non-human delivery in exchange for correctness and disclosure. See [[wiki/01-voice-agents-latency-turn-taking-safety|Tunability: speed vs expressiveness, guardrails, and routing]].
