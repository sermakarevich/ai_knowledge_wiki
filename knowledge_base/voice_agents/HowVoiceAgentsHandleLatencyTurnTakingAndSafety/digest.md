> [[index|Wiki]] | [[summary|Summary]]
# How Voice Agents Handle Latency, Turn-Taking, and Safety | Interview With Kræn Hansen — Digest

## 1. [[wiki/01-voice-agents-latency-turn-taking-safety|When We Turn Text Into Speech: Voice-Agent Pipeline, Latency, Turn-Taking, and Safety]]
**In one sentence:** A voice agent turns speech into text, reasons with a text LLM, and speaks the answer back with expressive TTS, while perceived latency is managed with audio cues, intelligent turn-taking, tunable speed/expressiveness tradeoffs, streaming-or-blocking safety guardrails, and fast-router-to-sub-agent delegation.
## Key points
- The pipeline is speech → text via speech-to-text, reasoning and output text via a text-based LLM, then text → speech on the other side.
- Expressive TTS lets the LLM laugh, whisper, and add expressiveness so the voice sounds human-like rather than robotic — sometimes indistinguishable from a real person when just listening.
- The LLM accounts for about 40 to 70% of pipeline latency, and pushing expressiveness can add latency artifacts that make speech sound more hesitant than intended.
- Latency is treated as perceived: background presence (office noise, music) signals the connection has not dropped, and tool-calling is narrated ("I'm gonna look you up in the system") plus audio cues such as keyboard clicking while work happens.
- Turn-taking is currently either-you-talk-or-I-talk, but the speech-to-text layer distinguishes affirmations ("yeah, yeah, okay") from real intent to interrupt so backchannels do not cut the agent off.
- The general tuning rule is that the faster the stack is made, the less expressive or less correct it becomes.
- Safety uses a second LLM standing on the side that cuts the conversation off if it goes off the rails (e.g. a banking agent must not give financial advice), in either streaming mode (audio passes through, cut on violation) or blocking mode (everything verified before audio), where blocking is safer but adds more latency.
- Routing and SDKs are layered for fit: a fast low-intelligence model (e.g. a secretary router) can delegate to a higher-capacity sub-agent with the same or a different voice, and the SDKs cascade from a universal platform-agnostic JavaScript library to a React package (hooks, provider) to a React Native package (audio input), with headless or prebuilt UI/chat-bubble options.

## The argument in five moves
1. A voice agent is a speech-to-text → text-LLM → text-to-speech pipeline where expressive TTS makes the output strikingly human-like.
2. Latency is the central pain point, with the LLM alone taking roughly 40–70% of pipeline time, so it is managed as perceived latency through presence audio and narrated tool-calling cues.
3. Turn-taking stays either-you-talk-or-I-talk, made tolerable by distinguishing mere backchannel affirmations from genuine interruptions.
4. Everything is tunable under one rule — faster means less expressive or less correct — covering expressiveness settings, streaming-versus-blocking safety guardrails, and router-to-sub-agent delegation.
5. Safety is enforced by a sidecar LLM that cuts off out-of-bounds speech, choosing streaming for lower latency or blocking for higher safety.
6. The whole stack is delivered through layered, code-generated SDKs and platform tiers so builders can bring their own components or adopt the full platform.
