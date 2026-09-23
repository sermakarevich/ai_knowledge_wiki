> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Background and Related Work: Why Delegate Tool Calls to a Backend
**In one sentence:** The chunk argues that full-duplex speech-to-speech models excel at natural low-latency interaction but lag text agents at tool calls, so instead of internalizing tool use the duplex speech-to-text frontend should emit a delegation token and hand streaming ASR transcripts to a text backend LLM whose results are prefilled back and spoken via streaming TTS.
## Key points
- Full-duplex speech-to-speech models give natural low-latency conversation with paralinguistic cues, turn-taking, and barge-in, but their voice-agent tool-call ability lags text agents.
- The gap is quantified via τ-Voice [24]: leading commercial duplex voice models complete only 31−51% of grounded customer-service tasks under clean conditions versus 85% for text agents such as GPT-5 on corresponding text-mode tasks, widening under noise and accented speech.
- The chunk poses a design choice: should duplex speech models directly internalize tool-call capabilities, or delegate to a backend text agent with mature instruction following, tool calls, and long-horizon reasoning.
- The proposed answer is delegation: a duplex speech-to-text frontend learns a delegation token, forwards streaming ASR transcripts to a text backend LLM (LangGraph framework [33]), stays silent during the call, then repeats the backend result injected via a lightweight prefill-and-repeat mechanism and streaming TTS.
- Audio-native modeling is claimed to impose "a fundamental capacity tradeoff," with the visible fragment stating "audio tokens consume parame-" (sentence truncated in the chunk).
- Reported results in the chunk: 92–97% tool-call recall in single-turn evaluation, competitive tool-call prediction, 81.2% accuracy rejecting irrelevant calls, and with a larger backend (e.g., Qwen3-235B-A22B) competitive Full-Duplex-Bench-V3 results plus EVA-Bench outperformance of GPT-realtime-mini and Qwen3-Omni-30B-A3B-Instruct.
- Concurrent hybrid designs listed are KAME [26], MoshiRAG [27], Thinking Machines [28], Qwen-audio-agent [29], and GPT-Live [30], plus cascaded systems NVIDIA Nemotron Voice Agent [39] and LiveKit EXA Deep Researcher [40]; the chunk says how the delegation signal and background-frontend interaction work in [28, 29, 30] remains unclear.
---
## Motivation and capability gap
The chunk states duplex speech-to-speech models operate directly in the speech modality, eliminating cascade latency and preserving paralinguistic cues with natural turn-taking and barge-in behavior [10, 11, 12, 13]. Text-based LLMs serve as reliable tool-using agents that decide when and how to invoke tools, query knowledge bases, and act on the world [14–19]. Voice-agent tool calls remain "substantially behind" text agents, citing τ-Voice [24]: 31−51% task completion for commercial duplex voice models under clean conditions versus 85% for GPT-5 on text-mode tasks, with the gap widening under realistic noise and accented speech.
**Covers:** Sect. 1 INTRODUCTION, motivation paragraphs.

## Direct modeling versus backend delegation
The chunk frames the question as "whether duplex speech models should directly internalize tool-call capabilities or instead delegate such capabilities to a backend text agent that already benefits from mature instruction following, tool calls, and long-horizon reasoning abilities." It notes recent work puts tool calls in a separate channel inside Moshi-style [4] duplex models [25], but claims audio-native modeling imposes a fundamental capacity tradeoff (fragment: "audio tokens consume parame-"). By contrast, "a delegation-style backend agent is more modular and consumes little modeling capacity from a frontend speech model," and the authors' conclusion is quoted verbatim: "backend delegation is an effective and modular approach for combining natural duplex speech interaction with strong agentic tool-call capabilities."
**Covers:** Sect. 1 INTRODUCTION, design-choice paragraphs.

## Concurrent hybrid designs
The chunk lists hybrids keeping a speech frontend for interaction while delegating reasoning/tool calls to a text backend: KAME [26] "injects backend 'oracle' tokens into a Moshi-style [4] S2S frontend for knowledge integration"; MoshiRAG [27] "augments Moshi with retrieval"; Thinking Machines [28] "proposes an interaction-background framework for user queries requiring deeper reasoning, tool calls, or long-horizon work"; "More recently, Qwen-audio-agent [29] and GPT-Live [30] also adopt similar frameworks." It adds: "However, it remains unclear how the delegation signal in [28, 29, 30] is designed and background model interacts with the duplex frontend."
**Covers:** Sect. 2 RELATED WORK, concurrent-designs paragraph.

## Cascaded frontend–backend systems
The chunk names "Cascaded frontend–backend systems, such as NVIDIA's Nemotron Voice Agent [39] and LiveKit's EXA Deep Researcher [40], combine ASR, LLM, and TTS into a frontend and use a separate backend for planning and tool execution," noting recent systems increasingly explore tool use and backend agents in real-time voice interaction.
**Covers:** Sect. 2 RELATED WORK, cascaded-systems paragraph.

## Architecture sketch given in this chunk
The chunk describes the system as a duplex speech-to-text frontend (based on [6, 31]) plus streaming TTS [32], with the frontend taking "user speech encoding, agent text and streaming user ASR transcript as inputs [31]." It predicts a delegation token for tool-call queries, sends streaming ASR transcripts to the backend LLM in a LangGraph framework [33], remains silent during the call, then the backend's natural-language result is "sent back to the frontend agent text channel via a prefill mechanism and the frontend is then trained to repeat the result," resuming normal duplex behavior afterward. The design "imposes minimal changes on the frontend duplex STT model by adding a tool-call control token to its prediction targets." Figure fragment shows control tokens including `<agent_bos>`, `<tc_bos>` ("Yes (<tc_bos>)"), `<tc eos>`, `<turn-1>`/`<turn_1>`, `<turn-2>`, and `<silence>`, with Text head, ASR head, and "Prefill" from agent text into the frontend. Training fragment: tool-call response text is prefilled into the agent text channel and the frontend is trained to reproduce it exactly; "tool-call tokens, filler, and reproduced regions are used for loss computation in the same way as for regular agent text, while prefill regions are masked and excluded from loss computation." Inference: "we send the streaming ASR transcript to the backend for tool call execution when <tc eos> fires." The frontend connects to VoiceChat-TTS [32], which "accepts explicit turn start and interruption control tokens and incrementally generates codec-based speech tokens." Demo link in chunk: https://huggingface.co/spaces/frontend-backend-duplex/demo
**Covers:** abstract + introduction architecture paragraphs + figure/training fragment (Sect. 3 pointer "see Sect. 3.2").

## Evaluation claims stated in this chunk
| Claim | Exact value in chunk |
|---|---|
| Single-turn tool-call recall (speech version of BFCL [34]) | 92–97% ("92% to 97% recall") |
| Rejecting irrelevant calls | 81.2% accuracy ("rejects irrelevant calls up to 81.2%") |
| Full-Duplex-Bench-V3 [35] (naturalistic queries with pauses, hesitations, self-corrections), Qwen3-235B-A22B backend | "response quality similar to GPT-realtime-mini"; "competitive results ... compared to open and closed source models" |
| EVA-Bench [36] (multi-turn conversations and tool calls) | "significantly outperforms GPT-realtime-mini and Qwen3-Omni-30B-A3B-Instruct [37], and performs similarly to Gemini 3.1 Flash Lite [38]" |
**Covers:** abstract + introduction results paragraphs.
