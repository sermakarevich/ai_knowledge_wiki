> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Interaction-Control States and Listen/Speak Transitions
**In one sentence:** Realtime-Venus serializes user, assistant, and background streams into one-second chunk units controlled by listen/speak/turn-end states plus delegate/backend spans, with playback-aware text scheduling and chunk-level autoregressive modeling that distinguishes pauses, backchannels, and interruptions, trained on a 2.8M-sample corpus.
## Key points
- Three streams share one conversational clock in one-second chunks: user perceptual features (ViT + Whisper at ~10 audio features/sec for Omni, audio-only for Audio), assistant foreground text plus ~25 S3 speech tokens/sec plus hidden delegation text, and asynchronous backend text results.
- Serialization emits one `<unit> input → output </unit>` per chunk (e.g. chunk 6 `<|speak|> T`, chunk 7 `<|speak|> <delegate> T </delegate>`, chunk 14 with `<backend> T </backend>` input), with four added tokens `<delegate>`, `</delegate>`, `<backend>`, `</backend>` and background results inserted at chunk boundaries as external context, not prediction targets.
- Three state tokens give chunk-level turn control: `<|listen|>` (perceive without speaking), `<|speak|>` (active foreground generation), `<|turn_eos|>` (close a completed turn), used to interpret backchannels and coordinate listening/speaking transitions.
- Speech stays on the conversational clock via `n_k = arg min_n |τ_{k-1} + D(Y_{k,1:n}) − t_k|` (Eq. 2), emitting fewer text tokens when speech lags and more when playback capacity is available; training assigns text and S3 tokens to chunks by start time with no fixed text–speech ratio.
- Full-duplex interaction factorizes as `p_{θ,φ}(O_{1:K} | U, B) = ∏_k p_θ(c_k, Y_k, D_k | U_{≤k}, B_{≤k}, O_{<k}) p_φ(S_k | H_{≤k}, Y_{≤k}, S_{<k})` (Eq. 3), keeping acoustic generation outside the LLM while control, text, and delegation share one semantic representation.
- Overlaps are role-conditioned, not uniform stop signals: pauses/noise → `<|listen|>`; short backchannels ("yes"/"right") keep `<|speak|>`; floor-taking interruptions → `<|turn_eos|>`, then stop/reject, repair/update, or redirect/follow-up of the unspoken remainder while played audio is unchanged.
- Post-training corpus exceeds 2.8M samples in nine categories: ~70% video (Omni only) vs ~30% audio (shared), ~56% offline understanding, ~37% proactive duplex interaction, ~6% delegation; duplex and delegation sources include interruptions as ordinary supervision.
---
## Figure 6 — Unified stream serialization
**Covers:** Fig. 6 caption, assistant-status row, and stream labels

> "Figure 6 Unified stream serialization for concurrent perception, speech generation, and delegation."

Assistant-status row in chunk: `LISTEN LISTEN LISTEN SPEAK ... SPEAK`. Foreground example: "I'll check the latest reporting and compare the accounts." Delegation example: "<delegate> Search current reliable news sources for developments today in Israel and Gaza talks. </delegate>". Backend example: "<backend> Talks show limited progress over Hamas disarmament and Israeli withdrawal…</backend>". Labeled streams: `Assistant Stream`, `Background Stream` (plus user audio/video timeline context).

## User, assistant, and background streams
**Covers:** Sec. 4.3 stream definitions

- "The user stream is a causal sequence of time-aligned perceptual features." "In Realtime-Venus-Omni, projected features from ViT (Dosovitskiy et al., 2020) are interleaved with projected features from Whisper (Radford et al., 2023) at approximately 10 audio features per second; Realtime-Venus-Audio omits the visual features." "The stream remains active during assistant output, preserving visual events, pauses, feedback, and overlapping speech on the shared timeline."
- "The assistant stream combines foreground text, aligned S3 speech tokens (Du et al., 2024a,b) at about 25 tokens per second, and optional text-only delegation instructions." "LLM hidden states preserve contextual prosody during speech generation, while delegation instructions are routed to the backend rather than spoken."
- "The background stream is an asynchronous text-only sequence that connects the interaction models to a more capable backend agent for complex reasoning and tool-based tasks." "A delegation instruction launches backend computation, which incurs a variable response delay." "A pending task contributes no result tokens, allowing foreground interaction to continue." "Once eligible for delivery, its result is inserted before the assistant stream at an available chunk boundary as external context rather than a prediction target."

