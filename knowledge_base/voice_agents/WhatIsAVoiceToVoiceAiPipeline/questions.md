---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: What is a Voice to Voice AI Pipeline? | Reduce Latency & Add Emotion to Voice Agents

### Q1. What are the four stages of the classic voice agent pipeline, and what conversion happens at each boundary?
> [!tip]- Answer
> Voice input goes to speech-to-text, then to an LLM, then to text-to-speech, then out of the speaker for the user to hear. Speech is flattened into text on the way in and rebuilt from text into speech on the way out, so the middle of the pipeline only ever sees words. See [[wiki/01-voice-to-voice-ai-pipeline|Voice-to-Voice AI Pipeline — Emotion and Low Latency]].

### Q2. Why does converting voice to text destroy the emotional channel, using the chunk's "Mark" example?
> [!tip]- Answer
> A user saying "Hi, I want to talk to Mark" in anger transcribes to the same words as a calm request, so the LLM receives the sentence but never sees the anger behind it. Without the tone, the model cannot choose a response with the right feeling, and the exchange feels robotic. See [[wiki/01-voice-to-voice-ai-pipeline|Voice-to-Voice AI Pipeline — Emotion and Low Latency]].

### Q3. Why does bolting an emotion-detection library onto the old pipeline fail to restore emotion?
> [!tip]- Answer
> A bolt-on library operates on the transcription, but the emotional signal — sadness, anger, tone, urgency — lives in the audio, not the text. Once voice has been flattened to words, the information the detector would need is already gone. See [[wiki/01-voice-to-voice-ai-pipeline|Voice-to-Voice AI Pipeline — Emotion and Low Latency]].

### Q4. What does "voice in, voice out" mean, and which two problems does the chunk claim it solves?
> [!tip]- Answer
> Instead of voice → text → voice, voice is fed into the LLM as voice and voice comes back out, carrying meaning plus emotion and a narrative of what to respond and in which emotion. The chunk claims this solves latency and emotion understanding, making the exchange natural like one human speaking to another. See [[wiki/01-voice-to-voice-ai-pipeline|Voice-to-Voice AI Pipeline — Emotion and Low Latency]].

### Q5. How do the encoder, modality adapters, LLM, and vocoder each function in the voice-to-voice flow?
> [!tip]- Answer
> The encoder turns raw audio into voice/data vectors carrying meaning, emotion, tone, and speed; the modality adapters shrink those normally long vectors to an LLM-compatible length. The LLM takes voice vectors plus prompt and outputs voice vectors, and the vocoder converts those output vectors back into speech the user hears. See [[wiki/01-voice-to-voice-ai-pipeline|Voice-to-Voice AI Pipeline — Emotion and Low Latency]].

### Q6. Why does the chunk use Llama Omni instead of OpenAI GPT models for the voice-to-voice LLM?
> [!tip]- Answer
> The pipeline needs an LLM that accepts voice vectors as input, and closed-weight GPT models offer no way to change the input type, so they cannot take voice vectors. Llama Omni models are presented as voice-to-voice models that natively accept them, with the caveat that GPT models might support them in the future. See [[wiki/01-voice-to-voice-ai-pipeline|Voice-to-Voice AI Pipeline — Emotion and Low Latency]].

### Q7. Evaluation: a team building a booking agent with heavy tool calls and strict prompt control wants to switch to voice-to-voice for naturalness — should they?
> [!tip]- Answer
> They should not switch this use case, because the chunk's stated limitations are less accurate tool calling and less prompt control, which are exactly what a booking agent depends on. They should stay on STT → LLM → TTS like almost all real-world deployments the chunk has seen, and reserve voice-to-voice for cases where low latency and emotional naturalness matter most. See [[wiki/01-voice-to-voice-ai-pipeline|Voice-to-Voice AI Pipeline — Emotion and Low Latency]].
