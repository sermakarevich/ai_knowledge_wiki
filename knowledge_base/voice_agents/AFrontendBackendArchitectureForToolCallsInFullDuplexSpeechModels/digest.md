> [[index|Wiki]] | [[summary|Summary]]
# A frontend-backend architecture for tool calls in full-duplex speech models — Digest

## 1. [[wiki/01-frontend-backend-architecture|A Frontend-Backend Architecture for Tool Calls]]
**In one sentence:** This chunk is garbled and contains no substantive claims beyond the paper title, author list, and a truncated abstract fragment.
## Key points
- The chunk file contains only the paper title "A FRONTEND-BACKEND ARCHITECTURE FOR TOOL CALLS IN FULL-DUPLEX SPEECH MODELS".
- The chunk file lists the authors (Ke Hu et al., NVIDIA, USA) with no further content.
- The only body text present is a truncated abstract fragment ("ters and context budget that text-only LLMs can devote to factual").
- No mechanisms, numbers, tables, or verbatim quotes beyond the title block can be extracted from this chunk.
- No factual claims about the frontend-backend architecture are present in this chunk, so none are stated here to avoid invention.

## 2. [[wiki/02-background-related-work|Background and Related Work: Why Delegate Tool Calls to a Backend]]
**In one sentence:** The chunk argues that full-duplex speech-to-speech models excel at natural low-latency interaction but lag text agents at tool calls, so instead of internalizing tool use the duplex speech-to-text frontend should emit a delegation token and hand streaming ASR transcripts to a text backend LLM whose results are prefilled back and spoken via streaming TTS.
## Key points
- Full-duplex speech-to-speech models give natural low-latency conversation with paralinguistic cues, turn-taking, and barge-in, but their voice-agent tool-call ability lags text agents.
- The gap is quantified via τ-Voice [24]: leading commercial duplex voice models complete only 31−51% of grounded customer-service tasks under clean conditions versus 85% for text agents such as GPT-5 on corresponding text-mode tasks, widening under noise and accented speech.
- The chunk poses a design choice: should duplex speech models directly internalize tool-call capabilities, or delegate to a backend text agent with mature instruction following, tool calls, and long-horizon reasoning.
- The proposed answer is delegation: a duplex speech-to-text frontend learns a delegation token, forwards streaming ASR transcripts to a text backend LLM (LangGraph framework [33]), stays silent during the call, then repeats the backend result injected via a lightweight prefill-and-repeat mechanism and streaming TTS.
- Audio-native modeling is claimed to impose "a fundamental capacity tradeoff," with the visible fragment stating "audio tokens consume parame-" (sentence truncated in the chunk).
- Reported results in the chunk: 92–97% tool-call recall in single-turn evaluation, competitive tool-call prediction, 81.2% accuracy rejecting irrelevant calls, and with a larger backend (e.g., Qwen3-235B-A22B) competitive Full-Duplex-Bench-V3 results plus EVA-Bench outperformance of GPT-realtime-mini and Qwen3-Omni-30B-A3B-Instruct.
- Concurrent hybrid designs listed are KAME [26], MoshiRAG [27], Thinking Machines [28], Qwen-audio-agent [29], and GPT-Live [30], plus cascaded systems NVIDIA Nemotron Voice Agent [39] and LiveKit EXA Deep Researcher [40]; the chunk says how the delegation signal and background-frontend interaction work in [28, 29, 30] remains unclear.

## 3. [[wiki/03-architecture-training-results|Architecture, Training and Results: STT Frontend, LangGraph Backend, Tool-Call Delegation]]
**In one sentence:** The paper trains a duplex speech-to-text frontend to emit a delegation token pair (`<tc bos>`/`<tc eos>`) in the agent-text channel when a tool is needed, routes the endpointed transcript to a LangGraph ReAct backend that runs multi-round tool calls, and prefills the backend's natural-language answer back into the frontend for spoken generation.
## Key points
- Frontend is a duplex STT model with three input streams (user speech, user transcript, agent text): a 600M-parameter Parakeet streaming encoder plus NVIDIA Nemotron-Nano-9B-v2-Base backbone, with a separate ASR embedding/prediction head sharing the backbone and a single decoding pass producing user and agent text jointly.
- Delegation mechanism: if user speech needs a tool (e.g. "what is the weather in New York?"), the agent-text channel fires `<tc bos>` (replacing regular `<agent bos>`, usually 320 ms after user-turn end), then a ~1 s filler, then `<tc eos>`; the backend answer is enclosed `<pf bos>`/`<pf eos>` and prefilled ~1 s after `<tc eos>`, which the frontend learns to continue from `<agent bos>`.
- At inference the `<user eos>`-endpointed transcript is sent to the backend, the backend's natural-language response is injected into the agent-text channel, and agent output is suppressed with pad tokens during the call; pad/silence regions with prefilled text are excluded from loss in training.
- Backend (Sec. 3.2) is LangGraph [33], a tool-augmented ReAct agent [16]: a state machine over a running message list with an instruction-following LLM agent node, a tools node, a conditional edge routing to tool execution whenever calls are emitted, and a thread-keyed checkpointer for multi-turn state; invalid tool-call syntax or plain-text replies are returned directly as prefill, so the larger backend falls back to natural-language explanations when the frontend misfires.
- Training (Sec. 4) is pretrain + SFT with ~530k hours pretraining, 111k hours SFT, ~16k hours ASR transcription, and 8.5k hours multi-turn tool-call data; text dialogues are generated by Nemotron 3 Nano / Gemma-4-31B-IT / Qwen3.5-397B-A17B then LLM-judge filtered, audiofied via filtering (drop math/code-heavy), VoiceChat-TTS, and Parakeet-tdt-0.6b-v2 WER/CER filtering, plus domain data (airline/retail) from two Qwen3.5-235B-A22B LLMs with failures discarded and user turns via Chatterbox.
- Frontend tool-call token recall is 97.2% (Simple), 92.0% (Multiple), 95.0% (Parallel), 93.5% (Parallel-Multiple); Ours-30B-extASR averages 74.6% BFCL AST vs 73.0% intASR, with Parallel-Multiple 55.1% → 61.1% from more accurate external ASR.
- On Full-Duplex-Bench v3 (100 real-human scenarios, 12 speakers) Res-Q is ~54–67% (larger Qwen3-235B-A22B backend better), turn-taking 100%, with high filler rate by design ("Let me pull that up") and high interruption rate from backchannels ("Okay, I am here.") while still listening; adding tool-call training only slightly degrades turn-taking Pr/Rec (85/94→82/91), ASR WER (10.80%→11.47%), and CommonEval (2.87→2.36).

## The argument in five moves
1. Full-duplex speech models deliver natural low-latency interaction but trail text agents badly on grounded tool-call tasks (31−51% vs 85%), so the paper rejects internalizing tool use in the audio-native model as a capacity tradeoff.
2. It instead splits the job: a duplex speech-to-text frontend owns interaction and learns a delegation token, while a mature text backend owns reasoning and tool execution.
3. The handoff is made minimal and modular — `<tc bos>`/`<tc eos>` detection, filler plus silence during the call, endpointed transcript routing, and prefill-and-repeat of the backend answer for spoken generation.
4. The backend is a LangGraph ReAct agent with multi-round tool execution and multi-turn state, with safe fallback to natural-language prefill when the frontend misfires or syntax is invalid.
5. Trained at scale (pretrain + SFT with synthetic audiofied tool-call dialogues), the system reaches 92–97% delegation recall and competitive BFCL/FDB3/EVA-Bench results that scale with backend size, at only small cost to turn-taking, ASR, and chat quality.