## Chunk serialization format
**Covers:** Sec. 4.3 serialization lines (chunks 5–8, 13–14)

"The three streams are interleaved into a single token stream consumed by the LLM backbone. The serialization takes the following form:"

| Chunk | Serialization in chunk |
|---|---|
| chunk 5 | `<unit> V A → <\|listen\|> </unit>` |
| chunk 6 | `<unit> V A → <\|speak\|> T <\|chunk_eos\|><\|turn_eos\|> </unit>` |
| chunk 7 | `<unit> V A → <\|speak\|> <delegate> T </delegate><\|chunk_eos\|><\|turn_eos\|> </unit>` |
| chunk 8 | `<unit> V A → <\|listen\|> </unit>` |
| chunk 13 | `<unit> V A → <\|listen\|> </unit>` |
| chunk 14 | `<unit> V A <backend> T </backend> → <\|speak\|> T <\|chunk_eos\|><\|turn_eos\|> </unit>` |

Notes: "Each line represents one unit, written as `<unit> input → output </unit>`." "Outputs are shown within one chunk for clarity; in practice, the text output tokens (T) of a single turn may span multiple consecutive chunks." "Here, T denotes text tokens, A an audio representation, and V a projected visual representation." "The V and A tokens are interleaved according to their arrival times in Realtime-Venus-Omni, whereas Realtime-Venus-Audio serializes only A."

## Delegate/backend and state control tokens
**Covers:** Sec. 4.3 control-token paragraphs

- "External tool requests appear as delegate spans, and their results appear as background spans on the shared timeline." "We add four control tokens—`<delegate>`, `</delegate>`, `<backend>`, and `</backend>`—to the tokenizer, input embeddings, and LM head."
- "When tools are required, the model emits a self-contained natural-language task inside a delegate span, which is hidden from display and speech." "The backend agent decomposes the task into one or more function calls and returns eligible results through a background span at an available input boundary." "An additional request arriving during assistant speech can therefore be dispatched without closing the foreground turn, while compound requests can trigger multiple calls in semantic order." "In both cases, tool execution proceeds asynchronously alongside foreground speech and perception."
- "Three state tokens represent full-duplex turn control. `<|listen|>` indicates continued perception without speech, `<|speak|>` marks active foreground generation, and `<|turn_eos|>` closes a completed assistant turn." "Together, they provide a compact chunk-level interface for interpreting backchannels, distinguishing interruptions, and coordinating transitions between listening and speaking."

## Playback-synchronized text emission (Eq. 2)
**Covers:** Sec. 4.3 speech-clock scheduling, Eq. (2)

"To synchronize generated speech with the conversational clock, we adapt text emission to accumulated playback progress. Let τ_{k−1} denote the end time of previously scheduled speech and D(Y_{k,1:n}) the estimated duration of the first n candidate text tokens. At chunk k, we select"

> "n_k = arg min_n |τ_{k−1} + D(Y_{k,1:n}) − t_k|, (2)"

"where t_k is the current chunk boundary and τ_{k−1} carries the accumulated playback progress." "The scheduler emits fewer text tokens when speech lags and more when playback capacity is available, aligning the response with the latest user audio and background results." "During training, text tokens and their corresponding S3 tokens are assigned to chunks by start time, teaching history-dependent interleaving without a fixed text-speech ratio."

## 4.4 Full-duplex interaction (Eq. 3)
**Covers:** Sec. 4.4, Eq. (3)

"We formulate spoken interaction as chunk-level autoregressive modeling over the three synchronized streams. Let U = (u_1, …, u_K) denote the causal user-audio features, B = (b_1, …, b_K) the sparse background results available at each chunk, and O_k = (c_k, Y_k, D_k, S_k) the assistant output at chunk k." "Here, c_k is an interaction-control token, Y_k is foreground response text, D_k is an optional delegate request, and S_k is the aligned S3 speech-token segment." "Fields that are inactive in a chunk are represented as empty sequences."

"The LLM with parameters θ predicts interaction control, foreground text, and delegate text, while the speech decoder with parameters ϕ generates speech tokens from the LLM hidden states H. The joint policy factorizes as"

