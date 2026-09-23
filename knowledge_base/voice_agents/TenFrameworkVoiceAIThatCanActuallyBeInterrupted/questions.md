---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: TEN Framework: Voice AI That Can Actually Be Interrupted

### Q1. What is TEN Framework and what test does the chunk use to judge it?
> [!tip]- Answer
> TEN Framework is an open-source runtime for real-time multi-model conversational voice AI, covering streaming audio, interruptions, turn detection, avatars, telephony, and edge deployment. The chunk frames it as built for live conversation rather than text-first with voice dropped on top, and the pass/fail test is whether it can be interrupted mid-sentence without falling apart. See [[wiki/01-is-this-one-of-the-best|Is this one of the best]].

### Q2. Why does a simple STT → LLM → TTS chain collapse in real conversations?
> [!tip]- Answer
> A simple chain works for basic setups but falls apart because real users interrupt while audio keeps streaming and the model is still thinking. It has no built-in way to stop speaking, cancel generation, detect silence, or run tool calls in parallel. TEN replaces the chain with a graph of single-job extensions to handle exactly that messiness. See [[wiki/01-is-this-one-of-the-best|Is this one of the best]].

### Q3. How does TEN's graph-of-extensions architecture handle interruptions?
> [!tip]- Answer
> TEN models an agent as a graph of extensions where STT, LLM, TTS, memory, tools, VAD, and turn detection are separate connected nodes instead of one forced pipeline. Each extension has one job and they work together, so the agent can stop speaking, cancel generation, detect silence, and call tools in parallel. Extensions can be written in Python, C++, Go, Rust, or TypeScript. See [[wiki/01-is-this-one-of-the-best|Is this one of the best]].

### Q4. What setup does TEN require and which ready-made configurations are mentioned?
> [!tip]- Answer
> Setup requires API keys for Agora for real-time audio, Deepgram for speech recognition, an LLM such as OpenAI, and ElevenLabs for voice, followed by one Docker Compose up command that takes a few minutes the first time. TEN ships several ready-made configs, with the Deepgram TTS assistant presented as the best option, a voice assistant as the second-best alternative, and XAI-based ones described as not as good. See [[wiki/01-is-this-one-of-the-best|Is this one of the best]].

### Q5. What did the live interruption tests actually show?
> [!tip]- Answer
> The tests confirmed the core promise: the agent could be cut off mid-sentence without collapsing, which the presenter called really cool. Answer quality was still imperfect — it misheard a TEN question as TensorFlow, could not explain its own purpose, and could not give the Paris weather. So interruption handling held up while correctness stayed bounded by the underlying models. See [[wiki/01-is-this-one-of-the-best|Is this one of the best]].

### Q6. What is the TEN designer tool for, and what are TEN's stated strong points?
> [!tip]- Answer
> The designer tool visualizes how extensions connect for a chosen configuration, showing dataflow such as the Agora RTC audio frame, which matters because real-time voice systems are hard to debug. Stated strengths include VAD and turn detection for natural listen-then-talk timing, many examples like avatars, SIP telephony, ESP32 hardware, and speaker diarization, plus open-source flexible deployment. The framing quote is that TEN gives the complexity of real-time voice AI an architecture rather than removing it. See [[wiki/01-is-this-one-of-the-best|Is this one of the best]].

### Q7. Evaluation: a team needs a production voice agent with frequent interruptions and low latency, but a colleague suggests a plain STT → LLM → TTS chain or LiveKit Agents for speed — what should you recommend and why?
> [!tip]- Answer
> Recommend TEN if natural interruption handling, low latency, multimodal input, or flexible deployment are the real requirements, since only the graph architecture stops speech, cancels generation, and parallelizes tools under barge-in. Recommend against TEN for a simple text agent where its setup is overkill, and prefer LiveKit Agents or PipeCat when the priority is the fastest voice prototype with least friction. The deciding factor is whether interruption robustness justifies the heavier multi-key Docker setup. See [[wiki/01-is-this-one-of-the-best|Is this one of the best]].
