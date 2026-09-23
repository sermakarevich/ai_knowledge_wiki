> [[index|Wiki]] | [[summary|Summary]]
# Find and Fix Latency Leaks in Real-time Voice Agents (Pipecat) — Digest
## 1. [[wiki/01-latency-leaks-in-pipecat-voice-agents|What Really Makes or Breaks a Voice App]]
**In one sentence:** Latency between a voice command and the system's response makes or breaks a voice app, and in a Pipecat voice-to-video demo the dominant leak was local Whisper STT at ~2.48 s, fixed by switching to remote Deepgram STT at ~0.001 s TTFB.
## Key points
- What makes or breaks a voice app is latency: how long the system takes to respond after the user gives a command.
- In the voice-to-video demo (voice command switches the playing video), the delay between command and video switch was substantial and destroyed the user experience.
- The pipeline is audio input → speech-to-text → aggregating for LLM → LLM (selects video ID) → video processor (plays/switches video), and the delay could be in any step.
- Pipecat puts all modules under the app's control, so per-module latency is measured by enabling a logging flag that records time taken by each frame processor, plus manual timing in the custom video module's `process_frame` (prints when extraction/switching takes more than ~0.7 seconds).
- Logs showed local Whisper STT time-to-first-frame of 2.48 seconds for a short utterance (the whole processing time), which was judged completely unacceptable and the suspected root cause.
- The Groq LLM was fast despite running on a remote API server: time-to-first-buffer ~0.13 seconds (135 ms) and total processing ~160 ms, so it was not the problem.
- Switching STT from local Whisper to remote Deepgram via a one-line Pipecat plugin change made switching feel instant ("Google video… that was quick; SAM video… awesome"), with Deepgram TTFB ~0.001 seconds even though remote.
- After the fix the LLM (~124+ ms / ~156 ms) became the relative bottleneck, and the lesson is that production apps need a robust per-component latency monitoring framework because many more leaks arise (TTS delay, geographic network delays, unoptimized private Docker/Kubernetes hosting, WebSocket vs WebRTC vs SIP).
## The argument in five moves
1. What makes or breaks a voice app is response latency, and the voice-to-video demo's substantial command-to-switch delay destroyed its user experience.
2. Because the delay could hide in any pipeline step (STT → LLM → video processor), debugging requires a systematic per-module measurement method.
3. Pipecat enables that method via a logging flag for built-in frame processors plus manual timing in the custom video module, which isolated local Whisper STT (~2.48 s) as the dominant leak while exonerating the Groq LLM (~135 ms TTFB / ~160 ms total).
4. A one-line Pipecat plugin swap from local Whisper to remote Deepgram STT (~0.001 s TTFB) made switching feel instant, shifting the relative bottleneck to the LLM (~124+ ms / ~156 ms).
5. Since production adds many more leak sources (TTS, geography, private hosting, transport protocols), the durable lesson is to run a robust per-component latency monitoring framework and fix delays systematically.
