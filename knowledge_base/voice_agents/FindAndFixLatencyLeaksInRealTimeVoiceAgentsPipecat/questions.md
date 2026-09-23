---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: Find and Fix Latency Leaks in Real-time Voice Agents (Pipecat)
### Q1. What single factor makes or breaks a voice app, and what symptom in the voice-to-video demo showed it was broken?
> [!tip]- Answer
> What makes or breaks a voice app is latency: how long the system takes to respond after the user gives a command. In the voice-to-video demo, the delay between saying a command like "Google IO" or "Sam video" and the video actually switching was substantial enough to destroy the user experience. See [[wiki/01-latency-leaks-in-pipecat-voice-agents|What Really Makes or Breaks a Voice App]].
### Q2. What are the stages of the voice-to-video pipeline under test, and why does that structure make ad-hoc debugging unreliable?
> [!tip]- Answer
> The pipeline runs audio input → speech-to-text → aggregating for the LLM → LLM (selects the video ID) → video processor (plays/switches the video). Because the delay could hide in any one of these steps, guessing without measurement cannot reliably locate the leak. That is why the video argues for a systematic per-module measurement method. See [[wiki/01-latency-leaks-in-pipecat-voice-agents|What Really Makes or Breaks a Voice App]].
### Q3. How was per-module latency instrumented in Pipecat, including the custom video module?
> [!tip]- Answer
> Pipecat keeps all modules under the app's control, so enabling a logging flag automatically records the time taken by each built-in frame processor, including STT. The custom video-playing module is not covered by that flag, so its `process_frame` was timed manually, printing whenever extraction/switching took more than ~0.7 seconds. See [[wiki/01-latency-leaks-in-pipecat-voice-agents|What Really Makes or Breaks a Voice App]].
### Q4. What did the logs reveal about local Whisper STT versus the Groq LLM, and what verdict followed?
> [!tip]- Answer
> Local Whisper STT took ~2.48 seconds time-to-first-frame for a short utterance, which was judged completely unacceptable since it consumed nearly the whole processing time. The remote Groq LLM, by contrast, reached first buffer in ~0.13 seconds (135 ms) with ~160 ms total processing, so it was exonerated. The verdict was that the locally hosted, unoptimized Whisper STT module was the dominant latency leak. See [[wiki/01-latency-leaks-in-pipecat-voice-agents|What Really Makes or Breaks a Voice App]].
### Q5. What was the fix for the STT bottleneck, and what were the before/after results?
> [!tip]- Answer
> The fix was swapping local Whisper for remote Deepgram STT via a one-line Pipecat plugin change. Before the swap, commands lagged ~2.5 seconds at the STT step; after it, switching felt instant ("that was quick… awesome") with Deepgram TTFB around ~0.001 seconds despite being remote. The remote service won because it is highly optimized for small utterances. See [[wiki/01-latency-leaks-in-pipecat-voice-agents|What Really Makes or Breaks a Voice App]].
### Q6. After the fix, which component became the relative bottleneck, and what further leak sources does the production lesson warn about?
> [!tip]- Answer
> After the Deepgram swap, the LLM at roughly 124–156 ms became the relative bottleneck of the now-fast pipeline. The production lesson warns that many more leaks arise at scale: TTS delay, geographic network delays, unoptimized private Docker/Kubernetes model hosting, and transport choices such as WebSocket vs WebRTC vs SIP. Hence the call for a robust per-component latency monitoring framework. See [[wiki/01-latency-leaks-in-pipecat-voice-agents|What Really Makes or Breaks a Voice App]].
### Q7. (Evaluation) A production voice agent gets complaints about sluggish responses but no one knows which stage is slow — what triage approach would you recommend and why?
> [!tip]- Answer
> I would recommend deploying per-component latency monitoring across every stage (STT, LLM, TTS, network, hosting, transport) and then fixing the measured worst leak first, as in the demo. This beats swapping components on intuition because a single unoptimized stage can dominate total latency while remote services may paradoxically be faster. Systematic measurement also transfers directly to the production leak sources the video lists. See [[wiki/01-latency-leaks-in-pipecat-voice-agents|What Really Makes or Breaks a Voice App]].
