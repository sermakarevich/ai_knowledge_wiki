---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: A frontend-backend architecture for tool calls in full-duplex speech models

### Q1. What does the wiki's first page actually contain about this paper, and what can you legitimately recall from it?

> [!tip]- Answer
> It contains only the paper title "A FRONTEND-BACKEND ARCHITECTURE FOR TOOL CALLS IN FULL-DUPLEX SPEECH MODELS", the author list (Ke Hu et al., NVIDIA, USA), and one truncated abstract fragment — no mechanisms, numbers, or results. The honest recall is therefore just the framing: a duplex speech frontend delegating tool calls to a text backend, with all substantive detail coming from later pages. See [[wiki/01-frontend-backend-architecture|Architecture]].

### Q2. Why does the paper argue duplex speech models should delegate tool calls to a backend instead of internalizing them, and what numbers motivate this?

> [!tip]- Answer
> Full-duplex speech-to-speech models give natural low-latency interaction with turn-taking and barge-in, but on τ-Voice grounded customer-service tasks they complete only 31−51% versus 85% for text agents like GPT-5, with the gap widening under noise and accents. The paper frames this as a design choice and claims audio-native modeling imposes a fundamental capacity tradeoff, so delegation to a mature text backend is more modular and costs the frontend little modeling capacity. See [[wiki/02-background-related-work|Background]].

### Q3. How does this paper's delegation design differ from KAME, MoshiRAG, Thinking Machines, Qwen-audio-agent, and GPT-Live, and where do cascaded systems fit?

> [!tip]- Answer
> KAME streams backend "oracle" tokens into a Moshi-style frontend every 100–500 ms for the frontend to anchor on, and MoshiRAG injects retrieved context into the inner-monologue stream, while this paper uses a minimal explicit delegation token plus prefill-and-repeat of the finished answer. For Thinking Machines, Qwen-audio-agent, and GPT-Live the paper says the delegation signal and backend-frontend interaction remain unclear, which is the gap it claims to fill with an explicit token design. Cascaded systems like NVIDIA Nemotron Voice Agent and LiveKit EXA Deep Researcher are the older alternative: separate ASR plus LLM plus TTS pipeline with a separate planning backend, rather than one duplex model with a token handoff. See [[wiki/02-background-related-work|Background]].

### Q4. Walk through the exact token-level handoff when a user asks "what is the weather in New York?" — what fires, when, and what is masked in training?

> [!tip]- Answer
> The agent-text channel fires `<tc bos>` in place of the regular `<agent bos>`, usually 320 ms after the user turn ends, then a ~1 s filler phrase, then `<tc eos>`; the `<user eos>`-endpointed transcript is sent to the backend, and its natural-language answer enclosed in `<pf bos>`/`<pf eos>` is prefilled ~1 s after `<tc eos>` for the frontend to repeat from `<agent bos>`. During the call the agent channel is suppressed with pad tokens and the frontend stays silent, and in training the pad/silence regions carrying prefilled text are excluded from loss while tool-call tokens, filler, and reproduced regions are trained like normal agent text. See [[wiki/03-architecture-training-results|Architecture]].

### Q5. How does the LangGraph ReAct backend work, and what happens when the frontend misfires or the backend emits invalid syntax?

> [!tip]- Answer
> The backend is a state machine over a running message list with an instruction-following LLM agent node, a tools node, and a conditional edge that routes to tool execution whenever calls are emitted, plus a thread-keyed checkpointer holding multi-turn state so each turn needs only the current ASR transcript. If the backend produces syntactically invalid tool calls or a plain-text reply, that text is returned directly as prefill, so the larger backend gracefully falls back to a natural-language explanation when the frontend delegated unnecessarily. See [[wiki/03-architecture-training-results|Architecture]].

### Q6. What data was the system trained on, and what were the headline BFCL, Full-Duplex-Bench-V3, and EVA-Bench results?

> [!tip]- Answer
> Training is pretrain plus SFT totaling ~530k hours pretraining, 111k hours SFT, ~16k hours ASR transcription, and 8.5k hours multi-turn tool-call audio, with text dialogues from Nemotron 3 Nano, Gemma-4-31B-IT, and Qwen3.5-397B-A17B filtered by LLM judges, audiofied via VoiceChat-TTS with WER/CER filtering, plus airline/retail domain trajectories with failures discarded. Results: 92–97% frontend delegation recall with 81.2% irrelevance rejection, BFCL average 74.6% with external ASR, FDB-V3 response quality ~54–67% with 100% turn-taking but high filler and backchannel-interruption rates by design, and EVA-Bench strongly scaling with backend size while adding tool-call training only slightly degrades turn-taking, ASR WER (10.80%→11.47%), and chat quality. See [[wiki/03-architecture-training-results|Architecture]].

### Q7. A product team wants to ship this frontend-backend design for a noisy real-world customer-service voice agent: should they, and what is the single biggest risk to check first?

> [!tip]- Answer
> They should pilot it rather than ship blindly, because delegation genuinely combines natural duplex interaction (100% turn-taking) with backend tool-call strength that scales with model size, but the headline benchmarks lean on clean single-turn recall and mock APIs. The biggest risk to check first is robustness under noise, accents, and disfluency: the motivating τ-Voice gap widens exactly there, external ASR quality already swings Parallel-Multiple scores by ~6 points, and the frontend's backchannel interruptions plus filler behavior need live testing before they read as helpful rather than disruptive. See [[wiki/03-architecture-training-results|Architecture]].