> "p_{θ,ϕ}(O_{1:K} | U, B) = ∏_{k=1}^{K} p_θ(c_k, Y_k, D_k | U_{≤k}, B_{≤k}, O_{<k}) p_ϕ(S_k | H_{≤k}, Y_{≤k}, S_{<k}). (3)"

"This factorization keeps acoustic generation outside the main LLM while allowing speech, turn control, and delegation to share the same semantic representation." "Background results are external observations rather than model outputs and become available only after the corresponding backend computation finishes."

"The control variable c_k determines whether the assistant listens, speaks, or closes its current turn." "Because c_k is predicted from the same semantic representation used for response generation, overlapping audio is interpreted according to its conversational role rather than treated as a uniform stop signal."

## Interruption and overlap handling
**Covers:** Sec. 4.4 case list and event-conditioned control

- "Pauses and background noise. Silence, hesitation, or acoustic activity not directed at the assistant produces `<|listen|>`, keeping perception continuously active without prematurely starting or terminating a response."
- "Backchannels. A short acknowledgment such as 'yes' or 'right' does not claim the conversational floor. The model preserves `<|speak|>` and continues the current response plan."
- "Interruptions. When overlapping user speech takes the conversational floor with a correction, redirection, or new request, the model emits `<|turn_eos|>` to terminate the stale response. It then incorporates the new intent into its conversational state before generating the next `<|speak|>` segment or delegate request, revising the unspoken continuation based on the new input while leaving already played audio unchanged."
- "We model interruptions as event-conditioned semantic control and jointly supervise the state transition and subsequent generation trajectory." "The stop/reject action closes the turn and discards its unspoken remainder; repair/update incorporates new evidence and regenerates the stale continuation; and redirect/follow-up suspends the current plan and transfers control to a new request." "A shared semantic state across turn control, text, speech, and delegate generation enables acoustically similar overlaps to produce distinct continuations, supporting native full-duplex control beyond binary reactions triggered by voice activity detection (VAD)."

## 4.5 Training data
**Covers:** Sec. 4.5 and Table 1

"Realtime-Venus-Omni and Realtime-Venus-Audio are trained on a common post-training corpus of over 2.8 million samples covering nine data categories, summarized in Table 1." "The corpus is organized into video and audio data. Realtime-Venus-Omni uses both modalities, while Realtime-Venus-Audio is trained only on audio data." "The data cover three main capabilities: offline understanding, including general audio–visual understanding, general audio understanding, and spoken question answering; proactive duplex interaction, including visual-, multimodal-, speech-, and audio-driven interaction with response timing and interruption handling; and delegation, which trains the delegate–backend–restate workflow described in Section 5."

> "Table 1 Training data composition."

| Modality | Category | Size | Role |
|---|---|---|---|
| Video | General AV understanding | 936k | offline AV comprehension |
| Video | Visual-proactive duplex | 454k | visually triggered proactivity |
| Video | Omni-proactive duplex | 201k | multimodal proactive interaction |
| Video | Speech-in duplex | 315k | proactive response to in-stream spoken queries |
| Video | Delegate | 95k | delegate–backend–restate |
| Audio | General audio understanding | 470k | offline audio comprehension |
| Audio | Spoken question answering | 205k | offline spoken question answering |
| Audio | Speech-only duplex | 100k | full-duplex interaction and interruption handling |
| Audio | Delegate | 90k | audio delegation |

"By modality, the video group constitutes approximately 70% of the corpus and is consumed exclusively by Realtime-Venus-Omni, whereas the audio group accounts for approximately 30% and is shared by Realtime-Venus-Omni and Realtime-Venus-Audio." "Offline understanding represents approximately 56% of the corpus, proactive duplex interaction accounts for approximately 37%, and delegation workflows comprise the remaining 6%." "Both duplex and delegation sources contain sessions with interruptions, so overlapping speech is supervised as part of ordinary interaction rather than through a separate module." "Section 6 describes how the full-duplex and delegate datasets are constructed." "Training uses this mixture under the unified recipe described in Section 4.6."

**Covers:** Fig. 6 + Sec. 4.3 streams/serialization/control tokens/Eq. (2) + Sec. 4.4/Eq. (3)/overlap cases + Sec. 4.5/Table 1; pp. 9–11 in chunk pagination.
