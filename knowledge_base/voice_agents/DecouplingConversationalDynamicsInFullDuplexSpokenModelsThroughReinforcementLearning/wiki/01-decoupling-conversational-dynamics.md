> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Decoupling Conversational Dynamics in Full-Duplex Spoken Models
**In one sentence:** The chunk argues the intelligence–dynamics trade-off in full-duplex spoken models is not fundamental and proposes DuplexPO, an RL framework that decouples when to speak from what to say and optimizes timing behavior with a Factorized Conversational Dynamics Reward plus a GRPO-style objective.
## Key points
- Full-duplex models enable simultaneous listening and speaking with low latency, backchannels, and barge-in handling, but perform substantially worse than half-duplex counterparts on instruction-following and reasoning benchmarks.
- The trade-off is analyzed at the modeling level: long structured decoding for reasoning conflicts with fragmented, rapidly changing contexts requiring local real-time speak/pause/silence decisions that bias toward short-range states.
- The trade-off is analyzed at the data level: SFT on human dialogue corpora such as Fisher teaches interaction patterns but is dominated by casual, non-goal-oriented exchanges misaligned with a helpful instruction-following assistant.
- Central hypothesis: by optimizing only real-time floor-control decisions (turn-taking, backchanneling, yielding), a model can improve dynamics while preserving instruction-following and reasoning.
- DuplexPO samples dynamics-critical windows (turn transitions, backchannels, barge-ins) from long multi-turn human conversations and trains on-policy under the model's own response distribution rather than imitating heterogeneous corpora.
- The reward signal is the Factorized Conversational Dynamics Reward (FCDR) for turn initiation, backchanneling, yielding, and regularized participation, optimized with a GRPO-style objective regularized toward the reference SFT model.
- Higher dynamics scores are claimed to translate into user-perceived naturalness, responsiveness, and temporal coordination; demo page at https://liyuxin44.github.io/DuplexPO/.
---
## Abstract
**Covers:** Title, authors, arXiv:2607.07148v1 [eess.AS] 8 Jul 2026, Abstract paragraph

Paper: "Decoupling Conversational Dynamics in Full-Duplex Spoken Models through Reinforcement Learning" — Yuxin Li, Donghang Wu (Nanyang Technological University); Guan-Ting Lin, Hung-yi Lee (National Taiwan University); Chengwei Qin (The Hong Kong University of Science and Technology); Zhehuai Chen, Chen Chen (NVIDIA).

Verbatim core claims:
- "conversational dynamics can instead be learned as a separate real-time decision policy from human dialogue data."
- "we propose DuplexPO, a reinforcement learning (RL) framework that decouples when to speak from what to say."
- "we formulate the Factorized Conversational Dynamics Reward (FCDR) to enable fine-grained temporal credit assignment for turn initiation, backchanneling, yielding, and regularized participation."
- "Experiments show that DuplexPO substantially improves full-duplex behaviors, including timely backchannels, smooth turn-taking, and barge-in handling, while maintaining strong reasoning and instruction-following performance."

## 1 Introduction
**Covers:** §1 Introduction (full)

- Speech is framed as the most natural modality for human-computer interaction; end-to-end spoken dialogue models are the paradigm for interactive helpful voice agents.
- Full-duplex models process incoming user speech while generating responses, enabling barge-in handling and timely backchannels — more responsive and human-like than turn-based approaches.
- Coupling "what to say" (semantic content, target of instruction tuning) with "when to speak" (temporal floor control) in one objective is diagnosed as the source of the conflict; the chunk states full-duplex dynamics "need not be relearned by imitating complete natural dialogue responses."
- Operationalization: sample dynamic-critical windows from long conversations, compute FCDR maps, optimize with a GRPO-style objective regularized toward the reference SFT model to limit drift and retain instruction-tuned semantics.
- Follows "the broader principle of targeted speech-specific alignment, where auxiliary speech capabilities are learned without replacing the model's general language capability."

## 2.1 Full-Duplex Dialogue: Systems vs. Models (opening only)
**Covers:** §2.1 opening paragraphs (chunk cuts off mid-section at figure labels)

- Traditional systems decompose interaction into recognition, dialogue management, incremental processing, and synthesis modules; full-duplexity is "best understood as a functional property rather than a single architecture."
- A system can get full-duplexity via external orchestration (VAD or dialogue-management control), while a model can internalize it as part of generation.
- Figure "DuplexPO" labels visible in chunk: "Backchannel", "Turn Taking & Barge in", "Streaming Speech Encoder", "Decoder-only LLM (Policy Model)", "Text Projector", numbered markers ① ② ③, token sequences `<bos> T1 T <eos>` and `<bos>T1 T2 T3 T4 <PAD> <eos>` — figure body itself is truncated in the chunk, so no further claims are recorded.
