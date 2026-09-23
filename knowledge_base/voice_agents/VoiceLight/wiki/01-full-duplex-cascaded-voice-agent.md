> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Voice-Light: A Full-Duplex Cascaded Voice Agent
**In one sentence:** Voice-Light is a full-duplex cascaded (ASR → LLM → TTS) voice agent whose central rule is that uncertain work may begin early but may become audible or durable only after explicit causal checks, combining immediate acoustic onset, a causal adapter sharing a streaming ASR encoder, reversible playback control, and private speculative generation.
## Key points
- Full duplex means microphone ingestion continues during assistant playback, playback can react reversibly to detected user speech, and generation, synthesis, and acknowledged audio are managed concurrently.
- The system retains a cascaded architecture because its boundaries expose typed tools, playback state, and cancellation.
- Design rule: uncertain work may begin early, but it may become audible or durable only after explicit causal checks; conversation history must contain only speech acknowledged by the listener's browser.
- Structured tool calls execute concurrently with audible bridge speech, while browser acknowledgments make rendered audio authoritative for durable history.
- Locked evaluation on 1,673 real-conversation silence candidates found an earlier learned completion checkpoint preserved a 2.70% false-cutoff rate but reached only 12.53% end-of-turn recall, compared with 95.60% for a Silero timing policy, so the deployed system retains a hybrid controller.
- Across three unscripted operator-run microphone sessions, 36 measured response turns had a 758 ms median from final VAD endpoint to first server audio, with 21 turns below 800 ms; these sessions are an instrumented case study, not a controlled user evaluation.
- The paper frames its contributions as systems and evaluation contributions only, explicitly not claiming a new state-of-the-art adapter, general tool competence from synthetic evaluation, or population-level interaction quality estimates.
---
## Abstract
**Covers:** Abstract (p. 1)

Natural spoken interaction requires more than streaming ASR, language generation, and speech synthesis: a system must react to overlap without canceling on every acknowledgment, prepare a response before a turn is certain, and ensure canceled audio cannot enter conversation history.

Voice-Light combines:

- immediate acoustic onset,
- a causal adapter sharing a streaming ASR encoder,
- reversible playback control,
- private speculative response generation.

| Reported result | Value |
|---|---|
| Locked evaluation size | 1,673 real-conversation silence candidates |
| Learned completion checkpoint false-cutoff rate | 2.70% |
| Learned completion checkpoint end-of-turn recall | 12.53% |
| Silero timing policy end-of-turn recall | 95.60% |
| Deployed decision | hybrid controller retained; no learned-policy replacement claimed |
| Latency case study | 3 unscripted operator-run microphone sessions, 36 measured response turns |
| Median final-VAD-endpoint to first-server-audio | 758 ms |
| Turns below 800 ms | 21 / 36 |

> "These sessions are an instrumented case study, not a controlled user evaluation."

Released artifacts: synthetic data, model artifacts, evaluation code and summaries, source code, and deployment configuration supporting the result.

Keywords: streaming voice agents, turn-taking, synthetic data, causal streaming inference, speech synthesis, tool use, deployment

## Introduction
**Covers:** §1 Introduction (p. 1)

A conventional assistant is drawn as a serial pipeline — ASR, then language model, then TTS — but that abstraction hides the interaction problem: deciding whether a silence is a completed turn or a within-turn hesitation, reacting immediately when speech begins during playback without canceling on every short acknowledgment, ensuring canceled audio cannot reappear, and distinguishing generated text from speech that actually reached the listener.

Three research questions:

1. Can a small causal adapter reuse features from a persistent streaming ASR encoder and improve turn commitment over deployable timing baselines?
2. Can a reversible controller exploit uncertain evidence without turning every VAD onset into cancellation?
3. How much response latency can private speculation hide in a deployed ASR–LLM–TTS cascade?

Four scoped contributions:

- a shared-encoder causal turn-taking adapter, together with locked evaluations reporting both the learned signal and its failure to replace stronger timing baselines;
- a typed hybrid controller for reversible ducking, floor-taking, interruption, backchannel resumption, stale-generation rejection, and audible-only history;
- private speculative generation integrated with streaming ASR, Qwen, Kyutai TTS, and sequential tool rounds in a public scale-to-zero deployment;
- released synthetic tool-use and turn-taking corpora, trained artifacts, evaluation code and result summaries, and an instrumented 36-turn latency case study.

> "The contributions are systems and evaluation contributions. The paper does not claim that the adapter is a new state of the art, that synthetic evaluation measures general tool competence, or that the microphone sessions estimate population-level interaction quality."

## Related work (opening) and runtime figure
**Covers:** §2 Related work opening (p. 1) + Figure 1 caption

- Turn-taking and endpointing: TurnGPT predicts turn completion from text; Voice Activity Projection (VAP) predicts future speaker activity directly from conversational audio; acoustic–language-model fusion shows lexical and prosodic evidence can be complementary; recent turn benchmarks emphasize endpointing, backchannels, and interruption vary with conversation type. Voice-Light does not propose a general turn-taking architecture.
- Full-duplex spoken agents: end-to-end systems such as Moshi jointly model user and assistant speech and avoid explicit ASR–LLM–TTS boundaries. A cascade instead exposes intermediate text, typed tools, playback state, and component failures; Voice-Light uses those boundaries to make overlap reversible, reject stale work, and construct history from acknowledged audio.
- Figure 1 (Production runtime): browser microphone 16 kHz PCM → Silero onset with reversible duck + streaming Nemotron ASR with shared encoder taps → causal adapter (completion / floor / feedback) + hybrid commitment and speculation policy → Qwen3-4B with typed tools, dedicated GPU Kyutai TTS, and browser playback clock and acknowledgments. Caption verbatim: "Immediate acoustic reaction and learned interaction evidence meet at a typed controller. Tool calls and results use a structured loop; acknowledged browser playback is authoritative for durable assistant history."

**Covers:** Abstract + §1 Introduction + §2 Related work (opening: turn-taking/endpointing and full-duplex agents) + Figure 1, arXiv:2609.20995v1 [cs.SD] 17 Sep 2026
