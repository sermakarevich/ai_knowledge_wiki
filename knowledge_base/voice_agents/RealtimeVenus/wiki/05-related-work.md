[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Related work
**In one sentence:** The chunk is headed "4 speech recognition (ASR) and text-to-speech" but its body is largely §3 System Overview (full-duplex frontend plus asynchronous harness delegation), citing only GPT-Realtime's asynchronous function calling and VoiceChat's separate tool-call output channel as related work.
## Key points
- GPT-Realtime (OpenAI, 2025) supports asynchronous function calling, per the chunk's related-work note.
- NemotronLabs VoiceChat (NVIDIA, 2026) provides a separate output channel for tool-calling scripts, per the chunk.
- Realtime-Venus studies a private delegation interface for separately trained audio and omni frontends.
- Realtime-Venus-Harness "fixes evidence at the request boundary, executes registered capabilities, and returns results to the originating session for integration into the current dialogue."
- Each session uses either Realtime-Venus-Audio (continuous audio) or Realtime-Venus-Omni (additionally visual inputs); both share the same delegation interface where the frontend handles live interaction and speech output and the harness executes delegated tasks and prepares replies.
- The frontend provides streaming text and speech output through its native Thinker–Talker architecture, and perception remains active during speech and background task execution.
- The interaction loop runs continuously and is latency-sensitive while the capability loop handles tasks on demand over potentially longer durations; their shared interface exchanges a task package bounded by the request's causal context and a prepared reply bound to the originating session.
---
## 4 speech recognition (ASR) and text-to-speech
**Covers:** Related work on omni models, audio, full-duplex, and tool use (chunk 05-4-speech-recognition-asr-and-text-to-speech; note: body text is largely §3 System Overview, not ASR/TTS detail)

The chunk's only ASR/TTS-headed related-work claims are, verbatim in substance:
- "GPT-Realtime (OpenAI, 2025) supports asynchronous function calling"
- "NemotronLabs VoiceChat (NVIDIA, 2026) provides a separate output channel for tool-calling scripts."
- "We study a private delegation interface for separately trained audio and omni frontends."
- "Realtime-Venus-Harness clarifies execution boundaries by fixing evidence at the request boundary, executing registered capabilities, and returning results to the originating session for integration into the current dialogue."

## 3 System Overview (as present in this chunk)
**Covers:** §3 body through Figure 4 as extracted in the chunk

- "Realtime-Venus combines a full-duplex conversational frontend with Realtime-Venus-Harness for asynchronous capability execution and reply preparation."
- "Each session uses either Realtime-Venus-Audio, which processes continuous audio, or Realtime-Venus-Omni, which additionally processes visual inputs."
- "Both share the same delegation interface: the frontend handles live interaction and speech output, while the harness executes delegated tasks and prepares replies."
- "Figure 3 summarizes the architecture" (caption in chunk: "Figure 3 Realtime-Venus runtime: full-duplex interaction with asynchronous delegation."), with interaction loop (full-duplex) vs capability loop (asynchronous), tracked work states Queued / Running / Completed / Delivering / Delivered, and user backends "LLM APIs · Agents".

## 3.1 Dual-loop architecture (as present in this chunk)
**Covers:** Interaction loop vs capability loop paragraphs

| Loop | Mechanism (verbatim/substance from chunk) |
|---|---|
| Interaction loop | "continuously processes incoming media, updates the session state, and controls when to listen, speak, or yield"; "handles requests that can be answered directly"; streaming text and speech via "native Thinker–Talker architecture"; "Perception remains active during speech and background task execution." |
| Capability loop | Activated by "a private natural-language delegation request from the frontend"; "host hides the request span from user-facing output, captures the context available at the request boundary, and creates an asynchronous work item"; "harness selects a backend capability, executes the task, and polishes the result into a reply for spoken delivery"; "Eligible replies return to the originating session through the private background channel"; "frontend chooses when to speak the prepared text ...; the harness determines its content and wording." |

Interface claim (verbatim substance): "The interaction loop runs continuously and is latency-sensitive, while the capability loop handles tasks on demand over potentially longer durations. Their shared interface exchanges a task package bounded by the request's causal context and a prepared reply bound to the originating session, allowing asynchronous execution alongside live interaction, as illustrated in Figure 4."

Figure 4 examples as given in the chunk (caption: "Figure 4 Example interactions with Realtime-Venus."):
- Omni-Proactive (Realtime-Venus-Omni): user at 00:03 "When the referee blows the whistle, please remind me."; assistant at 00:16 "The referee has blown the whistle! The game has started."
- Delegate (Realtime-Venus-Omni): user 00:03–00:08 "请你帮我查询一下北京今天汽车限行尾号。"; ack 00:08–00:10 "好的，我查询一下。"; "Query external service... Waiting for result (5s)" 00:10–00:15; answer 00:15–00:22 "今天北京市限行尾号为 3 和 8，限行时间为 7:00–20:00."
- Audio-interruption (Realtime-Venus-Audio): user 00:01–00:05 "Help me plan a three-day road trip with safe pacing."; assistant 00:05–00:13 "Aim for 5–7 driving hours daily, take a break every two hours, plus lunch and an [truncated]"; user interruption 13s–15s "What should each day look like for breaks and meals?"; new response 00:15–00:30 "Start after breakfast, drive two hours, then take a short break. Drive two more hours, stop for lunch, and continue one to three hours before dinner and overnight rest."

**Covers:** chunk 05-4-speech-recognition-asr-and-text-to-speech.md (§4 header + §3/3.1/Fig 3–4 text as extracted) → plan row Covers "Related work on omni models, audio, full-duplex, and tool use"
